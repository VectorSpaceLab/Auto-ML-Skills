# Integrations And Compatibility

Read this when choosing optional extras or combining speed/memory features.

## Optional Extras

| Workflow | Install |
| --- | --- |
| PEFT / LoRA | `pip install "trl[peft]"` |
| Quantization / bitsandbytes | `pip install "trl[quantization]"` |
| vLLM | `pip install "trl[vllm]"` |
| DeepSpeed | `pip install "trl[deepspeed]"` |
| Liger | `pip install "trl[liger]"` |
| Hub kernels | `pip install "trl[kernels]"` |
| Vision-language examples | `pip install "trl[vlm]"` |
| OpenReward | `pip install "trl[openreward]"` |

## PEFT

All major stable trainers support PEFT through a `peft_config` argument or CLI model args.

Common LoRA pattern:

```python
from peft import LoraConfig

peft_config = LoraConfig(
    r=32,
    lora_alpha=16,
    lora_dropout=0.05,
    bias="none",
    task_type="CAUSAL_LM",
)
```

For reward models:

```bash
--lora_task_type SEQ_CLS
```

LoRA often uses a learning rate around 10 times higher than full fine-tuning for the same trainer family.

## Quantization

Use with PEFT/QLoRA:

```bash
--load_in_4bit --bnb_4bit_quant_type nf4
```

Do not enable both `load_in_8bit` and `load_in_4bit`.

## Hub Kernels And Attention

Use Hub kernels through Transformers attention implementation fields:

```python
from trl import SFTConfig

args = SFTConfig(
    model_init_kwargs={"attn_implementation": "kernels-community/flash-attn2"}
)
```

CLI:

```bash
trl sft ... --attn_implementation kernels-community/flash-attn2
```

Hub kernels avoid local FlashAttention compilation in supported setups.

## Liger Kernel

Install:

```bash
pip install liger-kernel
```

Enable:

```python
from trl import SFTConfig

args = SFTConfig(use_liger_kernel=True)
```

Supported trainer families in inspected docs:

- SFT
- DPO
- GRPO
- KTO
- GKD

Compatibility caveat from inspected memory docs: `loss_type="chunked_nll"` is not compatible with `use_liger_kernel=True`, PEFT, or VLM.

## Padding-Free

Use `padding_free=True` with FlashAttention-compatible attention. Without a compatible attention implementation, padding-free batching can cause batch contamination.

## vLLM Compatibility

The inspected docs state TRL supports vLLM versions from `0.12.0` to `0.19.0`.

Trainers with vLLM support in docs:

- Stable: GRPO, RLOO.
- Experimental: Online DPO, NashMD, XPO.

Use server mode when you have dedicated inference GPUs. Use colocate mode for convenience when memory permits.

## Vision-Language Models

Install `trl[vlm]` for image/video helpers and examples. Use model processors carefully, and verify one row before training. Some example scripts are tested only with specific VLM architectures; do not generalize blindly.

## Logging Integrations

Inspected configs default `report_to="none"`. Enable external logging intentionally:

```python
args = SFTConfig(report_to="trackio", project="my-project")
```

or use supported Transformers/Trainer logging integrations available in the environment.
