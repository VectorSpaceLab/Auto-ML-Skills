# Backend Workflows

## Backend Map

OpenHands backend development centers on the Python package `openhands-ai` version `1.8.0`, requiring Python `>=3.12,<3.14`. The main backend package is `openhands`, with the FastAPI V1 app server under `openhands/app_server` and compatibility server entry points under `openhands/server`.

Important backend areas:

- `openhands/app_server/app.py`: constructs the FastAPI app, includes the V1 router and status router, mounts MCP and optional frontend static files, and registers middleware.
- `openhands/app_server/v1_router.py`: aggregates V1 routers under `/api/v1`.
- `openhands/app_server/config.py`: app-server configuration, dependency injector selection, event/sandbox/conversation service defaults, and env-driven fallback behavior.
- `openhands/app_server/settings`: user settings, diff-based settings updates, LLM profiles, schema endpoints, and settings store access.
- `openhands/app_server/secrets`: git-provider tokens and custom secrets separated from settings storage.
- `openhands/app_server/sandbox`: sandbox lifecycle, sandbox specs, session auth, and sandbox-scoped secret lookup.
- `openhands/app_server/app_conversation`: sandboxed conversation lifecycle, message routing to agent-server, exports, hooks, profiles, and git change helpers.
- `openhands/app_server/services`: shared injectors for JWT, HTTP clients, and database sessions.
- `openhands/server/__main__.py`: deprecated compatibility entry point that still runs `openhands.server.listen:app`; prefer direct `uvicorn openhands.app_server.app:app` for new docs.

## Setup And Installation

Start with the repository conventions:

```bash
make install-pre-commit-hooks
```

If the whole app needs to be built, use:

```bash
make build
```

Backend dependencies are Poetry-managed. The repository Makefile selects Python `3.12` or `3.13`, installs Poetry dependencies, and installs pre-commit hooks. If Poetry is missing, install it before expecting Makefile install or lint targets to work.

For backend-only development, prefer the smallest command that prepares the needed environment rather than a full application build. Avoid broad dependency downloads unless the task requires runtime-level verification.

## Running The Backend

For a direct backend app server smoke run, use Uvicorn when dependencies are available:

```bash
poetry run uvicorn openhands.app_server.app:app --host 0.0.0.0 --port 3000
```

For the repository's full local app workflow, the documented command is:

```bash
export INSTALL_DOCKER=0
export RUNTIME=local
make build && make run FRONTEND_PORT=12000 FRONTEND_HOST=0.0.0.0 BACKEND_HOST=0.0.0.0
```

Sandbox-heavy flows may need Docker, tmux, Playwright browsers, or local runtime cleanup. Do not use a full run as a routine validation step for small route/model/test edits.

## Backend Change Workflow

1. Identify the owner module and the route/service/model boundary. For V1 API changes, start from `v1_router.py` and the specific router, then follow its `Depends(...)` services into `config.py` injectors.
2. Update Pydantic models and service contracts before changing router behavior. Keep request/response model names aligned with existing files.
3. Preserve dependency-injection seams. App-server routers usually depend on helpers such as `depends_user_context()`, `depends_sandbox_service()`, `depends_app_conversation_service()`, `depends_db_session()`, or `get_dependencies()`.
4. Add or update focused unit tests in the nearest `tests/unit` area. Many tests call route functions directly with mocks; route-level tests build small FastAPI apps and override dependencies.
5. Run the narrowest matching test first, then broaden to relevant files, and finish with backend pre-commit when available.

## Test Commands

Native unit-test patterns:

```bash
poetry run pytest ./tests/unit
poetry run pytest ./tests/unit/app_server/test_settings_api.py
poetry run pytest ./tests/unit/app_server/test_settings_api.py::test_store_settings_rejects_legacy_nested_payload_keys
poetry run pytest -v ./tests/unit/app_server/test_config_router.py
```

Useful focused targets by change type:

- Settings/schema/profile changes: `tests/unit/app_server/test_settings_api.py`, `tests/unit/app_server/test_profiles_api.py`, `tests/unit/app_server/test_settings_agent_kind_switch.py`, `tests/unit/storage/data_models/test_settings.py`, `tests/unit/storage/data_models/test_llm_profiles.py`.
- Secrets changes: `tests/unit/app_server/test_secrets_api.py`, `tests/unit/app_server/test_sandbox_secrets_router.py`, `tests/unit/storage/data_models/test_secret_store.py`.
- Sandbox lifecycle/spec changes: `tests/unit/app_server/test_sandbox_service.py`, `tests/unit/app_server/test_process_sandbox_service.py`, `tests/unit/app_server/test_docker_sandbox_service.py`, `tests/unit/app_server/test_docker_sandbox_spec_service_injector.py`, `tests/unit/app_server/test_dynamic_remote_sandbox_spec_service.py`.
- Conversation router/service changes: `tests/unit/app_server/test_app_conversation_router.py`, `tests/unit/app_server/test_app_conversation_service_base.py`, `tests/unit/app_server/test_sql_app_conversation_info_service.py`, `tests/unit/app_server/test_sql_app_conversation_start_task_service.py`, `tests/unit/app_server/test_live_status_app_conversation_service.py`, `tests/unit/app_server/test_send_message_endpoint.py`.
- Config/model-provider changes: `tests/unit/app_server/test_config_router.py`, `tests/unit/app_server/test_llm_model_service.py`, `tests/unit/utils/test_llm_utils.py`.
- Event/webhook changes: `tests/unit/app_server/test_event_router.py`, `tests/unit/app_server/test_webhook_router_*.py`, `tests/unit/app_server/test_sql_event_callback_service.py`.
- Env/config injector changes: `tests/unit/app_server/test_default_web_client_config_injector.py`, `tests/unit/app_server/test_agent_server_env_override.py`, `tests/unit/app_server/utils/test_env_var_validation.py`, `tests/unit/app_server/test_db_session_injector.py`.

Backend lint/pre-commit command:

```bash
pre-commit run --config ./dev_config/python/.pre-commit-config.yaml
```

The repository instructions require pre-commit hooks before making changes and backend pre-commit before pushing backend changes. If the environment cannot run these commands, record the exact missing tool or dependency.

## Schema And OpenAPI Workflows

Use schema/OpenAPI generation only when backend model/API changes require regenerated artifacts and full backend dependencies are installed.

The bundled diagnostic includes a non-mutating `AppServerConfig.model_json_schema()` sanity check adapted from the repo's config-schema dumper, so start there for import/schema readiness. From a copied skill tree, run the helper by path inside that copied skill:

```bash
python /path/to/openhands-skill/sub-skills/backend-development/scripts/check_backend_imports.py --repo-root .
```

The source tree also contains a config-schema dumper and an OpenAPI updater. Treat those as repository-owned workflows, not bundled skill runtime helpers. The OpenAPI updater imports the FastAPI app, sanitizes descriptions, preserves existing server entries, updates the API version, creates a backup, and rewrites the OpenAPI artifact; use it only when a task explicitly calls for regenerated API docs and the repository environment is ready.

## Safe Import Diagnostic

This sub-skill bundles a read-only import checker that avoids server startup:

```bash
python /path/to/openhands-skill/sub-skills/backend-development/scripts/check_backend_imports.py --repo-root .
```

Use it to distinguish missing dependencies from application bugs before deeper validation. It checks selected modules only and prints actionable dependency messages. It does not import the FastAPI app, start Uvicorn, contact Docker, or generate schemas.

## Pulling Related Validation Into A Handoff

When handing off backend work, include:

- Files changed and the backend area they belong to.
- Focused tests run, exact commands, and results.
- Whether backend pre-commit was run or why it could not run.
- Any schema/OpenAPI artifacts regenerated and the command used.
- Any optional services intentionally not exercised, such as Docker, remote sandbox, database, or external provider APIs.
