#!/usr/bin/env python3
"""No-network smoke for LangChain SSRF and dangerous-tool boundary checks."""

from __future__ import annotations

import importlib.util
import json


def main() -> int:
    from langchain_core._security import SSRFPolicy, validate_url_sync

    policy = SSRFPolicy()
    blocked = []
    allowed = []
    for url in ["http://127.0.0.1/", "http://169.254.169.254/latest/meta-data/"]:
        try:
            validate_url_sync(url, policy)
            allowed.append(url)
        except Exception as exc:  # noqa: BLE001 - diagnostic script
            blocked.append({"url": url, "error": type(exc).__name__})

    try:
        validate_url_sync("https://example.com/", policy)
        example_allowed = True
    except Exception:
        example_allowed = False

    result = {
        "blocked": blocked,
        "unexpected_allowed": allowed,
        "example_allowed": example_allowed,
        "shell_middleware_importable": importlib.util.find_spec("langchain.agents.middleware") is not None,
    }
    result["pass"] = len(blocked) == 2 and not allowed and example_allowed
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
