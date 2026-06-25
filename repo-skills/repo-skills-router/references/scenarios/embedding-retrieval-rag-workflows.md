# Embedding Retrieval and RAG Workflows

## When To Read

Embedding models, semantic or sparse search, reranking, vector or graph RAG, retrieval training, corpus indexing, RAG pipelines, vector database clients, and retrieval evaluation.

## Repo Skill Options

<!-- SKILLQED_SCENARIO:embedding-retrieval-rag-workflows:START -->
### `beir`

Role: Provides self-contained routing and workflow guidance for the BEIR Python package and examples.
Read when: BEIR, beir, EvaluateRetrieval, GenericDataLoader, qrels, corpus.jsonl, queries.jsonl, DenseRetrievalExactSearch, BM25Search, Rerank, QueryGenerator, TrainRetriever, pytrec_eval.
Best for: Preparing BEIR datasets, validating custom corpora/qrels, running retrieval metrics, selecting dense/sparse/BM25/API backends, reranking candidates, generating synthetic queries, and planning SentenceTransformers training.
Avoid when: The task is about a different IR framework, general Elasticsearch operations without BEIR, or production search serving unrelated to BEIR benchmark data formats.
Useful entry points: `beir/SKILL.md`, `beir/sub-skills/data-loading/SKILL.md`, `beir/sub-skills/retrieval-evaluation/SKILL.md`, `beir/sub-skills/reranking/SKILL.md`, `beir/sub-skills/generation/SKILL.md`, `beir/sub-skills/training/SKILL.md`.

### `colbert`

Role: Use ColBERT/colbert-ai for late-interaction retrieval: prepare data, inspect configs, train/fine-tune, index collections, search rankings, update indexes, serve search, evaluate MS MARCO/LoTTE outputs, or reason about Baleen.
Read when: The request names `colbert` or asks for package-specific APIs, CLIs, configs, data/model artifacts, error messages, workflows, or repository maintenance that match this project.
Best for: baleen multihop, data and evaluation, index updates and serving, indexing and search, modeling and tokenization, and training and distillation.
Avoid when: another repo skill in this scenario matches the user's task, package, model family, data format, serving backend, or workflow more directly.
Useful entry points: `colbert/SKILL.md`, `colbert/sub-skills/baleen-multihop/`, `colbert/sub-skills/data-and-evaluation/`, `colbert/sub-skills/index-updates-and-serving/`, `colbert/sub-skills/indexing-and-search/`, `colbert/sub-skills/modeling-and-tokenization/`, `1 more sub-skills`.

### `feast`

Role: Use for Feast feature store tasks: feature repositories, definitions, CLI, retrieval, materialization, serving, RAG/vector search, integrations, and Feast contributor workflows.
Read when: The request names `feast` or asks for package-specific APIs, CLIs, configs, data/model artifacts, error messages, workflows, or repository maintenance that match this project.
Best for: feature definitions, feature repos and cli, integrations and extensibility, rag and vector search, repo development, and 2 other focused workflows.
Avoid when: another repo skill in this scenario matches the user's task, package, model family, data format, serving backend, or workflow more directly.
Useful entry points: `feast/SKILL.md`, `feast/sub-skills/feature-definitions/`, `feast/sub-skills/feature-repos-and-cli/`, `feast/sub-skills/integrations-and-extensibility/`, `feast/sub-skills/rag-and-vector-search/`, `feast/sub-skills/repo-development/`, `2 more sub-skills`.

### `flag-embedding`

Role: Use FlagEmbedding/BGE for embedding, reranking, retrieval/RAG model selection, fine-tuning data and command preparation, and evaluation workflow planning.
Read when: The request names `flag-embedding` or asks for package-specific APIs, CLIs, configs, data/model artifacts, error messages, workflows, or repository maintenance that match this project.
Best for: evaluation, finetuning, inference, and model catalog and rag.
Avoid when: another repo skill in this scenario matches the user's task, package, model family, data format, serving backend, or workflow more directly.
Useful entry points: `flag-embedding/SKILL.md`, `flag-embedding/sub-skills/evaluation/`, `flag-embedding/sub-skills/finetuning/`, `flag-embedding/sub-skills/inference/`, `flag-embedding/sub-skills/model-catalog-and-rag/`.

