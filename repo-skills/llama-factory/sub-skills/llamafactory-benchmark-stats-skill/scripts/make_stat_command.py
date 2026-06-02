#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path


UTILITY_MAP = {
    "length-cdf": "length-cdf-utility",
    "flops": "flops-utility",
    "mfu": "mfu-utility",
    "ppl": "ppl-utility",
    "lr": "lr-utility",
    "bench-qwen": "scripts/bench_qwen.py",
}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--task", choices=sorted(UTILITY_MAP), required=True)
    parser.add_argument("--model", default=None)
    parser.add_argument("--dataset", default="alpaca_en_demo")
    parser.add_argument("--dataset-dir", default="data")
    parser.add_argument("--template", default="qwen3_nothink")
    parser.add_argument("--batch-size", type=int, default=1)
    parser.add_argument("--seq-length", type=int, default=512)
    parser.add_argument("--num-steps", type=int, default=10)
    parser.add_argument("--extra-args", nargs=argparse.REMAINDER, default=[])
    args = parser.parse_args()

    utility = UTILITY_MAP[args.task]
    cmd = ["python", f"<vendored-skill-or-project-script>/{utility}"]
    if args.task == "length-cdf":
        cmd.extend(
            [
                "--model_name_or_path",
                str(args.model),
                "--dataset",
                args.dataset,
                "--dataset_dir",
                args.dataset_dir,
                "--template",
                args.template,
            ]
        )
    elif args.task == "flops":
        cmd.extend(["--model_name_or_path", str(args.model), "--batch_size", str(args.batch_size), "--seq_length", str(args.seq_length)])
    elif args.task == "mfu":
        cmd.extend(
            [
                "--model_name_or_path",
                str(args.model),
                "--batch_size",
                str(args.batch_size),
                "--seq_length",
                str(args.seq_length),
                "--num_steps",
                str(args.num_steps),
            ]
        )
    elif args.task == "bench-qwen":
        cmd.extend(["--model_name_or_path", str(args.model), "--batch_size", str(args.batch_size), "--seq_length", str(args.seq_length)])
    else:
        cmd.extend(args.extra_args)
    payload = {
        "task": args.task,
        "utility": utility,
        "model": args.model,
        "dataset": args.dataset,
        "dataset_dir": args.dataset_dir,
        "command": cmd,
        "note": "This utility is a public LLaMA-Factory repo script, not a stable installed-package CLI. Vendor/adapt the utility before execution, or use the bundled estimate_mfu.py for lightweight local estimates.",
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(args.output)
    print(" ".join(cmd))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
