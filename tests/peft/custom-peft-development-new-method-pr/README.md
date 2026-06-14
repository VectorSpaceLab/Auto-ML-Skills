# New Method PR

## User Persona
The user is a contributor planning a substantial PEFT feature.

## Scenario Coverage
- Skill area: `custom-peft-development`
- Capability: new PEFT method checklist, registration, tests, docs, contribution and AI policy
- Difficulty: advanced
- Prompt file: `user_request.txt`
- Expected references/scripts: `skills/peft/sub-skills/custom-peft-development/SKILL.md`, `skills/peft/sub-skills/custom-peft-development/references/new-method-pr-checklist.md`, `skills/peft/SKILL.md`
- Trigger expectation: The prompt mentions contributing a new PEFT method and an AI-assisted PR.

## Expected Successful Behavior
The agent should warn about AI-assisted contribution guideline breaches, require issue/maintainer coordination before coding, list `PeftType`, tuner package files, `register_peft_method`, public exports, mappings, tests, docs, examples, and focused commands such as `pytest tests/test_custom_models.py -k <method> -v` and `make style`.

## Failure Signals
The answer fails if it starts coding without coordination, omits AI disclosure requirements, suggests a tiny unapproved PR, or lacks concrete repo file targets.
