#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--kind", choices=["pissa", "loftq"], required=True)
    parser.add_argument("--model", required=True)
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--rank", type=int, default=16)
    parser.add_argument("--alpha", type=int, default=None)
    parser.add_argument("--dropout", type=float, default=0.0)
    parser.add_argument("--target", default="q_proj,v_proj")
    parser.add_argument("--pissa-iter", type=int, default=16)
    parser.add_argument("--loftq-bits", type=int, default=4)
    parser.add_argument("--loftq-iter", type=int, default=4)
    parser.add_argument("--no-safetensors", action="store_true")
    args = parser.parse_args()

    script = Path(__file__).resolve().with_name("init_adapter.py")
    cmd = [
        "python",
        str(script),
        "--kind",
        args.kind,
        "--model-name-or-path",
        args.model,
        "--output-dir",
        args.output_dir,
        "--lora-rank",
        str(args.rank),
        "--lora-dropout",
        str(args.dropout),
        "--lora-target",
        args.target,
    ]
    if args.alpha is not None:
        cmd.extend(["--lora-alpha", str(args.alpha)])
    if args.no_safetensors:
        cmd.append("--no-safetensors")
    if args.kind == "pissa":
        cmd.extend(["--pissa-iter", str(args.pissa_iter)])
        adapter_dir = str(Path(args.output_dir) / "pissa_init")
        handoff = {"pissa_init": False, "pissa_convert": True}
    else:
        cmd.extend(["--loftq-bits", str(args.loftq_bits), "--loftq-iter", str(args.loftq_iter)])
        adapter_dir = str(Path(args.output_dir) / "loftq_init")
        handoff = {"quantization_bit": args.loftq_bits}

    payload = {
        "kind": args.kind,
        "script": str(script),
        "model_name_or_path": args.model,
        "output_dir": args.output_dir,
        "adapter_dir": adapter_dir,
        "command": cmd,
        "handoff": {
            "model_name_or_path": args.output_dir,
            "adapter_name_or_path": adapter_dir,
            "finetuning_type": "lora",
            **handoff,
        },
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(args.output)
    print(" ".join(cmd))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
