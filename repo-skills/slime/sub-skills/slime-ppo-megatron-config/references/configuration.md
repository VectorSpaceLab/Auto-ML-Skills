# PPO And Megatron Role Configuration

## PPO Core Flags

```bash
--advantage-estimator ppo
--use-critic
--critic-load /checkpoints/critic_torch_dist
--critic-save /runs/critic
--critic-lr 1e-5
--num-critic-only-steps 0
--eps-clip 0.2
--value-clip 0.2
--kl-coef 0.0
```

## Resource Example

```bash
--actor-num-nodes 1
--actor-num-gpus-per-node 4
--critic-num-nodes 1
--critic-num-gpus-per-node 4
--rollout-num-gpus 8
```

Requires 16 GPUs.

## Role Override YAML

```yaml
megatron:
  - name: default
    role: actor
    overrides:
      lr: 1e-6
  - name: default
    role: critic
    overrides:
      lr: 1e-5
      load: /checkpoints/critic
      save: /runs/critic
```

Launch with:

```bash
--megatron-config-path megatron_ppo.yaml
```
