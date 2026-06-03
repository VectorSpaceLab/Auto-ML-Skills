# OPD Workflows

## SGLang Teacher

Teacher logprobs are obtained through a SGLang-compatible service:

```bash
--use-opd
--opd-type sglang
--opd-kl-coef 1.0
--custom-rm-path slime.rollout.on_policy_distillation.reward_func
--custom-reward-post-process-path slime.rollout.on_policy_distillation.post_process_rewards
--rm-url http://teacher-host:port/generate
```

Do not set `--opd-teacher-load` in this mode.

## Megatron Teacher

Teacher model is loaded by Megatron:

```bash
--use-opd
--opd-type megatron
--opd-kl-coef 1.0
--opd-teacher-load /checkpoints/teacher_torch_dist
```

Use `--opd-teacher-ckpt-step` to select a checkpoint step when needed.

## Placement Considerations

Megatron teacher mode increases training-side memory and compute. SGLang teacher mode depends on external serving capacity and network behavior.
