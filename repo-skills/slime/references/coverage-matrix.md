# slime Coverage Matrix

This matrix records the public workflows covered by the generated skill tree. Use it during review when a user asks for a slime capability and the correct sub-skill is not obvious.

| Capability | Evidence Source | Output Location | Depth Check |
| --- | --- | --- | --- |
| Environment setup, Docker, source install, Ray launch | README, quick start, Docker docs, build script | `slime-environment-setup`, root references/scripts | Includes Docker/source install, Ray head/job templates, runtime-env rules, Megatron preflight |
| HF to Megatron and Megatron to HF conversion | Quick start, conversion tools, checkpoint docs | `slime-checkpoint-conversion` | Includes checkpoint layout, conversion commands, model args, common export pitfalls |
| Model architecture argument recipes | `scripts/models/*.sh`, quick start usage | `slime-model-recipes` | Includes model family map and a reusable recipe-selection script |
| Standard RL training | README, usage guide, run scripts, examples | `slime-rl-training` | Covers resource math, args blocks, GRPO/GSPO/REINFORCE++/PPO decision points, bundled launcher |
| SFT training | SFT run scripts, SFT rollout module, examples | `slime-sft-training` | Covers `sft_rollout`, loss flags, data format, no-advantage path, bundled launcher |
| SGLang deployment and router | Usage guide, SGLang config advanced doc | `slime-sglang-deployment` | Covers `--sglang-*`, router flags, external engines, YAML validation, multi-model serving |
| PD disaggregation | PD advanced doc, SGLang config doc | `slime-pd-disaggregation` | Covers legacy and YAML paths, prefill/decode groups, capacity checks |
| Delta weight sync | Delta advanced doc and example | `slime-delta-weight-sync` | Covers mode/transport/encoding choices, non-colocate constraint, disk/NCCL templates |
| Low precision | Low precision advanced doc, low precision scripts | `slime-low-precision` | Covers FP8 rollout, FP8 KV cache, FP8 training, INT4 QAT, conversion commands |
| PPO actor/critic Megatron config | Usage PPO section, Megatron config doc | `slime-ppo-megatron-config` | Covers resource math, YAML schema, role overrides, critic-only warmup |
| On-policy distillation | OPD advanced doc and examples | `slime-on-policy-distillation` | Covers SGLang vs Megatron teacher modes and required flags |
| Custom rollout/hook interfaces | Customization guide, plugin contract tests | `slime-custom-rollout` | Includes verified signatures, templates, and contract-test guidance |
| Agentic tool use | Search-R1, ReTool, Tau-bench, Strands, multi-agent, coding-agent examples | `slime-agentic-tool-use` | Covers hook selection, dataset metadata, sandbox/tool dependencies, TITO cautions |
| Fully async rollout | Fully async example and module | `slime-fully-async-rollout` | Covers async driver, function path, limitations, queue behavior |
| VLM training | GEO3K VLM examples and docs | `slime-vlm-training` | Covers multimodal data, `--multimodal-keys`, VLM SFT/RL, backend caveats |
| Evaluation | Quick start eval args, eval config example | `slime-evaluation` | Covers CLI pair and YAML config, per-dataset overrides, custom eval |
| Rollout correction | Train-infer mismatch example, TIS flags | `slime-rollout-correction` | Covers TIS/MIS flags, logprob requirements, mismatch metrics |
| Debug, trace, profile | Debug/trace/profile docs, tools, tests | `slime-debug-trace-profile` | Covers debug-only modes, saved rollout replay, trace instrumentation, profile calls |
| Fault tolerance and reproducibility | Fault tolerance and reproducibility docs, FAQ | `slime-fault-tolerance-reproducibility` | Covers health checks, deterministic flags, resume and stop-token issues |
| AMD/ROCm | AMD tutorial, ROCm docker files, AMD script | `slime-amd-rocm` | Covers ROCm launch caveats and AMD-specific args |

Breadth rule: if a user asks for a workflow above, route to the named sub-skill before writing commands. Depth rule: a future agent should be able to complete ordinary setup or command generation from the sub-skill plus its linked files without reopening the original slime repository.
