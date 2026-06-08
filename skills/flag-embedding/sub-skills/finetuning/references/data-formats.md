# Fine-Tuning Data Formats

Read this before writing or validating FlagEmbedding training data.

## JSONL Row

Training data is JSONL: one JSON object per line.

Required fields for embedder and reranker training:

```json
{"query": "query text", "pos": ["positive text"], "neg": ["negative text"]}
```

Field rules:

- `query`: string.
- `pos`: non-empty list of positive passage/text strings.
- `neg`: list of negative passage/text strings. It can be empty only if a later step will sample or mine negatives, but most training commands expect negatives.

Optional fields:

- `pos_scores`: list of numbers aligned one-to-one with `pos`.
- `neg_scores`: list of numbers aligned one-to-one with `neg`.
- `prompt`: prompt or instruction text that can override query instructions or be used in reranker inputs.
- `type`: used by `bge-en-icl` style embedder training; examples include task categories such as normal, symmetric classification, or clustering variants.

## Knowledge Distillation

When using `--knowledge_distillation True`, include both score fields:

```json
{
  "query": "what is BGE?",
  "pos": ["BGE is a family of embedding models."],
  "neg": ["A cooking recipe."],
  "pos_scores": [0.98],
  "neg_scores": [0.05]
}
```

Validation should confirm:

- `len(pos_scores) == len(pos)`
- `len(neg_scores) == len(neg)`
- Scores are numeric.

## Reranker Prompt Rows

Reranker training uses the same `query`, `pos`, and `neg` fields. For prompt-based decoder rerankers, `prompt` can control the final input shape where the effective input is query, separator, passage, separator, prompt.

Example:

```json
{
  "query": "what is panda?",
  "pos": ["The giant panda is a bear species endemic to China."],
  "neg": ["Pandas is a Python data analysis library."],
  "prompt": "Given a query A and a passage B, determine whether the passage answers the query."
}
```

## Candidate Pool For Hard Negatives

When using an external candidate pool for hard-negative mining, use JSONL rows containing a `text` field:

```json
{"text": "candidate passage one"}
{"text": "candidate passage two"}
```

If no candidate pool is provided, hard-negative mining can retrieve from negatives in the input file.

## Local Validation

Use the bundled validator:

```bash
python scripts/validate_finetune_jsonl.py train.jsonl --task embedder
python scripts/validate_finetune_jsonl.py train.jsonl --task reranker --require-scores
python scripts/validate_finetune_jsonl.py candidates.jsonl --candidate-pool
```

The validator is intentionally conservative and does not download models or import FlagEmbedding.
