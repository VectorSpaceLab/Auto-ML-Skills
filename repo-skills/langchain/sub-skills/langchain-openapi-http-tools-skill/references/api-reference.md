# OpenAPI HTTP API Reference

## Classic And Community Imports

Common symbols:

```python
from langchain_classic.chains.api.base import APIChain
from langchain_classic.chains.openai_functions.openapi import openapi_spec_to_openai_fn
from langchain_community.agent_toolkits.openapi.spec import ReducedOpenAPISpec
from langchain_community.agent_toolkits.openapi.toolkit import OpenAPIToolkit, RequestsToolkit
```

Some imports are shims and may emit deprecation warnings. Prefer current standalone/community package locations reported by the installed version.

## APIChain Boundary

`APIChain` can make live HTTP calls. It includes safety controls such as `allow_dangerous_requests`. Do not enable it without explicit user confirmation, endpoint allowlists, and credential handling.

## OpenAPI Conversion

`openapi_spec_to_openai_fn(spec)` converts an OpenAPI spec object into function schemas and a callable. Validate this path with a minimal spec before introducing a live API.

## RequestsToolkit Boundary

`RequestsToolkit` exposes HTTP verbs as tools. Limit allowed methods, base URLs, headers, and request body shape. Treat it as potentially dangerous because agents may call external services.
