# RL Training Configuration

## Key Argument Blocks

Checkpoint:

```bash
--hf-checkpoint /path/to/hf
--ref-load /path/to/torch_dist
--load /path/to/run_ckpt
--save /path/to/run_ckpt
--save-interval 20
```

Rollout:

```bash
--prompt-data /path/to/train.jsonl
--input-key prompt
--label-key label
--apply-chat-template
--rm-type deepscaler
--num-rollout 100
--rollout-batch-size 16
--n-samples-per-prompt 8
--rollout-max-response-len 8192
```

Algorithm:

```bash
--advantage-estimator grpo
--use-kl-loss
--kl-loss-coef 0.0
--kl-loss-type low_var_kl
--eps-clip 0.2
--eps-clip-high 0.28
```

Performance:

```bash
--use-dynamic-batch-size
--max-tokens-per-gpu 4096
--balance-data
```

## Batch Constraint

For one train step per rollout:

```text
global_batch_size = rollout_batch_size * n_samples_per_prompt
```

More generally:

```text
rollout_batch_size * n_samples_per_prompt = global_batch_size * num_steps_per_rollout
```

If `--num-steps-per-rollout` is set and `--global-batch-size` is omitted, slime can infer global batch size.

## Reward Choices

Built-in `--rm-type` choices documented by slime include math-style and task reward functions such as `math`, `dapo`, `deepscaler`, `f1`, `gpqa`, `ifbench`, and `remote_rm`.

For custom reward logic, route to `slime-custom-rollout`.
