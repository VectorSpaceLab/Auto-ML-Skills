# Distributed PyTorch Training and Large Model Workflows

## When To Read

Distributed training loops, launchers, DeepSpeed/FSDP/TPU backends, PyTorch Lightning/Fabric, scalable GNN training, checkpoints, and memory planning.

## Repo Skill Options

<!-- DISCO_SCENARIO:distributed-pytorch-training-and-large-model-workflows:START -->
### `accelerate`

Role: Use Hugging Face Accelerate for PyTorch training-loop migration, distributed launch/configuration, DeepSpeed/FSDP/TPU backend setup, big-model inference/offload, checkpointing, tracking, and troubleshooting.
Read when: The request names `accelerate` or asks for package-specific APIs, CLIs, configs, data/model artifacts, error messages, workflows, or repository maintenance that match this project.
Best for: big model inference, checkpointing and tracking, configuration and cli, distributed training backends, and training loop integration.
Avoid when: another repo skill in this scenario matches the user's task, package, model family, data format, serving backend, or workflow more directly.
Useful entry points: `accelerate/SKILL.md`, `accelerate/sub-skills/big-model-inference/`, `accelerate/sub-skills/checkpointing-and-tracking/`, `accelerate/sub-skills/configuration-and-cli/`, `accelerate/sub-skills/distributed-training-backends/`, `accelerate/sub-skills/training-loop-integration/`.

### `deepspeed`

Role: Use DeepSpeed for distributed training, inference acceleration, ZeRO configuration, parallelism/MoE design, profiling, autotuning, and operational diagnostics.
Read when: The request names `deepspeed` or asks for package-specific APIs, CLIs, configs, data/model artifacts, error messages, workflows, or repository maintenance that match this project.
Best for: inference injection, ops tooling, parallelism moe, and training config.
Avoid when: another repo skill in this scenario matches the user's task, package, model family, data format, serving backend, or workflow more directly.
Useful entry points: `deepspeed/SKILL.md`, `deepspeed/sub-skills/inference-injection/`, `deepspeed/sub-skills/ops-tooling/`, `deepspeed/sub-skills/parallelism-moe/`, `deepspeed/sub-skills/training-config/`.

### `lightning`

Role: Build, configure, debug, distribute, and deploy PyTorch Lightning and Lightning Fabric workflows using Trainer, LightningModule, LightningCLI, Fabric, accelerators, strategies, and serving utilities.
Read when: The request names `lightning` or asks for package-specific APIs, CLIs, configs, data/model artifacts, error messages, workflows, or repository maintenance that match this project.
Best for: cli configuration, deployment serving, distributed accelerators, fabric expert loops, and training core.
Avoid when: another repo skill in this scenario matches the user's task, package, model family, data format, serving backend, or workflow more directly.
Useful entry points: `lightning/SKILL.md`, `lightning/sub-skills/cli-configuration/`, `lightning/sub-skills/deployment-serving/`, `lightning/sub-skills/distributed-accelerators/`, `lightning/sub-skills/fabric-expert-loops/`, `lightning/sub-skills/training-core/`.

### `nemo`

Role: Adds NeMo Speech-specific PyTorch Lightning, FSDP2/DTensor SpeechLM2, checkpoint, GPU memory, and batch-planning guidance for speech and audio models.
Read when: The request combines NeMo with PyTorch Lightning trainer configs, FSDP2 or DTensor, SpeechLM2 distributed training, `.nemo` or distributed checkpoint handling, OOMptimizer, dynamic bucketing, CUDA extras, compiled Automodel backends, or GPU memory planning.
Best for: NeMo-specific training/fine-tuning and memory planning for ASR, TTS, audio, SpeechLM2, and repository tests that use PyTorch Lightning/FSDP2/DTensor conventions.
Avoid when: Use a generic distributed PyTorch or Lightning skill when the task is framework-level and does not involve NeMo collections, configs, checkpoints, or examples.
Useful entry points: `nemo/SKILL.md`, `nemo/sub-skills/asr/SKILL.md`, `nemo/sub-skills/tts/SKILL.md`, `nemo/sub-skills/audio/SKILL.md`, `nemo/sub-skills/speechlm2/SKILL.md`, `nemo/sub-skills/repo-development/SKILL.md`.

### `openfold`

Role: Adds OpenFold-specific train_openfold.py, DeepSpeed config, checkpoint, seed, data-cache, and GPU runtime guidance to generic distributed PyTorch workflows.
Read when: Requests mention OpenFold training, fine-tuning, train_openfold.py, OpenProteinSet, DeepSpeed OpenFold configs, BF16/A100, multi-node OpenFold, resume_from_ckpt, or OpenFold training data caches.
Best for: Constructing dry-run OpenFold training/fine-tuning commands, generating DeepSpeed JSON safely, and diagnosing OpenFold-specific distributed training prerequisites.
Avoid when: The request is generic DeepSpeed, Lightning, Accelerate, FSDP, or LLM training without OpenFold-specific data or scripts.
Useful entry points: `openfold/sub-skills/training/SKILL.md`, `openfold/sub-skills/data-preparation/SKILL.md`, `openfold/sub-skills/installation-assets/SKILL.md`.

### `openrlhf`

