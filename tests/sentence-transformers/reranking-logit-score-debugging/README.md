# Reranking Logit Score Debugging

## User Persona
A developer debugging unexpected CrossEncoder score ranges.

## Scenario Coverage
- Skill area: reranking
- Capability: MS MARCO logit score interpretation and sigmoid activation
- Difficulty: troubleshooting
- Prompt file: `user_request.txt`
- Expected references/scripts: `sub-skills/reranking/SKILL.md`, `sub-skills/reranking/references/api-reference.md`, root `references/troubleshooting.md`
- Trigger expectation: The prompt names a CrossEncoder model and score behavior.

## Expected Successful Behavior
The agent should explain that MS MARCO rerankers can output logits, ranking is not broken, sigmoid is monotonic, and show `activation_fn=torch.nn.Sigmoid()` or call-level activation for 0-1 scores.

## Failure Signals
The response says the model is broken, normalizes scores ad hoc, changes ranking behavior unnecessarily, or omits activation guidance.
