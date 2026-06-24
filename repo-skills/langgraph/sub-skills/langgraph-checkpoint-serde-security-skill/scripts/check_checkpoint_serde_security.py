#!/usr/bin/env python3
"""Check LangGraph checkpoint serializer imports and security posture hints."""

from __future__ import annotations

import json
import os


def main() -> int:
    result: dict[str, object] = {
        "env": {
            "LANGGRAPH_STRICT_MSGPACK": os.environ.get("LANGGRAPH_STRICT_MSGPACK"),
        },
        "jsonplus": None,
        "encrypted_importable": False,
    }
    try:
        from langgraph.checkpoint.serde.jsonplus import JsonPlusSerializer

        serde = JsonPlusSerializer(pickle_fallback=False, allowed_msgpack_modules=None)
        result["jsonplus"] = {
            "importable": True,
            "pickle_fallback": getattr(serde, "pickle_fallback", None),
            "class": type(serde).__name__,
        }
    except Exception as exc:  # noqa: BLE001 - diagnostic script
        result["jsonplus"] = {"importable": False, "error": f"{type(exc).__name__}: {exc}"}

    try:
        from langgraph.checkpoint.serde.encrypted import EncryptedSerializer  # noqa: F401

        result["encrypted_importable"] = True
    except Exception:
        result["encrypted_importable"] = False

    result["pass"] = bool(result["jsonplus"] and result["jsonplus"].get("importable"))
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
