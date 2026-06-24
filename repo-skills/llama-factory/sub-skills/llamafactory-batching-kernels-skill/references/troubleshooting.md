# Batching And Kernel Troubleshooting

| Symptom | Likely cause | Action |
| --- | --- | --- |
| Loss changes dramatically after enabling an optimization | Masking, packing, or padding-free mismatch | Re-run a tiny deterministic sample and compare tokenization/loss masks |
| Kernel import error | Liger or backend package missing | Disable kernel switch or install the matching package |
| Attention shape error | Long-context/context-parallel incompatibility | Reduce context parallelism or return to standard attention |
| OOM despite fewer padded tokens | Effective token budget still too high | Lower cutoff, batch size, or max tokens per device |
| Dataloader stalls | Dynamic batching worker pressure | Lower workers and inspect sequence length distribution |

Do not enable every performance switch at once on a new model. Add one, smoke-test, then scale.
