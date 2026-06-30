---
name: enterprise-extension
description: "Modify and validate the OpenHands enterprise SaaS extension, including auth, storage, integrations, migrations, telemetry, billing, and enterprise tests."
disable-model-invocation: true
---

# Enterprise Extension

Use this sub-skill when a task changes the enterprise SaaS extension rather than the OSS backend, frontend, or repo-wide tooling. It covers the enterprise package, dynamic SaaS overrides, authentication and organization context, storage/database behavior, third-party integrations, billing, telemetry, migrations, sync jobs, and enterprise validation commands.

## Route Here

Route here for changes involving:

- SaaS app configuration and dynamic overrides: `SaaSServerConfig`, SaaS middleware/lifespan, enterprise routes, and app-mode feature flags.
- Authentication and authorization: Keycloak/OIDC tokens, cookies, API keys, `X-Org-Id`, effective organization resolution, role permissions, user settings, and secret inheritance in enterprise contexts.
- Enterprise storage: SQLAlchemy models/stores, database session wrappers, org/member/user settings stores, telemetry/billing tables, and SQLite-backed unit tests.
- Integrations: GitHub, GitLab, Slack, Jira, Jira Data Center, Linear, Bitbucket, Bitbucket Data Center, Azure DevOps, Stripe billing, PostHog/analytics, Resend, and resolver workflows.
- Alembic migrations and static migration integrity checks.
- Enterprise-only unit tests, fixtures, and pre-commit validation.

Do not use this sub-skill for unrelated OSS backend routes, general frontend UI work, or repo-wide CI/lockfile policy unless the enterprise extension is the primary reason for the change.

## Reference Map

- [Enterprise workflows](references/enterprise-workflows.md): code ownership, dynamic override model, import style, test strategy, validation commands, migrations, sync jobs, and native verification candidates.
- [Auth, storage, and integrations](references/auth-storage-integrations.md): practical implementation patterns for SaaS auth, org context, database stores, billing, telemetry, and integration managers.
- [Troubleshooting](references/troubleshooting.md): install/import failures, optional dependencies, config/data issues, CLI/API misuse, migration conflicts, and workflow-specific failure modes.

## Core Rules

- Keep enterprise application imports package-relative, for example `from storage.database import a_session_maker`, `from server.auth.saas_user_auth import SaasUserAuth`, and `from integrations.github.github_service import SaaSGitHubService`; avoid `enterprise.` prefixes in enterprise application code.
- Preserve the SaaS identity model: enterprise request handling centers on Keycloak user IDs and organization context, not user-provided GitHub PATs.
- Prefer isolated unit tests with SQLite, `AsyncMock`, `MagicMock`, patched external clients, and local fixtures over live PostgreSQL, Redis, Keycloak, Stripe, Slack, GitHub, GitLab, Jira, or Linear calls.
- Treat `enterprise/sync/` jobs as operational code with credential and service side effects; validate their pure logic with mocks and do not run them casually as smoke checks.
- For new boolean env toggles, accept both `"true"` and `"1"` as truthy values and add tests for both forms.

## Quick Validation

Use the narrowest safe command first, then broaden as confidence grows:

```bash
PYTHONPATH=".:$PYTHONPATH" poetry run --project=enterprise pytest enterprise/tests/unit/<area> --confcutdir=enterprise/tests/unit/<area>
```

```bash
PYTHONPATH=".:$PYTHONPATH" poetry run pytest tests/unit/test_enterprise_migration_integrity.py
```

```bash
cd enterprise && poetry run pre-commit run --all-files --show-diff-on-failure --config ./dev_config/python/.pre-commit-config.yaml
```
