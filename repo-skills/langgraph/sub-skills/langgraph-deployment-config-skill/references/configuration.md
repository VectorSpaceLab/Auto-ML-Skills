# Deployment Configuration Reference

## langgraph.json Fields

Common fields:

- `dependencies`: local paths or packages required by graphs.
- `graphs`: map graph names to import specs such as `./src/agent.py:graph`.
- `env`: optional env file path.
- `python_version`: runtime Python version.
- `dockerfile_lines`: optional extra image build commands.

## Hardening Checklist

- Dependencies are explicit and reproducible.
- Graph imports do not start servers, call providers, download models, or prompt users.
- Secrets are not embedded in config.
- Env files are not accidentally published.
- Python version matches package constraints.
- Monorepo paths include shared libs required at import time.
