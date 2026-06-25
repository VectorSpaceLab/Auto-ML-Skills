# AI Memory SDKs and App Integration

## When To Read

Persistent memory SDKs, memory search/update/delete flows, self-hosted memory services, memory CLIs, and agent memory integrations.

## Repo Skill Options

<!-- SKILLQED_SCENARIO:ai-memory-sdks-and-app-integration:START -->
### `mem0`

Role: Routes Mem0 SDK and OSS memory tasks to concrete Python/TypeScript APIs, configuration, and troubleshooting guidance.
Read when: mem0, mem0ai, MemoryClient, AsyncMemoryClient, Memory, mem0ai/oss, user_id filters, persistent memory, memory layer, OpenAI agent memory. mem0 init, mem0 add, mem0 search, @mem0/cli, mem0-cli, --agent, --json, MCP mem0, Codex hooks, Cursor MCP, Claude plugin, createMem0, @mem0/vercel-ai-provider, OpenClaw, Pi Agent. self-hosted Mem0, OpenMemory, server docker compose, dashboard auth, API keys, JWT_SECRET, ADMIN_API_KEY, AUTH_DISABLED, pgvector, Qdrant, local MCP, request logs.
Best for: Hosted Platform SDK calls, OSS Memory setup, provider/vector/LLM/reranker configuration, memory CRUD/search workflows, and app-level retrieve-generate-store patterns. CLI scripting, machine-readable memory operations, editor/agent plugin setup, Vercel AI SDK memory provider, and framework cookbook adaptation. Docker Compose setup, upgrade/auth troubleshooting, API key issuance, REST server behavior, OpenMemory MCP, migrations, backups, and environment validation.
Avoid when: The task is about an unrelated memory library, generic vector database theory, or a paper-to-skills workflow rather than the Mem0 repository. The task only needs raw database/vector-store internals or non-Mem0 CLI tooling. The user wants hosted Platform SDK usage or in-process OSS Memory without deploying services.
Useful entry points: `mem0/SKILL.md`, `mem0/sub-skills/sdk-memory/SKILL.md`, `mem0/sub-skills/provider-configuration/SKILL.md`, `mem0/sub-skills/cli-memory/SKILL.md`, `mem0/sub-skills/integrations-plugins/SKILL.md`, `mem0/sub-skills/self-hosted-openmemory/SKILL.md`.

<!-- SKILLQED_SCENARIO:ai-memory-sdks-and-app-integration:END -->

## How To Choose

Choose the memory skill for persistent user or application memory, and then use its sub-skill routes for SDK calls, CLI operations, or self-hosted deployment. Choose `mem0` over generic SDK skills when Mem0-specific package names, APIs, filters, providers, CLI, self-hosting, or integrations are mentioned. Start at the root router unless the request clearly names SDK or provider configuration. Choose the CLI sub-skill for shell commands and JSON envelopes; choose integrations/plugins for MCP, editor hooks, Vercel AI SDK, or framework adapters. Route service, dashboard, auth, Docker, and OpenMemory tasks here; route local SDK provider config back to provider-configuration.
