# Protein Structure Prediction and Design Workflows

## When To Read

AlphaFold, ColabFold, Boltz, Chai-1, ESM, ProteinMPNN, RFdiffusion, MSA generation, structure prediction outputs, protein backbone generation, binder design, and sequence design.

## Repo Skill Options

<!-- DISCO_SCENARIO:protein-structure-prediction-and-design-workflows:START -->
### `alphafold`

Role: AlphaFold-specific skill for planning and troubleshooting AlphaFold 2.x protein structure prediction workflows without running expensive prediction or data-download operations by default.
Read when: The task names AlphaFold, run_alphafold, AlphaFold-Multimer, pLDDT, PAE, pTM, ipTM, AlphaFold DB, AlphaFold Server JSON, FASTA protein prediction, MSA/template database setup, BFD/UniRef/MGnify/PDB70/PDB SeqRes data paths, OpenMM relaxation, or Docker/GPU AlphaFold execution.
Best for: Generating safe AlphaFold setup plans, validating FASTA and database paths, constructing direct run_alphafold commands, inspecting model presets/configuration, interpreting prediction confidence artifacts, creating Server JSON, and diagnosing relaxation or dependency failures.
Avoid when: Avoid for non-AlphaFold protein design tools such as RFdiffusion or ProteinMPNN, general molecular simulation unrelated to AlphaFold relaxation, or generic Docker/JAX troubleshooting without AlphaFold-specific flags, data layout, or output artifacts.
Useful entry points: `alphafold/SKILL.md`, `alphafold/sub-skills/docker-and-data-setup/SKILL.md`, `alphafold/sub-skills/prediction-cli/SKILL.md`, `alphafold/sub-skills/input-data-and-formats/SKILL.md`, `alphafold/sub-skills/model-config-and-api/SKILL.md`, `alphafold/sub-skills/outputs-and-confidence/SKILL.md`, `alphafold/sub-skills/relaxation/SKILL.md`.

### `alphafold3`

Role: Use `alphafold3` for AlphaFold 3 input preparation, prediction command planning, output interpretation, and Python API inspection. Covers the local AlphaFold 3 inference package, its JSON dialect, run_alphafold workflow, outputs.
Read when: The request names `alphafold3` or asks for package-specific APIs, CLIs, configs, data/model artifacts, error messages, workflows, or repository maintenance that match this project.
Best for: input preparation, output interpretation, python apis, and running predictions.
Avoid when: another repo skill in this scenario matches the user's task, package, model family, data format, serving backend, or workflow more directly.
Useful entry points: `alphafold3/SKILL.md`, `alphafold3/sub-skills/input-preparation/`, `alphafold3/sub-skills/output-interpretation/`, `alphafold3/sub-skills/python-apis/`, `alphafold3/sub-skills/running-predictions/`.

### `boltz`

Role: Provides self-contained routing and workflow guidance for the Boltz Python package across prediction, input schemas, output interpretation, data preparation, training, and evaluation.
Read when: User mentions Boltz, boltz predict, Boltz-1, Boltz-2, biomolecular interaction prediction, affinity_pred_value, affinity_probability_binary, MSA server, custom MSA, protein-ligand YAML, or Boltz training/evaluation scripts.
Best for: Writing and validating Boltz YAML/FASTA inputs, constructing boltz predict commands, diagnosing MSA/cache/GPU issues, preparing training data, auditing training configs, and summarizing Boltz prediction/evaluation outputs.
Avoid when: The task is generic molecular modeling unrelated to Boltz, asks for paper reproduction rather than package usage, or requires closed-source AlphaFold/Chai APIs without Boltz inputs or outputs.
Useful entry points: `boltz/SKILL.md`, `boltz/sub-skills/prediction/SKILL.md`, `boltz/sub-skills/data-preparation/SKILL.md`, `boltz/sub-skills/training/SKILL.md`, `boltz/sub-skills/evaluation/SKILL.md`.

### `chai-lab`

Role: Provides self-contained Chai Lab routing, API/CLI usage, input validation, MSA/template preparation, restraint/glycan guidance, and troubleshooting.
Read when: User mentions chai_lab, chai-lab, Chai-1, run_inference, fold, .aligned.pqt, a3m-to-pqt, template m8, contact restraints, pocket restraints, covalent bonds, or glycan syntax.
Best for: Generating Chai fold commands/scripts, validating Chai FASTA/MSA/restraint inputs, staging ColabFold outputs for Chai, and diagnosing Chai-specific runtime failures.
Avoid when: The task is general molecular modeling unrelated to Chai Lab, asks for another folding package, or requires reproducing benchmark science rather than using the Chai package interfaces.
Useful entry points: `chai-lab/SKILL.md`, `chai-lab/sub-skills/cli-inference/SKILL.md`, `chai-lab/sub-skills/input-data-formats/SKILL.md`, `chai-lab/sub-skills/msa-templates/SKILL.md`, `chai-lab/sub-skills/restraints-glycans/SKILL.md`.

