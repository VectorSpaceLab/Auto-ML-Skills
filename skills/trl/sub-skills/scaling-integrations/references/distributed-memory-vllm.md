# Distributed, Memory, And vLLM

Read this for practical scaling choices.

## Effective Batch Size

For data-parallel training:

```text
effective_batch_size = per_device_train_batch_size * num_devices * gradient_accumulation_steps
```

Use:

```bash
python scripts/effective_batch.py --per-device 4 --devices 8 --grad-accum 2
```

Keep effective batch size stable when moving from one GPU to many GPUs by reducing `per_device_train_batch_size` or `gradient_accumulation_steps`.

## Memory Reduction Levers

General:

- Lower `per_device_train_batch_size`.
- Increase `gradient_accumulation_steps`.
- Lower sequence length: `max_length` for SFT/DPO/Reward, `max_completion_length` for online methods.
- Use `bf16=True` on modern GPUs where supported.
- Use gradient checkpointing, enabled by default in inspected configs.
- Use PEFT/LoRA and QLoRA.
- Use `activation_offloading=True` if CPU RAM and transfer overhead are acceptable.

SFT-specific:

- `packing=True` with `packing_strategy="bfd"` for short examples.
- `packing_strategy="bfd_split"` to preserve overlong examples by splitting.
- `padding_free=True` with FlashAttention-compatible attention.
- `loss_type="chunked_nll"` for standard NLL with lower peak activation memory when compatible.

GRPO/RLOO-specific:

- Lower `num_generations`.
- Lower `max_completion_length`.
- Use vLLM to reduce generation bottlenecks.
- Tune `vllm_gpu_memory_utilization` and `vllm_max_model_length`.

## Accelerate

Basic launch:

```bash
accelerate config
accelerate launch train.py
```

With config:

```bash
accelerate launch --config_file multi_gpu.yaml train.py
```

TRL examples include configs for:

- single GPU
- multi-GPU
- DeepSpeed ZeRO 1/2/3
- FSDP1/FSDP2
- context parallelism
- ALST/Ulysses sequence parallelism

## DeepSpeed

Install:

```bash
pip install "trl[deepspeed]"
```

Launch:

```bash
accelerate launch --config_file deepspeed_zero2.yaml train.py
```

Use DeepSpeed when optimizer state, gradients, or parameters need partitioning or offloading. ZeRO stages trade memory savings against communication and complexity.

## FSDP And Context Parallelism

Context parallelism splits long sequences across GPUs using FSDP2/Ring Attention in the inspected docs.

Important notes:

- Requires compatible Accelerate and PyTorch FSDP2 support.
- Uses `cp_size` with `cp_backend="torch"` in Accelerate parallelism config.
- Sequence length must be divisible by `cp_size * 2`; use `pad_to_multiple_of`.
- SDPA attention is required for the Ring Attention path described in docs.
- Do not enable both FSDP activation checkpointing and config-level `gradient_checkpointing=True` when those settings conflict.

SFT config pattern:

```python
from trl import SFTConfig

args = SFTConfig(
    max_length=16384,
    packing=True,
    pad_to_multiple_of=4,
    use_liger_kernel=True,
    gradient_checkpointing=False,
    per_device_train_batch_size=1,
)
```

## ALST/Ulysses Sequence Parallelism

The inspected docs describe ALST/Ulysses as a DeepSpeed-backed sequence splitting approach:

- Uses `sp_size` with `sp_backend="deepspeed"`.
- Requires compatible Accelerate and DeepSpeed versions.
- Sequence length should be divisible by `sp_size`; use `pad_to_multiple_of`.
- Flash Attention 2 or SDPA can be used depending on setup.
- Ensure `dp_replicate_size * dp_shard_size * sp_size = num_processes`.

## vLLM Modes

Supported online trainer families in inspected docs:

- `GRPOTrainer`
- `RLOOTrainer`
- `experimental.online_dpo.OnlineDPOTrainer`
- `experimental.nash_md.NashMDTrainer`
- `experimental.xpo.XPOTrainer`

### Colocate Mode

```python
from trl import GRPOConfig

args = GRPOConfig(use_vllm=True)  # vllm_mode="colocate" by default
```

Colocate mode runs vLLM inside the trainer process and shares GPU memory. It is convenient but can increase memory contention.

### Server Mode

Start server:

```bash
CUDA_VISIBLE_DEVICES=0,1,2,3 trl vllm-serve --model Qwen/Qwen2.5-7B --tensor-parallel-size 4
```

Train on separate GPUs:

```python
from trl import GRPOConfig

args = GRPOConfig(use_vllm=True, vllm_mode="server")
```

```bash
CUDA_VISIBLE_DEVICES=4,5,6,7 accelerate launch train.py
```

Do not let the server and trainer use the same CUDA devices.

## vLLM Server Flags

Important `trl vllm-serve` flags:

- `--model`
- `--revision`
- `--tensor-parallel-size`
- `--data-parallel-size`
- `--host`
- `--port`
- `--gpu-memory-utilization`
- `--dtype`
- `--max-model-len`
- `--enable-prefix-caching`
- `--enforce-eager`
- `--kv-cache-dtype`
- `--trust-remote-code`
- `--vllm-model-impl`
- `--distributed-executor-backend`
- `--speculative-config`

Use [../scripts/vllm_server_command.py](../scripts/vllm_server_command.py) to construct a safe starter command.
