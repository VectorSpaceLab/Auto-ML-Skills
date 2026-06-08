# Loading And Checkpoints

Use this reference for PEFT adapter checkpoint layout and loading choices.

## Adapter Checkpoint Files

`PeftModel.save_pretrained` normally writes:

- `adapter_config.json`: adapter method and settings, including `peft_type`, `target_modules`, `task_type`, `base_model_name_or_path`, and revision where known.
- `adapter_model.safetensors` by default, or `adapter_model.bin` when safe serialization is disabled.
- `README.md`: model card metadata; not required for loading.

The adapter weight file stores adapter parameters, not the full base model. A user needs the compatible base model to load and run the adapter.

For LoRA, adapter state-dict keys commonly include path segments such as:

```text
base_model.model.<module-path>.lora_A.weight
base_model.model.<module-path>.lora_B.weight
```

Internally, loaded model parameter names may include the adapter name, such as `.lora_A.default.weight`; PEFT strips the adapter name when saving.

## Manual Load Pattern

Use this when the user needs control over base model arguments, tokenizer resizing, quantization, dtype, or device mapping:

```python
from peft import PeftConfig, PeftModel
from transformers import AutoModelForCausalLM

adapter_id = "path-or-hub-id"
config = PeftConfig.from_pretrained(adapter_id)
base_model = AutoModelForCausalLM.from_pretrained(
    config.base_model_name_or_path,
    revision=config.revision,
)
model = PeftModel.from_pretrained(base_model, adapter_id)
```

If the adapter was trained after adding tokens:

```python
tokenizer.add_tokens(new_tokens)
base_model.resize_token_embeddings(len(tokenizer))
model = PeftModel.from_pretrained(base_model, adapter_id)
```

## AutoPeft Load Pattern

Use this when the adapter config is complete and the user does not need custom base-model setup:

```python
from peft import AutoPeftModelForCausalLM

model = AutoPeftModelForCausalLM.from_pretrained(adapter_id, device_map="auto")
```

Available classes:

- `AutoPeftModel`
- `AutoPeftModelForCausalLM`
- `AutoPeftModelForSeq2SeqLM`
- `AutoPeftModelForSequenceClassification`
- `AutoPeftModelForTokenClassification`
- `AutoPeftModelForQuestionAnswering`
- `AutoPeftModelForFeatureExtraction`

If `AutoPeftModel` reports it cannot infer the class, use a task-specific `AutoPeftModelFor*` class or the manual `PeftConfig` plus base-model load path.

If AutoPeft reports an import allowlist error, inspect the adapter config `auto_mapping`. Add only trusted package import names:

```python
model = AutoPeftModel.from_pretrained(adapter_id, import_allowlist=["transformers", "my_safe_package"])
```

## Saving Adapters

```python
model.save_pretrained("adapter-output", safe_serialization=True)
```

Options to consider:

- `selected_adapters=["name"]`: save only selected adapters.
- `save_embedding_layers=True`: save embeddings when resized or trained.
- `save_embedding_layers=False`: avoid full embedding save only when safe.
- `path_initial_model_for_weight_conversion`: used by some conversion flows.

For non-default adapter names, PEFT may save the adapter under a matching subdirectory.

## Saving Full Merged Models

```python
merged = model.merge_and_unload()
merged.save_pretrained("full-model-output")
```

This creates a regular base-model checkpoint and removes PEFT adapter controls. Use only when the target adapter method and quantization setting support merge and the user wants a full model.

## Conversion Notes

When converting external adapters into PEFT format:

1. Create an `adapter_config.json` with at least `peft_type` and method-specific required fields such as `target_modules`.
2. Map weight keys into PEFT's expected naming.
3. Prefer `safetensors` for adapter weights.
4. Test by loading a base model, applying `PeftModel.from_pretrained`, and running a deterministic small input.

For LoRA, make sure adapter A/B weights and any variant-specific weights such as DoRA magnitude vectors are represented.
