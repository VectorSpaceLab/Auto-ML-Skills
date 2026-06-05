#!/usr/bin/env python3
"""No-network smoke for OpenAPI/HTTP tool safety checks."""

from __future__ import annotations

import json


SPEC = {
    "openapi": "3.0.0",
    "info": {"title": "Demo API", "version": "1.0.0"},
    "servers": [{"url": "https://api.example.test"}],
    "paths": {
        "/items/{item_id}": {
            "get": {
                "operationId": "getItem",
                "parameters": [{"name": "item_id", "in": "path", "required": True, "schema": {"type": "string"}}],
                "responses": {"200": {"description": "ok"}},
            }
        },
        "/items": {
            "post": {
                "operationId": "createItem",
                "responses": {"201": {"description": "created"}},
            }
        },
    },
}


def main() -> int:
    import importlib.util

    methods = []
    mutating = []
    for path, path_spec in SPEC["paths"].items():
        for method in path_spec:
            methods.append(f"{method.upper()} {path}")
            if method.upper() in {"POST", "PUT", "PATCH", "DELETE"}:
                mutating.append(f"{method.upper()} {path}")

    result = {
        "imports": {
            "openapi_converter": importlib.util.find_spec(
                "langchain_classic.chains.openai_functions.openapi"
            )
            is not None,
            "community_openapi_toolkit": importlib.util.find_spec(
                "langchain_community.agent_toolkits.openapi.toolkit"
            )
            is not None,
        },
        "endpoint_count": len(methods),
        "methods": methods,
        "mutating_methods": mutating,
        "network_calls": 0,
        "requires_dangerous_request_review": bool(mutating),
    }
    result["pass"] = result["endpoint_count"] == 2 and result["network_calls"] == 0
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
