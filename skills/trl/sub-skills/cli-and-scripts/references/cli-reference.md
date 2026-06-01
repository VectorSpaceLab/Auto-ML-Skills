# CLI Reference

Read this when constructing or debugging TRL terminal commands.

## Top-Level Command

```bash
trl --help
```

Expected inspected command set:

```text
trl {dpo,env,grpo,kto,reward,rloo,sft,skills,vllm-serve}
```

## Training Commands

All training commands share broad groups of arguments:

- Dataset args: `--dataset_name`, `--dataset_config`, `--dataset_train_split`, `--dataset_test_split`, `--dataset_streaming`.
- Training args: `--output_dir`, `--per_device_train_batch_size`, `--gradient_accumulation_steps`, `--num_train_epochs`, `--max_steps`, `--learning_rate`, `--bf16`, `--fp16`, `--eval_strategy`, `--save_strategy`, `--push_to_hub`.
- Model args: `--model_name_or_path`, `--model_revision`, `--dtype`, `--trust_remote_code`, `--attn_implementation`.
- PEFT args: `--use_peft`, `--lora_r`, `--lora_alpha`, `--lora_dropout`, `--lora_task_type`, `--load_in_4bit`, `--load_in_8bit`.
- Dataset mixture args: `--datasets`, `--streaming`, `--test_split_size`.

### `trl sft`

Use for supervised fine-tuning.

```bash
trl sft \
  --model_name_or_path Qwen/Qwen2.5-0.5B \
  --dataset_name trl-lib/Capybara \
  --learning_rate 2e-5 \
  --max_length 1024 \
  --output_dir sft-output
```

SFT-specific flags include:

- `--dataset_text_field`
- `--chat_template_path`
- `--eos_token`
- `--max_length`
- `--packing`
- `--packing_strategy`
- `--padding_free`
- `--completion_only_loss`
- `--assistant_only_loss`
- `--loss_type`
- `--activation_offloading`
- `--pad_token`

### `trl dpo`

Use for offline preference optimization.

```bash
trl dpo \
  --model_name_or_path Qwen/Qwen3-0.6B \
  --dataset_name trl-lib/ultrafeedback_binarized \
  --learning_rate 1e-6 \
  --beta 0.1 \
  --output_dir dpo-output
```

DPO-specific flags include:

- `--disable_dropout` / `--no_disable_dropout`
- `--max_length`
- `--padding_free`
- `--precompute_ref_log_probs`
- `--loss_type`
- `--loss_weights`
- `--label_smoothing`
- `--beta`
- `--sync_ref_model`
- `--activation_offloading`

### `trl grpo`

Use for online reward training.

```bash
trl grpo \
  --model_name_or_path Qwen/Qwen2.5-0.5B-Instruct \
  --dataset_name trl-lib/DeepMath-103K \
  --reward_funcs accuracy_reward \
  --num_generations 8 \
  --max_completion_length 256 \
  --output_dir grpo-output
```

GRPO-specific flags include:

- `--reward_model_name_or_path`
- `--reward_funcs`
- `--num_generations`
- `--max_completion_length`
- `--temperature`, `--top_p`, `--top_k`, `--min_p`
- `--generation_kwargs`
- `--use_vllm`
- `--vllm_mode`
- `--vllm_server_base_url`
- `--vllm_server_host`
- `--vllm_server_port`
- `--vllm_gpu_memory_utilization`
- `--vllm_tensor_parallel_size`
- `--beta`
- `--loss_type`
- `--reward_weights`
- `--log_completions`

### `trl rloo`

Use for REINFORCE Leave-One-Out training.

```bash
trl rloo \
  --model_name_or_path Qwen/Qwen2.5-0.5B-Instruct \
  --dataset_name trl-lib/DeepMath-103K \
  --reward_funcs accuracy_reward \
  --num_generations 2 \
  --output_dir rloo-output
```

RLOO shares many online generation and vLLM flags with GRPO.

### `trl reward`

Use for reward model training.

```bash
trl reward \
  --model_name_or_path Qwen/Qwen2.5-0.5B-Instruct \
  --dataset_name trl-lib/ultrafeedback_binarized \
  --learning_rate 1e-4 \
  --output_dir reward-output
```

Reward-specific flags include:

- `--chat_template_path`
- `--eos_token`
- `--max_length`
- `--center_rewards_coefficient`
- `--activation_offloading`

### `trl kto`

KTO is exposed as a CLI command in the inspected package, but docs mark KTO as experimental in v1. Expect an experimental warning.

```bash
trl kto \
  --model_name_or_path Qwen/Qwen2-0.5B-Instruct \
  --dataset_name trl-lib/kto-mix-14k \
  --learning_rate 1e-6 \
  --output_dir kto-output
```

KTO-specific flags include:

- `--loss_type`
- `--beta`
- `--desirable_weight`
- `--undesirable_weight`

## Other Commands

### `trl env`

Print environment information for bug reports and debugging:

```bash
trl env
```

### `trl vllm-serve`

Serve a model for vLLM-backed generation:

```bash
trl vllm-serve --model Qwen/Qwen2.5-7B --tensor-parallel-size 4
```

Important flags:

- `--model`
- `--revision`
- `--tensor_parallel_size` / `--tensor-parallel-size`
- `--data_parallel_size` / `--data-parallel-size`
- `--host`
- `--port`
- `--gpu_memory_utilization`
- `--dtype`
- `--max_model_len`
- `--enable_prefix_caching`
- `--enforce_eager`
- `--kv_cache_dtype`
- `--trust_remote_code`
- `--vllm_model_impl`
- `--distributed_executor_backend`
- `--speculative_config`

### `trl skills`

Manage packaged TRL agent skills:

```bash
trl skills list
trl skills install <skill-name>
trl skills uninstall <skill-name>
```

Inspect `trl skills --help` and subcommand help in the target environment before automating skill installation.
