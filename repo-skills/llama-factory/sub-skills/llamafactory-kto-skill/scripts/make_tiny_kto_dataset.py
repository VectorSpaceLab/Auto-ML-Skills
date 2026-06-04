#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from common import load_records


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Create a tiny registered ShareGPT KTO dataset with both label=true and label=false examples."
    )
    parser.add_argument("--source", type=Path, required=True, help="Source KTO JSON/JSONL file.")
    parser.add_argument("--output-dir", type=Path, required=True, help="Directory for dataset file and dataset_info.json.")
    parser.add_argument("--dataset-name", default="tiny_kto_demo")
    parser.add_argument("--records-per-label", type=int, default=1)
    args = parser.parse_args()

    rows = load_records(args.source)
    selected: list[dict[str, Any]] = []
    counts = {True: 0, False: 0}
    for row in rows:
        label = row.get("label")
        if isinstance(label, bool) and counts[label] < args.records_per_label:
            selected.append(row)
            counts[label] += 1
        if all(count >= args.records_per_label for count in counts.values()):
            break

    if any(count < args.records_per_label for count in counts.values()):
        raise SystemExit(
            "source dataset must contain at least "
            f"{args.records_per_label} true and {args.records_per_label} false KTO labels"
        )

    args.output_dir.mkdir(parents=True, exist_ok=True)
    data_file = args.output_dir / f"{args.dataset_name}.json"
    info_file = args.output_dir / "dataset_info.json"
    data_file.write_text(json.dumps(selected, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    info = {
        args.dataset_name: {
            "file_name": data_file.name,
            "formatting": "sharegpt",
            "columns": {"messages": "messages", "kto_tag": "label"},
            "tags": {
                "role_tag": "role",
                "content_tag": "content",
                "user_tag": "user",
                "assistant_tag": "assistant",
            },
        }
    }
    info_file.write_text(json.dumps(info, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"dataset_dir: {args.output_dir.resolve()}")
    print(f"dataset_name: {args.dataset_name}")
    print(f"records: {len(selected)}")
    print(f"label_true: {counts[True]}")
    print(f"label_false: {counts[False]}")
    print(f"data_file: {data_file}")
    print(f"dataset_info: {info_file}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
