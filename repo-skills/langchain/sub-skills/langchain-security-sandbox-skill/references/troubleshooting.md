# Security Sandbox Troubleshooting

## URL Is Blocked By SSRF Policy

This is usually correct for localhost, private networks, cloud metadata, or Kubernetes internal hosts. Add `allowed_hosts` only when the user explicitly trusts the target.

## `allow_dangerous_requests` Required

Do not bypass silently. Confirm the endpoint, methods, credentials, and expected side effects.

## Shell Tool Times Out

Lower command complexity, increase timeout only for trusted commands, and capture limited output. Do not remove limits to make an agent loop pass.

## Command Cannot Access Files

Check workspace root and sandbox policy. Do not broaden filesystem access unless the user asked for it and the risk is acceptable.

## Unsafe Deserialization Warning

Switch to safe JSON/document serialization or restrict data source to trusted stores.
