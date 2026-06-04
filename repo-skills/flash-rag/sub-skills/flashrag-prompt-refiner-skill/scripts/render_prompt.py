#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from doc_utils import load_docs, validate_docs


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--package-root", type=Path, default=None, help="Optional installed package root to add to PYTHONPATH.")
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--question", required=True)
    parser.add_argument("--docs", type=Path, required=True)
    parser.add_argument("--result-index", type=int, default=0)
    parser.add_argument("--jsonl-limit", type=int, default=None)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--system-prompt", default="")
    parser.add_argument("--user-prompt", default="")
    parser.add_argument("--reference-template", default=None)
    parser.add_argument("--no-chat", action="store_true")
    args = parser.parse_args()

    docs = load_docs(args.docs, result_index=args.result_index, jsonl_limit=args.jsonl_limit)
    errors = validate_docs(docs)
    if errors:
        raise ValueError("; ".join(errors[:5]))

    if args.package_root is not None:
        sys.path.insert(0, str(args.package_root.resolve()))
    from flashrag.config import Config
    from flashrag.prompt import PromptTemplate

    config = Config(str(args.config))
    template = PromptTemplate(
        config,
        system_prompt=args.system_prompt,
        user_prompt=args.user_prompt,
        reference_template=args.reference_template,
        enable_chat=not args.no_chat,
    )
    formatted_reference = template.format_reference(docs)
    prompt = template.get_string(question=args.question, retrieval_result=docs)
    payload = {
        "question": args.question,
        "doc_count": len(docs),
        "formatted_reference": formatted_reference,
        "prompt": prompt,
        "prompt_type": "messages" if isinstance(prompt, list) else "text",
        "max_input_len": config["generator_max_input_len"],
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"output": str(args.output), "doc_count": len(docs), "prompt_type": payload["prompt_type"]}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
