# Embodied AI Simulation and Training

## When To Read

Embodied AI simulation, navigation/rearrangement tasks, habitat-style configs, datasets, training, HITL apps, and simulator extension registries.

## Repo Skill Options

<!-- DISCO_SCENARIO:embodied-ai-simulation:START -->
### `habitat-lab`

Role: Routes agents to self-contained Habitat-Lab guidance for setup, configs, environments, datasets, baseline training/evaluation, HITL interaction, and extension patterns.
Read when: User mentions habitat-lab, habitat_baselines, habitat_hitl, Habitat-Sim, PointNav, ObjectNav, ImageNav, VLN, EQA, rearrangement, HITL, GymHabitatEnv, Hydra configs, habitat-baselines CLI, custom Habitat sensors/measures/actions, or registry errors.
Best for: Composing configs, diagnosing imports/data/backend issues, building Env/Gym/VectorEnv workflows, running safe baselines config probes, planning train/eval commands, reasoning about HITL app launch constraints, and adding registry extensions.
Avoid when: The task is only about low-level Habitat-Sim C++/viewer APIs outside Habitat-Lab, a different embodied-AI framework, or running large training/benchmark/data-download jobs without user approval.
Useful entry points: `habitat-lab/SKILL.md`, `habitat-lab/sub-skills/setup-and-configuration/SKILL.md`, `habitat-lab/sub-skills/tasks-datasets-and-envs/SKILL.md`, `habitat-lab/sub-skills/baselines-training-and-evaluation/SKILL.md`, `habitat-lab/sub-skills/hitl-apps-and-interaction/SKILL.md`, `habitat-lab/sub-skills/extension-patterns/SKILL.md`.

<!-- DISCO_SCENARIO:embodied-ai-simulation:END -->

## How To Choose

Use this scenario for embodied AI simulation and training stacks rather than generic reinforcement learning algorithms or vision models. Choose `habitat-lab` when Habitat-Lab repository APIs/configs are central; within it, route setup/import/config questions first to setup-and-configuration, runtime Env/dataset questions to tasks-datasets-and-envs, train/eval questions to baselines-training-and-evaluation, realtime interaction to HITL, and custom components to extension-patterns.
