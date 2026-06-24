# Troubleshooting

## Common Failures

- `reward_model is necessary for PPO training`: generate or provide a reward model first.
- `trl>=0.8.6,<=0.9.6` error: install a compatible TRL or deliberately set `DISABLE_VERSION_CHECK=1` for smoke only.
- Reward adapter fails to load value head: train RM with value head and keep `value_head.safetensors` or equivalent files.
- PPO OOM: lower `cutoff_len`, `max_new_tokens`, `ppo_buffer_size`, and batch size; prefer LoRA policy training.

## General Checks

- Run the root environment check from the installed public package environment before using `llamafactory-ppo-skill`.
- Validate user data and generated config files before launching a full run.
- Keep a one-sample or one-step smoke result beside the final run artifacts.
- Do not depend on private source checkout paths; use installed package CLIs/APIs and bundled scripts in this sub-skill.

