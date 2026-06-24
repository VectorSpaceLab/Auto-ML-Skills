---
name: langgraph-deployment-config-skill
description: "Use when a user wants LangGraph deployment configuration, langgraph.json hardening, Dockerfile/build config, environment variables, dependency packaging, monorepos, or deployment troubleshooting."
disable-model-invocation: true
---

# LangGraph Deployment Config

Use `langgraph-deployment-config-skill` for hardening deployment inputs after Platform/CLI basics are understood. Quick answer: validate `langgraph.json`, pin dependencies, separate secrets into env files or deployment secret stores, ensure graph specs import quickly, and run `scripts/audit_deployment_config.py`.

## Short Workflow

1. Start from Platform/CLI skill for basic `langgraph dev`, `up`, `build`, and `dockerfile` commands.
2. Audit `langgraph.json` for dependencies, graph import specs, env handling, Python version, and Dockerfile lines.
3. Ensure graph modules export compiled graphs or expected graph objects without interactive prompts or long jobs at import time.
4. Keep secrets out of `langgraph.json`; reference env files or deployment secret mechanisms.
5. Run [scripts/audit_deployment_config.py](scripts/audit_deployment_config.py).

## Bundled Scripts

- [scripts/audit_deployment_config.py](scripts/audit_deployment_config.py): static no-network audit for `langgraph.json` deployment risks.

## References

- [references/configuration.md](references/configuration.md): deployment config fields and hardening checklist.
- [references/workflows.md](references/workflows.md): local-to-container-to-hosted preparation.
- [references/troubleshooting.md](references/troubleshooting.md): dependency, import, env, Docker, and monorepo failures.

## Boundaries

Use `langgraph-platform-cli-skill` for command syntax and local server operation. Use this skill for productionizing config and packaging.
