# Molecular ML, Drug Discovery, and Chemistry Workflows

## When To Read

Cheminformatics, molecule processing, molecular property prediction, featurization, MoleculeNet, docking, molecular simulation, force fields, conformers, reactions, retrosynthesis, and chemistry model training.

## Repo Skill Options

<!-- DISCO_SCENARIO:molecular-ml-drug-discovery-and-chemistry-workflows:START -->
### `aizynthfinder`

Role: Provides self-contained routing and references for using AiZynthFinder CLI/API workflows, configuration assets, result analysis, and extension points.
Read when: User mentions aizynthfinder, aizynthcli, aizynthapp, smiles2stock, download_public_data, retrosynthetic planning, route trees, output.json.gz, trees.json, expansion policy, stock files, Chemformer plugin, custom scorer, or MCTS/DFPN/RetroStar search settings.
Best for: Building and validating AiZynthFinder configs, constructing CLI/API planning commands, inspecting output tables and reaction trees, troubleshooting optional dependencies, and implementing safe custom hooks or plugins.
Avoid when: The task is general cheminformatics unrelated to AiZynthFinder, requires designing new chemistry models from scratch, or only needs RDKit primitives without AiZynthFinder workflows.
Useful entry points: `aizynthfinder/SKILL.md`, `aizynthfinder/sub-skills/planning-workflows/SKILL.md`, `aizynthfinder/sub-skills/configuration-and-data/SKILL.md`, `aizynthfinder/sub-skills/route-analysis/SKILL.md`, `aizynthfinder/sub-skills/extension-and-development/SKILL.md`.

### `biotite`

Role: Biotite covers the molecular data preparation, file conversion, AtomArray manipulation, PubChem fetching, AutoDock Vina wrapper planning, RDKit/OpenMM/PyMOL conversion, and visualization side of chemistry-adjacent workflows.
Read when: Read biotite for AtomArray-to-RDKit/OpenMM/PyMOL conversions, MOL/SDF/PDB/PDBx/BinaryCIF parsing, PubChem CID queries/fetches, AutoDock Vina wrapper diagnostics, molecular structure filtering, finite-coordinate or BondList preparation, and visualization/export errors involving Biotite objects.
Best for: Preparing and converting molecular structure data with Biotite, diagnosing optional RDKit/OpenMM/PyMOL/Vina dependencies, and bridging local Biotite arrays to chemistry or visualization tools.
Avoid when: Avoid biotite when the request is primarily molecular ML model training/inference, retrosynthesis, property-prediction benchmarks, force-field parameterization, or full molecular dynamics simulation setup not centered on Biotite conversion or analysis.
Useful entry points: `biotite/SKILL.md`, `biotite/sub-skills/structure-analysis/SKILL.md`, `biotite/sub-skills/file-io-formats/SKILL.md`, `biotite/sub-skills/database-application/SKILL.md`, `biotite/sub-skills/interfaces-visualization/SKILL.md`.

### `chemprop`

Role: Guides Chemprop molecular property prediction workflows, including CLI training, prediction, fingerprints, data validation, Python APIs, reaction/atom-bond tasks, uncertainty, hpopt, and conversion workflows.
Read when: The request names `chemprop` or asks for package-specific APIs, CLIs, configs, data/model artifacts, error messages, workflows, or repository maintenance that match this project.
Best for: data featurization, prediction fingerprints, python api modeling, specialized molecular tasks, training cli, and uncertainty advanced.
Avoid when: another repo skill in this scenario matches the user's task, package, model family, data format, serving backend, or workflow more directly.
Useful entry points: `chemprop/SKILL.md`, `chemprop/sub-skills/data-featurization/`, `chemprop/sub-skills/prediction-fingerprints/`, `chemprop/sub-skills/python-api-modeling/`, `chemprop/sub-skills/specialized-molecular-tasks/`, `chemprop/sub-skills/training-cli/`, `chemprop/sub-skills/uncertainty-advanced/`.

### `datamol`

