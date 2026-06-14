# Deployment Config Workflows

## Local To Container

1. Validate `langgraph.json` with Platform/CLI validator.
2. Audit dependencies and graph specs.
3. Run local dev server.
4. Build Docker image or Dockerfile.
5. Smoke import graph inside the image before running production traffic.

## Monorepo

1. Include app and shared package paths in dependencies.
2. Avoid relative imports that only work from a developer shell.
3. Add package metadata for shared libs when possible.
4. Validate graph import specs from a clean working directory.

## Secrets

Keep API keys in env/secrets. Never put provider keys in `langgraph.json`, source code examples, traces, or graph state dumps.
