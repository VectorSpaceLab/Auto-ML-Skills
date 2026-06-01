# Scaling And Integrations Troubleshooting

## Effective Batch Changed After Scaling

Compute:

```text
per_device_train_batch_size * num_devices * gradient_accumulation_steps
```

If you scale from 1 GPU to 8 GPUs and keep every other setting unchanged, the effective batch becomes 8 times larger. Adjust per-device batch or accumulation.

## CUDA Out Of Memory

Apply in order:

1. Lower `per_device_train_batch_size`.
2. Lower `max_length` / `max_completion_length`.
3. Lower GRPO/RLOO `num_generations`.
4. Increase `gradient_accumulation_steps` only after lowering per-device batch.
5. Use PEFT/QLoRA.
6. Use SFT packing or chunked loss where compatible.
7. Use activation offloading or distributed sharding.

## vLLM NCCL Or Device Conflict

In server mode, ensure trainer and server use distinct devices:

```bash
CUDA_VISIBLE_DEVICES=0,1,2,3 trl vllm-serve --model model --tensor-parallel-size 4
CUDA_VISIBLE_DEVICES=4,5,6,7 accelerate launch train.py
```

Do not leave `CUDA_VISIBLE_DEVICES` unset on the trainer if the server is already using some GPUs.

## vLLM OOM At Startup

Try:

- Lower `--gpu-memory-utilization`.
- Set `--max-model-len` to the actual needed context.
- Lower trainer-side `vllm_gpu_memory_utilization`.
- Reduce tensor parallel size only if the model fits on fewer GPUs.
- Use `vllm_enable_sleep_mode` from trainer config when colocate mode memory contention is the issue.

## vLLM Version Error

The inspected docs support `vllm>=0.12.0,<=0.19.0`. Check:

```bash
python -m pip show vllm trl
```

Then align versions with the installed TRL package.

## DeepSpeed Launch Fails

Check:

- `deepspeed` is installed.
- Accelerate config references the correct ZeRO stage.
- `num_processes` matches available GPUs.
- The model and optimizer fit the chosen ZeRO/offload setup.

For ALST/Ulysses, verify `dp_replicate_size * dp_shard_size * sp_size = num_processes`.

## Context Parallelism Shape Error

For Ring Attention / FSDP2 context parallelism:

- Use `pad_to_multiple_of=cp_size * 2`.
- Use SDPA attention for the path described in docs.
- Use FSDP2.
- Avoid conflicting activation checkpointing settings.

## PEFT Import Error

Install:

```bash
pip install "trl[peft]"
```

If using QLoRA:

```bash
pip install "trl[quantization]"
```

Then verify:

```bash
python -c "import peft, bitsandbytes"
```

## Liger Or Kernels Error

Check compatibility:

- Liger requires `liger-kernel`.
- Hub kernels require `kernels` and a compatible Transformers attention implementation path.
- `chunked_nll` is not compatible with Liger, PEFT, or VLM in the inspected docs.
- Padding-free needs compatible attention such as FlashAttention-style kernels.
