# Deep Learning Training Engines

## When To Read

Tasks about engine-level utilities, runners, hooks, loops, config systems, logging, visualization, and debugging for deep learning training frameworks.

## Repo Skill Options

<!-- DISCO_SCENARIO:deep-learning-training-engines:START -->
### `mmengine`

Role: Provides repo-specific routing and self-contained references for MMEngine configuration, runners, data contracts, model/evaluator contracts, runtime utilities, and optional distributed/visualization paths.
Read when: User mentions MMEngine, OpenMMLab Runner, Config, Registry, BaseDataset, BaseModel, BaseMetric, Evaluator, Visualizer, MMLogger, MessageHub, FlexibleRunner, hooks, optim wrappers, schedulers, checkpoint/resume, or MMEngine distributed helpers.
Best for: Writing or repairing MMEngine configs and registries, assembling Runner/FlexibleRunner workflows, implementing MMEngine-compatible datasets/models/metrics, diagnosing checkpoint/resume/hook/scheduler errors, and selecting safe logging/visualization/distributed utilities.
Avoid when: The task is specific to a downstream OpenMMLab codebase's domain model or dataset format and does not involve generic MMEngine contracts, or when the user only needs generic PyTorch unrelated to MMEngine APIs.
Useful entry points: `mmengine/SKILL.md`, `mmengine/sub-skills/configuration-and-registry/SKILL.md`, `mmengine/sub-skills/runner-and-training/SKILL.md`, `mmengine/sub-skills/data-structures-and-io/SKILL.md`, `mmengine/sub-skills/models-metrics-and-inference/SKILL.md`, `mmengine/sub-skills/runtime-utilities-and-visualization/SKILL.md`.

### `torchdrug`

Role: TorchDrug's core.Engine and Configurable/Registry stack provide package-specific model/task training, evaluation, checkpoint, and config serialization workflows.
Read when: Tasks mention torchdrug.core.Engine, Configurable, Registry, task.predict, task.target, solver.train, solver.evaluate, solver.save, solver.load, config_dict, load_config_dict, gpus, logger='wandb', gradient_interval, or TorchDrug checkpoint loading.
Best for: TorchDrug-specific training harness assembly, Task contract debugging, checkpoint/config round-trips, CPU/GPU selection, and safe no-dataset smoke checks.
Avoid when: Use generic PyTorch, Lightning, Accelerate, or distributed-training skills when the training loop is not using TorchDrug's Engine and task abstractions.
Useful entry points: `torchdrug/SKILL.md`, `torchdrug/sub-skills/training-engine/SKILL.md`.

<!-- DISCO_SCENARIO:deep-learning-training-engines:END -->

## How To Choose

Use this scenario for framework engine internals such as MMEngine; choose model-family scenarios when the request is about a concrete model workflow. Choose `mmengine` for generic MMEngine engine-layer work. If a task also names a downstream OpenMMLab repository, use `mmengine` for shared engine contracts and the downstream repo skill for task-specific components. Choose torchdrug when the training engine question names TorchDrug abstractions or combines graph drug-discovery tasks with core.Engine; otherwise choose the framework owning the active training loop.