Role: Provides self-contained datamol routing and workflow guidance for RDKit-first molecular processing in Python.
Read when: datamol, dm.to_mol, RDKit Mol, SMILES, SDF, fingerprints, descriptors, Tanimoto, Butina, conformers, scaffold, reaction SMARTS, lasso highlight, datamol.viz, fsspec molecule files.
Best for: Building or debugging datamol-based Python workflows for molecule IO/prep, feature/similarity analysis, structure generation, and visualization/utility helpers.
Avoid when: The task is pure RDKit without datamol APIs, requires large-scale model training unrelated to datamol, or asks for proprietary chemistry services outside local Python molecule processing.
Useful entry points: `datamol/SKILL.md`, `datamol/sub-skills/molecule-io-prep/SKILL.md`, `datamol/sub-skills/fingerprints-similarity/SKILL.md`, `datamol/sub-skills/structure-generation/SKILL.md`, `datamol/sub-skills/visualization-utilities/SKILL.md`.

### `deepchem`

Role: Use DeepChem for molecular machine learning, data loading, featurization, model training, MoleculeNet, docking, and optional backend troubleshooting.
Read when: The request names `deepchem` or asks for package-specific APIs, CLIs, configs, data/model artifacts, error messages, workflows, or repository maintenance that match this project.
Best for: data and molnet, docking and structure, featurization, and model training.
Avoid when: another repo skill in this scenario matches the user's task, package, model family, data format, serving backend, or workflow more directly.
Useful entry points: `deepchem/SKILL.md`, `deepchem/sub-skills/data-and-molnet/`, `deepchem/sub-skills/docking-and-structure/`, `deepchem/sub-skills/featurization/`, `deepchem/sub-skills/model-training/`.

### `deepmd-kit`

Role: Guides DeePMD-kit installation, data/config preparation, model training/fine-tuning, frozen-model inference, model operations, LAMMPS/i-PI/native integrations, and troubleshooting for Deep Potential workflows.
Read when: The request names DeePMD-kit, deepmd-kit, DeePMD, Deep Potential, DeepPot, the `dp` CLI, `DeepPot`, `type.raw`, `type_map.raw`, DeePMD system `set.*` folders, `input.json` for DeePMD training, `.pb` or `.pth` DeePMD model artifacts, `dp test`, `dp model-devi`, `dp eval-desc`, `pair_style deepmd`, `deepspin`, or asks for ML interatomic potential training/inference/deployment in molecular dynamics.
Best for: Installing and validating DeePMD-kit backends, preparing DeePMD data/configs, drafting and troubleshooting `dp train`/freeze/fine-tune workflows, running Python/CLI inference and model operations, and writing LAMMPS/i-PI/native integration guidance for DeePMD models.
Avoid when: The task is generic cheminformatics, molecule featurization, OpenMM/MDAnalysis trajectory analysis without DeePMD models, or a different molecular ML package with its own skill. Use Python repository maintenance only when the user is editing this checkout rather than using DeePMD-kit workflows.
Useful entry points: `deepmd-kit/SKILL.md`, `deepmd-kit/sub-skills/data-config/SKILL.md`, `deepmd-kit/sub-skills/training-models/SKILL.md`, `deepmd-kit/sub-skills/inference-model-ops/SKILL.md`, `deepmd-kit/sub-skills/integrations-development/SKILL.md`.

### `dgl-lifesci`

Role: Guides DGL-LifeSci/dgllife workflows for DGL-based graph neural networks in chemistry and biology.
Read when: The request names DGL-LifeSci, dgllife, DGL molecular graphs, MoleculeNet with DGL, WLN reaction prediction, PDBBind binding affinity, ACNN, PotentialNet, DGMG, JTVAE, molecule graph featurizers, or needs chemistry/biology graph neural-network workflows with RDKit and DGL.
Best for: Molecule graph construction and featurization, custom SMILES/CSV datasets, supervised property prediction configs, dgllife model-zoo/pretrained constructors, reaction center and candidate ranking workflows, protein-ligand binding affinity planning, and DGMG/JTVAE molecular generation input validation.
Avoid when: Use RDKit or Datamol skills for standalone cheminformatics without DGL-LifeSci; use generic DGL skills for non-chemistry graph learning; use DeepChem/Chemprop skills when the task targets those frameworks instead of dgllife.
Useful entry points: `dgl-lifesci/SKILL.md`, `dgl-lifesci/sub-skills/molecule-data-prep/SKILL.md`, `dgl-lifesci/sub-skills/property-prediction/SKILL.md`, `dgl-lifesci/sub-skills/model-zoo-pretraining/SKILL.md`, `dgl-lifesci/sub-skills/reaction-prediction/SKILL.md`, `dgl-lifesci/sub-skills/binding-affinity/SKILL.md`, `dgl-lifesci/sub-skills/generative-models/SKILL.md`.

