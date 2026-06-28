# LLM Fine-Tuning, Training, and Serving Workflows

## When To Read

Transformers model usage, local generation, fine-tuning, serving CLIs, PEFT adapters, LlamaFactory/Axolotl/ms-swift training, vLLM/SGLang/LMDeploy serving, BentoML model services, and LLM deployment.

## Repo Skill Options

<!-- DISCO_SCENARIO:llm-finetuning-training-serving-workflows:START -->
### `accelerate`

Role: Use Hugging Face Accelerate for PyTorch training-loop migration, distributed launch/configuration, DeepSpeed/FSDP/TPU backend setup, big-model inference/offload, checkpointing, tracking, and troubleshooting.
Read when: The request names `accelerate` or asks for package-specific APIs, CLIs, configs, data/model artifacts, error messages, workflows, or repository maintenance that match this project.
Best for: big model inference, checkpointing and tracking, configuration and cli, distributed training backends, and training loop integration.
Avoid when: another repo skill in this scenario matches the user's task, package, model family, data format, serving backend, or workflow more directly.
Useful entry points: `accelerate/SKILL.md`, `accelerate/sub-skills/big-model-inference/`, `accelerate/sub-skills/checkpointing-and-tracking/`, `accelerate/sub-skills/configuration-and-cli/`, `accelerate/sub-skills/distributed-training-backends/`, `accelerate/sub-skills/training-loop-integration/`.

### `axolotl`

Role: Provides Axolotl-specific routing, config recipes, safe static helpers, and troubleshooting for config-driven LLM training workflows.
Read when: axolotl, axolotl train, axolotl preprocess, config.yaml, chat_template, LoRA, QLoRA, DPO, KTO, ORPO, GRPO, EBFT, vllm-serve, DeepSpeed, FSDP, config-schema, agent-docs.
Best for: Writing or debugging Axolotl YAML configs; choosing training/alignment methods; checking datasets and reward functions; selecting adapters/models; constructing CLI commands; triaging distributed/performance issues.
Avoid when: Task is about a different training framework, generic PyTorch/HuggingFace code outside Axolotl, or paper reproduction unrelated to Axolotl.
Useful entry points: `axolotl/SKILL.md`, `axolotl/sub-skills/data-and-configs/SKILL.md`, `axolotl/sub-skills/sft-and-pretraining/SKILL.md`, `axolotl/sub-skills/preference-tuning/SKILL.md`, `axolotl/sub-skills/rl-and-rewards/SKILL.md`, `axolotl/sub-skills/model-loading-and-adapters/SKILL.md`, `axolotl/sub-skills/distributed-and-performance/SKILL.md`, `axolotl/sub-skills/cli-and-operations/SKILL.md`.

### `bentoml`

Role: Use BentoML to author model-serving Services, build and containerize Bentos, run HTTP/gRPC servers and clients, manage models, operate the CLI and BentoCloud, and configure observability or production runtime behavior.
Read when: The request names `bentoml` or asks for package-specific APIs, CLIs, configs, data/model artifacts, error messages, workflows, or repository maintenance that match this project.
Best for: cli and cloud, model management, observability and operations, packaging and containerization, service authoring, and serving and clients.
Avoid when: another repo skill in this scenario matches the user's task, package, model family, data format, serving backend, or workflow more directly.
Useful entry points: `bentoml/SKILL.md`, `bentoml/sub-skills/cli-and-cloud/`, `bentoml/sub-skills/model-management/`, `bentoml/sub-skills/observability-and-operations/`, `bentoml/sub-skills/packaging-and-containerization/`, `bentoml/sub-skills/service-authoring/`, `1 more sub-skills`.

### `bitsandbytes`

Role: Use bitsandbytes for k-bit PyTorch quantization, Hugging Face quantized model loading, 8-bit and paged optimizers, direct quantized layers/functions, and backend installation diagnostics.
Read when: The request names `bitsandbytes` or asks for package-specific APIs, CLIs, configs, data/model artifacts, error messages, workflows, or repository maintenance that match this project.
Best for: installation diagnostics, optimizers training, quantized modules functions, and transformers integrations.
Avoid when: another repo skill in this scenario matches the user's task, package, model family, data format, serving backend, or workflow more directly.
Useful entry points: `bitsandbytes/SKILL.md`, `bitsandbytes/sub-skills/installation-diagnostics/`, `bitsandbytes/sub-skills/optimizers-training/`, `bitsandbytes/sub-skills/quantized-modules-functions/`, `bitsandbytes/sub-skills/transformers-integrations/`.

