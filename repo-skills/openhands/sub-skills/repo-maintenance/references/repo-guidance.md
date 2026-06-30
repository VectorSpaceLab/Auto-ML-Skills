# OpenHands Repo Maintenance Guidance

This reference captures repo-wide setup and maintenance rules for OpenHands. It is for choosing safe commands and policies; route code-area implementation to the backend, frontend, enterprise, or skills sub-skills.

## Repository Shape

- OpenHands is a Python backend plus React frontend repository.
- Backend code lives under `openhands`; current V1 app-server routes live under `openhands/app_server` and `make start-backend` launches `openhands.server.listen:app` unless V1 is disabled.
- Frontend code lives under `frontend`; VS Code extension code lives under `openhands/app_server/integrations/vscode`.
- Enterprise-only extensions live under `enterprise` and have separate dependency, lint, test, and migration workflows.
- The root package distribution is `openhands-ai`; the supported Python range is `>=3.12,<3.14`.

## First Step Before Edits

Attempt hook setup before making changes:

```bash
make install-pre-commit-hooks
```

This target checks Python, Poetry, installs Python dependencies with dev/test/runtime groups, and installs pre-commit using `dev_config/python/.pre-commit-config.yaml`. If Poetry is unavailable, dependency download times out, or the environment cannot install dependencies, record that blocker and continue only with narrow edits that you can reason about and validate by lighter checks.

## Validation Command Selection

Pick the smallest command that covers the touched area, then broaden if confidence requires it:

- Backend or root Python changes: `pre-commit run --config ./dev_config/python/.pre-commit-config.yaml` for staged files, or `poetry run pytest tests/unit/test_name.py` for focused tests.
- Backend-wide lint from Makefile: `make lint-backend`, which runs hooks with `--all-files --show-diff-on-failure` through Poetry.
- Frontend changes: `cd frontend && npm run lint:fix && npm run build` before handoff; use `npm run test -- -t "TestName"` for focused Vitest coverage when applicable.
- VS Code extension changes: `cd openhands/app_server/integrations/vscode && npm run lint:fix && npm run compile`.
- Enterprise changes: use enterprise-specific Poetry commands and include `--show-diff-on-failure` for CI-like lint behavior.
- Full project setup/build: `make build`, only when the task or validation scope justifies installing both backend and frontend dependencies.

The root pre-commit config includes basic file hygiene, YAML checks, debug-statement checks, `pyproject-fmt`, `validate-pyproject`, Ruff lint/format, mypy for `openhands/`, and a local guard against `AppMode.OSS` in backend code.

## Setup and Run Targets

Important Makefile targets:

- `make build`: checks dependencies, installs Python and frontend dependencies, installs hooks, and builds the frontend.
- `make lint`: runs frontend lint then backend lint.
- `make test`: runs frontend tests only; backend tests are run directly with Poetry/pytest.
- `make start-backend`: starts the backend via Uvicorn with reload.
- `make start-frontend`: starts the frontend with WSL-aware dev script selection.
- `make run`: starts backend and frontend locally after `_run_setup` waits for backend readiness.
- `make setup-config` and `make setup-config-basic`: create `config.toml`; avoid committing secrets produced by interactive config setup.

For local app debugging, the recommended pattern is to avoid Docker runtime when possible:

```bash
export INSTALL_DOCKER=0
export RUNTIME=local
make build && make run FRONTEND_PORT=12000 FRONTEND_HOST=0.0.0.0 BACKEND_HOST=0.0.0.0
```

## Git Practices

- Prefer `git add <specific-file>` over `git add .`.
- Avoid `git reset --hard`, especially after staging, unless the user explicitly authorizes destructive cleanup.
- Do not commit or branch unless the task asks for it.
- If synchronizing with upstream, use `git fetch upstream && git rebase upstream/<branch>` on the current branch.
- Before handoff, mention any generated files, auto-fixes, or unrun validation caused by missing prerequisites.

## GitHub Actions Policy

When editing workflow files:

- Pin external third-party actions to a full 40-character commit SHA and keep the readable version tag in a trailing comment, for example `uses: owner/repo@<40-char-sha> # v1.2.3`.
- GitHub-authored `actions/*`, `github/*`, and first-party `OpenHands/*` actions are exempt from this pinning requirement.
- Do not replace a pinned SHA with a mutable tag or branch.
- Dependabot's `github-actions` ecosystem is expected to update both the SHA and trailing comment.
- Existing workflow examples include pinned third-party actions such as Docker Buildx and coverage-comment actions, while `actions/checkout`, `actions/setup-node`, `actions/setup-python`, `actions/upload-artifact`, and OpenHands extension actions may use version tags according to policy.

## Lockfile Regeneration

Preserve the tool version that generated each lockfile to prevent noisy lock churn.

For `poetry.lock`, extract the Poetry version from the header, install that exact Poetry with pipx if necessary, then regenerate without updates:

```bash
POETRY_VERSION=$(grep -m1 "^# This file is automatically @generated by Poetry" poetry.lock | sed 's/.*Poetry \([0-9.]*\).*/\1/')
pipx install poetry==$POETRY_VERSION --force
poetry lock --no-update
```

The inspected `poetry.lock` header records Poetry `2.3.2`.

For `uv.lock`, inspect its header before regenerating. If a future uv header includes an explicit uv version, install that version with pipx and run `uv lock`. If the header only records lockfile format fields, avoid inventing a tool version; record the limitation and keep diffs minimal.

When the root `openhands-ai` version changes, also update the enterprise lockfile from inside `enterprise` with the same lockfile-version preservation principle.

## PR-Specific Artifacts

Use `.pr/` only for temporary PR review artifacts that should not merge into main, such as design notes, debugging logs, screenshots notes, or analysis documents.

- Do not put durable product docs, scripts, or required runtime files in `.pr/`.
- The PR artifacts workflow posts or updates a PR comment when `.pr/` exists.
- Same-repo PRs can have `.pr/` auto-removed after approval by an automation commit.
- Fork PRs cannot be auto-cleaned; the contributor must remove `.pr/` manually before merge.

## Maintenance Decision Checklist

Before handoff, confirm:

- Hook installation was attempted, or the missing prerequisite is documented.
- Validation commands match the touched area and any unrun checks are explained.
- Lockfiles were regenerated with the original tool version or left untouched.
- Workflow action changes follow SHA pinning policy.
- `.pr/` content is temporary and non-runtime.
- Git staging is explicit and no destructive command was used.
