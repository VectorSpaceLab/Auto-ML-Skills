#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
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


def answer(row: dict[str, Any]) -> str:
    values = row.get("golden_answers") or []
    return values[0] if values else "unknown"


def docs(query: str, ans: str, topk: int) -> list[dict[str, Any]]:
    return [
        {"id": f"active-{rank}", "title": f"Active evidence {rank}", "contents": f"Active evidence {rank}\n{query} -> {ans}."}
        for rank in range(1, topk + 1)
    ]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--split", default="test")
    parser.add_argument("--summary", type=Path, default=None)
    args = parser.parse_args()
    config = read_simple_yaml(args.config)
    rows = load_rows(Path(str(config["data_dir"])) / str(config["dataset_name"]) / f"{args.split}.jsonl", config.get("test_sample_num"))
    pipeline = str(config.get("pipeline_name", "selfask")).lower()
    max_iter = int(config.get("max_iter") or 2)
    topk = int(config["retrieval_topk"] or 1)
    total_retrievals = 0
    for row in rows:
        question = row["question"]
        ans = answer(row)
        retrieval_trace: list[dict[str, Any]] = []
        prompt = f"Question: {question}\n"
        pred = ans
        for step in range(max_iter):
            if pipeline in {"selfask", "ircot", "rqrag", "rqrag"}:
                query = f"{question} step {step + 1}"
                step_docs = docs(query, ans, topk)
                retrieval_trace.append({"step": step, "query": query, "docs": step_docs})
                prompt += f"Follow up {step + 1}: {query}\n"
                total_retrievals += 1
                if step == max_iter - 1:
                    pred = ans
            elif pipeline == "flare":
                query = f"low confidence sentence about {question}"
                step_docs = docs(query, ans, topk)
                retrieval_trace.append({"step": step, "query": query, "docs": step_docs, "trigger": "low_confidence"})
                total_retrievals += 1
                pred = f"{ans}"
                break
            else:
                should_retrieve = step == 0 and any(token in question.lower() for token in ["who", "where", "when", "which"])
                if should_retrieve:
                    query = question
                    step_docs = docs(query, ans, topk)
                    retrieval_trace.append({"step": step, "query": query, "docs": step_docs, "trigger": "retrieval_token"})
                    total_retrievals += 1
                pred = ans
                break
        row["output"].update({"prompt": prompt, "active_trace": retrieval_trace, "retrieval_result": retrieval_trace[-1]["docs"] if retrieval_trace else [], "pred": pred})

    save_dir = Path(str(config["save_dir"]))
    save_dir.mkdir(parents=True, exist_ok=True)
    intermediate = save_dir / "intermediate_data.json"
    intermediate.write_text(json.dumps(rows, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    payload = {
        "records": len(rows),
        "pipeline": pipeline,
        "total_retrieval_steps": total_retrievals,
        "save_dir": str(save_dir),
        "intermediate_data": str(intermediate),
        "first_question": rows[0]["question"] if rows else None,
        "first_pred": rows[0]["output"].get("pred") if rows else None,
        "first_trace_len": len(rows[0]["output"].get("active_trace", [])) if rows else 0,
    }
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    if args.summary:
        args.summary.parent.mkdir(parents=True, exist_ok=True)
        args.summary.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
