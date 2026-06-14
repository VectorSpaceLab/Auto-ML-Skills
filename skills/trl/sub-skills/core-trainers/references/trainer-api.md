# Trainer API Reference

Read this for stable TRL trainer constructor shapes, config defaults, and API decision points. Facts here were verified by installed-package inspection.

## Stable Root Namespace

The public `trl` package exposes:

```python
from trl import (
    SFTConfig, SFTTrainer,
    DPOConfig, DPOTrainer,
    GRPOConfig, GRPOTrainer,
    RewardConfig, RewardTrainer,
    RLOOConfig, RLOOTrainer,
)
```

`KTOConfig` and `KTOTrainer` are also present in the root lazy import structure, but TRL documentation warns that KTO is experimental and lives under `trl.experimental.kto`. Prefer the experimental import path for new KTO examples.

## Trainer Constructors

`SFTTrainer`:

```python
SFTTrainer(
    model,
    args=None,
    data_collator=None,
    train_dataset=None,
    eval_dataset=None,
    processing_class=None,
    compute_loss_func=None,
    compute_metrics=None,
    callbacks=None,
    optimizers=(None, None),
    optimizer_cls_and_kwargs=None,
    preprocess_logits_for_metrics=None,
    peft_config=None,
    formatting_func=None,
)
```

`DPOTrainer`:

```python
DPOTrainer(
    model,
    ref_model=None,
    args=None,
    data_collator=None,
    train_dataset=None,
    eval_dataset=None,
    processing_class=None,
    compute_metrics=None,
    callbacks=None,
    optimizers=(None, None),
    peft_config=None,
)
```

`GRPOTrainer`:

```python
GRPOTrainer(
    model,
    reward_funcs,
    args=None,
    train_dataset=None,
    eval_dataset=None,
    processing_class=None,
    reward_processing_classes=None,
    callbacks=None,
    optimizers=(None, None),
    peft_config=None,
    tools=None,
    rollout_func=None,
    environment_factory=None,
)
```

`RewardTrainer`:

```python
RewardTrainer(
    model,
    args=None,
    data_collator=None,
    train_dataset=None,
    eval_dataset=None,
    processing_class=None,
    compute_metrics=None,
    callbacks=None,
    optimizers=(None, None),
    optimizer_cls_and_kwargs=None,
    preprocess_logits_for_metrics=None,
    peft_config=None,
)
```

`RLOOTrainer`:

```python
RLOOTrainer(
    model,
    reward_funcs,
    args=None,
    train_dataset=None,
    eval_dataset=None,
    processing_class=None,
    reward_processing_classes=None,
    callbacks=None,
    optimizers=(None, None),
    peft_config=None,
)
```

## Important Config Knobs

All configs inherit the broad `TrainingArguments` surface: `output_dir`, batch sizes, `num_train_epochs`, `max_steps`, `learning_rate`, schedulers, optimizer, gradient accumulation, precision flags, logging, evaluation, saving, Hub push, seeds, dataloaders, `fsdp`, `deepspeed`, and distributed options.

Trainer-specific defaults and notable fields:

| Config | Starting learning rate | Notable fields |
| --- | --- | --- |
| `SFTConfig` | `2e-5` | `dataset_text_field`, `chat_template_path`, `max_length`, `packing`, `packing_strategy`, `completion_only_loss`, `assistant_only_loss`, `loss_type`, `activation_offloading` |
| `DPOConfig` | `1e-6` | `ref_model` handling, `max_length`, `precompute_ref_log_probs`, `loss_type`, `loss_weights`, `beta`, `label_smoothing`, `sync_ref_model` |
| `GRPOConfig` | `1e-6` | `num_generations`, `max_completion_length`, `use_vllm`, `vllm_mode`, `reward_weights`, `scale_rewards`, `loss_type`, `mask_truncated_completions`, tool and rollout controls |
| `RewardConfig` | `1e-4` | `max_length`, `center_rewards_coefficient`, sequence-classification initialization, `activation_offloading` |
| `RLOOConfig` | `1e-6` | `num_generations`, `max_completion_length`, `use_vllm`, `beta`, `normalize_advantages`, `reward_clip_range`, `mask_truncated_completions` |

## Model Arguments

For `SFTTrainer`, `DPOTrainer`, `GRPOTrainer`, `RewardTrainer`, and `RLOOTrainer`, `model` can be a model identifier string, a `transformers.PreTrainedModel`, or a PEFT model. When passing a string, config fields such as `model_init_kwargs` control model loading.

For reward modeling, the model is loaded as a sequence-classification reward model path where appropriate; TRL sets `num_labels=1` for RewardTrainer model initialization.

## Reference Models

DPO has an explicit `ref_model` constructor argument. GRPO and RLOO maintain a reference-policy relationship internally and expose knobs such as `beta`, `sync_ref_model`, `ref_model_mixup_alpha`, and `ref_model_sync_steps`.

Use `trl.create_reference_model(model)` when a custom reference model is needed outside a trainer workflow.

## Metrics To Watch

SFT:
`loss`, `entropy`, `mean_token_accuracy`, `num_tokens`, learning rate, grad norm.

DPO:
Preference losses and reward/margin trends. If the reward margin does not improve, inspect chosen/rejected formatting and reference log-prob setup.

GRPO/RLOO:
`reward`, per-reward means/stds, `reward_std`, `frac_reward_zero_std`, completion lengths, `kl`, `entropy`, clipping ratios. If `frac_reward_zero_std` is high, reward functions may be too coarse or generation diversity too low.

RewardTrainer:
`accuracy`, `mean_reward`, `margin`, and reward range. If accuracy is flat, verify that `chosen` really is preferred over `rejected`.
