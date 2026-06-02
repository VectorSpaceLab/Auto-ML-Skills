#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "scripts"))
from fr_skill_common import read_simple_yaml


def load_questions(path: Path | None) -> list[str]:
    if path is None or not path.exists():
        return ["Who wrote Hamlet?", "What is 2+2?", "Where is the Eiffel Tower?"]
    rows = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
    return [str(row.get("question") or row.get("query") or row) for row in rows]


def route(kind: str, question: str) -> dict:
    q = question.lower()
    if kind == "adaptive-rag":
        label = "C" if "where" in q or "who" in q else "A"
        route_name = {"A": "no_retrieval", "B": "single_hop", "C": "multi_hop"}[label]
        return {"label": label, "route": route_name}
    judgement = "ir_better" if "who" in q or "where" in q else "ir_worse"
    return {"judgement": judgement, "retrieve": judgement == "ir_better"}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--questions", type=Path, default=None)
    parser.add_argument("--summary", type=Path, required=True)
    args = parser.parse_args()
    cfg = read_simple_yaml(args.config)
    questions = load_questions(args.questions)
    kind = str(cfg.get("judger_name", "skr"))
    rows = [{"question": q, **route(kind, q)} for q in questions]
    result = {"judger_name": kind, "records": rows, "count": len(rows)}
    args.summary.parent.mkdir(parents=True, exist_ok=True)
    args.summary.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, indent=2))
    print(f"valid: {str(bool(rows)).lower()}")
    return 0 if rows else 1


if __name__ == "__main__":
    raise SystemExit(main())
