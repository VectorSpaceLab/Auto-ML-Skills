# Frontend Workflows

## Scope and Layout

The frontend is a React 19, React Router 7, Vite, TypeScript, Tailwind, TanStack Query, i18next, MSW, and Vitest application in `frontend/`. Use Node `>=22.12.0`; the package is private and declares `npm@10.5.0` plus Volta Node `22.12.0`.

Key areas:

- `frontend/src/api/`: typed service modules around the shared axios instance.
- `frontend/src/hooks/query/`: TanStack Query read hooks.
- `frontend/src/hooks/mutation/`: TanStack Query mutation hooks.
- `frontend/src/routes/`: React Router route modules and settings screens.
- `frontend/src/components/`: domain, layout, modal, and shared UI components.
- `frontend/src/i18n/`: `translation.json`, generated `declaration.ts`, and i18n setup.
- `frontend/src/services/`: frontend-only service helpers such as default settings and chat/action helpers.
- `frontend/__tests__/`: Vitest and React Testing Library tests.
- `frontend/tests/`: Playwright specs.
- `frontend/scripts/`: i18n generation and translation completeness checks.

## Package Scripts

Run commands from `frontend/` unless explicitly using root `make` targets.

- `npm install`: install frontend dependencies.
- `npm run dev`: generate i18n, then start React Router dev with `VITE_MOCK_API=false`.
- `npm run dev:mock`: generate i18n, then start with MSW API mocks and non-SaaS mode.
- `npm run dev:mock:saas`: generate i18n, then start with MSW API mocks and SaaS mode.
- `npm run build`: generate i18n, then build React Router output.
- `npm start -- --port 3001`: serve the built frontend.
- `npm run test`: run Vitest.
- `npm run test -- -t "<name>"`: run a focused Vitest test by name.
- `npm run test:e2e`: run Playwright.
- `npm run test:coverage`: generate i18n, then run Vitest coverage.
- `npm run lint`: generate i18n, run typegen, TypeScript, ESLint, and Prettier checks.
- `npm run lint:fix`: run ESLint fixes and Prettier writes for `src`.
- `npm run typecheck`: run React Router typegen and TypeScript.
- `npm run make-i18n`: regenerate locale JSON files and `src/i18n/declaration.ts` from `src/i18n/translation.json`.
- `npm run check-translation-completeness`: verify each translation key has exactly the supported language set.

For full app execution, root `make build` and `make run` build and run backend plus frontend. Do not run the full app unless needed for the change.

## Development Flow

1. Identify whether the change is UI-only, data-access, settings, chat/runtime, i18n, or testing.
2. For API-backed UI, inspect or add a service in `src/api/`, then expose it through a query or mutation hook; do not call services directly from components.
3. For settings screens, choose Pattern 1 or Pattern 2 from `settings-and-data-access.md` before editing state, save buttons, or mutations.
4. For user-visible text, use `useTranslation()` with `I18nKey` entries where possible. Add keys to `translation.json` and regenerate declarations with `npm run make-i18n`.
5. Add or update focused tests close to the behavior: hook tests for cache/mutation behavior, route/component tests for UI states, utility tests for parsing/formatting, and i18n tests for translation invariants.
6. Validate narrowly first with `npm run test -- -t "<name>"`, then run `npm run lint:fix && npm run build` when finalizing frontend changes.

## Testing Patterns

Vitest tests use React Testing Library, `userEvent`, MSW, and explicit mocks. Prefer accessible queries by role, label, text, or test id over brittle selectors.

Common patterns:

- Use `renderWithProviders()` from the frontend test utilities for components needing app providers or stores.
- Use a fresh `QueryClient` with retries disabled for TanStack Query hook tests.
- Mock route hooks with `vi.mock("react-router", ...)` when the component depends on params, navigation, revalidation, or loaders.
- Mock query hooks such as `useConfig`, `useIsAuthed`, `useActiveConversation`, or `useSettings` when the test target is UI behavior rather than data fetching.
- When mocking `useAgentState`, always include both `curAgentState` and `isArchived`; include `executionStatus` only when the target reads it.
- For organization-sensitive hooks, test cache isolation by asserting query keys include the selected organization id.
- For WebSocket/event behavior, reuse helpers under `__tests__/helpers/` where available.