### `colabfold`

Role: Use ColabFold for protein structure prediction workflows: validate FASTA/CSV/A3M inputs, generate MSAs, plan batch predictions, inspect outputs, and troubleshoot optional AlphaFold, MMseqs2, JAX, GPU, and OpenMM dependencies.
Read when: The request names `colabfold` or asks for package-specific APIs, CLIs, configs, data/model artifacts, error messages, workflows, or repository maintenance that match this project.
Best for: batch prediction, inputs and formats, msa search, and relaxation and outputs.
Avoid when: another repo skill in this scenario matches the user's task, package, model family, data format, serving backend, or workflow more directly.
Useful entry points: `colabfold/SKILL.md`, `colabfold/sub-skills/batch-prediction/`, `colabfold/sub-skills/inputs-and-formats/`, `colabfold/sub-skills/msa-search/`, `colabfold/sub-skills/relaxation-and-outputs/`.

### `esm`

Role: Provides self-contained routing and workflow guidance for using fair-esm protein language models and bundled command helpers.
Read when: User mentions ESM, fair-esm, esm.pretrained, esm-extract, esm-fold, ESMFold, ESM-IF1, ESM-1v, MSA Transformer, protein FASTA embeddings, PDB prediction, DMS mutation scoring, or inverse folding.
Best for: Computing protein embeddings/contacts, generating PDB structures from sequences, designing/scoring sequences from backbones, and scoring DMS variants with ESM-family models.
Avoid when: The task is unrelated to protein sequence/structure modeling, asks for general Hugging Face ESM usage without fair-esm-specific APIs, or requires Atlas bulk data acquisition as the main workflow.
Useful entry points: `esm/SKILL.md`, `esm/sub-skills/model-embeddings/SKILL.md`, `esm/sub-skills/structure-prediction/SKILL.md`, `esm/sub-skills/inverse-folding/SKILL.md`, `esm/sub-skills/variant-effect-prediction/SKILL.md`.

### `omega-fold`

Role: Use omega-fold for OmegaFold-specific FASTA-to-PDB inference, CLI command construction, FASTA/PDB handling, model config/API inspection, and dependency/backend troubleshooting.
Read when: The task names OmegaFold or omegafold, asks for de novo protein structure prediction from primary sequence, uses FASTA input to generate PDB output, mentions OmegaFold model 1 or model 2 weights, references --subbatch_size/--num_cycle/--weights_file, needs pLDDT-like confidence in PDB B-factors, or needs APIs such as make_config, OmegaFold.forward, pipeline.fasta2inputs, or pipeline.save_pdb.
Best for: OmegaFold command-line inference, no-download CLI and API smoke checks, choosing model/device/resource flags, validating FASTA records before prediction, interpreting one-PDB-per-sequence outputs and confidence B-factors, and using OmegaFold's Python model/config/pipeline helpers.
Avoid when: Use a different protein-structure skill for AlphaFold, ColabFold, Boltz, Chai-1, ESMFold, ProteinMPNN, RFdiffusion, binder design, sequence design, MSA generation outside OmegaFold, training/fine-tuning, or general PDB editing unrelated to OmegaFold outputs.
Useful entry points: `omega-fold/SKILL.md`, `omega-fold/sub-skills/inference-cli/SKILL.md`, `omega-fold/sub-skills/data-and-outputs/SKILL.md`, `omega-fold/sub-skills/model-api/SKILL.md`.

### `openfold`

