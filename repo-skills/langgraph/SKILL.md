---
name: langgraph
description: "Use when a user wants an agent to build, inspect, debug, or deploy LangGraph stateful graph, checkpoint, interrupt, streaming, prebuilt tool-agent, subgraph, multi-agent, Platform, Studio, CLI, or server workflows from natural language."
disable-model-invocation: true
---

# LangGraph

This is the router for the LangGraph repo skill. Use it to choose the nearest focused sub-skill, then read only that sub-skill plus the linked references/scripts. Do not require the source repository checkout; work from public package installs, public API docs, and the bundled helper scripts.

## Public Install

Prefer a clean Python environment supported by the current LangGraph packages.

```bash
python -m pip install -U pip setuptools wheel
pip install -U langgraph
python -c "from langgraph.graph import StateGraph; print(StateGraph.__name__)"
```

Optional public packages:

```bash
pip install -U "langgraph-cli[inmem]"
pip install -U langgraph-checkpoint-sqlite
pip install -U langgraph-checkpoint-postgres
```

Run the root checks after installation:

```bash
python scripts/check_langgraph_env.py
python scripts/inspect_langgraph_api.py --summary
```

See [references/installation.md](references/installation.md) for package choices and [references/troubleshooting.md](references/troubleshooting.md) for cross-cutting failures.

## Route To Sub-Skills

- **Graph API, StateGraph, MessageGraph, reducers, nodes, edges, conditional routing, Command, and Send.**: [sub-skills/langgraph-graph-state-skill/SKILL.md](sub-skills/langgraph-graph-state-skill/SKILL.md)
- **Graph visualization, `get_graph()`, Mermaid, xray, `path_map`, and diagram debugging.**: [sub-skills/langgraph-graph-visualization-introspection-skill/SKILL.md](sub-skills/langgraph-graph-visualization-introspection-skill/SKILL.md)
- **Node reliability policies: retry, cache, timeout, defer, error handlers, and clear-cache checks.**: [sub-skills/langgraph-node-policy-cache-retry-timeout-skill/SKILL.md](sub-skills/langgraph-node-policy-cache-retry-timeout-skill/SKILL.md)
- **Checkpoints, thread memory, `thread_id`, bare interrupts, resume, and human-in-the-loop.**: [sub-skills/langgraph-checkpoint-interrupt-skill/SKILL.md](sub-skills/langgraph-checkpoint-interrupt-skill/SKILL.md)
- **Checkpoint persistence backends: InMemory, SQLite, Postgres, async savers, and setup.**: [sub-skills/langgraph-persistence-backends-skill/SKILL.md](sub-skills/langgraph-persistence-backends-skill/SKILL.md)
- **Checkpoint serialization/security: strict msgpack, allowlists, encrypted serializers, and migration.**: [sub-skills/langgraph-checkpoint-serde-security-skill/SKILL.md](sub-skills/langgraph-checkpoint-serde-security-skill/SKILL.md)
- **Agent Inbox / HumanInterrupt schema payloads, action approval, and list-shaped resume responses.**: [sub-skills/langgraph-human-inbox-interrupt-skill/SKILL.md](sub-skills/langgraph-human-inbox-interrupt-skill/SKILL.md)
- **Prebuilt `create_react_agent`, `ToolNode`, `tools_condition`, tool errors, and fake tool-agent checks.**: [sub-skills/langgraph-prebuilt-tools-agent-skill/SKILL.md](sub-skills/langgraph-prebuilt-tools-agent-skill/SKILL.md)
- **Advanced prebuilt agent options: `response_format`, hooks, `ToolNode` wrappers, and injected state/store.**: [sub-skills/langgraph-prebuilt-advanced-agent-skill/SKILL.md](sub-skills/langgraph-prebuilt-advanced-agent-skill/SKILL.md)
- **Streaming, stream modes, events, async invoke/stream, custom output, and subgraph stream namespaces.**: [sub-skills/langgraph-streaming-async-skill/SKILL.md](sub-skills/langgraph-streaming-async-skill/SKILL.md)
- **Subgraphs, parent commands, multi-agent handoffs, map-reduce Send fan-out, and hierarchical agent patterns.**: [sub-skills/langgraph-subgraphs-multi-agent-skill/SKILL.md](sub-skills/langgraph-subgraphs-multi-agent-skill/SKILL.md)
- **Store/runtime context, injected store/state, configurable values, and runtime API drift.**: [sub-skills/langgraph-store-runtime-context-skill/SKILL.md](sub-skills/langgraph-store-runtime-context-skill/SKILL.md)
- **Long-term semantic memory stores, namespaces, search, TTL, and cross-thread memory.**: [sub-skills/langgraph-semantic-store-memory-skill/SKILL.md](sub-skills/langgraph-semantic-store-memory-skill/SKILL.md)
- **Functional API with `@task`, `@entrypoint`, checkpointed functions, and compact workflows.**: [sub-skills/langgraph-functional-api-skill/SKILL.md](sub-skills/langgraph-functional-api-skill/SKILL.md)
- **State debugging, `get_state`, `get_state_history`, `update_state`, and time travel.**: [sub-skills/langgraph-state-debug-time-travel-skill/SKILL.md](sub-skills/langgraph-state-debug-time-travel-skill/SKILL.md)
- **Local LLM validation with Transformers/Hugging Face models inside graph nodes.**: [sub-skills/langgraph-local-llm-validation-skill/SKILL.md](sub-skills/langgraph-local-llm-validation-skill/SKILL.md)
- **LangGraph Platform, Studio, CLI, dev server, langgraph.json, server build, and deployment preparation.**: [sub-skills/langgraph-platform-cli-skill/SKILL.md](sub-skills/langgraph-platform-cli-skill/SKILL.md)
- **Deployment config auditing, env vars, dependencies, auth hooks, and server packaging.**: [sub-skills/langgraph-deployment-config-skill/SKILL.md](sub-skills/langgraph-deployment-config-skill/SKILL.md)
- **Remote SDK clients, threads/runs, streaming sessions, auth, hosted/local server calls.**: [sub-skills/langgraph-remote-sdk-skill/SKILL.md](sub-skills/langgraph-remote-sdk-skill/SKILL.md)
- **Configuration, package integration, version migration, common errors, and repo-wide troubleshooting.**: [sub-skills/langgraph-configuration-troubleshooting-skill/SKILL.md](sub-skills/langgraph-configuration-troubleshooting-skill/SKILL.md)

