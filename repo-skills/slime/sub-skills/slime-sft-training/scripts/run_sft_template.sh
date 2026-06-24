#!/usr/bin/env bash
# Single-node SFT-style slime training template.
set -euo pipefail

: "${SLIME_SKILL_DIR:?Set SLIME_SKILL_DIR to the root slime skill directory}"
: "${MEGATRON_PATH:?Set MEGATRON_PATH to a full Megatron-LM checkout}"
: "${HF_CHECKPOINT:?Set HF_CHECKPOINT to a local HF checkpoint}"
: "${REF_LOAD:?Set REF_LOAD to a Megatron torch_dist checkpoint root}"
: "${PROMPT_DATA:?Set PROMPT_DATA to SFT data}"
: "${SAVE_DIR:?Set SAVE_DIR to the output checkpoint root}"
: "${MODEL_RECIPE:=qwen3-0.6b}"
: "${NUM_GPUS:=8}"

export SLIME_RUNNER="${SLIME_SKILL_DIR}/scripts/run_slime_train_async.py"
MODEL_ARGS=( $(python "${SLIME_SKILL_DIR}/scripts/inspect_model_recipe.py" "${MODEL_RECIPE}") )

bash "${SLIME_SKILL_DIR}/scripts/launch_ray_job_template.sh" \
  --actor-num-nodes 1 \
  --actor-num-gpus-per-node "${NUM_GPUS}" \
  "${MODEL_ARGS[@]}" \
  --hf-checkpoint "${HF_CHECKPOINT}" \
  --ref-load "${REF_LOAD}" \
  --load "${SAVE_DIR}" \
  --save "${SAVE_DIR}" \
  --save-interval 100 \
  --rollout-function-path slime.rollout.sft_rollout.generate_rollout \
  --prompt-data "${PROMPT_DATA}" \
  --input-key "${INPUT_KEY:-messages}" \
  --num-epoch "${NUM_EPOCH:-1}" \
  --rollout-batch-size "${ROLLOUT_BATCH_SIZE:-4}" \
  --global-batch-size "${GLOBAL_BATCH_SIZE:-4}" \
  --loss-type sft_loss \
  --calculate-per-token-loss \
  --disable-compute-advantages-and-returns \
  --debug-train-only \
  --optimizer adam \
  --lr "${LR:-1e-5}" \
  --lr-decay-style cosine \
  --min-lr "${MIN_LR:-1e-6}" \
  --lr-warmup-fraction 0.1 \
  --weight-decay 0.1 \
  --tensor-model-parallel-size 1 \
  --pipeline-model-parallel-size 1 \
  --context-parallel-size 1 \
  --expert-model-parallel-size 1 \
  --expert-tensor-parallel-size 1 \
  --use-dynamic-batch-size \
  --max-tokens-per-gpu "${MAX_TOKENS_PER_GPU:-2048}"
