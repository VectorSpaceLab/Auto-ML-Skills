#!/usr/bin/env bash
# Single-node GRPO-style slime training template.
set -euo pipefail

: "${SLIME_SKILL_DIR:?Set SLIME_SKILL_DIR to the root slime skill directory}"
: "${MEGATRON_PATH:?Set MEGATRON_PATH to a full Megatron-LM checkout}"
: "${HF_CHECKPOINT:?Set HF_CHECKPOINT to a local HF checkpoint}"
: "${REF_LOAD:?Set REF_LOAD to a Megatron torch_dist checkpoint root}"
: "${PROMPT_DATA:?Set PROMPT_DATA to JSONL training data}"
: "${SAVE_DIR:?Set SAVE_DIR to the output checkpoint root}"
: "${MODEL_RECIPE:=qwen3-0.6b}"
: "${NUM_GPUS:=8}"

export SLIME_RUNNER="${SLIME_SKILL_DIR}/scripts/run_slime_train.py"
MODEL_ARGS=( $(python "${SLIME_SKILL_DIR}/scripts/inspect_model_recipe.py" "${MODEL_RECIPE}") )

bash "${SLIME_SKILL_DIR}/scripts/launch_ray_job_template.sh" \
  --actor-num-nodes 1 \
  --actor-num-gpus-per-node "${NUM_GPUS}" \
  --colocate \
  "${MODEL_ARGS[@]}" \
  --hf-checkpoint "${HF_CHECKPOINT}" \
  --ref-load "${REF_LOAD}" \
  --load "${SAVE_DIR}" \
  --save "${SAVE_DIR}" \
  --save-interval 20 \
  --prompt-data "${PROMPT_DATA}" \
  --input-key prompt \
  --label-key label \
  --apply-chat-template \
  --rollout-shuffle \
  --rm-type deepscaler \
  --num-rollout "${NUM_ROLLOUT:-1}" \
  --rollout-batch-size "${ROLLOUT_BATCH_SIZE:-2}" \
  --n-samples-per-prompt "${N_SAMPLES_PER_PROMPT:-2}" \
  --num-steps-per-rollout 1 \
  --global-batch-size "${GLOBAL_BATCH_SIZE:-4}" \
  --rollout-max-response-len "${ROLLOUT_MAX_RESPONSE_LEN:-256}" \
  --rollout-temperature 1 \
  --advantage-estimator grpo \
  --use-kl-loss \
  --kl-loss-coef 0.00 \
  --kl-loss-type low_var_kl \
  --entropy-coef 0.00 \
  --eps-clip 0.2 \
  --eps-clip-high 0.28 \
  --optimizer adam \
  --lr "${LR:-1e-6}" \
  --lr-decay-style constant \
  --weight-decay 0.1 \
  --adam-beta1 0.9 \
  --adam-beta2 0.98 \
  --tensor-model-parallel-size 1 \
  --pipeline-model-parallel-size 1 \
  --context-parallel-size 1 \
  --expert-model-parallel-size 1 \
  --expert-tensor-parallel-size 1 \
  --use-dynamic-batch-size \
  --max-tokens-per-gpu "${MAX_TOKENS_PER_GPU:-2048}" \
  --rollout-num-gpus-per-engine 1 \
  --sglang-mem-fraction-static "${SGLANG_MEM_FRACTION_STATIC:-0.6}" \
  --sglang-cuda-graph-max-bs "${SGLANG_CUDA_GRAPH_MAX_BS:-32}"
