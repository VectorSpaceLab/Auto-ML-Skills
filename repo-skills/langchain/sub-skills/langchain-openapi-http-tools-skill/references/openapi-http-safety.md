# OpenAPI HTTP Safety

## Default Rules

- Do not make network calls in smoke tests.
- Do not pass user secrets into tool descriptions or prompts.
- Restrict base URL and allowed hosts.
- Disable mutating methods unless explicitly requested.
- Add request timeouts.
- Require explicit confirmation before enabling `allow_dangerous_requests`.

## Spec Audit Checklist

1. Confirm OpenAPI version and parse compatibility.
2. List endpoints and methods.
3. Identify mutating operations: `POST`, `PUT`, `PATCH`, `DELETE`.
4. Identify auth requirements.
5. Identify path/query/body parameters.
6. Reduce the spec to only needed endpoints before exposing tools.

## SSRF Boundary

HTTP tools can be abused to reach internal metadata services or private networks. Use SSRF protection where available and never allow arbitrary URL tools in untrusted workflows.

## Live API Workflow

Only after the offline audit passes:

1. Use a test endpoint or mock server.
2. Use least-privilege credentials.
3. Log all requested URLs/methods.
4. Add human approval for mutating operations.
