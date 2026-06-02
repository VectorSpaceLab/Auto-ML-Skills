# Troubleshooting

## Troubleshooting

- `Undefined dataset`: the `dataset` name is missing from `dataset_dir/dataset_info.json`.
- `Cannot find valid samples`: validate the dataset mapping; wrong column/tag names commonly drop every row.
- Cache is stale: remove `tokenized_path` and rerun after changing template, cutoff, packing, or source data.
- `streaming` with `tokenized_path`: LLaMA-Factory rejects saving tokenized data while streaming; turn streaming off.
- DPO preprocessing: LLaMA-Factory internally uses the pairwise RM processor, so registered DPO datasets must be `ranking: true`.

## General Checks

- Run the root environment check from the installed public package environment before using `llamafactory-dataset-preprocess-skill`.
- Validate user data and generated config files before launching a full run.
- Keep a one-sample or one-step smoke result beside the final run artifacts.
- Do not depend on private source checkout paths; use installed package CLIs/APIs and bundled scripts in this sub-skill.

