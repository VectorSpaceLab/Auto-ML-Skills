# Agentic Data Formats

## Generic Tool Task

```json
{
  "prompt": "Solve the task using tools when useful.",
  "label": "expected_result",
  "metadata": {
    "task_id": "task-001",
    "tool_config": {"backend": "local"},
    "reward_config": {"type": "exact_or_verifier"}
  }
}
```

Use:

```bash
--input-key prompt
--label-key label
--metadata-key metadata
```

## Coding-Agent Task

```json
{
  "prompt": "Issue body fallback",
  "label": "instance_id",
  "metadata": {
    "workdir": "/workspace/repo",
    "problem_statement": "Fix the failing behavior...",
    "eval_cmd": "pytest -q tests/test_target.py"
  }
}
```

Sandbox-specific image or routing fields belong in metadata, not hardcoded in the hook.

## Multi-Segment Output

For one environment trajectory split into multiple trainable samples:

- Keep `group_id` shared.
- Set `loss_mask` per segment.
- Avoid duplicating full reward across all segments unless intended.
