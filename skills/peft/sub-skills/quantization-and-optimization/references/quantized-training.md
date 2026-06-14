# Quantized PEFT Training

Use this reference for PEFT with quantized base models.

## bitsandbytes QLoRA

Install compatible packages:

```bash
python -m pip install -U peft transformers accelerate bitsandbytes
```

Load a 4-bit base model:

```python
import torch
from transformers import AutoModelForCausalLM, BitsAndBytesConfig

quant_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_use_double_quant=True,
    bnb_4bit_compute_dtype=torch.bfloat16,
)

base_model = AutoModelForCausalLM.from_pretrained(
    "model-id",
    quantization_config=quant_config,
    device_map="auto",
)
```

Prepare and wrap:

```python
from peft import LoraConfig, TaskType, get_peft_model, prepare_model_for_kbit_training

base_model = prepare_model_for_kbit_training(base_model)
config = LoraConfig(
    task_type=TaskType.CAUSAL_LM,
    target_modules="all-linear",
    r=16,
    lora_alpha=32,
    lora_dropout=0.05,
    bias="none",
)
model = get_peft_model(base_model, config)
```

Use `target_modules="all-linear"` when adapting all linear layers is intended, as in QLoRA.

## LoftQ

LoftQ initializes LoRA weights to reduce quantization error. Strong defaults:

- Use 4-bit NF4 quantization when available.
- Target as many linear layers as practical, often `target_modules="all-linear"`.
- Do not combine `init_lora_weights="loftq"` and `replace_lora_weights_loftq` in the same flow unless the user has a specific reason.

On-the-fly replacement:

```python
from peft import replace_lora_weights_loftq

model = get_peft_model(base_model, lora_config)
replace_lora_weights_loftq(model)
```

Limitations:

- The replacement helper supports only a limited LoftQ iteration.
- It expects compatible LoRA and quantized model state.
- It is focused on bitsandbytes 4-bit quantization and safetensors model files.

## GPTQ

PEFT supports post-training PEFT adapters on GPTQ-style quantized models through compatible Transformers/GPTQModel paths.

Install when needed:

```bash
python -m pip install "gptqmodel>=7.0.0"
```

Then load or create the GPTQ model with Transformers/GPTQ config and apply a LoRA config with `get_peft_model`.

## AQLM

AQLM quantized models support LoRA adapter tuning, but finetuned adapters should be saved separately. Merging LoRA adapters with AQLM quantized weights is not possible in the documented path.

Install when needed:

```bash
python -m pip install "aqlm>=1.0.2"
```

## EETQ

EETQ supports int8 quantized model loading through compatible Transformers versions and LoRA adapter training:

```python
from transformers import EetqConfig

quant_config = EetqConfig("int8")
base_model = AutoModelForCausalLM.from_pretrained("model-id", quantization_config=quant_config)
model = get_peft_model(base_model, lora_config)
```

## HQQ

HQQ models can be adapted with LoRA through the HQQ library or compatible Transformers `HqqConfig`.

```bash
python -m pip install hqq
```

Then load a quantized model and pass it to `get_peft_model`.

## torchao

PEFT supports LoRA with torchao int8 paths:

```python
from transformers import TorchAoConfig
from torchao.quantization import Int8WeightOnlyConfig

quant_config = TorchAoConfig(quant_type=Int8WeightOnlyConfig())
base_model = AutoModelForCausalLM.from_pretrained("model-id", quantization_config=quant_config)
model = get_peft_model(base_model, lora_config)
```

Caveats:

- Use recent torchao and Transformers.
- Only linear layers are currently supported in the documented guide.
- DoRA works only with `int8_weight_only` in the documented path.
- Merge correctness is limited, especially outside LoRA and int8 weight-only.

## Intel Neural Compressor

INC quantized models can load LoRA adapters for supported Linear layers. Documented caveats:

- `merge()` and `unmerge()` are not supported.
- Only Linear INC-quantized layers are supported for adapter loading in the documented path.

## Hardware Checks

For GPU quantized training, verify:

```python
import torch
print(torch.__version__, torch.version.cuda)
print(torch.cuda.is_available(), torch.cuda.device_count())
if torch.cuda.is_available():
    print(torch.cuda.get_device_name(0), torch.cuda.get_device_capability(0))
```

If CUDA is unavailable, check whether the torch wheel is CPU-only, whether the driver/container exposes GPUs, and whether the selected quantization library supports CPU fallback.
