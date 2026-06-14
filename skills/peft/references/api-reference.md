# PEFT API Reference

Use this reference for verified public APIs and adapter families. The signatures here were checked against an installed PEFT package from the current repository state and should be treated as practical guidance, not a replacement for inspecting the exact installed version when a user reports version-specific behavior.

## Package Facts

- Distribution name: `peft`
- Import module: `peft`
- Package requires Python `>=3.10.0` in the repository metadata.
- Runtime dependencies include `torch`, `transformers`, `accelerate`, `huggingface_hub`, `safetensors`, `numpy`, `packaging`, `psutil`, `pyyaml`, and `tqdm`.
- The repo CI test matrix includes Python `3.10`, `3.11`, `3.12`, and `3.13`.

## Core Signatures

```text
get_peft_model(
    model,
    peft_config,
    adapter_name="default",
    mixed=False,
    autocast_adapter_dtype=True,
    revision=None,
    low_cpu_mem_usage=False,
) -> PeftModel | PeftMixedModel
```

Use `get_peft_model` to create a PEFT-wrapped model for training or fresh adapter initialization. It modifies the passed model in place.

```text
PeftModel.from_pretrained(
    model,
    model_id,
    adapter_name="default",
    is_trainable=False,
    config=None,
    autocast_adapter_dtype=True,
    ephemeral_gpu_offload=False,
    low_cpu_mem_usage=False,
    key_mapping=None,
    **kwargs,
) -> PeftModel
```

Use `PeftModel.from_pretrained` to load trained adapter weights on top of an already-loaded compatible base model.

```text
PeftModel.save_pretrained(
    save_directory,
    safe_serialization=True,
    selected_adapters=None,
    save_embedding_layers="auto",
    is_main_process=True,
    path_initial_model_for_weight_conversion=None,
    **kwargs,
) -> None
```

By default this saves adapter files, not the full base model. Adapter checkpoints normally include `adapter_config.json`, `adapter_model.safetensors` or `adapter_model.bin`, and a model card `README.md`.

```text
PeftConfig.from_pretrained(pretrained_model_name_or_path, subfolder=None, **kwargs)
```

Use this to discover `peft_type`, `base_model_name_or_path`, task type, target modules, and other adapter settings from a local adapter directory or Hub repo.

```text
prepare_model_for_kbit_training(model, use_gradient_checkpointing=True, gradient_checkpointing_kwargs=None)
```

Use this after loading a quantized model and before wrapping it with a PEFT config for k-bit training.

## Auto Classes

Use `AutoPeftModel*` when the adapter config contains enough information to infer and load the base model:

- `AutoPeftModel`
- `AutoPeftModelForCausalLM`
- `AutoPeftModelForSeq2SeqLM`
- `AutoPeftModelForSequenceClassification`
- `AutoPeftModelForTokenClassification`
- `AutoPeftModelForQuestionAnswering`
- `AutoPeftModelForFeatureExtraction`

Relevant signature:

```text
AutoPeftModelForCausalLM.from_pretrained(
    pretrained_model_name_or_path,
    adapter_name="default",
    is_trainable=False,
    config=None,
    revision=None,
    import_allowlist=None,
    **kwargs,
)
```

`import_allowlist` protects dynamic base-model imports from adapter config `auto_mapping`. If a safe external package is needed and not in the defaults, pass its import name explicitly.

## Task Types

Use `TaskType` constants instead of raw strings when possible:

- `TaskType.SEQ_CLS`
- `TaskType.SEQ_2_SEQ_LM`
- `TaskType.CAUSAL_LM`
- `TaskType.TOKEN_CLS`
- `TaskType.QUESTION_ANS`
- `TaskType.FEATURE_EXTRACTION`

Supplying the right `task_type` helps PEFT pick the right wrapper class and can help with task heads such as sequence classification.

## Adapter Type To Config Class

Common adapter configs:

