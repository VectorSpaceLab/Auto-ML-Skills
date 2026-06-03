# Coding-Agent RL Troubleshooting

| Symptom | Likely cause | Action |
| --- | --- | --- |
| Agent client cannot connect | Sandbox cannot reach adapter host/port | Use a routable head-node IP and open the port |
| Tool calls are plain text | SGLang tool parser mismatch | Set parser flags for the served model |
| Empty or invalid training samples | Token provenance mismatch or no model output segment | Inspect rollout dump and loss masks |
| Reward always zero | Grader command missing, wrong workdir, or patch not applied | Validate JSONL and run one grading command manually |
| Sandbox boot long-tail blocks training | Too much synchronous rollout variance | Reduce concurrency or route to `slime-fully-async-rollout` |
| Batch size explodes after fan-out | Multiple segments per rollout | Track shared `group_id` and lower rollout batch size |

Always debug one sample end to end before increasing `n_samples_per_prompt`.
