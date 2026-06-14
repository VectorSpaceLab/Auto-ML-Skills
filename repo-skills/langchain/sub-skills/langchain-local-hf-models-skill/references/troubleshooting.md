# Local HF Troubleshooting

## `ModuleNotFoundError: langchain_huggingface`

Install:

```bash
pip install -U langchain-huggingface
```

If only raw model loading must be checked, run the smoke script with the Transformers path first.

## Missing `torch` Or `transformers`

Install the runtime packages:

```bash
pip install -U transformers torch
```

For GPU machines, match the Torch build to the CUDA runtime available on the host.

## Model Directory Does Not Load

Check that the local directory contains `config.json`, tokenizer files, and at least one weight file. If the path is a model id instead of a directory, network access may be required.

## Out Of Memory

Use a smaller model, lower `max_new_tokens`, CPU mode, or a lower dtype where supported. Do not make long generation part of a smoke test.

## Chat Wrapper Fails

Validate raw `HuggingFacePipeline` first. `ChatHuggingFace` needs a compatible tokenizer/model wrapper and may not support provider-specific chat features such as native tool calling.

## Output Echoes The Prompt

Set pipeline generation options such as `return_full_text=False` when supported, or strip the decoded prompt prefix in raw Transformers smoke tests.

## Tool Calling Does Not Work

Local Transformers text-generation models usually emit text, not provider-native `tool_calls`. Use an explicit prompt/parser loop or a model wrapper proven to implement `bind_tools()`.
