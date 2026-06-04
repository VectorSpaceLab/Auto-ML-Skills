# Troubleshooting

## Common Failures

- Layer-wise GaLore/APOLLO with DDP: disable layer-wise or run single process.
- Missing optimizer package: install the named package in the same environment used by `torchrun`.
- FP8 unsupported device: use bf16 or move to Hopper/compatible hardware and backend.
- Profiler output missing: set `enable_torch_profiler` and inspect `<output_dir>/profiler`.

## General Checks

- Run the root environment check from the installed public package environment before using `llamafactory-training-extensions-skill`.
- Validate user data and generated config files before launching a full run.
- Keep a one-sample or one-step smoke result beside the final run artifacts.
- Do not depend on private source checkout paths; use installed package CLIs/APIs and bundled scripts in this sub-skill.

