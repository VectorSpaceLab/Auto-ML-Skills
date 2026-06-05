# Local LLM Validation Troubleshooting

## Missing `torch` Or `transformers`

Install runtime packages in the environment that loads the model:

```bash
pip install -U transformers torch
```

## Model Path Fails

Check for `config.json`, tokenizer files, and model weights. Public model ids may require network access.

## Out Of Memory

Reduce `max_new_tokens`, use CPU, choose a smaller dtype if supported, or validate with a smaller model first.

## Chat Template Error

Fall back to a plain prompt. Chat templates are tokenizer/model specific.

## Tool Calls Missing

This is expected for many local causal LMs. Use text generation in graph nodes or add a wrapper/parser that explicitly supports tool-call formatting.
