# Local LLM Validation

## Validation Ladder

1. File/import preflight:

   ```bash
   python scripts/check_local_llm_env.py --model-path /path/to/model
   ```

2. Raw generation inside a graph node:

   ```bash
   python scripts/smoke_local_llm_stategraph.py --model-path /path/to/model
   ```

3. Checkpointed invocation:

   Add `checkpointer=InMemorySaver()` and pass a stable `thread_id`.

4. Streaming/debug:

   Once invoke works, test `graph.stream(..., stream_mode="updates")`.

## Prompt Handling

For chat-tuned models, try tokenizer chat templates:

```python
tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
```

If a model-specific template supports additional options, keep them in runtime code, not generic LangGraph instructions.

## Resource Controls

- `max_new_tokens`: keep small for smoke tests
- `do_sample=False`: deterministic smoke
- device: prefer GPU when available, CPU otherwise
- output: assert non-empty, not semantic correctness

## What Success Means

A passing local LLM graph smoke proves:

- the model loads
- generation returns text
- a LangGraph node can call the model
- `StateGraph.compile().invoke()` completes

It does not prove tool-calling or structured-output support.
