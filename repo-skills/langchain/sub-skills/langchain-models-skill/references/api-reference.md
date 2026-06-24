# Models API Reference

## Core Fake Models

Use fake models for deterministic no-key tests:

```python
from langchain_core.language_models import FakeListChatModel, FakeListLLM
from langchain_core.embeddings import DeterministicFakeEmbedding, FakeEmbeddings
```

Common methods:

- Chat models and LLMs implement `invoke`, `batch`, `stream`, `ainvoke`, `abatch`, and `astream`.
- Chat model inputs can be a string, a list of messages, or prompt output depending on the runnable.
- Embeddings implement `embed_query(text)` and `embed_documents(list_of_texts)`.

## Provider Packages

Install and import provider wrappers explicitly:

```python
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
```

Other provider packages follow the same pattern but can vary by class name. Check with the shared `inspect_langchain_api.py` script or package docs before writing production imports.

## Core Base Types

Useful for custom wrappers and type checks:

```python
from langchain_core.language_models import BaseChatModel, BaseLLM
from langchain_core.embeddings import Embeddings
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
```

Prefer composing models through LCEL instead of calling private generation methods.