Role: Use OpenRLHF for Ray/vLLM/DeepSpeed RLHF workflows, including dataset preparation, SFT/RM/DPO training, PPO-family RL and agent training, runtime operations, reward serving, LoRA merging, and troubleshooting.
Read when: The request names `openrlhf` or asks for package-specific APIs, CLIs, configs, data/model artifacts, error messages, workflows, or repository maintenance that match this project.
Best for: data preparation, operations and utilities, rl agent training, and supervised preference training.
Avoid when: another repo skill in this scenario matches the user's task, package, model family, data format, serving backend, or workflow more directly.
Useful entry points: `openrlhf/SKILL.md`, `openrlhf/sub-skills/data-preparation/`, `openrlhf/sub-skills/operations-and-utilities/`, `openrlhf/sub-skills/rl-agent-training/`, `openrlhf/sub-skills/supervised-preference-training/`.

### `optuna`

Role: Use `optuna` for Optuna hyperparameter optimization workflows: studies, trials, samplers, pruners, storage, CLI, visualization, artifacts, integrations, and advanced APIs.
Read when: The request names `optuna` or asks for package-specific APIs, CLIs, configs, data/model artifacts, error messages, workflows, or repository maintenance that match this project.
Best for: advanced apis, analysis visualization, artifacts integrations, cli and storage, optimization workflows, and samplers pruners.
Avoid when: another repo skill in this scenario matches the user's task, package, model family, data format, serving backend, or workflow more directly.
Useful entry points: `optuna/SKILL.md`, `optuna/sub-skills/advanced-apis/`, `optuna/sub-skills/analysis-visualization/`, `optuna/sub-skills/artifacts-integrations/`, `optuna/sub-skills/cli-and-storage/`, `optuna/sub-skills/optimization-workflows/`, `optuna/sub-skills/samplers-pruners/`.

### `pytorch-geometric`

Role: Use PyTorch Geometric to build graph data, loaders, GNN models, heterogeneous workflows, explainers, scalable/distributed jobs, and GraphGym experiments.
Read when: The request names `pytorch-geometric` or asks for package-specific APIs, CLIs, configs, data/model artifacts, error messages, workflows, or repository maintenance that match this project.
Best for: data and datasets, explainability, gnn modeling, graphgym experiments, heterogeneous graphs, and 2 other focused workflows.
Avoid when: another repo skill in this scenario matches the user's task, package, model family, data format, serving backend, or workflow more directly.
Useful entry points: `pytorch-geometric/SKILL.md`, `pytorch-geometric/sub-skills/data-and-datasets/`, `pytorch-geometric/sub-skills/explainability/`, `pytorch-geometric/sub-skills/gnn-modeling/`, `pytorch-geometric/sub-skills/graphgym-experiments/`, `pytorch-geometric/sub-skills/heterogeneous-graphs/`, `pytorch-geometric/sub-skills/loaders-and-sampling/`, `pytorch-geometric/sub-skills/scalable-distributed/`.

### `torchtune`

Role: Explains torchtune's distributed recipe launch shape, torchrun argument placement, checkpointing, precision, memory, and runtime preflight helpers.
Read when: The request mentions torchtune distributed recipes, `--nproc_per_node`, `--nnodes`, multinode, checkpoints, bf16, activation offloading, optimizer-in-backward, or memory planning.
Best for: Building safe torchtune distributed commands and diagnosing torchtune-specific launcher/checkpoint/device errors before expensive jobs.
Avoid when: The task is generic PyTorch distributed programming or a non-torchtune launcher/framework.
Useful entry points: `torchtune/sub-skills/post-training-recipes/SKILL.md`, `torchtune/sub-skills/training-utilities-and-rlhf/SKILL.md`.

### `verl`

Role: Use verl for LLM post-training workflows: setup, data and rewards, PPO/GRPO/SFT configs, rollout tools, checkpoints, profiling, and repository maintenance.
Read when: The request names `verl` or asks for package-specific APIs, CLIs, configs, data/model artifacts, error messages, workflows, or repository maintenance that match this project.
Best for: checkpoints and model ops, data and rewards, repo development, rollout and tools, setup and backends, and training and configs.
Avoid when: another repo skill in this scenario matches the user's task, package, model family, data format, serving backend, or workflow more directly.
Useful entry points: `verl/SKILL.md`, `verl/sub-skills/checkpoints-and-model-ops/`, `verl/sub-skills/data-and-rewards/`, `verl/sub-skills/repo-development/`, `verl/sub-skills/rollout-and-tools/`, `verl/sub-skills/setup-and-backends/`, `verl/sub-skills/training-and-configs/`.

<!-- DISCO_SCENARIO:distributed-pytorch-training-and-large-model-workflows:END -->

## How To Choose

Choose Accelerate for generic distributed loop migration and launch, DeepSpeed for ZeRO/DeepSpeed configs, Lightning for Lightning/Fabric, PyG for graph neural training, OpenRLHF/verl for RLHF-scale training stacks, and Optuna for hyperparameter optimization. Choose `accelerate` when the request names `accelerate`, centers on PyTorch training-loop migration, distributed launch/configuration, DeepSpeed/FSDP/TPU backend setup, big-model inference/offload, checkpointing, tracking, and troubleshooting, uses its APIs or CLIs, references its configs/artifacts/errors, or asks for repository workflows in distributed pytorch training and large model workflows. Choose `deepspeed` when the request names `deepspeed`, centers on distributed training, inference acceleration, ZeRO configuration, parallelism/MoE design, profiling, autotuning, and operational diagnostics, uses its APIs or CLIs, references its configs/artifacts/errors, or asks for repository workflows in distributed pytorch training and large model workflows. Choose `nemo` for distributed or large-model training questions when NeMo configs, speech/audio model families, NeMo checkpoints, OOMptimizer, Lhotse bucketing, SpeechLM2 FSDP2/DTensor, or NeMo optional backend extras appear in the request.
