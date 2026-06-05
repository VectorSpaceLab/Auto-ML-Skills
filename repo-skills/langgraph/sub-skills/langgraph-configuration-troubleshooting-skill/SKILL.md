---
name: langgraph-configuration-troubleshooting-skill
description: "Use when a user wants LangGraph installation, dependency, configuration, integration, migration, version, common error, package import, or troubleshooting help across graph, checkpoint, prebuilt, streaming, CLI, and deployment workflows."
disable-model-invocation: true
---

# LangGraph Configuration Troubleshooting

Use this sub-skill for cross-cutting setup, integration, migration, and debugging tasks that do not belong to one workflow family.

## Short Workflow

1. Run `../../scripts/check_langgraph_env.py`.
2. Inspect signatures with `../../scripts/inspect_langgraph_api.py --summary` if version drift is suspected.
3. Identify whether the failure is import/install, graph build, runtime config, checkpoint, prebuilt tools, streaming, or CLI.
4. Read [references/troubleshooting.md](references/troubleshooting.md) and the matching root reference.
5. Run [scripts/check_common_pitfalls.py](scripts/check_common_pitfalls.py) on user files when available.
6. Route to a more specific sub-skill after the failing surface is clear.

## References

- [references/troubleshooting.md](references/troubleshooting.md): cross-cutting issue taxonomy and fixes.
- [references/configuration.md](references/configuration.md): dependency, integration, deprecation, and migration notes.

## Bundled Scripts

- [scripts/check_common_pitfalls.py](scripts/check_common_pitfalls.py): static checker for common LangGraph mistakes in Python and JSON files.

## Boundaries

This sub-skill diagnoses and routes. Use the focused sub-skill for implementing substantial graph, agent, checkpoint, streaming, subgraph, or CLI changes.
