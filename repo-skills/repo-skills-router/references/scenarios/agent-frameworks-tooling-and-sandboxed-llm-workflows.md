# Agent Frameworks, Tooling, and Sandboxed LLM Workflows

## When To Read

LLM agent frameworks, browser automation agents, tool calling, graph/state runtimes, hosted or sandbox execution, MCP, CLIs, and production agent operations.

## Repo Skill Options

<!-- DISCO_SCENARIO:agent-frameworks-tooling-and-sandboxed-llm-workflows:START -->
### `adk-python`

Role: Provides self-contained routing and task guidance for building, running, debugging, evaluating, deploying, and maintaining ADK Python applications and the ADK Python source repository.
Read when: google-adk, google.adk, ADK Python, Agent, LlmAgent, Workflow, BaseNode, Runner, adk run, adk web, adk eval, ToolContext, FunctionTool, MCP toolset, ADK repo tests, AgentConfig.json.
Best for: Constructing ADK agents and Workflow graphs, binding tools, configuring runtime services, using CLI/YAML/deployment flows, debugging sessions/evals/traces, and selecting ADK repo validation commands.
Avoid when: The task concerns a different ADK implementation, a generic agent framework with no ADK signals, or cloud product administration that does not involve ADK Python APIs or CLI.
Useful entry points: `adk-python/SKILL.md`, `adk-python/sub-skills/agent-construction/SKILL.md`, `adk-python/sub-skills/workflow-orchestration/SKILL.md`, `adk-python/sub-skills/cli-configuration-deployment/SKILL.md`, `adk-python/sub-skills/repo-development/SKILL.md`.

### `autogen`

Role: Use `autogen` for maintaining, migrating, debugging, and safely operating Microsoft AutoGen Python 0.7.x applications, including AgentChat, Core runtimes, extensions, Studio, Magentic-One, AG Bench, and pyautogen compatibility.
Read when: The request names `autogen` or asks for package-specific APIs, CLIs, configs, data/model artifacts, error messages, workflows, or repository maintenance that match this project.
Best for: agentchat workflows, core runtime, extensions integrations, and tools studio bench.
Avoid when: another repo skill in this scenario matches the user's task, package, model family, data format, serving backend, or workflow more directly.
Useful entry points: `autogen/SKILL.md`, `autogen/sub-skills/agentchat-workflows/`, `autogen/sub-skills/core-runtime/`, `autogen/sub-skills/extensions-integrations/`, `autogen/sub-skills/tools-studio-bench/`.

### `browser-use`

Role: Use this self-contained Browser Use repo skill for Python agents that automate websites, browser sessions, custom tools, LLM/provider setup, persistent CLI sessions, cloud/sandbox production deployment, MCP, skills.
Read when: The request names `browser-use` or asks for package-specific APIs, CLIs, configs, data/model artifacts, error messages, workflows, or repository maintenance that match this project.
Best for: agent programming, browser control, cli and sessions, llm and output, production integrations, and tools and actions.
Avoid when: another repo skill in this scenario matches the user's task, package, model family, data format, serving backend, or workflow more directly.
Useful entry points: `browser-use/SKILL.md`, `browser-use/sub-skills/agent-programming/`, `browser-use/sub-skills/browser-control/`, `browser-use/sub-skills/cli-and-sessions/`, `browser-use/sub-skills/llm-and-output/`, `browser-use/sub-skills/production-integrations/`, `browser-use/sub-skills/tools-and-actions/`.

### `camel-ai`

Role: Guides future agents through CAMEL-AI's practical repo workflows with self-contained routes for agents, models, tools, memory/RAG, and datagen/evaluation.
Read when: User mentions CAMEL-AI, camel-ai, Python import camel, ChatAgent, RolePlaying, Workforce, ModelFactory, FunctionTool, MCPToolkit, CAMEL memory, CAMEL RAG, CAMEL benchmarks, or CAMEL datagen.
Best for: Creating CAMEL agents and multi-agent systems; selecting provider backends; attaching toolkits/runtimes/services; building memory/RAG/data pipelines; planning datagen, verifier, environment, or benchmark workflows.
Avoid when: The request is about an unrelated agent framework, pure OpenAI SDK usage without CAMEL, or implementing a new framework from scratch instead of using CAMEL-AI APIs.
Useful entry points: `camel-ai/SKILL.md`, `camel-ai/sub-skills/agents-and-societies/SKILL.md`, `camel-ai/sub-skills/models-and-configuration/SKILL.md`, `camel-ai/sub-skills/tools-runtimes-and-services/SKILL.md`, `camel-ai/sub-skills/memory-rag-and-data/SKILL.md`, `camel-ai/sub-skills/datagen-evaluation-and-benchmarks/SKILL.md`.

