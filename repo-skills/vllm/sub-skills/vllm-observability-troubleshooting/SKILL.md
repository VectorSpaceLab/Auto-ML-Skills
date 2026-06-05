---
name: vllm-observability-troubleshooting
description: "Use when a user wants vLLM environment checks, package/API inspection, collect-env output, health/metrics/log troubleshooting, install errors, CUDA/ROCm issues, model-loading failures, or serving diagnostics."
disable-model-invocation: true
---

# vLLM Observability And Troubleshooting

Use this sub-skill for diagnostics before or after vLLM workflows fail. Start here when the problem is not yet clearly offline inference, server lifecycle, LoRA, distributed serving, or a benchmark comparison.

## Use When

- The user reports install/import failures, CUDA/ROCm errors, model-loading failures, health-check failures, endpoint errors, OOM, or unexpected slowdowns.
- The user needs `vllm collect-env`, package/API inspection, `/health`, `/metrics`, logs, or a diagnostic bundle.
- The user asks for a safe debugging sequence on a shared machine.
- A generated command fails and the root cause is not obvious.

## Inputs To Collect

- Exact command, full traceback/log tail, package version, torch version, Python version, platform, GPU visibility, model ID, and config.
- Whether the issue reproduces with a small public model and minimal args.
- Server logs, client request/response, metrics, and whether any process is still running.

## Short Workflow

1. Capture environment with root `../../scripts/check_env.py --json` and this sub-skill's report script.
2. Read [references/workflows.md](references/workflows.md) for triage order.
3. Read [references/troubleshooting-playbook.md](references/troubleshooting-playbook.md) for failure-specific checks.
4. Collect server logs, `/health`, `/metrics`, `/v1/models`, command lines, configs, and minimal reproduction inputs.
5. Reduce to a small public model and minimal args, then add features back one at a time.
6. Separate import-only validation from real model-load and request validation in the report.

## Bundled Scripts

- [scripts/check_env.py](scripts/check_env.py): wrapper around root environment checks with optional `vllm collect-env`.
- [scripts/collect_report.py](scripts/collect_report.py): writes a diagnostic report bundle skeleton.

## References

- [references/workflows.md](references/workflows.md): diagnostic workflow and artifact capture.
- [references/troubleshooting-playbook.md](references/troubleshooting-playbook.md): install, GPU, model, server, endpoint, benchmark, and distributed failures.

## Boundaries

After isolating the problem, return to the relevant workflow sub-skill for the actual fix or rerun.

## Verification Notes

- The diagnostic scripts are safe for static checks and do not require a model unless explicitly requested.
- A real recovery should end with import, server/offline smoke, and cleanup evidence.
- Do not paste private paths, tokens, or model cache locations into public reusable skill docs.
