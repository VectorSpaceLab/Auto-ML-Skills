#!/usr/bin/env python3
"""No-key smoke test for LangChain chat history."""

from __future__ import annotations

import json


def main() -> int:
    from langchain_core.chat_history import InMemoryChatMessageHistory
    from langchain_core.messages import AIMessage, HumanMessage

    history = InMemoryChatMessageHistory()
    history.add_message(HumanMessage(content="hello"))
    history.add_message(AIMessage(content="hi"))
    result = {
        "count": len(history.messages),
        "first_type": history.messages[0].type,
        "last": history.messages[-1].content,
    }
    result["pass"] = result == {"count": 2, "first_type": "human", "last": "hi"}
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
