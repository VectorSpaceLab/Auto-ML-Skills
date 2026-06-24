# Offline CLI Reference

## `vllm chat`

Use for interactive local chat. Prefer package help for exact flags:

```bash
vllm chat --help
vllm chat Qwen/Qwen3-0.6B --generation-config vllm
```

## `vllm complete`

Use for prompt completion:

```bash
vllm complete --help
vllm complete Qwen/Qwen3-0.6B --prompt "The fastest way to test vLLM is" --max-tokens 32
```

## `vllm run-batch`

Use when the user has a JSONL file of OpenAI-format requests. Create small test files with `scripts/make_batch_requests.py`.

Example JSONL line for chat:

```json
{"custom_id":"request-0","method":"POST","url":"/v1/chat/completions","body":{"model":"Qwen/Qwen3-0.6B","messages":[{"role":"user","content":"Say hello."}],"temperature":0,"max_tokens":16}}
```

Example JSONL line for completion:

```json
{"custom_id":"request-0","method":"POST","url":"/v1/completions","body":{"model":"Qwen/Qwen3-0.6B","prompt":"Hello","temperature":0,"max_tokens":16}}
```

Always run `vllm run-batch --help` in the installed version because backend and output flags may change.
