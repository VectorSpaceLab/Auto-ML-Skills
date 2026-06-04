---
name: slime-agentic-tool-use
description: "Builds slime agentic RL workflows for search, RAG, tool use, sandbox execution, Tau-bench, Strands, multi-agent, and coding-agent rollouts."
disable-model-invocation: true
---

# slime Agentic Tool Use

Use this sub-skill when the user wants tool-calling, RAG/search, multi-turn environments, sandbox rewards, coding-agent RL, Tau-bench, Strands, ReTool, Search-R1, or multi-agent rollout.

## Short Workflow

1. Start with the default hook pattern: `--custom-generate-function-path` plus `--custom-rm-path`.
2. Use `--rollout-function-path` only when the whole orchestration must be replaced.
3. Put per-task inputs in JSONL `metadata` and pass `--metadata-key metadata`.
4. Preserve token provenance: train on model-sampled tokens, not retokenized strings, when building multi-turn trajectories.
5. For long-tail environments, consider `slime-fully-async-rollout`.

Read [references/workflows.md](references/workflows.md) for Search-R1, ReTool, Tau-bench, Strands, multi-agent, and coding-agent patterns. Read [references/data-formats.md](references/data-formats.md) for metadata schemas. Read [references/troubleshooting.md](references/troubleshooting.md) for sandbox, API, and token alignment issues.

## Scripts

- Adapt [scripts/custom_agent_generate.py](scripts/custom_agent_generate.py) as a minimal token-preserving custom generate skeleton.
- Adapt [scripts/search_tool_reward.py](scripts/search_tool_reward.py) for simple rule-based search/tool reward scaffolding.

## Related Sub-Skills

- `slime-custom-rollout` for exact hook signatures.
- `slime-sglang-deployment` for router session affinity and multi-model serving.
- `slime-rollout-correction` if using rollout logprobs/TIS for tool trajectories.