Representative focused candidates:

- Settings/query cache isolation: `npm run test -- -t "Organization-scoped query hooks"`.
- Query key helpers: `npm run test -- -t "SETTINGS_QUERY_KEYS"`.
- Settings parsing: `npm run test -- -t "parseMaxBudgetPerTask"` or `npm run test -- -t "extractSettings"`.
- Archived state: `npm run test -- -t "useAgentState"` and route/component tests around archived conversation view, VS Code tab, terminal, planner, and chat interface.
- i18n invariants: `npm run test -- -t "translation.json"` and `npm run check-translation-completeness`.

## Archived Conversation UI

Archived conversations are represented by `sandbox_status === "MISSING"`. The unified state hook returns `AgentState.STOPPED` and `isArchived: true` even if a live execution status is present. This avoids infinite loading or runtime-starting states for conversations that cannot resume.

Current touchpoints:

- `frontend/src/hooks/use-agent-state.ts`: maps V1 execution status plus sandbox status to frontend agent state and archive flag.
- `frontend/src/components/features/chat/chat-interface.tsx`: shows `ArchivedBanner` and hides `InteractiveChatBox` when archived.
- `frontend/src/components/features/chat/archived-banner.tsx`: read-only banner using `CONVERSATION$ARCHIVED_READ_ONLY`.
- `frontend/src/components/features/terminal/terminal.tsx`: shows read-only archived message and hides terminal DOM sizing.
- `frontend/src/routes/vscode-tab.tsx`: returns archived read-only content before loading iframe URLs.
- `frontend/src/routes/planner-tab.tsx`: disables plan creation for archived conversations.
- `frontend/src/components/features/conversation/archived-conversation-view.tsx`: archived conversation shell.

When adding UI that depends on a running sandbox, gate the interaction with `isArchived` or `sandbox_status`, and prefer a translated read-only message over loading placeholders.

## Chat and Action Rendering

Chat input is split across `frontend/src/components/features/chat/interactive-chat-box.tsx`, `custom-chat-input.tsx`, `components/chat-input-*`, and hooks under `frontend/src/hooks/chat/`. Keep cross-cutting keyboard, slash-command, draft, or file-upload behavior in hooks/utilities rather than large component bodies.

Action and observation labels use translation keys:

- V0 action type enum: `frontend/src/types/action-type.tsx`.
- V0 event rendering: `frontend/src/components/features/chat/event-content-helpers/get-event-content.tsx`.
- V1 event rendering: `frontend/src/components/v1/chat/event-content-helpers/get-event-content.tsx`.
- Translation key shape: `ACTION_MESSAGE$...` and `OBSERVATION_MESSAGE$...` in `translation.json` and generated `I18nKey` declarations.

When adding a new action/observation display:

1. Add or update the typed action/observation shape.
2. Update the V0 and/or V1 rendering helper as appropriate.
3. Add translation keys with interpolation placeholders such as command, path, pattern, or tool name.
4. Regenerate i18n declarations.
5. Add rendering tests that cover translated labels, fallback behavior, and any summary override.

## i18n Workflow

`frontend/src/i18n/translation.json` is the source of truth. `frontend/scripts/make-i18n-translations.cjs` mutates generated locale files and `frontend/src/i18n/declaration.ts`; use it through `npm run make-i18n`, not as a read-only check. `frontend/scripts/check-translation-completeness.cjs` verifies each key includes exactly the supported languages listed by i18n setup.

For a new key:

1. Add the key to `translation.json` with all supported languages.
2. Use stable key prefixes such as `SETTINGS$`, `COMMON$`, `CONVERSATION$`, `ACTION_MESSAGE$`, or the nearest feature prefix.
3. Run `npm run make-i18n`.
4. Import/use `I18nKey.KEY_NAME` when the key is static. Use a typed cast only for constrained dynamic keys.
5. Run translation completeness checks and focused tests.

The bundled helper `scripts/check_i18n_key_presence.mjs` only checks that a single key is present in `translation.json` and `declaration.ts`. It intentionally does not mutate generated files or verify every language.
