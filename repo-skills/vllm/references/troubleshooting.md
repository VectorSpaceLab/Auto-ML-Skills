# vLLM Troubleshooting Reference

## Triage Order

1. Run `python scripts/check_env.py --json`.
2. Run `python scripts/inspect_api.py --json` if API names or schemas are uncertain.
3. Confirm accelerator visibility: `nvidia-smi`, `rocm-smi`, or platform-specific equivalent.
4. Confirm model access and cache location.
5. Reproduce with a small public model and minimal args.
6. Add back tensor parallelism, quantization, LoRA, structured outputs, or multimodal features one at a time.

## Common Failures

- Import fails: incompatible Python, PyTorch, CUDA/ROCm wheel, missing shared library, or wrong accelerator package.
- CLI help hangs or is slow: heavy imports and platform probing. Use metadata checks first and apply timeouts.
- OOM at startup: reduce `--max-model-len`, reduce `--gpu-memory-utilization`, use quantized weights, reduce parallel replicas, or use a smaller model.
- OOM during requests: reduce `max_tokens`, batch/concurrency, context length, or KV cache pressure.
- HTTP 401/403 for model load: gated Hugging Face model or missing token.
- Chat output is malformed: wrong or missing chat template; use `llm.chat` or set `--chat-template`.
- Structured output fails: schema too complex, unsupported backend, insufficient `max_tokens`, or unsupported parameter name for this version.
- Embedding endpoint returns generation-shaped output: wrong model runner or endpoint.
- LoRA request ignored: server missing `--enable-lora`, adapter name mismatch, adapter rank exceeds configured maximum, or runtime updates disabled.
- Ray/multi-node errors: port/firewall/NCCL interface mismatch, missing password/address, inconsistent package versions, or object store pressure.
- Benchmark result has failed requests: server not warm, wrong endpoint type, overloaded request rate, or model ID mismatch.

## Server Debugging

Use a free localhost port for smoke:

```bash
vllm serve Qwen/Qwen3-0.6B --host 127.0.0.1 --port 8000 --generation-config vllm
curl -fsS http://127.0.0.1:8000/health
curl -fsS http://127.0.0.1:8000/v1/models
```

Keep logs:

```bash
mkdir -p run
vllm serve ... > run/server.log 2>&1 &
echo $! > run/server.pid
```

Shutdown:

```bash
kill "$(cat run/server.pid)"
```

## Environment Variables Worth Checking

- `CUDA_VISIBLE_DEVICES`
- `HIP_VISIBLE_DEVICES`
- `VLLM_USE_MODELSCOPE`
- `VLLM_API_KEY`
- `VLLM_ALLOW_RUNTIME_LORA_UPDATING`
- `HF_HOME`, `HF_TOKEN`, `TRANSFORMERS_CACHE`
- NCCL variables such as `NCCL_SOCKET_IFNAME`, `NCCL_DEBUG`

Do not blindly set many environment variables. Change one variable at a time and record why.
