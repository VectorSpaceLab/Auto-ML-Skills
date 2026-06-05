# Security Sandbox API Reference

## SSRF Protection

```python
from langchain_core._security import SSRFPolicy, validate_url_sync
```

Verified signatures:

```text
SSRFPolicy(allowed_schemes=frozenset({"http", "https"}), block_private_ips=True, block_localhost=True, block_cloud_metadata=True, block_k8s_internal=True, allowed_hosts=frozenset(), additional_blocked_cidrs=())
validate_url_sync(url, policy=SSRFPolicy())
```

Use:

```python
policy = SSRFPolicy()
validate_url_sync("https://example.com", policy)
```

Localhost, private networks, and metadata endpoints are blocked by default.

## Shell Tool Middleware

Modern LangChain agents expose shell middleware symbols such as:

```python
from langchain.agents.middleware import HostExecutionPolicy, ShellToolMiddleware
```

`HostExecutionPolicy` executes on the host and is suitable only for trusted environments. Treat shell middleware as high risk.

## Dangerous HTTP Requests

Classic API/requests tools may require `allow_dangerous_requests=True`. This flag exists because the tool can make arbitrary or mutating requests. Do not set it silently.

## Store Deserialization

Docstore adapters that deserialize bytes must read only trusted data unless the adapter explicitly guarantees safe decoding.
