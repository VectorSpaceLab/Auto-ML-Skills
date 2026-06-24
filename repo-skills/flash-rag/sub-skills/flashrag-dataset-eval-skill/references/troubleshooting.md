# Troubleshooting

## Troubleshooting

- `Dataset file ... not found`: FlashRAG expects `data_dir/dataset_name/<split>.jsonl`; regenerate config with the parent `data_dir`.
- All metric scores are zero: check prediction text normalization and whether `golden_answers` is a non-empty list.
- `rouge` import error: remove rouge metrics or install `rouge`/`rouge-chinese`.
- `nltk` import warning in `check_env.py`: `em/f1/acc/precision/recall` do not need it, but install `nltk` before using metrics or preprocessing paths that tokenize with NLTK.

## General Checks

- Run the root environment check from the installed public package environment before using `flashrag-dataset-eval-skill`.
- Validate user data and generated config files before launching a full run.
- Keep a one-sample or one-step smoke result beside the final run artifacts.
- Do not depend on private source checkout paths; use installed package CLIs/APIs and bundled scripts in this sub-skill.

