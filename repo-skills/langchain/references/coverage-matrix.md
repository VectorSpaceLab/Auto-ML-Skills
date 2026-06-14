# Coverage Matrix

| Capability | Sub-skill | References | Scripts |
| --- | --- | --- | --- |
| Chat models, LLMs, embeddings, fake models, provider packages | `langchain-models-skill` | `api-reference.md`, `configuration.md`, `troubleshooting.md` | `smoke_models.py` |
| Local HF/Transformers weights and Qwen-style local model validation | `langchain-local-hf-models-skill` | `api-reference.md`, `workflows.md`, `troubleshooting.md` | `check_hf_local_env.py`, `smoke_local_hf_model.py` |
| Prompt templates, messages, placeholders, output parsers | `langchain-prompts-parsers-skill` | `api-reference.md`, `workflows.md`, `troubleshooting.md` | `smoke_prompts_parsers.py` |
| LCEL runnable composition, routing, retries, fallbacks, config | `langchain-lcel-runnables-skill` | `api-reference.md`, `workflows.md`, `troubleshooting.md` | `smoke_lcel.py` |
| Document loading and loader dependency inspection | `langchain-document-loaders-skill` | `api-reference.md`, `workflows.md`, `troubleshooting.md` | `smoke_document_loaders.py`, `inspect_loader_requirements.py` |
| Text splitting and chunking | `langchain-text-splitters-skill` | `api-reference.md`, `workflows.md`, `troubleshooting.md` | `smoke_text_splitters.py` |
| Vector stores, indexing, ids, retriever search kwargs | `langchain-vectorstores-indexing-skill` | `api-reference.md`, `workflows.md`, `troubleshooting.md` | `smoke_vectorstores_indexing.py`, `check_vectorstore_package.py` |
| Basic retrieval and RAG composition | `langchain-retrieval-rag-skill` | `api-reference.md`, `workflows.md`, `troubleshooting.md` | `smoke_retrieval.py` |
| Advanced retrievers, parent docs, ensemble, self-query, compression | `langchain-advanced-retrievers-skill` | `api-reference.md`, `retriever-patterns.md`, `troubleshooting.md` | `smoke_advanced_retrievers.py`, `inspect_retriever_imports.py` |
| Agents, tools, tool calling | `langchain-agents-tools-skill` | `api-reference.md`, `workflows.md`, `troubleshooting.md` | `smoke_tools.py` |
| Agent middleware, hooks, shell middleware boundaries | `langchain-agent-middleware-skill` | `api-reference.md`, `workflows.md`, `troubleshooting.md` | `inspect_agent_middleware.py` |
| Memory, chat history, conversation state | `langchain-memory-history-skill` | `api-reference.md`, `workflows.md`, `troubleshooting.md` | `smoke_memory.py` |
| Stores, byte stores, docstores | `langchain-stores-docstores-skill` | `api-reference.md`, `workflows.md`, `troubleshooting.md` | `smoke_stores_docstores.py`, `inspect_store_apis.py` |
| Structured output, Pydantic, JSON parsers, function/tool parsers | `langchain-structured-output-skill` | `api-reference.md`, `workflows.md`, `troubleshooting.md` | `smoke_structured_output.py` |
| Streaming, batching, async, event streams | `langchain-streaming-async-skill` | `api-reference.md`, `workflows.md`, `troubleshooting.md` | `smoke_streaming_async.py` |
| Callbacks, tracing, LangSmith, config, metadata/tags | `langchain-observability-config-skill` | `api-reference.md`, `configuration.md`, `troubleshooting.md` | `smoke_observability.py` |
| Cache, rate limiting, usage metadata | `langchain-caching-rate-limits-usage-skill` | `api-reference.md`, `cache-rate-usage.md`, `troubleshooting.md` | `smoke_cache_rate_usage.py`, `inspect_cache_rate_usage.py` |
| LangSmith evaluation and hosted experiments | `langchain-langsmith-evaluation-skill` | `api-reference.md`, `workflows.md`, `troubleshooting.md` | `check_langsmith_eval_env.py` |
| Local classic evaluators | `langchain-local-evaluation-skill` | `api-reference.md`, `local-evaluators.md`, `troubleshooting.md` | `smoke_local_evaluators.py`, `inspect_local_evaluators.py` |
| SQLDatabase, SQL query chain, SQL/graph toolkits | `langchain-sql-graph-toolkits-skill` | `api-reference.md`, `sql-graph-safety.md`, `troubleshooting.md` | `smoke_sql_query_chain.py`, `inspect_sql_graph_imports.py` |
| OpenAPI, HTTP tools, APIChain, RequestsToolkit | `langchain-openapi-http-tools-skill` | `api-reference.md`, `openapi-http-safety.md`, `troubleshooting.md` | `smoke_openapi_http_tools.py`, `inspect_openapi_http_imports.py` |
| Security, SSRF, sandbox, dangerous tools | `langchain-security-sandbox-skill` | `api-reference.md`, `security-sandbox.md`, `troubleshooting.md` | `smoke_security_boundaries.py`, `audit_dangerous_tool_imports.py` |
| `langchain-classic` migration and deprecated import scanning | `langchain-classic-migration-skill` | `migration-map.md`, `workflows.md`, `troubleshooting.md` | `scan_classic_imports.py` |

## Source Signals Used During Extraction

- `libs/core/langchain_core`: prompts, messages, runnables, tools, output parsers, vector stores, embeddings, callbacks, tracing, chat history, fake models.
- `libs/langchain_v1/langchain`: modern `langchain.agents`, chat model and embedding namespace, tools, middleware.
- `libs/langchain/langchain_classic`: legacy chains, memory, classic agents, loaders, retrievers, and migration targets.
- `libs/text-splitters/langchain_text_splitters`: recursive and language-aware text splitting.
- `libs/partners/*`: provider-specific model integrations, tool calling, structured output support, and LangSmith parameter plumbing.
- Tests under `libs/*/tests`: runnable invocation, streaming/batching, prompt formatting, parser behavior, in-memory vector store, fake models, and provider integration patterns.
