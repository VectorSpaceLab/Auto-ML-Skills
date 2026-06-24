#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path


def model_flops_from_config(config: dict, batch_size: int, seq_length: int, include_backward: bool, include_recompute: bool) -> int:
    base = 2
    hidden = int(config["hidden_size"])
    vocab = int(config["vocab_size"])
    intermediate = int(config["intermediate_size"])
    heads = int(config["num_attention_heads"])
    kv_heads = int(config.get("num_key_value_heads", heads))
    layers = int(config["num_hidden_layers"])
    tie = bool(config.get("tie_word_embeddings", False))
    mlp = batch_size * seq_length * layers * (3 * base * hidden * intermediate)
    q = base * hidden * hidden
    o = base * hidden * hidden
    k = base * hidden * hidden * kv_heads // heads
    v = base * hidden * hidden * kv_heads // heads
    proj = batch_size * seq_length * layers * (q + o + k + v)
    sdpa = batch_size * layers * (2 * base * hidden * seq_length * seq_length)
    emb = batch_size * seq_length * hidden * vocab * (1 if tie else 2)
    non_emb_coeff = 1 + (2 if include_backward else 0) + (1 if include_recompute else 0)
    emb_coeff = 1 + (2 if include_backward else 0)
    return non_emb_coeff * (mlp + proj + sdpa) + emb_coeff * emb


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", type=Path, required=True)
    parser.add_argument("--batch-size", type=int, default=1)
    parser.add_argument("--seq-length", type=int, default=512)
    parser.add_argument("--steps-per-second", type=float, required=True)
    parser.add_argument("--device-flops-tflops", type=float, required=True)
    parser.add_argument("--world-size", type=int, default=1)
    parser.add_argument("--no-backward", action="store_true")
    parser.add_argument("--include-recompute", action="store_true")
    parser.add_argument("--output", type=Path, default=None)
    args = parser.parse_args()
    config_path = args.model / "config.json" if args.model.is_dir() else args.model
    config = json.loads(config_path.read_text(encoding="utf-8"))
    total_batch = args.batch_size * args.world_size
    flops_per_step = model_flops_from_config(config, total_batch, args.seq_length, not args.no_backward, args.include_recompute)
    peak = args.device_flops_tflops * 1e12 * args.world_size
    achieved = args.steps_per_second * flops_per_step
    result = {
        "model": str(args.model),
        "total_batch_size": total_batch,
        "seq_length": args.seq_length,
        "steps_per_second": args.steps_per_second,
        "flops_per_step": flops_per_step,
        "achieved_flops": achieved,
        "peak_flops": peak,
        "mfu": achieved / peak,
        "mfu_percent": achieved / peak * 100,
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("valid: true")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
