# Graph Learning Workflows

## When To Read

Graph neural network tasks, graph construction, message passing, graph datasets, graph data loaders, graph partitioning, sparse graph operations, and distributed graph training.

## Repo Skill Options

<!-- DISCO_SCENARIO:graph-learning-workflows:START -->
### `dgl`

Role: Guides DGL graph APIs, GNN model construction, message passing, sparse operations, and full-graph training workflows.
Read when: The request names DGL, Deep Graph Library, DGLGraph, heterograph, dgl.nn, dgl.function, GraphConv, SAGEConv, GATConv, HeteroGraphConv, dgl.sparse, or graph neural network training with DGL. The request names DGLDataset, CSVDataset, meta.yaml, DGL save_graphs/load_graphs, OnDiskDataset, GraphBolt metadata.yaml, DGL-Go, dgl configure, dgl recipe, or DGL YAML configs. The request names dgl.distributed, DistGraph, DistDataLoader, node_split, edge_split, partition_graph, part_config, ip_config.txt, DGL launch.py, graph partitions, or distributed GraphBolt.
Best for: Constructing DGL graphs, debugging graph feature schemas, implementing DGL message passing and PyTorch GNN layers, and running safe smoke checks for DGL model workflows. Validating DGL CSV datasets, writing custom DGLDataset subclasses, preparing GraphBolt metadata, linting DGL-Go configs, and linking data layout to training routes. Checking DGL partition metadata, planning trainer script changes, constructing reviewable launch commands, and identifying when SSH/shared-storage/GPU approval is required.
Avoid when: The task is about a different graph-learning framework such as PyG only, or about generic graph algorithms without DGL APIs. The data format is not for DGL or GraphBolt, or the task only needs generic CSV validation without graph semantics. The task is generic distributed systems work with no DGL partition or graph training surface, or when the user asks to run a cluster without confirming hosts and workspace safety.
Useful entry points: `dgl/SKILL.md`, `dgl/sub-skills/graph-apis/SKILL.md`, `dgl/sub-skills/message-passing-training/SKILL.md`, `dgl/sub-skills/datasets-and-io/SKILL.md`, `dgl/sub-skills/dataloading-graphbolt/SKILL.md`, `dgl/sub-skills/dglgo-cli/SKILL.md`, `dgl/sub-skills/distributed-tools/SKILL.md`, `dgl/references/troubleshooting.md`.

### `dgl-lifesci`

Role: Covers the chemistry/biology-specific DGL-LifeSci layer on top of DGL graph learning.
Read when: The request names DGL-LifeSci/dgllife plus graph construction, featurization, GNN predictors, molecule embeddings, link prediction heads, or DGL graph tensors for molecular or biological graph tasks.
Best for: DGL-LifeSci-specific graph constructors, featurizers, datasets, model-zoo constructors, molecule embeddings, and link prediction examples that use dgllife APIs.
Avoid when: Use a generic DGL skill for DistGraph, GraphBolt, distributed graph training, or non-chemistry graph workloads; use PyG skills for torch-geometric data/model APIs.
Useful entry points: `dgl-lifesci/SKILL.md`, `dgl-lifesci/sub-skills/molecule-data-prep/SKILL.md`, `dgl-lifesci/sub-skills/model-zoo-pretraining/SKILL.md`.

### `paddlehelix`

Role: Use paddlehelix for PaddleHelix-specific graph data and molecular GNN workflows built on pahelix and PGL conventions.
Read when: Requests mention pahelix graph records, InMemoryDataset, scaffold splitters, CompoundKit, Compound3DKit, mol_to_graph_data, mol_to_geognn_graph_data, PGL optional dependency errors, GEM/GeoGNN/LiteGEM featurizers, or PaddleHelix GNN model families.
Best for: Explaining PaddleHelix graph record schemas, cache formats, splitters, optional graph dependencies, and routing graph-model training questions to the compound workflow sub-skill.
Avoid when: Use PyG, DGL, or general graph-learning skills when the request is not about PaddleHelix or pahelix data/model contracts.
Useful entry points: `paddlehelix/SKILL.md`, `paddlehelix/sub-skills/core-api-data/SKILL.md`, `paddlehelix/sub-skills/compound-drug-discovery/SKILL.md`.

### `torchdrug`

Role: TorchDrug provides tensor-backed graph, molecule, protein, and knowledge-graph containers plus graph neural layers and models for graph ML workflows.
Read when: Tasks mention graph neural networks, message passing, PackedGraph, PackedMolecule, PackedProtein, GraphConv, GIN, RGCN, GAT, MPNN, SchNet, GearNet, GraphConstruction, variadic tensors, graph_collate, graph masking, graph packing, or TorchDrug model customization.
Best for: TorchDrug-specific graph object construction, batching/masking, layer/model selection, custom MessagePassingBase implementations, and training graph models with core.Engine.
Avoid when: Use PyG or DGL skills when the user is using torch-geometric or DGL APIs directly and does not need TorchDrug containers or task classes.
Useful entry points: `torchdrug/SKILL.md`, `torchdrug/sub-skills/graph-data/SKILL.md`, `torchdrug/sub-skills/layers-and-extensions/SKILL.md`, `torchdrug/sub-skills/training-engine/SKILL.md`.

<!-- DISCO_SCENARIO:graph-learning-workflows:END -->

## How To Choose

Use this scenario for graph ML packages; choose DGL for DGL/GraphBolt/DistGraph and PyG for torch-geometric data/model workflows. Choose `dgl` when DGL-specific graph objects, APIs, layers, or runtime errors appear; use more general graph skills only when no DGL package or API surface is involved. Choose `dgl` for graph-specific dataset folders, DGL-Go recipes, and GraphBolt data pipelines; use generic data validation skills only before the data is mapped to DGL graph semantics. Choose `dgl` when distributed graph training depends on DGL partition metadata or DistGraph APIs; keep execution dry until cluster preconditions are confirmed. Choose `dgl-lifesci` for graph-learning requests whose data, APIs, or errors mention molecules, SMILES, RDKit, MoleculeNet, dgllife datasets, or DGL-LifeSci model constructors. Choose paddlehelix for graph-learning tasks that use PaddleHelix data dictionaries, PGL/Paddle optional dependencies, molecular graph features, or the GEM/PretrainGNN app stack. Choose torchdrug for graph ML requests with TorchDrug API names, drug/protein/KG task classes, or tensor-backed PackedGraph workflows; choose another graph package skill only when the API surface is not TorchDrug.
