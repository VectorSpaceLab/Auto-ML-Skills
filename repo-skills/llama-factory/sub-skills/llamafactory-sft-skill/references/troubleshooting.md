# Troubleshooting

## Troubleshooting

- `Unknown command: sft`: `USE_V1=1` was not set.
- `No module named torchdata`: install `torchdata>=0.10,<=0.11` or add a dependency target dir to `PYTHONPATH`.
- v1 config unknown keys: remove v0 keys and regenerate.
- LoRA injection fails with `torchao`: fix `peft`/`torchao` versions or run full smoke to isolate the rest of the pipeline.
- CUDA OOM on GPU 0: choose a free GPU with `nvidia-smi`, then rerun with `CUDA_VISIBLE_DEVICES=<id>`.
- No loss tokens: SFT messages need at least one assistant response with positive `loss_weight`.

## General Checks

- Run the root environment check from the installed public package environment before using `llamafactory-sft-skill`.
- Validate user data and generated config files before launching a full run.
- Keep a one-sample or one-step smoke result beside the final run artifacts.
- Do not depend on private source checkout paths; use installed package CLIs/APIs and bundled scripts in this sub-skill.

