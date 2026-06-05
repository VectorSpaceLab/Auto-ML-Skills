---
name: vllm-observability-troubleshooting
description: "Use when a user wants vLLM environment checks, package/API inspection, collect-env output, health/metrics/log troubleshooting, install errors, CUDA/ROCm issues, model-loading failures, or serving diagnostics."
disable-model-invocation: true
---

# vLLM Observability And Troubleshooting

Use this sub-skill for diagnostics before or after vLLM workflows fail.

## Short Workflow

1. Capture environment with root `../../scripts/check_env.py --json` and this sub-skill's report script.
2. Read [references/workflows.md](references/workflows.md) for triage order.
3. Read [references/troubleshooting-playbook.md](references/troubleshooting-playbook.md) for failure-specific checks.
4. Collect server logs, `/health`, `/metrics`, `/v1/models`, command lines, configs, and minimal reproduction inputs.
5. Reduce to a small public model and minimal args, then add features back one at a time.

## Bundled Scripts

- [scripts/check_env.py](scripts/check_env.py): wrapper around root environment checks with optional `vllm collect-env`.
- [scripts/collect_report.py](scripts/collect_report.py): writes a diagnostic report bundle skeleton.

## References

- [references/workflows.md](references/workflows.md): diagnostic workflow and artifact capture.
- [references/troubleshooting-playbook.md](references/troubleshooting-playbook.md): install, GPU, model, server, endpoint, benchmark, and distributed failures.

## Boundaries

After isolating the problem, return to the relevant workflow sub-skill for the actual fix or rerun.
