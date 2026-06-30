# AI Memory SDKs and App Integration

## When To Read

Persistent memory SDKs, memory search/update/delete flows, self-hosted memory services, memory CLIs, and agent memory integrations.

## Repo Skill Options

<!-- DISCO_SCENARIO:ai-memory-sdks-and-app-integration:START -->
### `khoj`

Role: Khoj is a self-hosted AI second-brain application that combines document ingestion, semantic search, chat, agents, automations, and persistent memories.
Read when: Tasks mention Khoj, AI second brain, self-hosted personal AI, document chat/search, /api/content, /api/search, /api/chat, /api/agents, /api/automation, /api/memories, Khoj clients, local model providers, or errors involving Khoj startup, indexing, search, chat, agents, automations, or memory scoping.
Best for: Installing or operating Khoj, syncing and parsing personal documents, debugging semantic search and filters, configuring chat models and agents, creating scheduled automations, managing memories, or maintaining the Khoj Python repository.
Avoid when: Use a lower-level vector database, embedding model, generic document parser, or generic FastAPI/Django skill when the task is not specifically about Khoj or a Khoj-like second-brain app workflow.
Useful entry points: `khoj/SKILL.md`, `khoj/sub-skills/deployment-api/SKILL.md`, `khoj/sub-skills/content-indexing/SKILL.md`, `khoj/sub-skills/search-retrieval/SKILL.md`, `khoj/sub-skills/chat-agents/SKILL.md`, `khoj/sub-skills/automations-memory/SKILL.md`, `khoj/sub-skills/development/SKILL.md`.

### `mem0`

Role: Routes Mem0 SDK and OSS memory tasks to concrete Python/TypeScript APIs, configuration, and troubleshooting guidance.
Read when: mem0, mem0ai, MemoryClient, AsyncMemoryClient, Memory, mem0ai/oss, user_id filters, persistent memory, memory layer, OpenAI agent memory. mem0 init, mem0 add, mem0 search, @mem0/cli, mem0-cli, --agent, --json, MCP mem0, Codex hooks, Cursor MCP, Claude plugin, createMem0, @mem0/vercel-ai-provider, OpenClaw, Pi Agent. self-hosted Mem0, OpenMemory, server docker compose, dashboard auth, API keys, JWT_SECRET, ADMIN_API_KEY, AUTH_DISABLED, pgvector, Qdrant, local MCP, request logs.
Best for: Hosted Platform SDK calls, OSS Memory setup, provider/vector/LLM/reranker configuration, memory CRUD/search workflows, and app-level retrieve-generate-store patterns. CLI scripting, machine-readable memory operations, editor/agent plugin setup, Vercel AI SDK memory provider, and framework cookbook adaptation. Docker Compose setup, upgrade/auth troubleshooting, API key issuance, REST server behavior, OpenMemory MCP, migrations, backups, and environment validation.
Avoid when: The task is about an unrelated memory library, generic vector database theory, or a paper-to-skills workflow rather than the Mem0 repository. The task only needs raw database/vector-store internals or non-Mem0 CLI tooling. The user wants hosted Platform SDK usage or in-process OSS Memory without deploying services.
Useful entry points: `mem0/SKILL.md`, `mem0/sub-skills/sdk-memory/SKILL.md`, `mem0/sub-skills/provider-configuration/SKILL.md`, `mem0/sub-skills/cli-memory/SKILL.md`, `mem0/sub-skills/integrations-plugins/SKILL.md`, `mem0/sub-skills/self-hosted-openmemory/SKILL.md`.

<!-- DISCO_SCENARIO:ai-memory-sdks-and-app-integration:END -->

## How To Choose

Choose the memory skill for persistent user or application memory, and then use its sub-skill routes for SDK calls, CLI operations, or self-hosted deployment. Choose khoj when the user is working with Khoj's self-hosted AI second-brain server, document indexing/search, chat/agent tooling, automation/memory features, or the Khoj repository itself; choose more generic skills only when no Khoj-specific API, CLI, config, data-source, chat command, or error signal is present. Choose `mem0` over generic SDK skills when Mem0-specific package names, APIs, filters, providers, CLI, self-hosting, or integrations are mentioned. Start at the root router unless the request clearly names SDK or provider configuration. Choose the CLI sub-skill for shell commands and JSON envelopes; choose integrations/plugins for MCP, editor hooks, Vercel AI SDK, or framework adapters. Route service, dashboard, auth, Docker, and OpenMemory tasks here; route local SDK provider config back to provider-configuration.
