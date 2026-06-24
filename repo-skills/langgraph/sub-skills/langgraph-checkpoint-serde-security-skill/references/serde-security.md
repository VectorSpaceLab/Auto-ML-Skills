# Checkpoint Serde Security

## Trust Boundary

Checkpoint data can contain serialized Python-adjacent objects depending on serializer and configuration. Treat checkpoint stores as trusted inputs unless you have configured strict serializers and allowlists.

## JsonPlusSerializer

```python
from langgraph.checkpoint.serde.jsonplus import JsonPlusSerializer

serde = JsonPlusSerializer(
    pickle_fallback=False,
    allowed_json_modules=None,
    allowed_msgpack_modules=None,
)
```

Avoid `pickle_fallback=True` for untrusted checkpoints.

## Strict Msgpack And Allowlists

Use strict mode and module allowlists when reading checkpoints from less-trusted stores. Exact environment variable names and defaults can change; inspect the installed package and deployment configuration.

## Encrypted Serializer

`EncryptedSerializer` is importable in current packages, but production use needs key management, rotation, and operational recovery planning. Do not treat import success as a full security validation.

## Operational Rules

- Do not share checkpoint databases across trust boundaries.
- Keep serializer config versioned with deployments.
- Test resume after serializer or package upgrades.
- Keep backups before migration.
