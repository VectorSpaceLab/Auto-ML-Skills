#!/usr/bin/env python3
"""Convert a Hugging Face checkpoint to Megatron torch_dist for slime.

This is a bundled runner adapted from slime's public conversion entrypoint so
future agents do not need the original source checkout's `tools/` directory.
It still requires an installed slime package, slime_plugins, mbridge, torch,
and a full Megatron-LM checkout on PYTHONPATH.

Example:
  PYTHONPATH=/path/to/Megatron-LM:$PYTHONPATH python convert_hf_to_torch_dist.py \
    $(python inspect_model_recipe.py qwen3-0.6b) \
    --hf-checkpoint /models/Qwen3-0.6B \
    --save /models/Qwen3-0.6B_torch_dist
"""

from __future__ import annotations

import gc
import os
import shutil

import torch
import torch.distributed as dist
from megatron.core.enums import ModelType
from megatron.training.arguments import parse_args, validate_args
from megatron.training.checkpointing import get_checkpoint_name, get_checkpoint_tracker_filename, save_checkpoint
from megatron.training.training import get_model

import slime_plugins.mbridge  # noqa: F401
from mbridge import AutoBridge
from slime.backends.megatron_utils.arguments import set_default_megatron_args
from slime.backends.megatron_utils.initialize import init
from slime.backends.megatron_utils.model_provider import get_model_provider_func
from slime.utils.logging_utils import configure_logger
from slime.utils.memory_utils import print_memory


def add_conversion_args(parser):
    parser.add_argument("--hf-checkpoint", type=str, required=True, help="Hugging Face model path.")
    parser.add_argument(
        "--megatron-to-hf-mode",
        choices=["raw", "bridge"],
        default="raw",
        help="Megatron-to-HF bridge mode used later by slime.",
    )
    try:
        parser.add_argument("--padded-vocab-size", type=int, default=None)
    except Exception:
        pass
    return parser


def _ceildiv(a: int, b: int) -> int:
    return -(a // -b)


def get_args():
    args = parse_args(add_conversion_args)
    args = set_default_megatron_args(args)

    args.save_interval = 1
    args.micro_batch_size = 1
    world_size = int(os.environ.get("WORLD_SIZE", "1"))
    args.global_batch_size = world_size

    if world_size > args.num_layers:
        raise ValueError(
            f"World size {world_size} must be <= num_layers {args.num_layers}. "
            "Use fewer GPUs for conversion."
        )

    if args.pipeline_model_parallel_size == 1 and world_size > 1:
        pp_size = world_size
        while True:
            args.pipeline_model_parallel_size = pp_size
            args.decoder_last_pipeline_num_layers = args.num_layers - _ceildiv(args.num_layers, pp_size) * (pp_size - 1)
            if args.decoder_last_pipeline_num_layers > 0:
                break
            if pp_size % 2 == 0:
                pp_size //= 2
            else:
                raise ValueError(
                    f"Cannot find valid pipeline parallel size for {args.num_layers} layers and {world_size} GPUs."
                )

    print(
        "Using pipeline model parallel size: "
        f"{args.pipeline_model_parallel_size}, decoder last pipeline num layers: "
        f"{args.decoder_last_pipeline_num_layers}"
    )
    validate_args(args)
    return args


def main() -> int:
    if torch.version.hip:
        import megatron.core.dist_checkpointing.strategies.filesystem_async as filesystem_async_module
        from slime.utils.rocm_checkpoint_writer import ROCmFileSystemWriterAsync

        filesystem_async_module.FileSystemWriterAsync = ROCmFileSystemWriterAsync
        print("[ROCm] Applied FileSystemWriterAsync patch for HIP compatibility")

    configure_logger()

    world_size = int(os.getenv("WORLD_SIZE") or os.getenv("SLURM_NTASKS") or 1)
    local_rank = int(os.getenv("LOCAL_RANK") or os.getenv("SLURM_LOCALID") or 0)
    global_rank = int(os.getenv("RANK") or os.getenv("SLURM_PROCID") or 0)

    torch.cuda.set_device(local_rank)
    os.environ.setdefault("WORLD_SIZE", str(world_size))
    os.environ.setdefault("RANK", str(global_rank))
    os.environ.setdefault("LOCAL_RANK", str(local_rank))
    os.environ.setdefault("MASTER_ADDR", "localhost")
    os.environ.setdefault("MASTER_PORT", "12355")
    dist.init_process_group(
        backend="nccl",
        world_size=world_size,
        rank=global_rank,
        device_id=torch.device(f"cuda:{local_rank}"),
    )

    args = get_args()
    init(args)

    if hasattr(torch.version, "hip") and torch.version.hip is not None and not args.use_cpu_initialization:
        raise ValueError("AMD GPU conversion requires --use-cpu-initialization.")

    model = get_model(get_model_provider_func(args), ModelType.encoder_or_decoder, wrap_with_ddp=False)
    bridge = AutoBridge.from_pretrained(args.hf_checkpoint, trust_remote_code=True)
    bridge.load_weights(model, args.hf_checkpoint, memory_efficient=True)
    print(f"Model loaded: {args.hf_checkpoint}")

    if args.use_cpu_initialization:
        model[0] = model[0].cpu()

    print_memory("after loading model")
    torch.cuda.synchronize()
    gc.collect()
    torch.cuda.empty_cache()

    save_checkpoint(1, model, None, None, 0)

    if dist.get_rank() == 0:
        tracker_filename = get_checkpoint_tracker_filename(args.save)
        with open(tracker_filename, "w") as f:
            f.write("release")
        source_dir = get_checkpoint_name(args.save, 1, False, return_base_dir=True)
        target_dir = get_checkpoint_name(args.save, -1, True, return_base_dir=True)
        shutil.move(source_dir, target_dir)
    dist.barrier()
    dist.destroy_process_group()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
