---
name: trl
description: Use TRL to post-train foundation models with Hugging Face Transformers, including SFT, DPO, GRPO, RLOO, reward modeling, CLI training, data formatting, scaling integrations, experimental agent workflows, and TRL source development.
license: Apache-2.0
---

# TRL

TRL, short for Transformers Reinforcement Learning, is a Hugging Face library for post-training foundation models. It builds on `transformers`, `datasets`, and `accelerate` and exposes stable trainer classes, CLI training commands, data/chat-template utilities, reward functions, vLLM generation support, PEFT/quantization helpers, and an explicitly unstable `trl.experimental` area.

Use this skill when the task involves:

- Training or configuring `SFTTrainer`, `DPOTrainer`, `GRPOTrainer`, `RLOOTrainer`, `RewardTrainer`, or TRL-compatible KTO workflows.
- Running `trl sft`, `trl dpo`, `trl grpo`, `trl rloo`, `trl reward`, `trl kto`, `trl env`, `trl skills`, or `trl vllm-serve`.
- Preparing TRL dataset formats, chat templates, tool-calling data, multimodal messages, or reward functions.
- Choosing memory, speed, distributed, vLLM, PEFT, quantization, Liger, DeepSpeed, or kernels settings.
- Working with `trl.experimental`, OpenEnv, OpenReward, online/agent training, or unstable trainers.
- Modifying TRL source code, reviewing PRs, or keeping duplicated trainer logic consistent.

## Installation

For normal use:

```bash
pip install trl
```

For extras:

```bash
pip install "trl[peft]"          # PEFT and LoRA workflows
pip install "trl[quantization]"  # bitsandbytes quantization workflows
pip install "trl[vllm]"          # vLLM-backed generation for online methods
pip install "trl[liger]"         # Liger kernels
pip install "trl[openreward]"    # OpenReward experimental integration
```

For source development:

```bash
git clone https://github.com/huggingface/trl.git
cd trl
pip install -e ".[dev]"
```

Verify an environment with [scripts/check_env.py](scripts/check_env.py). Inspect installed signatures with [scripts/inspect_public_api.py](scripts/inspect_public_api.py) before relying on a detail that may have changed.

## Sub-Skills

- [training](sub-skills/training/SKILL.md): Use for Python trainer APIs, trainer configs, trainer selection, paper recipes, and training troubleshooting.
- [cli-and-scripts](sub-skills/cli-and-scripts/SKILL.md): Use for `trl` CLI commands, YAML configs, `TrlParser`, bundled training scripts, and reproducible command construction.
- [data-rewards-chat](sub-skills/data-rewards-chat/SKILL.md): Use for dataset formats, chat templates, tool calling, multimodal message preparation, reward functions, and preprocessing.
- [scaling-integrations](sub-skills/scaling-integrations/SKILL.md): Use for Accelerate, DeepSpeed, FSDP, sequence/context parallelism, PEFT, quantization, kernels, Liger, vLLM, memory, and speed.
- [experimental-agents](sub-skills/experimental-agents/SKILL.md): Use for `trl.experimental`, OpenEnv, OpenReward, environment-based GRPO, online DPO, PPO, GKD, and other unstable trainers.
- [repo-development](sub-skills/repo-development/SKILL.md): Use when editing or reviewing TRL source, docs, tests, examples, trainer duplication, paper implementations, or packaged skills.

## Shared References

- [references/capability-map.md](references/capability-map.md): Coverage map from TRL public capabilities to this skill tree.
- [references/installation-and-dependencies.md](references/installation-and-dependencies.md): Public installation commands, extras, package requirements, and import checks.
- [references/troubleshooting.md](references/troubleshooting.md): Cross-cutting install, import, CLI, dataset, vLLM, memory, and experimental warnings.

## Working Rules

- Prefer verified installed-package facts over remembered API details. Run `python scripts/inspect_public_api.py` in the target environment when signatures matter.
- Treat `trl.experimental` as unstable. Use it deliberately and warn users that APIs can change or disappear in any release.
- For source edits, read [repo-development](sub-skills/repo-development/SKILL.md) first. TRL intentionally duplicates trainer internals; consistency across duplicated trainer blocks is a requirement.
- For new paper-backed algorithms or methods in the TRL repo, update the paper index and use `https://huggingface.co/papers/<id>` paper links.

## Fast Routing

| User asks for | Start here |
| --- | --- |
| "Fine-tune this model with TRL" | [training](sub-skills/training/SKILL.md) |
| "Give me a `trl sft` command" | [cli-and-scripts](sub-skills/cli-and-scripts/SKILL.md) |
| "My dataset columns are wrong" | [data-rewards-chat](sub-skills/data-rewards-chat/SKILL.md) |
| "Use vLLM / DeepSpeed / LoRA" | [scaling-integrations](sub-skills/scaling-integrations/SKILL.md) |
| "Train an agent with an environment" | [experimental-agents](sub-skills/experimental-agents/SKILL.md) |
| "Modify or review TRL code" | [repo-development](sub-skills/repo-development/SKILL.md) |

If a task spans several rows, start with the user-facing workflow and open the lower-level sub-skill only when you reach that decision point.
