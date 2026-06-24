---
name: langgraph-remote-sdk-skill
description: "Use when a user wants LangGraph SDK clients, remote graph invocation, hosted/local server API calls, threads/runs, streaming over SDK, auth, or no-network SDK import checks."
disable-model-invocation: true
---

# LangGraph Remote SDK

Use `langgraph-remote-sdk-skill` for client-side interaction with a LangGraph server or Platform deployment. Quick answer: install/import `langgraph_sdk`, create a client for the server URL, use threads/runs APIs, stream when needed, and validate imports with `scripts/check_remote_sdk.py`.

## Short Workflow

1. Confirm `langgraph_sdk` import with [scripts/check_remote_sdk.py](scripts/check_remote_sdk.py).
2. Identify target: local `langgraph dev/up` server or hosted deployment.
3. Confirm base URL, graph/assistant id, auth token, and thread id policy.
4. Use SDK streaming APIs for long runs or UI updates.
5. Do not make network calls without user-provided endpoint and credentials.

## Bundled Scripts

- [scripts/check_remote_sdk.py](scripts/check_remote_sdk.py): import-checks `langgraph_sdk` and lists likely client factory symbols without network calls.

## References

- [references/api-reference.md](references/api-reference.md): SDK import surface, client concept, threads/runs/streaming vocabulary.
- [references/workflows.md](references/workflows.md): local server, hosted deployment, streaming, and auth checklists.
- [references/troubleshooting.md](references/troubleshooting.md): endpoint, auth, graph id, streaming, and version mismatch issues.

## Boundaries

Use Platform/CLI or deployment config sub-skills to start/build the server. Use this skill to call an already running server.
