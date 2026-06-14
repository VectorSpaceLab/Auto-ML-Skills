# PEFT Troubleshooting

Use this reference when PEFT imports, training, loading, merging, or inference behave unexpectedly.

## First Checks

Run:

```bash
python -m pip check
python - <<'PY'
import peft, torch, transformers, accelerate
print("peft", peft.__version__)
print("torch", torch.__version__, "cuda", torch.version.cuda, torch.cuda.is_available())
print("transformers", transformers.__version__)
print("accelerate", accelerate.__version__)
PY
```

If working from source, install editable with tests:

```bash
python -m pip install -e ".[test]"
```

## Wrong Way To Load A Trained Adapter

Symptom: output quality is random, adapter appears initialized but learned behavior is missing, or a user calls `get_peft_model(base_model, config)` for inference.

Cause: `get_peft_model` creates a PEFT model from a config; it does not load trained adapter weights.

Fix:

```python
from peft import PeftConfig, PeftModel
from transformers import AutoModelForCausalLM

adapter_id = "path-or-hub-id"
config = PeftConfig.from_pretrained(adapter_id)
base_model = AutoModelForCausalLM.from_pretrained(config.base_model_name_or_path)
model = PeftModel.from_pretrained(base_model, adapter_id)
model.eval()
```

Use `AutoPeftModelForCausalLM.from_pretrained(adapter_id)` only when the adapter config can safely infer and load the base model.

## Repeated `get_peft_model` Warning

Symptom: warning similar to trying to modify a model with PEFT for a second time.

Cause: the model already contains PEFT tuner layers.

Fix: reload the base model or call `.unload()` before applying a different PEFT config:

```python
peft_model = get_peft_model(base_model, old_config)
base_model = peft_model.unload()
peft_model = get_peft_model(base_model, new_config)
```

## Target Modules Not Found

Symptom: PEFT cannot find `target_modules`, trainable parameter count is zero, or unexpected layers are adapted.

Fix:

```python
for name, module in model.named_modules():
    if any(key in name for key in ["q_proj", "v_proj", "query", "value", "linear", "fc", "dense"]):
        print(name, type(module))
```

Then set `target_modules` to exact names, suffixes, a regex string, or `"all-linear"` for QLoRA-style LoRA across linear layers. For non-Transformers models, target names must come from `named_modules()`.

After wrapping, verify:

```python
model.print_trainable_parameters()
print(getattr(model, "targeted_module_names", None))
```

## Random Classification Head Or Missing `modules_to_save`

Symptom: a loaded adapter performs randomly on sequence classification, token classification, or another task with a newly initialized head.

Cause: the task head was trained but not saved with the adapter.

Fix: pass the right `task_type` and/or include the head in `modules_to_save`:

```python
from peft import LoraConfig, TaskType

config = LoraConfig(
    task_type=TaskType.SEQ_CLS,
    target_modules=["query", "value"],
    modules_to_save=["classifier"],
)
```

If Transformers warns that a layer was newly initialized, check whether that layer should be in `modules_to_save`.

## Added Tokens Or Resized Embeddings

Symptom: size mismatch when loading, missing learned behavior for new tokens, or huge adapter files after resizing embeddings.

Fix sequence:

```python
new_tokens = ["<new>"]
tokenizer.add_tokens(new_tokens)
base_model.resize_token_embeddings(len(tokenizer))
```

Then choose one of:

- `trainable_token_indices` to train only new token embeddings.
- Include embedding/lm-head names in `target_modules` for adapter training.
- Include embedding/lm-head names in `modules_to_save` for full head/embedding finetuning.

During inference, resize the base model the same way before loading the adapter. If safe, pass `save_embedding_layers=False` to avoid saving the full embedding matrix when trainable tokens track the changes.

## AMP Or Dtype Errors

Symptom: `ValueError: Attempting to unscale FP16 gradients`.

Cause: trainable adapter weights are in fp16 while automatic mixed precision expects trainable weights to be fp32.

Fix:

```python
from peft import cast_mixed_precision_params

peft_model = get_peft_model(base_model, config)
cast_mixed_precision_params(peft_model, dtype=torch.float16)
```

Or manually promote trainable parameters to float:

```python
for param in peft_model.parameters():
    if param.requires_grad:
        param.data = param.data.float()
```

By default, PEFT promotes many fp16/bf16 adapter weights to fp32 for stable training. Override with `autocast_adapter_dtype=False` only when the memory/speed tradeoff is deliberate.

## Irregular Adapter State

Symptoms: active adapters, merged adapters, enabled flags, or devices differ across layers; outputs are wrong after partial merge/switch operations.

Fix:

```python
status = model.get_model_status()
print(status)
for layer in model.get_layer_status():
    print(layer)
```

Look for `"irregular"` values. If present, reload the base model and adapters from checkpoints. Avoid manually merging only some target modules.

For non-`PeftModel` objects that still contain PEFT layers, use top-level helpers:

```python
from peft import get_layer_status, get_model_status
```

## Quantized Merge Or LoftQ Problems

Common constraints:

- For QLoRA-style training, call `prepare_model_for_kbit_training` before `get_peft_model`.
- Use `target_modules="all-linear"` when adapting all linear layers is the intended QLoRA behavior.
- LoftQ replacement with `replace_lora_weights_loftq` is limited and expects compatible LoRA and quantization settings.
- Merging adapters into quantized weights is not supported for every quantizer or adapter method.
- AQLM adapters should remain separate because merging into AQLM quantized weights is not possible.
- torchao merge support is most reliable for LoRA with `int8_weight_only`; other methods/dtypes may be incorrect or fail.
- INC-quantized models do not support `merge()` or `unmerge()` in the documented path.

When in doubt, keep base model and adapter separate for deployment:

```python
model = PeftModel.from_pretrained(base_model, adapter_id)
```

## `torch.compile` Caveats

PEFT can work with `torch.compile` for training, inference, generation, merging, quantized LoRA, multiple adapters, and several adapter types. Dynamic behavior can still cause graph breaks or incorrect output.

Best practice:

- Load all adapters before calling `torch.compile`.
- Test the uncompiled and compiled models on the same small input.
- Do not assume absence of errors means correctness.

## Contribution And AI-Assisted PR Pitfalls

For `huggingface/peft`, AI-assisted contribution guideline breaches can result in automatic banning.

Before PR work:

- Read the repository contribution guide.
- Check overlapping issues and PRs.
- Get maintainer approval before working on an existing issue or new feature.
- Avoid one-off tiny edits.
- The human submitter must understand and review every changed line.
- PR descriptions for AI-assisted work must include issue coordination, tests run, pass/fail status, and a clear AI-assistance statement.

Testing:

- For bug fixes, write a failing test first.
- Run focused tests with selectors that do not deselect all tests.
- For GPU-only changes, place tests in GPU test files and run the relevant GPU tests.
- Run `make style`, using the ruff version pinned by repo metadata.
