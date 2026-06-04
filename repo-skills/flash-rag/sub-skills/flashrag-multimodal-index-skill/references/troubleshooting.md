# Troubleshooting

## Common Failures

- Missing CLIP model path: use fake smoke or BM25 first.
- Image paths are relative to the wrong root: normalize paths before indexing.
- Parquet data: validate with a small JSONL export first, then run the real FlashRAG index builder on the original data.

## General Checks

- Run the root environment check from the installed public package environment before using `flashrag-multimodal-index-skill`.
- Validate user data and generated config files before launching a full run.
- Keep a one-sample or one-step smoke result beside the final run artifacts.
- Do not depend on private source checkout paths; use installed package CLIs/APIs and bundled scripts in this sub-skill.

