---
name: trl
description: "Use TRL to post-train transformer language models with SFT, DPO, GRPO, reward modeling, RLOO, CLI workflows, datasets, reward functions, vLLM generation, distributed training, experimental trainers, and TRL agent-skill management."
---

# TRL

Use this skill when a user asks how to install, configure, run, debug, or extend TRL, the Hugging Face Transformers Reinforcement Learning library for post-training foundation models.

TRL builds on `transformers`, `accelerate`, and `datasets`. The stable public package exposes trainer/config pairs for supervised fine-tuning, preference optimization, online RL with rewards, and reward modeling, plus a `trl` command-line interface for training jobs.

## Install

For normal usage:

```bash
pip install trl
python - <<'PY'
import trl
from trl import SFTTrainer, DPOTrainer, GRPOTrainer, RewardTrainer, RLOOTrainer
print("trl", trl.__version__)
PY
```

Install extras only for the workflow that needs them:

```bash
pip install "trl[peft]"       # LoRA / PEFT adapters
pip install "trl[vllm]"       # vLLM generation and vllm-serve
pip install "trl[vlm]"        # vision-language model data paths
pip install "trl[deepspeed]"  # DeepSpeed integration
pip install "trl[liger]"      # Liger kernels
```

Read [references/install-and-environment.md](references/install-and-environment.md) for version, extras, import checks, and common install failures.

## Route By Task

- For Python trainer APIs such as `SFTTrainer`, `DPOTrainer`, `GRPOTrainer`, `RewardTrainer`, and `RLOOTrainer`, use [sub-skills/core-trainers/SKILL.md](sub-skills/core-trainers/SKILL.md).
- For `trl sft`, `trl dpo`, `trl grpo`, `trl reward`, `trl rloo`, `trl kto`, YAML configs, and CLI troubleshooting, use [sub-skills/cli-training/SKILL.md](sub-skills/cli-training/SKILL.md).
- For dataset schemas, chat templates, tool-calling examples, multimodal message preparation, and built-in reward functions, use [sub-skills/data-and-rewards/SKILL.md](sub-skills/data-and-rewards/SKILL.md).
- For vLLM server/colocate generation, `trl vllm-serve`, Accelerate, DeepSpeed, FSDP, memory reduction, PEFT, Liger, and distributed jobs, use [sub-skills/vllm-and-distributed/SKILL.md](sub-skills/vllm-and-distributed/SKILL.md).
- For unstable incubating trainers under `trl.experimental`, use [sub-skills/experimental-trainers/SKILL.md](sub-skills/experimental-trainers/SKILL.md).
- For TRL's built-in agent-skill installer (`trl skills`) and `trl.skills` Python utilities, use [sub-skills/agent-skills-management/SKILL.md](sub-skills/agent-skills-management/SKILL.md).

## Core Decisions

Before giving commands or code, identify:

- Training method: SFT for supervised instruction/chat data, DPO for paired preferences, RewardTrainer for reward models, GRPO/RLOO for online generation with reward functions or reward models.
- Data format: language modeling, prompt-only, prompt-completion, preference, unpaired preference, stepwise supervision, conversational messages, tool calling, or multimodal messages.
- Interface: Python trainer for custom logic, CLI for reproducible jobs, or `accelerate launch` for scripts and distributed training.
- Optional systems: PEFT/LoRA, quantization, vLLM generation, DeepSpeed/FSDP, Liger kernels, chat templates, model card or Hub push.
- Stability: stable `trl` namespace vs `trl.experimental`, which may change or disappear without deprecation.

## Safe Checks

Run the bundled environment check before deeper debugging:

```bash
python skills/trl/scripts/check_trl_environment.py
```

Use the core trainer import check before claiming a Python environment is ready for trainer work:

```bash
python skills/trl/sub-skills/core-trainers/scripts/minimal_trainer_imports.py
```

These scripts are safe: they import packages and inspect CLI availability; they do not download models, start servers, or run training.

## Repository Contribution Notes

When working inside the TRL source repository:

- Keep stable trainer changes conservative and tested.
- Treat code under `trl.experimental` as less stable, but avoid large refactors there unless requested.
- If a change implements a method or algorithm from a research paper, update `docs/source/paper_index.md`.
- TRL intentionally duplicates trainer logic across trainers. When changing duplicated logic, propagate equivalent changes to the matching trainers instead of abstracting shared behavior into a new base class.

Read [references/coverage-map.md](references/coverage-map.md) for the evidence and capability map used to build this skill.
