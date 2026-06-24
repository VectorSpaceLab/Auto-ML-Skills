# Installation Reference

Read this when setting up FlashRAG in a new public environment.

## Public Install

```bash
python -m pip install -U pip setuptools wheel
pip install flashrag-dev
python -c "import flashrag; print(flashrag.__name__)"
```

If the package manager release lags the public repository, use an editable public source install:

```bash
git clone https://github.com/RUC-NLPIR/FlashRAG.git && pip install -e FlashRAG
```

Do not use private checkout paths or the inspection environment that produced this skill. The future agent should create its own environment and install from a package index or public repository.

## Minimal Verification

```bash
python scripts/check_flash_rag_env.py
python scripts/inspect_package.py flashrag
```

## Optional Backends

Install only the extras required by the selected sub-skill. Retrieval, quantization, distributed training, serving, and multimodal workflows often add extra packages, model downloads, GPU memory, or external services. Prefer a one-sample smoke test before a full run.
