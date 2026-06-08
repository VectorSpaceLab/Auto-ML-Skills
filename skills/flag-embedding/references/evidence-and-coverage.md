# Evidence And Coverage

This file records what evidence shaped the generated skill and where each capability is covered. It is useful for audits and future skill maintenance.

## Evidence Map

| Evidence source | Why it matters | Used for |
| --- | --- | --- |
| Package metadata | Distribution name, version, runtime dependencies, finetune extra | Root install instructions and environment verification. |
| Public README | High-level project purpose, install variants, quick-start API, model list | Root router, shared model overview. |
| Inference source modules | Public exports, auto loaders, model-class mappings, signatures | Inference API reference and safe smoke script. |
| Inference examples | Embedder/reranker workflows, instruction usage, BGE-M3 modes | Inference workflows reference. |
| Tests | Basic embedder/reranker behavior and result expectations | Inference smoke-test assumptions. |
| Finetune argument dataclasses | Required train data, important training flags, defaults | Finetuning references and validation script. |
| Finetune examples and scripts docs | Embedder/reranker torchrun recipes, hard negatives, teacher scores, split by length | Finetuning workflow reference. |
| Evaluation argument dataclasses | Common CLI flags and benchmark-specific arguments | Evaluation CLI reference. |
| Evaluation examples | MTEB, BEIR, MSMARCO, MIRACL, MLDR, MKQA, AIR-Bench, BRIGHT, custom dataset commands | Evaluation workflow reference and usability cases. |
| Installed-package inspection | Verified importability, public API signatures, enum values | API tables and environment check guidance. |

No existing repo-local generated skill was present, so this generated skill uses a fresh `flag-embedding` id and creates separate review cases under `skills/tests/flag-embedding`.

## Coverage Matrix

| Capability | Evidence source | Output location | Depth check |
| --- | --- | --- | --- |
| Package install and import verification | Metadata, README, installed inspection | Root `SKILL.md`, `scripts/check_flagembedding_env.py` | Includes public install variants and no-download verification. |
| Model family selection | Model mappings, README, live enum inspection | `references/model-overview.md` | Lists embedder/reranker model-class values and decision points. |
| Embedder inference | Source, examples, tests, live signatures | Inference sub-skill, `api-reference.md`, `workflows.md`, `inference_smoke_test.py` | Covers auto/custom loading, instructions, devices, batch behavior, and optional real-model smoke test. |
| BGE-M3 dense/sparse/ColBERT modes | Source signatures, examples | Inference `api-reference.md`, `workflows.md` | Covers return keys and score modes. |
| Reranker inference | Source, examples, tests, live signatures | Inference sub-skill and references | Covers raw and normalized scores, layerwise/lightweight parameters, devices. |
| Train-data validation | Finetune README, dataclasses | Finetuning `data-formats.md`, `validate_finetune_jsonl.py` | Covers required JSONL fields and score alignment. |
| Embedder fine-tuning | Finetune examples and arguments | Finetuning `training-workflows.md` | Covers standard, M3, decoder-only, ICL module choices and key flags. |
| Reranker fine-tuning | Finetune examples and arguments | Finetuning `training-workflows.md` | Covers encoder-only, decoder-only, layerwise commands and flags. |
| Hard negatives and teacher scores | Scripts docs | Finetuning `training-workflows.md` | Covers command shapes and when to run them. |
| Retrieval evaluation | Evaluation README, CLI modules, argument classes | Evaluation sub-skill, `cli-reference.md`, `data-formats.md`, validator script | Covers benchmarks, common flags, extra dependencies, and custom dataset layout. |
| Troubleshooting | Source errors, docs, dependency/runtime checks | Shared `troubleshooting.md` plus sub-skill references | Covers model mapping errors, dtype/device issues, data validation, benchmark dependencies. |

## Intentional Limits

- Research directories and multimodal projects are not expanded into separate sub-skills because the installed package's main public surface is embedding, reranking, fine-tuning, and evaluation.
- Scripts that launch training, download models, mine hard negatives, or compute teacher scores are documented but not bundled as runnable defaults because they have large side effects.
- Safe bundled scripts avoid model downloads unless a user explicitly passes model paths or model ids.
