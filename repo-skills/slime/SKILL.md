---
name: slime
description: "Routes agents through self-contained slime skills for Megatron plus SGLang LLM post-training, RL, SFT, rollout customization, evaluation, checkpoint conversion, and distributed deployment."
disable-model-invocation: true
---

# slime

Use this repo skill when the user wants to set up or operate **slime**, the THUDM LLM post-training framework that couples Megatron training with SGLang rollout serving.

The skill is intentionally a router. Load the nearest sub-skill for the requested workflow, then read only the references or scripts linked by that sub-skill.

## Install And Verify

Preferred production setup is the public Docker image:

```bash
docker pull slimerl/slime:latest
docker run --rm --gpus all --ipc=host --shm-size=16g \
  --ulimit memlock=-1 --ulimit stack=67108864 \
  -it slimerl/slime:latest /bin/bash
```

For source installs, clone the public repo and install in an environment that already has compatible CUDA, SGLang, Megatron-LM, and native kernels:

```bash
git clone https://github.com/THUDM/slime.git
cd slime
pip install -r requirements.txt
pip install -e . --no-deps
```

`slime` has no console entry point. Training normally needs `PYTHONPATH` to include a full Megatron-LM checkout that provides `megatron.training`. Check the installed package and optional training stack with [scripts/check_env.py](scripts/check_env.py):

```bash
python /path/to/skill/slime/scripts/check_env.py
python /path/to/skill/slime/scripts/check_env.py --strict-train --megatron-path /path/to/Megatron-LM
```

If the user has no source checkout, use the bundled training entrypoints [scripts/run_slime_train.py](scripts/run_slime_train.py) and [scripts/run_slime_train_async.py](scripts/run_slime_train_async.py). They mirror slime's public `train.py` and `train_async.py` flow using the installed `slime` package.

Read [references/installation.md](references/installation.md) for environment decisions, Docker/source tradeoffs, Megatron requirements, and the minimum runtime checks. Read [references/qwen3-0-6b-happy-path.md](references/qwen3-0-6b-happy-path.md) when the user wants the smallest Qwen3-0.6B SFT or GRPO pipeline. Read [references/troubleshooting.md](references/troubleshooting.md) when imports, Ray jobs, SGLang startup, checkpoint loading, or training stability fail. Read [references/coverage-matrix.md](references/coverage-matrix.md) when auditing whether a requested slime workflow is covered.

## Root Scripts

- Run [scripts/check_env.py](scripts/check_env.py) before any serious slime job to verify imports and optional Megatron training support.
- Use [scripts/run_slime_train.py](scripts/run_slime_train.py) and [scripts/run_slime_train_async.py](scripts/run_slime_train_async.py) as source-free training entrypoints.
- Adapt [scripts/launch_ray_job_template.sh](scripts/launch_ray_job_template.sh) when building Ray job submission wrappers.
- Use [scripts/inspect_model_recipe.py](scripts/inspect_model_recipe.py) to print bundled model argument recipes; it reads [scripts/model_recipes.json](scripts/model_recipes.json), which is bundled data for the script.
- Use [scripts/convert_hf_to_torch_dist.py](scripts/convert_hf_to_torch_dist.py) and [scripts/convert_torch_dist_to_hf.py](scripts/convert_torch_dist_to_hf.py) for checkpoint conversion without depending on the original source checkout.
- Run [scripts/validate_sglang_config.py](scripts/validate_sglang_config.py) before large jobs that use `--sglang-config`.
- Read or copy [scripts/minimal_custom_hooks.py](scripts/minimal_custom_hooks.py) when starting custom rollout, reward, or generation hook modules.

## Sub-Skill Router

