# Python AI API Services and Deployment

## When To Read

Python AI packages exposed as APIs, FastAPI services, OpenAI-compatible endpoints, MCP servers, secured services, custom routes, clusters, consoles, Docker/cloud/serverless deployment, or observability targets.

## Repo Skill Options

<!-- DISCO_SCENARIO:python-ai-api-services-and-deployment:START -->
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

Use this scenario when serving an AI application API is primary; use model-serving or gateway scenarios when the request is about model backends or provider routing. Route WebUI service exposure through launch-and-config first, then api-automation for request construction and endpoint troubleshooting. Choose `txtai` when the user wants a running service or configured Application; use sibling sub-skills for the underlying embeddings, workflow, RAG, or agent behavior.
