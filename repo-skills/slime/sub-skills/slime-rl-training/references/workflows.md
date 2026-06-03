# RL Training Workflows

## Standard Single-Node GRPO Skeleton

```bash
export NUM_GPUS=8
export MASTER_ADDR=127.0.0.1
export MEGATRON_PATH=/path/to/Megatron-LM
export SLIME_RUNNER=/path/to/skill/slime/scripts/run_slime_train.py

MODEL_ARGS=( $(python /path/to/skill/slime/scripts/inspect_model_recipe.py qwen3-0.6b) )

CKPT_ARGS=(
  --hf-checkpoint /models/Qwen3-0.6B
  --ref-load /models/Qwen3-0.6B_torch_dist
  --load /runs/qwen3-0.6b-slime
  --save /runs/qwen3-0.6b-slime
  --save-interval 20
)

ROLLOUT_ARGS=(
  --prompt-data /data/train.jsonl
  --input-key prompt
  --label-key label
  --apply-chat-template
  --rollout-shuffle
  --rm-type deepscaler
  --num-rollout 10
  --rollout-batch-size 4
  --n-samples-per-prompt 2
  --num-steps-per-rollout 1
  --global-batch-size 8
  --rollout-max-response-len 512
  --rollout-temperature 1
)

PERF_ARGS=(
  --tensor-model-parallel-size 1
  --pipeline-model-parallel-size 1
  --context-parallel-size 1
  --expert-model-parallel-size 1
  --expert-tensor-parallel-size 1
  --use-dynamic-batch-size
  --max-tokens-per-gpu 2048
)

GRPO_ARGS=(
  --advantage-estimator grpo
  --use-kl-loss
  --kl-loss-coef 0.00
  --kl-loss-type low_var_kl
  --entropy-coef 0.00
  --eps-clip 0.2
  --eps-clip-high 0.28
)

OPTIMIZER_ARGS=(
  --optimizer adam
  --lr 1e-6
  --lr-decay-style constant
  --weight-decay 0.1
  --adam-beta1 0.9
  --adam-beta2 0.98
)

SGLANG_ARGS=(
  --rollout-num-gpus-per-engine 1
  --sglang-mem-fraction-static 0.6
)

bash /path/to/skill/slime/scripts/launch_ray_job_template.sh \
  --actor-num-nodes 1 \
  --actor-num-gpus-per-node "${NUM_GPUS}" \
  --colocate \
  "${MODEL_ARGS[@]}" \
  "${CKPT_ARGS[@]}" \
  "${ROLLOUT_ARGS[@]}" \
  "${OPTIMIZER_ARGS[@]}" \
  "${GRPO_ARGS[@]}" \
  "${PERF_ARGS[@]}" \
  "${SGLANG_ARGS[@]}"
```

## Eval Add-On

```bash
EVAL_ARGS=(
  --eval-interval 5
  --eval-prompt-data aime /data/aime.jsonl
  --n-samples-per-eval-prompt 4
  --eval-max-response-len 2048
  --eval-top-p 1
)
```

Add `"${EVAL_ARGS[@]}"` to the job. For multiple datasets with different scoring, route to `slime-evaluation`.