- Use [slime-environment-setup](sub-skills/slime-environment-setup/SKILL.md) for Docker/source setup, Ray startup, runtime env JSON, and launch shell scaffolding.
- Use [slime-checkpoint-conversion](sub-skills/slime-checkpoint-conversion/SKILL.md) for Hugging Face to Megatron `torch_dist`, Megatron to HF export, FP8/INT4 conversion commands, and checkpoint layout checks.
- Use [slime-model-recipes](sub-skills/slime-model-recipes/SKILL.md) for bundled Megatron model-architecture argument blocks covering Qwen, GLM, DeepSeek, Llama, GPT-OSS, Mimo, Moonlight, MiniMax, and Kimi families.
- Use [slime-rl-training](sub-skills/slime-rl-training/SKILL.md) for standard GRPO, GSPO, REINFORCE++, PPO-like policy training with Megatron actor and SGLang rollout.
- Use [slime-sft-training](sub-skills/slime-sft-training/SKILL.md) for supervised fine-tuning through `slime.rollout.sft_rollout.generate_rollout` and `loss_type=sft_loss`.
- Use [slime-sglang-deployment](sub-skills/slime-sglang-deployment/SKILL.md) for SGLang server flags, router flags, `--sglang-config`, multi-model serving, external rollout engines, and topology validation.
- Use [slime-pd-disaggregation](sub-skills/slime-pd-disaggregation/SKILL.md) for prefill/decode disaggregation via `--prefill-num-servers` or `--sglang-config` server groups.
- Use [slime-delta-weight-sync](sub-skills/slime-delta-weight-sync/SKILL.md) for non-colocated delta weight sync over disk or NCCL.
- Use [slime-low-precision](sub-skills/slime-low-precision/SKILL.md) for BF16 training with FP8 rollout, FP8 KV cache, FP8 training, and INT4 QAT/rollout conversion.
- Use [slime-ppo-megatron-config](sub-skills/slime-ppo-megatron-config/SKILL.md) for PPO actor/critic resources and `--megatron-config-path` role-specific overrides.
- Use [slime-on-policy-distillation](sub-skills/slime-on-policy-distillation/SKILL.md) for OPD with SGLang or Megatron teachers.
- Use [slime-custom-rollout](sub-skills/slime-custom-rollout/SKILL.md) for custom rollout, custom generate, reward model, filters, losses, data sources, evaluation functions, and Megatron hooks.
- Use [slime-agentic-tool-use](sub-skills/slime-agentic-tool-use/SKILL.md) for Search-R1, ReTool, Tau-bench, Strands, multi-agent, coding-agent, sandbox, RAG, and tool-use rollout patterns.
- Use [slime-coding-agent-rl](sub-skills/slime-coding-agent-rl/SKILL.md) for SWE/coding-agent RL, Anthropic/OpenAI adapter routing, sandbox metadata, patch grading, and token-provenance checks.
- Use [slime-fully-async-rollout](sub-skills/slime-fully-async-rollout/SKILL.md) for `train_async.py` plus `slime.rollout.fully_async_rollout.generate_rollout_fully_async`.
- Use [slime-speculative-decoding](sub-skills/slime-speculative-decoding/SKILL.md) for SGLang speculative decoding, EAGLE/MTP flags, draft model paths, and online MTP training.
- Use [slime-vlm-training](sub-skills/slime-vlm-training/SKILL.md) for multimodal/VLM SFT and RL, GEO3K-style single-turn or multi-turn tasks, and `--multimodal-keys`.
- Use [slime-evaluation](sub-skills/slime-evaluation/SKILL.md) for periodic eval, `--eval-prompt-data`, structured `--eval-config`, multi-task eval, and custom eval rollout.
- Use [slime-rollout-correction](sub-skills/slime-rollout-correction/SKILL.md) for TIS/MIS, rollout logprob bypass, mismatch metrics, and train-inference mismatch mitigation.
- Use [slime-debug-trace-profile](sub-skills/slime-debug-trace-profile/SKILL.md) for rollout-only and train-only debugging, saved rollout replay, timeline traces, SGLang profiling, and CI-oriented checks.
- Use [slime-fault-tolerance-reproducibility](sub-skills/slime-fault-tolerance-reproducibility/SKILL.md) for rollout health checks, deterministic inference/training flags, resume patterns, and long-running stability.
- Use [slime-amd-rocm](sub-skills/slime-amd-rocm/SKILL.md) for AMD/ROCm deployment notes and ROCm-specific launch adjustments.

## Common Routing Rules

- If the request is "run a normal RL job", start with `slime-rl-training`; pull in `slime-checkpoint-conversion`, `slime-model-recipes`, and `slime-environment-setup` only as needed.
- If the request is "SFT", start with `slime-sft-training`, not the RL skill.
- If the request involves tool calls, search, RAG, sandbox execution, or multi-turn environment feedback, start with `slime-agentic-tool-use`, then use `slime-custom-rollout` for hook signatures. For SWE/coding-agent RL, route directly to `slime-coding-agent-rl` after confirming it is not a simpler tool-use rollout.
- If the request is mostly SGLang topology, multi-model serving, or external engines, start with `slime-sglang-deployment`.
- If the request is rollout speed via draft tokens, EAGLE, or MTP, start with `slime-speculative-decoding` and pull in SGLang deployment only for topology or memory tuning.
- If a failure occurs before training starts, inspect `slime-environment-setup` and root troubleshooting first. If the failure occurs during generation, inspect SGLang, debug/trace/profile, and fault-tolerance skills.

## Package Facts

- Public package name: `slime`
- Verified package version during extraction: `0.2.4`
- Python requirement: `>=3.10`
- Import packages: `slime`, `slime_plugins`
- No verified `console_scripts` entry point
- Main workflow entrypoints are Python scripts or equivalent bundled runners, plus Ray job submission.
