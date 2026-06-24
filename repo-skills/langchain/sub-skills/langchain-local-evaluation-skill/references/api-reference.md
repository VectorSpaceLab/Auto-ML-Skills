# Local Evaluator API Reference

## Imports

```python
from langchain_classic.evaluation import (
    ExactMatchStringEvaluator,
    JsonValidityEvaluator,
    RegexMatchStringEvaluator,
    StringDistanceEvalChain,
    load_evaluator,
)
```

Verified signatures:

```text
load_evaluator(evaluator, *, llm=None, **kwargs)
ExactMatchStringEvaluator(ignore_case=False, ignore_punctuation=False, ignore_numbers=False)
RegexMatchStringEvaluator(flags=0)
JsonValidityEvaluator()
StringDistanceEvalChain(distance=..., normalize_score=True)
```

## Deterministic Evaluators

```python
exact = ExactMatchStringEvaluator(ignore_case=True)
exact.evaluate_strings(prediction="Answer", reference="answer")

regex = RegexMatchStringEvaluator()
regex.evaluate_strings(prediction="ticket-123", reference=r"ticket-\d+")

json_eval = JsonValidityEvaluator()
json_eval.evaluate_strings(prediction='{"ok": true}')
```

These do not require API keys.

## Distance Evaluators

`StringDistanceEvalChain` requires `rapidfuzz`. Use it only after installing optional dependencies:

```bash
pip install rapidfuzz
```

## LLM-Judged Evaluators

Criteria, QA, and labeled criteria evaluators require an LLM. Pass the model explicitly, and keep prompts/criteria versioned because scores can vary by model and prompt.
