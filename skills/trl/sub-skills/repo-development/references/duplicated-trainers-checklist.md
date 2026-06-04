# Duplicated Trainers Checklist

Use this before editing or reviewing trainer internals.

## Principle

TRL trainers are self-contained by design. Shared logic is duplicated across trainers so each trainer can be read and modified in isolation.

Duplicated blocks must remain aligned:

- Same variable names where logic is the same.
- Same control-flow structure.
- Same branch order.
- Same comments, word-for-word, when logic is identical.
- Divergences only where trainer semantics require them.

Consistency is more important than silently fixing one copy.

## Common Duplicated Areas

Search these before editing:

```bash
rg "_last_loaded_step" trl/trainer trl/experimental
rg "_metrics\\[mode\\]" trl/trainer trl/experimental
rg "_get_per_token_logps" trl/trainer trl/experimental
rg "_calculate_rewards" trl/trainer trl/experimental
rg "_prepare_inputs" trl/trainer trl/experimental
rg "_generate_single_turn" trl/trainer trl/experimental
rg "use_vllm|vllm_mode|vllm_server" trl/trainer trl/experimental
rg "log_completions" trl/trainer trl/experimental
```

## When Editing GRPO

Also check:

- RLOO for vLLM generation path similarities.
- Online DPO, NashMD, and XPO under experimental for online generation similarities.
- Tool/environment logic if changing rollout or reward interfaces.
- Metric names and `_metrics[mode]` structure.

## When Editing RLOO

Also check:

- GRPO for vLLM generation, reward computation, and metric logging similarities.
- Other online trainers if the change is generation-related.

## When Editing DPO

Also check:

- Experimental preference trainers such as BCO, CPO, ORPO, SDPO, KTO, and online DPO when shared preference preprocessing or reference-model behavior changes.
- RewardTrainer when preference dataset processing changes.

## When Editing SFT

Also check:

- GKD and distillation trainers if they wrap or copy SFT behavior.
- Chat-template and data utility tests when masking, packing, or formatting changes.

## Review Questions

- Did the PR change one trainer copy but not the corresponding copies?
- Are variable names and comments still aligned?
- Is a divergence due to trainer semantics, or accidental drift?
- Did the PR introduce a helper/base abstraction that contradicts the repo's self-contained trainer design?
- If an original block looks wrong, did the author keep consistency and report the shared bug, rather than fixing only one copy?

## Useful Script

Run:

```bash
python scripts/find_trainer_pattern.py "_generate_single_turn"
```

or any pattern that changed.
