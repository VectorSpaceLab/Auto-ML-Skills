# Language Model Evaluation Workflows

## When To Read

LLM benchmark configuration, evaluation harness runs, OpenCompass configs, task authoring, model backends, result summaries, decontamination, and judge-based evaluation.

## Repo Skill Options

<!-- DISCO_SCENARIO:language-model-evaluation-workflows:START -->
### `evaluate`

Role: Use Hugging Face Evaluate to load metrics, comparisons, and measurements; compute and combine results; run evaluator pipelines; create custom modules; troubleshoot optional dependencies, cache, Hub, and CLI workflows.
Read when: The request names `evaluate` or asks for package-specific APIs, CLIs, configs, data/model artifacts, error messages, workflows, or repository maintenance that match this project.
Best for: evaluator pipelines, hub and cli, module computation, and module loading.
Avoid when: another repo skill in this scenario matches the user's task, package, model family, data format, serving backend, or workflow more directly.
Useful entry points: `evaluate/SKILL.md`, `evaluate/sub-skills/evaluator-pipelines/`, `evaluate/sub-skills/hub-and-cli/`, `evaluate/sub-skills/module-computation/`, `evaluate/sub-skills/module-loading/`.

### `lm-evaluation-harness`

Role: Use EleutherAI LM Evaluation Harness for language-model evaluation runs, YAML task authoring, model backend setup, result logging, decontamination hygiene, and maintainer workflows.
Read when: The request names `lm-evaluation-harness` or asks for package-specific APIs, CLIs, configs, data/model artifacts, error messages, workflows, or repository maintenance that match this project.
Best for: decontamination maintenance, evaluation runs, model backends, result logging, and task authoring.
Avoid when: another repo skill in this scenario matches the user's task, package, model family, data format, serving backend, or workflow more directly.
Useful entry points: `lm-evaluation-harness/SKILL.md`, `lm-evaluation-harness/sub-skills/decontamination-maintenance/`, `lm-evaluation-harness/sub-skills/evaluation-runs/`, `lm-evaluation-harness/sub-skills/model-backends/`, `lm-evaluation-harness/sub-skills/result-logging/`, `lm-evaluation-harness/sub-skills/task-authoring/`.

### `opencompass`

Role: Use OpenCompass to configure, run, debug, and analyze large-model evaluations across CLI/config workflows, datasets, model backends, prompts, inferencers, summarizers, and LLM-as-judge results.
Read when: The request names `opencompass` or asks for package-specific APIs, CLIs, configs, data/model artifacts, error messages, workflows, or repository maintenance that match this project.
Best for: configuration and datasets, evaluation workflows, model backends, prompt and inference, and results and analysis.
Avoid when: another repo skill in this scenario matches the user's task, package, model family, data format, serving backend, or workflow more directly.
Useful entry points: `opencompass/SKILL.md`, `opencompass/sub-skills/configuration-and-datasets/`, `opencompass/sub-skills/evaluation-workflows/`, `opencompass/sub-skills/model-backends/`, `opencompass/sub-skills/prompt-and-inference/`, `opencompass/sub-skills/results-and-analysis/`.

### `torchtune`

Role: Guides torchtune's `eleuther_eval` recipe, evaluation config changes, optional `lm_eval` dependency, and checkpoint compatibility.
Read when: The request mentions torchtune Eleuther evaluation, `eleuther_evaluation`, `lm_eval`, task lists, `truthfulqa_mc2`, or evaluating a torchtune checkpoint.
Best for: Planning torchtune evaluation commands and config edits after a compatible checkpoint/tokenizer exists.
Avoid when: The request is about writing custom Eleuther tasks or using lm-evaluation-harness directly outside torchtune.
Useful entry points: `torchtune/sub-skills/inference-evaluation-quantization/SKILL.md`, `torchtune/sub-skills/cli-and-config/SKILL.md`.

<!-- DISCO_SCENARIO:language-model-evaluation-workflows:END -->

## How To Choose

Choose by benchmark framework: lm-evaluation-harness for EleutherAI harness tasks, OpenCompass for OpenCompass configs/backends, and Evaluate for metric modules or evaluator utilities. Choose `evaluate` when the request names `evaluate`, centers on Use Hugging Face Evaluate to load metrics, comparisons, and measurements; compute and combine results; run evaluator pipelines; create custom modules; troubleshoot optional dependencies, cache, Hub, and CLI workflows, uses its APIs or CLIs, references its configs/artifacts/errors, or asks for repository workflows in language model evaluation workflows. Choose `lm-evaluation-harness` when the request names `lm-evaluation-harness`, centers on language-model evaluation runs, YAML task authoring, model backend setup, result logging, decontamination hygiene, and maintainer workflows, uses its APIs or CLIs, references its configs/artifacts/errors, or asks for repository workflows in language model evaluation workflows. Choose `opencompass` when the request names `opencompass`, centers on Use OpenCompass to configure, run, debugging, and analyze large-model evaluations across CLI/config workflows, datasets, model backends, prompts, inferencers, summarizers, and LLM-as-judge results, uses its APIs or CLIs, references its configs/artifacts/errors, or asks for repository workflows in language model evaluation workflows.
