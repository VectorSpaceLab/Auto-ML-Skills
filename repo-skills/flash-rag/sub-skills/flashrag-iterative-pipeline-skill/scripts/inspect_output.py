#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--summary", type=Path, default=None)
    parser.add_argument("--output-dir", type=Path, default=None)
    parser.add_argument("--iter-num", type=int, default=2)
    args = parser.parse_args()
    if args.summary:
        if not args.summary.is_file():
            print("valid: false")
            print("- summary is missing")
            return 1
        payload = json.loads(args.summary.read_text(encoding="utf-8"))
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        ok = payload.get("records", 0) > 0 and payload.get("iterations", args.iter_num) >= 1
        print(f"valid: {str(bool(ok)).lower()}")
        return 0 if ok else 1

    if args.output_dir is None:
        print("valid: false")
        print("- provide --summary or --output-dir")
        return 1
    errors: list[str] = []
    output_dir = args.output_dir
    print(f"output_dir: {output_dir.resolve()}")
    if not output_dir.is_dir():
        print("valid: false")
        print("- output_dir is missing")
        return 1
    names = {path.name for path in output_dir.iterdir()}
    for name in sorted(names):
        print(f"- {name}")
    required = {"config.yaml", "metric_score.txt", "intermediate_data.json"}
    missing = required - names
    if missing:
        errors.append(f"missing files: {sorted(missing)}")
    metric_path = output_dir / "metric_score.txt"
    if metric_path.exists():
        print(metric_path.read_text(encoding="utf-8").strip())
    data_path = output_dir / "intermediate_data.json"
    if data_path.exists():
        rows = json.loads(data_path.read_text(encoding="utf-8"))
        print(f"records: {len(rows)}")
        if not rows:
            errors.append("intermediate_data.json is empty")
        else:
            output = rows[0].get("output", {})
            required_keys = ["retrieval_result", "pred", "metric_score"]
            for idx in range(args.iter_num):
                required_keys.extend([f"retrieval_result_iter_{idx}", f"prompt_iter_{idx}", f"pred_iter_{idx}"])
            for key in required_keys:
                present = key in output
                print(f"first_output_has_{key}: {str(present).lower()}")
                if not present:
                    errors.append(f"first record missing output.{key}")
    if errors:
        print("valid: false")
        for error in errors:
            print(f"- {error}")
        return 1
    print("valid: true")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
