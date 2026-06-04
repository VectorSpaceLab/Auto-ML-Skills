# Megatron-Core Troubleshooting

| Symptom | Likely cause | Action |
| --- | --- | --- |
| Parallel-size assertion | TP/PP/EP product incompatible with GPU count | Recompute data parallel size and adjust factors |
| Sequence parallel failure | Enabled without compatible tensor parallelism | Disable `sequence_parallel` or increase TP |
| MoE all-to-all error | Expert parallelism or dispatcher unsupported | Reduce EP, change dispatcher, or smoke-test non-MoE config |
| OOM before first step | Cutoff, media pixels, or batch too high | Lower `cutoff_len`, media limits, or batch size; enable recompute |
| Slow startup timeout | Large checkpoint or MoE init | Increase timeout and verify storage throughput |

Do not assume a CUDA DeepSpeed config maps directly to MCore fields; keep the generated MCore YAML separate from generic distributed configs.
