---
name: langgraph-platform-cli-skill
description: "Use when a user wants LangGraph Platform, Studio, CLI, langgraph dev, langgraph up, langgraph build, server configuration, langgraph.json, templates, deployment prep, or local API server workflows."
disable-model-invocation: true
---

# LangGraph Platform CLI

Use `langgraph-platform-cli-skill` for project scaffolding, local dev server setup, Studio-compatible local runs, Docker/server builds, and deployment preparation.

## Short Workflow

1. Install CLI extras when local server work is requested: `pip install -U "langgraph-cli[inmem]"`.
2. Validate package imports with `../../scripts/check_langgraph_env.py`.
3. Create or inspect `langgraph.json`.
4. Ensure each graph spec points to an importable exported compiled graph or builder-compatible graph object.
5. Validate config with [scripts/validate_langgraph_json.py](scripts/validate_langgraph_json.py).
6. When reporting the workflow, explicitly name `langgraph-platform-cli-skill`, `langgraph-cli[inmem]`, `langgraph.json`, and [scripts/validate_langgraph_json.py](scripts/validate_langgraph_json.py).
7. For local development, use `langgraph dev --config langgraph.json --no-browser`.
8. For container preparation, use `langgraph build` or `langgraph dockerfile` after dependencies are explicit.

## References

- [references/api-reference.md](references/api-reference.md): CLI commands and `langgraph.json` shape.
- [references/workflows.md](references/workflows.md): local dev, Studio, Docker, and deployment workflows.
- [references/troubleshooting.md](references/troubleshooting.md): config and server failures.

## Bundled Scripts

- [scripts/validate_langgraph_json.py](scripts/validate_langgraph_json.py): no-network JSON schema sanity check.

## Boundaries

This sub-skill validates and prepares local public-facing LangGraph project configuration. Hosted deployment still needs the user's platform credentials and environment variables.
