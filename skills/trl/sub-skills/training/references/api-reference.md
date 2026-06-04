# Training API Reference

Read this when selecting trainer classes, constructing configs, or verifying public API expectations. Exact signatures can change; run `../../scripts/inspect_public_api.py` in the target environment when precision matters.

## Stable Top-Level Trainers

| Trainer | Config | Dataset type | Core extra inputs |
| --- | --- | --- | --- |
| `SFTTrainer` | `SFTConfig` | Language modeling or prompt-completion | Optional `processing_class`, `formatting_func`, `peft_config` |
| `DPOTrainer` | `DPOConfig` | Preference with `chosen` and `rejected`, optional `prompt` | Optional `ref_model`, `processing_class`, `peft_config` |
| `GRPOTrainer` | `GRPOConfig` | Prompt-only | Required `reward_funcs`; optional `tools`, `rollout_func`, `environment_factory` |
| `RLOOTrainer` | `RLOOConfig` | Prompt-only | Reward functions or reward model path depending on script/API workflow |
| `RewardTrainer` | `RewardConfig` | Preference with `chosen` and `rejected` | Optional `processing_class`, `peft_config`, `compute_metrics` |

## Constructor Shapes

The inspected installed package exposed these important shapes:

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

`RLOOTrainer` has the same broad Trainer-style shape but should be inspected in the installed environment when writing exact constructor code.

## Key Config Defaults

All trainer configs inherit many `transformers.TrainingArguments` fields. The most useful TRL-specific and training-control fields are below.

### `SFTConfig`

Important defaults from the inspected package:

- `learning_rate=2e-5`
- `per_device_train_batch_size=8`
- `num_train_epochs=3.0`
- `gradient_checkpointing=True`
- `report_to="none"`
- `dataset_text_field="text"`
- `max_length=1024`
- `packing=False`
- `packing_strategy="bfd"`
- `padding_free=False`
- `completion_only_loss=None`
- `assistant_only_loss=False`
- `loss_type="nll"`
- `activation_offloading=False`

Use `loss_type="chunked_nll"` for a memory-efficient standard SFT loss when compatible. Use `loss_type="dft"` for Dynamic Fine-Tuning when following that paper recipe.

### `DPOConfig`

Important defaults:

- `learning_rate=1e-6`
- `max_length=1024`
- `padding_free=False`
- `beta=0.1`
- `disable_dropout=True`
- `precompute_ref_log_probs=False`
- `loss_type` defaults to a list factory in the inspected package.
- `sync_ref_model=False`
- `activation_offloading=False`

Use `ref_model` when you need an explicit reference model. If omitted, TRL can create or manage a reference model depending on the model and config path.

### `GRPOConfig`

Important defaults:

- `learning_rate=1e-6`
- `num_generations=8`
- `max_completion_length=256`
- `use_vllm=False`
- `vllm_mode="colocate"`
- `vllm_server_host="0.0.0.0"`
- `vllm_server_port=8000`
- `vllm_gpu_memory_utilization=0.3`
- `vllm_tensor_parallel_size=1`
- `beta=0.0`
- `loss_type="dapo"`
- `reward_weights=None`
- `sync_ref_model=False`

GRPO is the main stable trainer for math/reasoning reward functions, tool-calling, and environment-based agent training.

### `RLOOConfig`

Important defaults:

- `learning_rate=1e-6`
- `num_generations=2`
- `max_completion_length=256`
- `use_vllm=False`
- `vllm_mode="colocate"`
- `beta=0.05`
- `reward_weights=None`
- `sync_ref_model=False`

RLOO computes leave-one-out baselines over generated completions.

### `RewardConfig`

Important defaults:

- `learning_rate=1e-4`
- `max_length=1024`
- `chat_template_path=None`
- `center_rewards_coefficient=None`
- `activation_offloading=False`
- `disable_dropout=True`

For LoRA reward modeling, use `lora_task_type="SEQ_CLS"`.

### `ModelConfig`

Useful fields for script-style workflows:

- `model_name_or_path`
- `model_revision="main"`
- `dtype="float32"` with choices such as `auto`, `bfloat16`, `float16`, `float32`
- `trust_remote_code=False`
- `attn_implementation=None`
- `use_peft=False`
- `lora_r=16`, `lora_alpha=32`, `lora_dropout=0.05`
- `lora_task_type="CAUSAL_LM"`
- `load_in_8bit=False`, `load_in_4bit=False`
- `bnb_4bit_quant_type="nf4"`

`load_in_8bit` and `load_in_4bit` are mutually exclusive.

## Stable Helpers

```python
from trl import create_reference_model
from trl import get_kbit_device_map, get_peft_config, get_quantization_config
from trl import ModelConfig
```

Use these when reproducing TRL scripts:

```python
model_args = ModelConfig(
    model_name_or_path="Qwen/Qwen2.5-0.5B",
    use_peft=True,
    lora_r=16,
)
peft_config = get_peft_config(model_args)
quantization_config = get_quantization_config(model_args)
device_map = get_kbit_device_map()
```

## Callbacks

Top-level callback exports include:

- `LogCompletionsCallback`
- `RichProgressCallback`
- `SyncRefModelCallback`
- `WeaveCallback`
- `BEMACallback`

Use normal Transformers callback patterns:

```python
trainer.add_callback(callback)
```

or pass `callbacks=[...]` in the trainer constructor.
