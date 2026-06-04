# Package Overview

Read this when you need public package facts for installing FlagEmbedding, checking imports, or choosing the right major workflow.

## Package Facts

The Python package name is `FlagEmbedding`. Public installation commands:

```bash
python -m pip install -U FlagEmbedding
python -m pip install -U "FlagEmbedding[finetune]"
```

The package metadata in the inspected repository declares version `1.4.0` and these base requirements:

```text
torch>=1.6.0
transformers>=4.44.2,<6.0.0
datasets>=2.19.0
accelerate>=0.20.1
sentence_transformers
peft
ir-datasets
sentencepiece
protobuf
```

The `finetune` extra adds:

```text
deepspeed
flash-attn
```

Evaluation examples commonly need extra packages that are not in the base metadata, especially `pytrec_eval` or `pytrec-eval-terrier`, `faiss`, `mteb`, and benchmark-specific packages such as `beir` or `air-benchmark`.

## Top-Level Exports

The inspected installed package exported these public names:

```text
AbsEmbedder
AbsReranker
BGEM3FlagModel
EmbedderModelClass
FlagAutoModel
FlagAutoReranker
FlagICLModel
FlagLLMModel
FlagLLMReranker
FlagModel
FlagPseudoMoEModel
FlagReranker
LayerWiseFlagLLMReranker
LightWeightFlagLLMReranker
RerankerModelClass
```

Use `FlagAutoModel` and `FlagAutoReranker` as the default public loading APIs. Use the concrete classes only when the caller needs a specific model family or a custom checkpoint.

## Module Entry Points

Training entry points are module commands, not console scripts:

```text
FlagEmbedding.finetune.embedder.encoder_only.base
FlagEmbedding.finetune.embedder.encoder_only.m3
FlagEmbedding.finetune.embedder.decoder_only.base
FlagEmbedding.finetune.embedder.decoder_only.icl
FlagEmbedding.finetune.reranker.encoder_only.base
FlagEmbedding.finetune.reranker.decoder_only.base
FlagEmbedding.finetune.reranker.decoder_only.layerwise
```

Evaluation entry points are also module commands:

```text
FlagEmbedding.evaluation.mteb
FlagEmbedding.evaluation.beir
FlagEmbedding.evaluation.msmarco
FlagEmbedding.evaluation.miracl
FlagEmbedding.evaluation.mldr
FlagEmbedding.evaluation.mkqa
FlagEmbedding.evaluation.air_bench
FlagEmbedding.evaluation.bright
FlagEmbedding.evaluation.custom
```

The original repository includes standalone helper scripts for hard-negative mining, reranker scoring, and length splitting. This skill bundles safe equivalents under `sub-skills/data-preparation/scripts/` so future agents do not need the source checkout.

## Public Workflow Boundaries

Use inference when the task is about vectors, dense/sparse scores, ColBERT vectors, reranker relevance scores, or choosing devices/precision for already trained models.

Use finetuning when the task is about training embedders or rerankers, adding LoRA, using DeepSpeed, formatting training JSONL, applying knowledge distillation, or resuming/checkpointing training.

Use evaluation when the task is about benchmark commands, retrieval metrics, benchmark-specific dataset names/splits, or custom retrieval dataset layout.

Use data preparation when the task is about mining negatives, assigning teacher scores, splitting long examples, or validating train/evaluation data files.

## Minimal Diagnostics

Import check:

```bash
python - <<'PY'
from FlagEmbedding import FlagAutoModel, FlagAutoReranker
print("FlagEmbedding import OK")
print(FlagAutoModel.from_finetuned)
print(FlagAutoReranker.from_finetuned)
PY
```

Installed metadata check:

```bash
python - <<'PY'
import importlib.metadata as md
dist = md.distribution("FlagEmbedding")
print(dist.metadata["Name"], dist.version)
for req in dist.requires or []:
    print(req)
PY
```

These checks avoid downloading Hugging Face models.
