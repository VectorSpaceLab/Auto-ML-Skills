# Installation And Capabilities

Read this when you need to choose install extras, understand which model family fits a task, or check public package requirements before using the sub-skills.

## Public Install Commands

Base install for inference with text models:

```bash
pip install -U sentence-transformers
```

Extras are additive:

```bash
pip install -U "sentence-transformers[train]"
pip install -U "sentence-transformers[image]"
pip install -U "sentence-transformers[audio]"
pip install -U "sentence-transformers[video]"
pip install -U "sentence-transformers[onnx]"
pip install -U "sentence-transformers[onnx-gpu]"
pip install -U "sentence-transformers[openvino]"
```

For conda users, install the base package from conda-forge and use pip for extras that conda does not model:

```bash
conda install -c conda-forge sentence-transformers
pip install -U "sentence-transformers[train,image]"
```

For development against the public repository:

```bash
git clone https://github.com/huggingface/sentence-transformers.git
cd sentence-transformers
pip install -e ".[dev]"
```

## Dependency Groups

Base dependencies include `transformers`, `huggingface-hub`, `torch`, `numpy`, `scikit-learn`, `scipy`, `typing_extensions`, and `tqdm`.

Training requires `datasets` and `accelerate`. Optional tracking packages such as `trackio`, `wandb`, or `codecarbon` are not installed by the base training extra unless the user installs them separately.

Image, audio, and video support come through the corresponding `transformers` extras. Passing `torchcodec.AudioDecoder` or `torchcodec.VideoDecoder` objects requires installing `torchcodec` separately.

ONNX support uses `optimum-onnx` with ONNX Runtime. OpenVINO support uses `optimum-intel` with OpenVINO.

## Capability Map

| Capability | Primary API | Best Sub-Skill | Notes |
| --- | --- | --- | --- |
| Dense text embeddings | `SentenceTransformer.encode` | `sentence-transformer` | Use for STS, clustering, classification features, semantic search, and retrieval. |
| Retrieval embeddings | `encode_query`, `encode_document` | `sentence-transformer` | Preserves query/document prompts when a model defines them. |
| Multimodal embeddings | `SentenceTransformer` | `sentence-transformer` | Requires matching extras and a multimodal model. |
| Pair scoring | `CrossEncoder.predict` | `cross-encoder` | Use when each input is a pair and an independent score or class is needed. |
| Reranking | `CrossEncoder.rank` | `cross-encoder` | Use after dense or sparse retrieval returns top candidates. |
| Sparse embeddings | `SparseEncoder.encode` | `sparse-encoder` | Produces high-dimensional sparse tensors for lexical+semantic retrieval. |
| Sparse term inspection | `SparseEncoder.decode`, `sparsity` | `sparse-encoder` | Useful for interpretability and debugging sparsity. |
| Fine-tuning | `*Trainer`, `*TrainingArguments` | `training-and-evaluation` | Choose loss from dataset columns before coding. |
| Hard-negative mining | `mine_hard_negatives` | `training-and-evaluation` | Converts positive pairs into triplets, n-tuples, labeled pairs, or labeled lists. |
| Evaluation | Evaluator classes | `training-and-evaluation` | Separate evaluator families exist for dense, cross, and sparse models. |
| Quantized embeddings | `quantize_embeddings`, `precision=` | `optimization-and-deployment` | Use for lower memory and faster retrieval indexes. |
| ONNX/OpenVINO export | backend export helpers | `optimization-and-deployment` | Requires installing the matching extra. |

## Model Family Boundaries

`SentenceTransformer` models encode each item independently and compare vectors later. They scale well to large corpora because documents can be embedded once and indexed.

`CrossEncoder` models score a pair jointly. They are usually more accurate for top-k reranking but slower because each query-document pair requires a model forward pass.

`SparseEncoder` models produce sparse vectors, often vocabulary-sized. They are useful for lexical-aware semantic search and hybrid retrieval, and are commonly based on SPLADE.

The package also includes shared base modules, utility functions, backend export helpers, model card data classes, trainer classes, training arguments, samplers, losses, evaluators, and data collators. Treat internal module paths as implementation details unless the public docs or imports expose them.

## Public Runtime Assumptions

Most pretrained examples download from Hugging Face Hub. For offline environments, use local model paths and pass `local_files_only=True`.

Many models support prompts or instructions. Prefer `encode_query` and `encode_document` for retrieval tasks so the model can select the right prompt automatically.

Large training and export workflows may need a GPU or a specific accelerator, but the import checks and metadata scripts in this skill are safe on CPU.

No primary package CLI entry points are required for normal use. Scripts in this skill are helper scripts for agents, not upstream package commands.
