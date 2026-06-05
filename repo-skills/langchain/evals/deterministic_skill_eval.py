#!/usr/bin/env python3
"""Deterministic fallback evaluation over public LangChain skill content."""

from __future__ import annotations

import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


TASKS = {
    "build a RAG chain with text splitters and an in-memory vector store": "langchain-retrieval-rag-skill",
    "debug a ChatPromptTemplate variable and parse JSON output": "langchain-prompts-parsers-skill",
    "compose RunnableLambda with batch and fallback behavior": "langchain-lcel-runnables-skill",
    "define a typed tool and inspect its schema": "langchain-agents-tools-skill",
    "add RunnableWithMessageHistory for session memory": "langchain-memory-history-skill",
    "validate Pydantic structured output": "langchain-structured-output-skill",
    "stream async chunks and batch requests": "langchain-streaming-async-skill",
    "configure LangSmith tracing metadata and callbacks": "langchain-observability-config-skill",
    "choose provider chat model and deterministic fake embeddings": "langchain-models-skill",
}


def main() -> int:
    root_text = (ROOT / "SKILL.md").read_text(encoding="utf-8")
    coverage = (ROOT / "references" / "coverage-matrix.md").read_text(encoding="utf-8")
    errors: list[str] = []
    for task, skill in TASKS.items():
        if skill not in root_text:
            errors.append(f"router missing {skill} for task: {task}")
        skill_dir = ROOT / "sub-skills" / skill
        if not (skill_dir / "SKILL.md").exists():
            errors.append(f"missing sub-skill file: {skill}")
        if skill not in coverage:
            errors.append(f"coverage matrix missing {skill}")
        smoke_scripts = list((skill_dir / "scripts").glob("smoke_*.py"))
        if not smoke_scripts:
            errors.append(f"missing smoke script: {skill}")
    names = re.findall(r"^name: ([a-z0-9-]+)$", root_text, flags=re.MULTILINE)
    if names != ["langchain"]:
        errors.append("root frontmatter name mismatch")
    result = {"pass": not errors, "tasks": len(TASKS), "errors": errors}
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
