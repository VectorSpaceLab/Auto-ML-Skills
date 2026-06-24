# Remote SDK API Reference

## Import Surface

```python
import langgraph_sdk
```

The Python SDK exposes client helpers for remote graph servers. Exact factory names and methods are version-sensitive; inspect the installed SDK before coding.

## Concepts

- server/base URL
- graph or assistant id
- thread id
- run id
- stream mode/events
- auth token or platform credentials

## No-Network Rule

Import and signature checks can run locally. Creating threads, invoking runs, or streaming requires a running LangGraph server and user-approved credentials.
