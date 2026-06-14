# GRPO Reward Debugging

## User Persona
An experienced alignment practitioner using online TRL training.

## Scenario Coverage
- Skill area: `core-trainers` and `data-and-rewards`
- Capability: GRPO reward callable shape, reward metrics, generation count, reward diversity
- Difficulty: troubleshooting
- Prompt file: `user_request.txt`
- Expected references/scripts: `core-trainers/references/trainer-workflows.md`, `data-and-rewards/references/reward-functions.md`
- Trigger expectation: The prompt names GRPO, TRL, reward metrics, and a custom reward function.

## Expected Successful Behavior
The agent should explain `frac_reward_zero_std`, advise testing the reward function on a tiny generated-completion batch, verify one reward per completion and use of the `solution` column, inspect reward scale/diversity, tune `num_generations`, `max_completion_length`, and reward weights, and recommend logging completions before scaling.

## Failure Signals
The response treats the issue as a generic optimizer problem, ignores reward output shape, omits GRPO-specific metrics, or tells the user to rewrite trainer internals.
