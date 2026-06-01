# Data Preparation Troubleshooting

Read this when validation, hard-negative mining, teacher scoring, or length splitting fails.

## Invalid JSONL

Use the validator:

```bash
python scripts/validate_retrieval_jsonl.py --input train.jsonl --mode train
```

Fix the first invalid row before running heavier model-based scripts.

## Candidate Pool Errors

Candidate pool rows must include `text`:

```json
{"text": "candidate passage"}
```

If a candidate pool is not provided, hard-negative mining builds its corpus from all positives and existing negatives. This can be too small for useful mining.

## FAISS Import Or GPU Failure

Hard-negative mining imports `faiss`. Install CPU FAISS for small/local runs, or a GPU build compatible with the target CUDA environment for `--use_gpu_for_searching`.

If GPU FAISS fails, rerun without `--use_gpu_for_searching`.

## Too Few Negatives

If many rows still have fewer negatives than requested, increase the candidate pool size, widen `--range_for_sampling`, or sample from later ranks.

Very small corpora cannot provide many distinct negatives after removing positives and query-identical strings.

## False Negatives

Hard negatives from early ranks can include unlabeled positives. Move the sampling window later, for example from `2-200` to `60-300`, or add filtering using known relevance labels.

## Teacher Score Length Mismatch

The scoring script writes one score per `pos` and `neg` text. If validation fails after scoring, inspect rows with empty or non-list `pos`/`neg` fields.

## Tokenizer Download Or Trust Remote Code

Length splitting uses `transformers.AutoTokenizer.from_pretrained`. Use a local tokenizer path or a model cache when offline. Set trust-remote-code only if the tokenizer/model repository is trusted and the script supports the needed option.

## Output Exists

The length splitter skips existing output files unless `--overwrite` is provided. The hard-negative and scoring scripts overwrite their output file when opened for writing; choose output paths carefully.
