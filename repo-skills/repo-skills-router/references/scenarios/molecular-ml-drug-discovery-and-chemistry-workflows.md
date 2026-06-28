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

### `chemprop`

Role: 3 for molecular property prediction: CLI training, prediction, fingerprints, data validation, Python APIs, reaction/atom-bond tasks, uncertainty, hpopt, and conversion workflows.
Read when: The request names `chemprop` or asks for package-specific APIs, CLIs, configs, data/model artifacts, error messages, workflows, or repository maintenance that match this project.
Best for: data featurization, prediction fingerprints, python api modeling, specialized molecular tasks, training cli, and uncertainty advanced.
Avoid when: another repo skill in this scenario matches the user's task, package, model family, data format, serving backend, or workflow more directly.
Useful entry points: `chemprop/SKILL.md`, `chemprop/sub-skills/data-featurization/`, `chemprop/sub-skills/prediction-fingerprints/`, `chemprop/sub-skills/python-api-modeling/`, `chemprop/sub-skills/specialized-molecular-tasks/`, `chemprop/sub-skills/training-cli/`, `1 more sub-skills`.

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

### `openmm`

Role: Use OpenMM for molecular simulation workflows, force-field/model preparation, custom forces/integrators, platform/performance diagnostics, and maintainer extension work.
Read when: The request names `openmm` or asks for package-specific APIs, CLIs, configs, data/model artifacts, error messages, workflows, or repository maintenance that match this project.
Best for: custom forces integrators, development extensions, force fields modeling, platforms performance, and simulation workflows.
Avoid when: another repo skill in this scenario matches the user's task, package, model family, data format, serving backend, or workflow more directly.
Useful entry points: `openmm/SKILL.md`, `openmm/sub-skills/custom-forces-integrators/`, `openmm/sub-skills/development-extensions/`, `openmm/sub-skills/force-fields-modeling/`, `openmm/sub-skills/platforms-performance/`, `openmm/sub-skills/simulation-workflows/`.

### `rdkit`

Role: Use for RDKit cheminformatics tasks: molecule parsing and validation, descriptors and fingerprints, conformers and drawing, reactions and standardization, data integrations, optional Contrib utilities, or RDKit repository.
Read when: The request names `rdkit` or asks for package-specific APIs, CLIs, configs, data/model artifacts, error messages, workflows, or repository maintenance that match this project.
Best for: conformers drawing, contrib utilities, data cli integration, descriptors fingerprints, molecule io core, and 2 other focused workflows.
Avoid when: another repo skill in this scenario matches the user's task, package, model family, data format, serving backend, or workflow more directly.
Useful entry points: `rdkit/SKILL.md`, `rdkit/sub-skills/conformers-drawing/`, `rdkit/sub-skills/contrib-utilities/`, `rdkit/sub-skills/data-cli-integration/`, `rdkit/sub-skills/descriptors-fingerprints/`, `rdkit/sub-skills/molecule-io-core/`, `2 more sub-skills`.

### `reinvent4`

Role: Routes REINVENT4 molecular design tasks to focused workflow sub-skills with self-contained config, validation, and troubleshooting guidance.
Read when: REINVENT4, reinvent, reinvent_datapre, sampling.toml, scoring.toml, transfer_learning.toml, staged_learning.toml, data_pipeline.toml, enumeration.toml, LibInvent, LinkInvent, Mol2Mol, PepInvent, scoring component, comp_ plugin, @add_tag, RDKit, OpenEye, Chemprop.
Best for: Preparing and validating REINVENT4 run configs, choosing CLI flags, designing scoring functions/plugins, preprocessing SMILES, and troubleshooting optional dependencies without reopening the source repo.
Avoid when: The task is general cheminformatics unrelated to REINVENT4, asks to reproduce the REINVENT4 paper from scratch, or requires long production training/external scoring execution without user approval.
Useful entry points: `reinvent4/SKILL.md`, `reinvent4/sub-skills/sampling/SKILL.md`, `reinvent4/sub-skills/scoring/SKILL.md`, `reinvent4/sub-skills/learning/SKILL.md`, `reinvent4/sub-skills/data-pipeline/SKILL.md`, `reinvent4/sub-skills/enumeration/SKILL.md`.

<!-- DISCO_SCENARIO:molecular-ml-drug-discovery-and-chemistry-workflows:END -->

## How To Choose

Choose by chemistry surface: RDKit/Datamol for molecule processing, Chemprop/DeepChem for molecular ML, OpenMM/MDAnalysis for simulation and trajectory analysis, AiZynthFinder for retrosynthesis, and REINVENT for molecular design CLI workflows. Choose `aizynthfinder` when the repository-specific terms, CLIs, config sections, output filenames, or search algorithms are AiZynthFinder-specific. For pure molecule parsing or reaction chemistry without route-search workflows, use a more general chemistry/RDKit skill if available. Choose `chemprop` when the request names `chemprop`, centers on molecular property prediction: CLI training, prediction, fingerprints, data validation, Python APIs, reaction/atom-bond tasks, uncertainty, hpopt, and conversion workflows, uses its APIs or CLIs, references its configs/artifacts/errors, or asks for repository workflows in molecular ml drug discovery and chemistry workflows. Choose `datamol` over generic chemistry guidance when user code imports datamol as dm or when datamol-specific defaults, file helpers, fingerprint names, clustering helpers, reaction wrappers, visualization helpers, or utility functions matter. Route within the skill by practical workflow: IO/prep first, then similarity, structure generation, or visualization/utilities. Choose `mdanalysis` when the user is writing or debugging MDAnalysis code.
