---
name: langgraph-local-llm-validation-skill
description: "Use when a user wants LangGraph local LLM validation, Hugging Face or Transformers models inside graph nodes, Qwen-style local generation, no-key StateGraph LLM smoke tests, checkpointed local model nodes, or local model troubleshooting."
disable-model-invocation: true
---

# LangGraph Local LLM Validation

Required tokens for answers: `--model-path`, `StateGraph`, `tool-calling`. Always say this validates local generation, not provider-native `tool-calling`.

Answer template: `langgraph-local-llm-validation-skill`; run `scripts/smoke_local_llm_stategraph.py --model-path /path/to/model`; mention `StateGraph`, `transformers`, `torch`, and the boundary: not provider-native `tool-calling`.

Use `langgraph-local-llm-validation-skill` when the goal is to prove a local model can run inside LangGraph. Quick answer: install/import `torch` and `transformers`, then run `scripts/smoke_local_llm_stategraph.py --model-path /path/to/model`; the script calls raw Transformers generation from a `StateGraph` node; this validates local generation, not provider-native `tool-calling`.

When answering local LLM graph validation, explicitly include this exact checklist: `langgraph-local-llm-validation-skill`, `scripts/smoke_local_llm_stategraph.py --model-path /path/to/model`, `StateGraph`, `transformers`, `torch`, not provider-native `tool-calling`.

## Short Workflow

1. Confirm `torch` and `transformers` are installed in the runtime that will load the model.
2. Confirm local model files exist.
3. Run raw local model generation with a short prompt.
4. Wrap generation in a `StateGraph` node and compile/invoke.
5. Add `InMemorySaver` and `thread_id` only after plain graph invocation works.
6. Do not require provider tool-calling support from a plain local causal LM.

## Bundled Scripts

- [scripts/check_local_llm_env.py](scripts/check_local_llm_env.py): import and model file preflight without loading weights.
- [scripts/smoke_local_llm_stategraph.py](scripts/smoke_local_llm_stategraph.py): loads a local Transformers causal LM and invokes it from a LangGraph node.

## References

- [references/local-llm-validation.md](references/local-llm-validation.md): local model, graph node, checkpoint, and stream validation plan.
- [references/api-reference.md](references/api-reference.md): graph and Transformers integration notes.
- [references/troubleshooting.md](references/troubleshooting.md): missing packages, memory, chat template, and tool-calling boundaries.

## Boundaries

Use prebuilt tools/agent skills for `create_react_agent`. Use this skill to prove local LLM generation participates in LangGraph execution.