### `datasets`

Role: Use `datasets` when working with Hugging Face Datasets: loading local or Hub datasets, defining Features schemas, processing/streaming datasets, converting formats, sharing to the Hub, managing cache/offline behavior, or using.
Read when: The request names `datasets` or asks for package-specific APIs, CLIs, configs, data/model artifacts, error messages, workflows, or repository maintenance that match this project.
Best for: features formats, loading local hub, processing streaming, and sharing cli cache.
Avoid when: another repo skill in this scenario matches the user's task, package, model family, data format, serving backend, or workflow more directly.
Useful entry points: `datasets/SKILL.md`, `datasets/sub-skills/features-formats/`, `datasets/sub-skills/loading-local-hub/`, `datasets/sub-skills/processing-streaming/`, `datasets/sub-skills/sharing-cli-cache/`.

### `deepspeed`

Role: Use DeepSpeed for distributed training, inference acceleration, ZeRO configuration, parallelism/MoE design, profiling, autotuning, and operational diagnostics.
Read when: The request names `deepspeed` or asks for package-specific APIs, CLIs, configs, data/model artifacts, error messages, workflows, or repository maintenance that match this project.
Best for: inference injection, ops tooling, parallelism moe, and training config.
Avoid when: another repo skill in this scenario matches the user's task, package, model family, data format, serving backend, or workflow more directly.
Useful entry points: `deepspeed/SKILL.md`, `deepspeed/sub-skills/inference-injection/`, `deepspeed/sub-skills/ops-tooling/`, `deepspeed/sub-skills/parallelism-moe/`, `deepspeed/sub-skills/training-config/`.

### `diffusers`

Role: Use `diffusers` for Hugging Face Diffusers tasks: pipeline inference, schedulers, adapters/loaders, training recipes, modular pipelines, conversion helpers, CLI checks, and repo maintenance.
Read when: The request names `diffusers` or asks for package-specific APIs, CLIs, configs, data/model artifacts, error messages, workflows, or repository maintenance that match this project.
Best for: adapters and loaders, conversion and maintenance, modular pipelines, pipelines and inference, schedulers, and training recipes.
Avoid when: another repo skill in this scenario matches the user's task, package, model family, data format, serving backend, or workflow more directly.
Useful entry points: `diffusers/SKILL.md`, `diffusers/sub-skills/adapters-and-loaders/`, `diffusers/sub-skills/conversion-and-maintenance/`, `diffusers/sub-skills/modular-pipelines/`, `diffusers/sub-skills/pipelines-and-inference/`, `diffusers/sub-skills/schedulers/`, `1 more sub-skills`.

### `litgpt`

Role: Provides self-contained LitGPT routing, CLI/API recipes, validation helpers, and troubleshooting for common local LLM workflows.
Read when: litgpt, LitGPT, LLM.load, litgpt generate, litgpt chat, litgpt finetune, LoRA, QLoRA, pretrain, convert_to_litgpt, merge_lora, litgpt evaluate, litgpt serve, LitServe, checkpoint_dir, model_config.yaml, lit_model.pth.
Best for: Planning and validating LitGPT CLI/Python workflows, checkpoint conversion and layout triage, custom training data checks, optional dependency checks, and safe preflights before expensive model operations.
Avoid when: The task is about a different LLM framework, generic PyTorch modeling unrelated to LitGPT, or production server operations that do not use LitGPT/LitServe.
Useful entry points: `litgpt/SKILL.md`, `litgpt/sub-skills/inference-chat/SKILL.md`, `litgpt/sub-skills/training-data/SKILL.md`, `litgpt/sub-skills/checkpoint-conversion/SKILL.md`, `litgpt/sub-skills/evaluation-serving/SKILL.md`.

### `llama-factory`

