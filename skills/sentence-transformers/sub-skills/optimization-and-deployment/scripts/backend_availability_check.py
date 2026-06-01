#!/usr/bin/env python
"""Check optional backend packages for Sentence Transformers optimization."""

from __future__ import annotations

import importlib


CHECKS = {
    "onnxruntime": "ONNX Runtime inference",
    "optimum.onnxruntime": "Optimum ONNX export/optimization",
    "openvino": "OpenVINO runtime",
    "optimum.intel": "Optimum Intel/OpenVINO integration",
    "faiss": "FAISS dense ANN or hard-negative mining acceleration",
}


def main() -> int:
    ok = True
    for module, purpose in CHECKS.items():
        try:
            imported = importlib.import_module(module)
            version = getattr(imported, "__version__", "unknown")
            print(f"{module}: ok ({version}) - {purpose}")
        except Exception as exc:
            print(f"{module}: missing ({type(exc).__name__}: {exc}) - {purpose}")
            ok = False
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
