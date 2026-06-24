# Troubleshooting

## Common Failures

- `NotImplementedError: DPO trainer is not implemented yet`: you used `USE_V1=1`; unset it.
- `No module named trl`: install/import `trl` in the same environment used by torchrun.
- `datasets>=2.16.0,<=4.0.0 is required`: install a compatible `datasets`, or add `--disable-version-check` for smoke-only validation.
- CUDA OOM on GPU 0: choose a free GPU with `nvidia-smi`, then rerun with `CUDA_VISIBLE_DEVICES=<id>`.
- Dataset rejected by stage: ensure `ranking: true` in `dataset_info.json`.
- Classic DPO OOM: switch to LoRA, lower `cutoff_len`, use `pref_loss: orpo` for smoke, or provide a smaller/quantized ref model deliberately.

## General Checks

- Run the root environment check from the installed public package environment before using `llamafactory-dpo-skill`.
- Validate user data and generated config files before launching a full run.
- Keep a one-sample or one-step smoke result beside the final run artifacts.
- Do not depend on private source checkout paths; use installed package CLIs/APIs and bundled scripts in this sub-skill.

