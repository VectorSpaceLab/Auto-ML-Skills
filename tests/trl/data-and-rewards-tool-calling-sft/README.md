# Tool Calling SFT Data

## User Persona
A dataset engineer preparing structured chat data for TRL SFT.

## Scenario Coverage
- Skill area: `data-and-rewards`
- Capability: tool-calling conversational data, `tools` column, JSON schema, datasets `Json`
- Difficulty: advanced
- Prompt file: `user_request.txt`
- Expected references/scripts: `data-and-rewards/SKILL.md`, `data-and-rewards/references/data-formats.md`
- Trigger expectation: The prompt asks for TRL dataset shape and tool-calling schema details.

## Expected Successful Behavior
The agent should describe `messages` plus `tools`, show assistant `tool_calls` and tool response rows, use `transformers.utils.get_json_schema`, and explain `Dataset.from_list(..., on_mixed_types="use_json")` or explicit `datasets.Json` features for arbitrary JSON arguments.

## Failure Signals
The response flattens tool calls into plain text only, omits the `tools` column, uses ad hoc schema strings, or ignores mixed JSON feature handling.
