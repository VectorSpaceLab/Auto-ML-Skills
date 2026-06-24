# Troubleshooting

## Common Failures

- DeepSpeed missing: install benchmark/profiling dependencies or use `estimate_mfu.py`.
- Benchmark OOM: lower `batch_size`, `seq_length`, or DeepSpeed stage.
- `length-cdf` slow on large datasets: sample or preprocess smaller splits first.
- MFU unsupported GPU name: pass measured peak TFLOPS to `estimate_mfu.py`.

## General Checks

- Run the root environment check from the installed public package environment before using `llamafactory-benchmark-stats-skill`.
- Validate user data and generated config files before launching a full run.
- Keep a one-sample or one-step smoke result beside the final run artifacts.
- Do not depend on private source checkout paths; use installed package CLIs/APIs and bundled scripts in this sub-skill.

