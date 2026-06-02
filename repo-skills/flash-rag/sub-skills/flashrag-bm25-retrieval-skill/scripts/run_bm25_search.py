#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

from flashrag_import_stubs import install_optional_import_stubs


def load_queries(args: argparse.Namespace) -> list[str]:
    queries: list[str] = []
    if args.query:
        queries.append(args.query)
    if args.queries:
        queries.extend(line.strip() for line in args.queries.read_text(encoding="utf-8").splitlines() if line.strip())
    if not queries:
        raise ValueError("provide --query or --queries")
    return queries


def simplify_doc(doc: dict[str, Any]) -> dict[str, Any]:
    return {
        "id": doc.get("id"),
        "title": doc.get("title"),
        "contents": doc.get("contents"),
        "score": doc.get("score"),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--package-root", type=Path, default=None, help="Optional installed package root to add to PYTHONPATH.")
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--query", default=None)
    parser.add_argument("--queries", type=Path, default=None)
    parser.add_argument("--topk", type=int, default=None)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    queries = load_queries(args)
    if args.package_root is not None:
        sys.path.insert(0, str(args.package_root.resolve()))
    install_optional_import_stubs()
    from flashrag.config import Config
    from flashrag.utils import get_retriever

    config = Config(str(args.config))
    retriever = get_retriever(config)
    topk = args.topk or config["retrieval_topk"]

    docs, scores = retriever.batch_search(queries, num=topk, return_score=True)
    output = {
        "queries": queries,
        "topk": topk,
        "results": [
            {
                "query": query,
                "docs": [
                    {**simplify_doc(doc), "score": float(score)}
                    for doc, score in zip(query_docs, query_scores)
                ],
            }
            for query, query_docs, query_scores in zip(queries, docs, scores)
        ],
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(output, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"queries": len(queries), "output": str(args.output), "first_docs": len(output["results"][0]["docs"])}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
