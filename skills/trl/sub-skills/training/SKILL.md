---
name: trl-training
description: Use TRL trainer classes and configs for SFT, DPO, GRPO, RLOO, reward modeling, and related post-training workflows.
license: Apache-2.0
---

# TRL Training

Use this sub-skill when a task asks for Python-code training with TRL, trainer selection, config tuning, reward function wiring, paper recipe translation, or trainer API troubleshooting.

## Trainer Selection

- Use `SFTTrainer` for supervised fine-tuning on language-modeling or prompt-completion data.
- Use `DPOTrainer` for offline preference optimization on paired `chosen` / `rejected` examples.
- Use `GRPOTrainer` for online RL-style training where the model samples multiple completions per prompt and reward functions or reward models score them.
- Use `RLOOTrainer` for REINFORCE Leave-One-Out online training with prompt-only data and rewards.
- Use `RewardTrainer` for outcome reward-model training on paired preferences.
- Treat KTO as experimental in v1-style TRL docs. Check the installed package before using top-level `KTOTrainer`; prefer `trl.experimental.kto` when docs indicate that location.

Read [references/api-reference.md](references/api-reference.md) for constructor shapes and key config fields. Read [references/workflows.md](references/workflows.md) for end-to-end examples.

## Minimal Workflow

1. Identify the dataset type: language modeling, prompt-only, prompt-completion, preference, unpaired preference, or stepwise supervision.
2. Choose the trainer from the table above.
3. Create the matching config class with only the arguments needed for the current job.
4. Pass a model identifier or already-loaded model, a `datasets.Dataset`, and optional processing class, reward functions, callbacks, optimizer, or PEFT config.
5. Run `trainer.train()`, then save or push the model through normal Transformers/Hub workflows.

Before training, run [scripts/trainer_smoke_test.py](scripts/trainer_smoke_test.py) to verify that the installed TRL package exposes the expected trainers/configs and that config construction works without downloading a model.

## Stable Quick Starts

```python
from datasets import load_dataset
from trl import SFTTrainer

trainer = SFTTrainer(
    model="Qwen/Qwen3-0.6B",
    train_dataset=load_dataset("trl-lib/Capybara", split="train"),
)
trainer.train()
```

```python
from datasets import load_dataset
from trl import DPOTrainer

trainer = DPOTrainer(
    model="Qwen/Qwen3-0.6B",
    train_dataset=load_dataset("trl-lib/ultrafeedback_binarized", split="train"),
)
trainer.train()
```

```python
from datasets import load_dataset
from trl import GRPOTrainer
from trl.rewards import accuracy_reward

trainer = GRPOTrainer(
    model="Qwen/Qwen2.5-0.5B-Instruct",
    reward_funcs=accuracy_reward,
    train_dataset=load_dataset("trl-lib/DeepMath-103K", split="train"),
)
trainer.train()
```

```python
from datasets import load_dataset
from trl import RewardTrainer

trainer = RewardTrainer(
    model="Qwen/Qwen2.5-0.5B-Instruct",
    train_dataset=load_dataset("trl-lib/ultrafeedback_binarized", split="train"),
)
trainer.train()
```

## Common Decisions

- Prefer passing `model="repo/id"` for simple training scripts; load the model yourself only when you need custom model construction.
- Use `ModelConfig` and `get_peft_config` when building script-style training flows that mirror TRL CLI scripts.
- For LoRA/QLoRA, pass `peft_config=LoraConfig(...)` or use CLI/script model args. Use `lora_task_type="SEQ_CLS"` for reward modeling adapters.
- For SFT assistant-only loss, use conversational data and `SFTConfig(assistant_only_loss=True)`. Confirm the chat template supports generation markers.
- For SFT prompt-completion data, completion-only loss is the default behavior unless `completion_only_loss=False`.
- For GRPO/RLOO, start by reducing `num_generations` and `max_completion_length` when memory is tight.
- For vLLM-backed generation, switch to [scaling-integrations](../scaling-integrations/SKILL.md).

## References

- [references/api-reference.md](references/api-reference.md): Verified public trainer/config imports and important constructor/config fields.
- [references/workflows.md](references/workflows.md): Focused SFT, DPO, GRPO, RLOO, Reward, KTO, PEFT, and customization recipes.
- [references/paper-recipes.md](references/paper-recipes.md): How TRL maps paper-backed methods and recipes to configs.
- [references/troubleshooting.md](references/troubleshooting.md): Trainer-specific failures, metrics, reward, masking, and checkpoint issues.
