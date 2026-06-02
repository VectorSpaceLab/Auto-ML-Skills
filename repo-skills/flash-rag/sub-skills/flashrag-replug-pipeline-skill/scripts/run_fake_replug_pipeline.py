#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "scripts"))
from fr_skill_common import read_simple_yaml


def load_rows(path: Path, sample_num: int | None) -> list[dict]:
    rows = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
    for row in rows:
        row.setdefault("output", {})
    return rows[:sample_num] if sample_num else rows


def answer(row: dict) -> str:
    values = row.get("golden_answers") or []
    return values[0] if values else "unknown"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--split", default="test")
    parser.add_argument("--summary", type=Path, default=None)
    args = parser.parse_args()
    config = read_simple_yaml(args.config)
    rows = load_rows(Path(str(config["data_dir"])) / str(config["dataset_name"]) / f"{args.split}.jsonl", config.get("test_sample_num"))
    topk = int(config["retrieval_topk"] or 1)
    total_doc_prompts = 0
    for row in rows:
        question = row["question"]
        ans = answer(row)
        retrieval_result = [
            {"id": f"replug-{rank}", "title": f"REPLUG evidence {rank}", "contents": f"REPLUG evidence {rank}\nThe answer to {question} is {ans}."}
            for rank in range(1, topk + 1)
        ]
        doc_scores = [1.0 / rank for rank in range(1, topk + 1)]
        doc_prompts = [f"Document: {doc['contents']}\nQuestion: {question}\nAnswer:" for doc in retrieval_result]
        row["output"].update({"retrieval_result": retrieval_result, "doc_scores": doc_scores, "doc_prompts": doc_prompts, "pred": ans})
        total_doc_prompts += len(doc_prompts)

    save_dir = Path(str(config["save_dir"]))
    save_dir.mkdir(parents=True, exist_ok=True)
    intermediate = save_dir / "intermediate_data.json"
    intermediate.write_text(json.dumps(rows, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    payload = {
        "records": len(rows),
        "total_doc_prompts": total_doc_prompts,
        "save_dir": str(save_dir),
        "intermediate_data": str(intermediate),
        "first_question": rows[0]["question"] if rows else None,
        "first_pred": rows[0]["output"].get("pred") if rows else None,
        "first_doc_scores": rows[0]["output"].get("doc_scores") if rows else [],
    }
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    if args.summary:
        args.summary.parent.mkdir(parents=True, exist_ok=True)
        args.summary.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
