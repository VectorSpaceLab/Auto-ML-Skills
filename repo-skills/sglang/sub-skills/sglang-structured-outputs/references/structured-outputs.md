# Structured Outputs Reference

## Native Sampling Fields

`SamplingParams` supports `json_schema`, `regex`, `ebnf`, and `structural_tag`. Native validation enforces that only one of `json_schema`, `regex`, or `ebnf` is set.

Server-level grammar controls include:

- `--grammar-backend` with choices including `xgrammar`, `outlines`, `llguidance`, and `none`.
- `--constrained-json-whitespace-pattern`.
- `--constrained-json-disable-any-whitespace`.

## Native JSON Schema Example

```json
{
  "text": "Extract a city and date from: Paris on 2026-06-05.",
  "sampling_params": {
    "max_new_tokens": 64,
    "temperature": 0,
    "json_schema": "{\"type\":\"object\",\"properties\":{\"city\":{\"type\":\"string\"},\"date\":{\"type\":\"string\"}},\"required\":[\"city\",\"date\"],\"additionalProperties\":false}"
  }
}
```

## Regex Example

```json
{
  "text": "Return a two digit number:",
  "sampling_params": {
    "max_new_tokens": 4,
    "regex": "[0-9]{2}",
    "temperature": 0
  }
}
```

## Language Frontend Choices

```python
import sglang as sgl

@sgl.function
def classify(s, text):
    s += "Label the sentiment: " + text + "\n"
    s += "Label: " + sgl.select("label", ["positive", "neutral", "negative"])
```

For scalar typed generation, `sgl.gen(..., dtype=int)` maps to a regex internally. Avoid setting both `dtype` and `regex` in the same frontend generation call.

## Choosing A Backend

- `xgrammar`: default structured decoding path in many modern SGLang builds.
- `llguidance`: useful for grammar-heavy workloads when installed and supported.
- `outlines`: compatibility path; can rely on disk cache unless disabled by env.
- `none`: disable grammar backend for debugging unconstrained behavior.

## Failure Modes

- Invalid JSON schema string: validate with `json.loads` first.
- Regex that can match empty string or creates extreme buffering: simplify and bound lengths.
- Too many alternatives in `choices`: use classification/scoring endpoints instead.
- OpenAI client field mismatch: native SGLang uses `json_schema` in `sampling_params`; OpenAI uses `response_format` or tools depending on route.
