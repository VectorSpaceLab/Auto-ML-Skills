# Benchmark Reproduction Setup

Read this when aligning a FlashRAG run with the public benchmark-style setup.

## Base Assets

The documented reproduction flow expects these asset categories:

- Generator model, commonly Llama3-8B-Instruct for baseline-style runs.
- Retriever model, commonly E5-base-v2 for dense retrieval.
- Dataset directory containing FlashRAG-format splits.
- Retrieval corpus JSONL, often Wikipedia-derived.
- Dense or sparse index built from that corpus and retriever choice.

The generated skill must not depend on original `examples/methods/my_config.yaml`. Instead, generate an equivalent config with bundled scripts and user-provided public asset paths.

## Unified Settings

Baseline-style settings commonly use:

- Retrieval: top 5 documents per query.
- Dense retriever: E5-style embedding with Faiss Flat index.
- Generator: vLLM or HF backend, deterministic generation, max input around 2048, max output around 32 for short-answer QA.
- Dataset sampling: first 1000 samples for reported benchmark-style comparisons unless the user requests a full run.
- Prompt: document-grounded short-answer format with document titles and contents.

Treat benchmark numbers as sensitive to model versions, prompts, retrieval corpus, split choice, and sampling. Do not claim score parity unless those settings match.

## Reproduction Flow

1. Validate dataset and corpus JSONL formats.
2. Build or locate the required index.
3. Generate a config skeleton with user asset paths.
4. Select a method and check method-specific assets.
5. Run a tiny split/sample smoke test.
6. Scale to the requested split/sample count.
7. Save config, command, predictions, metric output, and package versions together.

## Result Alignment Checklist

- Same dataset split: test vs dev differs by dataset.
- Same sample count and random-sampling setting.
- Same retriever model and pooling/instruction behavior.
- Same index type and corpus version.
- Same generator model, backend, prompt template, max lengths, and decoding settings.
- Same extra model checkpoints for refiner/judger/reasoning methods.
