# Trainer Workflows

Read this for practical task recipes and dataset expectations for stable TRL Python trainers.

## SFT

Use SFT for supervised learning on existing demonstrations, instructions, chat transcripts, or prompt-completion pairs.

Accepted examples include:

```python
{"text": "The sky is blue."}
{"messages": [{"role": "user", "content": "What color is the sky?"}, {"role": "assistant", "content": "It is blue."}]}
{"prompt": "The sky is", "completion": " blue."}
{"prompt": [{"role": "user", "content": "What color is the sky?"}], "completion": [{"role": "assistant", "content": "It is blue."}]}
```

Important choices:

- `assistant_only_loss=True` for conversational datasets when only assistant tokens should contribute loss. The chat template must support generation masks.
- `completion_only_loss` defaults depend on prompt-completion vs language-modeling data. Set it explicitly when behavior matters.
- `packing=True` improves throughput for SFT. Use `packing_strategy="bfd"`, `"bfd_split"`, or `"wrapped"` depending on whether overlong examples should be split or discarded.
- `formatting_func` can convert custom rows to text, but prefer converting datasets into TRL-supported schemas when possible.

## DPO

Use DPO for paired preference data:

```python
{"prompt": "The sky is", "chosen": " blue.", "rejected": " green."}
{"chosen": "The sky is blue.", "rejected": "The sky is green."}
```

Conversational preference rows are lists of role/content messages. DPO can use explicit prompt columns or implicit prompt in the `chosen`/`rejected` conversations.

Important choices:

- `beta` controls the strength of deviation from the reference model; a common starting value is `0.1`.
- `precompute_ref_log_probs=True` can help when reference computation is expensive and the dataset fits the workflow.
- Overlong prompt/completion truncation should be handled through `max_length` or dataset filtering/pre-truncation.
- If using PEFT and no separate `ref_model`, confirm reference behavior matches the intended adapter/base-model setup.

## GRPO

Use GRPO for online RL where the model samples several completions per prompt and rewards rank or score those completions.

Dataset rows usually contain `prompt`, often with an answer target such as `solution` for reward functions:

```python
{"prompt": "Solve 2+2.", "solution": "4"}
{"prompt": [{"role": "user", "content": "Solve 2+2."}], "solution": "4"}
```

Reward functions receive generated completions and dataset columns. Built-ins include:

```python
from trl.rewards import accuracy_reward, reasoning_accuracy_reward, think_format_reward
```

Important choices:

- `num_generations` controls completions per prompt. Lower it to reduce memory and generation cost.
- `max_completion_length` bounds generated tokens.
- `reward_weights` combines multiple reward functions.
- `use_vllm=True` can speed up generation but requires `trl[vllm]` and hardware/backend verification.
- `loss_type` includes GRPO-family formulations; current defaults favor token-level normalization for long-completion settings.

## RewardTrainer

Use RewardTrainer to train a scalar reward model from preferred/rejected examples:

```python
{"chosen": "The sky is blue.", "rejected": "The sky is green."}
{"prompt": "The sky is", "chosen": " blue.", "rejected": " green."}
```

Important choices:

- Reward models are sequence-classification style models with a single scalar score.
- `center_rewards_coefficient` can encourage centered rewards.
- When training LoRA adapters on a causal LM used as a reward model, include the score head in saved modules when needed by the PEFT setup.

## RLOO

Use RLOO for online REINFORCE-style training from rewards with leave-one-out baselines.

The data/reward pattern resembles GRPO:

```python
from trl import RLOOConfig, RLOOTrainer
from trl.rewards import accuracy_reward

trainer = RLOOTrainer(
    model="Qwen/Qwen2-0.5B-Instruct",
    reward_funcs=accuracy_reward,
    args=RLOOConfig(num_generations=2),
    train_dataset=dataset,
)
```

Important choices:

- `num_generations` defaults lower than GRPO and affects the leave-one-out baseline.
- `beta` controls KL penalty strength.
- `normalize_advantages` and `reward_clip_range` can stabilize reward scales.
- vLLM generation modes mirror GRPO.

## Memory And Stability Checklist

- Use small `per_device_train_batch_size` and raise `gradient_accumulation_steps` before changing trainer logic.
- Set `max_length`/`max_completion_length` to match real data and hardware.
- Use `gradient_checkpointing=True` unless latency or cache behavior matters more.
- For large models, use PEFT, quantization, FSDP, DeepSpeed, Liger kernels, or vLLM generation where appropriate.
- For online methods, log completions and per-reward metrics on a small run before scaling out.
