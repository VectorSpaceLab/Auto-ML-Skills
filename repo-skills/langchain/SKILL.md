---
name: langchain
description: "Use when a user wants an agent to build, debug, inspect, or smoke-test LangChain applications, including chat models, prompts, LCEL runnables, retrieval, agents, tools, memory, structured output, streaming, callbacks, LangSmith, installation, and integrations."
disable-model-invocation: true
---

# LangChain

This is the router for the LangChain repo skill. Use it to choose the focused sub-skill, then read only that sub-skill plus the linked bundled references/scripts. Do not rely on the source checkout used to create this skill.

## Public Install

Prefer installing only the packages needed for the user's workflow:

```bash
python -m pip install -U pip setuptools wheel
pip install langchain langchain-core
```

Common optional packages:

```bash
pip install langchain-community langchain-text-splitters langsmith
pip install langchain-openai
```

Provider integrations are split into provider packages, such as `langchain-openai`, `langchain-anthropic`, `langchain-ollama`, `langchain-chroma`, and `langchain-qdrant`. Install the matching integration instead of assuming it is bundled in `langchain`.

Run the bundled environment check after installation:

```bash
python scripts/check_langchain_env.py
```

See [references/installation.md](references/installation.md) for package boundaries and [references/troubleshooting.md](references/troubleshooting.md) for common failures.

## Route To Sub-Skills

- **Model/provider setup, fake models, embeddings, model profiles, and generic model configuration.**: [sub-skills/langchain-models-skill/SKILL.md](sub-skills/langchain-models-skill/SKILL.md)
- **Local Hugging Face/Transformers weights, Qwen-style local model smoke tests, and `HuggingFacePipeline`.**: [sub-skills/langchain-local-hf-models-skill/SKILL.md](sub-skills/langchain-local-hf-models-skill/SKILL.md)
- **Prompt templates, messages, placeholders, few-shot prompts, output parsers, and message formatting.**: [sub-skills/langchain-prompts-parsers-skill/SKILL.md](sub-skills/langchain-prompts-parsers-skill/SKILL.md)
- **LCEL runnable chains, routing, assignment, retries, fallbacks, config, and graph inspection.**: [sub-skills/langchain-lcel-runnables-skill/SKILL.md](sub-skills/langchain-lcel-runnables-skill/SKILL.md)
- **Document loaders and loader package requirements.**: [sub-skills/langchain-document-loaders-skill/SKILL.md](sub-skills/langchain-document-loaders-skill/SKILL.md)
- **Text splitters, recursive/language-aware chunking, chunk metadata, and splitter troubleshooting.**: [sub-skills/langchain-text-splitters-skill/SKILL.md](sub-skills/langchain-text-splitters-skill/SKILL.md)
- **Vector stores, indexing helpers, retriever search kwargs, ids, and vector DB package boundaries.**: [sub-skills/langchain-vectorstores-indexing-skill/SKILL.md](sub-skills/langchain-vectorstores-indexing-skill/SKILL.md)
- **Basic retrieval/RAG composition and no-key in-memory retrieval smoke tests.**: [sub-skills/langchain-retrieval-rag-skill/SKILL.md](sub-skills/langchain-retrieval-rag-skill/SKILL.md)
- **Advanced retrievers such as parent-document, multi-vector, multi-query, self-query, ensemble, and compression.**: [sub-skills/langchain-advanced-retrievers-skill/SKILL.md](sub-skills/langchain-advanced-retrievers-skill/SKILL.md)
- **Agents, tools, tool calling, and safe fake-tool smoke tests.**: [sub-skills/langchain-agents-tools-skill/SKILL.md](sub-skills/langchain-agents-tools-skill/SKILL.md)
- **Agent middleware, model/context/tool hooks, shell middleware boundaries, and middleware inspection.**: [sub-skills/langchain-agent-middleware-skill/SKILL.md](sub-skills/langchain-agent-middleware-skill/SKILL.md)
- **Memory, chat history, conversation state, and `RunnableWithMessageHistory`.**: [sub-skills/langchain-memory-history-skill/SKILL.md](sub-skills/langchain-memory-history-skill/SKILL.md)
- **Generic stores, byte stores, docstores, and parent-document storage adapters.**: [sub-skills/langchain-stores-docstores-skill/SKILL.md](sub-skills/langchain-stores-docstores-skill/SKILL.md)
- **Structured output with Pydantic, JSON schema, tool/function parsers, and provider capability checks.**: [sub-skills/langchain-structured-output-skill/SKILL.md](sub-skills/langchain-structured-output-skill/SKILL.md)
- **Streaming, batching, async invocation, event streams, and concurrency controls.**: [sub-skills/langchain-streaming-async-skill/SKILL.md](sub-skills/langchain-streaming-async-skill/SKILL.md)
- **Callbacks, tracing, runtime config, metadata, tags, and integration pitfalls.**: [sub-skills/langchain-observability-config-skill/SKILL.md](sub-skills/langchain-observability-config-skill/SKILL.md)
- **LLM cache, rate limiting, usage metadata callbacks, and token accounting.**: [sub-skills/langchain-caching-rate-limits-usage-skill/SKILL.md](sub-skills/langchain-caching-rate-limits-usage-skill/SKILL.md)
- **LangSmith datasets, examples, experiments, and evaluation client workflows.**: [sub-skills/langchain-langsmith-evaluation-skill/SKILL.md](sub-skills/langchain-langsmith-evaluation-skill/SKILL.md)
- **Local/classic evaluators such as exact match, regex, JSON validity, and string distance.**: [sub-skills/langchain-local-evaluation-skill/SKILL.md](sub-skills/langchain-local-evaluation-skill/SKILL.md)
- **SQLDatabase, SQL query chains, SQL agents/toolkits, graph QA, and database safety.**: [sub-skills/langchain-sql-graph-toolkits-skill/SKILL.md](sub-skills/langchain-sql-graph-toolkits-skill/SKILL.md)
- **OpenAPI, RequestsToolkit, APIChain, HTTP tools, and external request safety.**: [sub-skills/langchain-openapi-http-tools-skill/SKILL.md](sub-skills/langchain-openapi-http-tools-skill/SKILL.md)
- **Security boundaries, SSRF protection, shell/Python/database dangerous tools, and sandbox audits.**: [sub-skills/langchain-security-sandbox-skill/SKILL.md](sub-skills/langchain-security-sandbox-skill/SKILL.md)
- **`langchain-classic` migration, deprecated imports, legacy chains, and migration scanning.**: [sub-skills/langchain-classic-migration-skill/SKILL.md](sub-skills/langchain-classic-migration-skill/SKILL.md)