### `crewai`

Role: Provides self-contained CrewAI routing, verified APIs, workflow references, and safe diagnostics for the CrewAI Python framework and CLI.
Read when: CrewAI, crewai, crewai_tools, Agent, Task, Crew, Flow, crew.jsonc, crewai CLI, MCP, CrewAI memory, CrewAI tools, CrewAI tracing, multimodal input_files.
Best for: Designing crews and flows, validating JSONC projects, configuring provider/model settings, choosing tools/MCP/RAG/file workflows, troubleshooting CLI/runtime errors, and avoiding unsafe LLM or credential-bound execution.
Avoid when: The task is unrelated to CrewAI or asks about another agent framework without CrewAI migration or integration needs.
Useful entry points: `crewai/SKILL.md`, `crewai/sub-skills/core-runtime/SKILL.md`, `crewai/sub-skills/flows-and-events/SKILL.md`, `crewai/sub-skills/cli-and-projects/SKILL.md`.

### `haystack`

Role: Use Haystack to build, debug, evaluate, and maintain RAG, agent, pipeline, component, ingestion, retrieval, generator, tool-calling, and observability workflows for the haystack-ai package and repository.
Read when: The request names `haystack` or asks for package-specific APIs, CLIs, configs, data/model artifacts, error messages, workflows, or repository maintenance that match this project.
Best for: agents tools and hitl, data ingestion, evaluation and observability, generation and model components, pipelines and components, and 2 other focused workflows.
Avoid when: another repo skill in this scenario matches the user's task, package, model family, data format, serving backend, or workflow more directly.
Useful entry points: `haystack/SKILL.md`, `haystack/sub-skills/agents-tools-and-hitl/`, `haystack/sub-skills/data-ingestion/`, `haystack/sub-skills/evaluation-and-observability/`, `haystack/sub-skills/generation-and-model-components/`, `haystack/sub-skills/pipelines-and-components/`, `haystack/sub-skills/repo-development/`, `haystack/sub-skills/retrieval-and-rag/`.

### `langchain`

Role: Work on the LangChain Python monorepo: package routing, core primitives, v1 agents and middleware, classic APIs, partner integrations, standard tests, model profiles, and safe validation workflows.
Read when: The request names `langchain` or asks for package-specific APIs, CLIs, configs, data/model artifacts, error messages, workflows, or repository maintenance that match this project.
Best for: agents and middleware, classic chains, core primitives, integrations, monorepo development, and testing and profiles.
Avoid when: another repo skill in this scenario matches the user's task, package, model family, data format, serving backend, or workflow more directly.
Useful entry points: `langchain/SKILL.md`, `langchain/sub-skills/agents-and-middleware/`, `langchain/sub-skills/classic-chains/`, `langchain/sub-skills/core-primitives/`, `langchain/sub-skills/integrations/`, `langchain/sub-skills/monorepo-development/`, `langchain/sub-skills/testing-and-profiles/`.

### `langgraph`

Role: Build, run, persist, deploy, and operate LangGraph Python applications using the core runtime, prebuilt agents, checkpointing, CLI, and SDK clients.
Read when: The request names `langgraph` or asks for package-specific APIs, CLIs, configs, data/model artifacts, error messages, workflows, or repository maintenance that match this project.
Best for: cli deployment, graph runtime, persistence, prebuilt agents, and sdk clients.
Avoid when: another repo skill in this scenario matches the user's task, package, model family, data format, serving backend, or workflow more directly.
Useful entry points: `langgraph/SKILL.md`, `langgraph/sub-skills/cli-deployment/`, `langgraph/sub-skills/graph-runtime/`, `langgraph/sub-skills/persistence/`, `langgraph/sub-skills/prebuilt-agents/`, `langgraph/sub-skills/sdk-clients/`.

### `litellm`

