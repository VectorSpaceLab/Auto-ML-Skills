#!/usr/bin/env python3
"""Sanity-check common SGLang performance options."""

import argparse
import json


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate common SGLang performance config choices.")
    parser.add_argument("--mem-fraction-static", type=float)
    parser.add_argument("--max-running-requests", type=int)
    parser.add_argument("--max-total-tokens", type=int)
    parser.add_argument("--chunked-prefill-size", type=int)
    parser.add_argument("--speculative-algorithm")
    parser.add_argument("--speculative-draft-model-path")
    parser.add_argument("--disable-radix-cache", action="store_true")
    args = parser.parse_args()
    issues = []
    if args.mem_fraction_static is not None and not (0 < args.mem_fraction_static <= 1):
        issues.append("--mem-fraction-static should be in (0, 1]")
    for name in ["max_running_requests", "max_total_tokens", "chunked_prefill_size"]:
        val = getattr(args, name)
        if val is not None and val <= 0:
            issues.append(f"--{name.replace('_', '-')} should be positive")
    if args.speculative_algorithm and not args.speculative_draft_model_path and args.speculative_algorithm.lower() not in {"ngram"}:
        issues.append("draft-model speculative algorithms usually need --speculative-draft-model-path")
    print(json.dumps({"ok": not issues, "issues": issues}, indent=2))
    return 1 if issues else 0


if __name__ == "__main__":
    raise SystemExit(main())
