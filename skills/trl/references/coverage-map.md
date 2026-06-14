# Coverage Map

This reference records the evidence categories and capability map used by the generated skill. Use it when checking whether a TRL request has a matching sub-skill or when extending the skill.

## Evidence Used

| Evidence source | Why it matters | Skill use |
| --- | --- | --- |
| `pyproject.toml` | Package name, Python version, dependencies, extras, CLI entry point | Install and environment guidance |
| `README.md`, `docs/source/quickstart.md`, `docs/source/installation.md` | Public overview, quick examples, install paths | Root skill, trainer workflow examples |
| `docs/source/clis.md` and live `trl --help` | CLI commands, config files, Accelerate integration | `cli-training` |
| `docs/source/sft_trainer.md`, `dpo_trainer.md`, `grpo_trainer.md`, `reward_trainer.md`, `rloo_trainer.md` | Stable trainer workflows, dataset formats, metrics, customization | `core-trainers` |
| `docs/source/dataset_formats.md`, `chat_templates.md`, `rewards.md`, `script_utils.md` | Dataset schemas, chat template requirements, reward functions, parser utilities | `data-and-rewards` |
| `docs/source/vllm_integration.md`, `distributing_training.md`, `reducing_memory_usage.md`, `peft_integration.md` | Generation acceleration, distributed launch, memory and adapter options | `vllm-and-distributed` |
| `docs/source/experimental_overview.md` and experimental trainer docs | Unstable trainer catalog and warnings | `experimental-trainers` |
| `trl/skills/*.py`, `trl/skills/trl-training/SKILL.md`, live `trl skills --help` | Built-in agent-skill management behavior | `agent-skills-management` |
| Installed package inspection | Verified live imports, signatures, CLI commands, entry point metadata | API and CLI references |
| Tests under `tests/` | CLI, skill utilities, data utilities, rewards, and trainer behavior patterns | Troubleshooting and verification checks |

## Coverage Matrix

| Capability | Output location | Depth check |
| --- | --- | --- |
| Install TRL and verify environment | Root skill, `references/install-and-environment.md`, `scripts/check_trl_environment.py` | Includes public install commands, extras, import checks, CLI check, backend caveats |
| Stable Python trainer APIs | `sub-skills/core-trainers/` | Covers SFT, DPO, GRPO, RewardTrainer, RLOO with dataset expectations, minimal code, signatures, config notes |
| CLI training jobs | `sub-skills/cli-training/` | Covers `trl sft/dpo/grpo/reward/rloo/kto`, YAML configs, shared flags, Accelerate launch |
| Dataset schemas and chat templates | `sub-skills/data-and-rewards/` | Covers standard/conversational formats, preference/unpaired/stepwise types, tool calling, multimodal helpers |
| Reward functions | `sub-skills/data-and-rewards/` | Covers built-in reward signatures and custom reward callable shape for GRPO/RLOO |
| vLLM and distributed execution | `sub-skills/vllm-and-distributed/` | Covers `trl[vllm]`, `trl vllm-serve`, colocate/server modes, Accelerate, DeepSpeed, FSDP, memory reduction |
| Experimental trainers | `sub-skills/experimental-trainers/` | Names risk model, common import pattern, selected algorithms, paper-index requirement for contributors |
| TRL agent-skill CLI | `sub-skills/agent-skills-management/` | Covers `trl skills list/install/uninstall`, target scopes, Python utilities |

## Intentional Scope Limits

- The skill does not bundle full paper derivations or complete trainer docs. It gives practical routing, verified APIs, compact recipes, and troubleshooting anchors.
- Training commands are examples and may download models/datasets when run. Bundled scripts avoid downloads and training.
- vLLM, DeepSpeed, quantization, and kernel package installation depends on hardware and wheel availability. Verify the backend separately before promising a GPU run.
- Experimental trainer guidance marks instability explicitly. Future agents should inspect current package exports before relying on experimental APIs.