Role: Use for LiteLLM Python SDK, AI Gateway proxy, model routing, provider endpoint mapping, MCP/A2A agent tooling, pass-through routes, guardrails, virtual keys, spend tracking, and troubleshooting across OpenAI-compatible LLM.
Read when: The request names `litellm` or asks for package-specific APIs, CLIs, configs, data/model artifacts, error messages, workflows, or repository maintenance that match this project.
Best for: agent tools, providers and endpoints, proxy server, routing, and sdk core.
Avoid when: another repo skill in this scenario matches the user's task, package, model family, data format, serving backend, or workflow more directly.
Useful entry points: `litellm/SKILL.md`, `litellm/sub-skills/agent-tools/`, `litellm/sub-skills/providers-and-endpoints/`, `litellm/sub-skills/proxy-server/`, `litellm/sub-skills/routing/`, `litellm/sub-skills/sdk-core/`.

### `llama-index`

Role: Build, customize, troubleshoot, and maintain LlamaIndex Python applications and the LlamaIndex monorepo. Routes ingestion, indexing/querying, agents/workflows, structured outputs, integrations/storage, and repo-maintenance tasks.
Read when: The request names `llama-index` or asks for package-specific APIs, CLIs, configs, data/model artifacts, error messages, workflows, or repository maintenance that match this project.
Best for: agents and workflows, customization and structured outputs, indexing and querying, ingestion and loading, integrations and storage, and repo maintenance.
Avoid when: another repo skill in this scenario matches the user's task, package, model family, data format, serving backend, or workflow more directly.
Useful entry points: `llama-index/SKILL.md`, `llama-index/sub-skills/agents-and-workflows/`, `llama-index/sub-skills/customization-and-structured-outputs/`, `llama-index/sub-skills/indexing-and-querying/`, `llama-index/sub-skills/ingestion-and-loading/`, `llama-index/sub-skills/integrations-and-storage/`, `llama-index/sub-skills/repo-maintenance/`.

### `mcp-agent`

Role: Provides repo-specific guidance for mcp-agent's SDK, workflow patterns, MCP server integration, Temporal execution, CLI/cloud operations, and observability.
Read when: The task mentions mcp-agent, MCPApp, Agent, AgentSpec, AugmentedLLM, RequestParams, mcp_agent.config.yaml, mcp_agent.secrets.yaml, LLMRouter, ParallelLLM, Orchestrator, EvaluatorOptimizerLLM, FastMCP app servers, mcp-agent CLI, mcp-cloud, Temporal executor, or MCP Agent Cloud. The task mentions MCP server config, stdio, SSE, streamable HTTP, websocket, roots, allowed_tools, create_mcp_server_for_app, workflows-run, workflows-get_status, OAuth MCP servers, token stores, sampling, elicitation, prompts, resources, or app-as-server behavior. The task mentions execution_engine temporal, TemporalExecutor, create_temporal_worker_for_app, workflow_task_modules, workflow_task_retry_policies, wait_for_signal, signal_workflow, pause/resume, long-running tools, or workflow resume/cancel.
Best for: Creating/debugging mcp-agent apps, composing workflow patterns, exposing apps as MCP servers, validating config, operating the CLI/cloud deployment flow, adding Temporal durability, and configuring logging/tracing/provider integrations. Diagnosing mcp.servers entries, wiring Agent server_names, validating app server tool surfaces, handling OAuth/resource metadata, and preparing safe client install/deploy steps. Converting workflow code to Temporal, writing worker skeletons, designing pause/resume approvals, setting retry policies, and deciding what needs a running Temporal service.
Avoid when: The task is only about generic MCP protocol usage without mcp-agent, or about another unrelated agent framework with no mcp-agent APIs/CLI/config. The task is generic CLI deployment with no MCP transport/auth detail; use the CLI/cloud route inside the same skill instead. The user only needs in-process pattern choice or one-shot local generation; use workflow-patterns or core-sdk instead.
Useful entry points: `mcp-agent/SKILL.md`, `mcp-agent/sub-skills/core-sdk/SKILL.md`, `mcp-agent/sub-skills/workflow-patterns/SKILL.md`, `mcp-agent/sub-skills/mcp-server-integration/SKILL.md`, `mcp-agent/sub-skills/cli-cloud-operations/SKILL.md`, `mcp-agent/sub-skills/durable-execution/SKILL.md`, `mcp-agent/sub-skills/observability-integrations/SKILL.md`.

### `meta-gpt`