Role: Provides self-contained OpenFold-specific routing, command planning, data-layout validation, training planning, install troubleshooting, and programmatic API guidance.
Read when: Requests mention OpenFold, AlphaFold-compatible inference, run_pretrained_openfold.py, train_openfold.py, SoloSeq, multimer, precomputed alignments, OpenProteinSet, OpenFold parameters, DeepSpeed OpenFold training, attn_core_inplace_cuda, or OpenFold config/model APIs.
Best for: Planning OpenFold inference or training commands safely, validating OpenFold FASTA/MSA/mmCIF/alignment/cache layouts, diagnosing OpenFold installation/extension/backend failures, and using OpenFold config/weight/protein APIs.
Avoid when: The task is about a different protein framework such as ColabFold, ESM, Boltz, Chai-1, ProteinMPNN, or RFdiffusion without OpenFold-specific code or assets.
Useful entry points: `openfold/SKILL.md`, `openfold/sub-skills/installation-assets/SKILL.md`, `openfold/sub-skills/inference/SKILL.md`, `openfold/sub-skills/data-preparation/SKILL.md`, `openfold/sub-skills/training/SKILL.md`, `openfold/sub-skills/model-apis/SKILL.md`.

### `paddlehelix`

Role: Use paddlehelix to plan and validate PaddleHelix HelixFold family workflows without unsafe downloads or GPU inference by default.
Read when: Requests mention HelixFold, HelixFold3, HelixFold-S1, biomolecular entity JSON, MSA binaries, reduced databases, bf16 versus fp32, PaddlePaddle GPU stack, structure-prediction output directories, or malformed protein/DNA/RNA/ligand input JSON.
Best for: Preflighting HelixFold3/S1 JSON, comparing HelixFold variants, planning command substitutions, and diagnosing missing databases/checkpoints/CUDA/Paddle/MSA tools.
Avoid when: Use a non-PaddleHelix structure skill when the request is for AlphaFold, ColabFold, Boltz, Chai-1, ProteinMPNN, RFdiffusion, ESM, or structure-design workflows outside PaddleHelix.
Useful entry points: `paddlehelix/SKILL.md`, `paddlehelix/sub-skills/structure-prediction/SKILL.md`, `paddlehelix/sub-skills/protein-sequence-function/SKILL.md`.

### `protein-mpnn`

Role: Use ProteinMPNN to design protein sequences from backbones, prepare constraint JSONL inputs, interpret scores/probability outputs, retrain models, and use custom checkpoints in a local ProteinMPNN checkout.
Read when: The request names `protein-mpnn` or asks for package-specific APIs, CLIs, configs, data/model artifacts, error messages, workflows, or repository maintenance that match this project.
Best for: constraint inputs, inference design, and training custom models.
Avoid when: another repo skill in this scenario matches the user's task, package, model family, data format, serving backend, or workflow more directly.
Useful entry points: `protein-mpnn/SKILL.md`, `protein-mpnn/sub-skills/constraint-inputs/`, `protein-mpnn/sub-skills/inference-design/`, `protein-mpnn/sub-skills/training-custom-models/`.

### `protenix`

Role: Use `protenix` for Protenix-specific structure prediction, preprocessing, training-data, and model/backend workflows.
Read when: User mentions Protenix, protenix pred/json/msa/mt/prep, AlphaFold 3-style JSON, proteins with DNA/RNA/ligands/ions, MSA/template/RNA MSA, PROTENIX_ROOT_DIR, Protenix checkpoints, cuEquivariance/Triton/DeepSpeed kernels, TFG, Protenix confidence metrics, or Protenix training/fine-tuning.
Best for: Building safe Protenix commands, validating Protenix input JSON, checking MSA/template/RNA layouts, planning custom CIF preprocessing, preparing training or fine-tuning launches, and diagnosing Protenix-specific install/backend/config failures.
Avoid when: Use a different protein skill when the user names another package such as Boltz, Chai-1, ESM, ProteinMPNN, RFdiffusion, or ColabFold and Protenix is not involved; use generic PyTorch or MLOps skills for non-Protenix training infrastructure.
Useful entry points: `protenix/SKILL.md`, `protenix/sub-skills/cli-and-inference/SKILL.md`, `protenix/sub-skills/input-data-and-features/SKILL.md`, `protenix/sub-skills/msa-template-and-prep/SKILL.md`, `protenix/sub-skills/training-and-data-pipeline/SKILL.md`, `protenix/sub-skills/advanced-model-configuration/SKILL.md`.

### `rfdiffusion`

