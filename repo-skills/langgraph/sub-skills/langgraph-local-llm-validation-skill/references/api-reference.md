# Local LLM Validation API Reference

## Graph Imports

```python
from typing_extensions import TypedDict
from langgraph.graph import START, END, StateGraph
```

Optional checkpoint:

```python
from langgraph.checkpoint.memory import InMemorySaver
```

## Transformers Imports

```python
from transformers import AutoModelForCausalLM, AutoTokenizer
```

Use raw Transformers first. LangGraph does not require a LangChain model wrapper for a node function to call a local model.

## Node Pattern

```python
class State(TypedDict):
    prompt: str
    answer: str

def generate(state: State) -> dict[str, str]:
    text = run_local_model(state["prompt"])
    return {"answer": text}
```

Then add node/edges and compile normally.

## Tool Calling Boundary

Plain local causal LMs generate text. They do not automatically implement provider-native `tool_calls`, `.bind_tools()`, or structured output. Validate those separately with a compatible wrapper.
