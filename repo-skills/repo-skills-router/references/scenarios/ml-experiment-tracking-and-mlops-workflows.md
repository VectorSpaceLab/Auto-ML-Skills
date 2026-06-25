# ML Experiment Tracking and MLOps Workflows

## When To Read

Experiment tracking, AutoML/HPO, model registries, artifacts, sweeps, Launch jobs, MLflow projects/models/evaluation, data versioning pipelines, GenAI observability, local serving, and operational MLOps.

## Repo Skill Options

<!-- SKILLQED_SCENARIO:ml-experiment-tracking-and-mlops-workflows:START -->
### `autogluon`

Role: Provides repo-specific routing and practical API guidance for AutoGluon's tabular, time-series, and multimodal predictor families.
Read when: AutoGluon, autogluon, TabularPredictor, TimeSeriesPredictor, TimeSeriesDataFrame, MultiModalPredictor, AutoMM, presets, leaderboard, feature importance, Chronos, object detection, semantic matching, saved predictor load errors.
Best for: Choosing the right AutoGluon predictor, writing fit/predict/evaluate code, diagnosing package/backend issues, validating input schemas, and handling saved predictor portability.
Avoid when: The user is asking about a different AutoML library, generic scikit-learn modeling with no AutoGluon usage, or production cloud infrastructure unrelated to local AutoGluon APIs.
Useful entry points: `autogluon/SKILL.md`, `autogluon/sub-skills/tabular-ml/SKILL.md`, `autogluon/sub-skills/time-series-forecasting/SKILL.md`, `autogluon/sub-skills/multimodal-automl/SKILL.md`.

### `bentoml`

Role: Use BentoML to author model-serving Services, build and containerize Bentos, run HTTP/gRPC servers and clients, manage models, operate the CLI and BentoCloud, and configure observability or production runtime behavior.
Read when: The request names `bentoml` or asks for package-specific APIs, CLIs, configs, data/model artifacts, error messages, workflows, or repository maintenance that match this project.
Best for: cli and cloud, model management, observability and operations, packaging and containerization, service authoring, and serving and clients.
Avoid when: another repo skill in this scenario matches the user's task, package, model family, data format, serving backend, or workflow more directly.
Useful entry points: `bentoml/SKILL.md`, `bentoml/sub-skills/cli-and-cloud/`, `bentoml/sub-skills/model-management/`, `bentoml/sub-skills/observability-and-operations/`, `bentoml/sub-skills/packaging-and-containerization/`, `bentoml/sub-skills/service-authoring/`, `1 more sub-skills`.

### `dvc`

Role: Provides self-contained DVC CLI/API guidance for data tracking, reproducible pipelines, experiments, remote/cache operations, reporting, and Python access.
Read when: Signals include dvc init/add/stage/repro/status/push/pull/remote/exp/metrics/params/plots, dvc.api, DVCFileSystem, dvc.yaml, dvc.lock, .dvc, DVC cache, remote storage extras, experiment queues, or DVC codebase tests.
Best for: Building or debugging DVC workflows, choosing safe DVC commands, using DVC Python APIs, diagnosing optional remote backend failures, and maintaining the DVC repository with focused tests.
Avoid when: Avoid for generic Git, unrelated ML training frameworks, cloud storage tasks that do not involve DVC, or agent-skill authoring/verification workflows.
Useful entry points: `dvc/SKILL.md`, `dvc/sub-skills/data-and-pipelines/SKILL.md`, `dvc/sub-skills/experiments/SKILL.md`, `dvc/sub-skills/remotes-and-cache/SKILL.md`, `dvc/sub-skills/metrics-params-plots/SKILL.md`, `dvc/sub-skills/python-api/SKILL.md`, `dvc/sub-skills/repo-development/SKILL.md`.

### `mlflow`

Role: Use `mlflow` for MLflow repository work: experiment tracking, model registry, MLflow Models and flavors, evaluation, GenAI tracing/prompts/datasets/scorers, local serving, deployments, projects, CLI/server/auth.
Read when: The request names `mlflow` or asks for package-specific APIs, CLIs, configs, data/model artifacts, error messages, workflows, or repository maintenance that match this project.
Best for: genai observability, models and flavors, serving and projects, and tracking and registry.
Avoid when: another repo skill in this scenario matches the user's task, package, model family, data format, serving backend, or workflow more directly.
Useful entry points: `mlflow/SKILL.md`, `mlflow/sub-skills/genai-observability/`, `mlflow/sub-skills/models-and-flavors/`, `mlflow/sub-skills/serving-and-projects/`, `mlflow/sub-skills/tracking-and-registry/`.

