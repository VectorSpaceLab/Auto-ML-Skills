# TRL Skill Usability Cases

These cases exercise the generated `trl` skill and its sub-skills.

| Case | Target | User role | Scenario | Capability | Difficulty |
| --- | --- | --- | --- | --- | --- |
| `core-trainers-sft-lora-recipe` | `core-trainers` | Practitioner new to TRL Python APIs | Build an SFT LoRA trainer recipe | SFT, PEFT, dataset schema, verification | Intermediate |
| `core-trainers-grpo-reward-debugging` | `core-trainers` / `data-and-rewards` | Experienced RLHF user | Diagnose flat GRPO rewards | GRPO reward functions and metrics | Troubleshooting |
| `cli-training-yaml-sft-config` | `cli-training` | User prefers terminal workflows | Convert an SFT run to YAML and CLI command | CLI configs and flags | Basic |
| `data-and-rewards-tool-calling-sft` | `data-and-rewards` | Dataset engineer | Prepare tool-calling chat data for SFT | Conversational data, tools, JSON schema | Advanced |
| `vllm-and-distributed-server-mode` | `vllm-and-distributed` | ML platform engineer | Configure GRPO with a separate vLLM server | vLLM serve, server mode, memory flags | Advanced |
| `experimental-trainers-kto-warning` | `experimental-trainers` | Researcher | Use KTO and handle experimental API warning | Experimental imports and KTO data | Intermediate |
| `agent-skills-management-install-codex` | `agent-skills-management` | Agent tooling maintainer | Install TRL bundled skills into Codex | `trl skills` CLI and target scopes | Basic |

## Coverage Note

The case set covers every generated sub-skill and each major capability from the coverage matrix: stable Python trainers, CLI/YAML workflows, dataset and reward utilities, vLLM/distributed execution, experimental trainers, and TRL agent-skill management. The cases are intentionally broad enough to test natural triggering without mentioning the generated skill directory.
