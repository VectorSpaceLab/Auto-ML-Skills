# Troubleshooting

## Common Failures

- Real judger is missing: run fake smoke first; then install/configure the judger model.
- Adaptive route `C` fails: multi-hop routes use IRCOT-style logic and need a generator/retriever pair that supports iterative calls.
- Evaluation metrics fail on custom outputs: inspect `intermediate_data.json` before changing the pipeline.

## General Checks

- Run the root environment check from the installed public package environment before using `flashrag-conditional-pipeline-skill`.
- Validate user data and generated config files before launching a full run.
- Keep a one-sample or one-step smoke result beside the final run artifacts.
- Do not depend on private source checkout paths; use installed package CLIs/APIs and bundled scripts in this sub-skill.

