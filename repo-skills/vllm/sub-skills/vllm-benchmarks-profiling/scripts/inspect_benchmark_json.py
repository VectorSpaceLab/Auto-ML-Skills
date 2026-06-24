#!/usr/bin/env python3
"""Summarize vLLM benchmark JSON output."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


KEYS = [
    "request_throughput",
    "output_throughput",
    "total_token_throughput",
    "mean_ttft_ms",
    "median_ttft_ms",
    "mean_tpot_ms",
    "mean_itl_ms",
    "median_itl_ms",
    "completed",
    "duration",
]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("json_file")
    args = parser.parse_args()
    data = json.loads(Path(args.json_file).read_text(encoding="utf-8"))
    if isinstance(data, list):
        data = data[-1] if data else {}
    summary = {key: data.get(key) for key in KEYS if key in data}
    failed = data.get("failed", data.get("failed_requests"))
    if failed is not None:
        summary["failed"] = failed
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
