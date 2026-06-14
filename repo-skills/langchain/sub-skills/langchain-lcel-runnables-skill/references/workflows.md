# LCEL Workflows

## Sequence

```python
chain = prompt | model | parser
result = chain.invoke({"question": "What is LCEL?"})
```

## Parallel Mapping

```python
chain = RunnableParallel(
    original=RunnablePassthrough(),
    normalized=RunnableLambda(lambda x: x.strip().lower()),
)
```

## Assign Fields

```python
chain = RunnablePassthrough.assign(
    length=lambda x: len(x["text"]),
)
result = chain.invoke({"text": "hello"})
```

## Routing

Use `RunnableBranch` or a router lambda when the route is simple. Keep route outputs compatible so downstream steps see one schema.

## Retries And Fallbacks

Use retries for transient provider failures and fallbacks for alternate models or deterministic defaults. Keep fallback output type compatible with the primary runnable.

## Graph Inspection

For complex chains, call `chain.get_graph()` and inspect node/edge names or render Mermaid if the installed version supports it.
