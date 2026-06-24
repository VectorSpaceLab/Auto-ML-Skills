#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import sys
from importlib.machinery import ModuleSpec
from types import ModuleType
from pathlib import Path
from typing import Any

from doc_utils import load_docs, validate_docs


def terms(text: str) -> set[str]:
    return {token for token in re.findall(r"[A-Za-z0-9]+", text.lower()) if len(token) > 2}


def split_sentences(text: str) -> list[str]:
    return [item.strip() for item in re.split(r"(?<![A-Za-z]\.)(?<=[.!?])\s+", text) if len(item.strip()) > 5]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--package-root", type=Path, default=None, help="Optional installed package root to add to PYTHONPATH.")
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--question", required=True)
    parser.add_argument("--docs", type=Path, required=True)
    parser.add_argument("--result-index", type=int, default=0)
    parser.add_argument("--jsonl-limit", type=int, default=None)
    parser.add_argument("--topk-sentences", type=int, default=4)
    parser.add_argument("--max-chars", type=int, default=1200)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    docs = load_docs(args.docs, result_index=args.result_index, jsonl_limit=args.jsonl_limit)
    errors = validate_docs(docs)
    if errors:
        raise ValueError("; ".join(errors[:5]))

    if args.package_root is not None:
        sys.path.insert(0, str(args.package_root.resolve()))
    if "faiss" not in sys.modules:
        faiss = ModuleType("faiss")
        faiss.__spec__ = ModuleSpec("faiss", loader=None)
        faiss.omp_set_num_threads = lambda *_args, **_kwargs: None
        sys.modules["faiss"] = faiss
    if "langid" not in sys.modules:
        langid = ModuleType("langid")
        langid.__spec__ = ModuleSpec("langid", loader=None)
        langid.classify = lambda _text: ("en", 1.0)
        sys.modules["langid"] = langid
    from flashrag.config import Config
    from flashrag.dataset import Dataset
    from flashrag.prompt import PromptTemplate
    from flashrag.refiner.refiner import BaseRefiner

    class LexicalOverlapRefiner(BaseRefiner):
        def __init__(self, config):
            super().__init__(config)

        def run(self, item) -> str:
            question_terms = terms(item.question)
            candidates: list[tuple[int, float, str]] = []
            serial = 0
            for doc in item.retrieval_result:
                contents = str(doc.get("contents", ""))
                body = "\n".join(contents.splitlines()[1:]) if "\n" in contents else contents
                for sentence in split_sentences(body):
                    sentence_terms = terms(sentence)
                    overlap = len(question_terms & sentence_terms)
                    score = overlap / max(1, len(question_terms))
                    candidates.append((serial, score, sentence))
                    serial += 1
            if not candidates:
                return ""
            top = sorted(candidates, key=lambda item_: (-item_[1], item_[0]))[: args.topk_sentences]
            ordered = sorted(top, key=lambda item_: item_[0])
            compressed = " ".join(sentence for _, _, sentence in ordered)
            return compressed[: args.max_chars]

    config = Config(str(args.config))
    dataset = Dataset(
        config=config,
        data=[
            {
                "id": "offline-refiner-0",
                "question": args.question,
                "golden_answers": [],
                "retrieval_result": docs,
            }
        ],
    )
    refiner = LexicalOverlapRefiner(config)
    compressed_reference = refiner.batch_run(dataset)[0]
    template = PromptTemplate(config)
    prompt = template.get_string(question=args.question, formatted_reference=compressed_reference)
    payload: dict[str, Any] = {
        "question": args.question,
        "doc_count": len(docs),
        "compressed_reference": compressed_reference,
        "prompt": prompt,
        "prompt_type": "messages" if isinstance(prompt, list) else "text",
        "topk_sentences": args.topk_sentences,
        "max_input_len": config["generator_max_input_len"],
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"output": str(args.output), "doc_count": len(docs), "compressed_chars": len(compressed_reference)}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
