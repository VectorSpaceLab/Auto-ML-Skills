#!/usr/bin/env bash
# Template: load a bundled model recipe into MODEL_ARGS.
set -euo pipefail

: "${SLIME_SKILL_DIR:?Set SLIME_SKILL_DIR to the root slime skill directory}"
: "${MODEL_RECIPE:=qwen3-0.6b}"

MODEL_ARGS=( $(python "${SLIME_SKILL_DIR}/scripts/inspect_model_recipe.py" "${MODEL_RECIPE}") )
printf 'Loaded %s with %d shell words\n' "${MODEL_RECIPE}" "${#MODEL_ARGS[@]}"
