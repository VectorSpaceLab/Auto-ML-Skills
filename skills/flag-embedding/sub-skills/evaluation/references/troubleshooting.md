# Evaluation Troubleshooting

Read this when FlagEmbedding evaluation commands fail or metrics are missing.

## Missing Dependencies

Install benchmark dependencies explicitly:

```bash
python -m pip install pytrec_eval
python -m pip install pytrec-eval-terrier
python -m pip install beir
python -m pip install mteb==1.15.0
```

Use either `pytrec_eval` or `pytrec-eval-terrier` depending on platform compatibility. Install a FAISS package matching the target environment.

## Dataset Files Missing

For custom datasets, run:

```bash
python sub-skills/evaluation/scripts/check_eval_dataset.py --dataset-dir ./eval_data --splits test
```

For benchmark datasets, verify `--dataset_names` and `--splits` are valid for that benchmark. For example, MIRACL uses language codes as dataset names; MLDR has language names and `train/dev/test`; MSMARCO has `passage` and `document`.

## AIR-Bench Metrics Not Printed

The AIR-Bench module generates search results and then points to the official AIR-Bench metric submission/computation flow. This is expected behavior.

## Memory Or Runtime Too High

Reduce:

```text
--embedder_batch_size
--reranker_batch_size
--embedder_query_max_length
--embedder_passage_max_length
--reranker_max_length
--search_top_k
--rerank_top_k
```

For a quick run, evaluate fewer `--dataset_names`, fewer `--splits`, and smaller `--k_values`.

## Reranker Not Used

Pass `--reranker_name_or_path` to enable reranking. Without it, evaluation runs embedder retrieval only.

If using a custom reranker checkpoint, pass `--reranker_model_class`.

## Existing Outputs Are Reused

Set `--overwrite True` only when replacing existing results is intended. Otherwise stale search results can make it look like a new configuration had no effect.

## Instruction Formatting

Evaluation parsers replace literal `\n` in instruction formats. In shell commands, quote formats containing braces and newlines:

```bash
--query_instruction_format_for_retrieval "Instruct: {}\nQuery: {}"
```

For custom models, set `--embedder_model_class`, `--pooling_method`, and instruction formats explicitly.
