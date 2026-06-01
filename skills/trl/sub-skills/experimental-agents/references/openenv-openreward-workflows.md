# OpenEnv And OpenReward Workflows

Use this for environment-based GRPO and agentic training.

## When To Use Environments

Use tools when each call is stateless and independent. Use environments when actions affect future observations, such as games, browsers, simulators, or multi-turn tasks.

TRL's `GRPOTrainer` supports environment interaction through `environment_factory`.

## `environment_factory` Contract

The trainer creates one environment instance per generation/episode. Pass the class or a zero-argument factory, not a pre-created instance.

Required behavior:

- `reset(self, **kwargs)` is called at episode start. It receives dataset columns as keyword arguments and returns an initial observation string or `None`.
- Public methods other than `reset` become tools.
- Tool methods must use typed arguments and docstrings with `Args:` descriptions so schema generation works.
- Tool methods can raise exceptions to signal invalid actions; the trainer can feed error messages back to the model as tool responses.
- Reward functions can receive `environments` and read state stored on instances.

Minimal pattern:

```python
class MyEnv:
    def __init__(self):
        self.reward = 0.0

    def reset(self, **kwargs) -> str | None:
        self.reward = 0.0
        return "Initial observation."

    def action(self, value: str) -> str:
        """Take an action.

        Args:
            value: Action value.
        """
        self.reward = 1.0 if value == "target" else 0.0
        return "observation"

def reward_func(environments, **kwargs):
    return [env.reward for env in environments]
```

## OpenEnv

OpenEnv environments can be installed from their Hugging Face Space Git repositories. Example patterns from docs:

```bash
pip install "openenv-echo-env @ git+https://huggingface.co/spaces/openenv/echo_env"
pip install "openenv-textarena @ git+https://huggingface.co/spaces/openenv/wordle"
```

The TRL examples include OpenEnv scripts for echo, wordle, catch, sudoku, browsergym, CARLA, and multi-env training. Some scripts include PEP 723 metadata and can be run with `uv run` in a suitable checkout; when writing standalone code, copy the dependency requirements into project metadata instead of depending on example paths.

## OpenEnv Echo Pattern

```python
from datasets import Dataset
from trl import GRPOConfig, GRPOTrainer

ENV_URL = "https://openenv-echo-env.hf.space"

class EchoToolEnv:
    def __init__(self):
        from echo_env import EchoEnv

        self.env = EchoEnv(base_url=ENV_URL)
        self.reward = 0.0

    def reset(self, **kwargs) -> str | None:
        self.reward = 0.0
        return None

    def echo(self, message: str) -> str:
        """Echo a message.

        Args:
            message: The message to echo.
        """
        from echo_env.models import EchoAction

        observation = self.env.step(EchoAction(message=message))
        self.reward = observation.observation.reward
        return observation.observation.echoed_message

def reward_func(environments, **kwargs):
    return [env.reward for env in environments]

dataset = Dataset.from_dict(
    {"prompt": [[{"role": "user", "content": "Try to echo 'Hello World!'."}]] * 64}
)

trainer = GRPOTrainer(
    model="Qwen/Qwen3-0.6B",
    args=GRPOConfig(log_completions=True),
    train_dataset=dataset,
    environment_factory=EchoToolEnv,
    reward_funcs=reward_func,
)
```

## OpenReward

OpenReward uses the Open Reward Standard over HTTP/SSE. Install:

```bash
pip install "trl[openreward]"
```

Use `OpenRewardSpec`:

```python
from trl import GRPOConfig, GRPOTrainer
from trl.experimental.openreward import OpenRewardSpec

spec = OpenRewardSpec("Eigent/SETA", num_tasks=64)

trainer = GRPOTrainer(
    model="Qwen/Qwen3-4B",
    args=GRPOConfig(
        num_generations=2,
        max_steps=5,
        max_tool_calling_iterations=20,
        log_completions=True,
    ),
    train_dataset=spec.train_dataset,
    environment_factory=spec.environment_factory,
    reward_funcs=spec.reward_funcs,
)
trainer.train()
```

`OpenRewardSpec` maps a single ORS environment into:

- `train_dataset`
- `environment_factory`
- `reward_funcs`

## Self-Hosted OpenReward

For a self-hosted environment URL:

```python
spec = OpenRewardSpec("https://my-org-my-env.hf.space", env_name="my_env")
```

For single-host local/self-hosted servers, set SDK URL overrides before constructing `OpenRewardSpec`:

```python
import os

URL = "http://127.0.0.1:8000"
os.environ["OPENREWARD_API_URL"] = URL
os.environ["OPENREWARD_SESSION_URL"] = URL

spec = OpenRewardSpec(URL, env_name="echoenvironment")
```

## Reward Tips

- Sparse binary rewards often work well with GRPO because relative ranking within each generation group matters.
- Test the environment manually before training.
- Prefer judging final state over checking for one exact action sequence.
- Store reward on the environment instance and read it in the reward function.

## Multi-Turn Length

In environment/tool-call episodes, `max_completion_length` applies across generated tokens in the episode. If the model repeatedly calls tools, short limits can truncate before it reaches a final answer.
