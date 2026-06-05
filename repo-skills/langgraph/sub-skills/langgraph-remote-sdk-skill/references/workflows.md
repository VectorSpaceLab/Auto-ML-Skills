# Remote SDK Workflows

## Local Server Client

1. Start a local server using Platform/CLI skill.
2. Create SDK client with local base URL.
3. Create or reuse a thread.
4. Invoke the graph/assistant.
5. Stream events if the UI needs incremental updates.

## Hosted Deployment Client

1. Confirm deployment URL and auth token.
2. Confirm graph/assistant id.
3. Avoid logging request bodies that contain secrets or user data.
4. Capture run ids for support/debugging.

## Streaming

Choose stream modes that match the UI: values/updates for state, messages for token streams, events for detailed run telemetry.
