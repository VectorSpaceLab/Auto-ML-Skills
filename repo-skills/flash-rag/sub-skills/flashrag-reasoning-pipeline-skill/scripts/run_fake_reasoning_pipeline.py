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


def docs(query: str, ans: str, topk: int) -> list[dict]:
    return [
        {"id": f"reason-{rank}", "title": f"Reasoning evidence {rank}", "contents": f"Reasoning evidence {rank}\n{query}: {ans}."}
        for rank in range(1, topk + 1)
    ]


def query_tags(pipeline: str) -> tuple[str, str, str, str]:
    if pipeline == "simple-deepsearcher":
        return "<|begin_search_query|>", "<|end_search_query|>", "<|begin_search_result|>", "<|end_search_result|>"
    if pipeline in {"searchr1", "autorefine", "o2searcher"}:
        return "<search>", "</search>", "<information>", "</information>"
    return "<|begin_of_query|>", "<|end_of_query|>", "<|begin_of_documents|>", "<|end_of_documents|>"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--split", default="test")
    parser.add_argument("--summary", type=Path, default=None)
    args = parser.parse_args()
    config = read_simple_yaml(args.config)
    rows = load_rows(Path(str(config["data_dir"])) / str(config["dataset_name"]) / f"{args.split}.jsonl", config.get("test_sample_num"))
    pipeline = str(config.get("pipeline_name", "reasoning")).lower()
    max_steps = int(config.get("max_retrieval_num") or 2)
    topk = int(config.get("retrieval_topk") or 1)
    q0, q1, d0, d1 = query_tags(pipeline)
    total_queries = 0
    for row in rows:
        question = row["question"]
        ans = answer(row)
        prompt = f"User:{question}\nAssistant:<think>"
        trace = []
        for step in range(max_steps):
            query = f"{question} evidence step {step + 1}"
            step_docs = docs(query, ans, topk)
            prompt += f"{q0}{query}{q1}\n{d0}\n"
            prompt += "\n".join(doc["contents"] for doc in step_docs)
            prompt += f"\n{d1}\n"
            trace.append({"step": step, "query": query, "docs": step_docs})
            total_queries += 1
            if step == 0:
                break
        if pipeline == "simple-deepsearcher":
            pred = ans
            prompt += f"Final reasoning. \\boxed{{{ans}}}"
        else:
            pred = ans
            prompt += f"</think>\n<answer>{ans}</answer>"
        row["output"].update({"prompt": prompt, "reasoning_trace": trace, "retrieval_results": {str(i): item for i, item in enumerate(trace)}, "retrieval_result": trace[-1]["docs"] if trace else [], "pred": pred, "finish_flag": True})

    save_dir = Path(str(config["save_dir"]))
    save_dir.mkdir(parents=True, exist_ok=True)
    intermediate = save_dir / "intermediate_data.json"
    intermediate.write_text(json.dumps(rows, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    payload = {
        "records": len(rows),
        "pipeline": pipeline,
        "total_queries": total_queries,
        "save_dir": str(save_dir),
        "intermediate_data": str(intermediate),
        "first_question": rows[0]["question"] if rows else None,
        "first_pred": rows[0]["output"].get("pred") if rows else None,
        "first_trace_len": len(rows[0]["output"].get("reasoning_trace", [])) if rows else 0,
    }
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    if args.summary:
        args.summary.parent.mkdir(parents=True, exist_ok=True)
        args.summary.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
