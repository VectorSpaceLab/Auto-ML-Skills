# Reinforcement Learning Workflows

## When To Read

Gymnasium environments, Stable-Baselines3 algorithms, RL vectorization, policies, evaluation, experiment scripts, replay buffers, collectors, action masks, multi-agent RL environments, and PPO-family rollout-agent training.

## Repo Skill Options

<!-- DISCO_SCENARIO:reinforcement-learning-workflows:START -->
### `cleanrl`

Role: Routes CleanRL script-oriented RL training tasks to algorithm, CLI, optional dependency, and safe-run guidance.
Read when: cleanrl, CleanRL, ppo.py, dqn.py, c51.py, Atari, EnvPool, Procgen, MuJoCo, PettingZoo, JAX, tyro, --total-timesteps, --env-id. cleanrl benchmark, cleanrl_utils.benchmark, wandb cleanRL, Optuna tuner, resume training, reproduce, Slurm, AWS Batch, Docker, Terraform, benchmark/*.sh.
Best for: Choosing and safely running CleanRL algorithms, inspecting script arguments, diagnosing missing RL backends, and adapting single-file training commands. Generating dry-run command matrices, checking credential readiness without leaking secrets, and planning cloud/container/Slurm operations safely.
Avoid when: The task is about a different RL library, general RL theory without CleanRL code, or executing long benchmark/cloud jobs without CleanRL-specific context. The task is only about selecting one training script or evaluating a saved model artifact; route those to the training or evaluation sub-skills.
Useful entry points: `cleanrl/SKILL.md`, `cleanrl/sub-skills/training-scripts/SKILL.md`, `cleanrl/sub-skills/experiment-operations/SKILL.md`.

### `openrlhf`

Role: Use OpenRLHF for Ray/vLLM/DeepSpeed RLHF workflows, including dataset preparation, SFT/RM/DPO training, PPO-family RL and agent training, runtime operations, reward serving, LoRA merging, and troubleshooting.
Read when: The request names `openrlhf` or asks for package-specific APIs, CLIs, configs, data/model artifacts, error messages, workflows, or repository maintenance that match this project.
Best for: data preparation, operations and utilities, rl agent training, and supervised preference training.
Avoid when: another repo skill in this scenario matches the user's task, package, model family, data format, serving backend, or workflow more directly.
Useful entry points: `openrlhf/SKILL.md`, `openrlhf/sub-skills/data-preparation/`, `openrlhf/sub-skills/operations-and-utilities/`, `openrlhf/sub-skills/rl-agent-training/`, `openrlhf/sub-skills/supervised-preference-training/`.

### `pettingzoo`

Role: Guides agents through PettingZoo environment use, selection, authoring, validation, wrappers, and training-framework integration planning.
Read when: PettingZoo, AECEnv, ParallelEnv, agent_iter, parallel_env, action_mask, api_test, parallel_api_test, pettingzoo[classic], pettingzoo[atari], Pistonball, Connect Four, Tic-Tac-Toe, custom multi-agent env, CleanRL/Tianshou/SB3/RLlib with PettingZoo.
Best for: Writing correct AEC/Parallel loops, selecting optional environment-family extras, implementing custom environments, diagnosing compliance-test failures, composing wrappers/conversions, and adapting framework tutorials safely.
Avoid when: The task is only generic Gymnasium single-agent usage, general RL algorithm implementation without PettingZoo environments, or framework-specific training unrelated to PettingZoo adapters.
Useful entry points: `pettingzoo/SKILL.md`, `pettingzoo/sub-skills/use-environments/SKILL.md`, `pettingzoo/sub-skills/environment-families/SKILL.md`, `pettingzoo/sub-skills/custom-environments/SKILL.md`, `pettingzoo/sub-skills/testing-and-validation/SKILL.md`.

### `stable-baselines3`

Role: Use Stable-Baselines3 for PyTorch reinforcement learning: train algorithms, validate Gymnasium environments, vectorize envs, customize policies, evaluate callbacks, and save/load SB3 models.
Read when: The request names `stable-baselines3` or asks for package-specific APIs, CLIs, configs, data/model artifacts, error messages, workflows, or repository maintenance that match this project.
Best for: environments and vectorization, evaluation and persistence, policies and customization, and training and algorithms.
Avoid when: another repo skill in this scenario matches the user's task, package, model family, data format, serving backend, or workflow more directly.
Useful entry points: `stable-baselines3/SKILL.md`, `stable-baselines3/sub-skills/environments-and-vectorization/`, `stable-baselines3/sub-skills/evaluation-and-persistence/`, `stable-baselines3/sub-skills/policies-and-customization/`, `stable-baselines3/sub-skills/training-and-algorithms/`.

### `tianshou`

Role: Provides repo-specific routing and version-aware guidance for building Tianshou 2.0.1 RL experiments safely.
Read when: tianshou, Tianshou, ExperimentBuilder, DQNExperimentBuilder, PPOExperimentBuilder, Algorithm, Policy, OffPolicyTrainerParams, OnPolicyTrainerParams, Gymnasium RL training. Batch, ReplayBuffer, VectorReplayBuffer, PrioritizedReplayBuffer, HERReplayBuffer, Collector.collect, AsyncCollector, DummyVectorEnv, SubprocVectorEnv, PettingZooEnv, action mask, EnvPool, MuJoCo, Atari, VizDoom. CQL, BCQ, TD3+BC, DiscreteCQL, DiscreteBCQ, DiscreteCRR, GAIL, PSRL, ICM, MultiAgentOffPolicyAlgorithm, MultiAgentOnPolicyAlgorithm, JoblibExpLauncher, rliable, benchmark.
Best for: High-level builder skeletons, manual DQN/PPO/SAC wiring, bounded CartPole smokes, policy/network/trainer integration, API-v2 migration from older Tianshou examples. Debugging data shapes, buffer sampling, collector stop modes, vector-env worker choice, PettingZoo masks, optional backend install/import failures, and safe no-training smoke checks. Offline buffer preparation, expert-buffer validation, curiosity/model-based wrappers, PettingZoo multi-agent algorithm boundaries, multi-seed launcher planning, and rliable result aggregation.
Avoid when: The user wants a different RL framework, a generic RL explanation without Tianshou APIs, or benchmark-scale training without installed optional environment dependencies. The task is only about choosing an RL algorithm or high-level experiment builder with no custom data or env handling. The task only needs ordinary online DQN/PPO/SAC wiring or environment vectorization; use procedural-training or envs-and-vectorization instead.
Useful entry points: `tianshou/SKILL.md`, `tianshou/sub-skills/highlevel-experiments/SKILL.md`, `tianshou/sub-skills/procedural-training/SKILL.md`, `tianshou/sub-skills/data-collection/SKILL.md`, `tianshou/sub-skills/envs-and-vectorization/SKILL.md`, `tianshou/sub-skills/offline-and-specialized-rl/SKILL.md`, `tianshou/references/evaluation-and-benchmarks.md`.

### `trl`

Role: Use and modify TRL, the Hugging Face Transformers Reinforcement Learning library for post-training, CLI workflows, data/reward utilities, scaling backends, experimental environments, and repo development.
Read when: The request names `trl` or asks for package-specific APIs, CLIs, configs, data/model artifacts, error messages, workflows, or repository maintenance that match this project.
Best for: cli and configs, core training, data and rewards, experimental and environments, repo development, and scaling and backends.
Avoid when: another repo skill in this scenario matches the user's task, package, model family, data format, serving backend, or workflow more directly.
Useful entry points: `trl/SKILL.md`, `trl/sub-skills/cli-and-configs/`, `trl/sub-skills/core-training/`, `trl/sub-skills/data-and-rewards/`, `trl/sub-skills/experimental-and-environments/`, `trl/sub-skills/repo-development/`, `1 more sub-skills`.

### `verl`

Role: Use verl for LLM post-training workflows: setup, data and rewards, PPO/GRPO/SFT configs, rollout tools, checkpoints, profiling, and repository maintenance.
Read when: The request names `verl` or asks for package-specific APIs, CLIs, configs, data/model artifacts, error messages, workflows, or repository maintenance that match this project.
Best for: checkpoints and model ops, data and rewards, repo development, rollout and tools, setup and backends, and training and configs.
Avoid when: another repo skill in this scenario matches the user's task, package, model family, data format, serving backend, or workflow more directly.
Useful entry points: `verl/SKILL.md`, `verl/sub-skills/checkpoints-and-model-ops/`, `verl/sub-skills/data-and-rewards/`, `verl/sub-skills/repo-development/`, `verl/sub-skills/rollout-and-tools/`, `verl/sub-skills/setup-and-backends/`, `1 more sub-skills`.

<!-- DISCO_SCENARIO:reinforcement-learning-workflows:END -->

## How To Choose

Choose by RL package and layer: Stable-Baselines3 for algorithms, CleanRL for single-file training scripts and operations, Tianshou for collectors/buffers/offline RL, PettingZoo for multi-agent environments, and OpenRLHF/TRL/verl only when the task is LLM post-training. Prefer `cleanrl` over generic Python/ML guidance when the user names CleanRL or CleanRL script files; use training-scripts first for algorithm commands. Choose this scenario when the user asks how to run many experiments, track or reproduce results, or use CleanRL cloud/benchmark tooling. Choose `openrlhf` when the request names `openrlhf`, centers on Ray/vLLM/DeepSpeed RLHF workflows, including dataset preparation, SFT/RM/DPO training, PPO-family RL and agent training, runtime operations, reward serving, LoRA merging, and troubleshooting, uses its APIs or CLIs, references its configs/artifacts/errors, or asks for repository workflows in reinforcement learning workflows. Choose `pettingzoo` for PettingZoo-specific API contracts and repository-supported examples; choose a framework-specific skill only after this skill establishes the PettingZoo environment interface and optional dependencies. Choose highlevel-experiments for declarative builders and procedural-training for manual network/policy/algorithm/trainer wiring. Route buffer, env, offline, and evaluation details to the focused sub-skills.
