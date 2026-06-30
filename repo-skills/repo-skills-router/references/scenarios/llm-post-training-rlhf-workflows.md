# LLM Post-Training and RLHF Workflows

## When To Read

SFT, DPO, GRPO, PPO, reward models, RLHF data/rewards, rollout engines, post-training configs, LoRA merging, Ray/Megatron distributed RLHF, and preference optimization backends.

## Repo Skill Options

<!-- DISCO_SCENARIO:llm-post-training-rlhf-workflows:START -->
### `agilerl`

Role: AgileRL-specific guidance for LLM RL fine-tuning and post-training workflows implemented by AgileRL algorithms and trainers.
Read when: Use when the request names AgileRL plus GRPO, CISPO, GSPO, DPO, SFT, LLM PPO, LLM REINFORCE, AgileRL LLM envs, `finetune_llm_reasoning`, `finetune_llm_preference`, `finetune_llm_multiturn`, `finetune_llm_sft`, vLLM sleep/wake handoff, or `agilerl[llm]` optional dependencies.
Best for: Planning AgileRL LLM fine-tuning configs, optional dependency checks, reasoning/preference/multiturn/SFT trainer selection, checkpoint/quantization handling, and safe dry-run validation without model downloads.
Avoid when: Use other RLHF or LLM fine-tuning skills when the package is TRL, OpenRLHF, verl, Axolotl, LlamaFactory, ms-swift, or a serving-only stack and AgileRL is not involved.
Useful entry points: `agilerl/SKILL.md`, `agilerl/sub-skills/llm-fine-tuning/SKILL.md`.

### `ms-swift`

Role: Explains ms-swift advanced RL and distributed execution routes with optional dependency and parallelism caveats.
Read when: swift rlhf, swift sample, swift rollout, megatron sft, megatron rlhf, GRPO, GKD, reward_func, ORM, PRM, Ray device_groups, TP, PP, CP, EP, Mcore-Bridge.
Best for: Planning reward/plugin signatures, rollout placement, Ray YAML, Megatron parallel dimensions, and optional backend checks.
Avoid when: The task is ordinary SFT/pretraining without RL or Megatron/Ray-specific execution.
Useful entry points: `ms-swift/SKILL.md`, `ms-swift/sub-skills/advanced-rl-distributed/SKILL.md`.

### `openrlhf`

Role: Use OpenRLHF for Ray/vLLM/DeepSpeed RLHF workflows, including dataset preparation, SFT/RM/DPO training, PPO-family RL and agent training, runtime operations, reward serving, LoRA merging, and troubleshooting.
Read when: The request names `openrlhf` or asks for package-specific APIs, CLIs, configs, data/model artifacts, error messages, workflows, or repository maintenance that match this project.
Best for: data preparation, operations and utilities, rl agent training, and supervised preference training.
Avoid when: another repo skill in this scenario matches the user's task, package, model family, data format, serving backend, or workflow more directly.
Useful entry points: `openrlhf/SKILL.md`, `openrlhf/sub-skills/data-preparation/`, `openrlhf/sub-skills/operations-and-utilities/`, `openrlhf/sub-skills/rl-agent-training/`, `openrlhf/sub-skills/supervised-preference-training/`.

### `torchtune`

Role: Guides torchtune's PyTorch-native LLM post-training recipes, configs, RLHF utilities, and safe command planning.
Read when: The request names torchtune, tune run, LoRA, QLoRA, DPO, PPO, KD, QAT, GRPO, recipe configs, checkpoint resume, or torchtune.rlhf.
Best for: Selecting and adapting torchtune post-training recipes, validating configs/data, planning distributed launches, and debugging torchtune-specific post-training failures.
Avoid when: The request is about a different training framework such as Axolotl, LlamaFactory, TRL, OpenRLHF, or generic Transformers APIs with no torchtune-specific surface.
Useful entry points: `torchtune/SKILL.md`, `torchtune/sub-skills/post-training-recipes/SKILL.md`, `torchtune/sub-skills/training-utilities-and-rlhf/SKILL.md`.

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

<!-- DISCO_SCENARIO:llm-post-training-rlhf-workflows:END -->

## How To Choose

Choose this scenario when the request is about preference optimization or RLHF/post-training; choose the generic LLM training scenario for ordinary SFT or serving. Choose agilerl for LLM post-training only when AgileRL's algorithms, trainers, configs, or optional `[llm]` extras are part of the workflow. Choose `ms-swift` for ms-swift advanced RL/distributed workflows even when they also mention datasets or inference; use sibling sub-skills for shared schema or serving details. Choose `openrlhf` when the request names `openrlhf`, centers on Ray/vLLM/DeepSpeed RLHF workflows, including dataset preparation, SFT/RM/DPO training, PPO-family RL and agent training, runtime operations, reward serving, LoRA merging, and troubleshooting, uses its APIs or CLIs, references its configs/artifacts/errors, or asks for repository workflows in llm post training rlhf workflows. Choose torchtune when the workflow is explicitly `tune` CLI, torchtune recipe/config, PyTorch-native post-training, or torchtune RLHF utility work; choose neighboring RLHF/training skills when their package owns the runtime.
