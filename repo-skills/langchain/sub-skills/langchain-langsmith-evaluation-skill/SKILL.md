---
name: langchain-langsmith-evaluation-skill
description: "Use when a user wants LangSmith tracing, datasets, examples, evaluation, experiment comparison, offline evaluator planning, or no-key LangSmith client import checks."
disable-model-invocation: true
---

# LangChain LangSmith Evaluation

Use `langchain-langsmith-evaluation-skill` for LangSmith datasets, traces, experiments, and evaluation planning. Quick answer: tracing is configured by environment variables; evaluation uses LangSmith client/datasets and may require `LANGSMITH_API_KEY`; no-key validation uses `scripts/check_langsmith_eval_env.py`.

## Short Workflow

1. For tracing-only setup, route to observability/config if no datasets/evaluators are involved.
2. For evaluation, confirm `langsmith` import, API key availability, dataset name, target function/chain, evaluator(s), and experiment name.
3. Keep no-key smoke local: run [scripts/check_langsmith_eval_env.py](scripts/check_langsmith_eval_env.py).
4. Read [references/api-reference.md](references/api-reference.md) and [references/workflows.md](references/workflows.md) before live LangSmith calls.
5. Do not print API keys or upload private examples without user approval.

## Bundled Scripts

- [scripts/check_langsmith_eval_env.py](scripts/check_langsmith_eval_env.py): checks `langsmith` import and relevant environment variables without making network calls.

## References

- [references/api-reference.md](references/api-reference.md): LangSmith client imports and environment variables.
- [references/workflows.md](references/workflows.md): dataset/evaluation planning, experiment naming, and result comparison.
- [references/troubleshooting.md](references/troubleshooting.md): auth, tracing, dataset, evaluator, and network issues.

## Boundaries

Use `langchain-observability-config-skill` for callbacks/tags/metadata on ordinary runs. Use this skill for evaluation datasets and experiments.
