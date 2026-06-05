# Engine And Serve Args Reference

## Common Args

- `model`: public model ID or user-provided path.
- `served-model-name`: alias shown to clients and accepted in request `model`.
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
- `trust-remote-code`: use only when model requires it and the user accepts remote code risk.

## Quantization

vLLM supports multiple quantization ecosystems depending on installed version and platform, including AWQ, GPTQ/GPTQModel, bitsandbytes, GGUF, FP8, torchao, modelopt, INC, Quark, and quantized KV cache. Always pair `--quantization` with a compatible model artifact.

## Pitfalls

- TP size must not exceed visible GPU count.
- Some models require `trust_remote_code`; do not set it silently.
- Reducing `max-model-len` can make long prompts fail.
- Chat template mismatches can look like model quality problems.
- CLI and YAML key spelling uses long option names without leading dashes.
