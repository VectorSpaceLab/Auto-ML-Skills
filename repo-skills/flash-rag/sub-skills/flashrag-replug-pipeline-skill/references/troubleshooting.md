# Troubleshooting

## Common Failures

- Retriever returns docs but no scores: use a retriever backend that implements score return or adapt score defaults deliberately.
- Generator cannot accept logits processor: use a compatible HF-like model path.
- Slow generation: lower `retrieval_topk` first because every document creates another prompt.

## General Checks

- Run the root environment check from the installed public package environment before using `flashrag-replug-pipeline-skill`.
- Validate user data and generated config files before launching a full run.
- Keep a one-sample or one-step smoke result beside the final run artifacts.
- Do not depend on private source checkout paths; use installed package CLIs/APIs and bundled scripts in this sub-skill.

