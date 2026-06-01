#!/usr/bin/env python
"""Print concise help for installed TRL CLI commands.

Example:
    python scripts/print_cli_summary.py
    python scripts/print_cli_summary.py --commands sft grpo vllm-serve
"""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys


DEFAULT_COMMANDS = ["sft", "dpo", "grpo", "rloo", "reward", "kto", "env", "skills", "vllm-serve"]


def run_help(executable: str, args: list[str]) -> str:
    completed = subprocess.run([executable, *args], check=False, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    return completed.stdout


def first_lines(text: str, limit: int) -> str:
    return "\n".join(text.splitlines()[:limit])


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--commands", nargs="*", default=DEFAULT_COMMANDS)
    parser.add_argument("--lines", type=int, default=35)
    args = parser.parse_args()

    executable = shutil.which("trl")
    if executable is None:
        print("The `trl` executable is not on PATH.", file=sys.stderr)
        return 1

    print("## trl")
    print(first_lines(run_help(executable, ["--help"]), args.lines))
    for command in args.commands:
        print(f"\n## trl {command}")
        print(first_lines(run_help(executable, [command, "--help"]), args.lines))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