### `diffdock`

Role: Provides repo-specific routing, command construction, validation, troubleshooting, and benchmark/training guidance for DiffDock workflows.
Read when: User mentions DiffDock, DiffDock-L, docking inference, protein_ligand_csv, default_inference_args.yaml, PDBBind, BindingMOAD, DockGen, PoseBusters, GNINA, spyrmsd, DiffDock Web, score model training, or confidence model training.
Best for: Planning and debugging DiffDock inference, UI, training/data preparation, evaluation benchmarks, RMSD/confidence metrics, and safe preflight checks without re-reading the source repository.
Avoid when: The task is about a different docking package, generic RDKit chemistry unrelated to DiffDock, protein-protein docking, or installing arbitrary CUDA/Torch stacks without DiffDock-specific context.
Useful entry points: `diffdock/SKILL.md`, `diffdock/sub-skills/docking-inference/SKILL.md`, `diffdock/sub-skills/web-ui/SKILL.md`, `diffdock/sub-skills/training-data/SKILL.md`, `diffdock/sub-skills/evaluation-benchmarks/SKILL.md`.

### `mdanalysis`

Role: Provides repo-specific guidance for using MDAnalysis to load systems, select atoms, run analyses, transform/write trajectories, and handle format/converter dependencies.
Read when: User mentions MDAnalysis, mda.Universe, AtomGroup, select_atoms, AnalysisBase, RMSD/RDF/contacts/hydrogen bonds, transformations, trajectory writers, topology or coordinate formats, RDKit/OpenMM/ParmEd converters, or optional format import errors.
Best for: Python coding tasks that use MDAnalysis as a library for molecular simulation data loading, selection, analysis, transformation, writing, and optional dependency troubleshooting.
Avoid when: The task is about unrelated molecular packages, running MDAnalysis project release/CI maintenance, or reproducing benchmark performance rather than using the public package APIs.
Useful entry points: `mdanalysis/SKILL.md`, `mdanalysis/sub-skills/universe-io/SKILL.md`, `mdanalysis/sub-skills/selections-topology/SKILL.md`, `mdanalysis/sub-skills/analysis-workflows/SKILL.md`, `mdanalysis/sub-skills/transformations-writing/SKILL.md`, `mdanalysis/sub-skills/formats-converters/SKILL.md`.

### `omicverse`

Role: OmicVerse includes molecular structure and docking-adjacent helpers as one specialist domain within its omics platform.
Read when: Read `omicverse` when the task mentions `ov.mol`, `fetch_structure`, `predict_structure`, `known_drugs`, `pockets`, `druggability`, `dock`, OmicVerse molecular target workflows, or coordinating molecular outputs with omics analyses.
Best for: OmicVerse-specific molecular helper routing, optional `mol`/`mol-dock` dependency planning, and safe validation before network structure fetches or docking tools.
Avoid when: Use RDKit, Datamol, DeepChem, OpenMM, MDAnalysis, or docking-package skills when the task is primarily about those packages rather than OmicVerse molecular wrappers.
Useful entry points: `omicverse/SKILL.md`, `omicverse/sub-skills/specialist-domains/SKILL.md`.

### `openfe`

