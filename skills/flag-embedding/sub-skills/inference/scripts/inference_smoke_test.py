#!/usr/bin/env python3
"""Run safe FlagEmbedding inference checks.

Default mode imports public APIs only and does not download models.
Model modes may download/load models and should be used only when requested.
"""

from __future__ import annotations

import argparse
import json
import sys
from typing import Any


def emit(report: dict[str, Any]) -> int:
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report.get("ok") else 1


def import_check() -> dict[str, Any]:
    import importlib.metadata as md
    from FlagEmbedding import FlagAutoModel, FlagAutoReranker

    return {
        "ok": True,
        "mode": "import",
        "version": md.version("FlagEmbedding"),
        "apis": [FlagAutoModel.__name__, FlagAutoReranker.__name__],
    }


def embedder_check(args: argparse.Namespace) -> dict[str, Any]:
    import numpy as np
    from FlagEmbedding import FlagAutoModel

    kwargs: dict[str, Any] = {
        "use_fp16": args.use_fp16,
        "devices": args.device,
    }
    if args.model_class:
        kwargs["model_class"] = args.model_class
    if args.pooling_method:
        kwargs["pooling_method"] = args.pooling_method
    if args.query_instruction:
        kwargs["query_instruction_for_retrieval"] = args.query_instruction

    model = FlagAutoModel.from_finetuned(args.embedder, **kwargs)
    q = model.encode_queries([args.query])
    p = model.encode_corpus([args.passage])
    score = q @ p.T
    return {
        "ok": True,
        "mode": "embedder",
        "query_shape": list(q.shape),
        "passage_shape": list(p.shape),
        "score": np.asarray(score).tolist(),
    }


def reranker_check(args: argparse.Namespace) -> dict[str, Any]:
    from FlagEmbedding import FlagAutoReranker

    kwargs: dict[str, Any] = {
        "use_fp16": args.use_fp16,
    }
    if args.device is not None:
        kwargs["devices"] = args.device
    if args.model_class:
        kwargs["model_class"] = args.model_class

    reranker = FlagAutoReranker.from_finetuned(args.reranker, **kwargs)
    scores = reranker.compute_score([[args.query, args.passage]], normalize=args.normalize)
    return {"ok": True, "mode": "reranker", "scores": scores}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--mode", choices=["import", "embedder", "reranker"], default="import")
    parser.add_argument("--embedder", help="Embedder model id or local path for --mode embedder.")
    parser.add_argument("--reranker", help="Reranker model id or local path for --mode reranker.")
    parser.add_argument("--model-class", help="Explicit FlagEmbedding model_class for custom checkpoints.")
    parser.add_argument("--pooling-method", help="Explicit pooling method for custom embedders.")
    parser.add_argument("--query-instruction", help="Retrieval query instruction for embedder mode.")
    parser.add_argument("--query", default="What is the capital of France?")
    parser.add_argument("--passage", default="Paris is the capital of France.")
    parser.add_argument("--device", default="cpu", help="Device string, for example cpu or cuda:0.")
    parser.add_argument("--use-fp16", action="store_true", help="Use fp16. Avoid on CPU.")
    parser.add_argument("--normalize", action="store_true", help="Normalize reranker scores.")
    args = parser.parse_args()

    try:
        if args.mode == "import":
            return emit(import_check())
        if args.mode == "embedder":
            if not args.embedder:
                return emit({"ok": False, "error": "--embedder is required for embedder mode"})
            return emit(embedder_check(args))
        if args.mode == "reranker":
            if not args.reranker:
                return emit({"ok": False, "error": "--reranker is required for reranker mode"})
            return emit(reranker_check(args))
    except Exception as exc:
        return emit({"ok": False, "error": f"{type(exc).__name__}: {exc}"})

    return 1


if __name__ == "__main__":
    sys.exit(main())
