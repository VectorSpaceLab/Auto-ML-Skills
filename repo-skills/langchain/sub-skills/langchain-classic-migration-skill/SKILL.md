---
name: langchain-classic-migration-skill
description: "Use when a user wants LangChain classic migration, legacy chains, LLMChain replacement, classic agents/memory/loaders imports, deprecation triage, or LCEL modernization."
disable-model-invocation: true
---

# LangChain Classic Migration

Use `langchain-classic-migration-skill` when code imports `langchain_classic` or legacy paths such as `langchain.chains`, `langchain.memory`, `langchain.llms`, or `langchain.document_loaders`. Quick answer: identify the legacy surface, replace chains with LCEL, replace provider imports with integration packages, and validate with `scripts/scan_classic_imports.py`.

## Short Workflow

1. Run [scripts/scan_classic_imports.py](scripts/scan_classic_imports.py) on user files.
2. Classify findings: chains, memory, agents, document loaders, retrievers, vectorstores, callbacks, model providers.
3. For new code, prefer `langchain_core`, top-level `langchain` 1.x agent APIs, and provider packages.
4. Replace `LLMChain`-style flows with `prompt | model | parser` LCEL.
5. Read [references/migration-map.md](references/migration-map.md) before editing broad legacy apps.

## Bundled Scripts

- [scripts/scan_classic_imports.py](scripts/scan_classic_imports.py): static scan for common legacy imports and migration hints.

## References

- [references/migration-map.md](references/migration-map.md): legacy-to-modern import/workflow map.
- [references/workflows.md](references/workflows.md): chain, memory, loader, agent, and model modernization steps.
- [references/troubleshooting.md](references/troubleshooting.md): deprecation, package, and behavior-change issues.

## Boundaries

Use focused sub-skills after migration classification: LCEL for chain rewrites, memory/history for conversation state, models for providers, loaders/splitters/vectorstores for RAG ingestion.
