# Scientific Python Data Workflows

## When To Read

NumPy-style array analysis combined with molecular simulation trajectories, coordinate transformations, or per-frame scientific computations in Python.

## Repo Skill Options

<!-- DISCO_SCENARIO:scientific-python-data-workflows:START -->
### `biotite`

Role: Biotite provides practical guidance for sequence analysis, structure analysis, biological file IO, database fetch planning, and optional scientific visualization interfaces.
Read when: Read biotite for tasks mentioning Biotite, biotite.sequence, biotite.structure, AtomArray, AtomArrayStack, ProteinSequence, NucleotideSequence, FASTA/FASTQ/GenBank/GFF parsing, PDB/PDBx/BinaryCIF/GRO/PDBQT/MOL/SDF/trajectory parsing, sequence alignment, substitution matrices, k-mer search, profiles, phylogenetic trees, RCSB/Entrez/UniProt/AlphaFold DB/PubChem fetch planning, BLAST/MSA/DSSP/SRA/ViennaRNA wrappers, or NumPy-backed biomolecular analysis.
Best for: Local computational molecular biology workflows: constructing and validating sequences, aligning sequences, handling annotations/profiles/trees, reading and converting biological file formats, analyzing AtomArray structures, measuring geometry/contacts/SASA/superposition/trajectories, and planning database/application handoffs.
Avoid when: Avoid biotite when the request is primarily ML model training, protein structure prediction/design with AlphaFold/ESM/RFdiffusion-style models, bulk RNA-seq differential expression, general data pipelines, or materials-science crystal workflows that do not use Biotite APIs.
Useful entry points: `biotite/SKILL.md`, `biotite/sub-skills/sequence-analysis/SKILL.md`, `biotite/sub-skills/structure-analysis/SKILL.md`, `biotite/sub-skills/file-io-formats/SKILL.md`, `biotite/sub-skills/database-application/SKILL.md`.

### `mdanalysis`

Role: Explains how MDAnalysis exposes molecular data as arrays and per-frame objects for scientific Python workflows.
Read when: User asks for trajectory loops, per-frame distance calculations, custom AnalysisBase classes, NumPy coordinate arrays, periodic box handling, or writing derived molecular data outputs.
Best for: Building robust scientific Python scripts around molecular trajectory data where MDAnalysis is the data access and analysis layer.
Avoid when: The data is not molecular simulation data, no MDAnalysis APIs are involved, or a generic NumPy/Pandas workflow is sufficient.
Useful entry points: `mdanalysis/SKILL.md`, `mdanalysis/sub-skills/analysis-workflows/SKILL.md`, `mdanalysis/sub-skills/transformations-writing/SKILL.md`.

### `nilearn`

Role: Use nilearn for Python neuroimaging workflows built on NumPy, nibabel, scipy, scikit-learn, and domain-specific fMRI analysis APIs.
Read when: The task mentions Nilearn, neuroimaging, fMRI, NIfTI/Niimg, brain masks, surface meshes, fsaverage, fMRIPrep confounds, BIDS derivatives, first-level or second-level GLM, design matrices, contrasts, statistical maps, voxel decoding, searchlight, connectomes, atlases, or Nilearn plotting/reporting.
Best for: Image/signal preprocessing, masker and region extraction, surface workflows, GLM modeling, decoding/searchlight/connectivity/decomposition, dataset/template/atlas fetchers, fMRIPrep interfaces, and brain visualization/reporting.
Avoid when: Avoid for generic medical image segmentation/training frameworks, non-neuroimaging computer vision, non-Python neuroscience tools, or general scikit-learn tasks with no Nilearn/neuroimaging data contract.
Useful entry points: `nilearn/SKILL.md`, `nilearn/sub-skills/data-io-signal/SKILL.md`, `nilearn/sub-skills/maskers-regions/SKILL.md`, `nilearn/sub-skills/surface-workflows/SKILL.md`, `nilearn/sub-skills/glm-analysis/SKILL.md`, `nilearn/sub-skills/ml-decoding-connectivity/SKILL.md`, `nilearn/sub-skills/datasets-interfaces/SKILL.md`, `nilearn/sub-skills/plotting-reporting/SKILL.md`.

