# Store Runtime Troubleshooting

- Memory not found: check namespace tuple and key.
- Data leaked between users: include tenant/user scopes in namespace.
- Store confused with checkpoint: checkpoint resumes thread state; store persists cross-thread memory.
- Tool schema exposes internal args: use injected state/store patterns in prebuilt tools.
- Runtime context missing: verify config/context keys and installed API signatures.
- Store backend missing: install optional store/checkpoint package if using SQLite/Postgres store modules.
