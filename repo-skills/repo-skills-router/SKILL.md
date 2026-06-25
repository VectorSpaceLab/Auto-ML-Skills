---
name: repo-skills-router
description: "Use this two-layer router for imported repository skills. Read it when another agent needs to choose which repo-specific skill should inform a user request, when routing among similar repo skills, or after importing a repo skill to classify it by practical usage scenario and maintain selection guidance."
---

# Repo Skills Router

## Purpose

Use this skill as the maintained router for repo-specific skills imported into
SkillQED's managed skill library. It helps another agent pick a relevant repo
skill as reference for a user request without reading every imported skill.

The router uses two-layer progressive disclosure:

1. `SKILL.md` gives a compact first-pass map from practical repository usage
   scenarios to scenario pages.
2. Each `references/scenarios/<scenario>.md` page explains which repo skills
   belong to that scenario, what each one is for, how similar repo skills differ,
   and how to choose among them.

## How To Route

1. Scan the usage scenario quick map below for the user's likely task family.
2. Read only the relevant scenario page listed in
   [references/usage-scenarios.md](references/usage-scenarios.md).
3. On that scenario page, compare the candidate repo skills by role,
   non-fit cases, overlap notes, and selection guideline.
4. Read the selected repo skill's own `SKILL.md` before relying on it.
5. If no scenario fits, fall back to the available skill descriptions, project
   context, or repository evidence. Do not invent a router entry.

Use this router only for selection. A router entry is not a substitute for the
selected repo skill's detailed instructions.

## Maintenance After Skill Import

When a verified repo-specific skill is imported after user approval, update the
live SkillQED router by running the managed updater script inside the global
SkillQED import lock instead of editing router Markdown by hand. See
[references/maintenance.md](references/maintenance.md).

## Usage Scenario Quick Map

Keep this section short. It should route a future agent to the right scenario
page, not document the repo skills in full.

