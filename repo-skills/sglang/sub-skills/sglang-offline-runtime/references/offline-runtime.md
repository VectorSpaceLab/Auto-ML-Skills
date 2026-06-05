# Offline Runtime Reference

## Public API Surface

Installed package inspection confirmed these top-level symbols: `Runtime`, `RuntimeEndpoint(base_url, api_key=None, verify=None, chat_template_name=None)`, `set_default_backend(backend)`, `function(func=None, num_api_spec_tokens=None)`, `system`, `user`, `assistant`, `gen`, `select`, `image`, and `flush_cache`.

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

Useful request fields include `text`, `input_ids`, `input_embeds`, `image_data`, `audio_data`, `sampling_params`, `rid`, logprob controls, `stream`, `lora_path`, `custom_logit_processor`, `return_hidden_states`, and `return_routed_experts`.

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
