---
name: experimental-trainers
description: "Use and review TRL experimental trainers under trl.experimental, including unstable KTO, PPO, ORPO, CPO, GKD, Nash-MD, PRM, distillation, and paper-index requirements."
---

# Experimental Trainers

Use this sub-skill when a user asks about trainers or algorithms under `trl.experimental`, sees a `TRLExperimentalWarning`, or wants to add/review an experimental paper implementation.

## Stability Rule

`trl.experimental` is an incubation area. APIs there may change or be removed without deprecation. State that risk clearly in user-facing code and avoid presenting experimental imports as stable root-package APIs.

The package emits a warning on experimental imports unless `TRL_EXPERIMENTAL_SILENCE=1` is set. Do not silence it in examples unless the user explicitly accepts the risk.

## Import Pattern

Use submodule imports:

```python
from trl.experimental.kto import KTOConfig, KTOTrainer
```

Other experimental packages follow the same pattern where present:

```python
from trl.experimental.gkd import GKDConfig, GKDTrainer
from trl.experimental.orpo import ORPOConfig, ORPOTrainer
from trl.experimental.ppo import PPOConfig, PPOTrainer
```

Before writing code, inspect the current installed package:

```python
import inspect
from trl.experimental.kto import KTOTrainer
print(inspect.signature(KTOTrainer.__init__))
```

Read [references/experimental-reference.md](references/experimental-reference.md) for the catalog, safe usage rules, and contribution checks.

## KTO Example

KTO is documented as experimental in current TRL:

```python
from datasets import load_dataset
from transformers import AutoModelForCausalLM, AutoTokenizer
from trl.experimental.kto import KTOConfig, KTOTrainer

model = AutoModelForCausalLM.from_pretrained("Qwen/Qwen2-0.5B-Instruct")
tokenizer = AutoTokenizer.from_pretrained("Qwen/Qwen2-0.5B-Instruct")
dataset = load_dataset("trl-lib/kto-mix-14k", split="train")

args = KTOConfig(output_dir="Qwen2-0.5B-KTO")
trainer = KTOTrainer(model=model, args=args, processing_class=tokenizer, train_dataset=dataset)
trainer.train()
```

KTO expects unpaired preference data with a binary desirable/undesirable signal; paired preference data may be converted to unpaired.

## Repository Review Notes

When reviewing or changing a TRL experimental trainer:

- Keep the experimental implementation self-contained.
- Make only small consistency improvements unless the user explicitly asks for a refactor.
- If the implementation adds a paper method or algorithm, update `docs/source/paper_index.md`.
- If duplicated logic matches stable trainers or other experimental trainers, keep variable names, comments, and control flow aligned unless trainer semantics require divergence.