## Execution Contract

1. Clarify whether the user needs a local graph workflow, an agent/tool workflow, checkpointed/human-in-loop behavior, streaming, subgraph composition, or deployment.
2. Read the selected sub-skill `SKILL.md`, then load one linked reference only when needed.
3. Use bundled scripts for import checks, API inspection, minimal smoke tests, and config validation before adapting real user code.
4. Keep examples no-key by default. Ask for provider credentials only when the user explicitly wants a real model or hosted service run.
5. For durable state, require a checkpointer and a `config={"configurable": {"thread_id": "..."}}`.
6. Report exact commands, user artifact paths, stream modes, state transitions, checkpoint IDs when relevant, and unresolved version or provider risks.

## Shared Resources

- [references/coverage-matrix.md](references/coverage-matrix.md): maps public capability families to sub-skills and smoke scripts.
- [references/installation.md](references/installation.md): public package install, optional extras, and import checks.
- [references/troubleshooting.md](references/troubleshooting.md): common graph, checkpoint, prebuilt, streaming, CLI, and deployment failures.
- [scripts/check_langgraph_env.py](scripts/check_langgraph_env.py): safe import and version check for public packages.
- [scripts/inspect_langgraph_api.py](scripts/inspect_langgraph_api.py): read-only API signature helper.
- [scripts/run_all_smokes.py](scripts/run_all_smokes.py): runs bundled no-key smoke scripts and prints pass/fail JSON.
- [scripts/validate_skill_tree.py](scripts/validate_skill_tree.py): validates this skill tree's frontmatter, links, paths, and local-path leakage.

The `evals/` directory is a development artifact for extraction and test notes. It is not runtime documentation.
