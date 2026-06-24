# Deployment Config Troubleshooting

- Graph import fails in server: import spec path or dependency path is wrong.
- Build succeeds but run fails: graph module imports optional packages not in dependencies.
- Local works, container fails: missing shared monorepo package or relative path assumption.
- Secrets missing: deployment environment does not include required env vars.
- Import hangs: graph module does work at import time; move work into nodes/startup code.
- Docker build slow: avoid model downloads at image build unless intentionally pinned.
