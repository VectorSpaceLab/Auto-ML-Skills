---
name: langchain-local-evaluation-skill
description: "Use when a user wants LangChain local evaluators, load_evaluator, exact match, regex match, JSON validity, string distance, criteria evaluators, QA evaluators, or no-service evaluation smoke tests."
disable-model-invocation: true
---

# LangChain Local Evaluation

Use `langchain-local-evaluation-skill` for local/classic evaluator workflows that do not require LangSmith datasets or hosted evaluation. Quick answer: start with deterministic string/JSON evaluators, add optional dependencies such as `rapidfuzz` only when needed, and run [scripts/smoke_local_evaluators.py](scripts/smoke_local_evaluators.py).

## Short Workflow

1. Decide whether the evaluation is local-only or LangSmith-backed.
2. For local deterministic checks, use:
   - `ExactMatchStringEvaluator`
   - `RegexMatchStringEvaluator`
   - `JsonValidityEvaluator`
3. For string distance, install `rapidfuzz` before using `StringDistanceEvalChain`.
4. For LLM-judged criteria or QA evaluators, pass an LLM explicitly and validate with fake or local models first.
5. Run [scripts/smoke_local_evaluators.py](scripts/smoke_local_evaluators.py).
6. Read [references/local-evaluators.md](references/local-evaluators.md) for evaluator selection and output shapes.

## Bundled Scripts

- [scripts/smoke_local_evaluators.py](scripts/smoke_local_evaluators.py): no-key checks for exact match, regex, JSON validity, and optional string distance.
- [scripts/inspect_local_evaluators.py](scripts/inspect_local_evaluators.py): import/signature inspection for local evaluator APIs.

## References

- [references/api-reference.md](references/api-reference.md): public evaluator imports and signatures.
- [references/local-evaluators.md](references/local-evaluators.md): deterministic, distance, and LLM-judged evaluator workflow.
- [references/troubleshooting.md](references/troubleshooting.md): missing `rapidfuzz`, evaluator type mismatch, and empty score issues.

## Boundaries

Use LangSmith evaluation skill for hosted datasets, experiments, traces, and service-backed eval loops. Use this skill for local evaluator objects and no-service regression checks.
