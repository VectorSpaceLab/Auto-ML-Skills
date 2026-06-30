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

### `deepmd-kit`

Role: Provides DeePMD-kit-specific maintainer guidance, targeted validation commands, backend-aware build cautions, C++ build timing expectations, lint/format policy, and conventional commit guidance.
Read when: The request involves modifying DeePMD-kit source files, `deepmd/main.py`, backend modules, docs, examples, C++ APIs, LAMMPS/i-PI/native integration code, source builds, focused pytest selection, `ruff`, `uv`, `build_cc.sh`, or repository-specific CI/build failures.
Best for: Planning safe DeePMD-kit code changes, selecting focused tests instead of the full suite, running build/lint commands with appropriate timeouts, and keeping changes consistent with maintainer instructions.
Avoid when: The user only wants to train or run a DeePMD model as a package user; use the molecular workflow scenario entry points instead.
Useful entry points: `deepmd-kit/SKILL.md`, `deepmd-kit/sub-skills/integrations-development/SKILL.md`, `deepmd-kit/sub-skills/installation-backends/SKILL.md`.

### `galaxy`

Role: Galaxy provides repo-specific routing for server configuration, HTTP APIs, tool and workflow development, data/storage systems, Tool Shed operations, and Vue/TypeScript client development.
Read when: A task mentions Galaxy, galaxy.yml, run.sh, Galaxy API keys or OpenAPI, histories, datasets, workflows, tool XML, Format2 workflows, datatypes, object stores, file sources, data managers, Tool Shed repositories, shed_tool_conf.xml, client pnpm/Vitest/Vite, or errors from Galaxy config, API, tool-util, Tool Shed, storage, or client workflows.
Best for: Galaxy repository changes and usage workflows that need precise routing across backend Python packages, server admin configuration, API automation, Galaxy tool/workflow artifacts, data/storage behavior, Tool Shed repository maintenance, and web-client testing/builds.
Avoid when: Avoid for unrelated workflow engines, general Bioinformatics analysis without Galaxy repository/API/tool surfaces, or generic Python packaging questions that do not involve Galaxy-specific files, commands, APIs, or errors.
Useful entry points: `galaxy/SKILL.md`, `galaxy/sub-skills/configuration-and-admin/SKILL.md`, `galaxy/sub-skills/api-automation/SKILL.md`, `galaxy/sub-skills/workflows-and-tools/SKILL.md`, `galaxy/sub-skills/data-and-storage/SKILL.md`, `galaxy/sub-skills/tool-shed-operations/SKILL.md`, `galaxy/sub-skills/web-client-development/SKILL.md`.

### `kedro`

Role: Kedro also covers contribution-time facts for maintaining Kedro projects and interpreting Kedro's own Python package APIs, tests, templates, and extension boundaries.
Read when: Use kedro for maintenance tasks that involve editing a Kedro project, updating Kedro pipeline code, debugging Kedro project tests, packaging a Kedro project, writing project hooks, reviewing catalog/config changes, or troubleshooting Kedro-specific source changes.
Best for: Kedro-aware code review, project test triage, package metadata interpretation, project settings updates, pipeline registry changes, hook/plugin changes, and safe CLI/package diagnostics in Kedro repositories.
Avoid when: Avoid kedro for general Python maintenance that does not involve Kedro APIs, Kedro project metadata, Kedro CLI commands, or Kedro configuration artifacts.
Useful entry points: `kedro/SKILL.md`, `kedro/sub-skills/project-cli-and-sessions/SKILL.md`, `kedro/sub-skills/pipelines-and-nodes/SKILL.md`, `kedro/sub-skills/data-catalog-and-config/SKILL.md`, `kedro/sub-skills/hooks-and-extensions/SKILL.md`.

### `khoj`

Role: Khoj includes focused maintainer guidance for modifying the Khoj Python/FastAPI/Django repository, selecting tests, and handling migrations/frontend/docs side effects.
Read when: Tasks mention editing the Khoj repo, changing src/khoj routers, processors, search filters, database models or migrations, documentation, clients, tests, pyproject metadata, or maintainer scripts.
Best for: Choosing focused tests for Khoj code changes, planning Django migrations, understanding development setup, and avoiding unsafe dev/release script execution.
Avoid when: Use generic Python maintenance guidance for non-Khoj repositories or when no Khoj-specific source paths, tests, models, routers, parsers, or scripts are involved.
Useful entry points: `khoj/SKILL.md`, `khoj/sub-skills/development/SKILL.md`.