<!-- SKILLQED_REPO_SKILLS_ROUTER_SCENARIOS:START -->
| Usage scenario | When to read | Scenario page | Representative repo skills |
| --- | --- | --- | --- |
| `agent-frameworks-tooling-and-sandboxed-llm-workflows` | LLM agent frameworks, browser automation agents, tool calling, graph/state runtimes, hosted or sandbox execution, MCP, CLIs, and production agent operations. | `references/scenarios/agent-frameworks-tooling-and-sandboxed-llm-workflows.md` | `adk-python`, `autogen`, `browser-use`, `camel-ai`, `crewai`, `haystack`, `langchain`, `langgraph`, `litellm`, `llama-index`, `mcp-agent`, `openai-agents-python`, `pydantic-ai`, `smolagents` |
| `ai-gateway-and-llm-provider-integration` | OpenAI-compatible provider routing, gateway/proxy servers, model endpoint mapping, virtual keys, spend controls, pass-through APIs, and provider SDK troubleshooting. | `references/scenarios/ai-gateway-and-llm-provider-integration.md` | `litellm` |
| `ai-memory-sdks-and-app-integration` | Persistent memory SDKs, memory search/update/delete flows, self-hosted memory services, memory CLIs, and agent memory integrations. | `references/scenarios/ai-memory-sdks-and-app-integration.md` | `mem0` |
| `ai-pipelines-workflows-and-rag` | Pipeline and workflow frameworks that combine embeddings, LLMs, agents, task chains, services, and RAG orchestration. | `references/scenarios/ai-pipelines-workflows-and-rag.md` | `txtai` |
| `bulk-rna-seq-differential-expression-analysis` | Bulk RNA-seq raw-count differential expression analysis, DESeq2-like Python workflows, count/metadata validation, contrasts, Wald tests, LFC shrinkage, VST, and PyDESeq2 troubleshooting. | `references/scenarios/bulk-rna-seq-differential-expression-analysis.md` | `pydeseq2` |
| `computer-vision-modeling-and-augmentation` | Image augmentation, PIL/Pillow operations, vision datasets/transforms, classification and detection models, segmentation, YOLO/SAM/OpenMMLab workflows, and model export. | `references/scenarios/computer-vision-modeling-and-augmentation.md` | `albumentations`, `detectron2`, `grounding-dino`, `mmdetection`, `mmsegmentation`, `open-clip`, `pillow`, `segment-anything`, `tiatoolbox`, `timm`, `torchvision`, `ultralytics` |
| `data-model-customization` | Dataset schemas, message rows, column mappings, model/template registries, custom datasets/models/templates, and package-specific data customization workflows. | `references/scenarios/data-model-customization.md` | `ms-swift`, `torchtune` |
| `data-orchestration-and-parallel-computing` | Workflow engines, DAGs, assets, Snakefiles, lazy/parallel task graphs, distributed arrays/dataframes, feature stores, cloud compute orchestration, and production data pipelines. | `references/scenarios/data-orchestration-and-parallel-computing.md` | `apache-airflow`, `dagster`, `dask`, `feast`, `hail`, `prefect`, `pytorch-geometric`, `skypilot`, `snakemake` |
| `dataset-processing-evaluation-and-hub-workflows` | Dataset loading, schemas, streaming, format conversion, metric/evaluator modules, benchmark task selection, result caches, data validation, and Hub or CLI workflows. | `references/scenarios/dataset-processing-evaluation-and-hub-workflows.md` | `datasets`, `deepvariant`, `evaluate`, `great-expectations`, `hail`, `mteb` |
| `deep-learning-training-engines` | Tasks about engine-level utilities, runners, hooks, loops, config systems, logging, visualization, and debugging for deep learning training frameworks. | `references/scenarios/deep-learning-training-engines.md` | `mmengine` |
| `distributed-pytorch-training-and-large-model-workflows` | Distributed training loops, launchers, DeepSpeed/FSDP/TPU backends, PyTorch Lightning/Fabric, scalable GNN training, checkpoints, and memory planning. | `references/scenarios/distributed-pytorch-training-and-large-model-workflows.md` | `accelerate`, `deepspeed`, `lightning`, `openfold`, `openrlhf`, `optuna`, `pytorch-geometric`, `torchtune`, `verl` |
| `document-processing-unstructured-data-and-rag-preparation` | Document conversion, partitioning, OCR/table pipelines, Markdown conversion, document elements, chunking, extraction, cleaning, staging, remote document services, and RAG-ready document preparation. | `references/scenarios/document-processing-unstructured-data-and-rag-preparation.md` | `docling`, `marker`, `markitdown`, `unstructured` |
| `embedding-retrieval-rag-workflows` | Embedding models, semantic or sparse search, reranking, vector or graph RAG, retrieval training, corpus indexing, RAG pipelines, vector database clients, and retrieval evaluation. | `references/scenarios/embedding-retrieval-rag-workflows.md` | `beir`, `colbert`, `feast`, `flag-embedding`, `flashrag`, `graphrag`, `haystack`, `lightrag`, `llama-index`, `mteb`, `pyserini`, `qdrant-client`, `ragatouille`, `sentence-transformers`, `splade`, `tevatron`, `txtai` |
| `embodied-ai-simulation` | Embodied AI simulation, navigation/rearrangement tasks, habitat-style configs, datasets, training, HITL apps, and simulator extension registries. | `references/scenarios/embodied-ai-simulation.md` | `habitat-lab` |
| `graph-learning-workflows` | Graph neural network tasks, graph construction, message passing, graph datasets, graph data loaders, graph partitioning, sparse graph operations, and distributed graph training. | `references/scenarios/graph-learning-workflows.md` | `dgl` |
| `image-generation-and-lora-training-workflows` | Stable Diffusion or Diffusers pipelines, ComfyUI node graphs, image generation servers, diffusion schedulers/adapters, dataset TOML, LoRA training, and model utilities. | `references/scenarios/image-generation-and-lora-training-workflows.md` | `comfy-ui`, `control-net`, `diffusers`, `invokeai`, `sd-scripts`, `stable-diffusion-webui` |
| `language-model-evaluation-workflows` | LLM benchmark configuration, evaluation harness runs, OpenCompass configs, task authoring, model backends, result summaries, decontamination, and judge-based evaluation. | `references/scenarios/language-model-evaluation-workflows.md` | `evaluate`, `lm-evaluation-harness`, `opencompass`, `torchtune` |
| `llm-finetuning-training-serving-workflows` | Transformers model usage, local generation, fine-tuning, serving CLIs, PEFT adapters, LlamaFactory/Axolotl/ms-swift training, vLLM/SGLang/LMDeploy serving, BentoML model services, and LLM deployment. | `references/scenarios/llm-finetuning-training-serving-workflows.md` | `accelerate`, `axolotl`, `bentoml`, `bitsandbytes`, `datasets`, `deepspeed`, `diffusers`, `litgpt`, `llama-factory`, `lmdeploy`, `ms-swift`, `peft`, `sentence-transformers`, `sglang`, `torchtune`, `transformers`, `trl`, `unsloth`, `vllm` |
| `llm-post-training-rlhf-workflows` | SFT, DPO, GRPO, PPO, reward models, RLHF data/rewards, rollout engines, post-training configs, LoRA merging, Ray/Megatron distributed RLHF, and preference optimization backends. | `references/scenarios/llm-post-training-rlhf-workflows.md` | `ms-swift`, `openrlhf`, `torchtune`, `trl`, `verl` |
| `materials-science-and-crystal-structure-workflows` | Computational materials, crystal structures, entries and phase stability, Materials Project data, surfaces/interfaces, diffraction/spectra, VASP-oriented pymatgen CLIs, and materials-analysis Python workflows. | `references/scenarios/materials-science-and-crystal-structure-workflows.md` | `pymatgen` |
| `medical-imaging-and-segmentation-workflows` | Medical image transforms, nnU-Net planning/training/inference, MONAI bundles, TorchIO patch workflows, healthcare segmentation, and 3D image augmentation. | `references/scenarios/medical-imaging-and-segmentation-workflows.md` | `antspy`, `dipy`, `monai`, `nnunetv2`, `simpleitk`, `tiatoolbox`, `torchio`, `totalsegmentator` |
| `ml-experiment-tracking-and-mlops-workflows` | Experiment tracking, AutoML/HPO, model registries, artifacts, sweeps, Launch jobs, MLflow projects/models/evaluation, data versioning pipelines, GenAI observability, local serving, and operational MLOps. | `references/scenarios/ml-experiment-tracking-and-mlops-workflows.md` | `autogluon`, `bentoml`, `dvc`, `mlflow`, `nni`, `optuna`, `wandb` |
| `molecular-ml-drug-discovery-and-chemistry-workflows` | Cheminformatics, molecule processing, molecular property prediction, featurization, MoleculeNet, docking, molecular simulation, force fields, conformers, reactions, retrosynthesis, and chemistry model training. | `references/scenarios/molecular-ml-drug-discovery-and-chemistry-workflows.md` | `aizynthfinder`, `chemprop`, `datamol`, `deepchem`, `diffdock`, `mdanalysis`, `openmm`, `rdkit`, `reinvent4` |
| `multimodal-training-audio-naflex` | OpenCLIP training commands, open_clip_train, CSV/WebDataset data, task-era TrainingTask wrappers, FSDP, torch.compile, CLAP audio, NaFlex, GenLIP, or GenLAP. | `references/scenarios/multimodal-training-audio-naflex.md` | `open-clip` |
| `protein-structure-prediction-and-design-workflows` | AlphaFold, ColabFold, Boltz, Chai-1, ESM, ProteinMPNN, RFdiffusion, MSA generation, structure prediction outputs, protein backbone generation, binder design, and sequence design. | `references/scenarios/protein-structure-prediction-and-design-workflows.md` | `alphafold3`, `boltz`, `chai-lab`, `colabfold`, `esm`, `openfold`, `protein-mpnn`, `protenix`, `rfdiffusion` |
| `python-ai-api-services-and-deployment` | Python AI packages exposed as APIs, FastAPI services, OpenAI-compatible endpoints, MCP servers, secured services, custom routes, clusters, consoles, Docker/cloud/serverless deployment, or observability targets. | `references/scenarios/python-ai-api-services-and-deployment.md` | `stable-diffusion-webui`, `txtai` |
| `python-repository-maintenance` | Tasks that edit, review, test, document, package, or maintain Python source repositories rather than using them only as libraries. | `references/scenarios/python-repository-maintenance.md` | `cleanrl`, `crewai`, `prefect`, `pydantic-ai`, `skypilot`, `stable-diffusion-webui` |
| `reinforcement-learning-workflows` | Gymnasium environments, Stable-Baselines3 algorithms, RL vectorization, policies, evaluation, experiment scripts, replay buffers, collectors, action masks, multi-agent RL environments, and PPO-family rollout-agent training. | `references/scenarios/reinforcement-learning-workflows.md` | `cleanrl`, `openrlhf`, `pettingzoo`, `stable-baselines3`, `tianshou`, `trl`, `verl` |
| `scientific-python-data-workflows` | NumPy-style array analysis combined with molecular simulation trajectories, coordinate transformations, or per-frame scientific computations in Python. | `references/scenarios/scientific-python-data-workflows.md` | `mdanalysis` |
| `single-cell-omics-and-scanpy-workflows` | AnnData/MuData setup, Scanpy preprocessing/QC, graph analysis, marker genes, probabilistic scvi-tools models, multimodal/spatial omics, and single-cell plotting/reporting. | `references/scenarios/single-cell-omics-and-scanpy-workflows.md` | `anndata`, `pyscenic`, `scanpy`, `scvi-tools`, `squidpy` |
<!-- SKILLQED_REPO_SKILLS_ROUTER_SCENARIOS:END -->
