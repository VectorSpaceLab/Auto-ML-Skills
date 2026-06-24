#!/usr/bin/env python3
from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "scripts"))
from lf_skill_common import env_for, run_stream


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--work-dir", type=Path, default=Path.cwd(), help="Working directory for logs and relative config paths.")
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--launcher", choices=["torchrun", "accelerate", "v1-sft"], default="torchrun")
    parser.add_argument("--torchrun", default="torchrun")
    parser.add_argument("--python", default=sys.executable)
    parser.add_argument("--accelerate", default="accelerate")
    parser.add_argument("--accelerate-config", type=Path, default=None)
    parser.add_argument("--nproc-per-node", default="1")
    parser.add_argument("--master-port", default="29552")
    parser.add_argument("--log", type=Path, default=None)
    args = parser.parse_args()
    if args.launcher == "torchrun":
        env = env_for(None)
        cmd = [args.torchrun, "--nproc_per_node", args.nproc_per_node, "--master_addr", "127.0.0.1", "--master_port", args.master_port, "-m", "llamafactory.cli", "train", str(args.config)]
    elif args.launcher == "accelerate":
        env = env_for(None)
        cmd = [args.accelerate, "launch"]
        if args.accelerate_config:
            cmd += ["--config_file", str(args.accelerate_config)]
        cmd += ["-m", "llamafactory.cli", "train", str(args.config)]
    else:
        env = env_for(None, use_v1=True)
        cmd = [args.python, "-m", "llamafactory.cli", "sft", str(args.config)]
    return run_stream(cmd, args.work_dir, env, args.log)


if __name__ == "__main__":
    raise SystemExit(main())
