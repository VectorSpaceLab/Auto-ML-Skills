# Data, Model, Registry, and Template Customization

## When To Read

Dataset schemas, message rows, column mappings, model/template registries, custom datasets/models/templates, and package-specific data customization workflows.

## Repo Skill Options

<!-- SKILLQED_SCENARIO:data-model-customization:START -->
### `ms-swift`

Role: Covers ms-swift data formats, preprocessors, external plugins, registries, and template/model selection.
Read when: custom_dataset_info, external_plugins, register_dataset, register_model, register_template, messages format, rejected_response, loss_scale, images/videos/audios, tools.
Best for: Validating JSONL/CSV data, planning column mappings, authoring plugin skeletons, and checking registry/template behavior before training or inference.
Avoid when: The task is only to run an already valid training command or evaluate a model without custom data/schema work.
Useful entry points: `ms-swift/SKILL.md`, `ms-swift/sub-skills/data-model-customization/SKILL.md`.

### `torchtune`

Role: Explains torchtune dataset/message transforms, JSONL validation, config component dotpaths, model builders, tokenizer choices, and public API boundaries.
Read when: The request mentions torchtune datasets, Message rows, ShareGPT/OpenAI/Alpaca transforms, `column_map`, packing, prompt templates, model builders, or `_component_` dotpaths.
Best for: Adapting torchtune data/model config components and validating small data fixtures before a recipe run.
Avoid when: The task is generic dataset conversion unrelated to torchtune recipes or a different ML framework's registry.
Useful entry points: `torchtune/sub-skills/data-and-datasets/SKILL.md`, `torchtune/sub-skills/models-and-modules/SKILL.md`, `torchtune/sub-skills/cli-and-config/SKILL.md`.

<!-- SKILLQED_SCENARIO:data-model-customization:END -->

## How To Choose

Use this scenario when the request is primarily about adapting data or model registries for a specific ML framework; choose dataset-processing scenarios for generic dataset loading or evaluation plumbing. Route to `ms-swift` first when ms-swift errors mention malformed rows, missing media, column mapping, model_type, template, or external plugin loading. Choose torchtune when the data/model customization must fit torchtune builders, message transforms, or recipe YAML component fields.
