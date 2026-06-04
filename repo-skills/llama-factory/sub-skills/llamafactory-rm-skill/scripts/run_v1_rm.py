#!/usr/bin/env python3
from __future__ import annotations

import argparse
import sys
from pathlib import Path

from lf_common import build_env, run


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--work-dir", type=Path, default=Path.cwd(), help="Working directory for logs and relative config paths.")
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--python", default=sys.executable)
    parser.add_argument("--log", type=Path, default=None)
    parser.add_argument("--extra-pythonpath", action="append", default=[])
    parser.add_argument("--master-addr", default=None)
    parser.add_argument("--master-port", default=None)
    args = parser.parse_args()
    env = build_env(None, args.extra_pythonpath)
    if args.master_addr:
        env["MASTER_ADDR"] = args.master_addr
    if args.master_port:
        env["MASTER_PORT"] = args.master_port
    return run([args.python, "-m", "llamafactory.cli", "rm", str(args.config)], args.work_dir, env, args.log)


if __name__ == "__main__":
    raise SystemExit(main())
