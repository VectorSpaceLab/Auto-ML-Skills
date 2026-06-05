# LangSmith Evaluation Troubleshooting

- Import fails: install `langsmith`.
- Unauthorized: check `LANGSMITH_API_KEY` without printing it.
- Traces missing: set `LANGSMITH_TRACING=true` and ensure callbacks/config do not disable tracing.
- Dataset shape mismatch: inspect one example's inputs/outputs before bulk upload.
- Evaluator is flaky: lower concurrency, add deterministic target settings, or use non-LLM metrics for smoke checks.
- Network or endpoint issue: verify `LANGSMITH_ENDPOINT` and service reachability.
