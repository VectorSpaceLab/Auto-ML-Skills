# Rewards And Chat Templates

Read this when reward functions, chat templates, tool calling, or multimodal message rendering are involved.

## Built-In Rewards

Import from `trl.rewards`:

```python
from trl.rewards import (
    accuracy_reward,
    reasoning_accuracy_reward,
    think_format_reward,
    get_soft_overlong_punishment,
)
```

Use cases:

- `accuracy_reward`: math/answer accuracy reward for completions with expected solutions; requires the `math_verify` optional dependency.
- `reasoning_accuracy_reward`: accuracy reward variant intended for reasoning models; requires the `math_verify` optional dependency.
- `think_format_reward`: format reward for completions that should contain reasoning tags.
- `get_soft_overlong_punishment`: returns a reward function that softly penalizes overlong completions; useful in DAPO-style GRPO recipes.

Smoke-test with [../scripts/reward_smoke_test.py](../scripts/reward_smoke_test.py).

## Custom Reward Functions

For GRPO/RLOO, custom reward functions should accept completion-related inputs and any dataset columns passed by the trainer, then return one scalar per completion. Built-in rewards in the inspected package receive completions as a list of one-message lists:

```python
def reward_func(completions, **kwargs):
    texts = [completion[0]["content"] for completion in completions]
    return [1.0 if "expected" in text else 0.0 for text in texts]
```

Inspect what the installed trainer passes before writing version-sensitive code. Tool/environment workflows may pass richer structures or `environments`.

For multiple rewards:

```python
trainer = GRPOTrainer(
    ...,
    reward_funcs=[accuracy_reward, think_format_reward],
)
```

Use `reward_weights=[...]` in `GRPOConfig` or `RLOOConfig` when scales differ.

## Chat Templates

A chat template is a Jinja2 template that turns messages into the exact text form expected by a model.

In most normal workflows, the tokenizer provides the chat template and TRL applies it. You need to care when:

- `SFTConfig(assistant_only_loss=True)` is used.
- GRPO tool calling is used.
- A model family has a template that is not covered by TRL's automatic training-template patches.
- Tool-call arguments are JSON objects and a template expects strings.

## Assistant-Only Loss

For `assistant_only_loss=True`, the template must include generation markers around assistant output so TRL can produce assistant token masks. TRL bundles patched templates for common model families, including Qwen, Llama, DeepSeek-V3, Gemma, GPT-OSS, Phi, GLM, and several VLM variants.

If a model is unsupported, inspect the template manually or clone a training template from a compatible model family.

## Prefix Preservation For Tools

For GRPO tool calling, a template should be prefix-preserving: appending a tool message should not change how earlier messages are rendered. This matters because the trainer may render intermediate states during multi-turn tool execution.

If a model produces inconsistent tool-call rollouts, test whether rendering the same prefix with and without appended tool messages changes the prefix text.

## Tool Schemas

Define tools as typed Python callables with docstrings or JSON schema objects. For dataset rows, store tools in a `tools` column.

```python
from transformers.utils import get_json_schema

def control_light(room: str, state: str) -> str:
    """Controls a light.

    Args:
        room: Room name.
        state: Desired state, such as "on" or "off".
    """
    return f"{room}: {state}"

schema = get_json_schema(control_light)
```

For environment-based tools, see [experimental agents](../../experimental-agents/SKILL.md).

## Chat Template Helpers

```python
from trl import get_training_chat_template, clone_chat_template, supports_tool_calling
```

- `get_training_chat_template`: returns a TRL training template when the processing class/tokenizer is recognized.
- `clone_chat_template`: clones a source tokenizer chat template into another model/tokenizer setup and can resize token embeddings.
- `supports_tool_calling`: checks whether a processing class supports tool-calling-style templating.

## Multimodal Helpers

The inspected top-level public API exposes multimodal helpers through `trl.data_utils` and re-exports them at top level:

```python
from trl import prepare_multimodal_messages, prepare_multimodal_messages_vllm
```

Use `prepare_multimodal_messages_vllm` for vLLM-compatible multimodal message preparation. Do not assume these helpers live under `trl.chat_template_utils` in all versions.

## GPT-OSS / Harmony-Style Rows

TRL docs describe Harmony-style message fields for GPT-OSS models:

- developer role
- channels such as `analysis`, `final`, and `commentary`
- reasoning effort
- model identity

When using GPT-OSS-style chat templates, keep the model's expected fields and tokenizer kwargs aligned. Test a single row with `tokenizer.apply_chat_template(..., tokenize=False)` before training.
