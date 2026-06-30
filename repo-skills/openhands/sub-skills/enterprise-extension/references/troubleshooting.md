# Enterprise Troubleshooting

## Install And Import Failures

Symptoms:

- `poetry: command not found` when running enterprise setup or pre-commit commands.
- `ModuleNotFoundError: No module named 'server'`, `storage`, or `integrations` in enterprise tests.
- `ModuleNotFoundError` for optional services such as `stripe`, `keycloak`, `slack_sdk`, `asyncpg`, `pg8000`, `posthog`, or `resend`.
- Imports work from one directory but fail from another.

Checks and fixes:

- Ensure enterprise dependencies are installed with the enterprise project before running enterprise tests.
- Run enterprise tests with `PYTHONPATH=".:$PYTHONPATH"` from the repository root so package-relative imports resolve.
- Use `poetry run --project=enterprise pytest ...` from the repository root or `cd enterprise && poetry run ...` consistently; avoid mixing command roots in one debugging session.
- Keep enterprise application imports package-relative. If a test imports `enterprise.*`, verify it is intentionally testing from the repo root or a standalone script path.
- If an optional dependency is missing, decide whether the touched code truly needs that dependency for the focused test. Prefer narrow tests with mocked external clients when the dependency is not central to the change.

## Optional Dependency And Service Failures

Enterprise integrates with many external services. Local unit tests should not require live credentials for Keycloak, Stripe, Slack, GitHub, GitLab, Jira, Linear, Bitbucket, Azure DevOps, Redis, PostHog, Resend, Cloud SQL, or LiteLLM.

When a test unexpectedly contacts a service:

- Patch the provider client at the import path used by the code under test.
- Replace async client methods with `AsyncMock` and synchronous collaborators with `MagicMock`.
- Patch sleeps/retries for sync jobs and maintenance workers.
- Use fake response objects with `raise_for_status`, `json`, `text`, `content`, headers, and status codes that match the code path being exercised.
- Assert timeout/auth/error handling paths explicitly instead of relying only on a success path.

## Config And Data Issues

Common configuration failures:

- `SaaSServerConfig.verify_config()` raises because required env vars are missing.
- Feature flags or provider login buttons do not appear because provider client IDs or enable flags are absent.
- A new boolean toggle works for `"true"` but fails for `"1"`.
- Billing endpoints return 403 because billing is disabled.
- Webhook signature verification fails because the configured secret does not match the payload.

Debugging guidance:

- Distinguish config validation from business logic. Test validation failures directly and avoid hiding them with broad exception handling.
- For boolean env vars, use `lower() in ('true', '1')` and add tests for both truthy forms.
- For provider enablement, test missing, blank, and present env values.
- For data fixtures, seed the minimum required org, user, role, membership, settings, token, or integration rows.
- For org-scoped behavior, include cases for current org fallback, explicit `X-Org-Id`, API-key-bound org, and non-member org.

## CLI And Command Misuse

Common mistakes:

- Running `pytest enterprise/tests/unit/...` without `PYTHONPATH`, causing package-relative import failures.
- Running broad enterprise tests before installing enterprise test dependencies.
- Running sync scripts directly as smoke checks, causing credential or service side effects.
- Running pre-commit without `--show-diff-on-failure`, which can hide CI-equivalent formatting diffs.
- Running migration integrity checks against the wrong versions directory.

Safer commands:

```bash
PYTHONPATH=".:$PYTHONPATH" poetry run --project=enterprise pytest enterprise/tests/unit/<area> --confcutdir=enterprise/tests/unit/<area>
```

```bash
python scripts/check_enterprise_migration_integrity.py
```

```bash
cd enterprise && poetry run pre-commit run --all-files --show-diff-on-failure --config ./dev_config/python/.pre-commit-config.yaml
```

If running a single subdirectory with nested fixtures, set `--confcutdir` to the nearest relevant fixture root so unrelated top-level fixtures do not mask import or setup problems.

## Auth And Organization Failures

Symptoms:

- Requests succeed with cookie auth but fail with API-key auth.
- `X-Org-Id` returns unexpected 403 or 400.
- Settings, secrets, provider tokens, or billing data come from the wrong org.
- Cached settings/secrets remain stale after an org override changes.

Likely causes:

- API-key-bound org and `X-Org-Id` disagree.
- `X-Org-Id` is not a valid UUID.
- The authenticated user is not a member of the requested org.
- `SaasUserAuth` org-scoped caches were not cleared after override changes.
- A store call ignored the effective org and fell back to the user's current org.

Fix strategy:

- Add focused tests around `SaasUserAuth.get_effective_org_id()` or the route dependency that injects effective org.
- Patch the store session makers used by the called store modules, not only `storage.database.a_session_maker`.
- Assert status codes and error details for malformed UUID, non-member, and API-key mismatch separately.
- Verify billing/settings/secrets calls receive the resolved org ID.

## Storage And Migration Failures

Symptoms:

- SQLite tests fail with missing table errors.
- Async SQLAlchemy tests hang or cannot see seeded rows.
- Alembic check reports duplicate migration prefix, duplicate revision, missing down revision, or multiple heads.
- A migration-specific test passes but store behavior fails.

Fix strategy:

- Import every model needed by the fixture before `Base.metadata.create_all(...)`.
- Use the same file-backed SQLite database for sync and async engines when a test requires both.
- For in-memory async SQLite, use `StaticPool` when multiple connections must see the same schema/data.
- Keep migration filename prefix and `revision` identical.
- Ensure `down_revision` points to the previous single head unless deliberately resolving a branch.
- Pair schema migrations with model/store tests so static migration integrity is not the only coverage.

## Integration Workflow Failures

Git provider failures:

- Token lookup may fail because Keycloak broker tokens, offline tokens, app installation state, or provider user IDs are missing. Mock token manager methods and assert the service handles no-token, expired-token, and refresh paths.
- Repository or webhook operations should be idempotent under retries and handle not-found or permission-denied responses.

Slack failures:

- Redis-backed form state can expire or fail to store/retrieve. Test `SESSION_EXPIRED`, store failure, retrieve failure, and duplicate form submission paths.
- Thread timestamps and message timestamps are part of deduplication keys; include both in fixtures.

Jira/Jira DC/Linear failures:

- Workspace and user linking can be stale, inactive, or missing. Test no workspace, no active user, service-account decryption failure, and payload variants for comments vs labeled tickets.
- Conversation secret enrichment should handle missing credentials without leaking secrets.

Billing failures:

- Stripe customer lookup can miss local DB records and then fall back to Stripe search. Test no org, no customer, customer creation, Stripe error, and disabled billing flag paths.
- Credit calculations should handle missing or `None` LiteLLM budget/spend fields.

Telemetry failures:

- Consent and SaaS identity mapping affect event capture and identify/group calls. Test consent false, consent true, missing orgs, and provider client failures with mocks.

Sync job failures:

- Sync jobs can run before migrations are complete or before external service permissions are ready. Test database unavailable, stale webhook, missing admin permission, retry exhaustion, and idempotent reruns with mocks.

## Hard Usability Cases For Verification

Candidate 1: Add an org-scoped enterprise API route that reads settings and triggers a Stripe customer lookup. The expected solution must resolve effective org precedence correctly, avoid leaking secrets, mock Stripe, seed SQLite org/member/user data, and validate cookie-auth plus API-key-conflict behavior.

Candidate 2: Add a GitLab or Jira webhook workflow that creates a conversation from a provider payload. The expected solution must preserve package-relative imports, use typed payload/view models, mock token and provider clients, handle missing workspace/user/token states, and include a narrow `PYTHONPATH`/`--confcutdir` pytest command.
