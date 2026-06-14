#!/usr/bin/env python3
"""No-key smoke test for LangChain structured output parsers."""

from __future__ import annotations

import json

from pydantic import BaseModel, Field


class Answer(BaseModel):
    answer: str = Field(description="Short answer")
    score: int = Field(description="Confidence score")


def main() -> int:
    from langchain_core.output_parsers import JsonOutputParser, PydanticOutputParser

    raw = '{"answer": "ok", "score": 7}'
    json_value = JsonOutputParser().invoke(raw)
    model_value = PydanticOutputParser(pydantic_object=Answer).invoke(raw)
    schema = Answer.model_json_schema()
    result = {
        "json_answer": json_value["answer"],
        "model_score": model_value.score,
        "schema_has_answer": "answer" in schema.get("properties", {}),
    }
    result["pass"] = result["json_answer"] == "ok" and result["model_score"] == 7 and result["schema_has_answer"]
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
