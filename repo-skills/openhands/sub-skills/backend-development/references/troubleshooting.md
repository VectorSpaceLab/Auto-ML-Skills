# Backend Troubleshooting

## Install And Import Failures

Symptoms:

- `poetry: command not found` during `make install-pre-commit-hooks` or tests.
- `ModuleNotFoundError` for FastAPI, Pydantic, SQLAlchemy, Docker, Playwright, `openhands.sdk`, or provider libraries.
- Importing `openhands.app_server.app` fails before a route test starts.

Actions:

1. Confirm Python version is `>=3.12,<3.14`.
2. Install or expose Poetry, then run the smallest dependency install needed for the backend task.
3. Run the bundled import diagnostic from the copied skill tree:

   ```bash
   python /path/to/openhands-skill/sub-skills/backend-development/scripts/check_backend_imports.py --repo-root .
   ```

4. If only optional backend integrations fail, avoid importing their modules in focused tests unless the task owns that integration.
5. If a full dependency install times out, report that only partial import diagnostics were possible and avoid claiming deep runtime verification.

## Optional Services And Runtime Backends

Symptoms:

- Docker sandbox tests fail because Docker is unavailable.
- Remote runtime config raises missing `SANDBOX_API_KEY` or remote URL errors.
- Local/process runtime startup fails because tmux or agent-server dependencies are missing.
- Database tests try to connect to PostgreSQL or Cloud SQL instead of SQLite/mocks.

Actions:

- Prefer unit tests that mock sandbox, database, HTTP, and provider services unless the task explicitly changes live runtime behavior.
- Use `RUNTIME=local` or `RUNTIME=process` only when process sandbox behavior is under test; otherwise avoid changing runtime env globally.
- For DB changes, use SQLite or mocked drivers in unit tests. Only use real PostgreSQL for integration-level work.
- For Docker-related services, isolate construction/parsing logic from container startup and test with mocks where possible.

## Settings And Secret Misuse

Symptoms:

- `POST /api/v1/settings` returns `422` for nested settings keys.
- Saved settings overwrite unrelated SDK settings.
- Secret values appear in GET responses or logs.
- Custom secrets or provider tokens are stored in the wrong model.

Actions:

- Use `agent_settings_diff` and `conversation_settings_diff` for nested settings POST payloads.
- Keep `secrets_store` and `llm_profiles` out of generic settings mutation.
- Preserve omitted fields during partial updates; test explicit empty string clears separately from omitted values.
- Return secret-set flags rather than raw values from normal user/settings endpoints.
- Use `/api/v1/secrets` for custom secrets and git-provider tokens.
- Use sandbox-scoped secret endpoints plus `X-Session-API-Key` for raw sandbox lookups.

## Auth And Session API Key Failures

Symptoms:

- Sandbox-scoped secret endpoints return `401` or `403`.
- `/api/v1/users/me?expose_secrets=true` does not expose raw settings.
- Tests unexpectedly authenticate or reject requests because `SESSION_API_KEY` leaks from the environment.

Actions:

- Validate that the session key maps to a running sandbox.
- Ensure the sandbox ID in the path matches the sandbox returned by session auth.
- For `expose_secrets=true`, require both authenticated user context and `X-Session-API-Key` ownership.
- In unit tests, patch `SESSION_API_KEY` and the cached dependency state consistently when auth is not the subject of the test.

## Config And Environment Failures

Symptoms:

- Boolean env toggles work for `true` but not `1`.
- Feature flags treat arbitrary non-empty strings as true.
- `OH_AGENT_SERVER_ENV` parsing fails or forwards unexpected values.
- DB SSL mode or legacy env fallback changes break existing deployments.

Actions:

- For new boolean enable toggles, use `.lower() in ('true', '1')` and test both truthy values.
- For disable/hide flags that intentionally accept only a narrow value, document that behavior and add tests.
- Strip URL/key env vars and treat empty strings as unset where existing helpers do so.
- Preserve legacy env fallbacks unless the task explicitly removes them.
- Add tests around env unset, empty, whitespace, true, `1`, false, and unrelated values.

## API, CLI, And Server Startup Mistakes

Symptoms:

- New routes are not visible under `/api/v1`.
- A route is unprotected or missing OpenAPI tags.
- `openhands.server.__main__` behavior differs from direct app startup.
- Full app startup fails because frontend build, Playwright, tmux, Docker, or inherited session env is missing.

Actions:

- Include new routers through the V1 router, not by side-effect imports.
- Use `APIRouter(prefix=..., tags=[...], dependencies=get_dependencies())` unless there is a reason to differ.
- Prefer `uvicorn openhands.app_server.app:app` for new backend startup docs; the server `__main__` module is compatibility-oriented.
- For local browser QA, unset inherited `SESSION_API_KEY` if settings endpoints unexpectedly return unauthorized responses.
- Do not use full `make run` as the first validation for a small backend route change.

## Schema And OpenAPI Failures

Symptoms:

- `scripts/dump_config_schema.py` fails while importing config.
- `scripts/update_openapi.py` fails or unexpectedly rewrites `docs/openapi.json`.
- OpenAPI output includes internal examples or operational endpoints.

Actions:

- Run schema/OpenAPI helpers only after backend dependencies import cleanly.
- Treat OpenAPI update as mutating: expect a backup and a `docs/openapi.json` diff.
- If endpoint descriptions include internal details, sanitize or override them in the OpenAPI helper rather than exposing internal implementation text.
- If a new route should be public API, verify it appears in generated OpenAPI; if operational/UI-only, add a deliberate exclusion.

## Workflow-Specific Failure Modes

- Settings workflow: reject legacy nested payloads, preserve unrelated settings during partial saves, normalize LLM base URLs, and mask secrets in GET responses.
- Secrets workflow: validate provider token type on store, paginate/list custom secrets without values, and preserve provider tokens when editing custom secrets.
- Sandbox workflow: reject session keys for non-running sandboxes, distinguish paused/missing/error states, and verify path sandbox ID matches session key sandbox ID.
- Conversation workflow: validate UUID lists and limits, keep DB/HTTP resources open for background work, and return clear errors when sandbox/agent-server context is unavailable.
- Config search workflow: preserve pagination, `limit` bounds, query filtering, provider filtering, and verified-first provider ordering.
