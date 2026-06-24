# Repo-Wide Troubleshooting

Read this when a LLaMA-Factory workflow fails before reaching a sub-skill-specific error.

## Import Or Install Fails

- Confirm the active Python environment can import `llamafactory`.
- Reinstall from a public package or public source checkout; do not rely on private path state.
- Run `python scripts/check_llama_factory_env.py` and fix missing required packages before training or serving.

## GPU Or Backend Fails

- Run a CPU/offline smoke path first when the sub-skill provides one.
- Check CUDA availability, visible devices, and available memory before full training or real generation.
- Keep quantization, vLLM, FAISS, multimodal, and distributed extras scoped to workflows that actually need them.

## Data Or Config Fails

- Validate user data with the bundled validator in the relevant sub-skill before launching a real job.
- Save generated configs and logs in the output directory so failures are reproducible.
- If a config mixes incompatible trainer generations, stages, or backend options, regenerate it from the relevant sub-skill script/reference.

## Output Is Missing

- Inspect the exact output directory printed by the runner; some workflows create timestamped subdirectories.
- Confirm the run did not silently write under the current working directory.
- Use the sub-skill inspector script when available before declaring success.
