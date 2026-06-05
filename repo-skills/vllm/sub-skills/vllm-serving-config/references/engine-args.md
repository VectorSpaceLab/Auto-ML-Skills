# Engine And Serve Args Reference

## Common Args

- `model`: public model ID or user-provided path.
- `served-model-name`: alias shown to clients and accepted in request `model`.
- `tokenizer`: tokenizer ID/path when it intentionally differs from the model.
- `host`, `port`: bind interface. Prefer `127.0.0.1` for smoke.
- `dtype`: start with `auto`.
- `max-model-len`: reduce for memory-bound smoke tests.
- `gpu-memory-utilization`: fraction of GPU memory reserved by vLLM; lower when co-locating workloads.
- `tensor-parallel-size`: split model across GPUs.
- `pipeline-parallel-size`: pipeline model stages.
- `data-parallel-size`: replicas/data parallel where supported.
- `quantization`: only with compatible model/backend.
- `generation-config`: use `vllm` for deterministic skill smoke behavior.
- `chat-template`: override tokenizer chat template.
- `chat-template-content-format`: force `string` or OpenAI-style list content when auto-detection is wrong.
- `trust-remote-code`: use only when model requires it and the user accepts remote code risk.

## Quantization

vLLM supports multiple quantization ecosystems depending on installed version and platform, including AWQ, GPTQ/GPTQModel, bitsandbytes, GGUF, FP8, MXFP8/MXFP4, NVFP4, INT8, INT4, compressed-tensors, modelopt, torchao, INC, Quark, and quantized KV cache. Always pair `--quantization` with a compatible model artifact.

Weight quantization and KV cache quantization are separate:

- Weight/artifact quantization: `--quantization`.
- KV cache quantization: `--kv-cache-dtype` and possibly `--calculate-kv-scales`.

## Serving Feature Flags

- Tool calling: `--enable-auto-tool-choice --tool-call-parser PARSER`.
- Reasoning: `--reasoning-parser PARSER`.
- Responses API uses the same served model alias as chat/completions.
- Prefix caching: `--enable-prefix-caching`.
- Speculative decoding: `--speculative-config` or `--spec-model/--spec-method/--spec-tokens`.
- Disaggregated prefill/KV transfer: `--kv-transfer-config`.
- DBO: `--enable-dbo` plus optional threshold flags.

## Pitfalls

- TP size must not exceed visible GPU count.
- Some models require `trust_remote_code`; do not set it silently.
- Reducing `max-model-len` can make long prompts fail.
- Chat template mismatches can look like model quality problems.
- CLI and YAML key spelling uses long option names without leading dashes.