Role: Use meta-gpt for MetaGPT's multi-agent software-company framework, Data Interpreter, RoleZero agents, RAG/tool integrations, extension environments, and MetaGPT repository maintenance.
Read when: Read meta-gpt when tasks mention MetaGPT, metagpt, MGX, software-company agents, Team/Role/Action/ActionNode, DataInterpreter, RoleZero, DataAnalyst, SWEAgent, AFlow, SPO, MetaGPT RAG, MetaGPT tools, config2.yaml, the metagpt CLI, generated workspace projects, or errors from MetaGPT provider/config/import workflows.
Best for: Project generation from natural-language requirements, configuring and troubleshooting MetaGPT provider settings, custom multi-agent roles/actions, DI data-analysis agents, MetaGPT RAG/tool diagnostics, AFlow/SPO/environment extension setup, and focused MetaGPT source maintenance.
Avoid when: Use a provider gateway skill for generic OpenAI-compatible proxy routing, a vector database skill for standalone vector client operations, or a generic Python maintenance skill when the task is not specific to MetaGPT APIs, CLI, config, examples, or tests.
Useful entry points: `meta-gpt/SKILL.md`, `meta-gpt/sub-skills/software-company/SKILL.md`, `meta-gpt/sub-skills/data-interpreter/SKILL.md`, `meta-gpt/sub-skills/rag-and-tools/SKILL.md`, `meta-gpt/sub-skills/extensions-and-environments/SKILL.md`, `meta-gpt/sub-skills/maintainer-apis/SKILL.md`.

### `omicverse`

Role: OmicVerse exposes agent-facing analysis through CLI commands, MCP registry tools, JARVIS/gateway workflows, provider backends, and skill-seeker utilities.
Read when: Read `omicverse` when the task mentions `omicverse-mcp`, Model Context Protocol, MCP phases, `omicverse claw`, JARVIS, gateway, OpenClaw, OmicClaw, `ov.Agent`, `OmicVerseAgent`, provider auth, `ov-skill-seeker`, registry tools, session handles, or exposing OmicVerse analysis to AI assistants.
Best for: OmicVerse MCP/CLI flags, safe service-start decisions, registry/manifest inspection, stdio troubleshooting, JARVIS/gateway routing, and AI-assisted analysis workflows over AnnData.
Avoid when: Use generic agent-framework or gateway skills when the request is not about OmicVerse's MCP server, CLI, agent runtime, or registry tools.
Useful entry points: `omicverse/SKILL.md`, `omicverse/sub-skills/agentic-and-mcp/SKILL.md`.

### `openai-agents-python`

Role: Provides self-contained routing and workflow guidance for building, debugging, and maintaining OpenAI Agents Python SDK applications.
Read when: User mentions openai-agents, OpenAI Agents SDK Python, agents.Agent, Runner, RunConfig, function_tool, handoff, guardrails, sessions, MCP, realtime agents, SandboxAgent, tracing, or this repository.
Best for: Creating agent workflows, configuring tools/handoffs/guardrails, choosing sessions and model providers, integrating MCP/realtime/sandbox/tracing, or editing this SDK repository safely.
Avoid when: The task is about the JavaScript/TypeScript Agents SDK, direct low-level OpenAI API calls without the SDK, or generic agent design that does not use this package.
Useful entry points: `openai-agents-python/SKILL.md`, `openai-agents-python/sub-skills/core-runtime/SKILL.md`, `openai-agents-python/sub-skills/tools-handoffs-guardrails/SKILL.md`, `openai-agents-python/sub-skills/models-providers/SKILL.md`, `openai-agents-python/sub-skills/repo-development/SKILL.md`.

### `pydantic-ai`

Role: Provides focused Pydantic AI ecosystem routing and self-contained references for application and framework tasks.
Read when: User mentions Pydantic AI, pydantic_ai, pydantic-graph, pydantic-evals, clai, Agent, RunContext, Tool, TestModel, FunctionToolset, ModelRetry, MCP, GraphBuilder, Dataset, Case, pai, or clai web.
Best for: Agent construction, typed deps, streaming, tools/toolsets, structured outputs, provider configuration, optional extras, MCP/capabilities/hooks, evals, graph workflows, CLI apps, and deterministic tests.
Avoid when: The task is about the standalone Pydantic validation library without Pydantic AI, an unrelated AI framework, or generic Python code with no Pydantic AI APIs.
Useful entry points: `pydantic-ai/SKILL.md`, `pydantic-ai/sub-skills/agent-core/SKILL.md`, `pydantic-ai/sub-skills/tools-and-toolsets/SKILL.md`, `pydantic-ai/sub-skills/outputs-and-messages/SKILL.md`, `pydantic-ai/sub-skills/models-and-providers/SKILL.md`, `pydantic-ai/sub-skills/mcp-and-integrations/SKILL.md`, `pydantic-ai/sub-skills/evals-and-graph/SKILL.md`, `pydantic-ai/sub-skills/cli-and-apps/SKILL.md`.

