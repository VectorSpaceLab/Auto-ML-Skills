---
name: frontend-development
description: "Modify the OpenHands React/Vite frontend safely, including TanStack Query data access, settings UI patterns, i18n, archived conversation UI, tests, and build/lint workflows."
disable-model-invocation: true
---

# Frontend Development

Use this sub-skill when changing the OpenHands frontend under `frontend/`: React routes and components, TanStack Query hooks, frontend services, settings pages, i18n keys, chat/runtime UI, and Vitest/Playwright coverage.

Route backend API implementation, Python app-server behavior, and storage models to `backend-development`. Route enterprise SaaS backend, database migrations, billing/auth integrations, and enterprise-only server behavior to `enterprise-extension`. Route repo-wide hook policy, lockfile regeneration, GitHub Actions pinning, and non-frontend release maintenance to `repo-maintenance`.

## Start Here

- Read [Frontend Workflows](references/frontend-workflows.md) for project structure, scripts, tests, archived conversation UI, chat/action rendering, and validation commands.
- Read [Settings and Data Access](references/settings-and-data-access.md) before adding API calls, TanStack Query hooks, settings screens, MCP/API-key/secrets flows, or organization-scoped cache behavior.
- Read [Troubleshooting](references/troubleshooting.md) when installs, typegen, i18n, tests, mocks, WebSocket state, or runtime tabs fail.
- Use [check_i18n_key_presence.mjs](scripts/check_i18n_key_presence.mjs) for a quick non-mutating check that a translation key exists in both `translation.json` and the generated declaration file.

## Core Rules

- UI components must not call API services directly; wrap reads in `frontend/src/hooks/query/use-*.ts` and writes in `frontend/src/hooks/mutation/use-*.ts`.
- Use `frontend/src/api/*` service modules as the HTTP boundary and keep request/response types near the service when practical.
- Keep query keys stable and scoped, especially settings keys that include scope and selected organization id.
- Add new user settings across types, defaults, normalization, save payloads, UI, i18n, and tests; choose the correct settings save pattern before coding.
- Add or update `frontend/src/i18n/translation.json`, then run `npm run make-i18n` so `frontend/src/i18n/declaration.ts` and locale files are regenerated.
- For archived conversations, treat `sandbox_status === "MISSING"` as read-only: keep chat input hidden, runtime tabs non-interactive, and mocks/tests returning `isArchived` from `useAgentState`.

## Native Validation Candidates

- `cd frontend && npm run lint:fix && npm run build` for frontend changes before final handoff when validation is allowed.
- `cd frontend && npm run test -- -t "<name>"` for focused settings, hook, route, chat, i18n, or utility tests.
- `cd frontend && npm run check-translation-completeness` after translation edits.
- `node /path/to/openhands-skill/sub-skills/frontend-development/scripts/check_i18n_key_presence.mjs --translation frontend/src/i18n/translation.json --declaration frontend/src/i18n/declaration.ts --key 'SETTINGS$EXAMPLE'` as a quick bundled helper check from a copied skill tree, adjusting paths to the current checkout.
