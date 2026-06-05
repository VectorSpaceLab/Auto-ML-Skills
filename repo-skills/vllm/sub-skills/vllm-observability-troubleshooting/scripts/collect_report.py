#!/usr/bin/env python3
"""Create a vLLM diagnostic report directory skeleton."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path


def run_capture(argv: list[str], path: Path, timeout: float = 30.0) -> None:
    try:
        proc = subprocess.run(argv, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=timeout, check=False)
        path.write_text(proc.stdout, encoding="utf-8")
    except Exception as exc:
        path.write_text(f"{type(exc).__name__}: {exc}\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out-dir", required=True)
    parser.add_argument("--base-url", default=None)
    args = parser.parse_args()
    out = Path(args.out_dir)
    out.mkdir(parents=True, exist_ok=True)
    root_scripts = Path(__file__).resolve().parents[3] / "scripts"
    run_capture([sys.executable, str(root_scripts / "check_env.py"), "--json"], out / "check_env.json")
    run_capture([sys.executable, str(root_scripts / "inspect_api.py"), "--json"], out / "inspect_api.json")
    run_capture(["vllm", "collect-env"], out / "collect_env.txt")
    manifest = {"base_url": args.base_url, "files": sorted(p.name for p in out.iterdir())}
    (out / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(str(out))


if __name__ == "__main__":
    main()
