#!/usr/bin/env python3
from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "scripts"))
from lf_skill_common import write_yaml


def none_if_empty(value: str | None) -> str | None:
    return None if value in [None, "", "null", "None"] else value


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--model", required=True)
    parser.add_argument("--dataset", default="identity,alpaca_en_demo")
    parser.add_argument("--dataset-dir", required=True)
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--template", default="qwen3_nothink")
    parser.add_argument("--stage", choices=["sft", "pt"], default="sft")
    parser.add_argument("--variant", choices=["lora", "loraplus", "rslora", "dora", "pissa", "oft"], default="lora")
    parser.add_argument("--adapter-name-or-path", default=None)
    parser.add_argument("--create-new-adapter", action="store_true")
    parser.add_argument("--lora-rank", type=int, default=8)
    parser.add_argument("--lora-target", default="all")
    parser.add_argument("--additional-target", default=None)
    parser.add_argument("--loraplus-lr-ratio", type=float, default=16.0)
    parser.add_argument("--pissa-iter", type=int, default=16)
    parser.add_argument("--pissa-convert", action="store_true")
    parser.add_argument("--oft-block-size", type=int, default=32)
    parser.add_argument("--cutoff-len", type=int, default=512)
    parser.add_argument("--max-samples", type=int, default=16)
    parser.add_argument("--max-steps", type=int, default=1)
    parser.add_argument("--learning-rate", type=float, default=1e-4)
    args = parser.parse_args()
    finetuning_type = "oft" if args.variant == "oft" else "lora"
    cfg = {
        "model_name_or_path": args.model,
        "adapter_name_or_path": none_if_empty(args.adapter_name_or_path),
        "trust_remote_code": True,
        "flash_attn": "sdpa",
        "stage": args.stage,
        "do_train": True,
        "finetuning_type": finetuning_type,
        "additional_target": none_if_empty(args.additional_target),
        "create_new_adapter": args.create_new_adapter,
        "dataset": args.dataset,
        "dataset_dir": args.dataset_dir,
        "template": args.template,
        "cutoff_len": args.cutoff_len,
        "max_samples": args.max_samples,
        "preprocessing_num_workers": 1,
        "dataloader_num_workers": 0,
        "output_dir": args.output_dir,
        "logging_steps": 1,
        "save_steps": 500,
        "plot_loss": False,
        "overwrite_output_dir": True,
        "save_only_model": False,
        "report_to": "none",
        "per_device_train_batch_size": 1,
        "gradient_accumulation_steps": 1,
        "learning_rate": args.learning_rate,
        "num_train_epochs": 1.0,
        "max_steps": args.max_steps,
        "lr_scheduler_type": "cosine",
        "warmup_ratio": 0.0,
        "bf16": True,
        "ddp_timeout": 180000000,
    }
    if finetuning_type == "lora":
        cfg.update({"lora_rank": args.lora_rank, "lora_target": args.lora_target})
        if args.variant == "loraplus":
            cfg["loraplus_lr_ratio"] = args.loraplus_lr_ratio
        elif args.variant == "rslora":
            cfg["use_rslora"] = True
        elif args.variant == "dora":
            cfg["use_dora"] = True
        elif args.variant == "pissa":
            cfg["pissa_init"] = True
            cfg["pissa_iter"] = args.pissa_iter
            cfg["pissa_convert"] = args.pissa_convert
    else:
        cfg.update({"oft_block_size": args.oft_block_size, "oft_target": args.lora_target})
    write_yaml(args.output, cfg)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
