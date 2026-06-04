# Evaluation Troubleshooting

## `--eval-interval` Set But No Dataset

Add `--eval-prompt-data` or `--eval-config`.

## Odd Number Of `--eval-prompt-data` Values

The CLI form expects name/path pairs:

```bash
--eval-prompt-data name1 path1 name2 path2
```

## Reward Dicts

If the eval reward function returns dicts, set:

```bash
--eval-reward-key <key>
```
