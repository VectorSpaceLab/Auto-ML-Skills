# Python Repository Maintenance

## When To Read

Tasks that edit, review, test, document, package, or maintain Python source repositories rather than using them only as libraries.

## Repo Skill Options

<!-- DISCO_SCENARIO:python-repository-maintenance:START -->
### `cleanrl`

Role: Keeps CleanRL changes aligned with single-file implementation conventions, docs/tests, optional extras, and focused validation.
Read when: modify cleanrl script, add CLI flag, update docs/rl-algorithms, tests/test_*.py, pyproject.toml, requirements, CONTRIBUTING, RLOps regression.
Best for: Selecting focused native checks, preserving CleanRL style, updating docs and tests after script changes, and planning performance regression validation.
Avoid when: The user only wants to run an existing CleanRL command without changing the repository.
Useful entry points: `cleanrl/SKILL.md`, `cleanrl/sub-skills/repo-maintenance/SKILL.md`.

### `crewai`

Role: Captures CrewAI monorepo layout, docs snapshot rules, workspace package boundaries, and safe maintainer verification guidance.
Read when: CrewAI checkout, AGENTS.md docs rules, docs/edge, docs/v snapshots, Mintlify docs, lib/crewai tests, crewai workspace pyproject, release freeze, docs image rules.
Best for: Choosing focused pytest/ruff/mypy/docs checks, editing Edge docs safely, avoiding frozen snapshot and image hazards, and mapping changed paths to native verification candidates.
Avoid when: The user is only building an application with installed CrewAI and is not editing the CrewAI repository itself.
Useful entry points: `crewai/SKILL.md`, `crewai/sub-skills/repo-development/SKILL.md`.

### `prefect`

Role: Provides Prefect-specific repository structure, AGENTS-scoped development rules, test selection, generated artifact handling, and package-boundary guidance.
Read when: src/prefect, tests, docs/v3, client/pyproject.toml, uv.lock, AGENTS.md, just generate-docs, generated schema, prefect-client build.
Best for: Selecting focused tests and validation commands, respecting source/test mirrors and scoped AGENTS rules, updating generated docs/schemas/settings, and avoiding server state-transition anti-patterns.
Avoid when: The request only asks how to use Prefect as an end user, or it targets frontend implementation details under ui-v2 or provider integrations under src/integrations.
Useful entry points: `prefect/SKILL.md`, `prefect/sub-skills/repo-development/SKILL.md`.

### `pydantic-ai`

Role: Captures Pydantic AI repository layout, contribution philosophy, targeted validation, cassette workflows, docs examples, and generated-skill refresh expectations.
Read when: User mentions editing this checkout, AGENTS.md, agent_docs, uv workspace, pyright, ruff, pytest cassettes, VCR, inline snapshots, docs examples, PR review, or Pydantic AI maintainer workflows.
Best for: Choosing narrow validation commands, recording or replaying provider cassettes, updating docs/examples/tests, reviewing public API changes, and refreshing generated repo skills after code drift.
Avoid when: The user only wants to use Pydantic AI as an installed dependency and is not editing the repository.
Useful entry points: `pydantic-ai/SKILL.md`, `pydantic-ai/sub-skills/repo-development/SKILL.md`.

### `skypilot`

Role: Provides SkyPilot-specific maintainer guidance for coding conventions, risky code paths, focused tests, formatting, protobuf/dashboard regeneration, API compatibility, and PR handoff.
Read when: SkyPilot repo, AGENTS.md, format.sh, pytest SkyPilot, API_VERSION, protobuf regeneration, dashboard build, managed jobs recovery, API server performance, SkyPilot PR Tested section.
Best for: Editing SkyPilot code safely, selecting focused unit/smoke tests, avoiding generated-file mistakes, and preparing compatibility-aware code review notes.
Avoid when: The user only wants to run workloads with SkyPilot rather than modify the SkyPilot repository; use the end-user scenario instead.
Useful entry points: `skypilot/SKILL.md`, `skypilot/sub-skills/repo-development/SKILL.md`.

### `stable-diffusion-webui`

Role: Provides repo-specific maps of launch, API, extension, asset, and training modules plus safe bundled helpers for source auditing without starting WebUI.
Read when: User asks to edit WebUI source, inspect cmd_args.py, inspect modules/api/api.py, update extension callbacks, adapt built-in scripts, or understand native tests in the checkout.
Best for: Repository changes that require Stable Diffusion WebUI domain context before editing or testing.
Avoid when: Use a generic Python maintenance skill when the task is formatting, linting, packaging, or CI plumbing with no WebUI-specific behavior.
Useful entry points: `stable-diffusion-webui/SKILL.md`, `stable-diffusion-webui/scripts/inspect_webui_source.py`.

<!-- DISCO_SCENARIO:python-repository-maintenance:END -->

## How To Choose

Choose this scenario when the user is contributing to or modifying a repo checkout; otherwise choose the user-facing workflow scenario for the package. Use this scenario for maintainer-style code and documentation tasks; cross-route to training-scripts for flag semantics and experiment-operations for benchmarks. Use the repo-development route only for current-checkout contribution tasks; normal CrewAI app usage should start at core-runtime, flows, CLI/projects, tools/MCP, or provider sub-skills. Route maintainer edits to repo-development first, then cross-link to user-facing sub-skills only when behavior or docs need verification against public workflows. Use the repo-development sub-skill for maintainer tasks, and use the user-facing sub-skills when the task is about application code that consumes Pydantic AI. Choose repo-development only for source-maintenance tasks; choose ai-compute-orchestration for normal SkyPilot usage. Use the relevant sub-skill to understand the domain surface, then apply normal repo-maintenance practices for code edits and tests.
