# Image Generation and LoRA Training Workflows

## When To Read

Stable Diffusion or Diffusers pipelines, ComfyUI node graphs, image generation servers, diffusion schedulers/adapters, dataset TOML, LoRA training, and model utilities.

## Repo Skill Options

<!-- SKILLQED_SCENARIO:image-generation-and-lora-training-workflows:START -->
### `comfy-ui`

Role: Use ComfyUI as a modular AI content-creation engine: launch and automate the server, submit API workflows, validate graph JSON, author custom nodes, and configure model paths/backends.
Read when: The request names `comfy-ui` or asks for package-specific APIs, CLIs, configs, data/model artifacts, error messages, workflows, or repository maintenance that match this project.
Best for: custom nodes, models config, server api, and workflow execution.
Avoid when: another repo skill in this scenario matches the user's task, package, model family, data format, serving backend, or workflow more directly.
Useful entry points: `comfy-ui/SKILL.md`, `comfy-ui/sub-skills/custom-nodes/`, `comfy-ui/sub-skills/models-config/`, `comfy-ui/sub-skills/server-api/`, `comfy-ui/sub-skills/workflow-execution/`.

### `control-net`

Role: Guides ControlNet 1.0 source-checkout workflows for annotators, Gradio image-generation apps, Fill50K-style training data, configs, and checkpoint utilities.
Read when: User mentions ControlNet, lllyasviel/ControlNet, cldm, annotator, Fill50K, gradio_canny2image, control_sd15, control_sd21, Canny/HED/MLSD/MiDaS/OpenPose/Uniformer conditioning, or ControlNet checkpoint transfer.
Best for: Preparing conditioning maps, inspecting Gradio app parameters without launching servers, validating Fill50K-style datasets, understanding cldm configs/APIs, and dry-running ControlNet state-dict mappings.
Avoid when: The task is about a different ControlNet implementation, newer ControlNet 1.1-only features, generic Stable Diffusion use without ControlNet-specific controls, or production deployment outside this source checkout.
Useful entry points: `control-net/SKILL.md`, `control-net/sub-skills/annotators-and-preprocessing/SKILL.md`, `control-net/sub-skills/gradio-inference-apps/SKILL.md`, `control-net/sub-skills/training-and-datasets/SKILL.md`, `control-net/sub-skills/model-and-weight-utilities/SKILL.md`.

### `diffusers`

Role: Use `diffusers` for Hugging Face Diffusers tasks: pipeline inference, schedulers, adapters/loaders, training recipes, modular pipelines, conversion helpers, CLI checks, and repo maintenance.
Read when: The request names `diffusers` or asks for package-specific APIs, CLIs, configs, data/model artifacts, error messages, workflows, or repository maintenance that match this project.
Best for: adapters and loaders, conversion and maintenance, modular pipelines, pipelines and inference, schedulers, and training recipes.
Avoid when: another repo skill in this scenario matches the user's task, package, model family, data format, serving backend, or workflow more directly.
Useful entry points: `diffusers/SKILL.md`, `diffusers/sub-skills/adapters-and-loaders/`, `diffusers/sub-skills/conversion-and-maintenance/`, `diffusers/sub-skills/modular-pipelines/`, `diffusers/sub-skills/pipelines-and-inference/`, `diffusers/sub-skills/schedulers/`, `1 more sub-skills`.

### `invokeai`

Role: Use `invokeai` for InvokeAI-specific server configuration, node workflows, workflow queues, and model-management diagnostics.
Read when: The user mentions InvokeAI, invokeai-web, InvokeAI workflow JSON, custom invocations/nodes, session queue, model manager, LoRA/GGUF in InvokeAI, or InvokeAI auth/user CLI.
Best for: Configuring/routing InvokeAI server and API behavior, authoring/debugging InvokeAI nodes, validating workflow/queue payloads, and safely triaging model records/formats without full generation runs.
Avoid when: Use Diffusers for raw Python pipeline APIs, ComfyUI for ComfyUI graph/node workflows, and sd-scripts for LoRA training scripts not involving InvokeAI.
Useful entry points: `invokeai/SKILL.md`, `invokeai/sub-skills/operations-config/SKILL.md`, `invokeai/sub-skills/workflow-nodes/SKILL.md`, `invokeai/sub-skills/workflows-queues/SKILL.md`, `invokeai/sub-skills/model-management/SKILL.md`.

