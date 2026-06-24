# Workflows

## Local Dev Server

1. Install `langgraph-cli[inmem]`.
2. Ensure the graph module can be imported directly.
3. Create `langgraph.json`.
4. Run `python scripts/validate_langgraph_json.py path/to/langgraph.json`.
5. Start `langgraph dev --config path/to/langgraph.json --no-browser`.
6. Watch the terminal for import errors and dependency resolution failures.

## Studio

Use the local dev server and open the Studio URL or platform-provided UI. Keep graph names stable so traces and saved runs remain meaningful.

## Docker Build

1. Make dependencies explicit.
2. Avoid depending on editable local paths unless the project is copied into the image.
3. Generate or build with the CLI.
4. Test the image locally before hosted deployment.

## Hosted Deployment Prep

1. Separate public code from secrets.
2. Put required env vars in the platform's secret manager or a local `.env` only for local dev.
3. Include checkpointer/storage configuration intentionally.
4. Add a no-key graph smoke path when possible.
