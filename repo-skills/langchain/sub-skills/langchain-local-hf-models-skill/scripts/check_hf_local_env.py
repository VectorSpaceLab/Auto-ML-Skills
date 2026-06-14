#!/usr/bin/env python3
"""Preflight local Hugging Face model files and optional LangChain wrapper imports."""

from __future__ import annotations

import argparse
import importlib.util
import json
from pathlib import Path


def exists_module(name: str) -> bool:
    return importlib.util.find_spec(name) is not None


def inspect_model_dir(path: Path | None) -> dict[str, object]:
    if path is None:
        return {"provided": False}
    files = []
    if path.exists() and path.is_dir():
        files = [p.name for p in path.iterdir()]
    return {
        "provided": True,
        "exists": path.exists(),
        "is_dir": path.is_dir(),
        "has_config": (path / "config.json").exists(),
        "has_tokenizer": any(
            (path / name).exists()
            for name in ["tokenizer.json", "tokenizer.model", "vocab.json", "merges.txt"]
        ),
        "has_weights": any(
            suffix in name
            for name in files
            for suffix in [".safetensors", ".bin", ".gguf"]
        ),
        "file_count": len(files),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--model-path", help="Local model directory to inspect.")
    args = parser.parse_args()

    model_path = Path(args.model_path).expanduser() if args.model_path else None
    result = {
        "imports": {
            "torch": exists_module("torch"),
            "transformers": exists_module("transformers"),
            "langchain_huggingface": exists_module("langchain_huggingface"),
        },
        "model_dir": inspect_model_dir(model_path),
    }
    result["pass"] = result["imports"]["torch"] and result["imports"]["transformers"]
    if model_path is not None:
        result["pass"] = bool(
            result["pass"]
            and result["model_dir"].get("exists")
            and result["model_dir"].get("has_config")
            and result["model_dir"].get("has_tokenizer")
            and result["model_dir"].get("has_weights")
        )
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
