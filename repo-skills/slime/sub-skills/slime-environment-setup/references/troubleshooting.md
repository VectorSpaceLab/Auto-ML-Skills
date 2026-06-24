# Environment Troubleshooting

## `megatron.training` Missing

`megatron-core` can be installed while `megatron.training` is still unavailable. slime's Megatron backend imports `megatron.training.arguments`, so add a full Megatron-LM checkout to `PYTHONPATH`.

## Ray Dashboard URL Hangs

Check:

- Ray head is running on the expected node.
- `--address` points at the same dashboard port.
- GPU resource request matches available resources.
- The runtime env JSON is valid JSON, not shell syntax.

## Ray Socket Path Too Long

If Ray fails before job submission with:

```text
AF_UNIX path length cannot exceed 107 bytes
```

set a short temp directory before starting Ray:

```bash
export RAY_TMPDIR=/tmp/ray
mkdir -p "${RAY_TMPDIR}"
```

Avoid deeply nested temporary directories for Ray sessions.

## SGLang Or Ray Processes From Previous Runs

If a rerun sees stale ports or engine workers:

```bash
ray stop --force || true
pkill -f sglang || true
```

Do not kill arbitrary Python processes on shared systems.

## Docker Update Broke Native Libraries

If a previously working Docker container breaks after `pip install`, rebuild the container or reinstall slime with:

```bash
pip install -e . --no-deps
```

Avoid dependency re-resolution unless you know the CUDA/SGLang/Megatron pins.
