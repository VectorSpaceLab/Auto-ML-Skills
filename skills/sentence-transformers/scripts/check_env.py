#!/usr/bin/env python
"""Check a Sentence Transformers environment without downloading models.

Example:
    python skills/sentence-transformers/scripts/check_env.py

The script imports core APIs, reports package metadata, checks optional extras,
and prints basic torch device information. It does not load model weights.
"""

from __future__ import annotations

import importlib
import importlib.metadata as metadata
import sys
from dataclasses import dataclass


@dataclass
class OptionalCheck:
    label: str
    modules: tuple[str, ...]


OPTIONAL_CHECKS = [
    OptionalCheck("datasets / training", ("datasets", "accelerate")),
    OptionalCheck("image support", ("PIL",)),
    OptionalCheck("audio/video torchcodec", ("torchcodec",)),
    OptionalCheck("onnx runtime", ("onnxruntime",)),
    OptionalCheck("optimum onnx", ("optimum.onnxruntime",)),
    OptionalCheck("openvino", ("openvino", "optimum.intel")),
    OptionalCheck("faiss", ("faiss",)),
]


def module_available(name: str) -> bool:
    try:
        importlib.import_module(name)
    except Exception:
        return False
    return True


def main() -> int:
    print(f"python: {sys.version.split()[0]}")
    try:
        version = metadata.version("sentence-transformers")
    except metadata.PackageNotFoundError:
        print("sentence-transformers: not installed")
        return 1

    print(f"sentence-transformers distribution: {version}")
    try:
        import sentence_transformers
        from sentence_transformers import CrossEncoder, SentenceTransformer, SparseEncoder

        print(f"sentence_transformers module version: {sentence_transformers.__version__}")
        print(f"core APIs: {SentenceTransformer.__name__}, {CrossEncoder.__name__}, {SparseEncoder.__name__}")
    except Exception as exc:
        print(f"core import failed: {type(exc).__name__}: {exc}")
        return 1

    try:
        import torch

        print(f"torch: {torch.__version__}")
        print(f"cuda available: {torch.cuda.is_available()}")
        if torch.cuda.is_available():
            print(f"cuda devices: {torch.cuda.device_count()}")
    except Exception as exc:
        print(f"torch check failed: {type(exc).__name__}: {exc}")

    print("optional extras:")
    for check in OPTIONAL_CHECKS:
        statuses = [module_available(name) for name in check.modules]
        status = "ok" if all(statuses) else "missing"
        modules = ", ".join(f"{name}={'yes' if ok else 'no'}" for name, ok in zip(check.modules, statuses))
        print(f"  {check.label}: {status} ({modules})")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
