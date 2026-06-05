# Agent Middleware API Reference

## Import Surface

```python
import langchain.agents.middleware as middleware
```

The exact middleware symbols are version-sensitive. Always inspect the installed package before naming a class/function in user code. Use the bundled inspection script or Python introspection.

## Common Middleware Purposes

- dynamic system prompts or context injection
- before/after model request handling
- tool-call approval or filtering
- guardrails and validation
- summarization or message trimming
- human-in-the-loop boundaries when not using LangGraph

## Practical Rule

If the behavior needs persistent state, branching, interrupt/resume, or multi-agent routing, route to LangGraph. If it modifies a LangChain agent run around model/tool calls, use middleware.
