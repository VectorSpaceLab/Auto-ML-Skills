# Usage Scenarios

## Purpose

Use this file after the top-level router identifies a likely task family. It
maps practical repository usage scenarios to the scenario pages that contain
repo-specific skill roles, differences, and selection guidance.

## Scenario Table

Add scenarios only when at least one imported repo skill belongs there. Prefer
user-facing task families over implementation taxonomy. A repo skill may appear
in multiple scenarios when it genuinely supports multiple kinds of requests.

<!-- SKILLQED_REPO_SKILLS_ROUTER_SCENARIOS:START -->
| Usage scenario | When to read | Scenario page | Representative repo skills |
| --- | --- | --- | --- |
| `agent-frameworks-tooling-and-sandboxed-llm-workflows` | LLM agent frameworks, browser automation agents, tool calling, graph/state runtimes, hosted or sandbox execution, MCP, CLIs, and production agent operations. | `scenarios/agent-frameworks-tooling-and-sandboxed-llm-workflows.md` | `adk-python`, `autogen`, `browser-use`, `camel-ai`, `crewai`, `haystack`, `langchain`, `langgraph`, `litellm`, `llama-index`, `mcp-agent`, `openai-agents-python`, `pydantic-ai`, `smolagents` |
| `ai-gateway-and-llm-provider-integration` | OpenAI-compatible provider routing, gateway/proxy servers, model endpoint mapping, virtual keys, spend controls, pass-through APIs, and provider SDK troubleshooting. | `scenarios/ai-gateway-and-llm-provider-integration.md` | `litellm` |
| `ai-memory-sdks-and-app-integration` | Persistent memory SDKs, memory search/update/delete flows, self-hosted memory services, memory CLIs, and agent memory integrations. | `scenarios/ai-memory-sdks-and-app-integration.md` | `mem0` |
| `ai-pipelines-workflows-and-rag` | Pipeline and workflow frameworks that combine embeddings, LLMs, agents, task chains, services, and RAG orchestration. | `scenarios/ai-pipelines-workflows-and-rag.md` | `txtai` |
| `bulk-rna-seq-differential-expression-analysis` | Bulk RNA-seq raw-count differential expression analysis, DESeq2-like Python workflows, count/metadata validation, contrasts, Wald tests, LFC shrinkage, VST, and PyDESeq2 troubleshooting. | `scenarios/bulk-rna-seq-differential-expression-analysis.md` | `pydeseq2` |
| `computer-vision-modeling-and-augmentation` | Image augmentation, PIL/Pillow operations, vision datasets/transforms, classification and detection models, segmentation, YOLO/SAM/OpenMMLab workflows, and model export. | `scenarios/computer-vision-modeling-and-augmentation.md` | `albumentations`, `detectron2`, `grounding-dino`, `mmdetection`, `mmsegmentation`, `open-clip`, `pillow`, `segment-anything`, `tiatoolbox`, `timm`, `torchvision`, `ultralytics` |
| `data-model-customization` | Dataset schemas, message rows, column mappings, model/template registries, custom datasets/models/templates, and package-specific data customization workflows. | `scenarios/data-model-customization.md` | `ms-swift`, `torchtune` |
| `data-orchestration-and-parallel-computing` | Workflow engines, DAGs, assets, Snakefiles, lazy/parallel task graphs, distributed arrays/dataframes, feature stores, cloud compute orchestration, and production data pipelines. | `scenarios/data-orchestration-and-parallel-computing.md` | `apache-airflow`, `dagster`, `dask`, `feast`, `hail`, `prefect`, `pytorch-geometric`, `skypilot`, `snakemake` |
| `dataset-processing-evaluation-and-hub-workflows` | Dataset loading, schemas, streaming, format conversion, metric/evaluator modules, benchmark task selection, result caches, data validation, and Hub or CLI workflows. | `scenarios/dataset-processing-evaluation-and-hub-workflows.md` | `datasets`, `deepvariant`, `evaluate`, `great-expectations`, `hail`, `mteb` |
| `deep-learning-training-engines` | Tasks about engine-level utilities, runners, hooks, loops, config systems, logging, visualization, and debugging for deep learning training frameworks. | `scenarios/deep-learning-training-engines.md` | `mmengine` |
| `distributed-pytorch-training-and-large-model-workflows` | Distributed training loops, launchers, DeepSpeed/FSDP/TPU backends, PyTorch Lightning/Fabric, scalable GNN training, checkpoints, and memory planning. | `scenarios/distributed-pytorch-training-and-large-model-workflows.md` | `accelerate`, `deepspeed`, `lightning`, `openfold`, `openrlhf`, `optuna`, `pytorch-geometric`, `torchtune`, `verl` |
| `document-processing-unstructured-data-and-rag-preparation` | Document conversion, partitioning, OCR/table pipelines, Markdown conversion, document elements, chunking, extraction, cleaning, staging, remote document services, and RAG-ready document preparation. | `scenarios/document-processing-unstructured-data-and-rag-preparation.md` | `docling`, `marker`, `markitdown`, `unstructured` |
| `embedding-retrieval-rag-workflows` | Embedding models, semantic or sparse search, reranking, vector or graph RAG, retrieval training, corpus indexing, RAG pipelines, vector database clients, and retrieval evaluation. | `scenarios/embedding-retrieval-rag-workflows.md` | `beir`, `colbert`, `feast`, `flag-embedding`, `flashrag`, `graphrag`, `haystack`, `lightrag`, `llama-index`, `mteb`, `pyserini`, `qdrant-client`, `ragatouille`, `sentence-transformers`, `splade`, `tevatron`, `txtai` |
| `embodied-ai-simulation` | Embodied AI simulation, navigation/rearrangement tasks, habitat-style configs, datasets, training, HITL apps, and simulator extension registries. | `scenarios/embodied-ai-simulation.md` | `habitat-lab` |
| `graph-learning-workflows` | Graph neural network tasks, graph construction, message passing, graph datasets, graph data loaders, graph partitioning, sparse graph operations, and distributed graph training. | `scenarios/graph-learning-workflows.md` | `dgl` |
| `image-generation-and-lora-training-workflows` | Stable Diffusion or Diffusers pipelines, ComfyUI node graphs, image generation servers, diffusion schedulers/adapters, dataset TOML, LoRA training, and model utilities. | `scenarios/image-generation-and-lora-training-workflows.md` | `comfy-ui`, `control-net`, `diffusers`, `invokeai`, `sd-scripts`, `stable-diffusion-webui` |
| `language-model-evaluation-workflows` | LLM benchmark configuration, evaluation harness runs, OpenCompass configs, task authoring, model backends, result summaries, decontamination, and judge-based evaluation. | `scenarios/language-model-evaluation-workflows.md` | `evaluate`, `lm-evaluation-harness`, `opencompass`, `torchtune` |
| `llm-finetuning-training-serving-workflows` | Transformers model usage, local generation, fine-tuning, serving CLIs, PEFT adapters, LlamaFactory/Axolotl/ms-swift training, vLLM/SGLang/LMDeploy serving, BentoML model services, and LLM deployment. | `scenarios/llm-finetuning-training-serving-workflows.md` | `accelerate`, `axolotl`, `bentoml`, `bitsandbytes`, `datasets`, `deepspeed`, `diffusers`, `litgpt`, `llama-factory`, `lmdeploy`, `ms-swift`, `peft`, `sentence-transformers`, `sglang`, `torchtune`, `transformers`, `trl`, `unsloth`, `vllm` |
| `llm-post-training-rlhf-workflows` | SFT, DPO, GRPO, PPO, reward models, RLHF data/rewards, rollout engines, post-training configs, LoRA merging, Ray/Megatron distributed RLHF, and preference optimization backends. | `scenarios/llm-post-training-rlhf-workflows.md` | `ms-swift`, `openrlhf`, `torchtune`, `trl`, `verl` |
| `materials-science-and-crystal-structure-workflows` | Computational materials, crystal structures, entries and phase stability, Materials Project data, surfaces/interfaces, diffraction/spectra, VASP-oriented pymatgen CLIs, and materials-analysis Python workflows. | `scenarios/materials-science-and-crystal-structure-workflows.md` | `pymatgen` |
| `medical-imaging-and-segmentation-workflows` | Medical image transforms, nnU-Net planning/training/inference, MONAI bundles, TorchIO patch workflows, healthcare segmentation, and 3D image augmentation. | `scenarios/medical-imaging-and-segmentation-workflows.md` | `antspy`, `dipy`, `monai`, `nnunetv2`, `simpleitk`, `tiatoolbox`, `torchio`, `totalsegmentator` |
| `ml-experiment-tracking-and-mlops-workflows` | Experiment tracking, AutoML/HPO, model registries, artifacts, sweeps, Launch jobs, MLflow projects/models/evaluation, data versioning pipelines, GenAI observability, local serving, and operational MLOps. | `scenarios/ml-experiment-tracking-and-mlops-workflows.md` | `autogluon`, `bentoml`, `dvc`, `mlflow`, `nni`, `optuna`, `wandb` |
| `molecular-ml-drug-discovery-and-chemistry-workflows` | Cheminformatics, molecule processing, molecular property prediction, featurization, MoleculeNet, docking, molecular simulation, force fields, conformers, reactions, retrosynthesis, and chemistry model training. | `scenarios/molecular-ml-drug-discovery-and-chemistry-workflows.md` | `aizynthfinder`, `chemprop`, `datamol`, `deepchem`, `diffdock`, `mdanalysis`, `openmm`, `rdkit`, `reinvent4` |
| `multimodal-training-audio-naflex` | OpenCLIP training commands, open_clip_train, CSV/WebDataset data, task-era TrainingTask wrappers, FSDP, torch.compile, CLAP audio, NaFlex, GenLIP, or GenLAP. | `scenarios/multimodal-training-audio-naflex.md` | `open-clip` |
| `protein-structure-prediction-and-design-workflows` | AlphaFold, ColabFold, Boltz, Chai-1, ESM, ProteinMPNN, RFdiffusion, MSA generation, structure prediction outputs, protein backbone generation, binder design, and sequence design. | `scenarios/protein-structure-prediction-and-design-workflows.md` | `alphafold3`, `boltz`, `chai-lab`, `colabfold`, `esm`, `openfold`, `protein-mpnn`, `protenix`, `rfdiffusion` |
| `python-ai-api-services-and-deployment` | Python AI packages exposed as APIs, FastAPI services, OpenAI-compatible endpoints, MCP servers, secured services, custom routes, clusters, consoles, Docker/cloud/serverless deployment, or observability targets. | `scenarios/python-ai-api-services-and-deployment.md` | `stable-diffusion-webui`, `txtai` |
| `python-repository-maintenance` | Tasks that edit, review, test, document, package, or maintain Python source repositories rather than using them only as libraries. | `scenarios/python-repository-maintenance.md` | `cleanrl`, `crewai`, `prefect`, `pydantic-ai`, `skypilot`, `stable-diffusion-webui` |
| `reinforcement-learning-workflows` | Gymnasium environments, Stable-Baselines3 algorithms, RL vectorization, policies, evaluation, experiment scripts, replay buffers, collectors, action masks, multi-agent RL environments, and PPO-family rollout-agent training. | `scenarios/reinforcement-learning-workflows.md` | `cleanrl`, `openrlhf`, `pettingzoo`, `stable-baselines3`, `tianshou`, `trl`, `verl` |
| `scientific-python-data-workflows` | NumPy-style array analysis combined with molecular simulation trajectories, coordinate transformations, or per-frame scientific computations in Python. | `scenarios/scientific-python-data-workflows.md` | `mdanalysis` |
| `single-cell-omics-and-scanpy-workflows` | AnnData/MuData setup, Scanpy preprocessing/QC, graph analysis, marker genes, probabilistic scvi-tools models, multimodal/spatial omics, and single-cell plotting/reporting. | `scenarios/single-cell-omics-and-scanpy-workflows.md` | `anndata`, `pyscenic`, `scanpy`, `scvi-tools`, `squidpy` |
<!-- SKILLQED_REPO_SKILLS_ROUTER_SCENARIOS:END -->

