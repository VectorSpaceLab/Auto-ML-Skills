#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "scripts"))
from fr_skill_common import read_simple_yaml


def load_rows(path: Path, sample_num: int | None) -> list[dict[str, Any]]:
    rows = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
    for row in rows:
        row.setdefault("output", {})
    return rows[:sample_num] if sample_num else rows


def answer_for(row: dict[str, Any]) -> str:
    answers = row.get("golden_answers") or []
    return answers[0] if answers else "unknown"


def retrieve(question: str, answer: str, topk: int) -> list[dict[str, Any]]:
    return [
        {
            "id": f"cond-{rank}",
            "title": f"Conditional evidence {rank}",
            "contents": f"Conditional evidence {rank}\nThe answer to {question} is {answer}.",
        }
        for rank in range(1, topk + 1)
    ]


def route_binary(question: str, idx: int) -> bool:
    text = question.lower()
    if any(token in text for token in ["who", "when", "where", "which", "cite", "evidence"]):
        return True
    return idx % 2 == 0


def route_adaptive(question: str, idx: int) -> str:
    text = question.lower()
    if any(token in text for token in ["compare", "both", "multi", "why"]):
        return "C"
    if route_binary(question, idx):
        return "B"
    return "A"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--split", default="test")
    parser.add_argument("--summary", type=Path, default=None)
    args = parser.parse_args()

    config = read_simple_yaml(args.config)
    dataset_path = Path(str(config["data_dir"])) / str(config["dataset_name"]) / f"{args.split}.jsonl"
    if not dataset_path.is_file():
        raise FileNotFoundError(dataset_path)
    rows = load_rows(dataset_path, config.get("test_sample_num"))
    topk = int(config.get("retrieval_topk") or 1)
    pipeline_name = config.get("pipeline_name", "conditional")
    route_counts: dict[str, int] = {}

    for idx, row in enumerate(rows):
        question = row["question"]
        answer = answer_for(row)
        if pipeline_name == "adaptive":
            route = route_adaptive(question, idx)
            use_retrieval = route in {"B", "C"}
        else:
            use_retrieval = route_binary(question, idx)
            route = str(use_retrieval)
        docs = retrieve(question, answer, topk) if use_retrieval else []
        prompt = f"Question: {question}\n"
        if docs:
            prompt += "\n".join(doc["contents"] for doc in docs) + "\n"
        if route == "C":
            pred = f"reasoned multi-hop answer: {answer}"
        else:
            pred = answer if answer != "unknown" else re.sub(r"\\?$", "", question)
        row["output"].update({"judge_result": route, "retrieval_result": docs, "prompt": prompt, "pred": pred})
        route_counts[route] = route_counts.get(route, 0) + 1

    save_dir = Path(str(config["save_dir"]))
    save_dir.mkdir(parents=True, exist_ok=True)
    intermediate = save_dir / "intermediate_data.json"
    intermediate.write_text(json.dumps(rows, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    payload = {
        "records": len(rows),
        "pipeline": pipeline_name,
        "route_counts": route_counts,
        "save_dir": str(save_dir),
        "intermediate_data": str(intermediate),
        "first_question": rows[0]["question"] if rows else None,
        "first_route": rows[0]["output"].get("judge_result") if rows else None,
        "first_pred": rows[0]["output"].get("pred") if rows else None,
        "first_retrieved": len(rows[0]["output"].get("retrieval_result", [])) if rows else 0,
    }
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    if args.summary:
        args.summary.parent.mkdir(parents=True, exist_ok=True)
        args.summary.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
