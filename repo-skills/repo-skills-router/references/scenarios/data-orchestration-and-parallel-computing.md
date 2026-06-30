# Data Orchestration and Parallel Computing

## When To Read

Workflow engines, DAGs, assets, Snakefiles, lazy/parallel task graphs, distributed arrays/dataframes, feature stores, cloud compute orchestration, and production data pipelines.

## Repo Skill Options

<!-- DISCO_SCENARIO:data-orchestration-and-parallel-computing:START -->
### `apache-airflow`

Role: Routes Airflow tasks to focused guidance for authoring, operations, providers, deployment, and contribution tooling.
Read when: Apache Airflow, apache-airflow, airflow.sdk, Task SDK, Dag, airflow CLI, airflowctl, providers, Helm chart, Docker image, Breeze, prek, selective checks, Airflow repo.
Best for: Writing or migrating Dags, debugging Airflow CLI/API/config issues, maintaining providers/extensions, planning official Helm/Docker deployments, and safely contributing to the Airflow monorepo.
Avoid when: The task is only about a separate language SDK already covered by a more specific Java/Go/new-language SDK skill, or about a non-Airflow workflow orchestrator.
Useful entry points: `apache-airflow/SKILL.md`, `apache-airflow/sub-skills/authoring-task-sdk/SKILL.md`, `apache-airflow/sub-skills/operations-cli-api/SKILL.md`, `apache-airflow/sub-skills/providers-extensions/SKILL.md`, `apache-airflow/sub-skills/deployment-helm-docker/SKILL.md`, `apache-airflow/sub-skills/contribution-tooling/SKILL.md`.

### `dagster`

Role: Use when working with Dagster OSS: assets, jobs, Definitions, config/resources, schedules/sensors, automation, CLI/local development, deployment operations, GraphQL/webserver, Pipes external processes, components/projects.
Read when: The request names `dagster` or asks for package-specific APIs, CLIs, configs, data/model artifacts, error messages, workflows, or repository maintenance that match this project.
Best for: asset definitions, automation schedules sensors, cli local development, components projects, configuration resources, and 4 other focused workflows.
Avoid when: another repo skill in this scenario matches the user's task, package, model family, data format, serving backend, or workflow more directly.
Useful entry points: `dagster/SKILL.md`, `dagster/sub-skills/asset-definitions/`, `dagster/sub-skills/automation-schedules-sensors/`, `dagster/sub-skills/cli-local-development/`, `dagster/sub-skills/components-projects/`, `dagster/sub-skills/configuration-resources/`, `dagster/sub-skills/deployment-operations/`, `dagster/sub-skills/graphql-and-webserver/`, `dagster/sub-skills/pipes-external-processes/`, `dagster/sub-skills/repo-development/`.

### `dask`

Role: Use this repo skill for Dask, the Python parallel computing library, when working with lazy task graphs, schedulers, Dask Array, Dask DataFrame, Dask Bag/bytes IO, configuration, diagnostics, CLI usage, or contributor validation.
Read when: The request names `dask` or asks for package-specific APIs, CLIs, configs, data/model artifacts, error messages, workflows, or repository maintenance that match this project.
Best for: array workflows, bag bytes workflows, configuration diagnostics cli, core graphs schedulers, and dataframe workflows.
Avoid when: another repo skill in this scenario matches the user's task, package, model family, data format, serving backend, or workflow more directly.
Useful entry points: `dask/SKILL.md`, `dask/sub-skills/array-workflows/`, `dask/sub-skills/bag-bytes-workflows/`, `dask/sub-skills/configuration-diagnostics-cli/`, `dask/sub-skills/core-graphs-schedulers/`, `dask/sub-skills/dataframe-workflows/`.

### `feast`

Role: Use for Feast feature store tasks: feature repositories, definitions, CLI, retrieval, materialization, serving, RAG/vector search, integrations, and Feast contributor workflows.
Read when: The request names `feast` or asks for package-specific APIs, CLIs, configs, data/model artifacts, error messages, workflows, or repository maintenance that match this project.
Best for: feature definitions, feature repos and cli, integrations and extensibility, rag and vector search, repo development, and 2 other focused workflows.
Avoid when: another repo skill in this scenario matches the user's task, package, model family, data format, serving backend, or workflow more directly.
Useful entry points: `feast/SKILL.md`, `feast/sub-skills/feature-definitions/`, `feast/sub-skills/feature-repos-and-cli/`, `feast/sub-skills/integrations-and-extensibility/`, `feast/sub-skills/rag-and-vector-search/`, `feast/sub-skills/repo-development/`, `feast/sub-skills/retrieval-and-materialization/`, `feast/sub-skills/servers-and-remote/`.

### `hail`

