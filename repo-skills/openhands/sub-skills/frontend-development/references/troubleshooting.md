# Frontend Troubleshooting

## Install and Tooling

Symptoms:

- `npm install` or scripts fail with unsupported engine errors.
- React Router typegen or TypeScript fails before tests run.
- Pre-commit setup cannot proceed because a repo-wide tool is missing.

Checks and fixes:

- Use Node `>=22.12.0`; the frontend declares Volta Node `22.12.0` and `npm@10.5.0`.
- Run frontend commands from `frontend/` unless the command is a root `make` target.
- Run `npm install` before frontend validation if `node_modules/` is missing.
- `npm run typecheck` includes `react-router typegen`; typegen failures often indicate route module export/signature issues rather than pure TypeScript errors.
- Repo-wide hook installation is required by project policy before code changes, but it depends on root tooling. If the environment lacks that tooling, record the failed command and continue only with safe, local drafting or read-only work.

## Import and Path Aliases

Symptoms:

- Tests fail to resolve `#/...` imports.
- A new file compiles locally but fails under Vitest or React Router build.

Checks and fixes:

- Follow existing `#/` alias imports for frontend source modules.
- Place React hooks under `src/hooks/query`, `src/hooks/mutation`, or another existing hook subdirectory instead of inventing a new alias root.
- Ensure test files use the same alias setup as existing tests, or relative imports only for local test utilities.
- For React SVG imports, follow existing `?react` usage and Vite plugin expectations.

## Optional Dependency and Browser Tool Failures

Symptoms:

- Playwright tests fail because browsers are missing.
- MSW-backed dev mode starts but routes show incomplete data.
- Monaco, xterm, WebSocket, or browser tab components fail in a jsdom test.

Checks and fixes:

- Prefer focused Vitest for unit/component changes; use Playwright only for browser-flow changes.
- MSW mocks are partial; if a feature needs unmocked backend behavior, run against the actual backend or add a targeted mock.
- Mock browser-only APIs in tests when the component uses iframe, terminal, clipboard, WebSocket, storage, ResizeObserver, or scrolling behavior.
- Use helpers in `__tests__/helpers/` for WebSocket-related tests rather than rebuilding setup from scratch.

## Config and Data Problems

Symptoms:

- Settings data is missing until refresh.
- Organization switching shows stale values.
- SaaS-only UI appears in OSS mode or vice versa.
- A setting saves but the UI reverts.

Checks and fixes:

- Ensure query keys include every scope input: selected organization id, scope, resource id, filters, or pagination.
- Invalidate the same key shape used by the read hook. For settings, use `SETTINGS_QUERY_KEYS.byScope` or `SETTINGS_QUERY_KEYS.personal` as appropriate.
- Gate settings reads on auth/config/intermediate-page state just like existing `useSettings` does.
- If saving nested SDK settings, send diffs such as `agent_settings_diff` or `conversation_settings_diff` instead of full read-only schema payloads.
- Normalize backend omissions through `DEFAULT_SETTINGS` so first-time users and 404 settings responses still render usable forms.
- Use `useConfig().data.app_mode` to separate SaaS-only UI from OSS UI.

## API and Hook Misuse

Symptoms:

- Multiple duplicate requests occur.
- Loading/error state is inconsistent across components.
- Cache does not update after a mutation.
- Review finds API service imports inside route/component files.

Checks and fixes:

- Move direct service calls out of components into query/mutation hooks.
- Use `useQuery` for reads and `useMutation` for writes.
- Set `enabled` for queries that require auth, selected org, config, route params, or a non-intermediate page.
- Use mutation `onSuccess` to invalidate or update exact affected query keys.
- Fetch fresh settings inside mutations that modify nested arrays or objects, especially MCP server add/edit/delete flows.
- Add hook tests with a fresh QueryClient and retries disabled when changing cache behavior.

## Settings Workflow Failures

Symptoms:

- Save Changes is always disabled or always enabled.
- Entity add/delete waits for an unrelated form save.
- MCP server edits overwrite another server.
- Git provider disconnect logs the user out.

Checks and fixes:

- For form settings, track local dirty state or compare local values against current settings; reset dirty flags after settled mutation.
- For entity settings, use dedicated immediate-save mutations and confirmation modals where destructive.
- For MCP changes, fetch fresh settings inside mutation functions, parse current MCP config, modify a copy, convert to SDK MCP config, and save through `agent_settings_diff.mcp_config`.
- For git providers, use secrets endpoints through `useAddGitProviders` or `useDeleteGitProviders`; never reuse `useLogout`.
- For org settings, ensure the selected organization id is present before saving and invalidate personal settings if org defaults can affect personal display.

## i18n Failures

Symptoms:

- `I18nKey.NEW_KEY` is missing after adding translation JSON.
- `npm run check-translation-completeness` reports missing or extra languages.
- UI renders raw keys such as `SETTINGS$...`.
- Hardcoded English appears in tests.

Checks and fixes:

- Add the key to `frontend/src/i18n/translation.json` for every supported language.
- Run `npm run make-i18n` to regenerate `frontend/src/i18n/declaration.ts` and locale JSON files.
- Run `npm run check-translation-completeness` after translation edits.
- Use `useTranslation()` plus `I18nKey` for static keys.
- For dynamic keys, ensure the constructed key exists and has tests or a fallback.
- Use the bundled `check_i18n_key_presence.mjs` for a quick single-key read-only check; it is not a replacement for completeness checks.

## Archived Conversation and Runtime UI Failures

Symptoms:

- Archived conversations show loading spinners forever.
- Chat input remains usable on archived conversations.
- Terminal, VS Code, browser, planner, or controls try to connect to a missing sandbox.
- Tests that mock `useAgentState` fail after archived-state changes.

Checks and fixes:

- Treat `sandbox_status === "MISSING"` as archived and read-only.
- `useAgentState` should return `AgentState.STOPPED` and `isArchived: true` for missing sandboxes, even if a live execution status exists.
- Runtime tabs should show translated read-only messages before starting URL/terminal/runtime loading paths.
- Planner and other sandbox-dependent buttons should be disabled when `isArchived` is true.
- Chat UI should render `ArchivedBanner` instead of `InteractiveChatBox` when archived.
- Test mocks for `useAgentState` must include `isArchived`; older mocks that return only `curAgentState` are incomplete.

## Build, Lint, and Test Failures

Symptoms:

- `npm run lint` fails but `npm run lint:fix` changes files.
- `npm run build` fails after a route change.
- Focused tests pass but full frontend validation fails.

Checks and fixes:

- Run specific tests first, then `npm run lint:fix && npm run build` when finalizing frontend changes.
- If `lint:fix` changes files, rerun the failing command to verify the fix.
- Build failures after route edits often come from React Router type generation, loader/action typing, or route exports.
- Prettier checks only cover `src/**/*.{ts,tsx}` in the package script; tests may still need manually consistent formatting.
- Do not fix unrelated failing tests; record them separately if they block broad validation.

## Difficult Synthetic Usability Cases

Use these as higher-value cases when verifying this sub-skill:

1. Add an organization-scoped manual-save setting that appears only in SaaS mode, has a default for first-time users, uses generated i18n keys, preserves cache isolation across org switches, and validates with focused hook plus route tests.
2. Add a sandbox-dependent chat-side control that is hidden or disabled for archived conversations, uses translated labels, never calls an API service directly from the component, and has tests for running, loading, and `sandbox_status === "MISSING"` states.
