# Troubleshooting

## Troubleshooting

- `The current model does not support chat`: ensure `stage: sft`; RM/value-head models are for scoring, not generation.
- Adapter config error: pass the base model in `--model` and the PEFT directory in `--adapter`, or use a merged export as `--model`.
- `vLLM not install` or `SGLang not install`: switch to `--backend huggingface`.
- `No package metadata was found for jieba`: install `jieba nltk rouge-chinese`; LLaMA-Factory checks these when `predict_with_generate` is enabled.
- Empty or repetitive generations: lower `temperature`, set `--do-sample false`, and use a shorter prompt for smoke tests.
- CUDA OOM: choose a free GPU, lower `max_new_tokens`, use a merged model on CPU with `--infer-dtype float32`, or run on a smaller local model.

## General Checks

- Run the root environment check from the installed public package environment before using `llamafactory-inference-skill`.
- Validate user data and generated config files before launching a full run.
- Keep a one-sample or one-step smoke result beside the final run artifacts.
- Do not depend on private source checkout paths; use installed package CLIs/APIs and bundled scripts in this sub-skill.

