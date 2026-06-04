# Training Troubleshooting

Use this when a TRL trainer script imports but fails before, during, or after `trainer.train()`.

## The Wrong Trainer Was Chosen

Check dataset type first:

- Rows with only `text` or `messages`: use SFT.
- Rows with `prompt` and `completion`: use SFT.
- Rows with `chosen` and `rejected`: use DPO or RewardTrainer.
- Rows with `prompt`, `completion`, and boolean `label`: use KTO-style unpaired preference training.
- Rows with only `prompt`: use GRPO/RLOO/online methods with reward functions or reward models.

## Config Construction Fails

Run:

```bash
python scripts/trainer_smoke_test.py
python ../../scripts/inspect_public_api.py --objects SFTConfig DPOConfig GRPOConfig RLOOConfig RewardConfig
```

Common causes:

- A config field was renamed or removed in the installed TRL version.
- KTO moved between stable and experimental namespaces.
- `load_in_8bit=True` and `load_in_4bit=True` were both set.

## SFT Masks Are Empty Or Wrong

For `assistant_only_loss=True`, use conversational data and a chat template with generation markers. TRL auto-patches known model-family templates for common cases, but unsupported templates need manual checking.

For prompt-completion data, TRL trains on completion tokens by default. Set `completion_only_loss=False` only when the prompt tokens should also contribute.

## DPO Loss Does Not Move

Check:

- `chosen` and `rejected` are not accidentally identical.
- The prompt is not duplicated inside both the explicit `prompt` and the completion text.
- `beta` is suitable for the model and data.
- The reference model is what you expect; pass `ref_model` explicitly for custom loading.
- Dataset rows are not being truncated so heavily that completions are lost.

## GRPO/RLOO Rewards Are All Equal

GRPO and RLOO rely on relative reward signal across completions.

Check:

- Reward functions return one scalar per completion.
- Rewards vary within a generation group.
- `num_generations` is high enough for the reward to compare candidates.
- Format rewards do not dominate correctness rewards unless intentionally weighted.
- If using multiple rewards, use `reward_weights` to control scale.

Run [../scripts/trainer_smoke_test.py](../scripts/trainer_smoke_test.py) to exercise built-in reward functions on dummy completions.

## Online Training Is Too Slow

Generation is often the bottleneck for GRPO/RLOO. Options:

- Use vLLM; see [scaling integrations](../../scaling-integrations/SKILL.md).
- Reduce `max_completion_length`.
- Reduce `num_generations`.
- Increase batch size only after memory is stable.
- Use optimized attention kernels or Liger where compatible.

## Out Of Memory

Fast levers:

- Lower `per_device_train_batch_size`.
- Increase `gradient_accumulation_steps` to preserve effective batch size.
- Lower `max_length` or `max_completion_length`.
- For SFT, use `packing=True` when data is short.
- For SFT, consider `loss_type="chunked_nll"` when compatible.
- Use PEFT/LoRA/QLoRA.
- Enable `activation_offloading=True` if CPU RAM and transfer overhead are acceptable.

## Metrics Are Missing

Check:

- `report_to` defaults to `"none"` in inspected configs, so external loggers are not used unless requested.
- Some metrics are only logged by specific trainers or only when a feature is active. For example, KL metrics may require nonzero `beta`.
- Completion logging requires explicit callbacks or `log_completions` style options where available.

## Checkpoint Or Hub Issues

Use normal Transformers Trainer args:

- `output_dir`
- `save_strategy`
- `save_steps`
- `save_total_limit`
- `push_to_hub`
- `hub_model_id`

For adapters, remember that PEFT checkpoints may save adapter weights rather than a fully merged model. Merge adapters for standalone Transformers inference only when the larger merged checkpoint is desired.
