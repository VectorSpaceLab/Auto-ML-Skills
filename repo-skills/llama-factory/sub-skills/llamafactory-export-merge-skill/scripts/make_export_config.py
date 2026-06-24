#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

from common import emit


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate a LLaMA-Factory export/LoRA merge config.")
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--model", required=True)
    parser.add_argument("--export-dir", required=True)
    parser.add_argument("--adapter", default=None, help="LoRA adapter path. Omit to export/copy the base model.")
    parser.add_argument("--template", default="qwen3_nothink")
    parser.add_argument("--stage", choices=["sft", "rm"], default="sft")
    parser.add_argument("--finetuning-type", choices=["lora", "full"], default=None)
    parser.add_argument("--infer-dtype", choices=["auto", "float16", "bfloat16", "float32"], default="float32")
    parser.add_argument("--export-size", type=int, default=5)
    parser.add_argument("--export-device", choices=["cpu", "auto"], default="cpu")
    parser.add_argument("--legacy-format", action="store_true")
    parser.add_argument("--trust-remote-code", action="store_true")
    parser.add_argument("--quantization-bit", type=int, choices=[4, 8], default=None)
    parser.add_argument("--quantization-dataset", default=None)
    parser.add_argument("--quantization-nsamples", type=int, default=16)
    parser.add_argument("--quantization-maxlen", type=int, default=512)
    args = parser.parse_args()

    if args.adapter and args.quantization_bit is not None:
        raise SystemExit("LLaMA-Factory export cannot merge adapter and quantize in the same command")

    finetuning_type = args.finetuning_type
    if finetuning_type is None:
        finetuning_type = "lora" if args.adapter else "full"

    cfg = {
        "model_name_or_path": args.model,
        "template": args.template,
        "trust_remote_code": args.trust_remote_code,
        "stage": args.stage,
        "finetuning_type": finetuning_type,
        "infer_dtype": args.infer_dtype,
        "export_dir": args.export_dir,
        "export_size": args.export_size,
        "export_device": args.export_device,
        "export_legacy_format": args.legacy_format,
    }
    if args.adapter:
        cfg["adapter_name_or_path"] = args.adapter
    if args.quantization_bit is not None:
        cfg["export_quantization_bit"] = args.quantization_bit
        if args.quantization_dataset is None:
            raise SystemExit("--quantization-dataset is required when --quantization-bit is set")
        cfg["export_quantization_dataset"] = args.quantization_dataset
        cfg["export_quantization_nsamples"] = args.quantization_nsamples
        cfg["export_quantization_maxlen"] = args.quantization_maxlen

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text("\n".join(emit(cfg)) + "\n", encoding="utf-8")
    print(args.output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
