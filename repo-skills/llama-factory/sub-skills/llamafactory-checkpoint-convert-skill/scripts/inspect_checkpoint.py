#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--path", type=Path, required=True)
    parser.add_argument("--kind", choices=["hf", "dcp", "auto"], default="auto")
    args = parser.parse_args()
    path = args.path
    print(f"path: {path.resolve()}")
    if not path.exists():
        print("valid: false")
        print("- path does not exist")
        return 1
    files = sorted([p for p in path.rglob("*") if p.is_file()])
    for p in files[:80]:
        print(f"- {p.relative_to(path)} ({p.stat().st_size} bytes)")
    names = {p.name for p in files}
    hf_ok = "config.json" in names and any(name.endswith((".safetensors", ".bin")) for name in names)
    dcp_ok = any(name == ".metadata" or name.endswith(".distcp") for name in names)
    ok = hf_ok if args.kind == "hf" else dcp_ok if args.kind == "dcp" else hf_ok or dcp_ok or bool(files)
    if "config.json" in names:
        cfg = path / "config.json"
        if cfg.exists():
            print("config: " + json.dumps(json.loads(cfg.read_text(encoding="utf-8")), ensure_ascii=False)[:2000])
    print(f"hf_like: {str(hf_ok).lower()}")
    print(f"dcp_like: {str(dcp_ok).lower()}")
    print(f"valid: {str(ok).lower()}")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
