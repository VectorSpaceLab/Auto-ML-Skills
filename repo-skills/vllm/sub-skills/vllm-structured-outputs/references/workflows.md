# Structured Output Workflows

## Server Path

1. Start `vllm serve` for a text-generation/chat model.
2. Build a deterministic request with `temperature: 0` and small schema.
3. Send to `/v1/chat/completions` or `/v1/completions`.
4. Parse the returned text as JSON or validate it against the requested constraint.
5. If decoding fails, reduce schema complexity and increase `max_tokens`.

## Offline Path

Use `SamplingParams` fields for guided decoding when supported by the installed version. Because field names can change, inspect `vllm.SamplingParams` first:

```bash
python ../../scripts/inspect_api.py --object vllm:SamplingParams
```

## Tool Calling

Tool calling depends on model family, chat template, and parser. Provide tools in OpenAI chat format and use the parser/template recommended for the model. If tools are returned as plain text, check chat template and parser flags.
