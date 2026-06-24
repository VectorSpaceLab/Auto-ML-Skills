#!/usr/bin/env bash
OPD_ARGS=(
  --use-opd
  --opd-type sglang
  --opd-kl-coef "${OPD_KL_COEF:-1.0}"
  --custom-rm-path slime.rollout.on_policy_distillation.reward_func
  --custom-reward-post-process-path slime.rollout.on_policy_distillation.post_process_rewards
  --rm-url "${OPD_TEACHER_URL:?Set OPD_TEACHER_URL}"
)
