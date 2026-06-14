# vLLM Reference

Read this for TRL workflows that use vLLM.

## Install And Verify

```bash
pip install "trl[vllm]"
python - <<'PY'
import vllm
print(vllm.__version__)
PY
trl vllm-serve --help
```

vLLM support requires backend compatibility beyond normal TRL importability. Verify GPU visibility and CUDA/PyTorch compatibility if the user expects GPU serving.

## `trl vllm-serve`

Core command:

```bash
trl vllm-serve --model <model_name_or_path>
```

Important flags:

- `--model`: required model name or local path.
- `--revision`: model revision.
- `--tensor_parallel_size` / `--tensor-parallel-size`: tensor parallel workers.
- `--data_parallel_size` / `--data-parallel-size`: data parallel workers. For dense models, keep this at `1` unless the installed vLLM version and model support more.
- `--host`, `--port`: server binding.
- `--gpu_memory_utilization`: fraction of GPU memory for model weights, activations, and KV cache.
- `--dtype`: vLLM dtype, often `auto`.
- `--max_model_len`: cap context length when KV cache would otherwise be too large.
- `--enable_prefix_caching`, `--enforce_eager`, `--kv_cache_dtype`.
- `--trust_remote_code`: required for some custom models but executes model-repo code.
- `--vllm_model_impl`: `vllm` or `transformers`.
- `--distributed_executor_backend`: set to `ray` for multi-node tensor parallel workers when required.

## Trainer Integration

GRPO and RLOO configs expose vLLM controls:

```python
GRPOConfig(
    use_vllm=True,
    vllm_mode="colocate",
    vllm_gpu_memory_utilization=0.3,
)
```

```python
GRPOConfig(
    use_vllm=True,
    vllm_mode="server",
    vllm_server_base_url="http://localhost:8000",
    vllm_server_timeout=240.0,
)
```

Relevant fields include:

- `vllm_mode`: `colocate` or `server`.
- `vllm_server_base_url`, `vllm_server_host`, `vllm_server_port`, `vllm_server_timeout`.
- `vllm_gpu_memory_utilization`, `vllm_max_model_length`, `vllm_tensor_parallel_size`.
- `vllm_model_impl`, `vllm_enable_sleep_mode`, structured-output regex.
- `vllm_importance_sampling_correction`, `vllm_importance_sampling_mode`, and `vllm_importance_sampling_cap` for generation/training mismatch correction.

## Debugging

Server unreachable:
Check host/port, firewall/container networking, and that `trl vllm-serve` is still running. Use a short HTTP health or generation request only if the server API is available and the user expects it.

OOM on server start:
Lower `--gpu_memory_utilization`, set `--max_model_len`, reduce tensor parallelism mismatch, or use a smaller model/dtype.

OOM during colocate generation:
Lower trainer batch size, `num_generations`, `max_completion_length`, `generation_batch_size`, or `vllm_gpu_memory_utilization`.

Backend import failure:
Verify vLLM wheel, PyTorch CUDA, Python version, GPU architecture, and driver. Normal TRL training may still work without vLLM.