- `LORA`: `LoraConfig`
- `ADALORA`: `AdaLoraConfig`
- `IA3`: `IA3Config`
- `PROMPT_TUNING`: `PromptTuningConfig`
- `P_TUNING`: `PromptEncoderConfig`
- `PREFIX_TUNING`: `PrefixTuningConfig`
- `MULTITASK_PROMPT_TUNING`: `MultitaskPromptTuningConfig`
- `LOHA`: `LoHaConfig`
- `LOKR`: `LoKrConfig`
- `OFT`: `OFTConfig`
- `BOFT`: `BOFTConfig`
- `VERA`: `VeraConfig`
- `PVERA`: `PveraConfig`
- `RANDLORA`: `RandLoraConfig`
- `TRAINABLE_TOKENS`: `TrainableTokensConfig`
- `XLORA`: `XLoraConfig`
- `HIRA`: `HiraConfig`
- `SHIRA`: `ShiraConfig`
- `ROAD`: `RoadConfig`
- `WAVEFT`: `WaveFTConfig`
- `GRALORA`: `GraloraConfig`
- `CARTRIDGE`: `CartridgeConfig`
- `TINYLORA`: `TinyLoraConfig`
- `PSOFT`: `PsoftConfig`
- `PEANUT`: `PeanutConfig`

The repository contains additional method configs such as `AdamssConfig`, `AdaptionPromptConfig`, `BeftConfig`, `C3AConfig`, `CPTConfig`, `DeloraConfig`, `FourierFTConfig`, `HRAConfig`, `LilyConfig`, `LNTuningConfig`, `MissConfig`, `OSFConfig`, `PolyConfig`, and `VBLoRAConfig`.

## Important Config Signatures

`LoraConfig` accepts many options. High-impact parameters include:

```text
task_type=None
r=8
target_modules=None
exclude_modules=None
lora_alpha=8
lora_dropout=0.0
fan_in_fan_out=False
bias="none"
use_rslora=False
modules_to_save=None
init_lora_weights=True
rank_pattern={}
alpha_pattern={}
trainable_token_indices=None
use_dora=False
alora_invocation_tokens=None
use_qalora=False
qalora_group_size=16
target_parameters=None
ensure_weight_tying=False
```

`IA3Config` core options:

```text
task_type=None
target_modules=None
exclude_modules=None
feedforward_modules=None
fan_in_fan_out=False
modules_to_save=None
init_ia3_weights=True
```

`PromptTuningConfig` core options:

```text
task_type=None
num_virtual_tokens=None
token_dim=None
num_transformer_submodules=None
num_attention_heads=None
num_layers=None
prompt_tuning_init=PromptTuningInit.RANDOM
prompt_tuning_init_text=None
tokenizer_name_or_path=None
tokenizer_kwargs=None
```

`PrefixTuningConfig` core options:

```text
task_type=None
num_virtual_tokens=None
token_dim=None
num_transformer_submodules=None
num_attention_heads=None
num_layers=None
init_weights=None
encoder_hidden_size=None
prefix_projection=False
```

## Low-Level APIs

```text
inject_adapter_in_model(peft_config, model, adapter_name="default", low_cpu_mem_usage=False, state_dict=None)
```

Injects adapters into a plain `torch.nn.Module`. It does not provide all `PeftModel` utilities.

```text
get_peft_model_state_dict(model, state_dict=None, adapter_name="default", unwrap_compiled=False, save_embedding_layers="auto")
set_peft_model_state_dict(model, peft_model_state_dict, adapter_name="default", ignore_mismatched_sizes=False, low_cpu_mem_usage=False)
```

Use these when manually saving/loading adapter state dicts, especially with low-level injection.

```text
cast_mixed_precision_params(model, dtype) -> None
replace_lora_weights_loftq(peft_model, model_path=None, adapter_name="default", callback=None)
find_kappa_target_modules(model, top_p=0.2, max_dim_size_to_analyze=16384, moe_param_suffixes=None, show_progress=True)
```

Use `cast_mixed_precision_params` for adapter dtype handling, `replace_lora_weights_loftq` for in-place LoftQ replacement, and `find_kappa_target_modules` for KappaTune target selection.

## Mixed Adapter Compatibility

`PeftMixedModel` supports loading different compatible adapter types for inference-style composition. It is not meant as the default training path.

Verified mixed-compatible PEFT types include:

- `LORA`
- `ADALORA`
- `IA3`
- `BEFT`
- `LOHA`
- `LOKR`
- `ROAD`
- `HIRA`
- `SHIRA`

Relevant signatures:

```text
PeftMixedModel.from_pretrained(model, model_id, adapter_name="default", is_trainable=False, config=None, **kwargs)
PeftMixedModel.load_adapter(model_id, adapter_name, *args, **kwargs)
PeftMixedModel.set_adapter(adapter_name, inference_mode=False) -> None
```

`PeftMixedModel` does not support saving and loading mixed adapters as a single combined object. Keep the adapter-loading script.
