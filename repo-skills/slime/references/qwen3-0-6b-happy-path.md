# Qwen3-0.6B Minimal Happy Path

Read this when a user asks for the smallest practical slime pipeline using a local Qwen3-0.6B Hugging Face checkpoint.

Placeholders:

- `${SKILL_DIR}`: root of this generated `slime` skill directory.
- `${MEGATRON_PATH}`: full Megatron-LM checkout.
- `${HF_CHECKPOINT}`: local Qwen3-0.6B Hugging Face directory.
- `${TORCH_DIST}`: Megatron `torch_dist` output directory.
- `${DATA_JSONL}`: prompt or SFT dataset path.
- `${SAVE_DIR}`: slime training checkpoint root.

## 1. Verify Environment

```bash
python ${SKILL_DIR}/scripts/check_env.py
python ${SKILL_DIR}/scripts/check_env.py --strict-train --megatron-path ${MEGATRON_PATH}
```

## 2. Convert HF To Megatron

```bash
MODEL_ARGS=( $(python ${SKILL_DIR}/scripts/inspect_model_recipe.py qwen3-0.6b) )

PYTHONPATH=${MEGATRON_PATH}:${PYTHONPATH} python ${SKILL_DIR}/scripts/convert_hf_to_torch_dist.py \
  "${MODEL_ARGS[@]}" \
  --hf-checkpoint ${HF_CHECKPOINT} \
  --save ${TORCH_DIST}
```

After conversion, `${TORCH_DIST}` should contain `latest_checkpointed_iteration.txt` and an `iter_*` directory.

## 3A. Minimal SFT

Expected JSONL record:

```json
{"messages":[{"role":"user","content":"Say hello."},{"role":"assistant","content":"Hello!"}]}
```

Run template:

```bash
export SLIME_SKILL_DIR=${SKILL_DIR}
export MEGATRON_PATH=${MEGATRON_PATH}
export HF_CHECKPOINT=${HF_CHECKPOINT}
export REF_LOAD=${TORCH_DIST}
export PROMPT_DATA=${DATA_JSONL}
export SAVE_DIR=${SAVE_DIR}
export MODEL_RECIPE=qwen3-0.6b
export INPUT_KEY=messages
bash ${SKILL_DIR}/sub-skills/slime-sft-training/scripts/run_sft_template.sh
```

Do not set `--apply-chat-template` for this SFT path. `slime.rollout.sft_rollout.generate_rollout` expects `messages` to remain a list of role/content dictionaries so it can build the SFT loss mask.

## 3B. Minimal GRPO

Expected JSONL record:

```json
{"prompt":[{"role":"user","content":"Solve 1+1. Answer: "}],"label":"2"}
```

Run template:

```bash
export SLIME_SKILL_DIR=${SKILL_DIR}
export MEGATRON_PATH=${MEGATRON_PATH}
export HF_CHECKPOINT=${HF_CHECKPOINT}
export REF_LOAD=${TORCH_DIST}
export PROMPT_DATA=${DATA_JSONL}
export SAVE_DIR=${SAVE_DIR}
export MODEL_RECIPE=qwen3-0.6b
export SGLANG_CUDA_GRAPH_MAX_BS=1
bash ${SKILL_DIR}/sub-skills/slime-rl-training/scripts/run_grpo_template.sh
```

## Notes

- SFT template uses async runner and does not set `--colocate`.
- GRPO template uses colocated synchronous runner by default.
- Reduce batch sizes and response length for smoke tests.
- Use the bundled launch template path so Ray workers inherit PyTorch/NVIDIA library paths for SGLang subprocesses.
- For real training, replace toy data with task data and tune reward, stop tokens, and SGLang memory.
