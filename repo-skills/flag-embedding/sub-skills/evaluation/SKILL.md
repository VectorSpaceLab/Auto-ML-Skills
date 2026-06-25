---
name: evaluation
description: "Plan safe FlagEmbedding benchmark and custom retrieval evaluation workflows, generate commands, and interpret evaluation artifacts without triggering downloads or long runs by default."
disable-model-invocation: true
---

# FlagEmbedding Evaluation

Use this sub-skill when the task is to plan, configure, or review FlagEmbedding evaluations for BEIR, MTEB, MIRACL, MLDR, MKQA, MSMARCO, AIR-Bench, BRIGHT, or custom retrieval datasets.

Do not run benchmark commands unless the user explicitly approves network access, dataset/model downloads, benchmark runtime, and hardware usage. By default, produce a plan and a command string.

## Route First

- For embedding and reranking Python API usage, model loading, encode calls, or score computation, route to `../inference/`.
- For fine-tuning data preparation or training/eval during training, route to `../finetuning/`.
- For choosing BGE model families or RAG-level model tradeoffs, route briefly to `../model-catalog-and-rag/`, then return here for benchmark command planning.

## Evaluation Workflow

1. Identify the benchmark family and map it to the Python module in `references/benchmark-workflows.md`.
2. Decide whether the run is safe to execute now: local tiny/custom data may be safe; public benchmark downloads and full retrieval/reranking runs are usually not.
3. Confirm dataset/cache/output locations using portable paths supplied by the user; never assume hidden local caches.
4. Choose dataset selectors: `--dataset_names` for BEIR/MIRACL/MLDR/MKQA/MSMARCO/BRIGHT, `--languages`, `--tasks`, or `--task_types` for MTEB, and AIR-Bench-specific selectors for AIR-Bench.
5. Choose model args: `--embedder_name_or_path` is required; optional reranking uses `--reranker_name_or_path`; CPU runs should use small batches and avoid `cuda:*` devices.
6. Generate the command with `scripts/build_eval_command.py` and present it as a plan unless execution is explicitly authorized.
7. After execution, interpret search result directories and metric summaries using `references/api-reference.md`.

## Safe Command Builder

Use the bundled generator to construct shell-safe commands without executing them:

```bash
python sub-skills/evaluation/scripts/build_eval_command.py \
  --benchmark beir \
  --embedder BAAI/bge-m3 \
  --dataset-dir ./beir/data \
  --dataset-names fiqa arguana \
  --splits test \
  --output-dir ./beir/search_results \
  --eval-output-path ./beir/eval_results.md \
  --cache-path ./cache/data \
  --model-cache-dir ./cache/model
```

For custom datasets, provide a local dataset directory with `corpus.jsonl`, `<split>_queries.jsonl`, and `<split>_qrels.jsonl`, then use `--benchmark custom`.

## Execute vs Skip Criteria

Execute only when all are true:

- The user explicitly asks to run the benchmark or confirms execution after seeing the plan.
- Required datasets and models are already local, or the user approves downloads and credentials.
- Runtime is appropriate for the current hardware; full benchmark, reranking, and large corpora can be expensive.
- Output paths are writable and `--overwrite` is intentional.

Skip and return a command plan when any are true:

- Dataset/cache paths are missing or would trigger remote downloads without approval.
- HF credentials, private dataset access, or model access are uncertain.
- The request is broad, such as “evaluate on BEIR” without dataset subset, cache, output, and runtime budget.
- The environment is CPU-only and the run uses large corpora, long passages, reranking, or high `search_top_k`.

## References

- `references/benchmark-workflows.md`: benchmark routing, selectors, custom dataset layout, and command templates.
- `references/api-reference.md`: argument groups, output artifacts, and interpretation notes.
- `references/troubleshooting.md`: common failures and safe recovery steps.
