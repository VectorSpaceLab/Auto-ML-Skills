# OpenHands Troubleshooting

## Purpose

Use this root troubleshooting guide when OpenHands repo work fails before it clearly belongs to one sub-skill, or when a cross-stack task spans backend, frontend, enterprise, and repo-wide validation.

## Setup And Dependency Failures

- `poetry: command not found`: backend, enterprise, and `make install-pre-commit-hooks` commands require Poetry. Install/expose Poetry before expecting Makefile install, pre-commit, or pytest commands to work. If Poetry is unavailable, record the blocker and avoid claiming validation passed.
- Python version mismatch: OpenHands Python packages require `>=3.12,<3.14`; use Python 3.12 or 3.13 for repo setup.
- Node version mismatch: frontend scripts require Node `>=22.12.0`; run frontend commands from `frontend/` after dependency installation.
- Large browser/runtime downloads stall: avoid full app or Playwright installs for small code changes; use focused unit/static checks first and report skipped browser validation.

## Choosing The Right Route

- Backend route, settings, secrets, sandbox, server startup, or schema/OpenAPI failures: read `sub-skills/backend-development/references/troubleshooting.md`.
- Frontend build, i18n, TanStack Query, MSW, WebSocket, archived UI, or Vitest failures: read `sub-skills/frontend-development/references/troubleshooting.md`.
- Enterprise imports, auth/org context, database stores, migrations, billing, telemetry, sync jobs, or external service mocks: read `sub-skills/enterprise-extension/references/troubleshooting.md`.
- Skill/microagent frontmatter, triggers, listing, slash commands, or V0/V1 terminology: read `sub-skills/skills-and-microagents/references/troubleshooting.md`.
- Pre-commit, lockfiles, GitHub Actions pinning, `.pr/` artifacts, git safety, or issue automation: read `sub-skills/repo-maintenance/references/troubleshooting.md`.

## Runtime And Local App Failures

- Full local app startup can require backend dependencies, frontend build output, tmux, Docker or local runtime settings, Playwright browsers, and clean session state. Do not use it as the first check for small edits.
- If local runtime startup reports `duplicate session: test-session`, clear the stale tmux session on the default tmux socket before retrying.
- If `/api/v1/settings` returns unexpected `401` in local browser QA, unset inherited `SESSION_API_KEY` before running the app directly.
- If frontend mock dev servers are awkward through a proxy, prefer `npm run build` with mock env and serve `build/` with minimal mock endpoints for PR screenshots.

## Validation Strategy

- Start with the narrowest deterministic check for the touched behavior.
- Do not run networked provider flows, Docker-heavy sandbox checks, enterprise sync jobs, or real external service calls unless the task explicitly requires them.
- Treat skipped native checks as skipped, not passing. Pair skipped Docker/browser/credential checks with focused unit tests or static checks when possible.
- If validation tools auto-fix files, inspect the diff and rerun the same command before final handoff.

## Public Content And Privacy

- Do not put local environment prefixes, Python executable paths, raw API keys, private proxy commands, or machine-specific cache paths in docs or skill files.
- Do not store PR-only notes, verification logs, or temporary debugging artifacts in runtime source areas; use `.pr/` for repository PR artifacts and keep generated-skill verification artifacts outside the runtime skill tree.
