# Local Evaluator Troubleshooting

## `rapidfuzz` Missing

`StringDistanceEvalChain` requires `rapidfuzz`. Install it or skip distance checks in no-key smoke tests.

## Regex Score Is Zero

Ensure the regex is passed as `reference`, escape backslashes correctly, and set flags such as `re.IGNORECASE` when needed.

## JSON Validity Passes But Schema Is Wrong

`JsonValidityEvaluator` checks parseability, not schema. Use a schema evaluator or output parser for structure validation.

## LLM Evaluator Requires A Model

Criteria and QA evaluators need an explicit `llm`. Use fake/local models for smoke tests, but treat real scores as model-dependent.

## Unexpected Output Keys

Inspect the result dictionary. Do not hard-code keys beyond what that evaluator documents or returns in your smoke test.
