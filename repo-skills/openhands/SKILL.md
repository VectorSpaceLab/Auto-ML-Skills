---
name: openhands
description: "Develop and maintain the OpenHands repository, including backend app-server APIs, frontend UI, enterprise extension, skills/microagents, validation workflows, and repo-wide automation."
disable-model-invocation: true
---

# OpenHands

Use this repo skill when working on the OpenHands checkout: Python backend/app-server code, React frontend code, enterprise SaaS extension code, OpenHands skills/microagents, tests, build/lint commands, CI policy, and repo-wide maintenance.

## Start Here

- Read [Repository Provenance](references/repo-provenance.md) before deciding whether this skill matches the current checkout; refresh the skill if commit, package version, or major evidence paths changed.
- Read [Troubleshooting](references/troubleshooting.md) when setup, dependency installation, validation, local runtime, frontend build, enterprise tests, or import checks fail.
- Use the route map below to select the focused sub-skill before changing files.
- For simple one-area tasks, stay in one sub-skill; for cross-stack work, read every affected sub-skill and finish with the repo-maintenance validation guidance.

## Route Map

- [backend-development](sub-skills/backend-development/SKILL.md): Python backend, V1 app-server routes, settings/secrets/sandbox/conversation services, config/env behavior, schema/OpenAPI workflows, and backend unit tests.
- [frontend-development](sub-skills/frontend-development/SKILL.md): React/Vite frontend, TanStack Query hooks, API service boundaries, settings UI patterns, i18n, archived conversation UI, Vitest/Playwright tests, and frontend build/lint.
- [enterprise-extension](sub-skills/enterprise-extension/SKILL.md): Enterprise SaaS extension, auth/org context, storage/database stores, integrations, migrations, billing, telemetry, sync jobs, and enterprise-specific validation.
- [skills-and-microagents](sub-skills/skills-and-microagents/SKILL.md): OpenHands public skills, repository microagents, V0/V1 prompt-extension terminology, frontmatter/triggers, skill listing/loading, and skill documentation review.
- [repo-maintenance](sub-skills/repo-maintenance/SKILL.md): Repository setup, pre-commit hooks, validation command selection, GitHub Actions pinning, lockfile regeneration, PR artifacts, issue triage automation, and safe git practices.

## Repository Facts

- Python package: `openhands-ai` version `1.8.0`; import root `openhands`; Python `>=3.12,<3.14`.
- Frontend package: `openhands-frontend` version `1.8.0`; Node `>=22.12.0`; npm scripts live under `frontend/`.
- Main backend source: `openhands/`; current V1 app server lives under `openhands/app_server/`.
- Frontend source: `frontend/src/`; API calls must flow through TanStack Query hooks rather than direct service calls from UI components.
- Enterprise extension: `enterprise/`; enterprise application code uses package-relative imports without `enterprise.` prefixes.
- Prompt extensions: public reusable files live in `skills/`; repo-specific instructions live in `.openhands/microagents/` or `.openhands/skills/`.

## Default Workflow

1. Attempt repository hook setup before code changes when feasible: `make install-pre-commit-hooks`.
2. Identify the affected area and read the matching sub-skill plus linked references.
3. Make minimal, focused edits that follow the owning area’s architecture and validation patterns.
4. Run the narrowest safe test or static check for the changed behavior, then broaden only when needed.
5. For final handoff, report commands run, blockers such as missing Poetry or dependency downloads, and any skipped Docker/browser/credential/network checks.

## Validation Shortcuts

- Backend: `pre-commit run --config ./dev_config/python/.pre-commit-config.yaml` and focused `poetry run pytest tests/unit/<file>.py`.
- Frontend: `cd frontend && npm run lint:fix && npm run build`; focused tests use `cd frontend && npm run test -- -t "<name>"`.
- Enterprise: `cd enterprise && poetry run pre-commit run --all-files --show-diff-on-failure --config ./dev_config/python/.pre-commit-config.yaml`; focused pytest commands set `PYTHONPATH=".:$PYTHONPATH"`.
- VS Code extension: `cd openhands/app_server/integrations/vscode && npm run lint:fix && npm run compile` when that package is touched.

## Safety Notes

- Do not run full app, Docker, Playwright browser installs, enterprise sync jobs, networked issue automation, or real external integrations unless the task requires them and the environment is ready.
- New boolean environment feature gates must accept both `"true"` and `"1"` as truthy values and include tests for both forms.
- Preserve lockfile generator versions when regenerating `poetry.lock`, `enterprise/poetry.lock`, `uv.lock`, or `enterprise/uv.lock`.
- Pin external third-party GitHub Actions to a full 40-character SHA with a trailing version comment; GitHub-authored and first-party OpenHands actions are exempt.
- Keep PR-only design notes, logs, and temporary artifacts under `.pr/`, not in runtime code or generated skill content.
