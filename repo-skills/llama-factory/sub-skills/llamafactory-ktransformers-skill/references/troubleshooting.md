# KTransformers Troubleshooting

| Symptom | Likely cause | Action |
| --- | --- | --- |
| `use_kt` ignored | Installed package lacks KT integration | Confirm LLaMA-Factory and KTransformers versions before training |
| Missing converted weights | `AMXINT8`/`AMXINT4` selected without `kt_weight_path` | Use `AMXBF16` or provide converted expert weights |
| LoRA rank mismatch | `kt_config.lora_rank` differs from YAML `lora_rank` | Keep both values identical |
| CPU saturation | `kt_num_threads` too high or low for host | Tune threads and thread pools before scaling GPUs |
| FSDP wrap errors | Accelerate config not FSDP2-compatible | Use FSDP2 with transformer-based wrapping and full state dict |

KT jobs are sensitive to model family and backend support. Smoke-test a short run before launching a long MoE job.
