---
name: langchain-openapi-http-tools-skill
description: "Use when a user wants LangChain OpenAPI toolkits, RequestsToolkit, APIChain, OpenAPI function conversion, HTTP tool safety, allow_dangerous_requests, or API spec troubleshooting."
disable-model-invocation: true
---

# LangChain OpenAPI HTTP Tools

Use `langchain-openapi-http-tools-skill` for HTTP/API tool workflows. Quick answer: reduce and inspect OpenAPI specs offline first, do not make network calls by default, require explicit `allow_dangerous_requests` for APIChain-style tools, and validate imports/spec shape with [scripts/smoke_openapi_http_tools.py](scripts/smoke_openapi_http_tools.py).

## Short Workflow

1. Identify whether the user needs offline OpenAPI conversion, an HTTP requests toolkit, or a live API chain.
2. Inspect the OpenAPI spec locally and reduce it to the needed endpoints.
3. Keep live HTTP disabled until the user confirms base URL, auth, and allowed operations.
4. For APIChain or RequestsToolkit, require explicit dangerous-request acknowledgement and narrow allowlists.
5. Run [scripts/smoke_openapi_http_tools.py](scripts/smoke_openapi_http_tools.py).
6. Read [references/openapi-http-safety.md](references/openapi-http-safety.md) before enabling external calls.

## Bundled Scripts

- [scripts/smoke_openapi_http_tools.py](scripts/smoke_openapi_http_tools.py): no-network import and minimal OpenAPI spec audit.
- [scripts/inspect_openapi_http_imports.py](scripts/inspect_openapi_http_imports.py): reports OpenAPI/Requests/APIChain import availability and signatures.

## References

- [references/api-reference.md](references/api-reference.md): known OpenAPI/HTTP imports and package boundaries.
- [references/openapi-http-safety.md](references/openapi-http-safety.md): external request, auth, SSRF, and mutation safety.
- [references/troubleshooting.md](references/troubleshooting.md): Pydantic/OpenAPI parsing issues, dangerous request flags, and network failures.

## Boundaries

Use agents/tools for generic tool schemas and security-sandbox for SSRF/shell/dangerous execution policy. Use this skill when HTTP or OpenAPI tooling is central.