Role: Use for LlamaFactory repository workflows: training configs, dataset/template preparation, model loading/export, inference/API/Web UI operations, and experimental USE_V1 flows.
Read when: The request names `llama-factory` or asks for package-specific APIs, CLIs, configs, data/model artifacts, error messages, workflows, or repository maintenance that match this project.
Best for: data and templates, inference and serving, model loading and export, training and configs, v1 experimental, and webui and ops.
Avoid when: another repo skill in this scenario matches the user's task, package, model family, data format, serving backend, or workflow more directly.
Useful entry points: `llama-factory/SKILL.md`, `llama-factory/sub-skills/data-and-templates/`, `llama-factory/sub-skills/inference-and-serving/`, `llama-factory/sub-skills/model-loading-and-export/`, `llama-factory/sub-skills/training-and-configs/`, `llama-factory/sub-skills/v1-experimental/`, `1 more sub-skills`.

### `lmdeploy`

Role: Provides repo-specific guidance for running, serving, quantizing, tuning, and extending LMDeploy workflows.
Read when: User asks about lmdeploy pipeline, lmdeploy chat, lmdeploy serve api_server, OpenAI/Responses/Anthropic endpoints, lmdeploy lite, AWQ/GPTQ/SmoothQuant, VLM image/video/audio inputs, _turbomind, cache_max_entry_count, PytorchEngineConfig, TurbomindEngineConfig, or adding a new LMDeploy PyTorch model.
Best for: Building correct LMDeploy commands and Python snippets, selecting the right sub-skill for inference/serving/VLM/quantization/backend tasks, diagnosing install/backend/runtime errors, and planning safe validation without unnecessary model downloads.
Avoid when: The task is generic PyTorch/Transformers usage without LMDeploy APIs, unrelated OpenAI client work against a different server, or broad GPU benchmarking not tied to LMDeploy behavior.
Useful entry points: `lmdeploy/SKILL.md`, `lmdeploy/sub-skills/pipeline-inference/SKILL.md`, `lmdeploy/sub-skills/serving-apis/SKILL.md`, `lmdeploy/sub-skills/vision-language/SKILL.md`, `lmdeploy/sub-skills/quantization/SKILL.md`, `lmdeploy/sub-skills/backend-extension/SKILL.md`.

### `ms-swift`

Role: Provides ms-swift-specific routing and command/reference guidance for model training workflows.
Read when: ms-swift, swift sft, swift pt, LoRA, QLoRA, ModelScope SWIFT, training config, adapters, checkpoints, multimodal training. swift infer, swift app, swift deploy, vllm, sglang, lmdeploy, InferRequest, RequestConfig, adapters, served_model_name, OpenAI-compatible server. swift export, swift merge-lora, swift eval, EvalScope, AWQ, GPTQ, FP8, BNB, push_to_hub, hub_model_id, eval_backend.
Best for: Building and validating `swift sft` or `swift pt` commands, training configs, checkpoint handoffs, and memory/debug choices. Choosing `transformers` vs accelerated backends, building inference/deploy commands, smoke-testing local servers, and debugging multimodal serving. Choosing export/merge/quantization paths, checking custom eval datasets, and diagnosing missing EvalScope or quantization dependencies.
Avoid when: The task is about generic PyTorch training outside ms-swift or only about serving an already exported model. The task is only about training data schema or generic OpenAI API usage unrelated to ms-swift deployment. The task only asks for live serving or generic benchmark design outside ms-swift/EvalScope.
Useful entry points: `ms-swift/SKILL.md`, `ms-swift/sub-skills/training/SKILL.md`, `ms-swift/sub-skills/inference-deployment/SKILL.md`, `ms-swift/sub-skills/export-evaluation/SKILL.md`.

### `peft`

Role: Use PEFT for parameter-efficient fine-tuning adapters, LoRA and quantized workflows, prompt and soft methods, specialized tuners, save/load/merge operations, training integrations, and PEFT repository development.
Read when: The request names `peft` or asks for package-specific APIs, CLIs, configs, data/model artifacts, error messages, workflows, or repository maintenance that match this project.
Best for: adapter core, lora and quantization, prompt and soft methods, repo development, save load merge, and 2 other focused workflows.
Avoid when: another repo skill in this scenario matches the user's task, package, model family, data format, serving backend, or workflow more directly.
Useful entry points: `peft/SKILL.md`, `peft/sub-skills/adapter-core/`, `peft/sub-skills/lora-and-quantization/`, `peft/sub-skills/prompt-and-soft-methods/`, `peft/sub-skills/repo-development/`, `peft/sub-skills/save-load-merge/`, `2 more sub-skills`.

