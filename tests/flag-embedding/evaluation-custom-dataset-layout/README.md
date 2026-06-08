# Evaluation Custom Dataset Layout

## User Persona
Applied researcher preparing a local retrieval evaluation dataset.

## Scenario Coverage
- Skill area: evaluation
- Capability: custom dataset layout and validation
- Difficulty: intermediate
- Prompt file: `user_request.txt`
- Expected references/scripts: `sub-skills/evaluation/SKILL.md`, `sub-skills/evaluation/references/data-formats.md`, `sub-skills/evaluation/scripts/validate_custom_eval_dataset.py`
- Trigger expectation: The prompt names FlagEmbedding evaluation and custom retrieval dataset files.

## Expected Successful Behavior
The agent should show `corpus.jsonl`, `<split>_queries.jsonl`, `<split>_qrels.jsonl`, example rows, validation command, and then a custom evaluation command.

## Failure Signals
The agent assumes a benchmark download instead of local files, omits qrels, or provides a layout the validator would reject.
