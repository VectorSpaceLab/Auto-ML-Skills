# Remote SDK Troubleshooting

- Import fails: install `langgraph-sdk` or the package that includes it.
- 404 graph/assistant: verify graph id and deployed config.
- Unauthorized: check token presence without printing it.
- Server not reachable: verify local server process, host, port, and firewall.
- Stream hangs: check stream mode, server logs, and graph interrupt/checkpoint state.
- Version mismatch: compare SDK and server package versions.