### `sentence-transformers`

Role: Use Sentence Transformers for dense embeddings, semantic search, CrossEncoder reranking, SparseEncoder search, evaluation/training planning, and ONNX/OpenVINO backend optimization. Routes natural language tasks to focused.
Read when: The request names `sentence-transformers` or asks for package-specific APIs, CLIs, configs, data/model artifacts, error messages, workflows, or repository maintenance that match this project.
Best for: backend export optimization, embeddings and similarity, evaluation and training, reranking cross encoder, retrieval and utilities, and sparse encoder search.
Avoid when: another repo skill in this scenario matches the user's task, package, model family, data format, serving backend, or workflow more directly.
Useful entry points: `sentence-transformers/SKILL.md`, `sentence-transformers/sub-skills/backend-export-optimization/`, `sentence-transformers/sub-skills/embeddings-and-similarity/`, `sentence-transformers/sub-skills/evaluation-and-training/`, `sentence-transformers/sub-skills/reranking-cross-encoder/`, `sentence-transformers/sub-skills/retrieval-and-utilities/`, `1 more sub-skills`.

### `sglang`

Role: Use SGLang for high-throughput LLM and VLM serving, OpenAI-compatible APIs, frontend language programs, runtime/server arguments, benchmarking, profiling, model/kernel extension, and SGLang repository development.
Read when: The request names `sglang` or asks for package-specific APIs, CLIs, configs, data/model artifacts, error messages, workflows, or repository maintenance that match this project.
Best for: benchmarking profiling, frontend programming, model kernel extension, repo development, and serving runtime.
Avoid when: another repo skill in this scenario matches the user's task, package, model family, data format, serving backend, or workflow more directly.
Useful entry points: `sglang/SKILL.md`, `sglang/sub-skills/benchmarking-profiling/`, `sglang/sub-skills/frontend-programming/`, `sglang/sub-skills/model-kernel-extension/`, `sglang/sub-skills/repo-development/`, `sglang/sub-skills/serving-runtime/`.

### `torchtune`

Role: Covers torchtune model/dataset/config wiring plus generation, Eleuther evaluation, quantization, and adapter/checkpoint routing after training.
Read when: The request names torchtune models, tokenizers, adapters, generation, Eleuther evaluation, quantize, `FullModelTorchTuneCheckpointer`, or checkpoint output folders.
Best for: Using torchtune-specific model builders, PEFT modules, data transforms, generation/evaluation/quantization recipes, and checkpoint compatibility guidance.
Avoid when: The task is serving an OpenAI-compatible endpoint, using vLLM/SGLang directly, or generic Transformers generation with no torchtune config/checkpoint layer.
Useful entry points: `torchtune/sub-skills/models-and-modules/SKILL.md`, `torchtune/sub-skills/inference-evaluation-quantization/SKILL.md`, `torchtune/sub-skills/data-and-datasets/SKILL.md`.

### `transformers`

Role: Use and extend Hugging Face Transformers for inference, generation, training, tokenizers/processors, serving CLI, quantization/integrations, and contributor workflows.
Read when: The request names `transformers` or asks for package-specific APIs, CLIs, configs, data/model artifacts, error messages, workflows, or repository maintenance that match this project.
Best for: generation, inference pipelines, model extension, quantization integrations, serving cli, and 2 other focused workflows.
Avoid when: another repo skill in this scenario matches the user's task, package, model family, data format, serving backend, or workflow more directly.
Useful entry points: `transformers/SKILL.md`, `transformers/sub-skills/generation/`, `transformers/sub-skills/inference-pipelines/`, `transformers/sub-skills/model-extension/`, `transformers/sub-skills/quantization-integrations/`, `transformers/sub-skills/serving-cli/`, `2 more sub-skills`.

### `trl`

