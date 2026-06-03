# OPD Troubleshooting

## `--opd-type` Missing

When `--use-opd` is set, choose:

```bash
--opd-type sglang
```

or:

```bash
--opd-type megatron
```

## Teacher Load Wrong Mode

`--opd-teacher-load` is required for `--opd-type megatron` and should not be set for `--opd-type sglang`.

## Teacher Service Timeout

For SGLang teacher mode, confirm the URL is reachable from Ray worker processes, not only from the submitting shell.
