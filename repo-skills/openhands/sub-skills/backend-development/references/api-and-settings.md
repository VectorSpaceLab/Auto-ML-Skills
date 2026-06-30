# API And Settings Reference

## V1 Router Structure

The FastAPI app includes the app-server V1 router under `/api/v1`. The V1 router aggregates route modules for events, conversations, pending messages, sandboxes, sandbox specs, settings, secrets, users, skills, webhooks, web client config, git, and config search.

Common route prefixes:

- `/api/v1/settings`: user settings, LLM/profile schema endpoints, settings persistence, profile operations.
- `/api/v1/secrets`: git-provider tokens and custom secrets.
- `/api/v1/sandboxes`: sandbox lifecycle, sandbox search/batch reads, pause/resume/delete, and sandbox-scoped settings secrets.
- `/api/v1/app-conversations`: conversation search/count/batch reads, conversation startup, message forwarding, hooks, skills, exports, profiles, and runtime helpers.
- `/api/v1/users`: current user and git metadata.
- `/api/v1/config`: model/provider search endpoints.
- `/api/v1/web-client`: web client configuration surfaced from backend env/config.

Routers typically set `dependencies=get_dependencies()` so OpenAPI shows protected endpoints. Actual auth may be handled by middleware or route-specific dependencies.

## Dependency Injection Pattern

Backend services are injected through `openhands.app_server.config` and the generic `Injector` interface. Follow this pattern for new service dependencies:

- Define or reuse an injector class that implements `inject(self, state, request)` and yields the service.
- Add the injector to `AppServerConfig` when it is configurable.
- Initialize the default injector in `config_from_env()` when absent.
- Expose both context and FastAPI dependency helpers if the service is used in routers or lower-level utilities.
- In route tests, either call the route function directly with mocked service arguments or mount a small FastAPI app and override dependencies.

Keep request-scoped resources on `request.state` when nested injectors need to share them. For long-running post-response work, preserve required resources explicitly; conversation startup uses keep-open flags for DB sessions and HTTP clients before scheduling background consumption.

## Settings API Rules

Settings are persisted with top-level product settings plus SDK-owned `agent_settings` and `conversation_settings`.

Important rules:

- `GET /api/v1/settings` returns settings with raw secrets removed. LLM API keys are represented by flags such as `llm_api_key_set`.
- `POST /api/v1/settings` accepts partial updates. Nested SDK settings must use `agent_settings_diff` and `conversation_settings_diff`.
- Do not send legacy nested keys `agent_settings` or `conversation_settings` in POST payloads; the router rejects them with `422`.
- `secrets_store` and `llm_profiles` are not mutated through generic settings update. Secrets and profile mutations have dedicated APIs.
- LLM base URL fixups are applied after settings merge so OpenHands-managed models and provider defaults stay normalized.
- Empty string behavior is significant for secret-like fields; tests should cover explicit clear versus omitted field preservation.

Use `Settings.update(payload)` for settings merge behavior instead of hand-merging nested SDK models. The SDK owns agent-kind discriminated-union validation and migration.

## Secrets And Git Provider Tokens

The secrets router separates secret storage from user settings.

Key behaviors:

- `POST /api/v1/secrets/git-providers` stores git-provider tokens and validates provider token type when raw tokens are supplied.
- `DELETE /api/v1/secrets/git-providers` removes all git-provider tokens.
- `GET /api/v1/secrets/search` lists custom secrets without values and supports filtering/pagination.
- `POST /api/v1/secrets` creates or updates a custom secret.
- Secret values must not be returned through normal list/search endpoints.

When adding secret fields, validate environment-variable-compatible names where values are surfaced as env vars. The env-var validation utility accepts names that begin with a letter or underscore and contain letters, numbers, and underscores only.

## Sandbox Credential Inheritance

Sandbox credential inheritance is deliberately split so raw secrets flow only to sandbox callers that prove ownership.

Important endpoints and requirements:

- `GET /api/v1/users/me?expose_secrets=true` may return unmasked user settings, but only when the caller is an authenticated user and supplies `X-Session-API-Key` for an active sandbox owned by that user.
- `GET /api/v1/sandboxes/{sandbox_id}/settings/secrets` lists available secret names only. It authenticates with `X-Session-API-Key` and verifies the key belongs to the requested sandbox.
- `GET /api/v1/sandboxes/{sandbox_id}/settings/secrets/{secret_name}` returns a single raw value as `text/plain`, checking custom secrets first and then provider tokens.
- Session auth rejects missing, empty, invalid, non-running, paused, missing, or wrong-sandbox session keys.

Do not route sandbox secret reads through generic settings or user endpoints. Use the session-auth helpers and return plain values only from sandbox-scoped secret endpoints.

## Conversation And Sandbox Coupling

Conversation APIs rely on both conversation services and sandbox services:

- Conversations store `sandbox_id` and use sandbox status to decide whether runtime calls can proceed.
- Agent-server calls require a running sandbox, an exposed `AGENT_SERVER` URL, a sandbox spec, and usually a session API key.
- Paused sandboxes represent closed conversations for some helpers and should not be treated the same as missing or error states.
- Batch reads validate UUID inputs and enforce request limits.
- Search/list endpoints use pagination parameters with `limit` bounds.

When adding a conversation route, identify whether it is a pure metadata operation or a live agent-server operation. Live operations need runtime availability checks and HTTP client/session lifecycle care.

## Config And Env Patterns

Configuration is built from `AppServerConfig` via `from_env(AppServerConfig, 'OH')`, then legacy environment fallbacks fill service-specific defaults.

Backend env patterns to preserve:

- Persistence defaults to `OH_PERSISTENCE_DIR`, then legacy `FILE_STORE_PATH`, then a user OpenHands directory.
- File/event storage chooses local, AWS, or GCP based on storage-provider environment.
- `RUNTIME=remote` selects remote sandbox services and requires remote runtime credentials; `RUNTIME=local` or `RUNTIME=process` selects process sandbox services; otherwise Docker sandbox services are the default.
- Database env vars include `DB_HOST`, `DB_PORT`, `DB_NAME`, `DB_USER`, `DB_PASS`, `DB_SSL_MODE`/`PGSSLMODE`, plus GCP Cloud SQL env vars.
- Agent-server env forwarding accepts explicit `OH_AGENT_SERVER_ENV` JSON and auto-forwards `LLM_*` variables.

For new boolean enable toggles read from environment variables, accept both `true` and `1` as truthy values:

```python
os.getenv('MY_FEATURE_ENABLED', 'false').lower() in ('true', '1')
```

Add tests for both the `'true'` and `'1'` cases. Do not use `bool(os.getenv(...))`, a one-value comparison, or a check that treats every non-empty string as true.

## Web Client Config Boundary

The app server exposes web-client-safe feature flags and provider configuration. When changing backend-derived web client config:

- Keep raw credentials out of web client models.
- Strip whitespace from URL/key-like env vars and treat empty or whitespace-only values as unset when appropriate.
- Preserve backwards-compatible defaults for existing installs.
- Add tests around unset, empty, whitespace, true/false, and multi-flag cases.

If a change requires frontend UI work, route that portion to the frontend sub-skill rather than embedding React guidance here.
