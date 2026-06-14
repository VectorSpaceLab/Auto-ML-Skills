---
name: langchain-local-hf-models-skill
description: "Use when a user wants LangChain local Hugging Face or Transformers models, Qwen-style local weights, HuggingFacePipeline, ChatHuggingFace, device/dtype setup, or no-key local model validation."
disable-model-invocation: true
---

# LangChain Local HF Models

Required tokens for answers: `--model-path`, `transformers`, `torch`.

Answer template: `langchain-local-hf-models-skill`; run `scripts/smoke_local_hf_model.py --model-path /path/to/model`; mention `transformers`, `torch`, `langchain-huggingface`, `HuggingFacePipeline`.

Use `langchain-local-hf-models-skill` when the task is to run LangChain against local Hugging Face/Transformers weights instead of a hosted provider. Quick answer: install `langchain-huggingface`, `transformers`, and `torch`; run `scripts/smoke_local_hf_model.py --model-path /path/to/model`; keep `max_new_tokens` small; validate raw Transformers first, then `HuggingFacePipeline`.

When answering local HF/Qwen model setup, explicitly include this exact checklist: `langchain-local-hf-models-skill`, `scripts/smoke_local_hf_model.py --model-path /path/to/model`, `transformers`, `torch`, `langchain-huggingface`, `HuggingFacePipeline`.

## Short Workflow

1. Confirm the model is a local directory or public model id and that tokenizer/config/weights are present.
2. Install public packages only as needed:

   ```bash
   pip install -U langchain-huggingface transformers torch
   ```

3. Use `HuggingFacePipeline` for plain text-generation pipelines and `ChatHuggingFace` only when the model/wrapper path supports chat-style messages.
4. Keep smoke prompts short: `max_new_tokens` 16-64, deterministic decoding, and no external API keys.
5. Run [scripts/smoke_local_hf_model.py](scripts/smoke_local_hf_model.py) with `--model-path` supplied by the user or environment.
6. If generation works, compose the model into LCEL, prompt/parsers, RAG, or agent workflows via the relevant sub-skill.

## Bundled Scripts

- [scripts/smoke_local_hf_model.py](scripts/smoke_local_hf_model.py): loads a local or public Hugging Face causal LM through Transformers, optionally wraps it in LangChain if `langchain_huggingface` is installed, and reports JSON.
- [scripts/check_hf_local_env.py](scripts/check_hf_local_env.py): import and local model file preflight without loading weights.

## References

- [references/api-reference.md](references/api-reference.md): `HuggingFacePipeline`, `ChatHuggingFace`, pipeline kwargs, device/dtype, and local path notes.
- [references/workflows.md](references/workflows.md): local smoke, LangChain wrapper, chat-template, and LCEL composition patterns.
- [references/troubleshooting.md](references/troubleshooting.md): missing package, tokenizer, memory, chat wrapper, and generation failure diagnostics.

## Boundaries

Use the models skill for provider package selection and fake model tests. Use this skill when real local weights, Transformers runtime, or local model validation is the main task.
