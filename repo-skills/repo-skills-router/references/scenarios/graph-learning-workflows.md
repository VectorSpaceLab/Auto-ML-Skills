# Graph Learning Workflows

## When To Read

Graph neural network tasks, graph construction, message passing, graph datasets, graph data loaders, graph partitioning, sparse graph operations, and distributed graph training.

## Repo Skill Options

<!-- SKILLQED_SCENARIO:graph-learning-workflows:START -->
### `dgl`

Role: Guides DGL graph APIs, GNN model construction, message passing, sparse operations, and full-graph training workflows.
Read when: The request names DGL, Deep Graph Library, DGLGraph, heterograph, dgl.nn, dgl.function, GraphConv, SAGEConv, GATConv, HeteroGraphConv, dgl.sparse, or graph neural network training with DGL. The request names DGLDataset, CSVDataset, meta.yaml, DGL save_graphs/load_graphs, OnDiskDataset, GraphBolt metadata.yaml, DGL-Go, dgl configure, dgl recipe, or DGL YAML configs. The request names dgl.distributed, DistGraph, DistDataLoader, node_split, edge_split, partition_graph, part_config, ip_config.txt, DGL launch.py, graph partitions, or distributed GraphBolt.
Best for: Constructing DGL graphs, debugging graph feature schemas, implementing DGL message passing and PyTorch GNN layers, and running safe smoke checks for DGL model workflows. Validating DGL CSV datasets, writing custom DGLDataset subclasses, preparing GraphBolt metadata, linting DGL-Go configs, and linking data layout to training routes. Checking DGL partition metadata, planning trainer script changes, constructing reviewable launch commands, and identifying when SSH/shared-storage/GPU approval is required.
Avoid when: The task is about a different graph-learning framework such as PyG only, or about generic graph algorithms without DGL APIs. The data format is not for DGL or GraphBolt, or the task only needs generic CSV validation without graph semantics. The task is generic distributed systems work with no DGL partition or graph training surface, or when the user asks to run a cluster without confirming hosts and workspace safety.
Useful entry points: `dgl/SKILL.md`, `dgl/sub-skills/graph-apis/SKILL.md`, `dgl/sub-skills/message-passing-training/SKILL.md`, `dgl/sub-skills/datasets-and-io/SKILL.md`, `dgl/sub-skills/dataloading-graphbolt/SKILL.md`, `dgl/sub-skills/dglgo-cli/SKILL.md`, `dgl/sub-skills/distributed-tools/SKILL.md`, `dgl/references/troubleshooting.md`.

<!-- SKILLQED_SCENARIO:graph-learning-workflows:END -->

## How To Choose

Use this scenario for graph ML packages; choose DGL for DGL/GraphBolt/DistGraph and PyG for torch-geometric data/model workflows. Choose `dgl` when DGL-specific graph objects, APIs, layers, or runtime errors appear; use more general graph skills only when no DGL package or API surface is involved. Choose `dgl` for graph-specific dataset folders, DGL-Go recipes, and GraphBolt data pipelines; use generic data validation skills only before the data is mapped to DGL graph semantics. Choose `dgl` when distributed graph training depends on DGL partition metadata or DistGraph APIs; keep execution dry until cluster preconditions are confirmed.
