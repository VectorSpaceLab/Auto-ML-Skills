# Observability Troubleshooting

- No LangSmith traces: check tracing env vars, project name, network, and package version.
- Callback not firing: pass it through `config={"callbacks": [...]}` to the runnable being invoked.
- Secret leak risk: scrub inputs/outputs or disable tracing for sensitive runs.
- Nested chain hard to debug: use tags/run names at meaningful sub-chain boundaries.
- Too many traces: scope tracing to the target run or use project-level organization.
