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

### `celltypist`

Role: Guides CellTypist workflows for automated scRNA-seq cell type annotation, model cache/download management, custom classifier training, and result export or visualization.
Read when: The request names CellTypist or celltypist, asks to annotate scRNA-seq cells, label AnnData or h5ad data, run celltypist --indata, use built-in or local CellTypist .pkl models, download or cache CellTypist models, convert/subset CellTypist models, train a custom CellTypist classifier, debug majority voting/over-clustering, or export AnnotationResult tables, AnnData columns, UMAPs, or dotplots.
Best for: CellTypist package-specific annotation, probability-match and majority-voting decisions, CLI command construction, offline local-model workflows, model conversion/subsetting, custom CellTypist training preflight, and AnnotationResult export/plot troubleshooting.
Avoid when: Use anndata for generic AnnData storage semantics, Scanpy for broad preprocessing/QC/clustering/plotting outside CellTypist prediction, scvi-tools for probabilistic/deep generative single-cell models, pySCENIC for regulatory network inference, or bulk RNA-seq skills for DESeq2-like differential expression.
Useful entry points: `celltypist/SKILL.md`, `celltypist/sub-skills/annotation-workflows/SKILL.md`, `celltypist/sub-skills/model-management/SKILL.md`, `celltypist/sub-skills/training-and-custom-models/SKILL.md`, `celltypist/sub-skills/visualization-and-results/SKILL.md`.

### `omicverse`

Role: OmicVerse is a broad multi-omics analysis platform that extends AnnData/Scanpy-style workflows into single-cell, spatial, bulk, enrichment, metabolomics, proteomics, AIRR, genetics, and agentic analysis.
Read when: Read `omicverse` when the task mentions OmicVerse, `import omicverse as ov`, `ov.pp`, `ov.single`, `ov.pl`, `ov.space`, `ov.es`, `ov.metabol`, `ov.protein`, `ov.airr`, `ov.genetics`, AnnData QC/preprocessing/plotting, SCSA, CellVote, GPTCelltype, Tangram, STAGATE, trajectory, pseudobulk, or multi-omics workflows spanning several OmicVerse modules.
Best for: OmicVerse package-specific API choices, cross-domain omics routing, AnnData slot validation, optional dependency triage, bundled validators, CLI/MCP/JARVIS context, and workflows that combine core preprocessing with downstream biological interpretation.
Avoid when: Use narrower skills such as `anndata`, `scanpy`, `scvi-tools`, `celltypist`, `pyscenic`, or `squidpy` when the user is specifically using those packages rather than OmicVerse wrappers or OmicVerse-integrated workflows.
Useful entry points: `omicverse/SKILL.md`, `omicverse/sub-skills/core-analysis/SKILL.md`, `omicverse/sub-skills/single-cell-workflows/SKILL.md`, `omicverse/sub-skills/spatial-integration/SKILL.md`.

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
Useful entry points: `scvi-tools/SKILL.md`, `scvi-tools/sub-skills/advanced-operations/`, `scvi-tools/sub-skills/annotation-and-query/`, `scvi-tools/sub-skills/core-models/`, `scvi-tools/sub-skills/data-setup/`, `scvi-tools/sub-skills/downstream-analysis/`, `scvi-tools/sub-skills/model-io-and-hub/`, `scvi-tools/sub-skills/multimodal-and-spatial/`, `scvi-tools/sub-skills/training-and-inference/`.

### `squidpy`

Role: Squidpy-specific guidance for spatial molecular data loading, spatial graph statistics, image analysis, visualization, and experimental SpatialData imaging.
Read when: User mentions Squidpy, sq.gr, sq.im, sq.pl, sq.tl, sq.datasets, sq.read, Visium/Vizgen/Nanostring spatial data, ImageContainer, SpatialData tissue masks, spatial_neighbors, nhood_enrichment, ligrec, spatial_scatter, or tiling QC.
Best for: Loading spatial omics inputs, validating AnnData/SpatialData keys, building spatial neighbor graphs, computing Squidpy graph/statistical outputs, working with tissue images, rendering Squidpy plots, and using experimental SpatialData imaging APIs.
Avoid when: Use a Scanpy-focused skill for general non-spatial single-cell preprocessing and marker workflows; use computer-vision skills for generic image segmentation/modeling unrelated to Squidpy/SpatialData; use repository-maintenance skills for changing Squidpy source code itself.
Useful entry points: `squidpy/SKILL.md`, `squidpy/sub-skills/datasets-and-io/SKILL.md`, `squidpy/sub-skills/graph-analysis/SKILL.md`, `squidpy/sub-skills/image-analysis/SKILL.md`, `squidpy/sub-skills/visualization/SKILL.md`, `squidpy/sub-skills/tools-workflows/SKILL.md`, `squidpy/sub-skills/experimental-imaging/SKILL.md`.

<!-- DISCO_SCENARIO:single-cell-omics-and-scanpy-workflows:END -->

## How To Choose

Choose Scanpy for preprocessing, plotting, and AnnData workflows; choose scvi-tools for probabilistic models and deep generative single-cell analysis. Choose `anndata` for annotated matrix container semantics, H5AD/Zarr storage, backed/lazy access, concatenation, aligned annotation troubleshooting, and AnnData extension mechanics. Pair it with Scanpy or scvi-tools when the user asks for analysis or modeling workflows built on top of AnnData. Choose celltypist when the task is package-specific to CellTypist cell type classification, CellTypist model pickles/cache/downloads, custom CellTypist classifiers, the celltypist CLI, or AnnotationResult outputs; choose Scanpy/anndata/scvi-tools only when the task is not centered on CellTypist prediction or model workflows. Choose `omicverse` when the request names OmicVerse or combines AnnData preprocessing with OmicVerse-specific modules, plotting, spatial mapping, multi-omics statistics, or agent/MCP tooling; choose Scanpy/anndata/scvi/squidpy skills when the task is not using OmicVerse APIs. Select pySCENIC when the user is using SCENIC-specific resources or outputs; select Scanpy/scvi-style skills when the task is general single-cell preprocessing, plotting, or probabilistic modeling rather than regulatory-network inference. Choose `squidpy` when the named package or APIs are Squidpy-specific.
