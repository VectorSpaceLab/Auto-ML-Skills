from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def _read_jsonl(path: Path, limit: int | None = None) -> list[dict[str, Any]]:
    docs: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if not line:
                continue
            docs.append(json.loads(line))
            if limit is not None and len(docs) >= limit:
                break
    return docs


def load_docs(path: Path, result_index: int = 0, jsonl_limit: int | None = None) -> list[dict[str, Any]]:
    if path.suffix == ".jsonl":
        return _read_jsonl(path, jsonl_limit)

    payload = json.loads(path.read_text(encoding="utf-8"))
    if isinstance(payload, list):
        docs = payload
    elif isinstance(payload, dict) and "docs" in payload:
        docs = payload["docs"]
    elif isinstance(payload, dict) and "results" in payload:
        docs = payload["results"][result_index]["docs"]
    else:
        raise ValueError("unsupported docs format; expected JSONL, list, {'docs': ...}, or {'results': [{'docs': ...}]}")

    if jsonl_limit is not None:
        docs = docs[:jsonl_limit]
    if not isinstance(docs, list):
        raise TypeError("docs payload must resolve to a list")
    return docs


def validate_docs(docs: list[dict[str, Any]]) -> list[str]:
    errors: list[str] = []
    for idx, doc in enumerate(docs):
        if not isinstance(doc, dict):
            errors.append(f"doc {idx}: must be object")
            continue
        contents = doc.get("contents")
        if not isinstance(contents, str) or not contents.strip():
            errors.append(f"doc {idx}: contents must be a non-empty string")
    return errors
