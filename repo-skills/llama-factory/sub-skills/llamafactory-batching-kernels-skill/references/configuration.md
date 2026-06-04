# Batching And Kernel Configuration

Read this when optimizing LLaMA-Factory throughput after a baseline config already trains.

## Optimization Families

| Family | Typical use | Notes |
| --- | --- | --- |
| Dynamic batching | Variable-length datasets where fixed padding wastes compute | Watch max tokens per device and dataloader behavior |
| Padding-free training | Reduces padding overhead for full/FSDP2 training | Validate attention/backend support before scaling |
| Liger kernel | Faster supported transformer kernels | Requires compatible model, torch, and kernel package |
| Ulysses context parallelism | Long-context full training | Requires multi-GPU sizing and compatible attention path |

## Practical Order

1. Prove the base config trains for a few steps.
2. Enable one optimization and keep `max_steps` small.
3. Compare first-step loss and throughput to the base run.
4. Combine optimizations only after separate smoke tests pass.

## Config Snippets

Use the bundled script to generate snippets instead of copying source examples:

```bash
python scripts/make_perf_config.py --feature dynamic-batching
python scripts/make_perf_config.py --feature padding-free
python scripts/make_perf_config.py --feature liger
python scripts/make_perf_config.py --feature ulysses --context-parallel-size 2
```

Keep snippets close to the user's run config so the applied performance switches are auditable.
