# Fault Tolerance And Reproducibility Troubleshooting

## Health Check Fails During First Rollout

Increase:

```bash
--rollout-health-check-first-wait
```

Large MoE or deepgemm paths can compile before responding.

## Resume Starts From Reference Model

The `--load` directory likely lacks `latest_checkpointed_iteration.txt`. Point to checkpoint root, not `iter_xxx`.

## Determinism Still Differs

Distributed RL can still diverge due to reductions, routing, sampling, and dynamic batching. Deterministic flags reduce variance but do not guarantee identical full training curves across every hardware/software combination.
