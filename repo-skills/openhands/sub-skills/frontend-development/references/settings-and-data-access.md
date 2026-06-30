# Settings and Data Access

## Architecture Rule

Frontend data flow is:

`UI components/routes -> TanStack Query hooks -> API services -> backend endpoints`

Do not call `frontend/src/api/*` services directly from React components or route modules. Components should receive data and mutation functions from hooks, while hooks own query keys, enablement, invalidation, retry behavior, stale times, and toast metadata.

## API Services

Services live under `frontend/src/api/` and wrap the shared axios instance. Keep each service focused on a backend resource and keep request/response types nearby when practical.

Conventions:

- Directory: `feature-service/` for multi-file services or a resource-specific `.ts` file for smaller existing areas.
- Service file: `feature-service.api.ts`.
- Types file: `feature.types.ts`.
- Export: `featureService` or an existing project-specific client name.
- Method style: async object methods, typed return values, and destructured params for self-documenting calls.

Use existing services as evidence before adding new structure. Preserve current endpoint prefixes and auth behavior; backend route changes belong to `backend-development`.

## Query Hooks

Read hooks live in `frontend/src/hooks/query/` and should be named `use<Resource>` or `use<ResourceList>` based on returned data. Use TanStack `useQuery` for reads and centralize reusable query key builders when multiple hooks or invalidations need the same key.

Checklist for query hooks:

- Use a stable `queryKey`; include every scope input that changes returned data.
- Include selected organization id when data is organization-sensitive.
- Gate with `enabled` when auth, config, intermediate routes, or organization selection is required.
- Use `meta: { disableToast: true }` for expected background/controlled errors.
- Use explicit retry rules for known terminal errors, such as not retrying settings 404s.
- Set `staleTime` and `gcTime` when the data should remain warm but not permanently fresh.
- Return defaults carefully; avoid `initialData` when prepopulating cache would break tests or expectations.

Settings evidence:

- `useSettings(scope = "personal")` reads auth/config/selected organization and uses `SETTINGS_QUERY_KEYS.byScope(scope, organizationId)`.
- `getSettingsQueryFn("org", organizationId)` calls organization settings; personal settings call the settings service.
- Settings normalization merges `DEFAULT_SETTINGS`, schema-managed SDK settings, conversation settings, MCP parsing, and legacy flat fields.
- Tests assert cache isolation between organizations and the newer scoped settings key shape.

## Mutation Hooks

Write hooks live in `frontend/src/hooks/mutation/` and should be named `use<Action>` such as `useSaveSettings`, `useAddMcpServer`, or `useDeleteGitProviders`. Use `useMutation`, invalidate the exact query keys affected by the write, and keep components focused on user interaction and toast responses.

Checklist for mutation hooks:

- Trim or normalize payload values before sending where the domain requires it.
- Drop read-only schema fields from save payloads.
- Convert local UI structures into API/SDK payload structures inside the hook, not in every component.
- Fetch fresh settings inside mutation functions when editing nested settings derived from current server state to avoid stale closures.
- Invalidate scoped query keys on success.
- Use `meta: { disableToast: true }` when components handle success/error toasts themselves.
- Keep logout separate from credential disconnect flows; `useLogout` is app logout and should not be reused for git provider token deletion.

## Settings Pattern 1: Entity Management, Immediate Save

Use this for independent items where each add/edit/delete is an atomic action and the user should not need a separate Save Changes button. Existing examples include MCP servers, API keys, secrets, and git provider tokens.

Characteristics:

- Dedicated mutation hook for each operation.
- Action saves immediately on add, edit, delete, connect, or disconnect.
- Query invalidation updates UI after success.
- No global `isDirty` state for the whole page.
- Components may keep local view state for add/edit forms and confirmation modals.

MCP server flow evidence:

- `useAddMcpServer` fetches fresh settings, parses current MCP config, appends one server, saves `agent_settings_diff.mcp_config`, and invalidates `SETTINGS_QUERY_KEYS.personal(organizationId)`.
- `useDeleteMcpServer` fetches fresh settings, removes by encoded id such as `sse-0`, saves the new config, and invalidates the personal settings key.
- `mcp-settings.tsx` uses add/update/delete mutation hooks for server entities and a separate save path for the search API key.

Git provider token flow evidence:

- `useAddGitProviders` and `useDeleteGitProviders` call the V1 secrets endpoints via `SecretsService` and invalidate personal settings.
- Do not use `useLogout` for disconnecting tokens; logout targets app session behavior and clears unrelated client state.

