# AI Pipelines, Workflows, RAG, and Agents

## When To Read

Pipeline and workflow frameworks that combine embeddings, LLMs, agents, task chains, services, and RAG orchestration.

## Repo Skill Options

<!-- DISCO_SCENARIO:ai-pipelines-workflows-and-rag:START -->
### `kotaemon`

Role: Kotaemon covers a document-QA RAG app plus a composable Python RAG library for building, configuring, and debugging retrieval workflows.
Read when: The task mentions Kotaemon, ktem, document QA, file index chat, `BaseComponent`, `Document`, `RetrievedDocument`, vector retrieval, citation QA, RAG pipelines, prompt UI, reasoning modes, GraphRAG in Kotaemon, or a Gradio RAG app with LLM and embedding resources.
Best for: Installing or operating the Kotaemon web app, composing Kotaemon RAG pipelines, configuring file indexes and retrieval, debugging citations and low-confidence answers, and adding custom reasoning/index extensions.
Avoid when: Avoid for generic vector database clients, standalone LlamaIndex/LangChain tasks not using Kotaemon, or unrelated model serving frameworks; choose a narrower retrieval, provider, or serving skill instead.
Useful entry points: `kotaemon/SKILL.md`, `kotaemon/sub-skills/app-deployment/SKILL.md`, `kotaemon/sub-skills/rag-core/SKILL.md`, `kotaemon/sub-skills/model-providers/SKILL.md`.

### `langflow`

Role: Use `langflow` for Langflow's visual AI workflow system, flow JSON, components, executor, API clients, and deployment workflows.
Read when: The task mentions Langflow, flows, visual workflow builder, components, nodes/edges, tweaks, starter projects, flow import/export, `lfx run`, `lfx serve`, MCP tools, Langflow API run endpoints, or RAG/agent workflow orchestration in Langflow.
Best for: Authoring and validating Langflow flows, building components/bundles, running flows through LFX, calling Langflow REST/SDK APIs, and troubleshooting Langflow workflow execution.
Avoid when: Use a model-serving, vector database, generic LangChain, or provider-specific skill when the task is not about Langflow's workflow platform or repository.
Useful entry points: `langflow/SKILL.md`, `langflow/sub-skills/flow-authoring/SKILL.md`, `langflow/sub-skills/component-development/SKILL.md`, `langflow/sub-skills/executor-cli/SKILL.md`, `langflow/sub-skills/sdk-and-api-clients/SKILL.md`.

### `ragflow`

Role: RAGFlow skill for maintaining or using a full-stack RAG engine with document parsing, dataset ingestion, retrieval, chat, agents, and frontend/API surfaces.
Read when: Tasks mention RAGFlow, document ingestion, parser_config, datasets/documents/chunks, RAG retrieval, GraphRAG, RAPTOR, task executors, chat assistants, citations, or multi-service RAG app debugging.
Best for: Tracing RAGFlow workflows across deployment, backend API routes, parser_config, task execution, retrieval/search, SDK/HTTP calls, agent canvas, and frontend integration.
Avoid when: Use narrower vector database, retriever-model, document-conversion, or generic web-framework skills when the request is not about RAGFlow or a RAGFlow-like full-stack app.
Useful entry points: `ragflow/SKILL.md`, `ragflow/sub-skills/dataset-ingestion-retrieval/SKILL.md`, `ragflow/sub-skills/sdk-http-integration/SKILL.md`.

### `txtai`

Role: Helps agents choose between deterministic txtai workflows and agentic/LLM/RAG orchestration, then use the correct sub-skill.
Read when: txtai Workflow, Task, pipeline, Textractor, Summary, Translation, RAG, LLM, Agent, tools, smolagents, workflow YAML, generator not consumed.
Best for: Composing task pipelines, debugging lazy workflows, selecting LLM/RAG/agent backends, configuring tools, and producing safe no-download templates.
Avoid when: The user only needs a generic LangChain/LlamaIndex answer or asks for a non-txtai orchestration framework.
Useful entry points: `txtai/SKILL.md`, `txtai/sub-skills/pipelines-and-workflows/SKILL.md`, `txtai/sub-skills/agents-and-llm-orchestration/SKILL.md`.

<!-- DISCO_SCENARIO:ai-pipelines-workflows-and-rag:END -->

## How To Choose

Use this scenario when the package is primarily an end-to-end AI workflow system rather than only a retriever, vector database, or model-serving backend. Choose kotaemon when the request combines a document QA/RAG app, file indexing, LLM/embedding resources, citations, or Kotaemon/ktem APIs rather than only a generic provider SDK or vector store. Choose `langflow` when the user needs Langflow-specific flow JSON, components, visual workflow behavior, LFX execution, Langflow APIs/SDK, MCP integration, or Langflow deployment guidance rather than a generic LLM framework. Choose ragflow when the task combines RAG application operations, document ingestion, RAGFlow API/SDK calls, or RAGFlow-specific deployment and source-code changes. Choose pipelines-and-workflows for deterministic batch/stream processing; choose agents-and-llm-orchestration for RAG, model backends, tool choice, and multi-step reasoning.
