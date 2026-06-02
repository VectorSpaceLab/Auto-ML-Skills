#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

from common import env_for, stream


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--work-dir", type=Path, default=Path.cwd(), help="Working directory for logs and relative config paths.")
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--torchrun", default="torchrun")
    parser.add_argument("--log", type=Path, default=None)
    parser.add_argument("--master-port", default="29534")
    parser.add_argument("--extra-pythonpath", action="append", default=[])
    parser.add_argument("--disable-version-check", action="store_true")
    args = parser.parse_args()
    env = env_for(None, args.extra_pythonpath)
    if args.disable_version_check:
        env["DISABLE_VERSION_CHECK"] = "1"
    cmd = [
        args.torchrun,
        "--nproc_per_node",
        "1",
        "--master_addr",
        "127.0.0.1",
        "--master_port",
        args.master_port,
        "-m", "llamafactory.cli", "train",
        str(args.config),
    ]
    return stream(cmd, args.work_dir, env, args.log)


if __name__ == "__main__":
    raise SystemExit(main())
