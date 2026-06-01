# Experimental Map

Read this before using or editing `trl.experimental`.

## Stability

`trl.experimental` is a shipped incubation area for fast-moving ideas. APIs can change or disappear without deprecation. Avoid using it for production unless the user accepts frequent updates.

## Experimental Areas Seen In Source

The inspected source tree included these experimental modules:

- `async_grpo`
- `bco`
- `bema_for_ref_model`
- `cpo`
- `distillation`
- `dppo`
- `gfpo`
- `gkd`
- `gold`
- `grpo_with_replay_buffer`
- `gspo_token`
- `kto`
- `minillm`
- `nash_md`
- `online_dpo`
- `openenv`
- `openreward`
- `orpo`
- `papo`
- `ppo`
- `prm`
- `sdft`
- `sdpo`
- `self_distillation`
- `ssd`
- `tpo`
- `xpo`

## Common Use Cases

| Need | Likely module |
| --- | --- |
| KTO / unpaired preference optimization | `trl.experimental.kto` |
| Online DPO with generated completions and reward model | `trl.experimental.online_dpo` |
| PPO-style RLHF | `trl.experimental.ppo` |
| Knowledge distillation | `trl.experimental.gkd`, `trl.experimental.minillm`, `trl.experimental.distillation` |
| Odds-ratio / contrastive preference variants | `trl.experimental.orpo`, `trl.experimental.cpo`, `trl.experimental.bco`, `trl.experimental.sdpo` |
| Process reward modeling | `trl.experimental.prm` |
| Environment integrations | `trl.experimental.openreward`, OpenEnv examples with stable `GRPOTrainer` |
| Nash/XPO online methods with vLLM support | `trl.experimental.nash_md`, `trl.experimental.xpo` |

## KTO

Docs classify KTO as experimental in TRL v1:

```python
from trl.experimental.kto import KTOConfig, KTOTrainer
```

Expected data is unpaired preference. A paired preference dataset can be converted to unpaired data by the trainer.

Key config fields:

- `beta`
- `desirable_weight`
- `undesirable_weight`
- `loss_type`

## Online DPO

```python
from trl.experimental.online_dpo import OnlineDPOConfig, OnlineDPOTrainer
```

Use prompt-only data and a reward model or reward functions. Online DPO can use vLLM for generation.

## GKD

```python
from trl.experimental.gkd import GKDConfig, GKDTrainer
```

Use for generalized knowledge distillation with student and teacher models. Important config fields in docs include `lmbda`, `seq_kd`, and `beta`.

## PPO

PPO lives under `trl.experimental.ppo` in the inspected tree. Use it for legacy or experimental PPO workflows, not as the default stable path for new online training. Prefer GRPO/RLOO when they fit.

## PRM

Process reward modeling uses stepwise supervision data with `prompt`, `completions`, and `labels`. Treat API details as version-sensitive.

## Source Development Note

Experimental code may be less stable and less consistent than main code, but small non-invasive consistency improvements are encouraged. Avoid large refactors in experimental modules unless the user explicitly asks.