### `langflow`

Role: Use `langflow` for maintaining the Langflow monorepo across Python backend/base, LFX, SDK, bundles, frontend, docs, migrations, and release/version scripts.
Read when: The task mentions editing the Langflow checkout, `make init`, `make backend`, `make frontend`, `make unit_tests`, package-specific `uv` sync, Ruff/Biome, component indexes, Alembic migration tests, workspace package versions, bundle pins, frontend package scripts, or Langflow contributor policy.
Best for: Choosing focused Langflow tests, preserving component identity, updating workspace versions, maintaining generated artifacts, validating migrations, and coordinating backend/frontend/SDK/LFX changes in the repo.
Avoid when: Use a generic Python maintenance skill for unrelated repositories; use `langflow`'s workflow or deployment scenarios when the user is operating Langflow rather than editing its source.
Useful entry points: `langflow/SKILL.md`, `langflow/sub-skills/repo-maintenance/SKILL.md`, `langflow/sub-skills/component-development/SKILL.md`, `langflow/sub-skills/backend-runtime/SKILL.md`, `langflow/sub-skills/frontend-development/SKILL.md`.

### `nilearn`

Role: Use nilearn to follow this repository's import-layer architecture, estimator conventions, tests, docs, changelog, and generated-test marker rules.
Read when: The task mentions editing Nilearn source, adding Nilearn tests, fixing Nilearn docs, import-linter, tox, pre-commit, estimator checks, maskers/GLM/plotting internals, doc/changes/latest.rst, or @pytest.mark.ai_generated.
Best for: Targeted code changes in the Nilearn checkout, test selection, doc/gallery validation, changelog entries, import architecture checks, and coding-agent maintenance guidance.
Avoid when: Avoid for ordinary user analysis scripts that import Nilearn but do not modify the source checkout; route those to the scientific-python-data-workflows scenario entry instead.
Useful entry points: `nilearn/SKILL.md`, `nilearn/sub-skills/development-maintenance/SKILL.md`.

### `openfe`

Role: OpenFE-specific context for maintaining this Python package's APIs, CLI commands, docs, protocol tests, and dependency-sensitive scientific workflows.
Read when: Tasks ask to modify OpenFE source, update protocol or CLI behavior, adjust docs for OpenFE workflows, run focused OpenFE tests, debug package imports, or refresh repo-specific OpenFE skill coverage after repository changes.
Best for: Finding the right OpenFE source/test/docs area for changes, choosing safe focused tests around network planning, protocol settings, CLI commands, and result gathering, and understanding dependency/backend constraints while maintaining the package.
Avoid when: Do not use this maintenance route for ordinary OpenFE user workflows where no repository editing is needed; use the molecular chemistry workflow route instead.
Useful entry points: `openfe/SKILL.md`, `openfe/references/repo-provenance.md`.

### `openhands`

Role: OpenHands-specific maintainer guidance for backend, frontend, enterprise, skills/microagents, validation, and repository automation work.
Read when: Use for OpenHands, agent canvas, app-server, sandbox, settings, secrets, conversation APIs, React frontend settings/chat UI, enterprise SaaS extension, OpenHands skills or microagents, pre-commit hooks, lockfiles, GitHub Actions pinning, issue triage automation, or repo validation commands.
Best for: Changing the OpenHands checkout across Python backend routes/services, frontend TanStack Query/settings/i18n flows, enterprise auth/storage/integrations, prompt-extension files, or repo-wide maintenance automation.
Avoid when: The task is only to operate OpenHands as an end user without editing the repository, or when another skill targets the exact library/framework being modified outside this checkout.
Useful entry points: `openhands/SKILL.md`, `openhands/sub-skills/backend-development/SKILL.md`, `openhands/sub-skills/frontend-development/SKILL.md`, `openhands/sub-skills/enterprise-extension/SKILL.md`, `openhands/sub-skills/skills-and-microagents/SKILL.md`, `openhands/sub-skills/repo-maintenance/SKILL.md`.

