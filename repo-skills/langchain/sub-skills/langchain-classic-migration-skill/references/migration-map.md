# Classic Migration Map

| Legacy surface | Modern direction |
| --- | --- |
| `LLMChain` / `langchain.chains` | LCEL: `prompt | model | parser` |
| `langchain.llms`, `langchain.chat_models`, `langchain.embeddings` | Provider packages such as `langchain-openai`, `langchain-anthropic`, `langchain-ollama` |
| `langchain.document_loaders` | `langchain_community.document_loaders` or dedicated loader integrations |
| `langchain.text_splitter` | `langchain_text_splitters` |
| Classic memory classes | `RunnableWithMessageHistory` or LangGraph state/checkpoints |
| Classic agents | `langchain.agents.create_agent` or LangGraph prebuilt/custom graphs |
| Classic callbacks/tracing | `langchain_core.callbacks`, runtime config, LangSmith env vars |

Migration is not only import rewriting. Validate behavior, input/output shape, streaming, memory state, and callbacks after each change.
