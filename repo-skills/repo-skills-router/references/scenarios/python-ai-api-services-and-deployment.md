# Python AI API Services and Deployment

## When To Read

Python AI packages exposed as APIs, FastAPI services, OpenAI-compatible endpoints, MCP servers, secured services, custom routes, clusters, consoles, Docker/cloud/serverless deployment, or observability targets.

## Repo Skill Options

<!-- DISCO_SCENARIO:python-ai-api-services-and-deployment:START -->
### `khoj`

Role: Khoj provides concrete FastAPI/Django deployment, REST API, model-provider, database, auth, and Docker guidance for the Khoj AI app.
Read when: Tasks mention self-hosting Khoj, khoj CLI, FastAPI/Django routes, docker-compose for Khoj, PostgreSQL/embedded DB setup, KHOJ_DOMAIN, KHOJ_ALLOWED_DOMAIN, KHOJ_NO_HTTPS, KHOJ_ADMIN_EMAIL, model provider base URLs, or Khoj API route behavior.
Best for: Deploying or debugging Khoj as an AI API service, mapping Khoj REST endpoints, configuring auth/admin/model providers, and understanding server startup side effects.
Avoid when: Use a generic FastAPI/Django deployment skill when the service is not Khoj and does not share Khoj-specific CLI, route, model-provider, content, search, chat, automation, or memory behavior.
Useful entry points: `khoj/SKILL.md`, `khoj/sub-skills/deployment-api/SKILL.md`, `khoj/sub-skills/development/SKILL.md`.

### `kotaemon`

Role: Kotaemon covers deployment and configuration of the Kotaemon Gradio document-QA app and its model/resource settings.
Read when: The task mentions `python app.py`, Kotaemon Docker images, Gradio server variables, `.env`, `flowsettings.py`, app data, PDF.js, local Ollama or llama-cpp server setup for the app, first setup/login, or Chroma migration preflight.
Best for: Safe app configuration diagnostics, Docker/local setup guidance, PDF viewer setup, local provider URL checks, update/migration caution, and operator troubleshooting for Kotaemon deployments.
Avoid when: Avoid for deploying unrelated FastAPI/Gradio apps or generic model servers unless they are being configured as Kotaemon providers.
Useful entry points: `kotaemon/sub-skills/app-deployment/SKILL.md`, `kotaemon/sub-skills/model-providers/SKILL.md`.

### `langflow`

Role: Use `langflow` for Langflow's FastAPI backend, auth/authz, database migrations, Docker/Compose, environment variables, observability, and production operations.
Read when: The task mentions `langflow run`, FastAPI routes under `/api/v1`, Langflow OpenAI-compatible responses, MCP server/client, auth or authorization guards, shares/audit, migrations, PostgreSQL, Docker Compose, Langflow env vars, API keys, storage, workers, or deployment logs.
Best for: Backend route/service changes, guarded resources, database and migration work, Langflow server configuration, Docker/Compose setup, operational troubleshooting, and custom Langflow images.
Avoid when: Use `langflow`'s workflow scenario entry for flow-authoring-only tasks; use a generic FastAPI or deployment skill when Langflow APIs, settings, services, or images are not involved.
Useful entry points: `langflow/SKILL.md`, `langflow/sub-skills/backend-runtime/SKILL.md`, `langflow/sub-skills/deployment-and-operations/SKILL.md`, `langflow/sub-skills/frontend-development/SKILL.md`.

### `ragflow`

Role: RAGFlow skill for Quart/Peewee backend APIs, public REST and OpenAI-compatible endpoints, Docker/source/Helm configuration, and service health debugging.
Read when: Tasks mention RAGFlow deployment, Docker Compose, service_conf.yaml, DOC_ENGINE, /api/v1, /v1, Quart routes, API keys, OpenAI-compatible endpoints, healthz, MySQL, Redis, MinIO, Elasticsearch, Infinity, OpenSearch, or OceanBase.
Best for: Debugging RAGFlow service startup, route prefixes, auth/API-token behavior, backend service layers, SDK/HTTP integrations, and deployment config mismatches.
Avoid when: Use a generic FastAPI/Flask skill or infrastructure skill when RAGFlow code, APIs, or config keys are not involved.
Useful entry points: `ragflow/SKILL.md`, `ragflow/sub-skills/deployment-configuration/SKILL.md`, `ragflow/sub-skills/backend-api-services/SKILL.md`, `ragflow/sub-skills/sdk-http-integration/SKILL.md`.

### `stable-diffusion-webui`

Role: Covers WebUI-specific API service launch, authentication, CORS/TLS/subpath flags, /sdapi route behavior, and server lifecycle hazards.
Read when: User asks about --api, --nowebui, --api-auth, --listen, --subpath, CORS, TLS, /sdapi/v1 routes, WebUI API payloads, API errors, or server-stop/restart endpoints.
Best for: WebUI API deployment and automation tasks where WebUI-specific flags and /sdapi schemas matter more than generic FastAPI patterns.
Avoid when: Use generic FastAPI/deployment skills for non-WebUI services or AI gateway skills for provider routing/proxy infrastructure.
Useful entry points: `stable-diffusion-webui/sub-skills/launch-and-config/SKILL.md`, `stable-diffusion-webui/sub-skills/api-automation/SKILL.md`.

### `txtai`

Role: Provides txtai Application configuration, route activation, safe writable/reindex boundaries, auth, deployment, and console guidance.
Read when: txtai Application, CONFIG=app.yml, uvicorn txtai.api:app, OpenAI-compatible API, /v1/chat/completions, MCP, TOKEN, writable, reindex, Docker, cloud, console --help.
Best for: Creating service YAML, validating route families, starting Uvicorn, securing writable indexes, deploying containers/cloud patterns, and diagnosing console/API issues.
Avoid when: The task only asks for local embeddings query syntax or deterministic workflow internals without service deployment.
Useful entry points: `txtai/SKILL.md`, `txtai/sub-skills/api-and-deployment/SKILL.md`.

<!-- DISCO_SCENARIO:python-ai-api-services-and-deployment:END -->

## How To Choose

Use this scenario when serving an AI application API is primary; use model-serving or gateway scenarios when the request is about model backends or provider routing. Choose khoj for deployment/API tasks that include Khoj-specific environment variables, CLI behavior, route families, admin setup, model-provider setup, or startup errors. Choose kotaemon when deployment questions name Kotaemon/ktem or include its app config signals such as `KH_*`, `GRADIO_*`, File Index, Resources tab, PDF.js, or local RAG provider setup. Choose `langflow` when the Python AI service or deployment task is specifically a Langflow server, API, auth/authz, database, Docker, Compose, or frontend/backend contract issue. Choose ragflow for RAGFlow API route, deployment, health-check, auth, service-config, or SDK/HTTP tasks; route inside the skill by whether the user is deploying, changing backend code, or calling the public API. Route WebUI service exposure through launch-and-config first, then api-automation for request construction and endpoint troubleshooting. Choose `txtai` when the user wants a running service or configured Application; use sibling sub-skills for the underlying embeddings, workflow, RAG, or agent behavior.