Role: Use RFdiffusion for protein backbone generation workflows, including unconditional design, motif scaffolding, partial diffusion, binder design, symmetric oligomers, guided potentials, scaffold-guided design, and RFpeptides.
Read when: The request names `rfdiffusion` or asks for package-specific APIs, CLIs, configs, data/model artifacts, error messages, workflows, or repository maintenance that match this project.
Best for: binder design, guided potentials, macrocycle design, motif scaffolding, partial diffusion, and 3 other focused workflows.
Avoid when: another repo skill in this scenario matches the user's task, package, model family, data format, serving backend, or workflow more directly.
Useful entry points: `rfdiffusion/SKILL.md`, `rfdiffusion/sub-skills/binder-design/`, `rfdiffusion/sub-skills/guided-potentials/`, `rfdiffusion/sub-skills/macrocycle-design/`, `rfdiffusion/sub-skills/motif-scaffolding/`, `rfdiffusion/sub-skills/partial-diffusion/`, `rfdiffusion/sub-skills/scaffold-guided-design/`, `rfdiffusion/sub-skills/symmetric-oligomers/`, `rfdiffusion/sub-skills/unconditional-generation/`.

### `sa-prot`

Role: Use sa-prot as the package-specific guide for SaProt structure-aware protein language modeling workflows.
Read when: The task names SaProt or asks for AA+3Di token construction, Foldseek structure sequences, pLDDT masking, SaProt_35M/650M/1.3B checkpoints, EsmTokenizer with SaProt vocab, mutation strings like V3A, ProteinGym/ClinVar zero-shot evaluation, SaProt LMDB splits, or YAML configs for Thermostability, GO, EC, DeepLoc, PPI, Contact, or pretraining.
Best for: Converting structures to SaProt input, validating model assets, writing local embedding/mutation/inverse-folding code, preparing LMDB data, adapting SaProt task YAMLs, and safely reviewing training or benchmark launchers.
Avoid when: Use a general protein-structure predictor skill for AlphaFold/ColabFold/Boltz structure prediction, ProteinMPNN sequence design, or RFdiffusion backbone generation when SaProt APIs, checkpoints, or configs are not involved.
Useful entry points: `sa-prot/SKILL.md`, `sa-prot/sub-skills/structure-sequences/SKILL.md`, `sa-prot/sub-skills/model-inference/SKILL.md`, `sa-prot/sub-skills/datasets-configs/SKILL.md`, `sa-prot/sub-skills/training-evaluation/SKILL.md`.

### `torchdrug`

Role: TorchDrug/TorchProtein covers protein sequence and structure data, GearNet/ESM/protein encoders, contact prediction, protein property/function tasks, and PPI workflows.
Read when: Tasks mention TorchProtein, ProteinNet, AlphaFoldDB, EnzymeCommission, Fluorescence, Stability, BetaLactamase, protein contact prediction, GearNet, ESM, ProteinCNN, ProteinResNet, ProteinLSTM, ProteinBERT, PackedProtein, residue features, graph construction for proteins, or protein-protein interaction prediction.
Best for: Planning TorchDrug protein datasets, feature choices, model/task pairings, ESM/GearNet caveats, ContactPrediction settings, and Engine-based protein training loops.
Avoid when: Use AlphaFold/ColabFold/Boltz/ProteinMPNN/RFdiffusion skills for structure prediction or design systems that do not use TorchDrug/TorchProtein APIs.
Useful entry points: `torchdrug/SKILL.md`, `torchdrug/sub-skills/protein-workflows/SKILL.md`, `torchdrug/sub-skills/layers-and-extensions/SKILL.md`, `torchdrug/sub-skills/training-engine/SKILL.md`.

<!-- DISCO_SCENARIO:protein-structure-prediction-and-design-workflows:END -->

## How To Choose

Choose structure predictors for structure output tasks, ESM for protein language model embeddings or variant effects, ProteinMPNN for sequence design, and RFdiffusion for backbone/binder generation. Choose alphafold when the request involves AlphaFold 2.x structure prediction setup, input validation, prediction command planning, model preset/config inspection, confidence/output interpretation, AFDB/Server JSON artifacts, or OpenMM relaxation; choose another protein-structure skill when the package or model family is not AlphaFold. Choose `alphafold3` when the request names `alphafold3`, centers on AlphaFold 3 input preparation, prediction command planning, output interpretation, and Python API inspection. Covers the local AlphaFold 3 inference package, its JSON dialect, run_alphafold workflow, outputs, troubleshooting, and safe helper scripts, uses its APIs or CLIs, references its configs/artifacts/errors, or asks for repository workflows in protein structure prediction and design workflows. Choose `boltz` when Boltz-specific CLI flags, input schemas, outputs, training configs, preprocessing scripts, or evaluation assets matter; choose broader ML or scientific Python skills for non-Boltz implementation work. Choose `chai-lab` for Chai-specific CLI/API/data-format tasks. Route within it by workflow: inference, FASTA inputs, MSA/templates, or restraints/glycans.
