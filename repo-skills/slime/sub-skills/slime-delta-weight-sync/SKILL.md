---
name: slime-delta-weight-sync
description: "Configures slime delta weight synchronization for non-colocated training and rollout, including disk or NCCL transport and encoding choices."
disable-model-invocation: true
---

# slime Delta Weight Sync

Use this sub-skill when the user wants to reduce non-colocated weight-sync bandwidth by sending only changed positions and values.

## Short Workflow

1. Confirm the job is not colocated. Delta sync is rejected with `--colocate`.
2. Choose transport:
   - `disk` for shared filesystem / bandwidth-constrained trainer-to-rollout links.
   - `nccl` for intra-datacenter validation or direct broadcast.
3. Choose encoding:
   - `indices`: lowest compute, largest payload.
   - `deltas`: gap-encoded positions.
   - `deltas_zstd`: smallest disk payload, more compute.
4. For disk transport, set a shared `--update-weight-delta-dir`.

Read [references/configuration.md](references/configuration.md) for args and tradeoffs. Read [references/troubleshooting.md](references/troubleshooting.md) when validation or cleanup fails.

## Scripts

- Adapt [scripts/delta_disk_args.sh](scripts/delta_disk_args.sh) or [scripts/delta_nccl_args.sh](scripts/delta_nccl_args.sh).

## Constraints

- Do not use with `--colocate`.
- Disk path must be writable by trainer and readable by rollout engines.
- Keep files only for debugging; otherwise cleanup is expected after engine acknowledgement.