### `flashrag`

Role: Use FlashRAG for retrieval-augmented generation research workflows: config/data validation, retrieval and index building, generation/refinement components, RAG pipelines/method reproduction, evaluation, and WebUI setup.
Read when: The request names `flashrag` or asks for package-specific APIs, CLIs, configs, data/model artifacts, error messages, workflows, or repository maintenance that match this project.
Best for: data and config, evaluation and webui, generation and refinement, pipelines and methods, and retrieval and indexing.
Avoid when: another repo skill in this scenario matches the user's task, package, model family, data format, serving backend, or workflow more directly.
Useful entry points: `flashrag/SKILL.md`, `flashrag/sub-skills/data-and-config/`, `flashrag/sub-skills/evaluation-and-webui/`, `flashrag/sub-skills/generation-and-refinement/`, `flashrag/sub-skills/pipelines-and-methods/`, `flashrag/sub-skills/retrieval-and-indexing/`.

### `graphrag`

Role: Use Microsoft GraphRAG from CLI or Python: configure data/model/storage/vector settings, build or update indexes, query completed indexes, tune indexing prompts, and extend package factories safely.
Read when: The request names `graphrag` or asks for package-specific APIs, CLIs, configs, data/model artifacts, error messages, workflows, or repository maintenance that match this project.
Best for: configuration data, indexing, package extensions, prompt tuning, and querying.
Avoid when: another repo skill in this scenario matches the user's task, package, model family, data format, serving backend, or workflow more directly.
Useful entry points: `graphrag/SKILL.md`, `graphrag/sub-skills/configuration-data/`, `graphrag/sub-skills/indexing/`, `graphrag/sub-skills/package-extensions/`, `graphrag/sub-skills/prompt-tuning/`, `graphrag/sub-skills/querying/`.

### `haystack`

Role: Use Haystack to build, debug, evaluate, and maintain RAG, agent, pipeline, component, ingestion, retrieval, generator, tool-calling, and observability workflows for the haystack-ai package and repository.
Read when: The request names `haystack` or asks for package-specific APIs, CLIs, configs, data/model artifacts, error messages, workflows, or repository maintenance that match this project.
Best for: agents tools and hitl, data ingestion, evaluation and observability, generation and model components, pipelines and components, and 2 other focused workflows.
Avoid when: another repo skill in this scenario matches the user's task, package, model family, data format, serving backend, or workflow more directly.
Useful entry points: `haystack/SKILL.md`, `haystack/sub-skills/agents-tools-and-hitl/`, `haystack/sub-skills/data-ingestion/`, `haystack/sub-skills/evaluation-and-observability/`, `haystack/sub-skills/generation-and-model-components/`, `haystack/sub-skills/pipelines-and-components/`, `2 more sub-skills`.

### `lightrag`

Role: Provides repo-specific routes and verified guidance for using LightRAG's embedded APIs, ingestion pipeline, storage backends, provider bindings, and server/WebUI surfaces.
Read when: User mentions LightRAG, lightrag-hku, graph RAG, QueryParam, LightRAG.initialize_storages, process_options, LIGHTRAG_PARSER, lightrag-server, LightRAG WebUI, LightRAG storage classes, or LightRAG provider bindings.
Best for: Implementing embedded LightRAG workflows, configuring API/WebUI deployments, selecting storage backends, debugging document parser/chunker behavior, wiring LLM/embedding/rerank providers, and diagnosing common LightRAG errors.
Avoid when: The task is generic RAG theory, a different RAG framework, unrelated FastAPI/React work, or paper reproduction that does not involve the LightRAG repository/package.
Useful entry points: `lightrag/SKILL.md`, `lightrag/sub-skills/core-rag/SKILL.md`, `lightrag/sub-skills/document-pipeline/SKILL.md`, `lightrag/sub-skills/storage-backends/SKILL.md`, `lightrag/sub-skills/llm-providers/SKILL.md`, `lightrag/sub-skills/api-server/SKILL.md`.

