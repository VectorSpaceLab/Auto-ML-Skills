# FlagEmbedding Usability Test Cases

These cases exercise the generated `flag-embedding` skill across inference, finetuning, and evaluation workflows.

| Case directory | Skill area | User role | Scenario | Capability | Difficulty |
| --- | --- | --- | --- | --- | --- |
| `inference-embedder-smoke-test` | inference | New user | Verify install and run a minimal BGE embedder check | Install verification, embedder API, smoke script | Basic |
| `inference-custom-checkpoint-routing` | inference | Integrator | Load a local custom checkpoint that auto mapping cannot infer | Explicit `model_class`, pooling, device choices | Intermediate |
| `inference-reranker-ranking` | inference | RAG engineer | Rerank candidate passages and normalize scores | Reranker API and ranking logic | Intermediate |
| `finetuning-validate-distillation-data` | finetuning | Data engineer | Validate JSONL rows before distillation training | Data schema and validator | Troubleshooting |
| `finetuning-plan-decoder-lora-training` | finetuning | ML engineer | Plan decoder-only LoRA fine-tuning command | Module choice, LoRA flags, training command | Advanced |
| `finetuning-mine-negatives-and-score` | finetuning | Retrieval engineer | Mine hard negatives and add teacher scores | Data-prep scripts, side-effect warnings | Advanced |
| `evaluation-custom-dataset-layout` | evaluation | Applied researcher | Prepare and validate local custom retrieval dataset | Custom corpus/query/qrels layout | Intermediate |
| `evaluation-beir-with-reranker` | evaluation | Benchmark user | Run BEIR with embedder and reranker | CLI flags, benchmark dependencies, metrics | Intermediate |
| `evaluation-mteb-task-selection` | evaluation | Benchmark user | Run selected MTEB tasks | MTEB flags and output path | Basic |

## Coverage Note

The cases cover all generated sub-skills and major capabilities in the coverage matrix: install/import checks, embedder inference, reranker inference, custom model routing, training-data validation, embedder/reranker fine-tuning planning, hard-negative/teacher-score preparation, custom evaluation layout, and benchmark CLI usage.
