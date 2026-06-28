# Medical Imaging and Segmentation Workflows

## When To Read

Medical image transforms, nnU-Net planning/training/inference, MONAI bundles, TorchIO patch workflows, healthcare segmentation, and 3D image augmentation.

## Repo Skill Options

<!-- DISCO_SCENARIO:medical-imaging-and-segmentation-workflows:START -->
### `antspy`

Role: Provides repo-specific guidance for the ANTsPy/antspyx Python package and its ANTs/ITK-backed medical image workflows.
Read when: User mentions ANTsPy, antspyx, import ants, ANTsImage, ANTs registration, apply_transforms, Atropos, kmeans_segmentation, iMath, medical image registration, or ANTsPy plotting/label workflows.
Best for: Python ANTsPy package usage: image metadata, image operations, registration, transform application, segmentation/label analysis, plotting, interop, and learning helper utilities.
Avoid when: Use MONAI/nnU-Net/TorchIO skills for model training, bundle workflows, patch samplers, or deep learning frameworks not centered on ANTsPy; use generic Python maintenance skills for unrelated repo editing.
Useful entry points: `antspy/SKILL.md`, `antspy/sub-skills/image-core/SKILL.md`, `antspy/sub-skills/image-ops-math/SKILL.md`, `antspy/sub-skills/registration-transforms/SKILL.md`, `antspy/sub-skills/segmentation-labels/SKILL.md`, `antspy/sub-skills/visualization-interop/SKILL.md`, `antspy/sub-skills/learning-deeplearn/SKILL.md`.

### `dipy`

Role: Provides self-contained Dipy routing, API references, CLI workflow guidance, and safe smoke probes for diffusion MRI analysis workflows.
Read when: dipy, DIPY, diffusion MRI, DWI, bvals, bvecs, GradientTable, TensorModel, CSD, DKI, ODF, peaks, tractography, streamlines, QuickBundles, RecoBundles, BundleWarp, SyN, affine registration, PAM5, StatefulTractogram, dipy_* commands.
Best for: Using or debugging Dipy as a package: loading diffusion data, preprocessing, fitting reconstruction models, generating tractography, segmenting bundles, registering images/streamlines, and building Dipy CLI commands.
Avoid when: The task is generic repository maintenance unrelated to Dipy usage, clinical deployment decision support, non-Dipy medical imaging packages, or deep-learning model training outside Dipy optional helpers.
Useful entry points: `dipy/SKILL.md`, `dipy/sub-skills/io-data/SKILL.md`, `dipy/sub-skills/reconstruction-models/SKILL.md`, `dipy/sub-skills/tracking-segmentation/SKILL.md`, `dipy/sub-skills/denoising-preprocessing/SKILL.md`, `dipy/sub-skills/registration-alignment/SKILL.md`, `dipy/sub-skills/cli-workflows/SKILL.md`.

### `monai`

Role: Use MONAI, the PyTorch-based medical imaging AI toolkit, for data/transforms, modeling/inference, training/evaluation, Bundle configs, and Auto3DSeg/app workflows.
Read when: The request names `monai` or asks for package-specific APIs, CLIs, configs, data/model artifacts, error messages, workflows, or repository maintenance that match this project.
Best for: apps auto3dseg, bundle config, data transforms, modeling inference, and training evaluation.
Avoid when: another repo skill in this scenario matches the user's task, package, model family, data format, serving backend, or workflow more directly.
Useful entry points: `monai/SKILL.md`, `monai/sub-skills/apps-auto3dseg/`, `monai/sub-skills/bundle-config/`, `monai/sub-skills/data-transforms/`, `monai/sub-skills/modeling-inference/`, `monai/sub-skills/training-evaluation/`.

### `nnunetv2`

Role: Use nnU-Net v2 for medical image segmentation workflows: dataset preparation, planning/preprocessing, training, inference/evaluation, model sharing, and customization.
Read when: The request names `nnunetv2` or asks for package-specific APIs, CLIs, configs, data/model artifacts, error messages, workflows, or repository maintenance that match this project.
Best for: customization extension, data preparation, inference evaluation, planning preprocessing, and training configuration.
Avoid when: another repo skill in this scenario matches the user's task, package, model family, data format, serving backend, or workflow more directly.
Useful entry points: `nnunetv2/SKILL.md`, `nnunetv2/sub-skills/customization-extension/`, `nnunetv2/sub-skills/data-preparation/`, `nnunetv2/sub-skills/inference-evaluation/`, `nnunetv2/sub-skills/planning-preprocessing/`, `nnunetv2/sub-skills/training-configuration/`.

### `simpleitk`

Role: Provides self-contained SimpleITK guidance for Python image analysis workflows plus build/wrapping triage for optional compiled features.
Read when: User mentions SimpleITK, simpleitk, import SimpleITK as sitk, ReadImage, ImageSeriesReader, GetArrayFromImage, ImageRegistrationMethod, Resample, DICOM, ElastixImageFilter, TransformixImageFilter, WRAP_PYTHON, or SimpleITK_USE_ELASTIX.
Best for: Preserving image geometry, NumPy bridge pitfalls, ImageIO/DICOM workflows, filter and segmentation recipes, registration/transform setup, and deciding binary install versus source/SuperBuild.
Avoid when: The task is about deep-learning medical segmentation frameworks such as MONAI, nnU-Net, or TorchIO rather than SimpleITK APIs or builds.
Useful entry points: `simpleitk/SKILL.md`, `simpleitk/sub-skills/image-core/SKILL.md`, `simpleitk/sub-skills/io-and-data/SKILL.md`, `simpleitk/sub-skills/filtering-segmentation/SKILL.md`, `simpleitk/sub-skills/registration-transforms/SKILL.md`, `simpleitk/sub-skills/builds-and-wrapping/SKILL.md`.

