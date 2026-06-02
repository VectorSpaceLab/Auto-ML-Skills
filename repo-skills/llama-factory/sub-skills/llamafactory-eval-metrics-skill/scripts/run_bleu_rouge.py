#!/usr/bin/env python3
from __future__ import annotations

import argparse
import sys
from pathlib import Path
import json
from collections import Counter


def tokenize(text: str) -> list[str]:
    return text.strip().split()


def overlap_f1(pred: str, label: str) -> dict[str, float]:
    pred_tokens = tokenize(pred)
    label_tokens = tokenize(label)
    if not pred_tokens or not label_tokens:
        return {"precision": 0.0, "recall": 0.0, "f1": 0.0}
    pred_counts = Counter(pred_tokens)
    label_counts = Counter(label_tokens)
    common = sum((pred_counts & label_counts).values())
    precision = common / len(pred_tokens)
    recall = common / len(label_tokens)
    f1 = 0.0 if precision + recall == 0 else 2 * precision * recall / (precision + recall)
    return {"precision": precision, "recall": recall, "f1": f1}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--predictions", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--log", type=Path, default=None)
    args = parser.parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)
    rows = [json.loads(line) for line in args.predictions.read_text(encoding="utf-8").splitlines() if line.strip()]
    scores = []
    for row in rows:
        pred = str(row.get("predict") or row.get("prediction") or row.get("pred") or "")
        label = str(row.get("label") or row.get("answer") or row.get("target") or "")
        scores.append(overlap_f1(pred, label))
    summary = {
        "records": len(rows),
        "token_overlap_precision": sum(s["precision"] for s in scores) / max(1, len(scores)),
        "token_overlap_recall": sum(s["recall"] for s in scores) / max(1, len(scores)),
        "token_overlap_f1": sum(s["f1"] for s in scores) / max(1, len(scores)),
        "note": "Lightweight self-contained proxy; use task-specific BLEU/ROUGE libraries when exact published metrics are required.",
    }
    out = args.output_dir / "metrics.json"
    out.write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
