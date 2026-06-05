# Local Evaluator Workflows

## Regression Checks

Use deterministic evaluators for CI or local tests:

- exact match for canonical outputs
- regex match for structured strings
- JSON validity for parser outputs
- JSON schema evaluators when schema validation is required

## Similarity Or Distance

Use string distance when exact match is too strict. Install `rapidfuzz` and record the distance metric. Normalize scores when comparing across examples.

## LLM-Judged Criteria

Use LLM-judged evaluators when correctness depends on semantics. Keep these points explicit:

- evaluator model
- rubric or criteria
- prediction/reference/input fields
- randomness settings
- failure threshold

## Output Shape

Evaluator results are dictionaries. Common keys include:

- `score`
- `value`
- `reasoning`
- evaluator-specific metadata

Do not assume every evaluator returns every key.

## LangSmith Boundary

Local evaluators can be used inside LangSmith workflows, but this skill covers only the local evaluator objects. Dataset upload, experiments, tracing, and comparison views belong to the LangSmith evaluation skill.
