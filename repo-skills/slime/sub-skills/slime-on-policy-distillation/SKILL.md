---
name: slime-on-policy-distillation
description: "Configures slime on-policy distillation with SGLang or Megatron teachers using --use-opd and related reward or teacher checkpoint flags."
disable-model-invocation: true
---

# slime On-Policy Distillation

Use this sub-skill when the user wants OPD, teacher KL, or policy training with a SGLang/Megatron teacher.

## Short Workflow

1. Start from an RL training command.
2. Add `--use-opd` and choose `--opd-type sglang` or `--opd-type megatron`.
3. For SGLang teacher, configure teacher service URL and OPD reward/postprocess hooks.
4. For Megatron teacher, provide `--opd-teacher-load`.
5. Keep OPD separate from advantage-estimator choice; it can layer onto GRPO/PPO-style objectives.

Read [references/workflows.md](references/workflows.md) for both teacher modes. Read [references/troubleshooting.md](references/troubleshooting.md) for invalid flag combinations.

## Scripts

- Adapt [scripts/opd_sglang_teacher_args.sh](scripts/opd_sglang_teacher_args.sh) or [scripts/opd_megatron_teacher_args.sh](scripts/opd_megatron_teacher_args.sh).