Role: OpenFE-specific routing for alchemical free energy planning, OpenMM protocol configuration, command-line execution, and result analysis in molecular simulation campaigns.
Read when: Tasks mention OpenFE, Open Free Energy, alchemical free energy, RBFE, RHFE, ABFE, AHFE, SepTop, ligand networks, atom mappings, transformation JSONs, openfe quickrun, OpenMM free energy protocols, gather TSVs, result estimates, or uncertainty interpretation.
Best for: Planning ligand/protein/solvent systems, creating RBFE/RHFE networks, configuring OpenFE protocol classes and settings, constructing safe openfe CLI command plans, debugging quickrun/cache issues, and summarizing OpenFE result JSONs or gather outputs.
Avoid when: Use broader OpenMM or chemistry-tool skills when the task is generic molecular dynamics, force-field setup, RDKit molecule editing, docking, or trajectory analysis without OpenFE-specific planning, execution, or result artifacts.
Useful entry points: `openfe/SKILL.md`, `openfe/sub-skills/network-planning/SKILL.md`, `openfe/sub-skills/protocols/SKILL.md`, `openfe/sub-skills/cli-workflows/SKILL.md`, `openfe/sub-skills/results-analysis/SKILL.md`.

### `openff-toolkit`

Role: OpenFF Toolkit skill for molecule processing, topology/system assembly, SMIRNOFF force-field loading/editing/application, and backend wrapper troubleshooting.
Read when: User asks about openff-toolkit, Open Force Field Toolkit, openff.toolkit, Molecule, Topology, ForceField, SMIRNOFF, OFFXML, toolkit_registry, RDKit/OpenEye/AmberTools/NAGL wrappers, OpenFF force fields, parameter handlers, label_molecules, create_interchange, create_openmm_system, PDB unique_molecules, conformers, partial charges, SMARTS/SMIRKS, or force-field assignment errors.
Best for: Using or troubleshooting OpenFF Toolkit APIs for molecules, topology/PDB systems, SMIRNOFF .offxml force fields, OpenMM/Interchange handoff, and optional backend registry behavior.
Avoid when: Use OpenMM or MDAnalysis-specific skills for simulation engine or trajectory analysis after OpenFF has produced system/topology artifacts; use generic RDKit/datamol skills for chemistry tasks that do not involve OpenFF objects or SMIRNOFF force fields.
Useful entry points: `openff-toolkit/SKILL.md`, `openff-toolkit/sub-skills/molecules-and-io/SKILL.md`, `openff-toolkit/sub-skills/topology-and-systems/SKILL.md`, `openff-toolkit/sub-skills/smirnoff-force-fields/SKILL.md`, `openff-toolkit/sub-skills/toolkit-backends/SKILL.md`.

### `openmm`

Role: Use OpenMM for molecular simulation workflows, force-field/model preparation, custom forces/integrators, platform/performance diagnostics, and maintainer extension work.
Read when: The request names `openmm` or asks for package-specific APIs, CLIs, configs, data/model artifacts, error messages, workflows, or repository maintenance that match this project.
Best for: custom forces integrators, development extensions, force fields modeling, platforms performance, and simulation workflows.
Avoid when: another repo skill in this scenario matches the user's task, package, model family, data format, serving backend, or workflow more directly.
Useful entry points: `openmm/SKILL.md`, `openmm/sub-skills/custom-forces-integrators/`, `openmm/sub-skills/development-extensions/`, `openmm/sub-skills/force-fields-modeling/`, `openmm/sub-skills/platforms-performance/`, `openmm/sub-skills/simulation-workflows/`.

### `paddlehelix`

Role: Use paddlehelix to route PaddleHelix chemistry and drug-discovery tasks to compound workflow references and safe validators.
Read when: Requests mention PaddleHelix, pahelix compound utilities, GEM, GEM-2, PretrainGNNs, MoleculeNet-style property data, DTI apps such as GraphDTA or MolTrans, JT-VAE/SD-VAE/Seq-VAE, HelixDock, SMILES files, chemistry JSON configs, PDBbind docking data, or missing RDKit/OpenBabel/PGL/Paddle dependencies.
Best for: Planning or preflighting PaddleHelix molecular property, DTI, molecular generation, drug synergy, few-shot property, and HelixDock workflows without running heavy downloads or training by default.
Avoid when: Use a dedicated RDKit, DeepChem, Chemprop, OpenMM, or generic chemistry package skill when the task does not involve PaddleHelix APIs, app layouts, or HelixDock conventions.
Useful entry points: `paddlehelix/SKILL.md`, `paddlehelix/sub-skills/compound-drug-discovery/SKILL.md`, `paddlehelix/sub-skills/core-api-data/SKILL.md`.

