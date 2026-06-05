# LoRA Reference

## Key Flags

- `--enable-lora`: enables LoRA support.
- `--lora-modules`: maps adapter served name to adapter path or public adapter ID.
- `--max-loras`: maximum number of adapters active in a batch.
- `--max-lora-rank`: maximum supported adapter rank.
- `--enable-lora-bias`: use only when adapter requires bias support.

## Resolver Plugins

vLLM includes resolver plugin patterns for loading adapters dynamically from storage such as local filesystem or Hugging Face Hub. Filesystem resolver usage requires a configured storage root and a directory layout that contains adapter config and weights. Runtime loading must be explicitly enabled with `VLLM_ALLOW_RUNTIME_LORA_UPDATING`.

## Common Errors

- "LoRA adapter not found": wrong adapter name/path, resolver root, or runtime route.
- "Rank exceeds maximum": increase `--max-lora-rank` or use a lower-rank adapter.
- Base mismatch: outputs degrade or loading fails; confirm adapter was trained for the exact base family.
- Request hits base model: client used base model name instead of adapter served name.
