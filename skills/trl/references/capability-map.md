# Capability Map

Use this map to choose the nearest sub-skill and depth reference without reopening TRL docs.

| Capability | Evidence used to build this skill | Output location | Depth check |
| --- | --- | --- | --- |
| Stable Python trainers: SFT, DPO, GRPO, RLOO, Reward | public imports, trainer docs, config signatures | [training](../sub-skills/training/SKILL.md), [training API](../sub-skills/training/references/api-reference.md), [training workflows](../sub-skills/training/references/workflows.md) | Trainer selection, dataset requirements, key args, examples, and troubleshooting are covered. |
| KTO and other experimental trainers | experimental docs, KTO docs, module layout | [experimental-agents](../sub-skills/experimental-agents/SKILL.md), [experimental map](../sub-skills/experimental-agents/references/experimental-map.md) | Stability warning, imports, and representative workflows are covered. |
| TRL CLI and packaged scripts | `pyproject.toml`, `trl/cli`, `trl/scripts`, CLI help | [cli-and-scripts](../sub-skills/cli-and-scripts/SKILL.md), [CLI reference](../sub-skills/cli-and-scripts/references/cli-reference.md) | Commands, YAML config patterns, accelerate launch behavior, and reusable config script are covered. |
| Dataset formats | dataset format docs, data utility signatures | [data-rewards-chat](../sub-skills/data-rewards-chat/SKILL.md), [data formats](../sub-skills/data-rewards-chat/references/data-formats.md) | Standard/conversational, LM, prompt-only, prompt-completion, preference, unpaired preference, and stepwise formats are covered. |
| Chat templates and tool calling | chat-template docs, helpers, bundled templates | [data-rewards-chat](../sub-skills/data-rewards-chat/SKILL.md), [rewards and chat templates](../sub-skills/data-rewards-chat/references/rewards-and-chat-templates.md) | Training template requirements, tool schemas, Harmony-style data, and known gotchas are covered. |
| Reward functions | `trl.rewards` exports and reward docs | [data-rewards-chat](../sub-skills/data-rewards-chat/SKILL.md), [reward smoke script](../sub-skills/data-rewards-chat/scripts/reward_smoke_test.py) | Built-in reward names, custom reward callable shapes, and safety checks are covered. |
| PEFT, quantization, memory | `ModelConfig`, memory docs, PEFT docs | [scaling-integrations](../sub-skills/scaling-integrations/SKILL.md), [distributed memory vLLM](../sub-skills/scaling-integrations/references/distributed-memory-vllm.md) | LoRA/QLoRA, batch sizing, truncation, packing, padding-free, activation offloading, and chunked loss are covered. |
| vLLM integration | vLLM docs, CLI help, GRPO/RLOO config fields | [scaling-integrations](../sub-skills/scaling-integrations/SKILL.md), [vLLM command builder](../sub-skills/scaling-integrations/scripts/vllm_server_command.py) | Server/colocate modes, separate GPU warning, server flags, and config args are covered. |
| Distributed training | Accelerate, DeepSpeed, examples configs docs | [scaling-integrations](../sub-skills/scaling-integrations/SKILL.md), [effective batch script](../sub-skills/scaling-integrations/scripts/effective_batch.py) | Effective batch, Accelerate config use, DeepSpeed, FSDP2, context/sequence parallelism are covered. |
| OpenEnv and OpenReward agent training | OpenEnv/OpenReward docs and examples | [experimental-agents](../sub-skills/experimental-agents/SKILL.md), [agent workflows](../sub-skills/experimental-agents/references/openenv-openreward-workflows.md) | `environment_factory`, tool method contract, reward access, OpenRewardSpec, local/self-hosted notes are covered. |
| TRL source development and review | AGENTS.md, CONTRIBUTING, tests, paper index, source layout | [repo-development](../sub-skills/repo-development/SKILL.md) | Duplication policy, paper index rule, docstring style, test targeting, and review checklist are covered. |

## File Tree

```text
trl/
  SKILL.md
  references/
    capability-map.md
    installation-and-dependencies.md
    troubleshooting.md
  scripts/
    check_env.py
    inspect_public_api.py
  sub-skills/
    training/
      SKILL.md
      references/api-reference.md
      references/workflows.md
      references/paper-recipes.md
      references/troubleshooting.md
      scripts/trainer_smoke_test.py
    cli-and-scripts/
      SKILL.md
      references/cli-reference.md
      references/configuration.md
      references/troubleshooting.md
      scripts/make_trl_config.py
      scripts/print_cli_summary.py
    data-rewards-chat/
      SKILL.md
      references/data-formats.md
      references/rewards-and-chat-templates.md
      references/preprocessing-recipes.md
      references/troubleshooting.md
      scripts/validate_dataset_jsonl.py
      scripts/reward_smoke_test.py
    scaling-integrations/
      SKILL.md
      references/distributed-memory-vllm.md
      references/integrations-compatibility.md
      references/troubleshooting.md
      scripts/effective_batch.py
      scripts/vllm_server_command.py
    experimental-agents/
      SKILL.md
      references/experimental-map.md
      references/openenv-openreward-workflows.md
      references/troubleshooting.md
      scripts/openenv_environment_template.py
    repo-development/
      SKILL.md
      references/contributing-standards.md
      references/duplicated-trainers-checklist.md
      references/tests-and-review.md
      references/troubleshooting.md
      scripts/check_paper_index.py
      scripts/find_trainer_pattern.py
```