### `ragflow`

Role: RAGFlow skill for agent canvas DSL, components, templates, tools, memory, MCP retrieval, sandbox/code execution, webhooks, sessions, and debug traces inside RAGFlow.
Read when: Tasks mention RAGFlow agents, canvas DSL, components, templates, tool calls, memory, MCP ragflow_retrieval, sandbox/code executor, webhooks, component debug, agent sessions, or agent frontend canvas behavior.
Best for: Maintaining or debugging RAGFlow's agent workflow engine and integrating it with retrieval, memory, MCP, backend APIs, and frontend canvas screens.
Avoid when: Use another agent-framework skill when the task is about a different agent library or a generic MCP server unrelated to RAGFlow.
Useful entry points: `ragflow/sub-skills/agent-workflows/SKILL.md`, `ragflow/sub-skills/frontend-integration/SKILL.md`, `ragflow/sub-skills/sdk-http-integration/SKILL.md`.

### `smolagents`

Role: Build, debug, and operate Hugging Face smolagents agents, tools, model providers, secure executors, CLIs, and UI workflows with self-contained references and helpers.
Read when: The request names `smolagents` or asks for package-specific APIs, CLIs, configs, data/model artifacts, error messages, workflows, or repository maintenance that match this project.
Best for: agent workflows, cli and ui, execution and safety, model providers, and tools and integrations.
Avoid when: another repo skill in this scenario matches the user's task, package, model family, data format, serving backend, or workflow more directly.
Useful entry points: `smolagents/SKILL.md`, `smolagents/sub-skills/agent-workflows/`, `smolagents/sub-skills/cli-and-ui/`, `smolagents/sub-skills/execution-and-safety/`, `smolagents/sub-skills/model-providers/`, `smolagents/sub-skills/tools-and-integrations/`.

### `zenml`

Role: The zenml skill explains how to adapt ZenML agent and LLM examples into credential-aware, deployment-ready pipeline workflows.
Read when: The task mentions ZenML with agents, LLMOps, agent_comparison, deploying_agent, LangGraph/LangChain/LlamaIndex/OpenAI agents inside ZenML, deterministic fallbacks, DeploymentSettings, or agent service deployment.
Best for: Adapting ZenML agent examples, separating provider credentials from smoke tests, configuring pipeline deployments for agents, and routing framework matrix limitations safely.
Avoid when: Avoid for generic agent framework tasks that do not use ZenML pipelines, deployments, or repository examples; choose the framework-specific repo skill instead when available.
Useful entry points: `zenml/sub-skills/deployments-and-agents/SKILL.md`, `zenml/sub-skills/pipeline-authoring/SKILL.md`, `zenml/sub-skills/stacks-and-integrations/SKILL.md`.

<!-- DISCO_SCENARIO:agent-frameworks-tooling-and-sandboxed-llm-workflows:END -->

## How To Choose

Choose the repo skill whose framework, runtime, tool protocol, or agent execution surface most directly matches the request; use package names and API terms as the strongest signal. Choose `adk-python` over generic Python or agent skills when the task names ADK concepts, the google-adk distribution, the adk CLI, or files under an ADK Python checkout; use sub-skill routes to narrow to library usage, workflow graphs, CLI/deployment, debugging/eval, or repository maintenance. Choose `autogen` when the request names `autogen`, centers on maintaining, migrating, debugging, and safely operating Microsoft AutoGen Python 0.7.x applications, including AgentChat, Core runtimes, extensions, Studio, Magentic-One, AG Bench, and pyautogen compatibility, uses its APIs or CLIs, references its configs/artifacts/errors, or asks for repository workflows in agent frameworks tooling and sandboxed llm workflows. Choose `browser-use` when the request names `browser-use`, centers on Python agents that automate websites, browser sessions, custom tools, LLM/provider setup, persistent CLI sessions, cloud/sandbox production deployment, MCP, skills, and troubleshooting. Choose `camel-ai` for repository-specific CAMEL-AI API, configuration, optional-extra, troubleshooting, and workflow routing; choose a generic Python or OpenAI SDK skill only when CAMEL is not part of the task.
