# Troubleshooting

Read this for cross-cutting TRL issues before diving into a specific sub-skill.

## Imports Fail

Run:

```bash
python scripts/check_env.py --optional
python -m pip show trl transformers accelerate datasets
```

Common causes:

- TRL is installed in a different Python environment than the one running the task.
- Optional dependencies are missing. Install the relevant extra such as `trl[peft]`, `trl[quantization]`, `trl[vllm]`, `trl[liger]`, or `trl[openreward]`.
- Source checkouts need editable installation for local changes: `pip install -e ".[dev]"`.

## CLI Command Is Missing

Check:

```bash
trl --help
python -c "import trl; print(trl.__version__, trl.__file__)"
```

The inspected v1-style CLI exposes `dpo`, `env`, `grpo`, `kto`, `reward`, `rloo`, `sft`, `skills`, and `vllm-serve`. If a command differs, inspect the installed `trl.cli.commands` module and run `trl <command> --help`.

## Dataset Shape Errors

Most trainer failures start with a dataset format mismatch:

- SFT: language modeling rows with `text` or `messages`, or prompt-completion rows with `prompt` and `completion`.
- DPO: preference rows with `chosen` and `rejected`, optionally `prompt`.
- GRPO/RLOO: prompt-only rows with `prompt`; reward callables or reward models provide supervision.
- RewardTrainer: preference rows with `chosen` and `rejected`.
- KTO: unpaired preference rows with `prompt`, `completion`, and `label`, or paired preference rows that can be converted.

Use [../sub-skills/data-rewards-chat/scripts/validate_dataset_jsonl.py](../sub-skills/data-rewards-chat/scripts/validate_dataset_jsonl.py) for a quick JSONL shape check.

## Chat Template Problems

Symptoms:

- `assistant_only_loss=True` produces bad masks or all tokens are ignored.
- Tool-calling GRPO changes earlier rendered messages after a tool result is appended.
- Tool arguments fail because a template expected strings but received JSON objects.

Checks:

- For SFT assistant-only loss, the chat template must include generation markers.
- For tool-calling GRPO, the template must be prefix-preserving.
- TRL patches known model-family templates automatically in common cases; unsupported model families may need a manual template.
- Tool-calling datasets should use a `tools` column with JSON schema objects; with `datasets>=4.7.0`, prefer the `Json()` feature for mixed JSON objects.

## Out Of Memory

Start with simple reductions:

- Lower `per_device_train_batch_size`.
- Increase `gradient_accumulation_steps` to preserve effective batch size.
- Lower `max_length` or `max_completion_length`.
- For GRPO/RLOO, lower `num_generations`.
- Use LoRA/QLoRA through PEFT and quantization extras.
- Use `packing=True` for SFT when appropriate.
- Consider `padding_free=True` with FlashAttention-compatible attention.
- Consider `activation_offloading=True`.
- Consider `loss_type="chunked_nll"` for SFT when compatible.

Use [../sub-skills/scaling-integrations/scripts/effective_batch.py](../sub-skills/scaling-integrations/scripts/effective_batch.py) to compute effective batch size.

## vLLM Errors

Important constraints:

- Install with `pip install "trl[vllm]"`.
- In the inspected docs, supported vLLM versions are `>=0.12.0, <=0.19.0`.
- In server mode, run the vLLM server and trainer on separate CUDA devices.
- If vLLM cannot initialize because KV cache is too small or memory is tight, tune `vllm_gpu_memory_utilization`, `vllm_max_model_length`, or sleep mode settings.
- For multi-node tensor parallel server setups, inspect `trl vllm-serve --help` for distributed executor options.

## Experimental Warnings

`trl.experimental` is deliberately unstable. It may emit `TRLExperimentalWarning`. Use experimental APIs only when the workflow requires them and document that users may need to update code after TRL upgrades. To silence the runtime notice for known use cases, set:

```bash
export TRL_EXPERIMENTAL_SILENCE=1
```

## Source Development Failures

For changes to TRL source:

- Run focused tests first, such as `pytest tests/test_sft_trainer.py`.
- If duplicated trainer logic changes, update all aligned copies.
- If a method or algorithm from a paper is added, update `docs/source/paper_index.md`.
- Preserve TRL docstring style and Hugging Face paper links.

See [../sub-skills/repo-development/SKILL.md](../sub-skills/repo-development/SKILL.md).
