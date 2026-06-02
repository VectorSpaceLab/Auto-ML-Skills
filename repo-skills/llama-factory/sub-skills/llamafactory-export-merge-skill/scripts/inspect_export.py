#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser(description="Inspect an exported LLaMA-Factory model directory.")
    parser.add_argument("--export-dir", type=Path, required=True)
    parser.add_argument("--expect-merged", action="store_true", help="Fail if adapter files remain in export_dir.")
    args = parser.parse_args()

    path = args.export_dir
    errors: list[str] = []
    print(f"export_dir: {path.resolve()}")
    if not path.is_dir():
        print("valid: false")
        print("- export directory does not exist")
        return 1
    names = {p.name for p in path.iterdir()}
    for name in sorted(names):
        print(f"- {name}")

    if "config.json" not in names:
        errors.append("config.json is missing")
    if not ({"model.safetensors", "pytorch_model.bin"} & names) and not any(
        name.endswith(".safetensors") or name.endswith(".bin") for name in names
    ):
        errors.append("no model weight file found")
    if not ({"tokenizer.json", "tokenizer.model", "vocab.json"} & names):
        errors.append("no tokenizer file found")
    if "Modelfile" not in names:
        errors.append("Ollama Modelfile is missing")
    if args.expect_merged and ({"adapter_config.json", "adapter_model.safetensors", "adapter_model.bin"} & names):
        errors.append("adapter files remain; export does not look like a merged full model")

    cfg_path = path / "config.json"
    if cfg_path.exists():
        try:
            cfg = json.loads(cfg_path.read_text(encoding="utf-8"))
            print(f"model_type: {cfg.get('model_type')}")
            print(f"torch_dtype: {cfg.get('torch_dtype')}")
        except Exception as exc:
            errors.append(f"config.json is not valid JSON: {exc}")

    if errors:
        print("valid: false")
        for error in errors:
            print(f"- {error}")
        return 1
    print("valid: true")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