### `sd-scripts`

Role: Use sd-scripts for Stable Diffusion and image-model training, dataset preparation, image generation, LoRA/model utilities, and troubleshooting across SD1/2, SDXL, SD3, FLUX, Lumina, HunyuanImage, and Anima workflows.
Read when: The request names `sd-scripts` or asks for package-specific APIs, CLIs, configs, data/model artifacts, error messages, workflows, or repository maintenance that match this project.
Best for: data preparation, generation, model utilities, and training.
Avoid when: another repo skill in this scenario matches the user's task, package, model family, data format, serving backend, or workflow more directly.
Useful entry points: `sd-scripts/SKILL.md`, `sd-scripts/sub-skills/data-preparation/`, `sd-scripts/sub-skills/generation/`, `sd-scripts/sub-skills/model-utilities/`, `sd-scripts/sub-skills/training/`.

### `stable-diffusion-webui`

Role: Provides self-contained operational guidance for AUTOMATIC1111 Stable Diffusion WebUI workflows across launch/configuration, REST APIs, extensions, assets, and training/postprocessing.
Read when: User mentions stable-diffusion-webui, AUTOMATIC1111, WebUI, launch.py, webui.sh, /sdapi/v1, txt2img/img2img API payloads, alwayson_scripts, checkpoints, VAE, Lora, embeddings, hypernetworks, Extras, textual inversion, or WebUI extensions.
Best for: Running or configuring WebUI, constructing API requests, writing WebUI scripts/extensions, validating model asset layouts, managing Lora/extra networks, and planning WebUI training/postprocessing workflows.
Avoid when: Use Diffusers-specific skills for Python pipeline APIs outside WebUI, ComfyUI-specific skills for node graphs, or generic repository maintenance skills when the task is only source editing without WebUI domain behavior.
Useful entry points: `stable-diffusion-webui/SKILL.md`, `stable-diffusion-webui/sub-skills/launch-and-config/SKILL.md`, `stable-diffusion-webui/sub-skills/api-automation/SKILL.md`, `stable-diffusion-webui/sub-skills/assets-and-models/SKILL.md`, `stable-diffusion-webui/sub-skills/extension-scripting/SKILL.md`, `stable-diffusion-webui/sub-skills/training-and-postprocessing/SKILL.md`.

<!-- SKILLQED_SCENARIO:image-generation-and-lora-training-workflows:END -->

## How To Choose

Choose Diffusers for Python pipeline/model APIs, ComfyUI for graph nodes and server workflows, and sd-scripts for Stable Diffusion LoRA training scripts. Choose `comfy-ui` when the request names `comfy-ui`, centers on Use ComfyUI as a modular AI content-creation engine: launch and automate the server, submit API workflows, validate graph JSON, author custom nodes, and configure model paths/backends, uses its APIs or CLIs, references its configs/artifacts/errors, or asks for repository workflows in image generation and lora training workflows. Choose `control-net` when the request depends on this repository's ControlNet 1.0 scripts, configs, detector wrappers, training tutorials, or checkpoint utilities; choose Diffusers or other image-generation repo skills for generic Stable Diffusion pipelines or unrelated LoRA training frameworks. Choose `diffusers` when the request names `diffusers`, centers on Hugging Face Diffusers tasks: pipeline inference, schedulers, adapters/loaders, training recipes, modular pipelines, conversion helpers, CLI checks, and repo maintenance, uses its APIs or CLIs, references its configs/artifacts/errors, or asks for repository workflows in image generation and lora training workflows. Choose `stable-diffusion-webui` when the practical surface is AUTOMATIC1111 Stable Diffusion WebUI.
