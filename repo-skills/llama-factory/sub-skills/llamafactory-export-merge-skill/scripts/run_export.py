#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

from common import env_for, run


def main() -> int:
    parser = argparse.ArgumentParser(description="Run LLaMA-Factory export.")
    parser.add_argument("--work-dir", type=Path, default=Path.cwd(), help="Working directory for logs and relative config paths.")
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--python", default=None, help="Python executable. Defaults to current interpreter.")
    parser.add_argument("--log", type=Path, default=None)
    parser.add_argument("--extra-pythonpath", action="append", default=[])
    parser.add_argument("--disable-version-check", action="store_true")
    args = parser.parse_args()

    import sys

    python = args.python or sys.executable
    env = env_for(None, extra_pythonpath=args.extra_pythonpath)
    if args.disable_version_check:
        env["DISABLE_VERSION_CHECK"] = "1"
    cmd = [python, "-m", "llamafactory.cli", "export", str(args.config)]
    return run(cmd, args.work_dir, env, args.log)


if __name__ == "__main__":
    raise SystemExit(main())
