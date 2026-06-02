#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


def score_doc(query: str, doc: dict) -> float:
    if "score" in doc:
        try:
            return float(doc["score"])
        except Exception:
            pass
    q = set(re.findall(r"\w+", query.lower()))
    d = set(re.findall(r"\w+", str(doc.get("contents", "")).lower()))
    return len(q & d) / max(1, len(q))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--topk", type=int, default=5)
    args = parser.parse_args()
    payload = json.loads(args.input.read_text(encoding="utf-8"))
    query = payload.get("query", "")
    docs = payload.get("docs") or payload.get("retrieval_result") or []
    reranked = sorted(docs, key=lambda d: score_doc(query, d), reverse=True)[: args.topk]
    out = {"query": query, "docs": reranked}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"docs": len(reranked), "output": str(args.output)}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
