# Troubleshooting

## Common Failures

- Missing `image` column: use no-ret text-only smoke or provide image paths/base64 depending on the dataset.
- CLIP index path missing: run corpus/index creation first or use BM25-only `perform_modality text`.
- Real VLM OOM: reduce `generator_batch_size`, `test_sample_num`, and image resolution; keep smoke outputs unchanged for debugging.

## General Checks

- Run the root environment check from the installed public package environment before using `flashrag-multimodal-pipeline-skill`.
- Validate user data and generated config files before launching a full run.
- Keep a one-sample or one-step smoke result beside the final run artifacts.
- Do not depend on private source checkout paths; use installed package CLIs/APIs and bundled scripts in this sub-skill.

