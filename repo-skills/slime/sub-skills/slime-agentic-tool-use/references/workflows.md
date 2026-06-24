# Agentic Workflow Patterns

## Search-R1 / RAG

Use a custom generate function that calls search/retrieval between model turns:

```bash
--custom-generate-function-path my_search.generate
--custom-rm-path my_search.reward
--prompt-data /data/search_train.jsonl
--metadata-key metadata
```

If using TIS, ensure generated samples include rollout log probabilities; route to `slime-rollout-correction`.

## ReTool

Typical two-stage pattern:

1. SFT on tool traces with `slime-sft-training`.
2. RL with custom tool execution and reward.

Use sandboxed tool execution for untrusted code.

## Tau-Bench

Tau-bench style workflows need:

- Task environment configuration in metadata.
- User simulator API credentials or local simulator.
- Tool-call parser compatible with the served model.
- Reward that reflects task success, not only text matching.

## Strands

Strands-style agent loops can be connected through a custom generate function. Preserve token IDs from SGLang generation instead of retokenizing agent messages after the fact.

## Multi-Agent

If one prompt spawns multiple trainable segments, return `list[Sample]` from `custom_generate` and assign a shared `group_id`. Split a trajectory reward across segments if needed to avoid reward amplification.

## Coding-Agent RL

Coding-agent RL usually needs:

- A sandbox backend.
- Host-side bootstraps or images.
- A reachable adapter endpoint from sandbox to rollout head.
- A clean evaluation sandbox to prevent test cheating.
- Dataset metadata describing workdir, problem statement, and grader.

Use longer timeouts and save rollout dumps for auditability.
