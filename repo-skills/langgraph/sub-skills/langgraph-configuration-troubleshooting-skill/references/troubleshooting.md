# Cross-Cutting Troubleshooting

## Install

Run the root import check. Install only the optional package needed for the failing import.

## Build

Check node names, edge directions, reducer annotations, conditional route labels, and compile timing.

## Runtime

Check input state shape, missing context, missing `thread_id`, unexpected reducer behavior, and side effects around interrupts.

## Tools

Check tool schemas, message key, tool-call IDs, model tool-calling support, and `handle_tool_errors`.

## Streams

Check stream mode, sync versus async consumption, subgraph namespace settings, and whether the graph actually emits model messages.

## CLI

Check `langgraph.json`, graph importability, dependency list, env file path, and Python version.
