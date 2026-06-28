# Protein Structure Prediction and Design Workflows

## When To Read

AlphaFold, ColabFold, Boltz, Chai-1, ESM, ProteinMPNN, RFdiffusion, MSA generation, structure prediction outputs, protein backbone generation, binder design, and sequence design.

## Repo Skill Options

<!-- DISCO_SCENARIO:protein-structure-prediction-and-design-workflows:START -->
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

### `openfold`

Role: Provides self-contained OpenFold-specific routing, command planning, data-layout validation, training planning, install troubleshooting, and programmatic API guidance.
Read when: Requests mention OpenFold, AlphaFold-compatible inference, run_pretrained_openfold.py, train_openfold.py, SoloSeq, multimer, precomputed alignments, OpenProteinSet, OpenFold parameters, DeepSpeed OpenFold training, attn_core_inplace_cuda, or OpenFold config/model APIs.
Best for: Planning OpenFold inference or training commands safely, validating OpenFold FASTA/MSA/mmCIF/alignment/cache layouts, diagnosing OpenFold installation/extension/backend failures, and using OpenFold config/weight/protein APIs.
Avoid when: The task is about a different protein framework such as ColabFold, ESM, Boltz, Chai-1, ProteinMPNN, or RFdiffusion without OpenFold-specific code or assets.
Useful entry points: `openfold/SKILL.md`, `openfold/sub-skills/installation-assets/SKILL.md`, `openfold/sub-skills/inference/SKILL.md`, `openfold/sub-skills/data-preparation/SKILL.md`, `openfold/sub-skills/training/SKILL.md`, `openfold/sub-skills/model-apis/SKILL.md`.

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
Useful entry points: `rfdiffusion/SKILL.md`, `rfdiffusion/sub-skills/binder-design/`, `rfdiffusion/sub-skills/guided-potentials/`, `rfdiffusion/sub-skills/macrocycle-design/`, `rfdiffusion/sub-skills/motif-scaffolding/`, `rfdiffusion/sub-skills/partial-diffusion/`, `3 more sub-skills`.

<!-- DISCO_SCENARIO:protein-structure-prediction-and-design-workflows:END -->

## How To Choose

Choose structure predictors for structure output tasks, ESM for protein language model embeddings or variant effects, ProteinMPNN for sequence design, and RFdiffusion for backbone/binder generation. Choose `alphafold3` when the request names `alphafold3`, centers on AlphaFold 3 input preparation, prediction command planning, output interpretation, and Python API inspection. Covers the local AlphaFold 3 inference package, its JSON dialect, run_alphafold workflow, outputs, troubleshooting, and safe helper scripts, uses its APIs or CLIs, references its configs/artifacts/errors, or asks for repository workflows in protein structure prediction and design workflows. Choose `boltz` when Boltz-specific CLI flags, input schemas, outputs, training configs, preprocessing scripts, or evaluation assets matter; choose broader ML or scientific Python skills for non-Boltz implementation work. Choose `chai-lab` for Chai-specific CLI/API/data-format tasks. Route within it by workflow: inference, FASTA inputs, MSA/templates, or restraints/glycans. Prefer other bioinformatics skills only when the user names a different package or a non-Chai workflow. Choose model-embeddings for representations/contacts, structure-prediction for ESMFold PDB outputs, inverse-folding for ESM-IF1 backbone-conditioned design/scoring, and variant-effect-prediction for ESM-1v/MSA DMS mutation scoring.
