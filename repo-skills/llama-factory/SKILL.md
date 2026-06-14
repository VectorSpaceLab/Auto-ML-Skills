---
name: llama-factory
description: "Use when a user wants an agent to run LLaMA-Factory training, preference optimization, inference, serving, export, preprocessing, evaluation, benchmark, and checkpoint-conversion workflows from natural language using a public package install and bundled helper scripts."
disable-model-invocation: true
---

# LLaMA-Factory

This is the router for the LLaMA-Factory repo skill. Use it to choose the focused sub-skill, then read only that sub-skill plus the linked bundled references/scripts. Do not reopen the original source checkout or rely on the inspection environment used to create this skill.

## Public Install

Prefer a clean Python environment that satisfies Python 3.11 or newer.

```bash
python -m pip install -U pip setuptools wheel
pip install llamafactory
python -c "import llamafactory; print(llamafactory.__name__)"
```

For unreleased features, install from the public repository instead of a private local checkout:

```bash
git clone https://github.com/hiyouga/LLaMA-Factory.git && pip install -e LLaMA-Factory
```

Run the bundled environment check after installation:

```bash
python scripts/check_llama_factory_env.py
```

See [references/installation.md](references/installation.md) for optional extras and backend notes. See [references/troubleshooting.md](references/troubleshooting.md) for cross-cutting failures.

## Route To Sub-Skills

- **Standalone PiSSA or LoftQ adapter initialization before training.**: [sub-skills/llamafactory-adapter-init-skill/SKILL.md](sub-skills/llamafactory-adapter-init-skill/SKILL.md)
- **LoRA variants such as LoRA+, rsLoRA, DoRA, PiSSA, OFT, and adapter continuation.**: [sub-skills/llamafactory-adapter-variants-skill/SKILL.md](sub-skills/llamafactory-adapter-variants-skill/SKILL.md)
- **OpenAI-compatible client payload tests, tool calls, and image messages.**: [sub-skills/llamafactory-api-client-tests-skill/SKILL.md](sub-skills/llamafactory-api-client-tests-skill/SKILL.md)
- **FLOPs, MFU, length CDF, Qwen benchmark, and training-stat utilities.**: [sub-skills/llamafactory-benchmark-stats-skill/SKILL.md](sub-skills/llamafactory-benchmark-stats-skill/SKILL.md)
- **HF-DCP checkpoint conversion, Megatron/Qwen-Omni merge, and tiny/llamafy utilities.**: [sub-skills/llamafactory-checkpoint-convert-skill/SKILL.md](sub-skills/llamafactory-checkpoint-convert-skill/SKILL.md)
- **Dataset registration, dataset_info mappings, tokenized cache creation, and cache inspection.**: [sub-skills/llamafactory-dataset-preprocess-skill/SKILL.md](sub-skills/llamafactory-dataset-preprocess-skill/SKILL.md)
- **torchrun, DeepSpeed, FSDP/FSDP2, Ray, and multi-node launch setup.**: [sub-skills/llamafactory-distributed-train-skill/SKILL.md](sub-skills/llamafactory-distributed-train-skill/SKILL.md)
- **Ascend NPU SFT/QLoRA/full tuning with FSDP/FSDP2 and Qwen/Qwen-VL recipes.**: [sub-skills/llamafactory-ascend-npu-skill/SKILL.md](sub-skills/llamafactory-ascend-npu-skill/SKILL.md)
- **KTransformers MoE LoRA training with FSDP2 and AMX BF16/INT8/INT4 expert backends.**: [sub-skills/llamafactory-ktransformers-skill/SKILL.md](sub-skills/llamafactory-ktransformers-skill/SKILL.md)
- **Megatron-Core full-parameter training for Qwen-VL and Qwen MoE models.**: [sub-skills/llamafactory-megatron-core-skill/SKILL.md](sub-skills/llamafactory-megatron-core-skill/SKILL.md)
- **Dynamic batching, padding-free training, Liger kernels, and Ulysses context parallel settings.**: [sub-skills/llamafactory-batching-kernels-skill/SKILL.md](sub-skills/llamafactory-batching-kernels-skill/SKILL.md)
- **DPO / ORPO / SimPO / pairwise preference optimization.**: [sub-skills/llamafactory-dpo-skill/SKILL.md](sub-skills/llamafactory-dpo-skill/SKILL.md)
- **BLEU, ROUGE, perplexity, learning-rate, and score inspection utilities.**: [sub-skills/llamafactory-eval-metrics-skill/SKILL.md](sub-skills/llamafactory-eval-metrics-skill/SKILL.md)
- **LoRA adapter export, merge, Modelfile generation, and exported artifact inspection.**: [sub-skills/llamafactory-export-merge-skill/SKILL.md](sub-skills/llamafactory-export-merge-skill/SKILL.md)
- **Freeze tuning and partial-parameter training.**: [sub-skills/llamafactory-freeze-tuning-skill/SKILL.md](sub-skills/llamafactory-freeze-tuning-skill/SKILL.md)
- **Offline chat, one-shot inference, batch prediction, and adapter inference.**: [sub-skills/llamafactory-inference-skill/SKILL.md](sub-skills/llamafactory-inference-skill/SKILL.md)
- **KTO training from binary desirable/undesirable feedback.**: [sub-skills/llamafactory-kto-skill/SKILL.md](sub-skills/llamafactory-kto-skill/SKILL.md)
- **Vision-language or multimodal SFT data validation and training configs.**: [sub-skills/llamafactory-multimodal-sft-skill/SKILL.md](sub-skills/llamafactory-multimodal-sft-skill/SKILL.md)
- **OpenAI-compatible API server launch, health check, and shutdown.**: [sub-skills/llamafactory-openai-api-skill/SKILL.md](sub-skills/llamafactory-openai-api-skill/SKILL.md)
- **PPO / RLHF policy optimization that requires a reward model or reward API.**: [sub-skills/llamafactory-ppo-skill/SKILL.md](sub-skills/llamafactory-ppo-skill/SKILL.md)
- **Continued pretraining / causal LM pretraining on raw text.**: [sub-skills/llamafactory-pt-skill/SKILL.md](sub-skills/llamafactory-pt-skill/SKILL.md)
- **QLoRA and 4-bit or 8-bit LoRA training.**: [sub-skills/llamafactory-qlora-skill/SKILL.md](sub-skills/llamafactory-qlora-skill/SKILL.md)
- **Reward model training and pairwise preference scoring.**: [sub-skills/llamafactory-rm-skill/SKILL.md](sub-skills/llamafactory-rm-skill/SKILL.md)
- **SFT / supervised fine-tuning / instruction tuning / chat fine-tuning.**: [sub-skills/llamafactory-sft-skill/SKILL.md](sub-skills/llamafactory-sft-skill/SKILL.md)
- **GaLore, APOLLO, BAdam, Muon, Adam-mini, DFT/ASFT/EAFT, FP8, and profiler settings.**: [sub-skills/llamafactory-training-extensions-skill/SKILL.md](sub-skills/llamafactory-training-extensions-skill/SKILL.md)
- **vLLM batch inference using LLaMA-Factory prompt/data formats.**: [sub-skills/llamafactory-vllm-batch-infer-skill/SKILL.md](sub-skills/llamafactory-vllm-batch-infer-skill/SKILL.md)
- **LLaMA-Factory WebUI / LlamaBoard launch and health checks.**: [sub-skills/llamafactory-webui-skill/SKILL.md](sub-skills/llamafactory-webui-skill/SKILL.md)

