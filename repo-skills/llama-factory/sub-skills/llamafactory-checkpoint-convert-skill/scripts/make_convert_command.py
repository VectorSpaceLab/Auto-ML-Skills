#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path


UTILITY_MAP = {
    "hf2dcp": "scripts/hf2dcp.py",
    "dcp2hf": "scripts/dcp2hf.py",
    "megatron-merge": "scripts/megatron_merge.py",
    "qwen-omni-merge": "scripts/qwen_omni_merge.py",
    "llamafy-qwen": "scripts/convert_ckpt/llamafy_qwen.py",
    "llamafy-baichuan2": "scripts/convert_ckpt/llamafy_baichuan2.py",
    "tiny-qwen3": "scripts/convert_ckpt/tiny_qwen3.py",
    "tiny-llama4": "scripts/convert_ckpt/tiny_llama4.py",
}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--task", choices=sorted(UTILITY_MAP), required=True)
    parser.add_argument("--hf-path", default=None)
    parser.add_argument("--dcp-path", default=None)
    parser.add_argument("--config-path", default=None)
    parser.add_argument("--extra-args", nargs=argparse.REMAINDER, default=[])
    args = parser.parse_args()

    utility = UTILITY_MAP[args.task]
    cmd = ["python", f"<vendored-skill-or-project-script>/{utility}"]
    expected_output = None
    if args.task == "hf2dcp":
        cmd.extend(["convert", "--hf_path", str(args.hf_path), "--dcp_path", str(args.dcp_path)])
        expected_output = args.dcp_path
    elif args.task == "dcp2hf":
        cmd.extend(
            ["convert", "--dcp_path", str(args.dcp_path), "--hf_path", str(args.hf_path), "--config_path", str(args.config_path)]
        )
        expected_output = args.hf_path
    else:
        cmd.extend(args.extra_args)
    payload = {
        "task": args.task,
        "utility": utility,
        "hf_path": args.hf_path,
        "dcp_path": args.dcp_path,
        "config_path": args.config_path,
        "expected_output": expected_output,
        "command": cmd,
        "note": "This LLaMA-Factory utility is distributed as a public repo script, not a stable installed-package CLI. Vendor/adapt the utility into the working project before execution.",
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(args.output)
    print(" ".join(cmd))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
