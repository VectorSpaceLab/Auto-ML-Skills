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

<!-- DISCO_SCENARIO:deep-learning-training-engines:END -->

## How To Choose

Use this scenario for framework engine internals such as MMEngine; choose model-family scenarios when the request is about a concrete model workflow. Choose `mmengine` for generic MMEngine engine-layer work. If a task also names a downstream OpenMMLab repository, use `mmengine` for shared engine contracts and the downstream repo skill for task-specific components.
