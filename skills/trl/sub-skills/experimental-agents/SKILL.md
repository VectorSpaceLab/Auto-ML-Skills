---
name: trl-experimental-agents
description: Use TRL experimental trainers and agent/environment workflows, including OpenEnv, OpenReward, environment_factory, online DPO, PPO, GKD, KTO, and other unstable APIs.
license: Apache-2.0
---

# TRL Experimental And Agents

Use this sub-skill when a task involves `trl.experimental`, OpenEnv, OpenReward, environment-based GRPO, tool-calling agents, online DPO, PPO, GKD, BCO, CPO, ORPO, PRM, NashMD, XPO, or other unstable TRL features.

## Stability Contract

Anything under `trl.experimental` may change or be removed in any release, including patch releases. Use experimental APIs only when the workflow requires them, and warn users when producing reusable code.

Silence the runtime warning only when the user accepts the risk:

```bash
export TRL_EXPERIMENTAL_SILENCE=1
```

Read [references/experimental-map.md](references/experimental-map.md) for feature mapping.

## Agent Training Choices

- Use `GRPOTrainer(..., tools=[...])` for stateless function tools.
- Use `GRPOTrainer(..., environment_factory=...)` when environment state persists across turns.
- Use `GRPOTrainer(..., rollout_func=...)` only for lower-level custom rollout control.
- Use `OpenRewardSpec` when the environment speaks the Open Reward Standard.
- Use OpenEnv wrappers when training against OpenEnv environments or examples.

Read [references/openenv-openreward-workflows.md](references/openenv-openreward-workflows.md) for contracts and examples.

## Environment Factory Contract

An environment class should:

- Have a zero-argument constructor, or capture configuration through closure/module-level constants.
- Implement `reset(self, **kwargs) -> str | None`.
- Expose public tool methods with typed arguments and docstrings.
- Store reward/state on the instance if the reward function needs it.

Generate a template with [scripts/openenv_environment_template.py](scripts/openenv_environment_template.py).

## Minimal Environment Pattern

```python
from datasets import Dataset
from trl import GRPOConfig, GRPOTrainer

class MyEnv:
    def __init__(self):
        self.reward = 0.0

    def reset(self, **kwargs) -> str | None:
        self.reward = 0.0
        return "Initial observation."

    def submit(self, answer: str) -> str:
        """Submit an answer.

        Args:
            answer: Candidate answer.
        """
        self.reward = 1.0 if answer == "4" else 0.0
        return "submitted"

def reward_func(environments, **kwargs):
    return [env.reward for env in environments]

dataset = Dataset.from_dict({"prompt": [[{"role": "user", "content": "What is 2 + 2?"}]] * 16})

trainer = GRPOTrainer(
    model="Qwen/Qwen3-0.6B",
    args=GRPOConfig(num_generations=2, max_steps=1),
    train_dataset=dataset,
    environment_factory=MyEnv,
    reward_funcs=reward_func,
)
```

## References

- [references/experimental-map.md](references/experimental-map.md): Experimental module map, common imports, and when to use each feature.
- [references/openenv-openreward-workflows.md](references/openenv-openreward-workflows.md): OpenEnv and OpenReward workflows, contracts, and local/self-hosted patterns.
- [references/troubleshooting.md](references/troubleshooting.md): Experimental warnings, environment/tool schemas, reward, and rollout failures.
