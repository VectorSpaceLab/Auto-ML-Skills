---
name: trl-repo-development
description: Modify or review TRL source code while preserving trainer duplication consistency, docstring style, paper index rules, tests, and contribution standards.
license: Apache-2.0
---

# TRL Repo Development

Use this sub-skill when editing or reviewing TRL source, docs, tests, examples, scripts, trainers, configs, experimental modules, or packaged TRL skills.

## Core Repository Rules

- Main code should remain stable, consistent, and well-tested.
- Experimental code may be less stable, but avoid large refactors unless requested.
- Trainers are intentionally self-contained. Duplicated generation, reward, metric, vLLM, and input-preparation logic must stay aligned across trainers.
- Do not introduce shared abstractions merely to remove trainer duplication.
- If a PR implements a paper-backed method, algorithm, or training approach, update `docs/source/paper_index.md`.
- Use Hugging Face paper links: `https://huggingface.co/papers/<id>`.
- Preserve TRL docstring style.

Read [references/contributing-standards.md](references/contributing-standards.md) for style and contribution rules, and [references/duplicated-trainers-checklist.md](references/duplicated-trainers-checklist.md) before changing trainer internals.

## Source Layout

- Stable trainers: `trl/trainer/*_trainer.py` and `trl/trainer/*_config.py`.
- Stable CLI scripts: `trl/scripts/*.py`.
- CLI command wrappers: `trl/cli/commands/*.py`.
- Data/chat utilities: `trl/data_utils.py`, `trl/chat_template_utils.py`.
- Rewards: `trl/rewards/*.py`.
- vLLM generation: `trl/generation/*.py`.
- Experimental trainers: `trl/experimental/**`.
- Docs: `docs/source/*.md`.
- Examples: `examples/scripts`, `examples/notebooks`, `examples/accelerate_configs`.
- Tests: `tests/test_*.py`, `tests/experimental/test_*.py`, `tests/distributed`, `tests/invariant`.

## Development Workflow

1. Read the nearest trainer/config/docs/tests before editing.
2. Search for duplicated logic before changing trainer internals:

   ```bash
   rg "_last_loaded_step|_metrics\\[mode\\]|_generate_single_turn|_calculate_rewards|_prepare_inputs" trl
   ```

3. Make the smallest direct change that matches local patterns.
4. Update docs/examples if behavior or public API changes.
5. Update `docs/source/paper_index.md` for paper-backed methods.
6. Run focused tests first, then broader tests if shared behavior changed.

Use [scripts/find_trainer_pattern.py](scripts/find_trainer_pattern.py) to find duplicated trainer blocks and [scripts/check_paper_index.py](scripts/check_paper_index.py) to check for Hugging Face paper-link style.

## Fast Test Map

| Change area | Start with |
| --- | --- |
| Stable trainer | `tests/test_<trainer>_trainer.py` |
| Experimental trainer | `tests/experimental/test_<feature>_trainer.py` |
| Data or chat template | `tests/test_data_utils.py`, `tests/test_chat_template_utils.py` |
| Rewards | `tests/test_rewards.py` plus online trainer tests if integrated |
| CLI/scripts | `tests/test_cli.py`, `tests/test_cli_utils.py` |
| vLLM | `tests/test_vllm_client_server.py` plus GRPO/RLOO tests |
| Packaged skills | `tests/test_skills.py`, `tests/test_skills_cli.py` |

## Review Stance

When reviewing, lead with findings:

- Behavioral regressions.
- Missing consistency updates across duplicated trainers.
- Missing tests.
- Missing `paper_index.md` updates for paper-backed methods.
- Incorrect docstring format.
- Broken CLI/config compatibility.
- Experimental API exposed as stable.

## References

- [references/contributing-standards.md](references/contributing-standards.md): Contribution, docstring, paper-link, and simplicity rules.
- [references/duplicated-trainers-checklist.md](references/duplicated-trainers-checklist.md): What to verify when touching trainer internals.
- [references/tests-and-review.md](references/tests-and-review.md): Test targeting and review checklists.
- [references/troubleshooting.md](references/troubleshooting.md): Common development pitfalls.
