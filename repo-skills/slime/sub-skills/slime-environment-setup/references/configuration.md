# Environment Configuration

Read this when filling runtime environment variables and GPU resource flags.

## Required Environment Variables

For Ray job runtime:

```json
{
  "env_vars": {
    "PYTHONPATH": "/path/to/Megatron-LM",
    "CUDA_DEVICE_MAX_CONNECTIONS": "1",
    "PYTHONUNBUFFERED": "1"
  }
}
```

Optional deterministic or hardware-specific variables belong in other sub-skills.

## Resource Math

Colocated:

```bash
--actor-num-nodes 1
--actor-num-gpus-per-node 8
--colocate
```

Requires 8 GPUs total. `--rollout-num-gpus` is ignored under colocate.

Decoupled:

```bash
--actor-num-nodes 1
--actor-num-gpus-per-node 8
--rollout-num-gpus 8
--rollout-num-gpus-per-engine 2
```

Requires 16 GPUs total.

PPO with critic can require actor + critic + rollout resources:

```bash
--actor-num-gpus-per-node 4
--critic-num-gpus-per-node 4
--rollout-num-gpus 8
```

Requires 16 GPUs total.

## Async Driver

Use `run_slime_train_async.py` for fully async rollout or SFT data prefetch. It asserts that `--colocate` is not set. If the user needs colocate, use the synchronous runner.

## Minimal Package Checks

Expected package-level checks:

```bash
python - <<'PY'
import slime, slime_plugins
from slime.utils.types import Sample
from slime.rollout.base_types import RolloutFnTrainOutput, RolloutFnEvalOutput
print("ok")
PY
```

Strict training check:

```bash
PYTHONPATH=/path/to/Megatron-LM:$PYTHONPATH python - <<'PY'
import megatron.training.arguments
import slime.backends.megatron_utils.arguments
print("ok")
PY
```