## Execution Contract

1. Resolve the user's model, data/corpus, output directory, backend, and smoke/full-run target.
2. Read the nearest sub-skill `SKILL.md`, then one or two linked references only as needed.
3. Use bundled scripts for validation, config generation, smoke tests, and inspection where available.
4. Run package CLIs or public package APIs from the installed environment; do not require the original repo checkout.
5. Save generated configs, command logs, summaries, and inspection results beside the user's output artifacts.
6. Report exact artifact paths, validation status, metrics/losses, and unresolved risks.

## Shared Resources

- [references/coverage-matrix.md](references/coverage-matrix.md): maps public capability families to sub-skills.
- [references/installation.md](references/installation.md): public install, extras, import checks, and backend prerequisites.
- [references/troubleshooting.md](references/troubleshooting.md): repo-wide import, dependency, GPU, data, and output-location issues.
- [scripts/check_llama_factory_env.py](scripts/check_llama_factory_env.py): safe import and optional-dependency check for a fresh environment.
- [scripts/inspect_package.py](scripts/inspect_package.py): read-only package/API inspection helper.
- [scripts/make_demo_data.py](scripts/make_demo_data.py): creates tiny local demo datasets for sub-skill smoke checks.
- [scripts/lf_skill_common.py](scripts/lf_skill_common.py): shared helper library used by bundled LLaMA-Factory scripts; read it when adapting scripts.

The `evals/` directory is a development artifact for self-refine checks and is not linked as runtime documentation.
