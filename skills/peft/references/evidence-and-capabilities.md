# Evidence And Capability Map

Use this reference to understand what this generated skill covers and why the sub-skill boundaries exist.

## Evidence Used

| Evidence source | Why it matters | Skill use |
| --- | --- | --- |
| `setup.py`, `pyproject.toml` | Package name, dependencies, Python support, style tooling | Root install guidance and contribution checks |
| `src/peft/` | Canonical source root and public API exports | API signatures, config families, adapter behavior |
| `src/peft/tuners/` | PEFT method implementations | Adapter method routing, custom development guidance |
| `src/peft/auto.py`, `peft_model.py`, `mapping_func.py`, `mixed_model.py` | Loading, wrapping, AutoPeft, and mixed adapters | Loading/composition sub-skill |
| `src/peft/utils/peft_types.py`, mapping tables | Adapter types, task types, method registration | API reference and custom method workflow |
| `docs/source/install.md`, `quicktour.md` | Public installation and core train/inference pattern | Root workflow and adapter-training sub-skill |
| `docs/source/task_guides/` | LoRA, prompt-based, and IA3 task examples | Adapter-training workflows |
| `docs/source/developer_guides/` | LoRA variants, quantization, checkpoint format, low-level API, custom models, merging, troubleshooting, torch.compile, contributing | Sub-skill references and troubleshooting |
| `docs/source/package_reference/` | Public reference catalog | API coverage |
| `examples/` | Training and conversion patterns across LoRA variants, SFT, DreamBooth, quantization, SD, X-LoRA, etc. | Workflow examples and test scenarios |
| `tests/` | Behavior evidence, edge cases, test selectors, method matrices | Troubleshooting, custom development, verification strategy |
| Installed package inspection | Live import success, signatures, mapping tables, version facts | Verified API reference and smoke-test script |

## Coverage Matrix

| Capability | Output location | Depth check |
| --- | --- | --- |
| Install and import PEFT | Root `SKILL.md`, `scripts/check_peft_environment.py` | Public install commands, version check, import symbols, dependency check |
| Configure and train adapters | `sub-skills/adapter-training/` | Method selection, config examples, target modules, Trainer/custom loop, save adapter |
| LoRA and variants | `sub-skills/adapter-training/references/method-selection.md`, `workflows.md` | LoRA, AdaLoRA, LoHa, LoKr, DoRA, rsLoRA, initialization variants, trainable tokens |
| Prompt and prefix methods | `sub-skills/adapter-training/references/method-selection.md`, `workflows.md` | Prompt tuning, p-tuning, prefix tuning, virtual token parameters, task fit |
| IA3 and lightweight non-LoRA methods | `sub-skills/adapter-training/references/method-selection.md` | Config shape, `feedforward_modules`, seq2seq fit |
| Save/load checkpoints | `sub-skills/adapter-loading-and-composition/` | `PeftConfig`, `PeftModel.from_pretrained`, `AutoPeftModel*`, checkpoint files |
| Multiple adapters and merging | `sub-skills/adapter-loading-and-composition/references/composition-and-merging.md` | `load_adapter`, `set_adapter`, `disable_adapter`, `add_weighted_adapter`, `merge_and_unload`, mixed adapters |
| Adapter state debugging | `sub-skills/adapter-loading-and-composition/scripts/inspect_adapter_state.py`, root troubleshooting | Status methods, irregular states, wrong-load failures |
| Quantized PEFT | `sub-skills/quantization-and-optimization/` | bitsandbytes QLoRA, `prepare_model_for_kbit_training`, LoftQ, GPTQ/AQLM/EETQ/HQQ/torchao/INC caveats |
| Performance and dtype | `sub-skills/quantization-and-optimization/references/performance.md`, root troubleshooting | AMP dtype errors, adapter autocast, DoRA offload, `torch.compile`, low-memory flags |
| Custom models and low-level injection | `sub-skills/custom-peft-development/references/custom-models-and-low-level-api.md` | Non-Transformers models, `target_modules`, `modules_to_save`, `inject_adapter_in_model`, custom module mapping |
| New PEFT methods and repo PRs | `sub-skills/custom-peft-development/references/new-method-pr-checklist.md` | Maintainer approval, `PeftType`, tuner package, registration, docs/examples/tests, AI disclosure |

## Known Scope Limits

This skill intentionally does not embed every example script from PEFT. Many examples download models or datasets, require GPUs, or train for long periods. Instead, the skill distills repeatable patterns and provides safe diagnostic scripts.

For exact behavior in a specific PEFT version, run the bundled environment check and inspect signatures in the user's installed environment.
