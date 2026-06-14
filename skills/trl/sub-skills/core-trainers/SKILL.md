---
name: core-trainers
description: "Use TRL stable Python trainer APIs for SFT, DPO, GRPO, reward modeling, RLOO, configs, PEFT adapters, datasets, metrics, and trainer debugging."
---

# Core Trainers

Use this sub-skill when a user wants Python code using TRL trainers or asks which stable trainer fits a post-training task.

## Stable Trainer Map

| Goal | Trainer | Dataset type |
| --- | --- | --- |
| Supervised instruction/chat tuning | `SFTTrainer` with `SFTConfig` | language modeling or prompt-completion |
| Preference alignment from chosen/rejected pairs | `DPOTrainer` with `DPOConfig` | preference |
| Online RL with multiple completions per prompt | `GRPOTrainer` with `GRPOConfig` | prompt-only plus reward functions or reward models |
| Train a scalar reward model | `RewardTrainer` with `RewardConfig` | preference |
| Online REINFORCE leave-one-out training | `RLOOTrainer` with `RLOOConfig` | prompt-only plus reward functions or reward models |

Read [references/trainer-api.md](references/trainer-api.md) for verified constructor shapes and important config knobs. Read [references/trainer-workflows.md](references/trainer-workflows.md) for task recipes and dataset expectations. Run [scripts/minimal_trainer_imports.py](scripts/minimal_trainer_imports.py) to verify trainer imports and live signatures.

## Minimal Recipes

SFT:

```python
from datasets import load_dataset
from trl import SFTConfig, SFTTrainer

args = SFTConfig(output_dir="model-sft", learning_rate=2e-5, max_length=1024)
trainer = SFTTrainer(
    model="Qwen/Qwen3-0.6B",
    args=args,
    train_dataset=load_dataset("trl-lib/Capybara", split="train"),
)
trainer.train()
```

DPO:

```python
from datasets import load_dataset
from trl import DPOConfig, DPOTrainer

args = DPOConfig(output_dir="model-dpo", learning_rate=1e-6, beta=0.1)
trainer = DPOTrainer(
    model="Qwen/Qwen3-0.6B",
    args=args,
    train_dataset=load_dataset("trl-lib/ultrafeedback_binarized", split="train"),
)
trainer.train()
```

GRPO:

```python
from datasets import load_dataset
from trl import GRPOConfig, GRPOTrainer
from trl.rewards import accuracy_reward

args = GRPOConfig(output_dir="model-grpo", num_generations=4, max_completion_length=256)
trainer = GRPOTrainer(
    model="Qwen/Qwen2.5-0.5B-Instruct",
    reward_funcs=accuracy_reward,
    args=args,
    train_dataset=load_dataset("trl-lib/DeepMath-103K", split="train"),
)
trainer.train()
```

Reward modeling:

```python
from datasets import load_dataset
from trl import RewardConfig, RewardTrainer

args = RewardConfig(output_dir="model-reward", learning_rate=1e-4, max_length=1024)
trainer = RewardTrainer(
    model="Qwen/Qwen3-0.6B",
    args=args,
    train_dataset=load_dataset("trl-lib/ultrafeedback_binarized", split="train"),
)
trainer.train()
```

RLOO:

```python
from datasets import load_dataset
from trl import RLOOConfig, RLOOTrainer
from trl.rewards import accuracy_reward

args = RLOOConfig(output_dir="model-rloo", num_generations=2, max_completion_length=256)
trainer = RLOOTrainer(
    model="Qwen/Qwen2-0.5B-Instruct",
    reward_funcs=accuracy_reward,
    args=args,
    train_dataset=load_dataset("trl-lib/DeepMath-103K", split="train"),
)
trainer.train()
```

## PEFT And Adapters

All stable trainers accept `peft_config`. For LoRA, install `trl[peft]`, create a `peft.LoraConfig`, and pass it to the trainer. For CLI workflows, use the `--use_peft` family of flags instead.

```python
from peft import LoraConfig
from trl import SFTConfig, SFTTrainer

peft_config = LoraConfig(r=32, lora_alpha=16, lora_dropout=0.05, task_type="CAUSAL_LM")
args = SFTConfig(output_dir="model-sft-lora", learning_rate=2e-4)
trainer = SFTTrainer(model="Qwen/Qwen3-0.6B", args=args, train_dataset=dataset, peft_config=peft_config)
```

LoRA learning rates are commonly higher than full fine-tuning rates because fewer parameters are trained. Start with roughly 10x the full fine-tuning learning rate, then tune from metrics.

## Debugging Order

1. Verify package/imports with the root environment script.
2. Confirm the dataset schema matches the trainer: SFT uses `text`, `messages`, or `prompt`/`completion`; DPO and RewardTrainer use `chosen`/`rejected`; GRPO and RLOO need prompts plus rewards.
3. Print one formatted dataset row before training. For conversational data, confirm roles and chat template behavior.
4. Reduce memory pressure before changing algorithm logic: lower batch size, lower max length, use gradient accumulation, PEFT, quantization, Liger, FSDP, or DeepSpeed.
5. For GRPO/RLOO reward issues, inspect reward outputs directly on a small batch. Rewards should return one value per completion or prompt group as documented by the reward callable.

For dataset schemas and reward functions, switch to [../data-and-rewards/SKILL.md](../data-and-rewards/SKILL.md). For Accelerate, vLLM, and memory scaling, switch to [../vllm-and-distributed/SKILL.md](../vllm-and-distributed/SKILL.md).