### `paddlehelix`

Role: Use paddlehelix to understand PaddleHelix repository structure, source roots, build caveats, and safe focused checks before making repo changes.
Read when: Requests mention modifying PaddleHelix source, pahelix modules, setup.py, docs, app launchers, LinearRNA CMake/pybind builds, optional dependency import failures, or refreshing the generated PaddleHelix skill after code changes.
Best for: Repository-aware maintenance guidance that respects PaddleHelix public APIs, optional dependency boundaries, and safe test/example selection.
Avoid when: Use a generic Python packaging or CMake skill when the task is not PaddleHelix-specific and does not require its repo structure or domain workflows.
Useful entry points: `paddlehelix/SKILL.md`, `paddlehelix/references/repo-provenance.md`, `paddlehelix/references/troubleshooting.md`.

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

### `segmentation-models-pytorch`

Role: Provides focused maintainer routes for SMP source, docs, generated encoder tables, and pytest marker selection.
Read when: Use when a request asks to modify segmentation_models_pytorch source files, add a decoder or encoder, change losses/metrics, update docs/models.rst or docs/encoders*.rst, run focused SMP pytest commands, use Makefile targets, or troubleshoot SMP contributor workflows.
Best for: Selecting focused tests for changed SMP paths, understanding source ownership across decoders/encoders/losses/metrics, updating docs tables, and avoiding slow credentialed maintainer scripts unless explicitly requested.
Avoid when: Avoid for ordinary SMP model usage, inference, training, preprocessing, save/load, or export questions where no repository edit is needed.
Useful entry points: `segmentation-models-pytorch/SKILL.md`, `segmentation-models-pytorch/sub-skills/repo-development/SKILL.md`.

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

### `zenml`

Role: The zenml skill captures repository-specific maintenance rules, AGENTS guidance, optional dependency boundaries, targeted tests, docs, migrations, and PR-readiness checks for ZenML.
Read when: The task involves modifying ZenML source, tests, docs, scripts, integrations, CLI, FastAPI server, SQLModel schemas, Alembic migrations, pyproject dependencies, AGENTS instructions, or CI-equivalent validation commands.
Best for: Choosing targeted pytest/lint/docs/migration checks, preserving optional imports, updating CLI/client/model/schema/store layers consistently, and following ZenML contributor rules.
Avoid when: The user only wants to use ZenML as a library without modifying its repository; use the MLOps workflow scenario entry points instead.
Useful entry points: `zenml/SKILL.md`, `zenml/sub-skills/maintenance/SKILL.md`, `zenml/sub-skills/server-and-stores/SKILL.md`, `zenml/sub-skills/stacks-and-integrations/SKILL.md`, `zenml/sub-skills/cli-and-client/SKILL.md`.

<!-- DISCO_SCENARIO:python-repository-maintenance:END -->

## How To Choose

Choose this scenario when the user is contributing to or modifying a repo checkout; otherwise choose the user-facing workflow scenario for the package. Use this scenario for maintainer-style code and documentation tasks; cross-route to training-scripts for flag semantics and experiment-operations for benchmarks. Use the repo-development route only for current-checkout contribution tasks; normal CrewAI app usage should start at core-runtime, flows, CLI/projects, tools/MCP, or provider sub-skills. Choose `deepmd-kit` in Python repository maintenance when the checkout-specific build/test rules, backend dependencies, C++ components, examples, or DeePMD-kit contributor conventions affect the task. Choose galaxy when the user names Galaxy or asks about Galaxy-specific server config, API automation, tool/workflow artifacts, datatypes/storage, Tool Shed repositories, or client development; then route to the narrow sub-skill whose trigger terms match the task. Choose kedro for maintenance when the repository is a Kedro project or the changed files include Kedro pipeline factories, catalog/config files, settings.py, pipeline_registry.py, hooks, runners, sessions, or Kedro CLI commands. Choose khoj when repository-maintenance tasks target Khoj source paths, tests, docs, package metadata, Django models/migrations, or maintainer workflows.