### `llama-index`

Role: Build, customize, troubleshoot, and maintain LlamaIndex Python applications and the LlamaIndex monorepo. Routes ingestion, indexing/querying, agents/workflows, structured outputs, integrations/storage, and repo-maintenance tasks.
Read when: The request names `llama-index` or asks for package-specific APIs, CLIs, configs, data/model artifacts, error messages, workflows, or repository maintenance that match this project.
Best for: agents and workflows, customization and structured outputs, indexing and querying, ingestion and loading, integrations and storage, and repo maintenance.
Avoid when: another repo skill in this scenario matches the user's task, package, model family, data format, serving backend, or workflow more directly.
Useful entry points: `llama-index/SKILL.md`, `llama-index/sub-skills/agents-and-workflows/`, `llama-index/sub-skills/customization-and-structured-outputs/`, `llama-index/sub-skills/indexing-and-querying/`, `llama-index/sub-skills/ingestion-and-loading/`, `llama-index/sub-skills/integrations-and-storage/`, `1 more sub-skills`.

### `mteb`

Role: Use MTEB to evaluate embedding models, select tasks and benchmarks, validate model protocols, run CLI workflows, inspect result caches, and contribute tasks/models/benchmarks.
Read when: The request names `mteb` or asks for package-specific APIs, CLIs, configs, data/model artifacts, error messages, workflows, or repository maintenance that match this project.
Best for: cli and automation, contributing to mteb, evaluation workflows, models and encoders, results and leaderboard, and tasks and benchmarks.
Avoid when: another repo skill in this scenario matches the user's task, package, model family, data format, serving backend, or workflow more directly.
Useful entry points: `mteb/SKILL.md`, `mteb/sub-skills/cli-and-automation/`, `mteb/sub-skills/contributing-to-mteb/`, `mteb/sub-skills/evaluation-workflows/`, `mteb/sub-skills/models-and-encoders/`, `mteb/sub-skills/results-and-leaderboard/`, `1 more sub-skills`.

### `pyserini`

Role: Pyserini-specific routing and operational guidance for sparse Lucene retrieval, dense/Faiss retrieval, evaluation/fusion, REST/MCP serving, and source checkout maintenance.
Read when: pyserini, anserini, LuceneSearcher, LuceneIndexer, FaissSearcher, pyserini.encode, pyserini.eval, trec_eval, mcpyserini, Pyserini REST, No matching jar file found, pyjnius, faiss missing.
Best for: Installing Pyserini, indexing/searching/fetching with Lucene, building dense encoder/Faiss commands, evaluating TREC/MS MARCO/KILT runs, configuring REST/MCP servers, or selecting focused Pyserini source tests.
Avoid when: The task is generic IR theory, unrelated Lucene Java development, generic FastAPI/MCP usage without Pyserini, or another repository's retrieval stack.
Useful entry points: `pyserini/SKILL.md`, `pyserini/sub-skills/install-and-runtime/SKILL.md`, `pyserini/sub-skills/index-search-fetch/SKILL.md`, `pyserini/sub-skills/dense-encoding/SKILL.md`, `pyserini/sub-skills/evaluation-and-fusion/SKILL.md`, `pyserini/sub-skills/serving-and-agent-tools/SKILL.md`, `pyserini/sub-skills/repo-development/SKILL.md`.

### `qdrant-client`