## Settings Pattern 2: Form Settings, Manual Save

Use this for configuration forms where multiple fields are interdependent or should be saved together after local edits. Existing examples include Application, LLM, Agent, Skills, Condenser, and verification settings.

Characteristics:

- UI tracks dirty state for fields or derives clean/dirty status from local form state.
- A Save Changes button is disabled while clean or pending.
- One submit/action handler extracts form values, normalizes them, and calls `useSaveSettings`.
- Component handles success/error toasts and resets dirty flags on settle.

Application settings evidence:

- `app-settings.tsx` tracks dirty flags for language, analytics, sound notifications, proactive starters, solvability analysis, sandbox grouping, max budget, git user name, and git email.
- It falls back to `DEFAULT_SETTINGS` for missing values.
- It parses numeric max budget with `parseMaxBudgetPerTask`.
- It shows SaaS-only switches based on `useConfig().data.app_mode`.
- It calls `useSaveSettings` once with a partial settings payload, then resets dirty flags.

`useSaveSettings` evidence:

- Removes `agent_settings_schema` and `conversation_settings_schema` before save.
- Converts non-empty `conversation_settings_diff` and `agent_settings_diff` into save payloads and removes full settings objects.
- Trims LLM API key, search API key, git user name, and git user email.
- Saves org settings through `organizationService.saveOrganizationSettings` when scope is `"org"` and an organization id is present.
- Invalidates `SETTINGS_QUERY_KEYS.byScope(scope, organizationId)` and also personal settings when saving org settings.

## Adding a New User Setting

When adding a user setting, update every layer that owns the value.

Frontend checklist:

1. Add the field to `frontend/src/types/settings.ts` in `Settings` and any relevant supporting type.
2. Add a default in `frontend/src/services/settings.ts` under `DEFAULT_SETTINGS`.
3. Update `frontend/src/hooks/query/use-settings.ts` normalization if the backend can omit the value, the value moved into `agent_settings`/`conversation_settings`, or legacy flat fields must be reconciled.
4. Update `frontend/src/hooks/mutation/use-save-settings.ts` if the field needs trimming, diff conversion, schema omission, or org-scoped handling.
5. Add UI in the appropriate route or component.
6. Choose Pattern 1 or Pattern 2 and wire either dedicated mutation hooks or a manual-save form.
7. Add i18n keys to `translation.json`, regenerate declarations with `npm run make-i18n`, and use `I18nKey` in components.
8. Add focused tests for parsing, normalization, dirty/save behavior, cache invalidation, org scope, and user-visible states.

Backend model/API changes are outside this sub-skill; route them to `backend-development` and coordinate contracts before frontend changes assume new fields exist.

## Query Key and Organization Scope

OpenHands supports personal and organization settings. Organization-aware frontend data must not share cache entries across org ids.

Use central key builders when available:

- `SETTINGS_QUERY_KEYS.all` for removing all settings queries.
- `SETTINGS_QUERY_KEYS.byScope(scope, organizationId)` for the canonical scoped key.
- `SETTINGS_QUERY_KEYS.personal(organizationId)` for personal settings in the selected organization context.

Test cache behavior when adding or changing keys:

- Render a hook with a selected org id and assert cached data appears under the org-specific key.
- Switch selected org id and rerender; assert the hook fetches different data and both caches remain isolated.
- Assert stale old keys are not populated.

## i18n for Settings and Data UI

Static text should use `I18nKey` imports. For constrained dynamic keys, use a typed cast only when the set of possible keys is obvious from an enum/object, such as sandbox grouping labels derived from `SandboxGroupingStrategyOptions`.

After editing translations:

1. Run `npm run make-i18n`.
2. Run `npm run check-translation-completeness`.
3. Use the bundled `check_i18n_key_presence.mjs` as a quick single-key check when reviewing a specific change.
4. Add or update tests for hardcoded English avoidance when the UI has historically regressed.

## Common Review Smells

- A component imports `SettingsService`, `organizationService`, `SecretsService`, `ApiKeysClient`, or another API client directly.
- A query key omits organization id, scope, filters, pagination, or resource id.
- A mutation saves a stale nested settings object captured from render instead of fetching fresh state at mutation time.
- A form setting saves immediately even though related fields should be committed together.
- An entity setting waits for a page-level Save Changes button even though add/edit/delete is independent.
- New settings have defaults in the UI but no normalization for missing backend values.
- Translation keys are added to `translation.json` but `declaration.ts` was not regenerated.
- Git provider disconnect calls logout or clears global login state.