### `paddlehelix`

Role: Use paddlehelix for dependency-light pahelix utilities, protein sequence tokenization, LinearRNA checks, and local data/config preflights tied to PaddleHelix.
Read when: Requests mention pahelix InMemoryDataset, NPZ part files, ProteinTokenizer, LinearRNA/LinearFold/LinearPartition, RNA constraints, FASTA/plain sequence validation, or local PaddleHelix input preflight scripts.
Best for: Using bundled safe checkers to validate data/config/sequences and explain dependency-light PaddleHelix APIs without launching app workflows.
Avoid when: Use broader scientific Python skills when the task is generic NumPy/pandas analysis or unrelated to PaddleHelix data contracts, protein/RNA utilities, or pahelix APIs.
Useful entry points: `paddlehelix/SKILL.md`, `paddlehelix/sub-skills/core-api-data/SKILL.md`, `paddlehelix/sub-skills/protein-sequence-function/SKILL.md`, `paddlehelix/sub-skills/linear-rna/SKILL.md`.

### `scikit-bio`

Role: scikit-bio provides focused guidance for bioinformatics data structures, file formats, and statistical workflows built around the scikit-bio package.
Read when: The user names scikit-bio, skbio, DNA/RNA/Protein sequence objects, TabularMSA, TreeNode, Newick, FASTA/FASTQ, BIOM Table, SampleMetadata, alpha_diversity, beta_diversity, UniFrac, Faith PD, DistanceMatrix, PERMANOVA, ANOSIM, Mantel, PCoA, CCA/RDA, ANCOM, compositional transforms, or protein embeddings.
Best for: Using scikit-bio library APIs for sequence/alignment manipulation, phylogenetic trees, diversity metrics, biological IO/metadata, table-like count workflows, distance statistics, ordination, composition analysis, and embeddings.
Avoid when: Avoid for general scikit-learn machine learning, Scanpy/AnnData-centered single-cell workflows, molecular chemistry modeling, protein structure prediction/design, or generic pandas/NumPy analysis that does not use scikit-bio data objects or APIs.
Useful entry points: `scikit-bio/SKILL.md`, `scikit-bio/sub-skills/io-metadata/SKILL.md`, `scikit-bio/sub-skills/sequences-alignment/SKILL.md`, `scikit-bio/sub-skills/trees-phylogeny/SKILL.md`, `scikit-bio/sub-skills/diversity-tables/SKILL.md`, `scikit-bio/sub-skills/statistics-ordination/SKILL.md`.

<!-- DISCO_SCENARIO:scientific-python-data-workflows:END -->

## How To Choose

Use this scenario when the task is scientific data analysis rather than chemistry modeling, drug discovery, or general data pipelines. Choose biotite when the task names Biotite or uses its biological sequence/structure object model, file formats, database clients, or wrappers. For molecular simulations, choose biotite when the work is AtomArray/trajectory analysis or OpenMM conversion, and choose a dedicated simulation package skill when force-field setup or simulation execution is primary. Use `mdanalysis` when the scientific Python task depends on MDAnalysis trajectory, topology, or AtomGroup semantics; otherwise use a generic scientific Python skill. Choose nilearn when the user needs Python code or troubleshooting for neuroimaging arrays, Niimg/NIfTI files, fMRI statistical models, brain masks/atlases, surface meshes, BIDS/fMRIPrep interfaces, or Nilearn-specific plotting/reporting APIs. Choose a broader scientific Python skill only when the task has no neuroimaging or Nilearn-specific concepts. Choose paddlehelix when a scientific data workflow depends on PaddleHelix-specific data loaders, NPZ metadata, tokenizer IDs, RNA folding APIs, or the bundled PaddleHelix validators. If the task is repository maintenance rather than package use, combine this skill with the Python Repository Maintenance scenario only after identifying the scikit-bio module being edited.
