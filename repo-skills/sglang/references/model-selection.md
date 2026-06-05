# Public Model Selection

Use public model identifiers or placeholders in all examples. Do not include local model directories.

Recommended placeholders:

- General text smoke: `Qwen/Qwen3-0.6B` or `<MODEL_ID>`.
- OpenAI chat smoke: `Qwen/Qwen3-0.6B` when the environment can run it; otherwise keep `<MODEL_ID>`.
- Embedding smoke: `<EMBEDDING_MODEL_ID>` with `--is-embedding`; examples often use BGE/GTE/E5-family models.
- Vision-language smoke: `<VLM_MODEL_ID>`; use an explicit VLM only when the user requests vision.
- Rerank/reward smoke: `<RERANK_MODEL_ID>` or `<REWARD_MODEL_ID>` with the endpoint-specific sub-skill.
- LoRA smoke: `<BASE_MODEL_ID>` and `<LORA_ADAPTER_PATH_OR_ID>`; local adapter paths are acceptable only in user-specific commands, not in reusable skill docs.

Rules:

- Prefer exact public IDs when the user names a model.
- Use `<MODEL_ID>` when hardware requirements are unclear.
- Mention hardware needs for large or multimodal models.
- Never write creator inspection paths, virtualenv paths, or private cache directories into final commands.
