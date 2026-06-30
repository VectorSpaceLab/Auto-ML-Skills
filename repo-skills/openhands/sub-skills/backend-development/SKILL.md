---
name: backend-development
description: "Modify the OpenHands Python backend, V1 app-server APIs, settings, secrets, sandboxes, conversations, config, and backend validation workflows safely."
disable-model-invocation: true
---

# Backend Development

Use this sub-skill when changing the OpenHands Python backend: FastAPI V1 routes, app-server services, settings/secrets/sandbox/conversation flows, config/env behavior, server startup, backend tests, and schema/OpenAPI workflows.

## Route First

- Use [references/backend-workflows.md](references/backend-workflows.md) for setup, startup, testing, linting, pre-commit, config schema, OpenAPI, and backend change workflow guidance.
- Use [references/api-and-settings.md](references/api-and-settings.md) for V1 route structure, dependency injection, settings payloads, secrets APIs, sandbox credential inheritance, conversation lifecycles, and config/env patterns.
- Use [references/troubleshooting.md](references/troubleshooting.md) when imports, dependency installation, optional services, data/config, route tests, CLI/server startup, or schema/OpenAPI generation fail.
- Use [scripts/check_backend_imports.py](scripts/check_backend_imports.py) as a safe read-only diagnostic before deeper backend work or when dependency problems are suspected.

## Choose This Sub-Skill For

- Adding or changing routes under `openhands/app_server`, including `/api/v1/settings`, `/api/v1/secrets`, `/api/v1/sandboxes`, `/api/v1/app-conversations`, `/api/v1/config`, web client config, status, git, pending messages, events, and webhooks.
- Updating Python backend models, services, injectors, app lifespan, server startup, config defaults, env-var parsing, or storage behavior.
- Writing or updating backend unit tests under `tests/unit`, especially `tests/unit/app_server`, `tests/unit/storage`, `tests/unit/utils`, and integration-provider unit tests.
- Regenerating or validating backend-derived schemas such as config schema or OpenAPI after a backend API/model change.

## Route Away

- Frontend UI, TanStack Query hooks, i18n, React routes, or settings screens belong in `../frontend-development/SKILL.md` when available.
- Enterprise SaaS-only overrides, enterprise database migrations, billing, org management, and enterprise-specific integrations belong in `../enterprise-extension/SKILL.md` when available.
- Repo-local skills, microagents, or prompt-authoring changes belong in `../skills-and-microagents/SKILL.md` when available.
- Repo-wide CI policy, GitHub Actions pinning, lockfile regeneration, PR artifacts, and release/process work belong in `../repo-maintenance/SKILL.md` when available.

## Safety Defaults

- Install pre-commit hooks before code changes when possible: `make install-pre-commit-hooks`. If Poetry or dependencies are unavailable, record the blocker and still keep backend edits minimal.
- Prefer focused backend tests first: `poetry run pytest tests/unit/app_server/test_name.py` or an exact `::test_name`, then broaden only as needed.
- For backend edits, run `pre-commit run --config ./dev_config/python/.pre-commit-config.yaml` before handoff when the environment supports it.
- Do not start Docker, remote runtimes, migrations, schema writers, or OpenAPI writers unless the task requires them and the environment is ready.
- Never log or return raw secrets; use masked flags, `SecretStr`, and sandbox-scoped `LookupSecret` paths according to [references/api-and-settings.md](references/api-and-settings.md).
