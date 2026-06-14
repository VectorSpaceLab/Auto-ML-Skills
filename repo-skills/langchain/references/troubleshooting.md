# Cross-Cutting Troubleshooting

## Import Errors

- `ModuleNotFoundError: langchain_openai`: install the provider package; it is not bundled by `langchain`.
- `ModuleNotFoundError: langchain_text_splitters`: install `langchain-text-splitters`.
- `ModuleNotFoundError: langchain_community`: install `langchain-community`.
- Legacy imports such as `from langchain.chains import LLMChain` may require `langchain-classic` or should be migrated to LCEL.

## Version Drift

- In LangChain 1.x, framework primitives usually live in `langchain_core`.
- Top-level `langchain` is mostly for agents and high-level app construction.
- Provider wrappers moved to partner packages. Avoid old imports from `langchain.chat_models`, `langchain.llms`, or `langchain.embeddings` when writing new code.

## API Keys And Tracing

- Provider model calls need provider keys. No-key smoke tests should use `FakeListChatModel`, `FakeListLLM`, `DeterministicFakeEmbedding`, or deterministic `RunnableLambda`.
- LangSmith tracing normally uses `LANGSMITH_TRACING=true`, `LANGSMITH_API_KEY`, and optional `LANGSMITH_PROJECT`.
- Do not enable tracing in smoke tests unless the user requests it.

## LCEL Shape Errors

- `prompt | model | parser` is a `RunnableSequence`; call `.invoke`, `.batch`, `.stream`, `.ainvoke`, `.abatch`, or `.astream`.
- Dict literals inside LCEL create parallel runnable mappings. Use `RunnablePassthrough.assign(...)` when preserving the original input and adding fields.
- Message prompts often expect dict input, not a raw string, unless the prompt has exactly one input variable.

## Tool Calling And Structured Output

- Tool calling is provider-dependent. `bind_tools` may exist but live behavior can differ by provider and model.
- `with_structured_output` requires model support or a provider-specific fallback. Validate with a fake or provider-supported schema before production use.
- Pydantic schemas should have clear field descriptions for best provider behavior.

## Retrieval

- Vector stores and loaders are integration-specific. Install the exact backend package, for example Chroma or Qdrant integrations.
- Use deterministic fake embeddings for local smoke tests; do not download embedding models unless the user asks.
- Text splitters are not a vector store; split documents before embedding or indexing.

## Async And Streaming

- Use `ainvoke`, `abatch`, `astream`, and `astream_events` in async contexts.
- Do not call `asyncio.run` inside an already running event loop; await the coroutine instead.
- Streaming chunks may be message chunks, strings, parser diffs, or event dicts depending on the runnable.
