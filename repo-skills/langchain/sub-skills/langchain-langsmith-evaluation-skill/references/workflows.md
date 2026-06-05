# LangSmith Evaluation Workflows

## No-Key Planning

1. Define the task and expected outputs.
2. Decide dataset schema and example count.
3. Pick evaluator types: exact match, embedding similarity, LLM-as-judge, custom function, or metadata checks.
4. Run import/env check.
5. Ask for credentials before service calls.

## Live Evaluation Checklist

1. Confirm `LANGSMITH_API_KEY` and endpoint.
2. Create or select dataset.
3. Define target runnable/function with deterministic config where possible.
4. Run evaluation with an experiment name that includes date, model/provider, and code version.
5. Compare experiments and report metric deltas plus example-level failures.

## Privacy

Do not upload private user data, secrets, or regulated records without explicit approval and a retention policy.
