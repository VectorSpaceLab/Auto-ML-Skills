#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

from common import emit


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate a LLaMA-Factory batch prediction config.")
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--model", required=True)
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--adapter", default=None)
    parser.add_argument("--eval-dataset", default="identity")
    parser.add_argument("--dataset-dir", required=True)
    parser.add_argument("--template", default="qwen3_nothink")
    parser.add_argument("--method", choices=["lora", "full"], default=None)
    parser.add_argument("--trust-remote-code", action="store_true")
    parser.add_argument("--cutoff-len", type=int, default=512)
    parser.add_argument("--max-samples", type=int, default=2)
    parser.add_argument("--max-new-tokens", type=int, default=32)
    parser.add_argument("--per-device-eval-batch-size", type=int, default=1)
    parser.add_argument("--bf16", choices=["true", "false"], default="true")
    args = parser.parse_args()

    method = args.method
    if method is None:
        method = "lora" if args.adapter else "full"
    cfg = {
        "model_name_or_path": args.model,
        "trust_remote_code": args.trust_remote_code,
        "flash_attn": "sdpa",
        "stage": "sft",
        "do_predict": True,
        "finetuning_type": method,
        "eval_dataset": args.eval_dataset,
        "dataset_dir": args.dataset_dir,
        "template": args.template,
        "cutoff_len": args.cutoff_len,
        "max_samples": args.max_samples,
        "overwrite_cache": True,
        "preprocessing_num_workers": 1,
        "dataloader_num_workers": 0,
        "output_dir": args.output_dir,
        "overwrite_output_dir": True,
        "report_to": "none",
        "per_device_eval_batch_size": args.per_device_eval_batch_size,
        "predict_with_generate": True,
        "max_new_tokens": args.max_new_tokens,
        "do_sample": False,
        "bf16": args.bf16 == "true",
        "ddp_timeout": 180000000,
    }
    if args.adapter:
        cfg["adapter_name_or_path"] = args.adapter
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text("\n".join(emit(cfg)) + "\n", encoding="utf-8")
    print(args.output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
