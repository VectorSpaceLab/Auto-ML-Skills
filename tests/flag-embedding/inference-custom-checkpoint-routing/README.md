# Inference Custom Checkpoint Routing

## User Persona
Integrator using a local model checkpoint and familiar with retrieval concepts but not FlagEmbedding auto mapping.

## Scenario Coverage
- Skill area: inference
- Capability: explicit model class selection for custom checkpoints
- Difficulty: intermediate
- Prompt file: `user_request.txt`
- Expected references/scripts: `sub-skills/inference/SKILL.md`, `sub-skills/inference/references/api-reference.md`, `references/model-overview.md`, `sub-skills/inference/references/troubleshooting.md`
- Trigger expectation: The prompt mentions `FlagAutoModel`, local checkpoint, and mapping failure, which should route to inference troubleshooting and API details.

## Expected Successful Behavior
The agent should explain why auto mapping failed, choose `model_class="encoder-only-base"`, set `pooling_method="cls"`, pass the BGE English retrieval instruction, use `devices=["cuda:0"]`, and include `encode_queries()`/`encode_corpus()`.

## Failure Signals
The agent suggests changing source mappings, guesses unsupported class values, omits pooling, tells the user to inspect original repo paths, or sets `trust_remote_code=True` without a reason.
