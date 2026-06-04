# Workflow Reference

Read this when executing `flashrag-judger-skill`. This reference is self-contained and assumes FlashRAG is installed from a package index or public repository, not from the original extraction checkout.

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

- `scripts/check_env.py`: run `python scripts/check_env.py --help`; use it for validation, config generation, fake smoke execution, real package API execution, inspection, or handoff as its name indicates.
- `scripts/inspect_output.py`: run `python scripts/inspect_output.py --help`; use it for validation, config generation, fake smoke execution, real package API execution, inspection, or handoff as its name indicates.
- `scripts/make_judger_config.py`: run `python scripts/make_judger_config.py --help`; use it for validation, config generation, fake smoke execution, real package API execution, inspection, or handoff as its name indicates.
- `scripts/make_skr_training.py`: run `python scripts/make_skr_training.py --help`; use it for validation, config generation, fake smoke execution, real package API execution, inspection, or handoff as its name indicates.
- `scripts/run_fake_judger.py`: run `python scripts/run_fake_judger.py --help`; use it for validation, config generation, fake smoke execution, real package API execution, inspection, or handoff as its name indicates.
- `scripts/validate_judger_training.py`: run `python scripts/validate_judger_training.py --help`; use it for validation, config generation, fake smoke execution, real package API execution, inspection, or handoff as its name indicates.

## Typical Execution Pattern

```bash
mkdir -p <work_dir>
python scripts/check_env.py
python ../../scripts/make_demo_data.py --data-dir <work_dir>/dataset --dataset-name tiny_qa --corpus <work_dir>/corpus.jsonl
python scripts/validate_judger_training.py --data <work_dir>/dataset/tiny_qa/test.jsonl
python scripts/make_judger_config.py --output <work_dir>/config.yaml --data-dir <work_dir>/dataset --dataset-name tiny_qa --save-dir <work_dir>/outputs
python scripts/run_fake_judger.py --config <work_dir>/config.yaml --summary <work_dir>/summary.json
python scripts/inspect_output.py --summary <work_dir>/summary.json
```

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