Role: Provides repo-specific guidance for Hail's Python APIs, Hailtop Batch DAGs, hailctl command families, and Hail backend setup/troubleshooting.
Read when: User mentions Hail, hail, hailtop, hailctl, MatrixTable, VariantDataset, VDS, GVCF combiner, hl.init, Hail Batch, LocalBackend, ServiceBackend, VCF/PLINK/BGEN import, genomic QC, or Hail cloud execution.
Best for: Using Hail Tables, dense MatrixTables, VDS/GVCF workflows, Hail Batch DAGs, hailctl config/auth/batch/dataproc/hdinsight commands, and diagnosing Hail setup/backend failures.
Avoid when: The task is about unrelated Hail monorepo service deployment, Kubernetes infrastructure, release automation, generic Spark without Hail, or non-genomic data systems not using Hail APIs.
Useful entry points: `hail/SKILL.md`, `hail/sub-skills/setup-and-backends/SKILL.md`, `hail/sub-skills/tables-and-expressions/SKILL.md`, `hail/sub-skills/genomics-analysis/SKILL.md`, `hail/sub-skills/variant-datasets/SKILL.md`, `hail/sub-skills/batch-and-cli/SKILL.md`.

### `kedro`

Role: Kedro covers production-ready Python data and analytics pipeline projects with nodes, pipelines, catalogs, configuration, sessions, runners, hooks, inspection, and project CLI workflows.
Read when: Use kedro when tasks mention Kedro, data/analytics pipelines, node or Pipeline APIs, DataCatalog or catalog.yml, OmegaConfigLoader, credentials.yml, parameters.yml, kedro run, KedroSession, project scaffolding with kedro new, hooks/plugins, SequentialRunner, ThreadRunner, ParallelRunner, project snapshots, or optional Kedro server endpoints.
Best for: Designing and running Kedro pipelines, configuring DataCatalog and OmegaConfigLoader, creating Kedro projects, constructing kedro run commands, selecting runners, writing hooks/plugins/custom datasets, using Kedro sessions, and inspecting Kedro projects without running pipelines.
Avoid when: Avoid kedro for generic Airflow/Dagster/Prefect orchestration, Dask dataframe/array compute, Feast feature-store tasks, generic pandas ETL, or concrete dataset implementation details that belong to kedro-datasets unless the task is specifically about wiring those datasets through Kedro.
Useful entry points: `kedro/SKILL.md`, `kedro/sub-skills/pipelines-and-nodes/SKILL.md`, `kedro/sub-skills/data-catalog-and-config/SKILL.md`, `kedro/sub-skills/project-cli-and-sessions/SKILL.md`, `kedro/sub-skills/runners-and-execution/SKILL.md`, `kedro/sub-skills/hooks-and-extensions/SKILL.md`, `kedro/sub-skills/inspection-and-server/SKILL.md`.

### `prefect`

Role: Routes Prefect usage and maintenance requests to focused SDK, deployment, CLI/server, API/settings, events/blocks/assets, and repo-development guidance.
Read when: prefect, @flow, @task, prefect.yaml, work pool, worker, deployment, automation, block, asset, PrefectClient, PREFECT_API_URL, prefect-client, Prefect server, Prefect Cloud.
Best for: Authoring and debugging Prefect workflows, creating deployments, operating local or Cloud profiles, using the Python API client, validating automations/YAML, and modifying the Prefect repository safely.
Avoid when: The task is about a deep provider integration package, UI-v2 React implementation, legacy UI, benchmark/load test infrastructure, or a different workflow orchestrator.
Useful entry points: `prefect/SKILL.md`, `prefect/sub-skills/flow-task-authoring/SKILL.md`, `prefect/sub-skills/deployments-workers/SKILL.md`, `prefect/sub-skills/cli-server-operations/SKILL.md`, `prefect/sub-skills/api-client-settings/SKILL.md`, `prefect/sub-skills/events-blocks-assets/SKILL.md`, `prefect/sub-skills/repo-development/SKILL.md`.

### `pytorch-geometric`

Role: Use PyTorch Geometric to build graph data, loaders, GNN models, heterogeneous workflows, explainers, scalable/distributed jobs, and GraphGym experiments.
Read when: The request names `pytorch-geometric` or asks for package-specific APIs, CLIs, configs, data/model artifacts, error messages, workflows, or repository maintenance that match this project.
Best for: data and datasets, explainability, gnn modeling, graphgym experiments, heterogeneous graphs, and 2 other focused workflows.
Avoid when: another repo skill in this scenario matches the user's task, package, model family, data format, serving backend, or workflow more directly.
Useful entry points: `pytorch-geometric/SKILL.md`, `pytorch-geometric/sub-skills/data-and-datasets/`, `pytorch-geometric/sub-skills/explainability/`, `pytorch-geometric/sub-skills/gnn-modeling/`, `pytorch-geometric/sub-skills/graphgym-experiments/`, `pytorch-geometric/sub-skills/heterogeneous-graphs/`, `pytorch-geometric/sub-skills/loaders-and-sampling/`, `pytorch-geometric/sub-skills/scalable-distributed/`.

### `ray`

