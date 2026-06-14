# Checkpoint Migration

## Migration Risks

LangGraph checkpoint internals can evolve across versions. User-visible risks include:

- resume failing from old checkpoints
- interrupt payload shape changes
- pending writes or task metadata changes
- channel/value migration issues

## Safe Migration Workflow

1. Record current package versions and serializer config.
2. Back up checkpoint stores.
3. Test a small set of representative threads.
4. Verify `get_state`, `get_state_history`, resume with `Command(resume=...)`, and new invocations.
5. Roll out with monitoring and rollback plan.

## When To Rebuild

If old checkpoints are not needed for resume or audit, it may be simpler to start new thread ids after a major graph/schema migration.
