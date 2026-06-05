# LCEL API Reference

## Public Classes

```python
from langchain_core.runnables import (
    RunnableLambda,
    RunnableParallel,
    RunnablePassthrough,
    RunnableBranch,
)
```

Common methods on runnables:

- `.invoke(input, config=None)`
- `.batch(inputs, config=None)`
- `.stream(input, config=None)`
- `.ainvoke(input, config=None)`
- `.abatch(inputs, config=None)`
- `.astream(input, config=None)`
- `.with_config(tags=[...], metadata={...}, run_name="...")`
- `.with_retry(...)`
- `.with_fallbacks([...])`

## LCEL Operators

- `a | b` creates a sequence.
- Dict literals inside an LCEL sequence create parallel keyed outputs; use `RunnableParallel(...)` when invoking a parallel mapping by itself.
- `RunnablePassthrough.assign(key=runnable_or_callable)` preserves the incoming dict and adds computed fields.

## Config

Pass runtime config as:

```python
chain.invoke(data, config={"tags": ["demo"], "metadata": {"case": "smoke"}})
```

Do not put secrets in metadata or tags because they may be traced.
