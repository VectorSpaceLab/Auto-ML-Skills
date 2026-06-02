---
name: flash-rag
description: "Use when a user wants an agent to run FlashRAG corpus processing, retrieval, reranking, generation, RAG pipelines, multimodal RAG, refiner, judger, evaluation, and WebUI workflows from natural language using a public package install and bundled helper scripts."
disable-model-invocation: true
---

# FlashRAG

This is the router for the FlashRAG repo skill. Use it to choose the focused sub-skill, then read only that sub-skill plus the linked bundled references/scripts. Do not reopen the original source checkout or rely on the inspection environment used to create this skill.

## Public Install

Prefer a clean Python environment that satisfies Python 3.9 or newer.

```bash
python -m pip install -U pip setuptools wheel
pip install flashrag-dev
python -c "import flashrag; print(flashrag.__name__)"
```

For unreleased features, install from the public repository instead of a private local checkout:

```bash
git clone https://github.com/RUC-NLPIR/FlashRAG.git && pip install -e FlashRAG
```

Run the bundled environment check after installation:

```bash
python scripts/check_flash_rag_env.py
```

See [references/installation.md](references/installation.md) for optional extras and backend notes. See [references/troubleshooting.md](references/troubleshooting.md) for cross-cutting failures.

## Route To Sub-Skills

- **SelfRAG, FLARE, SelfAsk, IRCOT, and RQ-RAG active retrieval workflows.**: [sub-skills/flashrag-active-rag-pipeline-skill/SKILL.md](sub-skills/flashrag-active-rag-pipeline-skill/SKILL.md)
- **BM25s lexical index building and search without dense models.**: [sub-skills/flashrag-bm25-retrieval-skill/SKILL.md](sub-skills/flashrag-bm25-retrieval-skill/SKILL.md)
- **Conditional and adaptive pipeline routing by judger decisions.**: [sub-skills/flashrag-conditional-pipeline-skill/SKILL.md](sub-skills/flashrag-conditional-pipeline-skill/SKILL.md)
- **Corpus chunking and long-document passage preparation.**: [sub-skills/flashrag-corpus-chunking-skill/SKILL.md](sub-skills/flashrag-corpus-chunking-skill/SKILL.md)
- **Offline metric evaluation on saved predictions and dataset splits.**: [sub-skills/flashrag-dataset-eval-skill/SKILL.md](sub-skills/flashrag-dataset-eval-skill/SKILL.md)
- **Dense retrieval, embedding index command generation, and search inspection.**: [sub-skills/flashrag-dense-retrieval-skill/SKILL.md](sub-skills/flashrag-dense-retrieval-skill/SKILL.md)
- **HF/vLLM/FastChat/OpenAI-compatible generator config and fake generation smoke.**: [sub-skills/flashrag-generator-skill/SKILL.md](sub-skills/flashrag-generator-skill/SKILL.md)
- **Iterative multi-round retrieval-generation pipeline smoke.**: [sub-skills/flashrag-iterative-pipeline-skill/SKILL.md](sub-skills/flashrag-iterative-pipeline-skill/SKILL.md)
- **SKR and adaptive judger data validation and fake route checks.**: [sub-skills/flashrag-judger-skill/SKILL.md](sub-skills/flashrag-judger-skill/SKILL.md)
- **KG-Trace triple extraction and evidence-chain context smoke workflows.**: [sub-skills/flashrag-kg-trace-refiner-skill/SKILL.md](sub-skills/flashrag-kg-trace-refiner-skill/SKILL.md)
- **Named methods from FlashRAG examples, including naive, zero-shot, SKR, TRACE, reasoning, and refiner variants.**: [sub-skills/flashrag-methods-runner-skill/SKILL.md](sub-skills/flashrag-methods-runner-skill/SKILL.md)
- **BM25+dense/CLIP multi-retriever configuration and merge settings.**: [sub-skills/flashrag-multi-retriever-skill/SKILL.md](sub-skills/flashrag-multi-retriever-skill/SKILL.md)
- **CLIP/openai-clip/chinese-clip multimodal index preflight and smoke tests.**: [sub-skills/flashrag-multimodal-index-skill/SKILL.md](sub-skills/flashrag-multimodal-index-skill/SKILL.md)
- **MMSequentialPipeline and multimodal no-retrieval/RAG smoke workflows.**: [sub-skills/flashrag-multimodal-pipeline-skill/SKILL.md](sub-skills/flashrag-multimodal-pipeline-skill/SKILL.md)
- **Multi-turn generator prompt rendering and conversation smoke tests.**: [sub-skills/flashrag-multiturn-generator-skill/SKILL.md](sub-skills/flashrag-multiturn-generator-skill/SKILL.md)
- **RAG prompt rendering and LLMLingua/SelectiveContext/RECOMP-style refiner checks.**: [sub-skills/flashrag-prompt-refiner-skill/SKILL.md](sub-skills/flashrag-prompt-refiner-skill/SKILL.md)
- **Reasoning-search pipelines such as SimpleDeepSearcher, SearchR1, AutoRefine, O2Searcher, ReaRAG, and CoRAG.**: [sub-skills/flashrag-reasoning-pipeline-skill/SKILL.md](sub-skills/flashrag-reasoning-pipeline-skill/SKILL.md)
- **REPLUG document-score weighted generation workflows.**: [sub-skills/flashrag-replug-pipeline-skill/SKILL.md](sub-skills/flashrag-replug-pipeline-skill/SKILL.md)
- **Reranker configuration, offline rerank checks, and reranked-output inspection.**: [sub-skills/flashrag-reranker-skill/SKILL.md](sub-skills/flashrag-reranker-skill/SKILL.md)
- **Sequential retrieve-generate-evaluate RAG pipeline smoke and real-run transition.**: [sub-skills/flashrag-sequential-pipeline-skill/SKILL.md](sub-skills/flashrag-sequential-pipeline-skill/SKILL.md)
- **SuRe candidate, summary, validation, ranking, and final-answer pipeline smoke.**: [sub-skills/flashrag-sure-pipeline-skill/SKILL.md](sub-skills/flashrag-sure-pipeline-skill/SKILL.md)
- **FlashRAG WebUI launch, health check, and shutdown.**: [sub-skills/flashrag-webui-skill/SKILL.md](sub-skills/flashrag-webui-skill/SKILL.md)

## Execution Contract

1. Resolve the user's model, data/corpus, output directory, backend, and smoke/full-run target.
2. Read the nearest sub-skill `SKILL.md`, then one or two linked references only as needed.
3. Use bundled scripts for validation, config generation, smoke tests, and inspection where available.
4. Run package CLIs or public package APIs from the installed environment; do not require the original repo checkout.
5. Save generated configs, command logs, summaries, and inspection results beside the user's output artifacts.
6. Report exact artifact paths, validation status, metrics/losses, and unresolved risks.

## Shared Resources

- [references/coverage-matrix.md](references/coverage-matrix.md): maps public capability families to sub-skills.
- [references/installation.md](references/installation.md): public install, extras, import checks, and backend prerequisites.
- [references/troubleshooting.md](references/troubleshooting.md): repo-wide import, dependency, GPU, data, and output-location issues.
- [scripts/check_flash_rag_env.py](scripts/check_flash_rag_env.py): safe import and optional-dependency check for a fresh environment.
- [scripts/inspect_package.py](scripts/inspect_package.py): read-only package/API inspection helper.

The `evals/` directory is a development artifact for self-refine checks and is not linked as runtime documentation.
