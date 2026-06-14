# Offline Inference Workflows

## API Generation

Use `vllm.LLM` and `vllm.SamplingParams` for local batched inference.

```python
from vllm import LLM, SamplingParams

llm = LLM(model="Qwen/Qwen3-0.6B", generation_config="vllm")
params = SamplingParams(temperature=0.0, max_tokens=32)
outputs = llm.generate(["Explain vLLM in one sentence."], params)
print(outputs[0].outputs[0].text)
```

Set `generation_config="vllm"` for deterministic skill smoke runs; otherwise vLLM may apply the model repository's `generation_config.json`.

## Chat

Use `llm.chat` for chat/instruct models when messages are already in OpenAI format:

```python
messages = [[{"role": "user", "content": "Give one practical vLLM tip."}]]
outputs = llm.chat(messages, SamplingParams(temperature=0, max_tokens=32))
```

If using `llm.generate` with chat models, manually apply the tokenizer chat template before generation.

## SamplingParams

Common smoke-safe parameters:

- `temperature=0.0`
- `max_tokens=16` to `64`
- `top_p=1.0` when deterministic output is desired
- `stop=[...]` when the prompt format needs hard stops

Common production parameters:

- `temperature`, `top_p`, `top_k`, `min_p`
- `n`, `best_of` where supported
- `presence_penalty`, `frequency_penalty`, `repetition_penalty`
- `logprobs`, `prompt_logprobs`
- structured output fields are covered by `vllm-structured-outputs`

## Smoke Discipline

1. Run `python ../../scripts/check_env.py --json`.
2. Run `python scripts/run_offline_smoke.py --dry-run --model Qwen/Qwen3-0.6B`.
3. If model loading is allowed, run `python scripts/run_offline_smoke.py --model Qwen/Qwen3-0.6B --max-tokens 8`.
4. Save stdout and JSON summary to the user's output directory.

Optional limit parameters for small real smoke runs:

- `--max-model-len 512`: reduce context allocation for a short prompt.
- `--gpu-memory-utilization 0.25`: reserve a smaller fraction of one GPU for smoke testing.
- `--enforce-eager`: disable CUDA graph/compile capture when diagnosing startup issues.
- `--dtype auto`: keep dtype explicit while allowing vLLM to choose a supported type.
- `--report-model-name NAME`: use a display name in saved reports when the actual model argument is a private path.

These parameters are for bounded validation, not production defaults. For real production sizing, restore the target context length and memory/concurrency settings before benchmarking.

## Output Inspection

For each `RequestOutput`, inspect:

- `prompt`
- `outputs[0].text`
- `outputs[0].token_ids` when token counts matter
- finish reason if exposed by the installed version

If generation is empty, check max tokens, stop strings, chat template, tokenizer mismatch, and model-specific generation config.
