# OpenAPI HTTP Troubleshooting

## OpenAPI Parser Fails

Some installed package combinations have strict OpenAPI/Pydantic compatibility. Convert specs to a supported OpenAPI version or reduce the spec manually before conversion.

## `allow_dangerous_requests` Error

This is a safety gate. Do not bypass it silently. Confirm endpoint, method allowlist, credentials, and user intent.

## Tool Calls Unexpected URL

Restrict base URL and allowed hosts. Do not expose arbitrary URL request tools to an agent.

## Auth Header Leaks

Keep secrets outside prompt text and tool descriptions. Pass credentials through secure runtime configuration only.

## Network Timeout

Add short timeouts, retry policy outside the model loop, and clear error messages. Do not let agents retry mutating requests blindly.
