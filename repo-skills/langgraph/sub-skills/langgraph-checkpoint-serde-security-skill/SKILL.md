---
name: langgraph-checkpoint-serde-security-skill
description: "Use when a user wants LangGraph checkpoint serialization, JsonPlusSerializer, strict msgpack, allowed modules, pickle fallback, encrypted serializers, checkpoint migration, or persistence security troubleshooting."
disable-model-invocation: true
---

# LangGraph Checkpoint Serde Security

Use `langgraph-checkpoint-serde-security-skill` for checkpoint serialization and security boundaries. Quick answer: avoid pickle fallback for untrusted data, use strict/allowlisted serializers, treat checkpoint stores as trusted unless configured otherwise, and run [scripts/check_checkpoint_serde_security.py](scripts/check_checkpoint_serde_security.py).

## Short Workflow

1. Identify the checkpoint backend and serializer.
2. For untrusted checkpoint data, avoid pickle fallback and use allowlists.
3. Inspect environment and serializer imports with the bundled script.
4. For encrypted checkpoints, verify key management separately before production use.
5. During migrations, test resume/state-history behavior on representative checkpoints.
6. Read [references/serde-security.md](references/serde-security.md) before loading old or external checkpoints.

## Bundled Scripts

- [scripts/check_checkpoint_serde_security.py](scripts/check_checkpoint_serde_security.py): import-checks serializer classes and reports strict/allowlist environment posture.
- [scripts/inspect_checkpoint_serde_apis.py](scripts/inspect_checkpoint_serde_apis.py): signature inspection for serializer classes.

## References

- [references/serde-security.md](references/serde-security.md): strict msgpack, allowed modules, pickle fallback, and encryption guidance.
- [references/checkpoint-migration.md](references/checkpoint-migration.md): migration and compatibility notes.
- [references/troubleshooting.md](references/troubleshooting.md): unsafe deserialization, missing cryptography, and migration failures.

## Boundaries

Use persistence backends for SQLite/Postgres saver setup. Use this skill when serializer safety, checkpoint trust, or migration compatibility is the main task.