Role: Provides self-contained routing and workflow guidance for the Qdrant Python client package.
Read when: qdrant-client, QdrantClient, AsyncQdrantClient, qdrant_client.models, Qdrant Cloud, FastEmbed, local mode, upload_collection, upload_points, migrate, REST/gRPC conversion. RAG, semantic search, vector upload, sparse vectors, hybrid query, filters, payload indexes, FastEmbed, Qdrant Cloud inference, query_points.
Best for: Connecting to Qdrant, prototyping with local mode, running sync or async operations, constructing model objects, using inference objects, bulk uploading vectors, and migrating collections. Building or debugging Python retrieval flows that create collections, upload vectors/documents, query with filters or fusion, and validate model/input schemas.
Avoid when: The task is about running the Qdrant server itself, designing vector search concepts without Python client code, or using another vector database client. The request needs framework-specific integration code for LangChain, LlamaIndex, or a non-Qdrant vector store without direct qdrant-client API usage.
Useful entry points: `qdrant-client/SKILL.md`, `qdrant-client/sub-skills/client-operations/SKILL.md`, `qdrant-client/sub-skills/local-mode/SKILL.md`, `qdrant-client/sub-skills/connection-and-transport/SKILL.md`, `qdrant-client/sub-skills/async-client/SKILL.md`, `qdrant-client/sub-skills/inference/SKILL.md`, `qdrant-client/sub-skills/migration-and-upload/SKILL.md`, `qdrant-client/sub-skills/models-and-conversions/SKILL.md`.

### `ragatouille`

Role: Guides agents through RAGatouille's training, indexing, search, reranking, integration, and export APIs with safe dependency and verification checks.
Read when: User asks to use RAGatouille, build/search ColBERT indexes, prepare RAG training data, rerank candidate documents, integrate with LangChain/LlamaIndex, or export ColBERT checkpoints.
Best for: Python RAG pipelines that need RAGatouille-specific API signatures, data formats, metadata handling, troubleshooting, and lightweight offline validation scripts.
Avoid when: The task is generic vector database work without RAGatouille/ColBERT, asks for a different retrieval package, or targets a post-PyLate RAGatouille release not covered by this source snapshot.
Useful entry points: `ragatouille/SKILL.md`, `ragatouille/sub-skills/pretrained-indexing-search/SKILL.md`, `ragatouille/sub-skills/training-data-finetuning/SKILL.md`, `ragatouille/sub-skills/index-free-reranking/SKILL.md`, `ragatouille/sub-skills/integrations-export/SKILL.md`.

### `sentence-transformers`

Role: Use Sentence Transformers for dense embeddings, semantic search, CrossEncoder reranking, SparseEncoder search, evaluation/training planning, and ONNX/OpenVINO backend optimization. Routes natural language tasks to focused.
Read when: The request names `sentence-transformers` or asks for package-specific APIs, CLIs, configs, data/model artifacts, error messages, workflows, or repository maintenance that match this project.
Best for: backend export optimization, embeddings and similarity, evaluation and training, reranking cross encoder, retrieval and utilities, and sparse encoder search.
Avoid when: another repo skill in this scenario matches the user's task, package, model family, data format, serving backend, or workflow more directly.
Useful entry points: `sentence-transformers/SKILL.md`, `sentence-transformers/sub-skills/backend-export-optimization/`, `sentence-transformers/sub-skills/embeddings-and-similarity/`, `sentence-transformers/sub-skills/evaluation-and-training/`, `sentence-transformers/sub-skills/reranking-cross-encoder/`, `sentence-transformers/sub-skills/retrieval-and-utilities/`, `1 more sub-skills`.

### `splade`

