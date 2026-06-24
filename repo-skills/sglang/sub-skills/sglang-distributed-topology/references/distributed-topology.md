# Distributed Topology Reference

## Server Parallelism

Key server args:

- Tensor parallel: `--tp-size` or `--tp`.
- Data parallel: `--dp-size`, `--load-balance-method`.
- Pipeline parallel: `--pp-size`, `--pp-max-micro-batch-size`, `--pp-async-batch-depth`.
- Attention/expert parallel variants: `--attn-cp-size`, `--moe-dp-size`, `--ep-size`/`--expert-parallel-size`, `--moe-a2a-backend`, `--moe-runner-backend`, `--deepep-mode`, and expert placement/rebalance flags.
- Multi-node: `--nnodes`, `--node-rank`, `--dist-init-addr`, `--nccl-port`, `--dist-timeout`.
- Ray: `--use-ray` for selected distributed launches.

Single-node example:

```bash
python -m sglang.launch_server \
  --model-path <MODEL_ID> \
  --host 0.0.0.0 --port 30000 \
  --tp-size 4
```

Two-node pattern:

```bash
# node 0
python -m sglang.launch_server --model-path <MODEL_ID> --tp-size 16 --nnodes 2 --node-rank 0 --dist-init-addr <NODE0_IP>:5000

# node 1
python -m sglang.launch_server --model-path <MODEL_ID> --tp-size 16 --nnodes 2 --node-rank 1 --dist-init-addr <NODE0_IP>:5000
```

Confirm the exact interpretation of `tp_size` against current SGLang release for multi-node; operationally, all nodes must agree on model, tokenizer, and distributed init.

## Expert Parallel / MoE

Use expert parallelism for MoE models, not dense-only models. Common knobs:

- `--ep-size` or `--expert-parallel-size` controls expert parallel degree.
- `--moe-a2a-backend` selects all-to-all transfer backend such as `deepep`, `mooncake`, `nixl`, `mori`, `flashinfer`, or platform-specific choices.
- `--deepep-mode auto|normal|low_latency`: `auto` is the normal serving default; PD deployments often use `normal` for prefill and `low_latency` for decode.
- `--ep-num-redundant-experts`, `--init-expert-location`, `--enable-eplb`, and expert distribution recorder flags support expert load balancing and placement diagnostics.
- Expert distribution record HTTP routes can start, stop, and dump routing statistics; pair them with metrics only for bounded diagnostic windows.

Validate EP arithmetic against TP/DP/PP before launch. Some EP backends require RDMA/NVLink fabric and matching environment variables or device lists.

## Router / Model Gateway

Router argument source exposes:

- Worker selection: `--worker-urls`, `--policy`, `--prefill-policy`, `--decode-policy`, `--balance-abs-threshold`, `--balance-rel-threshold`.
- Service discovery: Kubernetes selectors/namespaces/ports for regular, prefill, and decode workers.
- Reliability: request timeout, retries, circuit breaker, health checks, max concurrent requests, queue size, rate limit.
- Auth/security: API key, control-plane API keys, JWT, TLS/mTLS certificate paths.
- Parsers/templates: `--chat-template`, `--reasoning-parser`, `--tool-call-parser`.
- Metrics/tracing: Prometheus host/port/buckets, OpenTelemetry trace endpoint.
- PD disaggregation: `--pd-disaggregation`, `--prefill URL [BOOTSTRAP_PORT]`, `--decode URL`.

Router direct pattern:

```bash
python -m sglang_router.launch_router \
  --host 0.0.0.0 --port 30080 \
  --worker-urls http://worker-a:30000 http://worker-b:30000 \
  --policy cache_aware
```

PD MiniLB-style pattern:

```bash
python -m sglang_router.launch_router \
  --host 0.0.0.0 --port 30080 \
  --pd-disaggregation \
  --prefill http://prefill-a:30000 8998 \
  --decode http://decode-a:30000
```

## Kubernetes

SGLang includes service/deployment examples for single-node and distributed stateful sets. For a self-contained deployment plan, spell out:

- Image tag and CUDA/platform compatibility.
- GPU resources and shared memory.
- Model cache/token secret handling.
- Service ports for HTTP, distributed init, bootstrap, metrics, and tracing.
- Readiness checks against `/health`.

## Failure Checks

- Mismatched model IDs or tokenizer paths across workers.
- `tp_size * pp_size` exceeding visible GPUs unless multi-node/Ray is configured.
- Router can reach `/health` but worker model route uses a different root path.
- PD prefill/decode ports not mutually reachable.
- EP backend chosen on hardware/fabric that cannot support it.
- Exposed router without auth/rate limit.
