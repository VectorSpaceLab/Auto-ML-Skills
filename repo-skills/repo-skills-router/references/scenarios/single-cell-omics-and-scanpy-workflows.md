# Single-Cell Omics and Scanpy Workflows

## When To Read

AnnData/MuData setup, Scanpy preprocessing/QC, graph analysis, marker genes, probabilistic scvi-tools models, multimodal/spatial omics, and single-cell plotting/reporting.

## Repo Skill Options

<!-- DISCO_SCENARIO:single-cell-omics-and-scanpy-workflows:START -->
### `anndata`

Role: Provides package-specific AnnData guidance for object modeling, storage I/O, data combination, reference accessors, and extension namespaces.
Read when: Use when the task involves annotated matrix containers, AnnData, H5AD/Zarr storage, backed or lazy reads, concatenation, AnnCollection, aligned obs/var/layers/obsm/varm/obsp/varp data, raw snapshots, anndata.acc references, or extension namespaces.
Best for: Building and validating AnnData objects, reading/writing H5AD or Zarr, choosing backed/lazy access, combining batches, troubleshooting aligned annotations, and designing AnnData-aware library helpers.
Avoid when: The task is primarily Scanpy preprocessing/plotting, scvi-tools modeling, MuData multimodal workflows, or bulk RNA-seq differential expression without direct AnnData API questions.
Useful entry points: `anndata/SKILL.md`, `anndata/sub-skills/data-model/SKILL.md`, `anndata/sub-skills/storage-io/SKILL.md`, `anndata/sub-skills/combining-data/SKILL.md`, `anndata/sub-skills/accessors-extensions/SKILL.md`.

### `pyscenic`

Role: Use `pyscenic` for pySCENIC-specific regulatory-network workflows from expression matrices through regulons and AUCell activity outputs.
Read when: The request mentions pySCENIC, SCENIC, GRNBoost2, GENIE3, cisTarget ranking databases, motif pruning, regulons, AUCell, SCope loom, or pySCENIC CLI/container commands.
Best for: Constructing pySCENIC CLI/API workflows, diagnosing resource and format issues, choosing output formats, and routing among GRN inference, ctx pruning, AUCell scoring, export, and containers.
Avoid when: The task is generic Scanpy preprocessing, scvi-tools modeling, broad AnnData manipulation without pySCENIC outputs, or repository maintenance unrelated to pySCENIC usage.
Useful entry points: `pyscenic/SKILL.md`, `pyscenic/sub-skills/network-inference/SKILL.md`, `pyscenic/sub-skills/motif-pruning-and-regulons/SKILL.md`, `pyscenic/sub-skills/aucell-and-binarization/SKILL.md`, `pyscenic/sub-skills/data-io-and-export/SKILL.md`, `pyscenic/sub-skills/cli-and-containers/SKILL.md`.

### `scanpy`

Role: Use for Scanpy single-cell analysis workflows: AnnData IO, preprocessing/QC, graph embeddings, clustering, marker genes, plotting/reporting, optional integrations, and Scanpy package troubleshooting.
Read when: The request names `scanpy` or asks for package-specific APIs, CLIs, configs, data/model artifacts, error messages, workflows, or repository maintenance that match this project.
Best for: external integrations, graph embedding analysis, io data access, plotting reporting, and preprocessing qc.
Avoid when: another repo skill in this scenario matches the user's task, package, model family, data format, serving backend, or workflow more directly.
Useful entry points: `scanpy/SKILL.md`, `scanpy/sub-skills/external-integrations/`, `scanpy/sub-skills/graph-embedding-analysis/`, `scanpy/sub-skills/io-data-access/`, `scanpy/sub-skills/plotting-reporting/`, `scanpy/sub-skills/preprocessing-qc/`.

### `scvi-tools`

Role: Use scvi-tools for probabilistic single-cell omics analysis with AnnData/MuData setup, model selection, training, downstream analysis, save/load, Hub workflows, and advanced extension/autotune tasks.
Read when: The request names `scvi-tools` or asks for package-specific APIs, CLIs, configs, data/model artifacts, error messages, workflows, or repository maintenance that match this project.
Best for: advanced operations, annotation and query, core models, data setup, downstream analysis, and 3 other focused workflows.
Avoid when: another repo skill in this scenario matches the user's task, package, model family, data format, serving backend, or workflow more directly.
Useful entry points: `scvi-tools/SKILL.md`, `scvi-tools/sub-skills/advanced-operations/`, `scvi-tools/sub-skills/annotation-and-query/`, `scvi-tools/sub-skills/core-models/`, `scvi-tools/sub-skills/data-setup/`, `scvi-tools/sub-skills/downstream-analysis/`, `3 more sub-skills`.

### `squidpy`

Role: Squidpy-specific guidance for spatial molecular data loading, spatial graph statistics, image analysis, visualization, and experimental SpatialData imaging.
Read when: User mentions Squidpy, sq.gr, sq.im, sq.pl, sq.tl, sq.datasets, sq.read, Visium/Vizgen/Nanostring spatial data, ImageContainer, SpatialData tissue masks, spatial_neighbors, nhood_enrichment, ligrec, spatial_scatter, or tiling QC.
Best for: Loading spatial omics inputs, validating AnnData/SpatialData keys, building spatial neighbor graphs, computing Squidpy graph/statistical outputs, working with tissue images, rendering Squidpy plots, and using experimental SpatialData imaging APIs.
Avoid when: Use a Scanpy-focused skill for general non-spatial single-cell preprocessing and marker workflows; use computer-vision skills for generic image segmentation/modeling unrelated to Squidpy/SpatialData; use repository-maintenance skills for changing Squidpy source code itself.
Useful entry points: `squidpy/SKILL.md`, `squidpy/sub-skills/datasets-and-io/SKILL.md`, `squidpy/sub-skills/graph-analysis/SKILL.md`, `squidpy/sub-skills/image-analysis/SKILL.md`, `squidpy/sub-skills/visualization/SKILL.md`, `squidpy/sub-skills/tools-workflows/SKILL.md`, `squidpy/sub-skills/experimental-imaging/SKILL.md`.

<!-- DISCO_SCENARIO:single-cell-omics-and-scanpy-workflows:END -->

## How To Choose

Choose Scanpy for preprocessing, plotting, and AnnData workflows; choose scvi-tools for probabilistic models and deep generative single-cell analysis. Choose `anndata` for annotated matrix container semantics, H5AD/Zarr storage, backed/lazy access, concatenation, aligned annotation troubleshooting, and AnnData extension mechanics. Pair it with Scanpy or scvi-tools when the user asks for analysis or modeling workflows built on top of AnnData. Select pySCENIC when the user is using SCENIC-specific resources or outputs; select Scanpy/scvi-style skills when the task is general single-cell preprocessing, plotting, or probabilistic modeling rather than regulatory-network inference. Choose `scanpy` when the request names `scanpy`, centers on Use for Scanpy single-cell analysis workflows: AnnData IO, preprocessing/QC, graph embeddings, clustering, marker genes, plotting/reporting, optional integrations, and Scanpy package troubleshooting, uses its APIs or CLIs, references its configs/artifacts/errors, or asks for repository workflows in single cell omics and scanpy workflows. Choose `squidpy` when the named package or APIs are Squidpy-specific. For overlapping Scanpy tasks, route to `squidpy` only when spatial coordinates, tissue images, SpatialData, or Squidpy graph/plot/image APIs are central.
