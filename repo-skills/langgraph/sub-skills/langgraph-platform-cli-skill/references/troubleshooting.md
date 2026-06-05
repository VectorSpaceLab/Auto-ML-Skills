# Platform CLI Troubleshooting

- `langgraph` command missing: install `langgraph-cli` or `langgraph-cli[inmem]`.
- Graph import fails: run `python -c "from module import graph"` from the project root.
- Bad graph spec: use `path.py:variable` or an importable module path with an exported graph object.
- Dependency missing in dev server: add it to `dependencies` or install it in the environment.
- Provider key missing: local server can start, but real model calls fail until env vars are set.
- Docker build misses local code: include the package path in dependencies and project packaging.
