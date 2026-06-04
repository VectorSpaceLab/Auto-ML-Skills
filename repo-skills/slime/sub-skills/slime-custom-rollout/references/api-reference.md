# Custom Hook API Reference

Verified against slime runtime APIs and plugin contract tests.

## Core Types

```python
from slime.utils.types import Sample
from slime.rollout.base_types import RolloutFnTrainOutput, RolloutFnEvalOutput
```

Important `Sample` fields:

- `tokens: list[int]`
- `response: str`
- `response_length: int`
- `label: str | None`
- `reward: float | dict | None`
- `loss_mask: list[int] | None`
- `status: Sample.Status`
- `metadata: dict`
- `group_id: int | None`
- `rollout_log_probs: list[float] | None`
- `teacher_log_probs: list[float] | None`
- `remove_sample: bool`

## Full Rollout Function

```python
def generate_rollout(args, rollout_id, data_source, evaluation=False) -> RolloutFnTrainOutput | RolloutFnEvalOutput:
    ...
```

Training return:

```python
RolloutFnTrainOutput(samples=list_of_sample_groups, metrics={})
```

Evaluation return:

```python
RolloutFnEvalOutput(data={"dataset": {"rewards": [], "truncated": [], "samples": []}}, metrics={})
```

## Custom Generate

```python
async def custom_generate(args, sample: Sample, sampling_params: dict) -> Sample | list[Sample]:
    ...
```

Returning `list[Sample]` is valid for trajectory segmentation. Sibling segments should share `group_id` so aggregation counts them as one rollout group.

## Custom Reward

Single sample:

```python
async def custom_rm(args, sample: Sample) -> float | dict:
    ...
```

Group mode with `--group-rm`:

```python
async def custom_rm(args, samples: list[Sample]) -> list[float]:
    ...
```

## Filters

Dynamic sampling:

```python
from slime.rollout.filter_hub.base_types import DynamicFilterOutput

def filter_function(args, samples: list[Sample], **kwargs) -> DynamicFilterOutput:
    return DynamicFilterOutput(keep=True, reason=None)
```

Buffer:

```python
def buffer_filter(args, rollout_id, buffer: list[list[Sample]], num_samples: int) -> list[list[Sample]]:
    ...
```

Sample mask:

```python
def rollout_sample_filter(args, groups: list[list[Sample]]) -> None:
    for group in groups:
        for sample in group:
            sample.remove_sample = False
```

## Runtime Hooks

Rollout log:

```python
def log_rollout_data(rollout_id, args, samples, rollout_extra_metrics, rollout_time) -> bool:
    return False
```

Reward postprocess:

```python
def post_process_rewards(args, samples):
    return raw_rewards, processed_rewards
```

Train data conversion:

```python
def convert_samples_to_train_data(args, samples) -> dict:
    return {"tokens": ..., "response_lengths": ..., "rewards": ..., "raw_reward": ..., "truncated": ..., "sample_indices": ..., "loss_masks": ...}
```

## Data Source

```python
class CustomDataSource:
    def __init__(self, args): ...
    def get_samples(self, num_samples: int) -> list[list[Sample]]: ...
    def add_samples(self, samples: list[list[Sample]]): ...
    def save(self, rollout_id): ...
    def load(self, rollout_id=None): ...
    def __len__(self) -> int: ...
```
