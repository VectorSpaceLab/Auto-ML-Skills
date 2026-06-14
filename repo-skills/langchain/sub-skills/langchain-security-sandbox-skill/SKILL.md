---
name: langchain-security-sandbox-skill
description: "Use when a user wants LangChain security boundaries, SSRF protection, ShellToolMiddleware, HostExecutionPolicy, dangerous request tools, sandboxing, unsafe deserialization, or agent tool safety audits."
disable-model-invocation: true
---

# LangChain Security Sandbox

Use `langchain-security-sandbox-skill` when a workflow exposes network, shell, Python, database, file, or deserialization capabilities to an agent. Quick answer: default to no external side effects, use SSRF protection for URL access, avoid host shell execution unless explicitly trusted, and run [scripts/smoke_security_boundaries.py](scripts/smoke_security_boundaries.py).

## Short Workflow

1. Identify dangerous surfaces: HTTP requests, shell/Python tools, SQL execution, filesystem access, arbitrary URLs, or stored serialized objects.
2. Require explicit user approval before enabling side effects or `allow_dangerous_requests`.
3. Use allowlists for hosts, paths, commands, tables, and methods.
4. Prefer sandboxed or mock execution for tests.
5. Run [scripts/smoke_security_boundaries.py](scripts/smoke_security_boundaries.py) to validate SSRF blocking and security imports.
6. Read [references/security-sandbox.md](references/security-sandbox.md) before wiring tools into agents.

## Bundled Scripts

- [scripts/smoke_security_boundaries.py](scripts/smoke_security_boundaries.py): validates `SSRFPolicy` blocks localhost/private URLs and import-checks shell middleware policy symbols.
- [scripts/audit_dangerous_tool_imports.py](scripts/audit_dangerous_tool_imports.py): scans a Python file for dangerous LangChain tool imports and flags review items.

## References

- [references/api-reference.md](references/api-reference.md): SSRF and shell middleware public imports/signatures.
- [references/security-sandbox.md](references/security-sandbox.md): practical safety rules for agents and tools.
- [references/troubleshooting.md](references/troubleshooting.md): blocked URLs, sandbox errors, dangerous request flags, and unsafe deserialization.

## Boundaries

Use SQL/Graph or OpenAPI/HTTP skills for those specific workflows. Use this skill to audit or constrain security-sensitive behavior across LangChain apps.
