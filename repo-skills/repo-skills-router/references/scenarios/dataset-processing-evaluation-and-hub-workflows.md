# Dataset Processing, Evaluation, and Hub Workflows

## When To Read

Dataset loading, schemas, streaming, format conversion, metric/evaluator modules, benchmark task selection, result caches, data validation, and Hub or CLI workflows.

## Repo Skill Options

<!-- DISCO_SCENARIO:dataset-processing-evaluation-and-hub-workflows:START -->
### `datasets`

Role: Use `datasets` when working with Hugging Face Datasets: loading local or Hub datasets, defining Features schemas, processing/streaming datasets, converting formats, sharing to the Hub, managing cache/offline behavior, or using.
Read when: The request names `datasets` or asks for package-specific APIs, CLIs, configs, data/model artifacts, error messages, workflows, or repository maintenance that match this project.
Best for: features formats, loading local hub, processing streaming, and sharing cli cache.
Avoid when: another repo skill in this scenario matches the user's task, package, model family, data format, serving backend, or workflow more directly.
Useful entry points: `datasets/SKILL.md`, `datasets/sub-skills/features-formats/`, `datasets/sub-skills/loading-local-hub/`, `datasets/sub-skills/processing-streaming/`, `datasets/sub-skills/sharing-cli-cache/`.

### `deepvariant`

Role: DeepVariant-specific repo skill for planning and troubleshooting germline, family, pangenome-aware, stage-level, training, and analysis workflows around genomic variant calling.
Read when: User mentions DeepVariant, DeepTrio, run_deepvariant, run_deeptrio, run_pangenome_aware_deepvariant, make_examples, call_variants, postprocess_variants, gVCF, VCF stats, show_examples, haploid/PAR flags, GBZ pangenome, DeepVariant custom model, or DeepVariant training examples.
Best for: DeepVariant command previews, Docker/Singularity mount review, BAM/CRAM/FASTA/index compatibility checks, DeepTrio family-output planning, pangenome-aware GBZ workflows, sharded stage contracts, custom-model metadata review, and post-run report interpretation.
Avoid when: The task is raw read alignment, genome assembly, generic VCF parsing, somatic calling with DeepSomatic, unrelated omics analysis, or maintaining the repository source code rather than using DeepVariant workflows.
Useful entry points: `deepvariant/SKILL.md`, `deepvariant/sub-skills/germline-calling/SKILL.md`, `deepvariant/sub-skills/trio-calling/SKILL.md`, `deepvariant/sub-skills/pangenome-aware-calling/SKILL.md`, `deepvariant/sub-skills/pipeline-stages/SKILL.md`, `deepvariant/sub-skills/training-custom-models/SKILL.md`, `deepvariant/sub-skills/analysis-visualization/SKILL.md`.

### `evaluate`

Role: Use Hugging Face Evaluate to load metrics, comparisons, and measurements; compute and combine results; run evaluator pipelines; create custom modules; troubleshoot optional dependencies, cache, Hub, and CLI workflows.
Read when: The request names `evaluate` or asks for package-specific APIs, CLIs, configs, data/model artifacts, error messages, workflows, or repository maintenance that match this project.
Best for: evaluator pipelines, hub and cli, module computation, and module loading.
Avoid when: another repo skill in this scenario matches the user's task, package, model family, data format, serving backend, or workflow more directly.
Useful entry points: `evaluate/SKILL.md`, `evaluate/sub-skills/evaluator-pipelines/`, `evaluate/sub-skills/hub-and-cli/`, `evaluate/sub-skills/module-computation/`, `evaluate/sub-skills/module-loading/`.

### `fastmri`

Role: Use `fastmri` when dataset/evaluation work depends on fastMRI split names, HDF5 keys, challenge target keys, reconstruction metrics, or prediction-file contracts.
Read when: Requests mention checking fastMRI `.h5` keys, `kspace`, `reconstruction_rss`, `reconstruction_esc`, prediction files with dataset `reconstruction`, fastMRI MSE/NMSE/PSNR/SSIM metrics, `fastmri.evaluate`, v2 filename conversion, zero-filled baseline files, or target/prediction filename mismatches.
Best for: Validating local fastMRI data and predictions, choosing target keys by challenge, running or explaining fastMRI metrics, and diagnosing output-file schema problems before submission-style packaging.
Avoid when: The dataset task is not fastMRI HDF5 MRI reconstruction data, does not involve k-space/reconstruction target keys, or is better handled by a general dataset library skill.
Useful entry points: `fastmri/SKILL.md`, `fastmri/sub-skills/data-loading/SKILL.md`, `fastmri/sub-skills/evaluation-submission/SKILL.md`.

### `great-expectations`

