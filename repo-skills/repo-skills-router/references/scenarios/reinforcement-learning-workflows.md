# Reinforcement Learning Workflows

## When To Read

Gymnasium environments, Stable-Baselines3 algorithms, RL vectorization, policies, evaluation, experiment scripts, replay buffers, collectors, action masks, multi-agent RL environments, and PPO-family rollout-agent training.

## Repo Skill Options

<!-- DISCO_SCENARIO:reinforcement-learning-workflows:START -->
### `acme`

Role: Use acme for DeepMind Acme framework tasks spanning dm_env loops, Reverb replay, JAX agents, and TensorFlow/Sonnet agents.
Read when: User mentions Acme, dm-acme, acme.EnvironmentLoop, acme.specs, acme.adders, Reverb adders, acme.jax.experiments, acme.agents.jax, acme.agents.tf, Sonnet networks, Launchpad Acme examples, or asks to choose/adapt D4PG, DQN, IMPALA, R2D2, SAC, MPO, PPO, BC, CQL, CRR, MCTS, MBOP, SQIL, PWIL, or DQfD in Acme.
Best for: Selecting Acme agent families, wiring dm_env environments to actors/learners, choosing replay adder/dataset structures, adapting JAX experiment configs, debugging TensorFlow/Sonnet Acme agents, and understanding optional backend dependencies.
Avoid when: Use another RL skill when the task primarily targets Stable-Baselines3, CleanRL, Tianshou, PettingZoo, TRL, OpenRLHF, or generic RL theory without Acme APIs or examples.
Useful entry points: `acme/SKILL.md`, `acme/sub-skills/core-workflows/SKILL.md`, `acme/sub-skills/replay-and-data/SKILL.md`, `acme/sub-skills/jax-agents/SKILL.md`, `acme/sub-skills/tf-agents/SKILL.md`.

### `agilerl`

Role: AgileRL-specific guidance for building, debugging, and validating reinforcement learning workflows with evolvable algorithms and population-based HPO.
Read when: Use for tasks naming AgileRL, agilerl, PPO/DQN/RainbowDQN/DDPG/TD3/CQL/ILQL/NeuralUCB/NeuralTS/MADDPG/MATD3/IPPO in AgileRL, create_population, Mutations, TournamentSelection, EvolvableModule, AsyncPettingZooVecEnv, BanditEnv, train_on_policy, train_off_policy, train_offline, train_bandits, train_multi_agent_* APIs, or AgileRL training YAML configs.
Best for: Classical and multi-agent AgileRL training setup, evolutionary HPO, evolvable network configuration, replay/offline/bandit data handling, PettingZoo wrappers, and safe smoke checks before long RL runs.
Avoid when: Use generic RL environment skills for PettingZoo/Gymnasium environment authoring without AgileRL, other RL library skills for Stable-Baselines3/CleanRL/Tianshou-specific APIs, and LLM post-training skills when the task is not using AgileRL's LLM algorithms.
Useful entry points: `agilerl/SKILL.md`, `agilerl/sub-skills/training-workflows/SKILL.md`, `agilerl/sub-skills/hpo-and-mutation/SKILL.md`, `agilerl/sub-skills/evolvable-modules/SKILL.md`, `agilerl/sub-skills/multi-agent-and-wrappers/SKILL.md`, `agilerl/sub-skills/offline-bandits-data/SKILL.md`, `agilerl/sub-skills/llm-fine-tuning/SKILL.md`.

### `cleanrl`

