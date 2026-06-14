# Custom Models And Low-Level API

Use this reference when PEFT is applied outside ordinary Transformers auto classes.

## Custom `torch.nn.Module`

Example:

```python
import torch
from torch import nn
from peft import LoraConfig, get_peft_model


class MLP(nn.Module):
    def __init__(self):
        super().__init__()
        self.seq = nn.Sequential(
            nn.Linear(20, 200),
            nn.ReLU(),
            nn.Linear(200, 2),
        )

    def forward(self, x):
        return self.seq(x)


model = MLP()
print([(name, type(module)) for name, module in model.named_modules()])

config = LoraConfig(
    target_modules=["seq.0"],
    modules_to_save=["seq.2"],
)
model = get_peft_model(model, config)
model.print_trainable_parameters()
```

For custom models, PEFT cannot infer architecture-specific target modules. Choose targets from `named_modules()`.

## Supported Target Kinds

LoRA supports several module families, including Linear, embedding, convolution layers, Transformers `Conv1D`, and custom LoRA-dispatched modules. The current repo tests cover many custom cases such as MLP, embeddings, Conv1d/2d/3d, grouped Conv2d, MultiheadAttention, and target parameters.

Unsupported module types require a custom dispatcher or a feature request.

## Regex Targets

You can use regex-like string targets for repeated modules:

```python
config = LoraConfig(
    target_modules=r".*\.mlp\.fc\d",
    modules_to_save=["head.fc"],
)
```

Verify after wrapping:

```python
print(model.targeted_module_names)
```

## Custom LoRA Module Dispatch

Experimental custom dispatch can map a base module type to a custom LoRA layer:

```python
from torch import nn
from peft import LoraConfig, get_peft_model

config = LoraConfig(target_modules=["lstm"])
config._register_custom_module({nn.LSTM: MyLoraLSTMLayer})
model = get_peft_model(base_model, config)
```

Important constraints:

- The custom module should inherit from `nn.Module` and PEFT's LoRA layer base where appropriate.
- Constructor should accept `base_layer` and `adapter_name` positional arguments.
- Adapter parameters should be stored in `ModuleDict` or `ParameterDict` keyed by adapter name.
- Trainable adapter parameter attributes should start with `lora_`.
- Implement `merge`/`unmerge` only if merge support is intended.
- Custom dispatch is not persisted in the saved adapter; register it again before loading.

## Low-Level Injection

Use when the user wants to mutate a plain module in place without `PeftModel` wrappers:

```python
from peft import LoraConfig, inject_adapter_in_model

config = LoraConfig(target_modules=["linear"])
model = inject_adapter_in_model(config, model)
```

Tradeoff:

- Pro: preserves original object attributes and methods.
- Con: does not provide all `PeftModel` utilities such as adapter disabling and merging.

Manual save/load:

```python
from peft import get_peft_model_state_dict, set_peft_model_state_dict

state = get_peft_model_state_dict(model)
model = inject_adapter_in_model(config, fresh_model)
result = set_peft_model_state_dict(model, state)
print(result.unexpected_keys)
```

For large adapter loads:

```python
model = inject_adapter_in_model(config, model, low_cpu_mem_usage=True)
set_peft_model_state_dict(model, state, low_cpu_mem_usage=True)
```

Use `state_dict=` with `inject_adapter_in_model` only to infer target layers from checkpoint keys. It creates layers but does not populate their weights; call `set_peft_model_state_dict` after injection.

## Extending Default Target Mappings

If a Transformers architecture works only when explicit `target_modules` are supplied, consider whether PEFT should add a mapping in `src/peft/utils/constants.py`. For a PR, include tests and update docs/support matrix where relevant.
