#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--kind", choices=["pissa", "loftq"], required=True)
    args = parser.parse_args()
    adapter_dir = args.output_dir / f"{args.kind}_init"
    expected_base = ["config.json", "tokenizer_config.json"]
    expected_adapter = ["adapter_config.json"]
    ok = args.output_dir.is_dir() and adapter_dir.is_dir()
    print(f"output_dir: {args.output_dir.resolve()}")
    print(f"adapter_dir: {adapter_dir.resolve()}")
    if args.output_dir.exists():
        print("base_files:")
        for path in sorted(args.output_dir.iterdir()):
            print(f"- {path.name}")
    if adapter_dir.exists():
        print("adapter_files:")
        for path in sorted(adapter_dir.iterdir()):
            print(f"- {path.name}")
        cfg = adapter_dir / "adapter_config.json"
        if cfg.exists():
            print("adapter_config: " + json.dumps(json.loads(cfg.read_text(encoding="utf-8")), ensure_ascii=False)[:2000])
    ok = ok and all((args.output_dir / name).exists() for name in expected_base)
    ok = ok and all((adapter_dir / name).exists() for name in expected_adapter)
    ok = ok and any((adapter_dir / name).exists() for name in ["adapter_model.safetensors", "adapter_model.bin"])
    print(f"valid: {str(ok).lower()}")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
