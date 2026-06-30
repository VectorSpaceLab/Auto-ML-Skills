# Enterprise Workflows

## Scope And Ownership

The enterprise extension is a Python package layered on top of OpenHands. It is packaged separately as `enterprise_server`, depends on the local `openhands-ai` package, and targets Python `>=3.12,<3.14`.

Primary enterprise source areas:

- `enterprise/server/`: SaaS server config, middleware, auth, routes, services, sharing, rate limits, verified model routes, and lifespan hooks.
- `enterprise/storage/`: SQLAlchemy models, store classes, database/session wrappers, Redis helpers, org/user/settings/secrets/billing/telemetry persistence.
- `enterprise/integrations/`: provider-specific managers, services, callbacks, views, webhook stores, resolver context, Slack/Jira/GitHub/GitLab/Bitbucket/Azure DevOps workflows, and Stripe service helpers.
- `enterprise/migrations/`: Alembic environment and versioned database migrations.
- `enterprise/sync/`: operational sync/backfill jobs that may contact external systems.
- `enterprise/tests/unit/`: enterprise-focused tests and fixtures.

Route away from this sub-skill when the task primarily changes OSS backend behavior that enterprise only consumes, generic React UI, or repo-wide CI/packaging policy.

## SaaS Extension Model

Enterprise extends OpenHands in two ways:

1. Stacked behavior: enterprise middleware, routes, services, and lifespan hooks run alongside the OSS OpenHands app.
2. Dynamic overrides: enterprise config and classes replace OSS implementations through configured import paths. `SaaSServerConfig` is the central example and sets SaaS-specific classes such as settings store, secret store, user auth, conversation secret enricher, and analytics user provider.

When changing a dynamic override:

- Verify the configured class path string still resolves after renames.
- Preserve the constructor/interface expected by the OSS call site.
- Check both SaaS behavior and the fallback OSS behavior when the same global config is read outside enterprise.
- Avoid importing enterprise modules into OSS-only paths unless the import is guarded or configured dynamically.

## Import Conventions

Enterprise application code uses package-relative imports because it is run with `enterprise` on `PYTHONPATH` or as the active project root.

Preferred examples:

- `from storage.database import a_session_maker`
- `from server.auth.saas_user_auth import SaasUserAuth`
- `from integrations.gitlab.gitlab_service import SaaSGitLabService`

Avoid examples in enterprise application code:

- `from enterprise.storage.database import a_session_maker`
- `from enterprise.server.auth.saas_user_auth import SaasUserAuth`

Some tests that import scripts or run from the repo root may use `enterprise.` import paths deliberately; do not mechanically rewrite them without checking the execution context.

## Testing Patterns

Enterprise tests should be fast, isolated, and external-service-free.

Use these patterns:

- SQLite databases for storage/unit tests. Existing fixtures use file-backed SQLite and `sqlite+aiosqlite`; some focused tests use in-memory SQLite with `StaticPool`.
- `Base.metadata.create_all(...)` to build only the imported SQLAlchemy model tables needed by the test.
- `AsyncMock` for async store/client/service methods and `MagicMock` for complex model or service objects.
- Patch the import path used by the code under test, such as `storage.org_member_store.a_session_maker` or `integrations.jira.jira_manager.JiraIntegrationStore.get_instance`.
- Prefer typed fixture factories for Keycloak user info, organizations, memberships, provider tokens, integration payloads, and webhook views.
- Mock HTTP clients, Keycloak, Stripe, Slack, GitHub, GitLab, Jira, Redis, PostHog, Resend, and LiteLLM rather than using live credentials.

Narrow command examples:

```bash
PYTHONPATH=".:$PYTHONPATH" poetry run --project=enterprise pytest enterprise/tests/unit/server/auth --confcutdir=enterprise/tests/unit/server/auth
```

```bash
PYTHONPATH=".:$PYTHONPATH" poetry run --project=enterprise pytest enterprise/tests/unit/integrations/jira --confcutdir=enterprise/tests/unit/integrations/jira
```

```bash
PYTHONPATH=".:$PYTHONPATH" poetry run --project=enterprise pytest enterprise/tests/unit/storage --confcutdir=enterprise/tests/unit/storage
```

For a single enterprise test file:

```bash
PYTHONPATH=".:$PYTHONPATH" poetry run --project=enterprise pytest enterprise/tests/unit/test_billing.py --confcutdir=enterprise/tests/unit
```

## Validation Commands

Use enterprise validation when enterprise files changed:

```bash
cd enterprise && poetry run pre-commit run --all-files --show-diff-on-failure --config ./dev_config/python/.pre-commit-config.yaml
```

The `--show-diff-on-failure` flag matters because CI uses it to expose formatter changes and lint diffs.

For full enterprise unit tests when dependencies are installed:

```bash
PYTHONPATH=".:$PYTHONPATH" poetry run --project=enterprise pytest --forked -n auto -s -p no:ddtrace -p no:ddtrace.pytest_bdd -p no:ddtrace.pytest_benchmark ./enterprise/tests/unit --cov=enterprise --cov-branch
```

If dependencies are not installed, do not claim runtime coverage; record the missing dependency or install blocker and still run static or focused checks that are available.

## Migrations

Enterprise migrations live under `enterprise/migrations/versions/` and are sequentially numbered. When adding or editing migrations:

- Sync with the target branch before finalizing to reduce conflicts.
- Use a unique numeric filename prefix that matches the `revision` string.
- Set `down_revision` to the previous head unless deliberately creating a branch merge.
- Keep exactly one Alembic head for normal development.
- Add or update storage model tests when schema behavior changes.

Safe static migration check:

```bash
python scripts/check_enterprise_migration_integrity.py
```

Focused test for the checker:

```bash
PYTHONPATH=".:$PYTHONPATH" poetry run pytest tests/unit/test_enterprise_migration_integrity.py
```

The migration checker is reference-only in this generated skill: use the repository command when working in the repo, but this sub-skill does not bundle a copy because the source script is small, repo-maintained, and tied to the current migration tree.

## Sync Jobs

`enterprise/sync/` contains operational scripts for jobs such as GitLab webhook installation, Resend contact syncing, and data enrichment. These jobs can depend on production-style database configuration, credentials, external APIs, and timing/retry behavior.

When changing sync code:

- Separate pure planning/filtering logic from side-effectful execution.
- Test with mocked stores, service clients, sleep/retry calls, and response objects.
- Do not run sync scripts as local smoke checks unless the user explicitly provides a safe environment and credentials.
- Validate idempotency: repeated job runs should not duplicate webhooks, contacts, or records.

## Native Candidate Map

Useful native candidates for verification planning:

- Auth/org context: `enterprise/tests/unit/server/auth/test_saas_user_auth_effective_org.py`, `enterprise/tests/unit/test_authorization.py`, and API-key/org route tests.
- Storage: `enterprise/tests/unit/storage/`, `enterprise/tests/unit/test_org_store.py`, settings/secrets stores, telemetry metrics, and database wrapper tests.
- Integrations: provider directories under `enterprise/tests/unit/integrations/` plus resolver context tests.
- Billing: `enterprise/tests/unit/test_billing.py`, `enterprise/tests/unit/test_billing_stripe_integration.py`, `enterprise/tests/unit/test_stripe_service_db.py`.
- Migrations: `tests/unit/test_enterprise_migration_integrity.py` and migration-specific tests under `enterprise/tests/unit/`.
- Sync: `enterprise/tests/unit/sync/` with external clients mocked.
