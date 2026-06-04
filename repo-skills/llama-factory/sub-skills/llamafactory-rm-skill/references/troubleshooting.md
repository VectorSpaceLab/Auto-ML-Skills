# Troubleshooting

## Common Failures

- `RM training requires pair-format samples`: dataset lacks `chosen_messages` and `rejected_messages`, or converter is missing.
- `No valid RM pairs found`: `cutoff_len` truncated one side of the pair; increase it.
- `IndexError: list index out of range` in `render_qwen3_nothink_messages`: raw RM data was likely written with already-converted `chosen_messages`/`rejected_messages` while the dataset YAML also set `converter: pair`. Use raw `chosen` and `rejected` OpenAI-style message lists, then let the converter create internal `chosen_messages`/`rejected_messages`.
- `Qwen3ForTokenClassification` has no `prepare_inputs_for_generation`: LoRA RM can fail on token-classification reward heads in some PEFT/Transformers combinations. For a Qwen3 RM smoke test, use `--method full`; use LoRA only after confirming the installed PEFT stack supports the reward-head model class.
- CUDA OOM on GPU 0: choose a free GPU with `nvidia-smi`, then rerun with `CUDA_VISIBLE_DEVICES=<id>`.
- Hub download for `v1_dpo_demo.yaml`: that YAML points to a remote dataset; create a local YAML for `data/v1_dpo_demo.jsonl` during smoke tests.

## General Checks

- Run the root environment check from the installed public package environment before using `llamafactory-rm-skill`.
- Validate user data and generated config files before launching a full run.
- Keep a one-sample or one-step smoke result beside the final run artifacts.
- Do not depend on private source checkout paths; use installed package CLIs/APIs and bundled scripts in this sub-skill.