Role: Use and modify TRL, the Hugging Face Transformers Reinforcement Learning library for post-training, CLI workflows, data/reward utilities, scaling backends, experimental environments, and repo development.
Read when: The request names `trl` or asks for package-specific APIs, CLIs, configs, data/model artifacts, error messages, workflows, or repository maintenance that match this project.
Best for: cli and configs, core training, data and rewards, experimental and environments, repo development, and scaling and backends.
Avoid when: another repo skill in this scenario matches the user's task, package, model family, data format, serving backend, or workflow more directly.
Useful entry points: `trl/SKILL.md`, `trl/sub-skills/cli-and-configs/`, `trl/sub-skills/core-training/`, `trl/sub-skills/data-and-rewards/`, `trl/sub-skills/experimental-and-environments/`, `trl/sub-skills/repo-development/`, `1 more sub-skills`.

### `unsloth`

Role: Provides repo-specific routing and self-contained workflows for Unsloth Core APIs, CLI commands, Studio runtime, and checkpoint export.
Read when: User says unsloth, FastLanguageModel, FastVisionModel, get_peft_model, unsloth train, unsloth studio, unsloth run, unsloth connect, GGUF export, Ollama Modelfile, Studio API, Cloudflare secure tunnel, RAG, or llama.cpp runtime.
Best for: Planning and troubleshooting Unsloth finetuning scripts, CLI dry-runs, Studio launch/connect/runtime behavior, and safe checkpoint export or GGUF conversion preflights.
Avoid when: The task is generic Hugging Face Transformers, generic TRL/PEFT use without Unsloth, unrelated model evaluation, or running long training/export jobs without explicit approval.
Useful entry points: `unsloth/SKILL.md`, `unsloth/sub-skills/core-training/SKILL.md`, `unsloth/sub-skills/cli-workflows/SKILL.md`, `unsloth/sub-skills/model-export/SKILL.md`, `unsloth/sub-skills/studio-runtime/SKILL.md`.

### `vllm`

Role: Route vLLM tasks across offline inference, OpenAI-compatible serving, structured/tool/reasoning, multimodal/LoRA/pooling, and deployment/performance workflows.
Read when: The request names `vllm` or asks for package-specific APIs, CLIs, configs, data/model artifacts, error messages, workflows, or repository maintenance that match this project.
Best for: deployment performance, modalities adapters pooling, offline inference, openai serving, and structured tool reasoning.
Avoid when: another repo skill in this scenario matches the user's task, package, model family, data format, serving backend, or workflow more directly.
Useful entry points: `vllm/SKILL.md`, `vllm/sub-skills/deployment-performance/`, `vllm/sub-skills/modalities-adapters-pooling/`, `vllm/sub-skills/offline-inference/`, `vllm/sub-skills/openai-serving/`, `vllm/sub-skills/structured-tool-reasoning/`.

<!-- DISCO_SCENARIO:llm-finetuning-training-serving-workflows:END -->

## How To Choose

Choose by primary surface: Transformers for core model/tokenizer/trainer APIs, PEFT/bitsandbytes for adapters or quantization, Axolotl/LlamaFactory/ms-swift/Unsloth for training frameworks, vLLM/SGLang/LMDeploy for serving, BentoML for packaging services, and LitGPT for local lightweight workflows. Choose `accelerate` when the request names `accelerate`, centers on PyTorch training-loop migration, distributed launch/configuration, DeepSpeed/FSDP/TPU backend setup, big-model inference/offload, checkpointing, tracking, and troubleshooting, uses its APIs or CLIs, references its configs/artifacts/errors, or asks for repository workflows in llm finetuning training serving workflows. Choose `axolotl` when Axolotl is named or when the task involves Axolotl-specific YAML keys, CLI commands, prompt strategies, trainer methods, model adapter settings, or distributed launch patterns. Use generic ML skills only after Axolotl-specific config and CLI behavior are ruled out. Choose `bentoml` when the request names `bentoml`, centers on Use BentoML to author model-serving Services, build and containerize Bentos, run HTTP/gRPC servers and clients, manage models, operate the CLI and BentoCloud, and configure observability or production runtime behavior. Choose `litgpt` for LitGPT-specific commands, APIs, checkpoint layouts, recipes, and errors.