## Scenario Registry

Canonical scenario IDs and aliases are owned by
[`scenario-registry.json`](scenario-registry.json). When importing a new repo
skill, prefer an existing canonical scenario or one of its aliases. Create a new
scenario only when the request domain does not fit the registry and the metadata
declares an explicit split rationale.

## Legacy Suggested Scenario Names

These older defaults remain as examples only. The registry is authoritative for
current imports:


- `embedding-retrieval-workflows`: Embeddings, reranking, vector search, retrieval model training, corpus indexing, and search quality work.
- `llm-serving-inference-workflows`: Model serving, inference APIs, batching, OpenAI-compatible endpoints, decoding, and deployment troubleshooting.
- `training-finetuning-workflows`: Supervised training, fine-tuning, distributed training, adapters, checkpoints, and evaluation loops.
- `data-preparation-evaluation-workflows`: Dataset conversion, validation, metrics, benchmark runners, data layouts, and eval harnesses.
- `agent-tooling-workflows`: Agent frameworks, tool execution, workflow engines, memory systems, and orchestration utilities.
- `ml-infrastructure-ops-workflows`: Deployment, monitoring, scaling, CUDA/backend setup, storage, queues, and operational troubleshooting.
- `repo-maintenance-development-workflows`: Contributor workflows, code generation, testing policy, release maintenance, and docs upkeep.

## Scenario Page Shape

Scenario pages under `references/scenarios/<scenario>.md` are generated by
`verify-repo-skill/scripts/update_repo_skills_router.mjs` from
structured routing metadata. Do not hand-edit generated pages during import.
Instead, update the imported skill's routing metadata and rerun the updater
inside the global import lock.

Each generated scenario page has this shape:

```markdown
# <Scenario Title>

## When To Read
[Task descriptions that should route to this scenario.]

## Repo Skill Options
<!-- SKILLQED_SCENARIO:<scenario>:START -->
### `<skill-name>`

Role: [one-sentence practical role in this scenario.]
Read when: [user terms, repo names, task shapes, data/model/API signals.]
Best for: [specific workflows this skill should support.]
Avoid when: [clear non-fit or better scenario/skill.]
Useful entry points: [root SKILL.md, sub-skills, references, scripts.]
<!-- SKILLQED_SCENARIO:<scenario>:END -->

## How To Choose
[Compare similar repo skills in this same scenario.]
```

Keep scenario pages compact enough for routing, but include the comparison
needed to choose among similar skills. Do not create a separate third layer for
similar-skill differences.
