# Finetuning Validate Distillation Data

## User Persona
Data engineer preparing retrieval training rows for model fine-tuning.

## Scenario Coverage
- Skill area: finetuning
- Capability: JSONL schema validation for distillation
- Difficulty: troubleshooting
- Prompt file: `user_request.txt`
- Expected references/scripts: `sub-skills/finetuning/SKILL.md`, `sub-skills/finetuning/references/data-formats.md`, `sub-skills/finetuning/scripts/validate_finetune_jsonl.py`
- Trigger expectation: The prompt names fine-tuning, BGE-M3, distillation, and JSONL train data.

## Expected Successful Behavior
The agent should run or recommend `validate_finetune_jsonl.py --require-scores`, explain required fields and score-list length alignment, and avoid launching training until validation passes.

## Failure Signals
The agent jumps to a full `torchrun` command without validating data, omits `pos_scores`/`neg_scores` alignment, or points to original repo data examples as required runtime dependencies.
