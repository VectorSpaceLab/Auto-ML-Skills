# Bad Loaded Results

## User Persona
The user is debugging an adapter that appears to load but performs badly.

## Scenario Coverage
- Skill area: `adapter-loading-and-composition`
- Capability: correct adapter loading, `PeftConfig`, `PeftModel.from_pretrained`, `modules_to_save`, resized embeddings, status checks
- Difficulty: troubleshooting
- Prompt file: `user_request.txt`
- Expected references/scripts: `skills/peft/sub-skills/adapter-loading-and-composition/SKILL.md`, `skills/peft/sub-skills/adapter-loading-and-composition/references/loading-checkpoints.md`, `skills/peft/references/troubleshooting.md`, `skills/peft/sub-skills/adapter-loading-and-composition/scripts/inspect_adapter_state.py`
- Trigger expectation: The prompt mentions PEFT adapter reload, random predictions, a trained task head, and tokenizer changes.

## Expected Successful Behavior
The agent should distinguish `get_peft_model` from `PeftModel.from_pretrained`, load the compatible base model, resize tokenizer embeddings the same way as training, ensure the trained task head was included in `modules_to_save` or saved otherwise, run model/layer status checks, and suggest a small deterministic validation input.

## Failure Signals
The answer fails if it only says to call `.eval()`, ignores the task head and added tokens, suggests reinitializing with `get_peft_model`, or cannot name concrete inspection commands.