### `prolif`

Role: Use prolif for protein-ligand interaction fingerprint workflows that combine RDKit/MDAnalysis inputs, docking or trajectory structures, residue-level interaction definitions, fingerprint exports, and ProLIF plotting outputs.
Read when: Tasks mention ProLIF, protein-ligand interaction fingerprints, IFPs from docking poses or MDAnalysis trajectories, residue-pair interaction metadata, WaterBridge, implicit hydrogen interactions, LigNetwork, Barcode, Complex3D, SDF/MOL2/PDBQT suppliers, or converting molecular structures into interaction fingerprint DataFrames/bitvectors.
Best for: Preparing ProLIF Molecule objects, choosing interaction classes and parameters, running Fingerprint.run or run_from_iterable, exporting pandas/RDKit fingerprint results, and creating ProLIF interaction network/barcode/3D visualizations.
Avoid when: Use a broader RDKit, MDAnalysis, OpenMM, or molecular-ML skill when the task is general molecule editing, trajectory analysis, simulation, force-field setup, molecular model training, or docking execution rather than ProLIF interaction fingerprint analysis.
Useful entry points: `prolif/SKILL.md`, `prolif/sub-skills/molecules-and-io/SKILL.md`, `prolif/sub-skills/interactions/SKILL.md`, `prolif/sub-skills/fingerprints/SKILL.md`, `prolif/sub-skills/visualization/SKILL.md`.

### `rdkit`

Role: Use for RDKit cheminformatics tasks: molecule parsing and validation, descriptors and fingerprints, conformers and drawing, reactions and standardization, data integrations, optional Contrib utilities, or RDKit repository.
Read when: The request names `rdkit` or asks for package-specific APIs, CLIs, configs, data/model artifacts, error messages, workflows, or repository maintenance that match this project.
Best for: conformers drawing, contrib utilities, data cli integration, descriptors fingerprints, molecule io core, and 2 other focused workflows.
Avoid when: another repo skill in this scenario matches the user's task, package, model family, data format, serving backend, or workflow more directly.
Useful entry points: `rdkit/SKILL.md`, `rdkit/sub-skills/conformers-drawing/`, `rdkit/sub-skills/contrib-utilities/`, `rdkit/sub-skills/data-cli-integration/`, `rdkit/sub-skills/descriptors-fingerprints/`, `rdkit/sub-skills/molecule-io-core/`, `rdkit/sub-skills/reactions-standardization/`, `rdkit/sub-skills/repo-development/`.

### `reinvent4`

Role: Routes REINVENT4 molecular design tasks to focused workflow sub-skills with self-contained config, validation, and troubleshooting guidance.
Read when: REINVENT4, reinvent, reinvent_datapre, sampling.toml, scoring.toml, transfer_learning.toml, staged_learning.toml, data_pipeline.toml, enumeration.toml, LibInvent, LinkInvent, Mol2Mol, PepInvent, scoring component, comp_ plugin, @add_tag, RDKit, OpenEye, Chemprop.
Best for: Preparing and validating REINVENT4 run configs, choosing CLI flags, designing scoring functions/plugins, preprocessing SMILES, and troubleshooting optional dependencies without reopening the source repo.
Avoid when: The task is general cheminformatics unrelated to REINVENT4, asks to reproduce the REINVENT4 paper from scratch, or requires long production training/external scoring execution without user approval.
Useful entry points: `reinvent4/SKILL.md`, `reinvent4/sub-skills/sampling/SKILL.md`, `reinvent4/sub-skills/scoring/SKILL.md`, `reinvent4/sub-skills/learning/SKILL.md`, `reinvent4/sub-skills/data-pipeline/SKILL.md`, `reinvent4/sub-skills/enumeration/SKILL.md`.

