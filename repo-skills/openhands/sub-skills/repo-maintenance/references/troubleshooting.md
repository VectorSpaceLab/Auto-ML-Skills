# Repo Maintenance Troubleshooting

Use this reference when repo-wide setup, validation, CI, lockfile, or automation tasks fail.

## Install and Import Failures

- `make install-pre-commit-hooks` fails with `poetry: command not found`: install Poetry compatible with the repo requirement, then rerun the target. If the task cannot install tools, document that hook installation was attempted and blocked.
- Poetry version is too old: the Makefile requires Poetry `1.8` or later for normal setup. Lockfile regeneration may require the exact lockfile header version instead.
- Compatible Python missing: use Python `3.12` or `3.13`; the repo supports `>=3.12,<3.14`.
- Dependency installation times out: retry only if useful, consider narrower validation that does not require full install, and avoid claiming full runtime verification.
- Backend imports fail after partial install: run focused import checks only after dependency setup is complete; do not mask missing optional dependencies as code bugs.

## Optional Dependency and Runtime Failures

- Docker checks fail during setup: for local non-Docker work, set `INSTALL_DOCKER=0` when using Makefile targets that would otherwise check Docker.
- `nc: command not found` while starting the local app: install a netcat package such as `netcat-openbsd` in the host environment.
- Local runtime reports `duplicate session: test-session`: clear the stale `test-session` tmux session on the default tmux socket for the host environment.
- Browser or runtime startup misses Playwright Chromium: install it through Poetry with a stable browser cache path, for example `PLAYWRIGHT_BROWSERS_PATH=$HOME/.cache/playwright poetry run playwright install chromium`.
- Frontend mock dev server is hard to browse through a proxy: build the frontend and serve the static `build/` output with minimal mock JSON endpoints for the page under review.

## Config and Data Issues

- Local web UI returns `401` from settings in a sandbox-like environment: check whether an inherited `SESSION_API_KEY` is present and unset it for direct local UI testing when appropriate.
- `config.toml` contains secrets from `make setup-config`: do not commit it unless the repository explicitly tracks a safe example; avoid echoing raw API keys in logs.
- Environment-variable enable toggles must accept both `true` and `1` when adding backend feature gates. Add tests for both truthy values.
- Enterprise tests unexpectedly hit external databases: use in-memory SQLite or mocked database connections for unit tests and keep real services for integration contexts.

## CLI and API Misuse

- Do not run networked issue scripts without confirming `OPENHANDS_API_KEY`, `GITHUB_TOKEN`, repository, issue number, output path, and side effects.
- Do not use logout flows to disconnect local/OSS git provider tokens; token management uses the V1 secrets endpoints for git providers.
- When writing backend docs for V1 web-app LLM setup, point users to the Settings UI rather than obsolete configuration paths.
- For sandbox credential inheritance, raw secret values should flow SaaS to sandbox through guarded APIs, not through SDK clients or logs.

## Workflow-Specific Failures

- Pre-commit changes files automatically: inspect the diff, fix remaining issues, then rerun the same command until clean or record the blocker.
- GitHub CI lint differs from local lint: rerun the relevant pre-commit command with `--show-diff-on-failure` to match CI output.
- Frontend build fails after lint fixes: rerun `npm run lint:fix`, then `npm run build`; do not change unrelated UI areas to silence unrelated failures.
- GitHub Actions pinning review fails: ensure external third-party actions use a full SHA plus trailing version comment. Leave `actions/*`, `github/*`, and `OpenHands/*` according to the repo exemption.
- Lockfile diff is huge after regeneration: verify the generating Poetry or uv version from the lockfile header and regenerate with the original version; if the header lacks a tool version, avoid unnecessary regeneration.
- `.pr/` cleanup fails on fork PRs: manual removal is expected; do not rely on the same-repo auto-cleanup workflow.

## Issue Automation Failures

- Good-first-issue automation labels too aggressively: check duplicate-veto precheck first, then result normalization. The final label should require high confidence and no disqualifiers.
- Duplicate-check automation wants to auto-close overlapping issues: this is a bug; overlapping-scope should be comment-only and `auto_close_candidate` must be false.
- OpenHands or GitHub API calls fail: inspect token presence, HTTP error body, rate limits, and output-path creation; do not retry with broader permissions unless authorized.
- Local classifier probe disagrees with production automation: treat the probe as a deterministic heuristic only. Production behavior uses OpenHands/GitHub context and maintainer policy.

## Safe Recovery Pattern

When blocked:

1. State the exact command that failed and the missing prerequisite or error class.
2. Switch to the smallest non-networked check that still validates the edited files.
3. Avoid destructive cleanup commands.
4. Record unrun commands in the handoff so a maintainer can rerun them in a prepared environment.
