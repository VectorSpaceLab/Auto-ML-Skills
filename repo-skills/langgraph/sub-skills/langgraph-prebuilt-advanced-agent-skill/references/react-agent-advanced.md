# React Agent Advanced Options

## Common Options

`create_react_agent` supports advanced options such as:

- `prompt`
- `response_format`
- `pre_model_hook`
- `post_model_hook`
- `state_schema`
- `context_schema`
- `checkpointer`
- `store`
- `interrupt_before`
- `interrupt_after`
- `version`
- `name`

Inspect the installed signature because this surface changes across LangGraph releases.

## Structured Response Boundary

`response_format` requires a model path that can produce structured output, usually through `.with_structured_output()` or provider-native schema support. A plain local Transformers model may not satisfy this automatically.

## Hooks

Hooks must return valid state updates. Use them for:

- trimming/summarizing messages before model call
- injecting system/context messages
- validating model output after the call
- collecting side-channel metadata

Do not mutate state in-place and assume LangGraph noticed; return the update explicitly.

## Remaining Steps

Agent loops need a remaining-step budget to avoid infinite tool/model cycles. If a graph stops unexpectedly, inspect `remaining_steps` state and tool loop conditions.
