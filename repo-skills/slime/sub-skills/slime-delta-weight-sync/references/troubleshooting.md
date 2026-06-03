# Delta Weight Sync Troubleshooting

## Rejected With Colocate

Delta sync has no bandwidth benefit under colocate because colocated weight sync uses CUDA IPC handles. Remove `--colocate` or use full sync.

## Disk Files Missing

Check `--update-weight-delta-dir` is shared across trainer and every rollout engine. Local-only paths fail in multi-node runs.

## Debugging Delta Files

Temporarily add:

```bash
--update-weight-delta-keep-files
```

Remove it for production so old sync directories do not fill storage.
