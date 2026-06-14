# Classic Migration Workflows

## LLMChain To LCEL

1. Identify prompt variables and output parser.
2. Build a prompt object from `langchain_core.prompts`.
3. Use a provider chat model or fake model for smoke tests.
4. Compose `prompt | model | parser`.
5. Replace `.run`/`.predict` call sites with `.invoke`, `.batch`, `.stream`, or async variants.

## Classic Memory To Runnable History

1. Identify the session key and message variable name.
2. Store messages through `InMemoryChatMessageHistory` or a production-backed history.
3. Wrap the LCEL chain with `RunnableWithMessageHistory`.
4. Pass `config={"configurable": {"session_id": "..."}}`.

## Provider Import Migration

Install the provider package and import from it directly. Keep provider credentials outside prompts, metadata, and logs.

## RAG Import Migration

Move loaders to community/provider packages, splitters to `langchain_text_splitters`, and vector stores to core/provider integration packages.
