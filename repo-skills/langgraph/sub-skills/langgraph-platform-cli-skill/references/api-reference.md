# API Reference

## CLI Commands

```bash
langgraph new PATH --template TEMPLATE_NAME
langgraph dev --config langgraph.json --host 127.0.0.1 --port 2024 --no-browser
langgraph up --config langgraph.json --port 8123 --wait
langgraph build -t IMAGE_TAG --config langgraph.json
langgraph dockerfile Dockerfile --config langgraph.json
```

## langgraph.json

Minimal shape:

```json
{
  "dependencies": ["."],
  "graphs": {
    "agent": "./src/agent.py:graph"
  },
  "env": ".env",
  "python_version": "3.11"
}
```

Important fields:

- `dependencies`: packages or local project paths required by the graph.
- `graphs`: mapping from public graph name to import spec.
- `env`: optional env file.
- `python_version`: runtime Python version.
- `dockerfile_lines`: optional extra Dockerfile commands.

The graph export should be importable without running long jobs or requiring interactive prompts.