Role: Routes CleanRL script-oriented RL training tasks to algorithm, CLI, optional dependency, and safe-run guidance.
Read when: cleanrl, CleanRL, ppo.py, dqn.py, c51.py, Atari, EnvPool, Procgen, MuJoCo, PettingZoo, JAX, tyro, --total-timesteps, --env-id. cleanrl benchmark, cleanrl_utils.benchmark, wandb cleanRL, Optuna tuner, resume training, reproduce, Slurm, AWS Batch, Docker, Terraform, benchmark/*.sh.
Best for: Choosing and safely running CleanRL algorithms, inspecting script arguments, diagnosing missing RL backends, and adapting single-file training commands. Generating dry-run command matrices, checking credential readiness without leaking secrets, and planning cloud/container/Slurm operations safely.
Avoid when: The task is about a different RL library, general RL theory without CleanRL code, or executing long benchmark/cloud jobs without CleanRL-specific context. The task is only about selecting one training script or evaluating a saved model artifact; route those to the training or evaluation sub-skills.
Useful entry points: `cleanrl/SKILL.md`, `cleanrl/sub-skills/training-scripts/SKILL.md`, `cleanrl/sub-skills/experiment-operations/SKILL.md`.

### `gymnasium`

Role: Gymnasium provides the standard single-agent RL environment API plus spaces, wrappers, vectorized environment utilities, and reference built-in environments.
Read when: Use for tasks mentioning Gymnasium, gym.make, Env.reset, Env.step, terminated/truncated, action_space, observation_space, wrappers, RecordVideo, make_vec, SyncVectorEnv, AsyncVectorEnv, CartPole, Taxi, FrozenLake, MuJoCo, Box2D, Atari/ALE, action_mask, or old Gym migration.
Best for: Creating and validating Gymnasium Env loops or custom environments, choosing spaces, applying wrappers/recording, vectorizing RL rollouts, selecting built-in environment families, and troubleshooting optional extras or versioned environment IDs.
Avoid when: Do not choose gymnasium for RL algorithm implementations, replay buffers, policy optimization, model training frameworks, multi-agent PettingZoo environments, or Stable-Baselines3/CleanRL-specific training code unless the task specifically depends on Gymnasium environment APIs.
Useful entry points: `gymnasium/SKILL.md`, `gymnasium/sub-skills/environment-api/SKILL.md`, `gymnasium/sub-skills/spaces-data/SKILL.md`, `gymnasium/sub-skills/wrappers-recording/SKILL.md`, `gymnasium/sub-skills/vectorization/SKILL.md`, `gymnasium/sub-skills/builtin-envs/SKILL.md`.

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

### `ray`

Role: Use `ray` for RLlib-specific reinforcement-learning workflows that run on Ray and integrate with Ray Tune.
Read when: The task names RLlib, ray.rllib, PPOConfig, AlgorithmConfig, EnvRunner, Learner, Gymnasium custom env registration for Ray, multi-agent RL with Ray, RLlib checkpoint/evaluation, or RLlib Tune sweeps.
Best for: Configuring, validating, and troubleshooting RLlib workloads, especially PPO/custom Gymnasium envs, config-only checks, and Ray Tune integration.
Avoid when: Use another RL package skill for Stable-Baselines3, CleanRL, Tianshou, PettingZoo-only environments, or generic RL scripts that do not use Ray RLlib.
Useful entry points: `ray/sub-skills/rllib-workloads/SKILL.md`, `ray/sub-skills/train-tune/SKILL.md`, `ray/sub-skills/core-runtime/SKILL.md`.

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
Useful entry points: `trl/SKILL.md`, `trl/sub-skills/cli-and-configs/`, `trl/sub-skills/core-training/`, `trl/sub-skills/data-and-rewards/`, `trl/sub-skills/experimental-and-environments/`, `trl/sub-skills/repo-development/`, `trl/sub-skills/scaling-and-backends/`.

### `verl`

Role: Use verl for LLM post-training workflows: setup, data and rewards, PPO/GRPO/SFT configs, rollout tools, checkpoints, profiling, and repository maintenance.
Read when: The request names `verl` or asks for package-specific APIs, CLIs, configs, data/model artifacts, error messages, workflows, or repository maintenance that match this project.
Best for: checkpoints and model ops, data and rewards, repo development, rollout and tools, setup and backends, and training and configs.
Avoid when: another repo skill in this scenario matches the user's task, package, model family, data format, serving backend, or workflow more directly.
Useful entry points: `verl/SKILL.md`, `verl/sub-skills/checkpoints-and-model-ops/`, `verl/sub-skills/data-and-rewards/`, `verl/sub-skills/repo-development/`, `verl/sub-skills/rollout-and-tools/`, `verl/sub-skills/setup-and-backends/`, `verl/sub-skills/training-and-configs/`.

<!-- DISCO_SCENARIO:reinforcement-learning-workflows:END -->

## How To Choose

Choose by RL package and layer: Stable-Baselines3 for algorithms, CleanRL for single-file training scripts and operations, Tianshou for collectors/buffers/offline RL, PettingZoo for multi-agent environments, and OpenRLHF/TRL/verl only when the task is LLM post-training. Choose acme when the task includes Acme package/API names or Acme-style RL workflow signals such as dm_env specs, EnvironmentLoop, Reverb adders, JAX ExperimentConfig, TensorFlow Sonnet agents, Launchpad distributed Acme examples, or Acme algorithm builders. Choose agilerl when the user is using AgileRL's package APIs, YAML configs, evolvable architecture/HPO features, or AgileRL-specific training helpers rather than a different reinforcement learning framework. Prefer `cleanrl` over generic Python/ML guidance when the user names CleanRL or CleanRL script files; use training-scripts first for algorithm commands. Choose this scenario when the user asks how to run many experiments, track or reproduce results, or use CleanRL cloud/benchmark tooling. Choose gymnasium when the task is about the RL environment interface, environment IDs, spaces, wrappers, vectorized envs, or Gym-to-Gymnasium migration; choose algorithm/framework skills such as Stable-Baselines3, CleanRL, Tianshou, or PettingZoo when the user primarily asks about training algorithms, experiment scripts, collectors, buffers, or multi-agent APIs.
