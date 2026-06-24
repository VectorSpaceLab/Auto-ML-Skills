# SGLang Deployment Configuration

## Default Managed Engines

```bash
--rollout-num-gpus 8
--rollout-num-gpus-per-engine 2
--sglang-mem-fraction-static 0.7
--sglang-context-length 32768
```

SGLang flags are passed through by prefixing the native SGLang option with `--sglang-`.

Examples:

- SGLang `--mem-fraction-static` becomes `--sglang-mem-fraction-static`.
- SGLang `--context-length` becomes `--sglang-context-length`.
- SGLang `--enable-dp-attention` becomes `--sglang-enable-dp-attention`.

## Router Flags

Router flags use `--router-*`.

```bash
--router-policy cache_aware
--router-balance-abs-threshold 10
```

For multi-turn agents that need session affinity:

```bash
--router-policy consistent_hashing
```

## External Engines

Use external engines when SGLang servers are pre-deployed:

```bash
--rollout-external
--rollout-external-engine-addrs host1:10090 host2:10091
```

Do not combine with `--sglang-config`.
