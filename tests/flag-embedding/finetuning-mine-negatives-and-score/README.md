# Finetuning Mine Negatives And Score

## User Persona
Retrieval engineer improving training data before fine-tuning.

## Scenario Coverage
- Skill area: finetuning
- Capability: hard-negative mining and teacher-score generation
- Difficulty: advanced
- Prompt file: `user_request.txt`
- Expected references/scripts: `sub-skills/finetuning/SKILL.md`, `sub-skills/finetuning/references/training-workflows.md`, `sub-skills/finetuning/scripts/mine_hard_negatives.py`, `sub-skills/finetuning/scripts/add_reranker_scores.py`
- Trigger expectation: The prompt names mining negatives and teacher scores with BGE models.

## Expected Successful Behavior
The agent should validate input first, run the bundled hard-negative script, then run the bundled teacher-score script, and explicitly mention model downloads, FAISS, GPU use, and output files.

## Failure Signals
The agent references original repo scripts as the only path, skips validation, does not warn about side effects, or writes over input data.
