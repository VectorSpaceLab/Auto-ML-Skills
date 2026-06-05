# Offline Runtime Reference

## Public API Surface

Installed package inspection confirmed these top-level symbols: `Runtime`, `Engine`, `RuntimeEndpoint(base_url, api_key=None, verify=None, chat_template_name=None)`, `set_default_backend(backend)`, `function(func=None, num_api_spec_tokens=None)`, `system`, `user`, `assistant`, `gen`, `select`, `image`, `video`, and `flush_cache`.

`sgl.gen` accepts generation controls including `max_tokens`, `min_tokens`, `n`, `stop`, `stop_token_ids`, `stop_regex`, `temperature`, `top_p`, `top_k`, `min_p`, frequency/presence penalties, logprob flags, `dtype`, `choices`, `regex`, and `json_schema`.

## Language Frontend Pattern

```python
import sglang as sgl

@sgl.function
def answer(s, question):
    s += sgl.system("You answer concisely.")
    s += sgl.user(question)
    s += sgl.assistant(sgl.gen("answer", max_tokens=64, temperature=0.0))

backend = sgl.RuntimeEndpoint("http://127.0.0.1:30000")
sgl.set_default_backend(backend)
state = answer.run("What is SGLang?", max_new_tokens=64)
print(state["answer"])
```

Notes:

- `RuntimeEndpoint` calls `/get_model_info` during construction, so the server must already be up.
- `flush_cache()` is available for server-backed runtime cleanup.
- Frontend `max_tokens` maps into runtime sampling; native HTTP uses `max_new_tokens`.

## Native `/generate` Payload

```json
{
  "text": "Write one sentence about prefix caching.",
  "sampling_params": {
    "max_new_tokens": 32,
    "temperature": 0.0,
    "top_p": 1.0
  },
  "stream": false
}
```

Useful request fields include `text`, `input_ids`, `input_embeds`, `image_data`, `audio_data`, `video_data`, `sampling_params`, `rid`, logprob controls, `stream`, `lora_path`, `custom_logit_processor`, `return_hidden_states`, `return_routed_experts`, PD bootstrap fields, and routed data-parallel rank fields.

`Engine.generate(...)` mirrors the native request surface for offline Python. It accepts `prompt` or `input_ids`, `sampling_params`, multimodal fields, logprob controls, LoRA, custom logit processors, hidden states, routed experts, streaming, PD bootstrap fields, and routing rank overrides.

Minimal offline Engine smoke:

```python
import sglang as sgl

engine = sgl.Engine(model_path="<MODEL_ID>", context_length=512, mem_fraction_static=0.25)
try:
    out = engine.generate(
        prompt="Reply with OK.",
        sampling_params={"max_new_tokens": 4, "temperature": 0.0},
    )
    print(out)
finally:
    engine.shutdown()
```

The bundled `scripts/run_offline_smoke.py` exposes the same guardrails for a real smoke: `--max-new-tokens` defaults to 4, `--context-length` defaults to 512, `--mem-fraction-static` defaults to 0.25, `--report-model-name` lets reports print a safe label instead of echoing a local model path, and `--out` saves the JSON report. `--dry-run` and `--help` do not import SGLang or load a model.

Native chat is not a separate SGLang HTTP route in this skill. Use language frontend role helpers (`sgl.system`, `sgl.user`, `sgl.assistant`) for offline chat-shaped prompts, `/v1/chat/completions` for OpenAI-compatible chat, and `/api/chat` for Ollama-compatible chat.

## Sampling Parameters

Core native sampling params:

- Length/stops: `max_new_tokens`, `min_new_tokens`, `stop`, `stop_token_ids`, `stop_regex`.
- Randomness: `temperature`, `top_p`, `top_k`, `min_p`.
- Penalties: `frequency_penalty`, `presence_penalty`, `repetition_penalty`.
- Multiplicity/logprobs: `n`, `return_logprob`, `logprob_start_len`, `top_logprobs_num`, `token_ids_logprob`, `return_text_in_logprobs`.
- Constraints: `json_schema`, `regex`, `ebnf`, `structural_tag`.
- Output handling: `ignore_eos`, `skip_special_tokens`, `spaces_between_special_tokens`, `no_stop_trim`, `stream_interval`, `sampling_seed`, `logit_bias`.

`temperature=0` is normalized to greedy behavior internally. Only one of `regex`, `json_schema`, or `ebnf` can be set.

## Offline Engine Guidance

The examples describe an Engine API for batch inference, embeddings, VLM, hidden states, speculative decoding, torchrun, and custom servers. When writing public instructions:

- Keep model IDs symbolic unless the user gives hardware.
- Use batch examples for throughput, not for single prompt correctness checks.
- State that hidden states can reduce throughput and may rebuild CUDA graphs.
- For speculative offline inference, route cache/performance tuning questions to `sglang-cache-performance`.
- For language frontend programs with remote servers, use `RuntimeEndpoint`; for local smoke without HTTP, use `Engine` directly.
