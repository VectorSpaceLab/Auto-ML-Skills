# Inference Embedder Smoke Test

## User Persona
New user who understands embeddings broadly but does not know FlagEmbedding's package APIs.

## Scenario Coverage
- Skill area: inference
- Capability: install verification, no-download import check, minimal embedder workflow
- Difficulty: basic
- Prompt file: `user_request.txt`
- Expected references/scripts: `skills/flag-embedding/SKILL.md`, `sub-skills/inference/SKILL.md`, `sub-skills/inference/scripts/inference_smoke_test.py`, `sub-skills/inference/references/workflows.md`
- Trigger expectation: The prompt names FlagEmbedding and embedding, which should trigger the root skill and inference sub-skill.

## Expected Successful Behavior
The agent should run or recommend the no-download environment check, provide the optional model-loading smoke command only after acknowledging download side effects, and describe single-query/single-passage output shapes.

## Failure Signals
The agent skips verification, claims a model was downloaded without running it, relies on original repo examples instead of bundled scripts, leaks private conda paths, or omits query/passages API distinction.
