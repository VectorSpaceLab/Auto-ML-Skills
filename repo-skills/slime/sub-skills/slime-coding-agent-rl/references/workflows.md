# Coding-Agent RL Workflow

Read this when wiring a software-engineering agent loop into slime.

## Components

- Custom generate function: boots the sandbox, starts the agent client, captures tool interactions, collects token segments, and returns one or more slime `Sample` objects.
- Protocol adapter: exposes Anthropic or OpenAI-compatible endpoints to the agent client while calling SGLang with `input_ids` and preserving sampled token ids.
- Sandbox backend: provides an isolated repo/workdir, command execution, file writes, patch capture, and clean evaluation.
- Reward/grader: evaluates a patch using SWE metadata, a test command, or a custom harness.

## Launch Pattern

Use the standard slime RL command plus coding-agent-specific rollout args:

```bash
--custom-generate-function-path <module.generate>
--prompt-data <swe_train.jsonl>
--input-key prompt
--label-key label
--metadata-key metadata
--rollout-batch-size <small_first>
--n-samples-per-prompt <small_first>
--rollout-max-context-len <agent_context_budget>
--rollout-max-response-len <per_turn_generation_cap>
--save-debug-rollout-data <run_root>/rollout_dumps/rollout_{rollout_id}.pt
```

For Qwen-style coding models, SGLang parser flags must match the model:

```bash
--sglang-tool-call-parser <model_tool_parser>
--sglang-reasoning-parser <model_reasoning_parser>
```

## Token Provenance

Coding agents operate with strings, messages, tool calls, and observations. Training must remain token-based:

- The adapter sends rendered prompt `input_ids` to SGLang.
- SGLang returns sampled `output_ids` with logprobs.
- Tool observations and environment text are added with `loss_mask=0`.
- Only model-sampled output tokens keep `loss_mask=1`.
- If later conversation text no longer token-matches earlier sampled output, do not train through the mismatched suffix.

## Fan-Out Samples

One agent trajectory may produce multiple trainable segments, such as subagent branch, pre-compaction chain, and final answer. Return `list[Sample]` with a shared `group_id` so loss aggregation treats siblings as one rollout group.

## Smoke Test

Before a long run:

1. Validate JSONL metadata.
2. Boot one sandbox manually or with the adapter's preflight path.
3. Run one prompt with one sample per prompt.
4. Confirm a patch or terminal result is captured.
5. Confirm the reward/grader runs in a clean sandbox.
6. Inspect rollout dump for token ids and loss masks.
