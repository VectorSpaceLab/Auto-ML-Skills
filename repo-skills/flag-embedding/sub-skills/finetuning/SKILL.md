---
name: finetuning
description: "Prepare and troubleshoot FlagEmbedding fine-tuning data, preprocessing utilities, and embedder/reranker training command construction without running expensive jobs by default."
disable-model-invocation: true
---

# FlagEmbedding Fine-tuning

Use this sub-skill when an agent needs to prepare FlagEmbedding fine-tune JSONL data, mine hard negatives, add reranker teacher scores, split long examples, or construct a safe training command for embedders or rerankers. Do not run training, download checkpoints, or launch model inference unless the user explicitly approves that cost.

## Fast workflow

1. Pick the target family in `references/training-commands.md`: encoder-only embedder, M3 embedder, decoder-only embedder, ICL embedder, encoder reranker, decoder reranker, or decoder layerwise reranker.
2. Validate data with `scripts/validate_finetune_jsonl.py` before building a command.
3. If negatives are weak or missing, plan hard-negative mining from `references/utility-scripts.md`; treat mining as model inference and ask before running it.
4. If using distillation, add or verify `pos_scores` and `neg_scores` with the teacher-score guidance in `references/utility-scripts.md`.
5. Print a command with `scripts/build_finetune_command.py`; inspect warnings, DeepSpeed config, precision flags, LoRA/flash-attention choices, and output overwrite behavior before execution.
6. Route post-training retrieval or reranking quality evaluation to `../evaluation/`; route inference API usage and scoring primitives to `../inference/`.

## Bundled references

- `references/data-formats.md` documents JSONL schemas, field rules, ICL metadata, score validation, and candidate-pool format.
- `references/training-commands.md` maps model families to `FlagEmbedding.finetune...` entry points and important flags.
- `references/utility-scripts.md` explains hard-negative mining, teacher scoring, and safe length splitting.
- `references/troubleshooting.md` covers optional dependencies, malformed data, batching, memory, DeepSpeed, and hard-negative pitfalls.

## Safe helper scripts

- `scripts/validate_finetune_jsonl.py`: validates tiny or large JSONL files/directories without importing FlagEmbedding, torch, transformers, faiss, or deepspeed.
- `scripts/build_finetune_command.py`: prints a `torchrun -m FlagEmbedding.finetune...` command and warnings; it never executes the command.
- `scripts/split_data_by_length.py`: splits JSONL by approximate length using no ML dependencies by default; tokenizer-backed mode is opt-in and warns about possible model downloads.

## Guardrails

- Training requires `FlagEmbedding[finetune]` plus accelerator-specific packages such as DeepSpeed or flash-attn only when those features are selected.
- Hard-negative mining and teacher scoring are inference jobs that may download models and use FAISS/GPU resources; provide commands for review, not automatic execution.
- Keep runtime instructions self-contained. Do not point future agents to source-repository example paths as required runtime inputs.