### `tiatoolbox`

Role: Use `tiatoolbox` for TIAToolbox package workflows in digital pathology: WSI I/O, preprocessing, model inference, annotation storage/querying, visualization, and CLI planning.
Read when: User mentions TIAToolbox, TIA Toolbox, tiatoolbox, WSIReader, PatchPredictor, SemanticSegmentor, MultiTaskSegmentor, AnnotationStore, stain-norm, tissue-mask, whole-slide pathology images, or pathology visualization overlays.
Best for: Using TIAToolbox APIs or CLI to read WSIs, prepare image patches and masks, run pretrained/custom pathology inference, inspect annotation outputs, visualize overlays, and troubleshoot installation/backend/configuration issues.
Avoid when: The task is generic Python repo maintenance, Docker/release automation, benchmark execution, or unrelated medical imaging packages such as MONAI, nnU-Net, or TorchIO.
Useful entry points: `tiatoolbox/SKILL.md`, `tiatoolbox/sub-skills/wsi-io/SKILL.md`, `tiatoolbox/sub-skills/image-preprocessing/SKILL.md`, `tiatoolbox/sub-skills/model-inference/SKILL.md`, `tiatoolbox/sub-skills/annotation-visualization/SKILL.md`, `tiatoolbox/sub-skills/cli-and-configuration/SKILL.md`.

### `torchio`

Role: 0 for medical image loading, preprocessing, augmentation, patch-based training/inference, CLI conversion, and I/O troubleshooting.
Read when: The request names `torchio` or asks for package-specific APIs, CLIs, configs, data/model artifacts, error messages, workflows, or repository maintenance that match this project.
Best for: cli and io, data model, patch workflows, and transforms.
Avoid when: another repo skill in this scenario matches the user's task, package, model family, data format, serving backend, or workflow more directly.
Useful entry points: `torchio/SKILL.md`, `torchio/sub-skills/cli-and-io/`, `torchio/sub-skills/data-model/`, `torchio/sub-skills/patch-workflows/`, `torchio/sub-skills/transforms/`.

### `totalsegmentator`

Role: Use this repo skill for TotalSegmentator-specific task discovery, CLI/API segmentation, runtime setup, output parsing, DICOM formatting, auxiliary analysis, and retraining boundaries.
Read when: User mentions TotalSegmentator, totalsegmentator, TotalSegmentator CLI, totalseg_info, totalseg_combine_masks, CT/MR segmentation, --roi_subset, --report, statistics.json, DICOM SEG, RTSTRUCT, model weights, license, body stats, contrast phase, modality prediction, Evans index, or TotalSegmentator nnU-Net retraining.
Best for: Planning and troubleshooting TotalSegmentator runs; discovering valid tasks/classes; building reproducible segmentation commands; parsing run reports/statistics; configuring weights/licenses/offline use; validating DICOM/NIfTI format choices; using secondary analysis CLIs; understanding advanced retraining/evaluation workflows.
Avoid when: Use a general MONAI, nnU-Net, TorchIO, or medical-imaging skill when the task is not TotalSegmentator-specific; avoid using this skill as clinical validation guidance or as a generic medical diagnosis tool.
Useful entry points: `totalsegmentator/SKILL.md`, `totalsegmentator/sub-skills/capability-discovery/SKILL.md`, `totalsegmentator/sub-skills/segmentation-workflows/SKILL.md`, `totalsegmentator/sub-skills/outputs-and-statistics/SKILL.md`, `totalsegmentator/sub-skills/runtime-configuration/SKILL.md`, `totalsegmentator/sub-skills/dicom-and-formats/SKILL.md`, `totalsegmentator/sub-skills/auxiliary-analysis/SKILL.md`, `totalsegmentator/sub-skills/advanced-training/SKILL.md`.

<!-- DISCO_SCENARIO:medical-imaging-and-segmentation-workflows:END -->

## How To Choose

Choose by medical imaging package and workflow: MONAI for healthcare model/bundle workflows, nnU-Net for nnU-Net planning/training/inference, and TorchIO for 3D augmentation and patch sampling. Choose `antspy` when the task is explicitly about ANTsPy/antspyx or ANTs-style Python image registration/segmentation APIs. Choose adjacent medical imaging skills only when the named package or workflow is MONAI, nnU-Net, TorchIO, TotalSegmentator, SimpleITK, or a neural-network training/inference pipeline rather than ANTsPy usage. Choose `dipy` when the request names Dipy or Dipy-specific APIs/CLIs. For generic medical segmentation frameworks choose MONAI, nnU-Net, or TorchIO skills when those packages are named instead; choose Python repository maintenance only when editing Dipy source code rather than using Dipy workflows. Choose `monai` when the request names `monai`, centers on data/transforms, modeling/inference, training/evaluation, Bundle configs, and Auto3DSeg/app workflows, uses its APIs or CLIs, references its configs/artifacts/errors, or asks for repository workflows in medical imaging and segmentation workflows. Choose `simpleitk` when SimpleITK itself owns the image object, IO, filter, registration, transform, or build surface named by the request; choose model-family skills when the user primarily asks for neural network training/inference workflows.
