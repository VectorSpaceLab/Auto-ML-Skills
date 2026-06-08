---
name: custom-peft-development
description: "Use this sub-skill for applying PEFT to custom torch modules, low-level adapter injection, custom LoRA modules, adding PEFT methods, extending model mappings, writing PEFT tests, and preparing PEFT contributions."
---

# Custom PEFT Development

Use this sub-skill when a user is applying PEFT outside standard Transformers wrappers, targeting a custom model, using `inject_adapter_in_model`, registering custom LoRA module dispatch, adding a new PEFT method, extending default target-module mappings, or preparing a PEFT repository contribution.

Read `references/custom-models-and-low-level-api.md` for custom `torch.nn.Module` adaptation, target discovery, low-level injection, and manual state-dict handling.

Read `references/new-method-pr-checklist.md` for adding a new PEFT method and meeting contribution/test requirements.

Run `scripts/smoke_custom_lora.py` to verify that a simple custom `torch.nn.Module` can be adapted, trained enough to produce gradients, saved, and reloaded through PEFT.

## Contribution Warning

For `huggingface/peft`, breaching AI-assisted contribution guidelines can result in automatic banning. A human submitter must understand and review every changed line, coordinate with maintainers before PR work, run relevant tests, and disclose AI assistance in the PR description.

## Custom Model Flow

1. Print `named_modules()` for the base model.
2. Choose supported target modules such as `nn.Linear`, embeddings, Conv layers, or supported Transformers `Conv1D`.
3. Add task heads or output layers to `modules_to_save` if they must train without adapters.
4. Wrap with `get_peft_model` for normal PEFT utilities, or use `inject_adapter_in_model` for raw module injection.
5. Verify trainable parameters and targeted names.
6. Write a focused test that covers forward pass, backward pass, save/load, and merge only if the method supports merge.

## Low-Level Injection

```python
from peft import LoraConfig, inject_adapter_in_model

config = LoraConfig(target_modules=["linear"], r=8, lora_alpha=16)
model = inject_adapter_in_model(config, model)
```

Low-level injection modifies the model in place and does not provide every `PeftModel` utility. Use `get_peft_model_state_dict` and `set_peft_model_state_dict` for manual save/load.

## New Method Flow

Adding a new PEFT method is a substantial PR, not a tiny cleanup:

1. Open or join an approved proposal issue.
2. Add `PeftType`.
3. Create `src/peft/tuners/<method>/`.
4. Implement config/model/layer files as needed.
5. Register with `register_peft_method`.
6. Export public classes.
7. Add target-module mappings if needed.
8. Add tests in the existing method matrices.
9. Add docs, examples, and benchmark settings when appropriate.
10. Run focused tests and `make style`.

## Test Selection

For method-specific changes:

```bash
pytest tests/ -k "ia3"
pytest tests/ -k "lora and not adalora and not randlora"
pytest tests/test_custom_models.py -k "<method-name>" -v
```

Ensure the selector runs at least one test. If no tests cover the behavior, add tests in the matching existing test file.