## Execution Contract

1. Resolve whether the user is building a modern LangChain 1.x workflow or maintaining `langchain-classic` code.
2. Pick the closest sub-skill and load its `SKILL.md`; read one or two linked references only when needed.
3. Prefer public imports from `langchain_core`, `langchain`, integration packages, `langchain_community`, and `langchain_text_splitters`.
4. Use bundled scripts for no-key smoke tests, import inspection, config checks, and deterministic debug examples.
5. Avoid requiring a real API key for validation unless the user explicitly requests a live provider run.
6. Report exact commands, artifact paths, public package versions, and any live-provider assumptions.

## Shared Resources

- [references/coverage-matrix.md](references/coverage-matrix.md): maps LangChain capability families to sub-skills and bundled scripts.
- [references/installation.md](references/installation.md): package boundaries, optional integrations, and import checks.
- [references/troubleshooting.md](references/troubleshooting.md): cross-cutting import, version, provider, key, and migration issues.
- [scripts/check_langchain_env.py](scripts/check_langchain_env.py): safe public package and optional dependency checker.
- [scripts/inspect_langchain_api.py](scripts/inspect_langchain_api.py): read-only API/signature inspection helper.
- [scripts/run_all_smokes.py](scripts/run_all_smokes.py): runs bundled no-key smoke scripts and prints pass/fail JSON.
- [scripts/validate_skill_tree.py](scripts/validate_skill_tree.py): validates frontmatter, local links, lowercase-hyphen names, path leaks, and eval metadata.

The `evals/` directory is a development artifact for self-refine checks and is not linked as runtime documentation.