### `schnetpack`

Role: SchNetPack-specific guidance for atomistic neural network potentials, datasets, Hydra training/prediction configs, ASE/MD interfaces, and LAMMPS deployment.
Read when: Use for requests naming SchNetPack, schnetpack, spktrain, spkpredict, spkconvert, spkdeploy, spkmd, SchNet, PaiNN, AtomisticModel, NeuralNetworkPotential, ASEAtomsData, AtomsDataModule, SpkCalculator, atomistic datasets, neural network potentials, energy/force/stress model training, QM9/MD17/rMD17 configs, ASE calculators, molecular dynamics, or LAMMPS pair_style schnetpack.
Best for: Creating and validating ASE DB datasets, composing Hydra training or prediction commands, wiring atomistic model components and property keys, using trained models with ASE/MD, and preparing LAMMPS TorchScript deployment.
Avoid when: Avoid for generic cheminformatics molecule manipulation without atomistic neural-network potentials, non-SchNetPack molecular simulation engines, or repository-maintenance tasks unrelated to SchNetPack workflows.
Useful entry points: `schnetpack/SKILL.md`, `schnetpack/sub-skills/data-pipelines/SKILL.md`, `schnetpack/sub-skills/training-configs/SKILL.md`, `schnetpack/sub-skills/models-atomistic/SKILL.md`, `schnetpack/sub-skills/interfaces-md/SKILL.md`.

### `torchdrug`

Role: TorchDrug provides PyTorch graph-learning workflows for molecular property prediction, molecular pretraining, generation, retrosynthesis, and chemistry datasets.
Read when: Tasks mention TorchDrug, TorchProtein, SMILES, RDKit molecule graphs, ClinTox, BACE, Tox21, ZINC250k, USPTO50k, GIN/RGCN molecular models, GCPN, GraphAF, G2Gs, retrosynthesis, scaffold splits, molecule property prediction, molecule generation, or drug-discovery graph neural networks.
Best for: Building or debugging TorchDrug molecular datasets, feature choices, graph neural model/task pairs, Engine wiring, molecular generation planning, and retrosynthesis pipelines.
Avoid when: Use RDKit/Datamol-specific skills for standalone cheminformatics operations, simulation skills for molecular dynamics, or generic PyTorch skills when no TorchDrug data/model/task APIs are involved.
Useful entry points: `torchdrug/SKILL.md`, `torchdrug/sub-skills/graph-data/SKILL.md`, `torchdrug/sub-skills/molecular-workflows/SKILL.md`, `torchdrug/sub-skills/training-engine/SKILL.md`.

<!-- DISCO_SCENARIO:molecular-ml-drug-discovery-and-chemistry-workflows:END -->

## How To Choose

Choose by chemistry surface: RDKit/Datamol for molecule processing, Chemprop/DeepChem for molecular ML, OpenMM/MDAnalysis for simulation and trajectory analysis, AiZynthFinder for retrosynthesis, and REINVENT for molecular design CLI workflows. Choose `aizynthfinder` when the repository-specific terms, CLIs, config sections, output filenames, or search algorithms are AiZynthFinder-specific. For pure molecule parsing or reaction chemistry without route-search workflows, use a more general chemistry/RDKit skill if available. Choose biotite for chemistry-adjacent tasks when Biotite owns the data representation or handoff: AtomArray, BondList, MOL/SDF/PDBx IO, PubChem fetches, RDKit/OpenMM/PyMOL conversion, or Vina wrapper planning. Choose a dedicated RDKit/OpenMM/MD/ML skill when Biotite is only a peripheral input format. Choose `chemprop` when the request names `chemprop`, centers on molecular property prediction: CLI training, prediction, fingerprints, data validation, Python APIs, reaction/atom-bond tasks, uncertainty, hpopt, and conversion workflows, uses its APIs or CLIs, references its configs/artifacts/errors, or asks for repository workflows in molecular ml drug discovery and chemistry workflows. Route within the skill by practical workflow: IO/prep first, then similarity, structure generation, or visualization/utilities.
