# LangSmith Evaluation API Reference

## Imports

```python
from langsmith import Client
```

LangSmith APIs are service-backed. Import checks and local planning can run without credentials, but dataset creation, example upload, tracing, and evaluation require credentials and network access.

## Environment Variables

- `LANGSMITH_API_KEY`: required for service calls.
- `LANGSMITH_TRACING=true`: enables tracing in LangChain runs.
- `LANGSMITH_PROJECT`: optional project name for traces.
- `LANGSMITH_ENDPOINT`: optional non-default endpoint.

## Evaluation Planning Fields

- dataset name or id
- input schema and expected outputs
- target chain/function/model
- evaluators and metrics
- experiment prefix/name
- concurrency and retry policy
