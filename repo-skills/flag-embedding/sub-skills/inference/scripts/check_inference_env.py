#!/usr/bin/env python3
"""No-download FlagEmbedding inference environment diagnostic."""

from __future__ import annotations

import argparse
import importlib
import importlib.metadata
import json
import sys
from typing import Any


def _status(name: str, fn) -> dict[str, Any]:
    try:
        value = fn()
        return {"name": name, "ok": True, "value": value}
    except Exception as exc:  # pragma: no cover - diagnostic output
        return {"name": name, "ok": False, "error": f"{type(exc).__name__}: {exc}"}


def _import(name: str) -> str:
    module = importlib.import_module(name)
    return getattr(module, "__file__", "imported") or "imported"


def _distribution_version() -> str:
    return importlib.metadata.version("FlagEmbedding")


def _torch_backends() -> dict[str, Any]:
    import torch

    backends: dict[str, Any] = {
        "torch_version": torch.__version__,
        "cuda_available": bool(torch.cuda.is_available()),
        "cuda_device_count": int(torch.cuda.device_count()) if torch.cuda.is_available() else 0,
        "mps_available": bool(getattr(torch.backends, "mps", None) and torch.backends.mps.is_available()),
        "musa_available": bool(hasattr(torch, "musa") and torch.musa.is_available()),
    }
    try:
        from transformers import is_torch_npu_available

        backends["npu_available"] = bool(is_torch_npu_available())
    except Exception as exc:  # pragma: no cover - optional backend check
        backends["npu_available"] = False
        backends["npu_check_error"] = f"{type(exc).__name__}: {exc}"
    return backends


def _device_resolution() -> dict[str, Any]:
    from FlagEmbedding.abc.inference import AbsEmbedder, AbsReranker

    samples: list[Any] = [None, "cpu", 0, [0], ["cpu"]]
    resolved: dict[str, Any] = {}
    for sample in samples:
        key = repr(sample)
        try:
            resolved[f"embedder:{key}"] = AbsEmbedder.get_target_devices(sample)
        except Exception as exc:
            resolved[f"embedder:{key}"] = f"{type(exc).__name__}: {exc}"
        try:
            resolved[f"reranker:{key}"] = AbsReranker.get_target_devices(sample)
        except Exception as exc:
            resolved[f"reranker:{key}"] = f"{type(exc).__name__}: {exc}"
    return resolved


def _mapping_summary(show_mappings: bool) -> dict[str, Any]:
    from FlagEmbedding.inference.embedder.model_mapping import (
        AUTO_EMBEDDER_MAPPING,
        EMBEDDER_CLASS_MAPPING,
    )
    from FlagEmbedding.inference.reranker.model_mapping import (
        AUTO_RERANKER_MAPPING,
        RERANKER_CLASS_MAPPING,
    )

    summary: dict[str, Any] = {
        "embedder_model_classes": [item.value for item in EMBEDDER_CLASS_MAPPING.keys()],
        "reranker_model_classes": [item.value for item in RERANKER_CLASS_MAPPING.keys()],
        "auto_embedder_count": len(AUTO_EMBEDDER_MAPPING),
        "auto_reranker_count": len(AUTO_RERANKER_MAPPING),
    }
    if show_mappings:
        summary["auto_embedder_keys"] = list(AUTO_EMBEDDER_MAPPING.keys())
        summary["auto_reranker_keys"] = list(AUTO_RERANKER_MAPPING.keys())
    else:
        summary["auto_embedder_sample"] = list(AUTO_EMBEDDER_MAPPING.keys())[:12]
        summary["auto_reranker_sample"] = list(AUTO_RERANKER_MAPPING.keys())[:12]
    return summary


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Check FlagEmbedding inference imports, torch backends, device resolution, and model mappings without downloading models."
    )
    parser.add_argument(
        "--show-mappings",
        action="store_true",
        help="Print full auto embedder/reranker mapping keys instead of short samples.",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Emit machine-readable JSON.",
    )
    args = parser.parse_args()

    checks = [
        _status("distribution", _distribution_version),
        _status("import FlagEmbedding", lambda: _import("FlagEmbedding")),
        _status("import auto_embedder", lambda: _import("FlagEmbedding.inference.auto_embedder")),
        _status("import auto_reranker", lambda: _import("FlagEmbedding.inference.auto_reranker")),
        _status("import AbsEmbedder", lambda: _import("FlagEmbedding.abc.inference.AbsEmbedder")),
        _status("import AbsReranker", lambda: _import("FlagEmbedding.abc.inference.AbsReranker")),
        _status("torch_backends", _torch_backends),
        _status("device_resolution", _device_resolution),
        _status("model_mappings", lambda: _mapping_summary(args.show_mappings)),
    ]

    ok = all(item["ok"] for item in checks)
    payload = {"ok": ok, "checks": checks}

    if args.json:
        print(json.dumps(payload, indent=2, sort_keys=True))
    else:
        for item in checks:
            marker = "OK" if item["ok"] else "FAIL"
            print(f"[{marker}] {item['name']}")
            if item["ok"]:
                print(json.dumps(item["value"], indent=2, sort_keys=True, default=str))
            else:
                print(item["error"])
        print(f"overall_ok={ok}")

    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
