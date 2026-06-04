# Tests And Review

Use this when selecting tests or reviewing a TRL change.

## Test Targeting

Stable trainer tests:

- `tests/test_sft_trainer.py`
- `tests/test_dpo_trainer.py`
- `tests/test_grpo_trainer.py`
- `tests/test_rloo_trainer.py`
- `tests/test_reward_trainer.py`

Utilities:

- `tests/test_data_utils.py`
- `tests/test_chat_template_utils.py`
- `tests/test_rewards.py`
- `tests/test_model_utils.py`
- `tests/test_callbacks.py`
- `tests/test_cli.py`
- `tests/test_cli_utils.py`
- `tests/test_vllm_client_server.py`

Experimental:

- `tests/experimental/test_<feature>_trainer.py`
- `tests/experimental/test_openreward.py`

Distributed:

- `tests/distributed/test_distributed.py`
- `tests/invariant/test_invariant.py`

Skills:

- `tests/test_skills.py`
- `tests/test_skills_cli.py`

## Choosing Scope

- Single trainer config/default change: run that trainer's test file and any config/parser tests.
- Data format or chat template change: run `tests/test_data_utils.py`, `tests/test_chat_template_utils.py`, and touched trainer tests.
- Reward change: run `tests/test_rewards.py` plus GRPO/RLOO tests when reward integration changes.
- vLLM change: run GRPO/RLOO tests and `tests/test_vllm_client_server.py`; add distributed/slow tests only when relevant and available.
- CLI/script change: run `tests/test_cli.py`, `tests/test_cli_utils.py`, and smoke the command help.
- Experimental change: run the corresponding `tests/experimental` file plus any stable utilities it touches.
- Paper-backed method: also verify `docs/source/paper_index.md`.

## Review Findings

Lead with actionable findings. Include file and line references when reviewing a real diff.

Prioritize:

- Incorrect behavior or regression.
- Missing duplicated-trainer propagation.
- Missing tests for touched behavior.
- Missing paper-index update.
- Unstable experimental API treated as stable.
- Inconsistent docstring format.
- CLI flag or config key breakage.
- Memory/distributed behavior that will fail on common setups.

## Paper Review Checklist

- Paper link uses `https://huggingface.co/papers/<id>`.
- `docs/source/paper_index.md` has a subsection.
- Config snippet uses actual config fields.
- Unsupported paper features are called out rather than implied.
- Dataset and reward assumptions are stated.

## CLI Review Checklist

- `make_parser()` exists for script-backed commands.
- New CLI args are dataclass fields or parser args with matching help.
- YAML config keys use dataclass field names.
- Accelerate launch args are not accidentally passed into script-only parsing.

## Documentation Review Checklist

- Docstrings use TRL/Hugging Face style.
- Docs link to generated or bundled content that exists.
- Examples use public imports where possible.
- Experimental examples include stability context.
