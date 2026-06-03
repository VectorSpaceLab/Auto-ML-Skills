# AMD ROCm Configuration

## Runtime Environment

Typical ROCm jobs need HIP/NCCL/RCCL-aware environment variables and ROCm-compatible PyTorch/SGLang builds. Use ROCm-specific Docker or conda setup.

Example runtime adjustments:

```bash
export HIP_VISIBLE_DEVICES="${HIP_VISIBLE_DEVICES:-0,1,2,3,4,5,6,7}"
export PYTORCH_HIP_ALLOC_CONF="${PYTORCH_HIP_ALLOC_CONF:-expandable_segments:True}"
```

## Launch Flags

Some AMD paths disable CUDA-specific fusion:

```bash
--no-gradient-accumulation-fusion
```

Attention backend and low-precision options must match ROCm support.

## Checkpoint Conversion

HF to Megatron conversion may need CPU initialization or ROCm-specific build compatibility. Validate conversion on the target environment before launching a long job.
