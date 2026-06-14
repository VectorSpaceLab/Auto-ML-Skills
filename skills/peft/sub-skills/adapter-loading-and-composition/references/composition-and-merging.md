# Composition And Merging

Use this reference for multi-adapter workflows and merge behavior.

## Add And Switch Adapters

```python
from peft import PeftModel

model = PeftModel.from_pretrained(base_model, adapter_a, adapter_name="a")
model.load_adapter(adapter_b, adapter_name="b")

model.set_adapter("a")
model.set_adapter("b")
```

The newly loaded adapter is not automatically active in every workflow. Call `set_adapter` explicitly.

To disable adapters temporarily:

```python
with model.disable_adapter():
    base_outputs = model(**inputs)
```

If the adapter has bias settings that alter base behavior, disabling can warn or produce behavior that is not identical to the original base model.

## Multiple Active Adapters

Some PEFT layers support multiple active adapters:

```python
model.base_model.set_adapter(["default", "other"])
```

Use this only when the method supports the intended combination. If active adapters are set inconsistently across layers, status inspection may report `"irregular"`.

## Mixed Adapter Types

Use `PeftMixedModel` when the user wants to combine different compatible adapter types for inference:

```python
from peft import PeftMixedModel

model = PeftMixedModel.from_pretrained(base_model, lora_adapter, adapter_name="lora")
model.load_adapter(loha_adapter, adapter_name="loha")
model.set_adapter(["lora", "loha"])
```

Mixed-compatible PEFT types include LoRA, AdaLoRA, IA3, BEFT, LoHa, LoKr, ROAD, Hira, and Shira in the inspected repo state.

Limitations:

- Not every PEFT type is compatible.
- Mixed-adapter training is not the recommended path.
- `PeftMixedModel` does not save and reload mixed adapters as one combined checkpoint.
- Loading order can affect performance and output; group same adapter types together when possible for speed.

## Weighted Adapter Merge

For LoRA-style adapter combination:

```python
model.load_adapter(adapter_b, adapter_name="b")
model.add_weighted_adapter(
    adapters=["default", "b"],
    weights=[1.0, 0.7],
    adapter_name="merged",
    combination_type="ties",
    density=0.2,
)
model.set_adapter("merged")
```

Common `combination_type` values include linear-style combinations and methods such as TIES/DARE variants where supported by the tuner.

IA3 supports `add_weighted_adapter` without the same `combination_type` parameter:

```python
model.add_weighted_adapter(["a", "b"], weights=[0.5, 0.5], adapter_name="merged")
model.set_adapter("merged")
```

Parameter-targeted adapters may not support `add_weighted_adapter`.

## Merge And Unload

```python
merged_model = model.merge_and_unload(safe_merge=True)
```

Use this when:

- The user wants a full standalone base model with adapter weights folded in.
- The method supports merging.
- Quantization settings allow correct merging.
- The user no longer needs adapter switching, disabling, or PEFT-specific controls.

Do not use it when:

- The user needs multiple adapters at runtime.
- The adapter method does not support merge.
- The quantizer documents merge limitations.
- The user wants to keep adapter files small and separate from the base model.

## Status Inspection

```python
status = model.get_model_status()
layers = model.get_layer_status()
```

Use this to inspect:

- Base model type.
- Adapter model type.
- PEFT types by adapter name.
- Trainable and total parameter counts.
- Active adapters.
- Merged adapters.
- Available adapters.
- Whether adapters are enabled.

If status fields contain `"irregular"`, reload the model and adapter checkpoints. Irregular state means at least one adapter/layer differs from the rest, which can invalidate outputs.
