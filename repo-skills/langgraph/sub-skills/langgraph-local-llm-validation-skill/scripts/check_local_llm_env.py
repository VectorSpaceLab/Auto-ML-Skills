#!/usr/bin/env python3
"""Preflight local model files and runtime imports for LangGraph local LLM smoke."""

from __future__ import annotations

import argparse
import importlib.util
import json
from pathlib import Path


def has_module(name: str) -> bool:
    return importlib.util.find_spec(name) is not None


def inspect_model(path: Path) -> dict[str, object]:
    files = [p.name for p in path.iterdir()] if path.exists() and path.is_dir() else []
    return {
        "exists": path.exists(),
        "is_dir": path.is_dir(),
        "has_config": (path / "config.json").exists(),
        "has_tokenizer": any((path / name).exists() for name in ["tokenizer.json", "tokenizer.model", "vocab.json"]),
        "has_weights": any(name.endswith((".safetensors", ".bin", ".gguf")) for name in files),
        "file_count": len(files),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--model-path", required=True)
    args = parser.parse_args()
    path = Path(args.model_path).expanduser()
    result = {
        "imports": {
            "torch": has_module("torch"),
            "transformers": has_module("transformers"),
            "langgraph": has_module("langgraph"),
        },
        "model": inspect_model(path),
    }
    result["pass"] = bool(
        result["imports"]["torch"]
        and result["imports"]["transformers"]
        and result["imports"]["langgraph"]
        and result["model"]["exists"]
        and result["model"]["has_config"]
        and result["model"]["has_tokenizer"]
        and result["model"]["has_weights"]
    )
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
