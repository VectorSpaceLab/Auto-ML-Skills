# Paper Recipes

Use this reference when translating paper-backed methods into TRL configs or reviewing a PR that implements a method from a paper.

## Paper Link Rule

When linking to papers in TRL docs or `paper_index.md`, use:

```text
https://huggingface.co/papers/<id>
```

Do not use arXiv `abs` links in new TRL docs.

## Paper Index Rule

If a PR implements a method, algorithm, or training approach from a research paper, add a corresponding subsection to `docs/source/paper_index.md`.

For reviews, explicitly check that the paper index was updated.

## DPO

Direct Preference Optimization is exposed through `DPOTrainer` / `DPOConfig`.

Key config:

```python
from trl import DPOConfig

args = DPOConfig(
    beta=0.1,
    learning_rate=1e-6,
    max_length=1024,
)
```

Data is paired preference data with `chosen` and `rejected` completions, optionally sharing an explicit `prompt`.

## GRPO

Group Relative Policy Optimization is exposed through `GRPOTrainer` / `GRPOConfig`.

Key config:

```python
from trl import GRPOConfig

args = GRPOConfig(
    num_generations=8,
    max_completion_length=256,
    beta=0.0,
)
```

Use reward functions or reward models to score completions. `accuracy_reward` and `reasoning_accuracy_reward` are available under `trl.rewards`.

## DeepSeek-R1-Style Reasoning RL

The inspected paper index maps reasoning-oriented GRPO stages to:

```python
from trl import GRPOConfig

args = GRPOConfig(
    learning_rate=4e-5,
    max_completion_length=32768,
    num_generations=16,
    beta=0.001,
    use_vllm=True,
)
```

Combine rule-based rewards such as accuracy and format rewards. Use vLLM for long reasoning completions if hardware permits.

## DAPO-Style GRPO Variant

DAPO-related settings in TRL include:

```python
from trl import GRPOConfig
from trl.rewards import get_soft_overlong_punishment

args = GRPOConfig(
    mask_truncated_completions=True,
    loss_type="dapo",
    epsilon=0.2,
    epsilon_high=0.28,
    beta=0.0,
)

soft_overlong = get_soft_overlong_punishment(
    max_completion_len=20480,
    soft_punish_cache=4096,
)
```

Dynamic sampling is called out as unsupported in the inspected paper index.

## GSPO

GSPO is configured through GRPO sequence-level importance sampling:

```python
from trl import GRPOConfig

args = GRPOConfig(
    importance_sampling_level="sequence",
    loss_type="grpo",
    beta=0.0,
    epsilon=3e-4,
    epsilon_high=4e-4,
    gradient_accumulation_steps=1,
    steps_per_generation=4,
)
```

This matters when training is slightly off-policy, such as when `steps_per_generation > gradient_accumulation_steps` or `num_iterations > 1`.

## High-Entropy Token Training

The inspected paper index maps the "80/20" high-entropy-token recipe to a DAPO-like GRPO config plus `top_entropy_quantile=0.2`:

```python
from trl import GRPOConfig

args = GRPOConfig(
    loss_type="dapo",
    mask_truncated_completions=True,
    epsilon=0.2,
    epsilon_high=0.28,
    beta=0.0,
    top_entropy_quantile=0.2,
)
```

Check installed `GRPOConfig` fields before using this in a specific release.

## KTO

Kahneman-Tversky Optimization is documented as experimental in v1-style docs:

```python
from trl.experimental.kto import KTOConfig

args = KTOConfig(
    beta=0.1,
    desirable_weight=1.0,
    undesirable_weight=1.0,
)
```

Use unpaired preference data. Keep learning rates conservative; inspected docs recommend keeping KTO learning rates in a narrow low range for most models.

## New Paper-Backed Method Checklist

- Add or update trainer and config classes in the appropriate stable or experimental namespace.
- Add tests for config construction, preprocessing, loss behavior, and trainer smoke behavior.
- Add docs for dataset format, usage tips, and metrics.
- Add an example or script if the method is user-facing.
- Add a `paper_index.md` subsection with a Hugging Face papers link.
- If the method copies duplicated trainer logic, keep names, control flow, and comments aligned with neighboring trainers.
