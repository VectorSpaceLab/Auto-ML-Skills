# KTO Experimental Warning

## User Persona
A researcher using TRL experimental methods and reviewing implementation quality.

## Scenario Coverage
- Skill area: `experimental-trainers`
- Capability: KTO import path, experimental warning, unpaired preference data, paper index review rule
- Difficulty: intermediate
- Prompt file: `user_request.txt`
- Expected references/scripts: `experimental-trainers/SKILL.md`, `references/experimental-reference.md`
- Trigger expectation: The prompt names `TRLExperimentalWarning`, KTO, and PR review of paper-based trainer work.

## Expected Successful Behavior
The agent should state that KTO is experimental, show `from trl.experimental.kto import KTOConfig, KTOTrainer`, provide a compact skeleton, describe unpaired preference data with labels, and mention updating `docs/source/paper_index.md` with Hugging Face paper links for paper implementations.

## Failure Signals
The response presents KTO as stable, uses only root imports without warning, omits dataset format, or ignores the paper-index review requirement.
