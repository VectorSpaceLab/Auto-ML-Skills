#!/usr/bin/env bash
OPD_ARGS=(
  --use-opd
  --opd-type megatron
  --opd-kl-coef "${OPD_KL_COEF:-1.0}"
  --opd-teacher-load "${OPD_TEACHER_LOAD:?Set OPD_TEACHER_LOAD}"
)
