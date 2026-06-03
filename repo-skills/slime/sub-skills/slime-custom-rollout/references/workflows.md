# Customization Workflows

## RAG Or Tool Use

Use:

```bash
--custom-generate-function-path my_project.generate.custom_generate
--custom-rm-path my_project.reward.custom_rm
```

This reuses slime's default rollout loop, SGLang request handling, reward application, and training conversion.

## Complex Multi-Agent Or Environment Loop

Use:

```bash
--rollout-function-path my_project.rollout.generate_rollout
```

Only choose this when per-sample `custom_generate` cannot express the orchestration.

## Dynamic Sampling

Use:

```bash
--dynamic-sampling-filter-path slime.rollout.filter_hub.dynamic_sampling_filters.check_reward_nonzero_std
```

or a custom implementation returning `DynamicFilterOutput`.

## Custom Loss

Use:

```bash
--loss-type custom_loss
--custom-loss-function-path my_project.loss.custom_loss
```

Keep train data fields consistent with what the loss consumes.

## Contract Validation

Before GPU jobs, import the hook and inspect its signature:

```bash
python sub-skills/slime-custom-rollout/scripts/validate_custom_hook_import.py \
  --path my_project.generate.custom_generate \
  --kind custom-generate
```

The original slime test suite also includes CPU-only plugin contract tests, but ordinary skill users should start with import/signature validation.
