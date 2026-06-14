# Method Selection

Use this reference when choosing a PEFT method or explaining tradeoffs.

## Default Recommendation

Start with LoRA unless the user has a specific reason to use another method. LoRA has the broadest examples, model support, quantization support, merging support, and troubleshooting coverage.

Basic LoRA:

```python
from peft import LoraConfig, TaskType

config = LoraConfig(
    task_type=TaskType.CAUSAL_LM,
    r=8,
    lora_alpha=16,
    target_modules=["q_proj", "v_proj"],
    lora_dropout=0.05,
    bias="none",
)
```

## LoRA And Variants

Use LoRA for linear, embedding, Conv1d, Conv2d, Conv3d, Transformers `Conv1D`, and many custom modules. Important parameters:

- `r`: rank. Higher rank increases capacity and adapter size.
- `lora_alpha`: scaling.
- `lora_dropout`: regularization during training.
- `target_modules`: module names, suffixes, regex, or `"all-linear"`.
- `modules_to_save`: non-adapter modules to train and save.
- `bias`: `"none"`, `"all"`, or `"lora_only"`.
- `rank_pattern` and `alpha_pattern`: per-layer overrides.

Use `use_rslora=True` when higher ranks are unstable or when rank-stabilized scaling is desired.

Use `use_dora=True` for Weight-Decomposed LoRA. DoRA can improve low-rank performance but adds overhead. Merge for inference when possible. DoRA currently targets embedding, linear, and Conv2d-style layers and has reported issues in some QDoRA plus DeepSpeed Zero2 settings.

Use `trainable_token_indices` when newly added tokens should be trained efficiently without saving full embedding matrices.

Use `target_parameters` when adapting raw `nn.Parameter` tensors instead of modules. This is useful for fused MoE parameter tensors but is not supported by every adapter composition operation.

Use `init_lora_weights` variants deliberately:

- `True`: default identity-style initialization.
- `"gaussian"`: Diffusers-style initialization.
- `"pissa"` or `"pissa_niter_<n>"`: SVD-based initialization.
- `"olora"`: QR-based OLoRA initialization.
- `"eva"` plus `EvaConfig`: data-driven SVD on activations; use `low_cpu_mem_usage=True` and call `initialize_lora_eva_weights`.
- `"corda"` plus `CordaConfig`: task-aware or knowledge-preserving initialization; call the preprocessing function before wrapping.
- `"loftq"` or `replace_lora_weights_loftq`: quantization-error-aware LoRA initialization.
- `False`: debugging/testing only; not an identity transform.

Use LoRA-adjacent configs when the user names the method:

- `AdaLoraConfig`: adaptive rank allocation; requires budget/update handling and often a custom loop or Trainer integration.
- `LoHaConfig`: Low-Rank Hadamard Product.
- `LoKrConfig`: Low-Rank Kronecker Product.
- `BOFTConfig`, `OFTConfig`, `VeraConfig`, `RandLoraConfig`, `HiraConfig`, `ShiraConfig`, and related configs for method-specific experiments.

## IA3

Use IA3 when the user wants very few trainable parameters. IA3 learns activation-scaling vectors for attention and feed-forward blocks.

```python
from peft import IA3Config, TaskType

config = IA3Config(
    task_type=TaskType.SEQ_2_SEQ_LM,
    target_modules=["k", "v", "wo"],
    feedforward_modules=["wo"],
)
```

For Transformers architectures with default mappings, PEFT may infer targets. For custom models, specify both `target_modules` and `feedforward_modules`.

## Prompt-Based Methods

Use prompt methods for language-model tasks where the user wants learned virtual tokens instead of internal module adaptation.

Prompt tuning:

```python
from peft import PromptTuningConfig, PromptTuningInit

config = PromptTuningConfig(
    task_type="CAUSAL_LM",
    num_virtual_tokens=20,
    prompt_tuning_init=PromptTuningInit.TEXT,
    prompt_tuning_init_text="Classify the input.\n",
    tokenizer_name_or_path="base-model-id",
)
```

Prefix tuning:

```python
from peft import PrefixTuningConfig

config = PrefixTuningConfig(task_type="CAUSAL_LM", num_virtual_tokens=20)
```

P-tuning:

```python
from peft import PromptEncoderConfig

config = PromptEncoderConfig(task_type="CAUSAL_LM", num_virtual_tokens=20, encoder_hidden_size=128)
```

Prompt-learning methods depend on task/model handling and are not the right choice for arbitrary `torch.nn.Module` adapters.

## Task Type Selection

Use:

- `TaskType.CAUSAL_LM` for decoder-only generation.
- `TaskType.SEQ_2_SEQ_LM` for encoder-decoder generation.
- `TaskType.SEQ_CLS` for sequence classification.
- `TaskType.TOKEN_CLS` for token classification.
- `TaskType.QUESTION_ANS` for question answering.
- `TaskType.FEATURE_EXTRACTION` for hidden-state feature extraction.

Correct task type helps PEFT select a specific `PeftModelFor*` wrapper and handle task heads.

## Target Module Heuristics

Common attention target names:

- Llama/Mistral/Qwen-style: `q_proj`, `v_proj`, sometimes `k_proj`, `o_proj`, `gate_proj`, `up_proj`, `down_proj`.
- BERT-style: `query`, `value`, sometimes `key` and output dense layers.
- GPT-2-style: `c_attn`, `c_proj`.
- Vision Transformer: `query`, `value`, classifier head in `modules_to_save`.
- Generic MLP/custom: inspect `named_modules()` and choose layer names such as `lin0`, `linear`, `fc1`, `dense`.

When unsure, inspect module names from the actual model. Do not copy target names from a different architecture without checking.