Role: Routes SPLADE repository tasks to focused guidance for classic Hydra pipelines, HF Trainer/reranking, model/data APIs, and export/pruning/evaluation.
Read when: User mentions SPLADE, splade.*, SParse Lexical AnD Expansion, Hydra configs, naver/splade models, Anserini SPLADE vectors, pytrec_eval, BEIR, PISA, static pruning, hard negatives, or RankT5/monoT5 reranking.
Best for: Constructing safe SPLADE commands, validating SPLADE data layouts, inspecting SPLADE APIs without downloads, diagnosing dependency/config errors, and planning export/evaluation/pruning workflows.
Avoid when: The task is generic dense retrieval unrelated to SPLADE, a different retrieval repo is named, or the user only needs general Hydra/Hugging Face help with no SPLADE-specific signals.
Useful entry points: `splade/SKILL.md`, `splade/sub-skills/hydra-pipelines/SKILL.md`, `splade/sub-skills/hf-training-reranking/SKILL.md`, `splade/sub-skills/model-data-api/SKILL.md`, `splade/sub-skills/pruning-export-evaluation/SKILL.md`.

### `tevatron`

Role: Provides Tevatron-specific routing, command construction, data schemas, optional dependency guidance, and bundled safe helpers for neural retrieval workflows.
Read when: Use when the task involves neural retriever datasets, retriever or reranker training, query/corpus encoding outputs, FAISS search, qrels, TREC runs, rerank JSONL, GradCache, LoRA retrievers, RepLLaMA, RankLLaMA, ColPali, DSE, Qwen, multimodal retrieval fields, or Tevatron module names such as tevatron.retriever and tevatron.reranker.
Best for: Preparing Tevatron datasets, building retriever training commands, encoding embeddings, searching and merging retrieval results, preparing or running rerankers, and planning multimodal or LLM retriever workflows.
Avoid when: Avoid for generic vector database usage, unrelated FAISS libraries, non-Tevatron Hugging Face training, or paper reproduction tasks that do not use Tevatron APIs and workflows.
Useful entry points: `tevatron/SKILL.md`, `tevatron/sub-skills/data-preparation/`, `tevatron/sub-skills/training/`, `tevatron/sub-skills/encoding-retrieval/`, `tevatron/sub-skills/reranking/`, `tevatron/sub-skills/multimodal-llm/`.

### `txtai`

Role: Routes agents to txtai-specific embeddings database construction, querying, persistence, and troubleshooting guidance.
Read when: txtai, Embeddings, semantic search, vector search, similar(...), SQL search, hybrid search, graph search, subindexes, content=True, FAISS, sparse, dense, object storage.
Best for: Building and maintaining txtai Embeddings indexes, writing query/filter logic, diagnosing result shapes, and selecting optional ANN/database/graph dependencies.
Avoid when: The task is about generic vector databases not using txtai, or about serving an already-built index over FastAPI without changing query logic.
Useful entry points: `txtai/SKILL.md`, `txtai/sub-skills/embeddings-search/SKILL.md`.

<!-- SKILLQED_SCENARIO:embedding-retrieval-rag-workflows:END -->

## How To Choose

Choose the repo skill whose package owns the retrieval layer named by the request: vector client, retriever model, sparse index, graph RAG system, RAG framework, or benchmark harness. Choose `beir` when the user names BEIR or uses BEIR-specific data, APIs, metrics, or example workflows; use sub-skill routes to narrow from dataset preparation to retrieval, reranking, generation, or training. Choose `colbert` when the request names `colbert`, centers on late-interaction retrieval: prepare data, inspect configs, train/fine-tune, index collections, search rankings, update indexes, serve search, evaluate MS MARCO/LoTTE outputs, or reason about Baleen multi-hop retrieval, uses its APIs or CLIs, references its configs/artifacts/errors, or asks for repository workflows in embedding retrieval rag workflows. Choose `feast` when the request names `feast`, centers on Use for Feast feature store tasks: feature repositories, definitions, CLI, retrieval, materialization, serving, RAG/vector search, integrations, and Feast contributor workflows, uses its APIs or CLIs, references its configs/artifacts/errors, or asks for repository workflows in embedding retrieval rag workflows. Choose `lightrag` when the user names LightRAG or its concrete APIs/CLI/configs. Prefer narrower generic skills only when the user is not using Pyserini. Choose `qdrant-client` for practical Python client usage.
