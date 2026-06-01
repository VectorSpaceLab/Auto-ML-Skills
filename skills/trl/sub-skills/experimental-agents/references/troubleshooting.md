# Experimental And Agents Troubleshooting

## Experimental Warning

`TRLExperimentalWarning` is expected for `trl.experimental`. It means the API is unstable. Do not hide it in reusable code unless the user explicitly accepts that instability.

To silence in a local run:

```bash
export TRL_EXPERIMENTAL_SILENCE=1
```

## Tool Schema Generation Fails

Check environment tool methods:

- Method is public and does not start with `_`.
- Method is not `reset`.
- Arguments have type annotations.
- Docstring has `Args:` entries for arguments.
- Names are descriptive. Avoid generic `step(action)` when the model needs meaningful tool names.

## Environment Constructor Needs Args

`environment_factory` should be zero-argument. Capture external config in a closure:

```python
URL = "https://example"

class MyEnv:
    def __init__(self):
        self.client = Client(URL)
```

or:

```python
def make_env():
    return MyEnv(url)
```

## Rewards Are Always Zero

Check:

- Environment methods update `self.reward` or equivalent state.
- Reward function receives `environments` and returns one scalar per environment.
- Environment is not reset before reward is read in the installed trainer behavior.
- The model can actually call the exposed tool with the chat template/model pair.

## Model Never Calls Tools

Check:

- The chat template supports tool calling.
- Tool names and docstrings are clear.
- The prompt asks for tool use.
- `max_completion_length` allows enough tokens for tool call and final answer.
- The model family has tool-calling capability or has been SFT-trained for it.

## OpenReward Auth Or URL Fails

For catalog environments, set the API key expected by the SDK:

```bash
export OPENREWARD_API_KEY=...
```

For local/single-host servers, set:

```bash
export OPENREWARD_API_URL=http://127.0.0.1:8000
export OPENREWARD_SESSION_URL=http://127.0.0.1:8000
```

## vLLM With Experimental Online Trainers Fails

Use the same rules as stable GRPO/RLOO:

- Install `trl[vllm]`.
- Keep server and trainer GPUs separate in server mode.
- Confirm the experimental trainer config actually has `use_vllm` and `vllm_mode` fields in the installed package.

## API Moved

Experimental modules move. Inspect before coding:

```bash
python - <<'PY'
import inspect
from trl.experimental.online_dpo import OnlineDPOTrainer, OnlineDPOConfig
print(inspect.signature(OnlineDPOTrainer))
print(inspect.signature(OnlineDPOConfig))
PY
```

Do the same for any experimental module used.
