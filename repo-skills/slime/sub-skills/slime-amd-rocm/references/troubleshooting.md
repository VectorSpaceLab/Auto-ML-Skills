# AMD ROCm Troubleshooting

## CUDA Kernel Import Fails

The environment likely installed CUDA wheels or CUDA-only kernels. Use ROCm-compatible builds for torch, SGLang, and native extensions.

## Attention Backend Unsupported

Remove CUDA-specific `--attention-backend flash` or select a ROCm-supported backend.

## Conversion Works On CPU But Training Fails

Check Megatron and SGLang ROCm patches, not only the slime Python package.
