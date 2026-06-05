# Troubleshooting Playbook

## Install And Import

- Check Python version and `vllm` distribution version.
- Check PyTorch and accelerator wheel compatibility.
- Use `check_env.py` before heavy imports.

## GPU And Memory

- Confirm visible devices and driver.
- Reduce `max-model-len` and request `max_tokens`.
- Lower concurrency and GPU memory utilization if co-located.

## Serving

- Probe `/health` before endpoint calls.
- Probe `/v1/models` to confirm served model alias.
- Match request `model` to served alias or LoRA adapter name.
- Inspect 422 responses for schema issues.

## Distributed

- Verify package versions on every node.
- Confirm NCCL interface and ports.
- Check Ray address and object store capacity.

## Benchmarks

- Inspect failed request count.
- Warm server before measuring steady state.
- Keep client host close to server or record network effects.
