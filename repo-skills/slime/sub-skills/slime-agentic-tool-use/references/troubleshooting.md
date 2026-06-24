# Agentic Tool-Use Troubleshooting

## Sandbox Cannot Reach Model Adapter

Use a routable head-node IP, not `127.0.0.1`, when the sandbox runs outside the Ray head process.

## Tool Calls Not Parsed

Set SGLang parser flags matching the model:

```bash
--sglang-tool-call-parser <parser>
--sglang-reasoning-parser <parser>
```

## Token Drift In Multi-Turn Trajectories

Do not retokenize final strings to reconstruct training tokens. Store token IDs and logprobs from SGLang responses and mask unproven prompt/tool-observation suffixes.

## Long-Tail Generation Blocks Training

Use `slime-fully-async-rollout`, reduce task timeout, or add partial rollout/requeue logic.
