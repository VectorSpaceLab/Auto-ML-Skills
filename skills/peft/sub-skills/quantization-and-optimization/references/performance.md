# Performance, Dtype, And Compile

Use this reference for PEFT performance and memory decisions.

## Adapter Dtype

PEFT commonly keeps adapter weights in float32 for stable training even when the base model uses fp16 or bf16. This is usually a good default because adapters are small relative to the base model.

If a user deliberately wants lower precision adapter weights:

```python
model = get_peft_model(base_model, config, autocast_adapter_dtype=False)
```

Risk: lower precision adapter weights can be smaller and slightly faster, but can underflow/overflow or degrade loss.

For mixed precision training:

```python
from peft import cast_mixed_precision_params

cast_mixed_precision_params(model, dtype=torch.float16)
```

## Low CPU Memory

Use `low_cpu_mem_usage=True` for faster/lower-memory adapter loading or initialization on very large models:

```python
model = get_peft_model(base_model, config, low_cpu_mem_usage=True)
model = PeftModel.from_pretrained(base_model, adapter_id, low_cpu_mem_usage=True)
```

Do not leave meta-device adapter weights unfilled before training. This flag is best for load flows where weights are immediately populated.

## DoRA Performance

DoRA can improve quality but adds overhead. It is optimized for evaluation mode or zero dropout because PEFT can reuse base results.

For offloaded DoRA adapters:

```python
from peft import LoraConfig, LoraRuntimeConfig

config = LoraConfig(
    use_dora=True,
    runtime_config=LoraRuntimeConfig(ephemeral_gpu_offload=True),
)
```

For loading:

```python
model = PeftModel.from_pretrained(base_model, adapter_id, ephemeral_gpu_offload=True)
```

For inference, consider merging if supported:

```python
model = model.merge_and_unload()
```

## KappaTune Target Selection

Use `find_kappa_target_modules` to select LoRA targets by condition-number heuristics:

```python
from peft.helpers import find_kappa_target_modules

targets = find_kappa_target_modules(model, top_p=0.2)
config = LoraConfig(
    target_modules=targets["target_modules"],
    target_parameters=targets["target_parameters"],
)
```

This can be expensive because it scans layers and computes condition numbers. Use it when target selection quality matters more than setup time.

## torch.compile

Documented working areas include training, inference, generation, merging, disabling adapters, unloading, multiple adapters, mixed adapter batches, and bitsandbytes quantization for tested adapter types.

Practical workflow:

```python
# Load base model and all adapters first.
model.load_adapter(adapter_b, adapter_name="b")
model.set_adapter("default")

compiled_model = torch.compile(model)
```

Verify correctness:

```python
model.eval()
compiled_model.eval()
with torch.no_grad():
    expected = model(**batch)
    actual = compiled_model(**batch)
```

Compare relevant tensors or generation output. Do not assume success from lack of exceptions alone.

## Trainer And Batch Size

Because PEFT trains a small parameter subset, users can often raise learning rates and batch sizes compared with full finetuning. Still verify memory and loss. LoRA-like examples often use higher learning rates such as `1e-3` to `5e-3` depending on task and model, but exact values are task-specific.

## Safe Merge Checks

Use:

```python
merged = model.merge_and_unload(safe_merge=True)
```

When quantized, compiled, or using variant adapters, run a small output comparison before and after merge. If outputs differ unexpectedly or merge fails, keep adapter and base model separate.
