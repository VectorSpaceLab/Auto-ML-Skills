# Workflow Reference

Read this when executing `flashrag-bm25-retrieval-skill`. This reference is self-contained and assumes FlashRAG is installed from a package index or public repository, not from the original extraction checkout.

## Environment

```bash
python -m pip install -U pip setuptools wheel
pip install flashrag-dev
python ../../scripts/check_flash_rag_env.py
python scripts/check_env.py
```

Use `--package-root <path>` only when inspecting a separately installed package tree. Do not point scripts at a private source checkout.

## Inputs To Resolve

- `<work_dir>`: output/work directory for configs, corpus, datasets, summaries, and logs.
- `<data_dir>` and `<dataset_name>`: user QA data or tiny generated QA data.
- `<corpus_path>` and `<index_dir>`: retrieval corpus/index paths when a retriever is used.
- `<model_path>`: embedding, generator, reranker, judger, or multimodal model path when real models are requested.
- Smoke scale: prefer generated tiny data and fake retriever/generator scripts before real model runs.

## Self-Contained Demo Data

```bash
python ../../scripts/make_demo_data.py --data-dir <work_dir>/dataset --dataset-name tiny_qa --corpus <work_dir>/corpus.jsonl
```

This creates `<work_dir>/dataset/tiny_qa/test.jsonl` and `<work_dir>/corpus.jsonl` without opening the original repo examples.

## Bundled Scripts

- `scripts/build_bm25_index.py`: run `python scripts/build_bm25_index.py --help`; use it for validation, config generation, fake smoke execution, real package API execution, inspection, or handoff as its name indicates.
- `scripts/check_env.py`: run `python scripts/check_env.py --help`; use it for validation, config generation, fake smoke execution, real package API execution, inspection, or handoff as its name indicates.
- `scripts/flashrag_import_stubs.py`: support module imported by nearby scripts; read or adapt it only when modifying helper behavior.
- `scripts/inspect_output.py`: run `python scripts/inspect_output.py --help`; use it for validation, config generation, fake smoke execution, real package API execution, inspection, or handoff as its name indicates.
- `scripts/make_bm25_config.py`: run `python scripts/make_bm25_config.py --help`; use it for validation, config generation, fake smoke execution, real package API execution, inspection, or handoff as its name indicates.
- `scripts/run_bm25_search.py`: run `python scripts/run_bm25_search.py --help`; use it for validation, config generation, fake smoke execution, real package API execution, inspection, or handoff as its name indicates.
- `scripts/validate_corpus.py`: run `python scripts/validate_corpus.py --help`; use it for validation, config generation, fake smoke execution, real package API execution, inspection, or handoff as its name indicates.

## Typical Execution Pattern

```bash
mkdir -p <work_dir>
python scripts/check_env.py
python ../../scripts/make_demo_data.py --data-dir <work_dir>/dataset --dataset-name tiny_qa --corpus <work_dir>/corpus.jsonl
python scripts/validate_corpus.py --corpus <work_dir>/corpus.jsonl
python scripts/build_bm25_index.py --corpus <work_dir>/corpus.jsonl --save-dir <work_dir>/index --overwrite
python scripts/make_bm25_config.py --output <work_dir>/bm25.yaml --corpus <work_dir>/corpus.jsonl --index-path <work_dir>/index/bm25 --save-dir <work_dir>/outputs --dataset-name tiny_qa --data-dir <work_dir>/dataset --topk 2
python scripts/run_bm25_search.py --config <work_dir>/bm25.yaml --query "What is the capital of France?" --output <work_dir>/search.json
python scripts/inspect_output.py --output <work_dir>/search.json
```

## Public BM25 Index Builder Commands

Use these commands when moving from the bundled smoke scripts to a real FlashRAG index build.

BM25s backend:

```bash
python -m flashrag.retriever.index_builder \
  --retrieval_method bm25 \
  --corpus_path <work_dir>/corpus.jsonl \
  --bm25_backend bm25s \
  --save_dir <work_dir>/indexes
```

Pyserini backend:

```bash
python -m flashrag.retriever.index_builder \
  --retrieval_method bm25 \
  --corpus_path <work_dir>/corpus.jsonl \
  --bm25_backend pyserini \
  --save_dir <work_dir>/indexes
```

Prefer BM25s for a Python-only local smoke path. Use Pyserini when the user's production setup already has Java/Pyserini available and needs Lucene-compatible indexes.

## Success Criteria

- Environment check prints `valid: true`, or missing optional packages are irrelevant to the selected fake/offline path.
- Data/corpus validators report records and no fatal schema errors.
- Config files and summaries are saved under `<work_dir>`.
- Fake/offline smoke scripts produce predictions, retrieval results, prompts, route traces, metrics, or handoff JSON.
- Real model runs are attempted only after the fake/offline path passes and required model/index/backend dependencies are available.

## Troubleshooting Notes

- If a package import is missing, install the package in the active environment and rerun `scripts/check_env.py`.
- If dense, generator, reranker, multimodal, or web UI dependencies are missing, use the fake/offline smoke path first.
- If a script emits a handoff JSON, that capability is not exposed as a stable installed-package CLI; follow the handoff note instead of opening the original extraction checkout.
- Keep generated configs, logs, summaries, and inspection outputs in `<work_dir>`.
- For Pyserini, check Java availability before starting the index build.
- For BM25s, keep the original corpus JSONL near the index because downstream inspection often needs original document text.
