#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path
from typing import Any

from common import env_for


def _parse_simple_yaml(path: Path) -> dict[str, Any]:
    data: dict[str, Any] = {}
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or ":" not in line:
            continue
        key, value = line.split(":", 1)
        value = value.strip()
        if value in {"true", "True"}:
            parsed: Any = True
        elif value in {"false", "False"}:
            parsed = False
        elif value in {"null", "None", "~"}:
            parsed = None
        elif (value.startswith("'") and value.endswith("'")) or (value.startswith('"') and value.endswith('"')):
            parsed = value[1:-1]
        else:
            try:
                parsed = int(value) if value.isdigit() else float(value)
            except ValueError:
                parsed = value
        data[key.strip()] = parsed
    return data


def main() -> int:
    parser = argparse.ArgumentParser(description="Run one LLaMA-Factory ChatModel request.")
    parser.add_argument("--package-root", type=Path, default=None, help="Optional installed package root to add to PYTHONPATH.")
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--prompt", required=True)
    parser.add_argument("--system", default=None)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--extra-pythonpath", action="append", default=[])
    parser.add_argument("--disable-version-check", action="store_true")
    parser.add_argument("--max-new-tokens", type=int, default=None)
    args = parser.parse_args()

    env = env_for(args.package_root, extra_pythonpath=args.extra_pythonpath)
    if args.disable_version_check:
        env["DISABLE_VERSION_CHECK"] = "1"
    os.environ.update(env)
    for path in env.get("PYTHONPATH", "").split(os.pathsep):
        if path and path not in sys.path:
            sys.path.insert(0, path)

    from llamafactory.chat import ChatModel

    model_args = _parse_simple_yaml(args.config)
    if args.max_new_tokens is not None:
        model_args["max_new_tokens"] = args.max_new_tokens
    chat_model = ChatModel(model_args)
    responses = chat_model.chat(
        [{"role": "user", "content": args.prompt}],
        system=args.system,
        max_new_tokens=model_args.get("max_new_tokens"),
        temperature=model_args.get("temperature"),
        top_p=model_args.get("top_p"),
        top_k=model_args.get("top_k"),
        do_sample=model_args.get("do_sample"),
    )
    rows = []
    for response in responses:
        rows.append(
            {
                "prompt": args.prompt,
                "response": response.response_text,
                "response_length": response.response_length,
                "prompt_length": response.prompt_length,
                "finish_reason": response.finish_reason,
            }
        )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text("\n".join(json.dumps(row, ensure_ascii=False) for row in rows) + "\n", encoding="utf-8")
    for row in rows:
        print(json.dumps(row, ensure_ascii=False))
    return 0 if rows and rows[0]["response"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
