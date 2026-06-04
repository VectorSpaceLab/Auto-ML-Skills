#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import shutil
from pathlib import Path
from typing import Any

from common import load_records


def _entry(args: argparse.Namespace, file_name: str) -> dict[str, Any]:
    item: dict[str, Any] = {"file_name": file_name}
    if args.format != "alpaca":
        item["formatting"] = args.format
    columns: dict[str, str] = {}
    tags: dict[str, str] = {}
    if args.format == "alpaca":
        columns = {"prompt": args.prompt_col, "query": args.query_col, "response": args.response_col}
        if args.system_col:
            columns["system"] = args.system_col
        if args.history_col:
            columns["history"] = args.history_col
    else:
        columns = {"messages": args.messages_col}
        tags = {
            "role_tag": args.role_tag,
            "content_tag": args.content_tag,
            "user_tag": args.user_tag,
            "assistant_tag": args.assistant_tag,
        }
    if args.ranking:
        item["ranking"] = True
        columns["chosen"] = args.chosen_col
        columns["rejected"] = args.rejected_col
    if args.kto:
        columns["kto_tag"] = args.kto_tag_col
    item["columns"] = columns
    if tags:
        item["tags"] = tags
    return item


def main() -> int:
    parser = argparse.ArgumentParser(description="Create a LLaMA-Factory dataset_dir with dataset_info.json.")
    parser.add_argument("--source", type=Path, required=True, help="Input .json or .jsonl data file.")
    parser.add_argument("--dataset-dir", type=Path, required=True)
    parser.add_argument("--dataset-name", required=True)
    parser.add_argument("--format", choices=["alpaca", "sharegpt", "openai"], default="alpaca")
    parser.add_argument("--copy", action="store_true", help="Copy source into dataset-dir instead of referencing it.")
    parser.add_argument("--max-records", type=int, default=None, help="Optionally write only the first N records.")
    parser.add_argument("--ranking", action="store_true", help="Register chosen/rejected pairwise data for RM/DPO.")
    parser.add_argument("--kto", action="store_true", help="Register boolean KTO labels.")
    parser.add_argument("--prompt-col", default="instruction")
    parser.add_argument("--query-col", default="input")
    parser.add_argument("--response-col", default="output")
    parser.add_argument("--system-col", default=None)
    parser.add_argument("--history-col", default=None)
    parser.add_argument("--messages-col", default="messages")
    parser.add_argument("--chosen-col", default="chosen")
    parser.add_argument("--rejected-col", default="rejected")
    parser.add_argument("--kto-tag-col", default="label")
    parser.add_argument("--role-tag", default="role")
    parser.add_argument("--content-tag", default="content")
    parser.add_argument("--user-tag", default="user")
    parser.add_argument("--assistant-tag", default="assistant")
    args = parser.parse_args()

    if not args.source.is_file():
        raise SystemExit(f"source file not found: {args.source}")

    args.dataset_dir.mkdir(parents=True, exist_ok=True)
    file_name = args.source.name
    target = args.dataset_dir / file_name
    if args.copy or args.max_records is not None:
        if args.max_records is None:
            shutil.copy2(args.source, target)
        else:
            rows = load_records(args.source)[: args.max_records]
            if args.source.suffix == ".jsonl":
                target.write_text(
                    "\n".join(json.dumps(row, ensure_ascii=False) for row in rows) + "\n",
                    encoding="utf-8",
                )
            else:
                target.write_text(json.dumps(rows, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        file_name = target.name

    info_path = args.dataset_dir / "dataset_info.json"
    info: dict[str, Any] = {}
    if info_path.exists():
        info = json.loads(info_path.read_text(encoding="utf-8"))
    info[args.dataset_name] = _entry(args, file_name)
    info_path.write_text(json.dumps(info, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(f"dataset_dir: {args.dataset_dir.resolve()}")
    print(f"dataset_name: {args.dataset_name}")
    print(f"dataset_info: {info_path}")
    print(f"data_file: {args.dataset_dir / file_name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
