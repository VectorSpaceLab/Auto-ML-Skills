# Delta Weight Sync Configuration

## Disk Transport

```bash
--update-weight-mode delta
--update-weight-transport disk
--update-weight-encoding deltas_zstd
--update-weight-delta-dir /shared/fs/delta-updates
```

Use disk when trainer and rollout communicate through a shared filesystem or the network link is bandwidth constrained.

## NCCL Transport

```bash
--update-weight-mode delta
--update-weight-transport nccl
--update-weight-encoding indices
```

Use NCCL when comparing delta wire format against full sync inside one fast network domain.

## Receiver Chunk Cap

```bash
--sglang-update-weight-delta-chunk-bytes 2147483648
```

Tune this when SGLang `load_weights` calls become too large.

## Encoding Choice

- `indices`: int32 absolute positions, largest payload, lowest compute.
- `deltas`: smaller position stream via gaps.
- `deltas_zstd`: compresses delta stream, best for bandwidth-limited disk paths.
