# PPO Megatron Config Troubleshooting

## Critic Resources Missing

If critic resource flags are omitted, slime may default critic resources to actor-style settings. Explicitly set critic nodes/GPUs for clarity.

## YAML Does Not Change Placement

`num_nodes` and GPU counts in YAML are not the placement mechanism. Use CLI resource flags.

## Different Parallel Topology

Avoid role-specific tensor/pipeline/context/expert parallel differences unless the current slime version explicitly supports the case.
