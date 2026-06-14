# CLI Reference

Read this when writing TRL terminal commands, YAML configs, or troubleshooting CLI runs.

## Command Groups

| Command | Purpose |
| --- | --- |
| `trl sft` | Supervised fine-tuning |
| `trl dpo` | Direct Preference Optimization |
| `trl grpo` | Group Relative Policy Optimization |
| `trl reward` | Reward model training |
| `trl rloo` | REINFORCE Leave-One-Out online RL |
| `trl kto` | KTO training; currently experimental in Python docs |
| `trl env` | Print environment information |
| `trl vllm-serve` | Serve a model for vLLM-backed generation |
| `trl skills` | Manage TRL-provided agent skills |

## Shared Training Flags

Most training commands expose common `TrainingArguments`-style flags:

- Model and data: `--model_name_or_path`, `--dataset_name`, `--dataset_config`, `--dataset_train_split`, `--dataset_test_split`, `--dataset_streaming`.
- Output and schedule: `--output_dir`, `--num_train_epochs`, `--max_steps`, `--learning_rate`, `--lr_scheduler_type`, `--warmup_steps`.
- Batch/memory: `--per_device_train_batch_size`, `--gradient_accumulation_steps`, `--max_length`, `--gradient_checkpointing`, `--bf16`, `--fp16`.
- Logging/eval/save: `--logging_steps`, `--eval_strategy`, `--eval_steps`, `--save_strategy`, `--save_steps`, `--report_to`, `--push_to_hub`.
- Distributed: `--num_processes`, `--fsdp`, `--fsdp_config`, `--deepspeed`, and backend-related Accelerate flags where supported.
- PEFT: `--use_peft`, `--lora_r`, `--lora_alpha`, and related LoRA options in trainer scripts.

Always check `trl <command> --help` for the current accepted flag names.

## Config Files

All CLI arguments can be represented in YAML:

```yaml
model_name_or_path: Qwen/Qwen2.5-0.5B-Instruct
dataset_name: trl-lib/ultrafeedback_binarized
output_dir: dpo-output
learning_rate: 1.0e-6
per_device_train_batch_size: 2
gradient_accumulation_steps: 8
num_train_epochs: 1
eval_strategy: steps
eval_steps: 100
report_to: none
```

Launch:

```bash
trl dpo --config dpo_config.yaml
```

YAML avoids shell quoting issues for lists, dictionaries, and values such as chat templates or generation kwargs.

## Command-Specific Notes

`trl sft`:
Use for `text`, `messages`, or `prompt`/`completion` data. Useful flags include `--packing`, `--packing_strategy`, `--assistant_only_loss`, `--completion_only_loss`, `--dataset_text_field`, `--chat_template_path`, and `--eos_token`.

`trl dpo`:
Use paired preference data with `chosen` and `rejected`. Useful flags include `--beta`, `--loss_type`, `--precompute_ref_log_probs`, and `--max_length`.

`trl grpo`:
Use prompt data plus rewards. Useful flags include `--reward_funcs`, `--reward_model_name_or_path`, `--num_generations`, `--max_completion_length`, `--reward_weights`, `--use_vllm`, and vLLM server/colocate options.

`trl reward`:
Use preference data to train a scalar reward model. Useful flags include `--max_length`, `--center_rewards_coefficient`, and PEFT options for adapter training.

`trl rloo`:
Use prompt data plus rewards. Useful flags resemble GRPO but RLOO defaults to a lower `num_generations` and uses RLOO-specific advantage behavior.

`trl kto`:
Use unpaired preference data with labels. Current docs warn that KTO API is experimental, and the CLI may emit `TRLExperimentalWarning`.

## Troubleshooting

Unknown argument:
Run `trl <command> --help`. Some Python config fields are not exposed for every command, and older/newer TRL versions may differ.

Dataset column errors:
Check dataset type. SFT expects `text`, `messages`, or `prompt`/`completion`; DPO and RewardTrainer expect `chosen`/`rejected`; KTO expects `completion` plus `label` or data that can be converted; GRPO/RLOO need prompts and reward inputs.

Shell parsing errors:
Move arguments into YAML, especially lists such as `reward_funcs`, dictionaries such as `model_init_kwargs`, and values containing brackets or quotes.

OOM:
Lower `per_device_train_batch_size`, lower sequence lengths, increase `gradient_accumulation_steps`, and add PEFT or distributed strategies before changing trainer algorithms.

Experimental warnings:
Do not hide them unless the user accepts unstable APIs. KTO and other experimental code may change without deprecation.