Role: Guides coding agents through current GX Core Python APIs for context setup, data connection, expectation suites, validations, checkpoints, actions, and Data Docs.
Read when: great_expectations, GX Core, gx.get_context, ExpectationSuite, ValidationDefinition, Checkpoint, Data Docs, datasource, data asset, batch definition, expectation, validation result, unexpected rows. Python import great_expectations, package API inspection, public API signatures, no CLI entry point, optional dependencies, pydantic validation errors.
Best for: Building or debugging local GX Core workflows with Python APIs, pandas/filesystem/SQL assets, expectation suites, validation runs, result-format choices, checkpoints, and safe notification/Data Docs configuration. Writing scripts or tests that import GX, instantiate public GX objects, and verify behavior with tiny local fixtures without relying on original repository files.
Avoid when: The task is exclusively about GX Cloud UI operations, unrelated data validation frameworks, contributed third-party expectation packages, or backend service administration rather than GX Core code. The user is asking for maintainer-only repository release, docs build, CI, lint, or contribution workflow automation.
Useful entry points: `great-expectations/SKILL.md`, `great-expectations/sub-skills/contexts-and-configuration/SKILL.md`, `great-expectations/sub-skills/datasources-and-assets/SKILL.md`, `great-expectations/sub-skills/expectations-and-suites/SKILL.md`, `great-expectations/sub-skills/validations-and-results/SKILL.md`, `great-expectations/sub-skills/checkpoints-actions-and-data-docs/SKILL.md`, `great-expectations/scripts/inspect_gx_environment.py`.

### `hail`

Role: Covers Hail-specific genomic dataset import/export formats, schemas, row/column/entry axes, sparse VDS representation, and data validation/troubleshooting.
Read when: User asks about VCF, PLINK, BGEN, GVCF, Table, MatrixTable, VariantDataset, contig recoding, reference genomes, local alleles, sample annotations, schema inspection, or Hail data import/export.
Best for: Hail-specific genomic data processing, format conversion, schema/field troubleshooting, QC preparation, and self-contained recipe templates.
Avoid when: The task is only generic dataset loading/evaluation outside Hail or requires a different dataset/evaluation framework with no Hail APIs.
Useful entry points: `hail/SKILL.md`, `hail/sub-skills/tables-and-expressions/SKILL.md`, `hail/sub-skills/genomics-analysis/SKILL.md`, `hail/sub-skills/variant-datasets/SKILL.md`.

### `mteb`

Role: Use MTEB to evaluate embedding models, select tasks and benchmarks, validate model protocols, run CLI workflows, inspect result caches, and contribute tasks/models/benchmarks.
Read when: The request names `mteb` or asks for package-specific APIs, CLIs, configs, data/model artifacts, error messages, workflows, or repository maintenance that match this project.
Best for: cli and automation, contributing to mteb, evaluation workflows, models and encoders, results and leaderboard, and tasks and benchmarks.
Avoid when: another repo skill in this scenario matches the user's task, package, model family, data format, serving backend, or workflow more directly.
Useful entry points: `mteb/SKILL.md`, `mteb/sub-skills/cli-and-automation/`, `mteb/sub-skills/contributing-to-mteb/`, `mteb/sub-skills/evaluation-workflows/`, `mteb/sub-skills/models-and-encoders/`, `mteb/sub-skills/results-and-leaderboard/`, `mteb/sub-skills/tasks-and-benchmarks/`.

### `nemo`

Role: Adds NeMo-specific speech/audio manifest, Lhotse, tarred dataset, tokenizer, ASR evaluator, CTC segmentation, and checkpoint utility guidance to dataset-processing tasks.
Read when: The request names NeMo manifests, audio_filepath/duration/text JSONL, Lhotse CutSet or Shar, tarred audio datasets, NeMo tokenizer scripts, duration bins, dataset weights, ASR evaluator, CTC segmentation, speech data explorer, customization dataset preparation, or NeMo conversion utilities.
Best for: Validating and planning NeMo speech/audio data pipelines, sharding audio manifests, estimating duration bins, routing ASR/TTS/audio data formats, and preflighting NeMo evaluator or tokenizer workflows.
Avoid when: Use a generic dataset-processing skill when the data is not speech/audio and does not use NeMo JSON manifests, NeMo tools, Lhotse, tarred audio, or NeMo evaluators.
Useful entry points: `nemo/SKILL.md`, `nemo/sub-skills/data-tools/SKILL.md`, `nemo/sub-skills/asr/SKILL.md`, `nemo/sub-skills/tts/SKILL.md`, `nemo/sub-skills/audio/SKILL.md`.

<!-- DISCO_SCENARIO:dataset-processing-evaluation-and-hub-workflows:END -->

## How To Choose

Use dataset and evaluation packages here when the request is about data or metrics plumbing; route model benchmark harnesses to language-model-evaluation-workflows when LLM evaluation configuration is primary. Choose `datasets` when the request names `datasets`, centers on working with Hugging Face Datasets: loading local or Hub datasets, defining Features schemas, processing/streaming datasets, converting formats, sharing to the Hub, managing cache/offline behavior, or using datasets-cli, uses its APIs or CLIs, references its configs/artifacts/errors, or asks for repository workflows in dataset processing evaluation and hub workflows. Choose `deepvariant` when DeepVariant or DeepTrio is the named tool or when the request involves DeepVariant-specific model types, wrappers, stage files, helper scripts, or errors. Choose broader dataset/evaluation skills for generic data plumbing and a different genomics-specific skill if the tool is not DeepVariant. Choose `evaluate` when the request names `evaluate`, centers on Use Hugging Face Evaluate to load metrics, comparisons, and measurements; compute and combine results; run evaluator pipelines; create custom modules; troubleshoot optional dependencies, cache, Hub, and CLI workflows, uses its APIs or CLIs, references its configs/artifacts/errors, or asks for repository workflows in dataset processing evaluation and hub workflows.