Role: Use `ray` for Ray-specific distributed Python, cluster operations, data processing, training/tuning, serving, and RLlib workflows.
Read when: The task names Ray, ray, ray.remote, Ray Core, Ray Data, Ray Train, Ray Tune, Ray Serve, RLlib, ObjectRef, actor, task, ray job, runtime_env, ray status, serve deploy, Tuner, TuneConfig, PPOConfig, AlgorithmConfig, or asks to scale Python/data/ML/RL work across CPUs, GPUs, nodes, jobs, or Serve replicas.
Best for: Ray package usage: task/actor code, cluster CLI and Jobs, runtime environment packaging, Data loading/transforms, Train/Tune checkpointed experiments and hyperparameter sweeps, Serve YAML/application deployment, and RLlib AlgorithmConfig/Gymnasium workflows.
Avoid when: Use a generic PyTorch, Dask, Airflow, Kubernetes, cloud-provider, FastAPI, or reinforcement-learning package skill when the request is not using Ray APIs or Ray-managed execution. Use a repo maintenance scenario if the user is editing Ray source internals rather than using Ray as a library.
Useful entry points: `ray/SKILL.md`, `ray/sub-skills/core-runtime/SKILL.md`, `ray/sub-skills/cluster-ops/SKILL.md`, `ray/sub-skills/data-pipelines/SKILL.md`, `ray/sub-skills/train-tune/SKILL.md`, `ray/sub-skills/serve-deployments/SKILL.md`, `ray/sub-skills/rllib-workloads/SKILL.md`.

### `skypilot`

Role: Routes SkyPilot end-user workflows across task YAML authoring, interactive clusters, managed jobs, serving, infrastructure/storage, and the Python SDK.
Read when: SkyPilot, skypilot, sky launch, sky exec, sky jobs, sky serve, sky check, sky gpus, task.yaml, SkyServe, managed spot, Kubernetes GPUs, Slurm, file_mounts, volumes, cloud failover, GPU availability, API server.
Best for: Writing SkyPilot YAMLs, planning safe CLI/SDK commands, debugging SkyPilot install/API server/cloud/provider issues, deploying managed jobs or services, and translating AI workload requirements into SkyPilot workflows.
Avoid when: The task is local-only Docker/conda work with no SkyPilot involvement, asks for a generic cloud provider SDK instead of SkyPilot, or needs direct credentials/resource mutation without user authorization.
Useful entry points: `skypilot/SKILL.md`, `skypilot/sub-skills/task-yaml/SKILL.md`, `skypilot/sub-skills/cluster-operations/SKILL.md`, `skypilot/sub-skills/managed-jobs/SKILL.md`, `skypilot/sub-skills/serving/SKILL.md`, `skypilot/sub-skills/infrastructure-storage/SKILL.md`, `skypilot/sub-skills/sdk-api-server/SKILL.md`.

### `snakemake`

Role: Guides Snakemake workflows, including Snakefile authoring, CLI execution, configuration/data validation, deployment/storage, reporting/testing, and Python API/plugin usage.
Read when: The request names `snakemake` or asks for package-specific APIs, CLIs, configs, data/model artifacts, error messages, workflows, or repository maintenance that match this project.
Best for: configuration data, debugging reporting, deployment storage, execution cli, python api plugins, and workflow authoring.
Avoid when: another repo skill in this scenario matches the user's task, package, model family, data format, serving backend, or workflow more directly.
Useful entry points: `snakemake/SKILL.md`, `snakemake/sub-skills/configuration-data/`, `snakemake/sub-skills/debugging-reporting/`, `snakemake/sub-skills/deployment-storage/`, `snakemake/sub-skills/execution-cli/`, `snakemake/sub-skills/python-api-plugins/`, `snakemake/sub-skills/workflow-authoring/`.

<!-- DISCO_SCENARIO:data-orchestration-and-parallel-computing:END -->

## How To Choose

Choose by execution substrate: Airflow/Dagster/Prefect/Snakemake for workflow orchestration, Dask for parallel Python data compute, Feast for feature stores, SkyPilot for cloud compute jobs, and PyG/DGL only when graph-data workflows are central. Choose by practical task: Dag code -> authoring-task-sdk; installed/running Airflow or APIs -> operations-cli-api; providers/extensions -> providers-extensions; Helm/Docker/Kubernetes -> deployment-helm-docker; repo edits/tests/PRs -> contribution-tooling. Choose `dagster` when the request names `dagster`, centers on Use when working with Dagster OSS: assets, jobs, Definitions, config/resources, schedules/sensors, automation, CLI/local development, deployment operations, GraphQL/webserver, Pipes external processes, components/projects, or editing the Dagster repository itself, uses its APIs or CLIs, references its configs/artifacts/errors, or asks for repository workflows in data orchestration and parallel computing. Choose `dask` when the request names `dask`, centers on Dask, the Python parallel computing library, when working with lazy task graphs, schedulers, Dask Array, Dask DataFrame, Dask Bag/bytes IO, configuration, diagnostics, CLI usage, or contributor validation, uses its APIs or CLIs, references its configs/artifacts/errors, or asks for repository workflows in data orchestration and parallel computing.
