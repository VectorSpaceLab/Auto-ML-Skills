# Evaluation Configuration

## CLI Pair Form

```bash
--eval-interval 5
--eval-prompt-data aime /data/aime.jsonl
--n-samples-per-eval-prompt 16
--eval-max-response-len 2048
--eval-top-p 1
```

## YAML Form

```yaml
eval:
  defaults:
    n_samples_per_eval_prompt: 1
    temperature: 0.7
    top_p: 1.0
  datasets:
    - name: aime
      path: /data/aime.jsonl
      rm_type: math
      input_key: prompt
      label_key: label
    - name: ifbench
      path: /data/ifbench.jsonl
      rm_type: ifbench
```

Launch with:

```bash
--eval-config eval.yaml
```

Dataset-level values override defaults, which override CLI fallback fields.

## Custom Eval Function

```bash
--eval-function-path my_project.eval.generate_rollout
```

Signature matches full rollout:

```python
def generate_rollout(args, rollout_id, data_source, evaluation=False):
    ...
```
