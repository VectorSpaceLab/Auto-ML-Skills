# Troubleshooting

## Troubleshooting

- `Unknown task: kto`: the config did not set `stage: kto`, or an old source checkout is being used.
- `USE_V1=1` errors: unset `USE_V1`; KTO uses the default trainer.
- `No module named trl`: install TRL in the same environment used by `torchrun`.
- Dataset rejected or empty: ensure `dataset_info.json` maps `columns.messages` and `columns.kto_tag`, and the records alternate user/assistant turns.
- `Your dataset only has one preference type`: add both `label=true` and `label=false` samples.
- CUDA OOM: switch to LoRA, lower `cutoff_len`, reduce batch size, choose a free GPU, and avoid full KTO unless you have enough memory for a trainable model plus reference model.

## General Checks

- Run the root environment check from the installed public package environment before using `llamafactory-kto-skill`.
- Validate user data and generated config files before launching a full run.
- Keep a one-sample or one-step smoke result beside the final run artifacts.
- Do not depend on private source checkout paths; use installed package CLIs/APIs and bundled scripts in this sub-skill.

