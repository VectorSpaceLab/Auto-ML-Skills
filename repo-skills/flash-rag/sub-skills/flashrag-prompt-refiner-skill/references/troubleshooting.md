# Troubleshooting

## Troubleshooting

- `AutoConfig.from_pretrained` is called during prompt rendering: your config is not using `framework: openai`; regenerate with `make_prompt_config.py`.
- `No module named faiss` when importing refiners: use this skill's offline refiner runner or install `faiss-cpu`; FlashRAG's refiner module imports retriever encoder utilities at module import time.
- `No module named langid` when importing refiners: use this skill's offline refiner runner or install `langid`; the source imports retriever utilities even for refiner classes.
- `tiktoken` cannot map the model: set `--generator-model gpt-3.5-turbo`.
- Prompt contains no references: validate the docs file and check `--result-index` when reading BM25 search output.
- Real refiner fails on CPU: several source refiners assume CUDA; use the offline smoke first, then choose a GPU and local model path for the real refiner.
- `spacy.load("en_core_web_lg")` fails for SelectiveContext: install the spaCy model or use another refiner.

## General Checks

- Run the root environment check from the installed public package environment before using `flashrag-prompt-refiner-skill`.
- Validate user data and generated config files before launching a full run.
- Keep a one-sample or one-step smoke result beside the final run artifacts.
- Do not depend on private source checkout paths; use installed package CLIs/APIs and bundled scripts in this sub-skill.

