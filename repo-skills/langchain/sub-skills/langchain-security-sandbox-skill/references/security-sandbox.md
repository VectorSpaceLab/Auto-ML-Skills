# Security Sandbox Workflows

## Review Checklist

Before exposing a tool to an agent, record:

- what side effects it can perform
- allowed hosts, paths, commands, methods, or tables
- credential scope
- timeout and output limits
- audit log behavior
- human approval requirements

## HTTP Tools

- Allowlist hosts.
- Block localhost/private networks unless explicitly required and trusted.
- Disable mutating methods by default.
- Add request timeouts.
- Keep secrets out of prompts/tool descriptions.

## Shell And Python Tools

- Prefer a sandbox or container.
- Use a temporary workspace.
- Limit CPU, memory, output bytes, and timeout.
- Never run shell tools against user-provided commands without a clear trust boundary.

## SQL And Database Tools

- Use read-only users.
- Restrict visible tables.
- Review generated SQL before execution.
- Reject DDL/DML by default.

## Deserialization

Do not deserialize untrusted stored objects. Use simple JSON or typed schemas when possible.
