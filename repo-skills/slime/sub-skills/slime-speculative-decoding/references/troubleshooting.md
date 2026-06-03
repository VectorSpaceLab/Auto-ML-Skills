# Speculative Decoding Troubleshooting

| Symptom | Likely cause | Action |
| --- | --- | --- |
| SGLang startup rejects flags | SGLang version lacks the selected speculative option | Run without speculative flags or upgrade the runtime |
| No speedup or slowdown | Draft acceptance too low or prompt shape is prefill-bound | Reduce draft tokens, disable speculative decoding, or try online MTP |
| Missing MTP weights | Checkpoint converted without `--mtp-num-layers` | Reconvert with matching MTP layer count |
| RL loss changes unexpectedly | MTP loss weight too high or baseline unstable | Lower `--mtp-loss-scaling-factor` and compare against non-speculative tiny run |
| OOM after enabling speculative decoding | Extra draft state increases memory | Lower SGLang memory fraction, batch size, or draft tokens |

Do not assume speculative decoding is always faster. Keep a non-speculative baseline command for rollback.
