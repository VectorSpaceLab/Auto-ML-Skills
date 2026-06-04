# Troubleshooting

Read this when FlagEmbedding import, model loading, inference, fine-tuning, evaluation, or data preparation fails.

## Import Or Package Metadata Fails

Check the install:

```bash
python - <<'PY'
import importlib.metadata as md
import FlagEmbedding
print("module OK", FlagEmbedding.__name__)
print(md.distribution("FlagEmbedding").version)
PY
```

If `FlagEmbedding[finetune]` fails because `flash-attn` cannot build, first install a Torch/CUDA combination compatible with the target machine, then retry the extra. For inference-only workflows, install `FlagEmbedding` without the fine-tuning extra.

## Auto Mapping Rejects A Model

Error pattern: model name not found in `AUTO_EMBEDDER_MAPPING` or `AUTO_RERANKER_MAPPING`.

Use explicit class selection:

```python
from FlagEmbedding import FlagAutoModel
model = FlagAutoModel.from_finetuned(
    "path-or-hf-model",
    model_class="encoder-only-base",
    pooling_method="cls",
    query_instruction_for_retrieval="Represent this sentence for searching relevant passages: ",
)
```

For rerankers:

```python
from FlagEmbedding import FlagAutoReranker
reranker = FlagAutoReranker.from_finetuned(
    "path-or-hf-reranker",
    model_class="encoder-only-base",
)
```

Choose the class from `references/model-overview.md`.

## Trust Remote Code

Some mapped models require `trust_remote_code=True`, including several GTE and code-oriented models. Do not set it silently for untrusted model repositories. Explain the security implication and ask before loading unfamiliar remote code.

## Precision And Device Issues

`use_fp16=True` speeds inference and is common in examples, but CPU or unsupported GPU paths may fail. For CPU diagnosis, set `use_fp16=False` and `devices="cpu"` where supported.

For BF16-capable GPUs, some decoder-only or pseudo-MoE workflows may prefer `use_bf16=True`. Do not set both FP16 and BF16 casually; choose based on hardware and model family.

Large LLM embedders and rerankers can exceed GPU memory quickly. Reduce `batch_size`, `query_max_length`, `passage_max_length`, or `max_length`, and prefer encoder-only models for smoke tests.

## Evaluation Dependencies

Evaluation examples mention:

```bash
python -m pip install pytrec_eval
python -m pip install pytrec-eval-terrier
python -m pip install beir
python -m pip install mteb==1.15.0
```

The original examples also used a GPU FAISS wheel URL. Prefer installing a FAISS build compatible with the target Python/CUDA environment; use CPU FAISS for data validation and small local tests.

## Training Data Errors

Training JSONL rows require at least:

```json
{"query": "text", "pos": ["positive"], "neg": ["negative"]}
```

Distillation rows add `pos_scores` and `neg_scores` with lengths matching `pos` and `neg`.

Embedder ICL rows may include `type`. Prompt-based reranker rows may include `prompt`.

Run `sub-skills/data-preparation/scripts/validate_retrieval_jsonl.py` before training.

## DeepSpeed Config Paths

The source examples pass `--deepspeed` to JSON configs. This skill bundles config generators instead of relying on source repo paths. Use:

```bash
python sub-skills/finetuning/scripts/write_deepspeed_config.py --stage 0 --output ds_stage0.json
python sub-skills/finetuning/scripts/write_deepspeed_config.py --stage 1 --output ds_stage1.json
```

Then pass `--deepspeed ./ds_stage0.json` or `--deepspeed ./ds_stage1.json`.

## Benchmark Data Layout

Custom evaluation requires a dataset directory with:

```text
corpus.jsonl
<split>_queries.jsonl
<split>_qrels.jsonl
```

or multiple child directories each containing that layout. Run `sub-skills/evaluation/scripts/check_eval_dataset.py` to catch missing files before starting a benchmark.
