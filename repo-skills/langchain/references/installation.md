# Installation And Package Boundaries

LangChain 1.x is split across a small core package, the top-level agent package, optional community integrations, and provider-specific partner packages.

## Minimal Installs

- Core LCEL, prompts, messages, parsers, fake models, callbacks, in-memory vector store: `langchain-core`.
- Top-level agents and default agent factory: `langchain`.
- Community loaders, retrievers, vector stores, and legacy compatibility: `langchain-community` and `langchain-classic`.
- Text splitters: `langchain-text-splitters`.
- LangSmith tracing/evaluation client: `langsmith`.
- Provider model packages: install only the provider package needed by the user, for example `langchain-openai`, `langchain-anthropic`, `langchain-ollama`, `langchain-chroma`, or `langchain-qdrant`.

## Import Rules

- Prefer `langchain_core.prompts`, `langchain_core.messages`, `langchain_core.output_parsers`, `langchain_core.runnables`, `langchain_core.tools`, `langchain_core.vectorstores`, and `langchain_core.embeddings` for framework primitives.
- Use `from langchain.agents import create_agent` for modern agent construction.
- Use provider packages for live models, for example `from langchain_openai import ChatOpenAI, OpenAIEmbeddings`.
- Use `langchain_text_splitters` for splitters such as `RecursiveCharacterTextSplitter`.
- Use `langchain_community` for loaders/vector stores that are not in core or a dedicated provider package.
- Treat `langchain_classic` as maintenance mode for legacy chains, legacy agents, and old memory APIs.

## No-Key Validation

Use fake models and deterministic embeddings for smoke tests:

```python
from langchain_core.language_models import FakeListChatModel, FakeListLLM
from langchain_core.embeddings import DeterministicFakeEmbedding
```

The bundled scripts use these fake components when available and fall back to simple deterministic runnables when an optional package is absent.

## Live Provider Runs

For live runs, collect these before executing:

- Provider package name and version.
- Model name, endpoint/base URL if any, and environment variable name for the key.
- Whether streaming, tool calling, JSON mode, or structured output is required.
- Timeout, max retries, and rate-limit expectations.

Never print secrets. When debugging, print whether a key is present, not its value.
