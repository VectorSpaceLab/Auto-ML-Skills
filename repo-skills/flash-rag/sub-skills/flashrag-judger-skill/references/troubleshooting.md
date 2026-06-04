# Troubleshooting

## Common Failures

- SKR training data is too imbalanced: inspect label counts and add examples.
- FAISS/encoder dependencies missing: fake smoke can still validate route logic; real SKR needs encoder and FAISS.
- Adaptive model unavailable: preflight should warn; provide a local seq2seq classifier path for real runs.

## General Checks

- Run the root environment check from the installed public package environment before using `flashrag-judger-skill`.
- Validate user data and generated config files before launching a full run.
- Keep a one-sample or one-step smoke result beside the final run artifacts.
- Do not depend on private source checkout paths; use installed package CLIs/APIs and bundled scripts in this sub-skill.

