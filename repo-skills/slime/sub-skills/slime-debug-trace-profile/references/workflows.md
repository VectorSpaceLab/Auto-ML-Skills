# Debug, Trace, And Profile Workflows

## Rollout Only

```bash
--debug-rollout-only
--save-debug-rollout-data /tmp/rollout_{rollout_id}.pt
--num-rollout 1
```

Use when SGLang generation, reward, custom generate, or custom RM may be failing.

## Train Only Replay

```bash
--debug-train-only
--load-debug-rollout-data /tmp/rollout_{rollout_id}.pt
```

Use when rollout data exists and training/logprob/loss is failing.

## Forge Replay

Use `--load-forge-rollout-data` when you want to replay saved data while keeping SGLang engines, router, weight update, and offload/onload behavior live for memory/performance testing.

## SGLang Profiling

If the rollout router is available:

```bash
python /path/to/slime/tools/profile_rollout.py \
  --router-url http://127.0.0.1:3000 \
  --action start \
  --num-steps 3 \
  --output-dir /tmp/sglang_profile
```

Stop manually:

```bash
python /path/to/slime/tools/profile_rollout.py --router-url http://127.0.0.1:3000 --action stop
```

## CPU Contract Tests

For plugin code, validate import/signature locally before GPU:

```bash
python /path/to/skill/slime/sub-skills/slime-custom-rollout/scripts/validate_custom_hook_import.py \
  --path my_project.generate.custom_generate \
  --kind custom-generate
```
