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
    parser.add_argument("--extension", choices=["galore", "apollo", "badam", "muon", "adam-mini", "dft", "asft", "eaft", "fp8", "profiler"], required=True)
    parser.add_argument("--method", choices=["full", "lora"], default="full")
    parser.add_argument("--cutoff-len", type=int, default=512)
    parser.add_argument("--max-samples", type=int, default=16)
    parser.add_argument("--max-steps", type=int, default=1)
    parser.add_argument("--learning-rate", type=float, default=1e-5)
    parser.add_argument("--gradient-accumulation-steps", type=int, default=None)
    parser.add_argument("--layerwise", action="store_true")
    parser.add_argument("--rank", type=int, default=16)
    parser.add_argument("--target", default="all")
    parser.add_argument("--scale", type=float, default=None)
    parser.add_argument("--badam-mode", choices=["layer", "ratio"], default="layer")
    parser.add_argument("--badam-switch-interval", type=int, default=50)
    parser.add_argument("--asft-alpha", type=float, default=0.1)
    parser.add_argument("--eaft-alpha", type=float, default=1.0)
    parser.add_argument("--fp8-backend", default="torchao")
    parser.add_argument("--deepspeed", default=None)
    parser.add_argument("--profile-modules", default=None)
    args = parser.parse_args()
    grad_accum = args.gradient_accumulation_steps
    if grad_accum is None:
        grad_accum = 1 if args.layerwise and args.extension in {"galore", "apollo"} else 8
    cfg = {
        "model_name_or_path": args.model,
        "trust_remote_code": True,
        "flash_attn": "sdpa",
        "stage": "sft",
        "do_train": True,
        "finetuning_type": args.method,
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
        "gradient_accumulation_steps": grad_accum,
        "learning_rate": args.learning_rate,
        "num_train_epochs": 1.0,
        "max_steps": args.max_steps,
        "lr_scheduler_type": "cosine",
        "warmup_ratio": 0.0,
        "bf16": True,
        "ddp_timeout": 180000000,
        "deepspeed": none_if_empty(args.deepspeed),
    }
    if args.method == "lora":
        cfg.update({"lora_rank": 8, "lora_target": "all"})
    if args.extension == "galore":
        cfg.update({"use_galore": True, "galore_layerwise": args.layerwise, "galore_target": args.target, "galore_rank": args.rank, "galore_scale": args.scale if args.scale is not None else 2.0})
        if args.layerwise:
            cfg["pure_bf16"] = True
            cfg.pop("bf16", None)
    elif args.extension == "apollo":
        cfg.update({"use_apollo": True, "apollo_layerwise": args.layerwise, "apollo_target": args.target, "apollo_rank": args.rank, "apollo_scale": args.scale if args.scale is not None else 32.0, "apollo_scale_type": "channel"})
        if args.layerwise:
            cfg["pure_bf16"] = True
            cfg.pop("bf16", None)
    elif args.extension == "badam":
        cfg.update({"use_badam": True, "badam_mode": args.badam_mode, "badam_switch_mode": "ascending", "badam_switch_interval": args.badam_switch_interval, "badam_verbose": 2})
    elif args.extension == "muon":
        cfg["use_muon"] = True
    elif args.extension == "adam-mini":
        cfg["use_adam_mini"] = True
    elif args.extension == "dft":
        cfg["use_dft_loss"] = True
    elif args.extension == "asft":
        cfg.update({"use_asft_loss": True, "asft_alpha": args.asft_alpha})
    elif args.extension == "eaft":
        cfg.update({"use_eaft_loss": True, "eaft_alpha": args.eaft_alpha})
    elif args.extension == "fp8":
        cfg.update({"fp8": True, "fp8_backend": args.fp8_backend, "fp8_enable_fsdp_float8_all_gather": False})
    elif args.extension == "profiler":
        cfg.update({"enable_torch_profiler": True, "profiler_output_dir": str(Path(args.output_dir) / "profiler"), "profiler_wait_steps": 1, "profiler_warmup_steps": 1, "profiler_active_steps": 1, "profiler_repeat": 1, "profile_modules": none_if_empty(args.profile_modules)})
    write_yaml(args.output, cfg)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
