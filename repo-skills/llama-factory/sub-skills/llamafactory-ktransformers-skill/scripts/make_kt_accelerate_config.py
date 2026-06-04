#!/usr/bin/env python3
"""Emit an Accelerate FSDP2 config snippet with KTransformers kt_config."""

from __future__ import annotations

import argparse


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate an Accelerate KT FSDP2 YAML snippet.")
    parser.add_argument("--num-processes", type=int, default=4)
    parser.add_argument("--kt-backend", choices=["AMXBF16", "AMXINT8", "AMXINT4"], default="AMXBF16")
    parser.add_argument("--kt-num-threads", type=int, default=96)
    parser.add_argument("--lora-rank", type=int, default=8)
    args = parser.parse_args()
    print(
        f"""compute_environment: LOCAL_MACHINE
distributed_type: FSDP
fsdp_config:
  fsdp_auto_wrap_policy: TRANSFORMER_BASED_WRAP
  fsdp_cpu_ram_efficient_loading: true
  fsdp_offload_params: false
  fsdp_reshard_after_forward: true
  fsdp_state_dict_type: FULL_STATE_DICT
  fsdp_version: 2
mixed_precision: bf16
num_machines: 1
num_processes: {args.num_processes}
rdzv_backend: static
same_network: true
use_cpu: false

kt_config:
  enabled: true
  kt_backend: {args.kt_backend}
  kt_num_threads: {args.kt_num_threads}
  kt_tp_enabled: true
  kt_threadpool_count: 2
  kt_max_cache_depth: 2
  kt_share_backward_bb: true
  lora_rank: {args.lora_rank}"""
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