### `nni`

Role: Routes NNI AutoML tasks to focused HPO, NAS, compression, and utility guidance with bundled validators and diagnostics.
Read when: nni, nnictl, ExperimentConfig, search_space, tuner, assessor, ModelSpace, LayerChoice, config_list, pruner, quantizer, GBDTSelector, concrete_trace, torch or pytorch_lightning import failures in NNI workflows.
Best for: Creating and debugging NNI experiments, search spaces, NAS model spaces, compression configs, feature selectors, optional dependency triage, and repo-specific API routing.
Avoid when: The task is general model training unrelated to NNI, frontend-only TypeScript development, or cloud resource provisioning without an NNI experiment/config context.
Useful entry points: `nni/SKILL.md`, `nni/sub-skills/hpo-experiments/`, `nni/sub-skills/nas/`, `nni/sub-skills/model-compression/`, `nni/sub-skills/feature-engineering-and-utilities/`.

### `optuna`

Role: Use `optuna` for Optuna hyperparameter optimization workflows: studies, trials, samplers, pruners, storage, CLI, visualization, artifacts, integrations, and advanced APIs.
Read when: The request names `optuna` or asks for package-specific APIs, CLIs, configs, data/model artifacts, error messages, workflows, or repository maintenance that match this project.
Best for: advanced apis, analysis visualization, artifacts integrations, cli and storage, optimization workflows, and samplers pruners.
Avoid when: another repo skill in this scenario matches the user's task, package, model family, data format, serving backend, or workflow more directly.
Useful entry points: `optuna/SKILL.md`, `optuna/sub-skills/advanced-apis/`, `optuna/sub-skills/analysis-visualization/`, `optuna/sub-skills/artifacts-integrations/`, `optuna/sub-skills/cli-and-storage/`, `optuna/sub-skills/optimization-workflows/`, `1 more sub-skills`.

### `wandb`

Role: Use W&B's Python SDK and CLI for experiment tracking, offline/local workflows, artifacts and registries, Public API exports, automations, sweeps, and Launch jobs.
Read when: The request names `wandb` or asks for package-specific APIs, CLIs, configs, data/model artifacts, error messages, workflows, or repository maintenance that match this project.
Best for: artifacts and registries, cli and local workflows, experiment tracking, public api and automation, and sweeps and launch.
Avoid when: another repo skill in this scenario matches the user's task, package, model family, data format, serving backend, or workflow more directly.
Useful entry points: `wandb/SKILL.md`, `wandb/sub-skills/artifacts-and-registries/`, `wandb/sub-skills/cli-and-local-workflows/`, `wandb/sub-skills/experiment-tracking/`, `wandb/sub-skills/public-api-and-automation/`, `wandb/sub-skills/sweeps-and-launch/`.

<!-- SKILLQED_SCENARIO:ml-experiment-tracking-and-mlops-workflows:END -->

## How To Choose

Choose MLflow/W&B for experiment tracking and registries, Optuna/NNI/AutoGluon for optimization or AutoML, DVC for data and pipeline versioning, and BentoML when packaging or serving is the main action. Use `autogluon` for practical repository-specific AutoGluon usage. Route tabular rows to tabular-ml, timestamped horizons to time-series-forecasting, and text/image/document/object/matching tasks to multimodal-automl. Use the root references for environment and saved-predictor problems. Choose `bentoml` when the request names `bentoml`, centers on Use BentoML to author model-serving Services, build and containerize Bentos, run HTTP/gRPC servers and clients, manage models, operate the CLI and BentoCloud, and configure observability or production runtime behavior. Use when tasks mention BentoML, bentoml service.py, bentofile.yaml, Bento build/serve/deploy, BentoCloud, or BentoML model stores, uses its APIs or CLIs, references its configs/artifacts/errors, or asks for repository workflows in ml experiment tracking and mlops workflows. Choose `dvc` when DVC-specific command syntax, file formats, cache/remotes, experiment semantics, public dvc.api behavior, or DVC repository tests matter; then route to the most specific sub-skill by task family. Choose `nni` for NNI-specific AutoML APIs and configs; route within it by practical workflow instead of source folder names.
