# PEFT Skill Usability Test Cases

These cases exercise the generated `peft` skill and its sub-skills with natural future-user prompts. The prompts intentionally avoid local checkout paths and temporary inspection environment details.

| Case directory | Skill area | User role | Scenario | Capability | Difficulty |
| --- | --- | --- | --- | --- | --- |
| `peft-install-smoke-check` | root skill | New PEFT user | Set up PEFT and verify imports | Installation, import check, dependency sanity | Basic |
| `adapter-training-lora-sequence-classification-head` | `adapter-training` | Applied ML engineer | Train LoRA for sequence classification with a classifier head | `LoraConfig`, `TaskType.SEQ_CLS`, `modules_to_save`, saving adapters | Intermediate |
| `adapter-training-soft-prompt-causal-lm` | `adapter-training` | NLP practitioner | Choose and configure prompt tuning for a causal LM | Prompt tuning, virtual tokens, custom loop shape | Intermediate |
| `adapter-loading-and-composition-bad-loaded-results` | `adapter-loading-and-composition` | Debugging user | Adapter loads but predictions are random | Correct `PeftModel.from_pretrained`, task head, tokenizer/embedding checks | Troubleshooting |
| `adapter-loading-and-composition-merge-three-adapters` | `adapter-loading-and-composition` | Experienced PEFT user | Load and merge several LoRA adapters | `load_adapter`, `add_weighted_adapter`, `set_adapter`, merge caveats | Advanced |
| `quantization-and-optimization-qlora-setup` | `quantization-and-optimization` | LLM finetuning user | Configure 4-bit QLoRA | bitsandbytes, `prepare_model_for_kbit_training`, `target_modules="all-linear"` | Intermediate |
| `quantization-and-optimization-torch-compile-validation` | `quantization-and-optimization` | Performance-focused engineer | Use `torch.compile` safely with adapters | Adapter load order, compiled/uncompiled validation, graph-break caution | Advanced |
| `custom-peft-development-custom-mlp-lora` | `custom-peft-development` | PyTorch developer | Apply LoRA to a custom MLP | `named_modules`, custom targets, `modules_to_save`, smoke tests | Intermediate |
| `custom-peft-development-new-method-pr` | `custom-peft-development` | Contributor | Add a new PEFT method | `PeftType`, tuner package, registration, tests, docs, AI disclosure | Advanced |
| `custom-peft-development-low-level-injection` | `custom-peft-development` | Library integrator | Use adapter injection without `PeftModel` | `inject_adapter_in_model`, state dict helpers, tradeoffs | Advanced |

Coverage note: the cases cover the root skill plus every generated sub-skill. They include setup, ordinary adapter training, prompt methods, loading/debugging, multi-adapter composition, quantized training, performance validation, custom model use, low-level APIs, and contribution workflows. No major capability from `skills/peft/references/evidence-and-capabilities.md` is intentionally left untested.
