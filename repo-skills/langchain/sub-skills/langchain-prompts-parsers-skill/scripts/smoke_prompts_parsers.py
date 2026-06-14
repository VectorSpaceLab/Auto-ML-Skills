#!/usr/bin/env python3
"""No-key smoke test for LangChain prompts and output parsers."""

from __future__ import annotations

import json

from pydantic import BaseModel


class Answer(BaseModel):
    answer: str
    score: int


def main() -> int:
    from langchain_core.output_parsers import JsonOutputParser, PydanticOutputParser, StrOutputParser
    from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", "Answer in {style}."),
            MessagesPlaceholder("history"),
            ("human", "{question}"),
        ]
    )
    rendered = prompt.invoke({"style": "one sentence", "history": [], "question": "Ping?"})
    text = StrOutputParser().invoke("plain")
    parsed_json = JsonOutputParser().invoke('{"answer": "pong", "score": 1}')
    parsed_model = PydanticOutputParser(pydantic_object=Answer).invoke('{"answer": "pong", "score": 1}')
    result = {
        "message_count": len(rendered.messages),
        "str": text,
        "json_answer": parsed_json["answer"],
        "pydantic_score": parsed_model.score,
    }
    result["pass"] = result == {
        "message_count": 2,
        "str": "plain",
        "json_answer": "pong",
        "pydantic_score": 1,
    }
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
