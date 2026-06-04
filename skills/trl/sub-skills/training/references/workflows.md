# Training Workflows

These examples are intentionally small and task-oriented. They omit hardware-specific launch details; use the scaling sub-skill for distributed and memory settings.

## SFT: Supervised Fine-Tuning

Dataset format:

- Language modeling: `{"text": "..."}`
- Conversational language modeling: `{"messages": [{"role": "user", "content": "..."}, ...]}`
- Prompt-completion: `{"prompt": "...", "completion": "..."}`
- Conversational prompt-completion: `{"prompt": [...], "completion": [...]}`

Minimal code:

```python
from datasets import load_dataset
from trl import SFTConfig, SFTTrainer

args = SFTConfig(
    output_dir="sft-output",
    learning_rate=2e-5,
    max_length=1024,
)

trainer = SFTTrainer(
    model="Qwen/Qwen3-0.6B",
    args=args,
    train_dataset=load_dataset("trl-lib/Capybara", split="train"),
)
trainer.train()
```

Use `packing=True` to improve throughput when many examples are short. Use `assistant_only_loss=True` with conversational data when only assistant turns should contribute to loss. Use `completion_only_loss=True` for prompt-completion data when only completions should contribute.

## DPO: Offline Preference Optimization

Dataset format:

```python
{"prompt": "...", "chosen": "...", "rejected": "..."}
```

or conversational equivalents with lists of `{role, content}` messages.

Minimal code:

```python
from datasets import load_dataset
from trl import DPOConfig, DPOTrainer

args = DPOConfig(
    output_dir="dpo-output",
    learning_rate=1e-6,
    beta=0.1,
)

trainer = DPOTrainer(
    model="Qwen/Qwen3-0.6B",
    args=args,
    train_dataset=load_dataset("trl-lib/ultrafeedback_binarized", split="train"),
)
trainer.train()
```

Use an explicit `ref_model` if reference-model construction needs custom loading, quantization, or device placement.

## GRPO: Online Reward Training

Dataset format:

```python
{"prompt": "Solve: 2 + 2 = ?"}
```

or conversational prompt-only rows:

```python
{"prompt": [{"role": "user", "content": "Solve: 2 + 2 = ?"}]}
```

Minimal code:

```python
from datasets import load_dataset
from trl import GRPOConfig, GRPOTrainer
from trl.rewards import accuracy_reward

args = GRPOConfig(
    output_dir="grpo-output",
    num_generations=8,
    max_completion_length=256,
)

trainer = GRPOTrainer(
    model="Qwen/Qwen2.5-0.5B-Instruct",
    args=args,
    reward_funcs=accuracy_reward,
    train_dataset=load_dataset("trl-lib/DeepMath-103K", split="train"),
)
trainer.train()
```

Reward functions should return one scalar per completion. Multiple reward functions can be passed as a list; use `reward_weights` when their relative scale matters.

## RLOO: REINFORCE Leave-One-Out

RLOO also uses prompt-only data and reward functions or a reward model. It generates `num_generations` completions and uses the leave-one-out baseline to reduce variance.

```python
from datasets import load_dataset
from trl import RLOOConfig, RLOOTrainer
from trl.rewards import accuracy_reward

args = RLOOConfig(
    output_dir="rloo-output",
    num_generations=2,
    beta=0.05,
)

trainer = RLOOTrainer(
    model="Qwen/Qwen2.5-0.5B-Instruct",
    args=args,
    reward_funcs=accuracy_reward,
    train_dataset=load_dataset("trl-lib/DeepMath-103K", split="train"),
)
trainer.train()
```

Inspect the installed signature before using RLOO in version-sensitive code.

## Reward Modeling

Dataset format:

```python
{"prompt": "...", "chosen": "...", "rejected": "..."}
```

Minimal code:

```python
from datasets import load_dataset
from trl import RewardConfig, RewardTrainer

args = RewardConfig(
    output_dir="reward-output",
    learning_rate=1e-4,
    max_length=1024,
)

trainer = RewardTrainer(
    model="Qwen/Qwen2.5-0.5B-Instruct",
    args=args,
    train_dataset=load_dataset("trl-lib/ultrafeedback_binarized", split="train"),
)
trainer.train()
```

For LoRA reward modeling, configure `lora_task_type="SEQ_CLS"` in model args or PEFT config.

## KTO

KTO is documented as experimental in v1-style TRL docs. Prefer:

```python
from datasets import load_dataset
from trl.experimental.kto import KTOConfig, KTOTrainer

args = KTOConfig(output_dir="kto-output")
dataset = load_dataset("trl-lib/kto-mix-14k", split="train")

trainer = KTOTrainer(
    model=model,
    args=args,
    processing_class=tokenizer,
    train_dataset=dataset,
)
trainer.train()
```

Expected data is unpaired preference data with `prompt`, `completion`, and `label`. A paired preference dataset can also be converted by the trainer.

## PEFT And LoRA

```python
from peft import LoraConfig
from trl import SFTConfig, SFTTrainer

peft_config = LoraConfig(
    r=32,
    lora_alpha=16,
    lora_dropout=0.05,
    bias="none",
    task_type="CAUSAL_LM",
)

args = SFTConfig(
    output_dir="sft-lora",
    learning_rate=2e-4,
)

trainer = SFTTrainer(
    model="Qwen/Qwen2.5-0.5B",
    args=args,
    train_dataset=train_dataset,
    peft_config=peft_config,
)
```

Typical LoRA learning rates are higher than full fine-tuning because only adapter parameters are trained.

## Customization

Pass custom optimizer and scheduler:

```python
from torch import optim

optimizer = optim.AdamW(model.parameters(), lr=1e-6)
scheduler = optim.lr_scheduler.StepLR(optimizer, step_size=30, gamma=0.1)
trainer = DPOTrainer(..., optimizers=(optimizer, scheduler))
```

Add custom metrics:

```python
def compute_metrics(eval_preds):
    return {"custom_metric": 0.0}

trainer = DPOTrainer(..., compute_metrics=compute_metrics, eval_dataset=eval_dataset)
```

Add callbacks:

```python
from transformers import TrainerCallback

class CustomLoggingCallback(TrainerCallback):
    def on_log(self, args, state, control, logs=None, **kwargs):
        if logs is not None:
            print(state.global_step, logs)

trainer = DPOTrainer(..., callbacks=[CustomLoggingCallback()])
```
