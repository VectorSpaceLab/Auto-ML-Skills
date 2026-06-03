---
name: slime-coding-agent-rl
description: "Builds slime SWE and coding-agent RL workflows with Anthropic/OpenAI adapters, sandbox metadata, patch grading, fan-out samples, and token-provenance validation."
disable-model-invocation: true
---

# slime Coding-Agent RL

Use this sub-skill when the user asks for SWE-bench style coding-agent RL, Claude Code/OpenAI agent adapters, sandbox execution, patch grading, tool-use trajectories, or fan-out training samples.

## Short Workflow

1. Confirm the base slime RL path works first with `slime-rl-training`.
2. Prepare JSONL rows with `prompt`, `label`, and `metadata`; validate them with [scripts/validate_swe_jsonl.py](scripts/validate_swe_jsonl.py).
3. Configure sandbox metadata and reachable adapter host/port; read [references/sandbox.md](references/sandbox.md).
4. Use `--custom-generate-function-path` for the coding-agent generate loop and set `--metadata-key metadata`.
5. Set SGLang tool-call and reasoning parsers that match the served model.
6. Keep rollout dumps enabled for trajectory inspection and reward debugging.
7. Verify token provenance and fan-out semantics with a tiny dataset before increasing `rollout_batch_size` or `n_samples_per_prompt`.

Read [references/workflows.md](references/workflows.md) for the full coding-agent flow. Read [references/data-formats.md](references/data-formats.md) for JSONL schema. Read [references/troubleshooting.md](references/troubleshooting.md) for adapter, sandbox, and token-alignment failures.

## Scripts

- [scripts/validate_swe_jsonl.py](scripts/validate_swe_jsonl.py): validates coding-agent RL JSONL rows and metadata keys before launch.
- [scripts/coding_agent_args.sh](scripts/coding_agent_args.sh): read and adapt this args block for coding-agent rollouts.

## Related Sub-Skills

- `slime-agentic-tool-use` for general tool/RAG/multi-agent rollouts.
- `slime-custom-rollout` for hook signatures and `Sample` construction.
- `slime-sglang-deployment` for router session affinity and parser flags.
- `slime-debug-trace-profile` for rollout dump replay and trace inspection.
