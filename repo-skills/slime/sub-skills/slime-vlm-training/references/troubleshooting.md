# VLM Troubleshooting

## Backend Missing VLM Fields

Some multimodal models rely on Megatron Bridge or plugin providers. Confirm the provider passes the required architecture fields, freezing flags, and MoE/Vision settings.

## Slow Conv3D Or Vision Tower

Check CUDA/cuDNN versions. Some torch/cuDNN combinations can regress conv3d performance.

## Images Not Loaded

Confirm `--multimodal-keys` JSON maps the media type to the dataset field and that all paths are reachable from Ray workers.
