#!/usr/bin/env bash
PPO_ARGS=(
  --advantage-estimator ppo
  --use-critic
  --critic-load "${CRITIC_LOAD:?Set CRITIC_LOAD}"
  --critic-save "${CRITIC_SAVE:?Set CRITIC_SAVE}"
  --critic-lr "${CRITIC_LR:-1e-5}"
  --num-critic-only-steps "${NUM_CRITIC_ONLY_STEPS:-0}"
  --eps-clip 0.2
  --value-clip 0.2
  --kl-coef 0.0
)
