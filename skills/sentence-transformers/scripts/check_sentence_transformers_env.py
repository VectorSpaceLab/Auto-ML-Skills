#!/usr/bin/env python3
"""
Check a Python environment for sentence-transformers use.

This script is read-only: it imports the package, reports key dependency and
backend facts, and optionally inspects one model when --model is provided.

Example:
  python check_sentence_transformers_env.py
  python check_sentence_transformers_env.py --model sentence-transformers/all-MiniLM-L6-v2 --class sentence
"""

from __future__ import annotations

import argparse
import importlib
import importlib.metadata as md
import json
import platform
from typing import Any


def dist_version(name: str) -> str | None:
    try:
        return md.version(name)
    except md.PackageNotFoundError:
        return None


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", help="Optional model id or local path to load for a smoke check.")
    parser.add_argument(
        "--class",
        dest="model_class",
        choices=["sentence", "cross", "sparse"],
        default="sentence",
        help="Model class to use with --model.",
    )
    parser.add_argument("--backend", choices=["torch", "onnx", "openvino"], default="torch")
    parser.add_argument("--local-files-only", action="store_true")
    args = parser.parse_args()

    report: dict[str, Any] = {
        "python": platform.python_version(),
        "platform": platform.platform(),
        "packages": {
            "sentence-transformers": dist_version("sentence-transformers"),
            "torch": dist_version("torch"),
            "transformers": dist_version("transformers"),
            "huggingface-hub": dist_version("huggingface-hub"),
            "numpy": dist_version("numpy"),
            "scikit-learn": dist_version("scikit-learn"),
            "scipy": dist_version("scipy"),
        },
        "imports": {},
        "torch": {},
        "model": None,
    }

    for module_name in ["sentence_transformers", "torch", "transformers", "huggingface_hub"]:
        try:
            module = importlib.import_module(module_name)
            report["imports"][module_name] = {
                "ok": True,
                "version": getattr(module, "__version__", None),
            }
        except Exception as exc:  # pragma: no cover - diagnostic path.
            report["imports"][module_name] = {"ok": False, "error": f"{type(exc).__name__}: {exc}"}

    try:
        import torch

        report["torch"] = {
            "version": torch.__version__,
            "cuda_version": getattr(torch.version, "cuda", None),
            "cuda_available": bool(torch.cuda.is_available()),
            "cuda_device_count": int(torch.cuda.device_count()),
            "mps_available": bool(getattr(torch.backends, "mps", None) and torch.backends.mps.is_available()),
        }
        if torch.cuda.is_available():
            report["torch"]["cuda_device_0"] = torch.cuda.get_device_name(0)
            report["torch"]["cuda_capability_0"] = list(torch.cuda.get_device_capability(0))
    except Exception as exc:  # pragma: no cover - diagnostic path.
        report["torch"] = {"error": f"{type(exc).__name__}: {exc}"}

    if args.model:
        try:
            from sentence_transformers import CrossEncoder, SentenceTransformer, SparseEncoder

            cls = {
                "sentence": SentenceTransformer,
                "cross": CrossEncoder,
                "sparse": SparseEncoder,
            }[args.model_class]
            model = cls(args.model, backend=args.backend, local_files_only=args.local_files_only)
            report["model"] = {
                "ok": True,
                "class": cls.__name__,
                "model": args.model,
                "backend": args.backend,
                "device": str(getattr(model, "device", "")),
                "modalities": getattr(model, "modalities", None),
            }
        except Exception as exc:  # pragma: no cover - diagnostic path.
            report["model"] = {"ok": False, "error": f"{type(exc).__name__}: {exc}"}

    print(json.dumps(report, indent=2, sort_keys=True))
    import_ok = report["imports"].get("sentence_transformers", {}).get("ok") is True
    model_ok = not args.model or (report["model"] or {}).get("ok") is True
    return 0 if import_ok and model_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
