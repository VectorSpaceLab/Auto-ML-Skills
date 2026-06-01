# CLI And Script Troubleshooting

## Command Not Found

Check environment:

```bash
python -c "import trl; print(trl.__version__, trl.__file__)"
python -m pip show trl
trl --help
```

If `trl` is missing but `import trl` works, the console script may not be on `PATH`. Use `python -m trl.cli.main --help` only for diagnosis; install or activate the correct environment for normal use.

## Wrong Command Set

Different TRL versions can expose different commands. Run:

```bash
python scripts/print_cli_summary.py
```

Then build commands from the installed help output rather than static examples.

## Config File Not Applied

Check:

- The command uses `--config path/to/file.yaml`.
- YAML keys match dataclass fields, such as `model_name_or_path`, not shell-style `model-name-or-path`.
- Lists are actual YAML lists for fields like `reward_funcs`.
- `datasets:` mixture config supersedes `dataset_name`.

## Accelerate Args Are Not Forwarded

TRL training commands split config args and CLI args to resolve Accelerate launch args. If distributed launch behavior is confusing:

```bash
trl sft --help | grep -E 'num_processes|config_file|deepspeed|fsdp'
```

Then pass launch-related args directly to the `trl` command. For complex jobs, use `accelerate launch --config_file ... train.py` with an explicit Python training script.

## KTO Emits Experimental Warning

This is expected for v1-style TRL. It means KTO lives in or imports from `trl.experimental` and has no stable API guarantee. Only silence it when the user accepts that risk:

```bash
export TRL_EXPERIMENTAL_SILENCE=1
```

## vLLM Server Fails

Use `trl vllm-serve --help` to confirm installed server flags. In server mode, keep trainer and server on separate CUDA devices:

```bash
CUDA_VISIBLE_DEVICES=0,1,2,3 trl vllm-serve --model Qwen/Qwen2.5-7B --tensor-parallel-size 4
CUDA_VISIBLE_DEVICES=4,5,6,7 trl grpo --config grpo.yaml
```

Install vLLM support with `pip install "trl[vllm]"`.

## Dataset Loading Fails

Check whether the dataset requires:

- A dataset config name.
- A non-default split.
- Authentication to a private Hub repo.
- Local `data_files`.
- Streaming mode.

For mixtures, validate each `path`, `name`, and `split` independently with `datasets.load_dataset` before combining.
