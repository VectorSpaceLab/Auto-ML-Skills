---
name: adapter-loading-and-composition
description: "Use this sub-skill for loading PEFT adapters, AutoPeftModel classes, checkpoint files, multi-adapter workflows, adapter switching, merging, mixed adapters, and debugging adapter state."
---

# Adapter Loading And Composition

Use this sub-skill when a user wants to load a trained PEFT adapter, deploy it for inference, inspect checkpoint files, use `AutoPeftModel*`, attach more than one adapter, set active adapters, disable adapters, merge or unload adapter weights, or debug wrong outputs after loading.

Read `references/loading-checkpoints.md` for correct loading paths, checkpoint file contents, adapter config handling, and save/load caveats.

Read `references/composition-and-merging.md` for `load_adapter`, `set_adapter`, `disable_adapter`, `add_weighted_adapter`, `PeftMixedModel`, `merge_and_unload`, and model-status debugging.

Run `scripts/inspect_adapter_state.py` inside a user's project when they already have a `model` object and need to inspect active, merged, enabled, and available adapters.

## Correct Loading Paths

Load a trained adapter by loading a compatible base model first:

```python
from peft import PeftConfig, PeftModel
from transformers import AutoModelForCausalLM

adapter_id = "namespace/adapter-repo"
config = PeftConfig.from_pretrained(adapter_id)
base_model = AutoModelForCausalLM.from_pretrained(config.base_model_name_or_path)
model = PeftModel.from_pretrained(base_model, adapter_id)
model.eval()
```

Use `AutoPeftModelForCausalLM.from_pretrained(adapter_id)` when the adapter config is sufficient to load the base model automatically:

```python
from peft import AutoPeftModelForCausalLM

model = AutoPeftModelForCausalLM.from_pretrained(adapter_id)
model.eval()
```

Do not use `get_peft_model` to load trained adapter weights. That creates a newly initialized PEFT model.

## Multiple Adapters

```python
model = PeftModel.from_pretrained(base_model, first_adapter, adapter_name="first")
model.load_adapter(second_adapter, adapter_name="second")
model.set_adapter("second")
```

For inference with compatible mixed adapter types:

```python
from peft import PeftMixedModel

model = PeftMixedModel.from_pretrained(base_model, first_adapter, adapter_name="lora")
model.load_adapter(second_adapter, adapter_name="loha")
model.set_adapter(["lora", "loha"])
```

`PeftMixedModel` is mainly for inference-time composition. It does not save a combined mixed-adapter checkpoint.

## Merge For Standalone Inference

```python
merged_model = model.merge_and_unload()
merged_model.save_pretrained("merged-full-model")
```

Merging can speed up inference and produce a regular base-model object, but it removes PEFT-specific adapter controls. Not every PEFT method and quantization setting supports merging.

## Debug Adapter State

```python
print(model.get_model_status())
for layer in model.get_layer_status():
    print(layer)
```

If status fields show `"irregular"`, reload the base model and adapters. Irregular states usually mean active, merged, enabled, or trainable settings differ across target layers.

## Common Mistakes

- Loading a classification adapter without saving/loading the trained classification head.
- Loading an adapter on a base model with different tokenizer size or revision than training.
- Merging into a quantized model when that quantization path does not support merge.
- Forgetting `model.set_adapter(...)` after adding a second adapter.
- Assuming `PeftMixedModel` can save a single mixed checkpoint.
- Passing unsafe `import_allowlist` values for AutoPeft dynamic imports.
