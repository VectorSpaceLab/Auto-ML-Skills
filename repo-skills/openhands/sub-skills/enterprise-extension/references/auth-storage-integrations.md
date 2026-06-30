# Auth, Storage, And Integrations

## SaaS Auth Model

Enterprise authentication is different from OSS OpenHands:

- OSS local behavior revolves around user-provided provider tokens or PATs stored in settings.
- Enterprise behavior revolves around Keycloak/OIDC identity, a SaaS user ID, organization context, signed cookies/API keys, and provider tokens retrieved through enterprise token management.
- Git provider service classes such as `SaaSGitHubService` fetch current provider tokens through enterprise token flows rather than directly trusting `request.state.github_token`.

When modifying auth:

- Preserve the distinction between Keycloak user ID, provider user ID, org ID, API-key ID, and provider access token.
- Keep raw secrets in `SecretStr`, encrypted stores, or secret-store objects; do not log token values.
- Validate refresh-token paths and expired-session paths explicitly.
- Patch external Keycloak/OIDC calls in tests; do not require a live Keycloak server.
- Test both cookie-auth and API-key-auth contexts when a route uses effective organization resolution.

## Effective Organization Context

`SaasUserAuth` resolves an effective organization for request-scoped behavior. The important precedence is:

1. Trusted server-side override, after membership/API-key checks.
2. Org-bound API key; a conflicting `X-Org-Id` must be rejected.
3. `X-Org-Id` header, validated as a UUID and checked against memberships.
4. User's current org fallback.

Implementation checklist:

- Clear org-scoped caches when changing the effective org override.
- Use `UUID` values for org IDs at storage boundaries and stringify only for external APIs/log fields.
- Return 400 for malformed `X-Org-Id`; return 403 for non-member or API-key/org mismatch.
- Ensure billing, settings, secrets, resolver, and integration code pass the effective org where needed.
- Add unit tests for fallback, override, membership failure, malformed header, API-key conflict, and cache invalidation.

## Enterprise Storage

Enterprise storage uses SQLAlchemy models and stores, with session creation delegated through `storage.database` to OpenHands global DB config.

Common patterns:

- `a_session_maker()` for async database operations.
- `session_maker()` for legacy synchronous code and backward-compatible kwargs such as `expire_on_commit=False`.
- Store classes for persistence rules; avoid placing complex persistence policy directly in routes.
- SQLite tests for stores and models, with only required models imported before `Base.metadata.create_all(...)`.

When adding a model/table:

- Add or update the SQLAlchemy model under `enterprise/storage/`.
- Add an Alembic migration under `enterprise/migrations/versions/`.
- Import the model in relevant test fixtures so the table is created for SQLite tests.
- Add store-level tests for create/read/update/delete, uniqueness, foreign keys, effective-org scoping, and error behavior.
- Run the migration integrity checker before handoff.

## Settings And Secrets

Enterprise uses SaaS settings/secrets stores configured by `SaaSServerConfig`:

- Settings store class: `storage.saas_settings_store.SaasSettingsStore`.
- Secret store class: `storage.saas_secrets_store.SaasSecretsStore`.
- User auth class: `server.auth.saas_user_auth.SaasUserAuth`.

When changing settings or secrets:

- Keep user-scoped and org-scoped settings distinct.
- Preserve masked-vs-raw secret behavior at API boundaries.
- Avoid moving raw secret values through clients when a lookup/secret-source object is intended.
- Include migration and default-version handling when storage schemas evolve.
- Test org override behavior for stores that are cached on `SaasUserAuth`.

## Integration Managers And Views

Integrations use provider-specific managers, services, callback processors, payload/view models, and storage stores. The shared manager interface receives a `Message`, sends a message back to the provider, and starts an OpenHands job from a provider-specific view object.

Provider areas:

- GitHub and GitLab: provider token lookup, repository and PR/issue context, webhook/callback processing, repository caching, app installation state.
- Slack: OAuth, message/thread handling, Redis-backed temporary state, form interaction deduplication, conversation start/update flows.
- Jira/Jira DC/Linear: issue/comment/labeled-ticket payload parsing, workspace/user linking, service-account credentials, conversation secret enrichment.
- Bitbucket/Bitbucket Data Center/Azure DevOps: provider-specific OAuth/webhook/service-account differences.
- Stripe: billing sessions, customer lookup/creation, payment method checks, subscription access, LiteLLM budget/credit interactions.
- Telemetry/analytics: PostHog and enterprise telemetry tables, consent handling, org/user identity mapping.

Integration implementation checklist:

- Confirm provider enable flags and required env vars before exposing routes or frontend config.
- Keep provider-token retrieval behind `TokenManager`, provider services, or user-auth methods.
- Use provider-specific typed payload/view models rather than unstructured dicts when possible.
- Make webhook handlers idempotent and safe under retries.
- Record enough log context for debugging but never include token or secret values.
- Mock provider clients in unit tests, including timeout, auth failure, missing resource, and stale-link cases.

## Billing And Telemetry

Billing routes and services should be organization-aware. Stripe customer records can be resolved by org ID and fall back only where explicitly documented for compatibility.

When changing billing:

- Gate mutable billing operations behind the billing feature flag.
- Pass effective organization ID to customer lookup, credit, and payment-method functions.
- Mock Stripe async methods in tests; never require real Stripe credentials.
- Validate Decimal/float boundaries for credit displays and LiteLLM budget calculations.
- Test missing customer, missing org, disabled billing, and successful session creation.

When changing telemetry:

- Respect user consent and SaaS-vs-OSS differences.
- Keep identity/group updates separate from event capture behavior.
- Mock PostHog clients and verify call payloads rather than making network calls.
- Add storage tests for telemetry tables and identity mappings when schema changes.

## Environment Toggles

New boolean environment toggles must accept both legacy Helm-style `"1"` and string boolean `"true"` values.

Use this pattern:

```python
os.getenv('MY_FEATURE_ENABLED', 'false').lower() in ('true', '1')
```

Add tests for:

- unset value defaults to false;
- `"false"` is false;
- `"true"` is true;
- `"1"` is true;
- blank value does not accidentally enable the feature.
