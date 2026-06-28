# Computer Vision Modeling and Augmentation

## When To Read

Image augmentation, PIL/Pillow operations, vision datasets/transforms, classification and detection models, segmentation, YOLO/SAM/OpenMMLab workflows, and model export.

## Repo Skill Options

<!-- DISCO_SCENARIO:computer-vision-modeling-and-augmentation:START -->
### `albumentations`

Role: Build, debug, serialize, and integrate Albumentations 2.x augmentation pipelines for images, masks, bboxes, keypoints, volumes, and PyTorch-style datasets.
Read when: The request names `albumentations` or asks for package-specific APIs, CLIs, configs, data/model artifacts, error messages, workflows, or repository maintenance that match this project.
Best for: framework integration, pipeline composition, serialization and reproducibility, targets and formats, and transform catalog.
Avoid when: another repo skill in this scenario matches the user's task, package, model family, data format, serving backend, or workflow more directly.
Useful entry points: `albumentations/SKILL.md`, `albumentations/sub-skills/framework-integration/`, `albumentations/sub-skills/pipeline-composition/`, `albumentations/sub-skills/serialization-and-reproducibility/`, `albumentations/sub-skills/targets-and-formats/`, `albumentations/sub-skills/transform-catalog/`.

### `detectron2`

Role: Guides Detectron2 configuration, datasets, training/evaluation, inference/visualization, deployment export, and extension/project workflows.
Read when: The request names Detectron2, Detectron, model_zoo, DefaultPredictor, DefaultTrainer, DatasetCatalog, MetadataCatalog, Instances, Boxes, Mask R-CNN, Faster R-CNN, RetinaNet, PointRend, DeepLab, DensePose, ViTDet, TorchScript export, or COCO/LVIS/Cityscapes detection workflows. The request mentions Detectron2 training, DefaultTrainer, SimpleTrainer, launch, train/eval drivers, COCOEvaluator, inference_on_dataset, DetectionCheckpointer, SOLVER settings, MODEL.ROI_HEADS.NUM_CLASSES, or fine-tuning a model-zoo config. The request mentions Detectron2 export_model, TorchScript, TracingAdapter, scripting_with_instances, dump_torchscript_IR, Caffe2Tracer, ONNX export, FLOP/activation/parameter analysis, or benchmark.py in a Detectron2 context.
Best for: Using Detectron2 APIs and standard workflows for configs/model zoo, custom datasets, training/evaluation, inference/visualization, deployment export, and custom model/project extension. Detectron2 training/evaluation setup, one-GPU adaptation of model-zoo recipes, custom evaluator/checkpoint planning, and diagnosing registered-dataset or checkpoint failures. Detectron2 model export planning, TorchScript method selection, optional Caffe2/ONNX caveats, and safe analysis/benchmark command previews.
Avoid when: The task is only generic PyTorch, OpenCV image processing, or a different computer vision framework with no Detectron2-specific APIs, configs, data formats, or errors. The training task uses a non-Detectron2 framework, does not use Detectron2 data/config/model APIs, or is only about generic optimizer math. The deployment task targets a generic PyTorch model without Detectron2 structures or export APIs, or requires a production ONNX/TensorRT pipeline outside Detectron2's supported export surface.
Useful entry points: `detectron2/SKILL.md`, `detectron2/sub-skills/configuration-model-zoo/SKILL.md`, `detectron2/sub-skills/data-datasets/SKILL.md`, `detectron2/sub-skills/training-evaluation/SKILL.md`, `detectron2/sub-skills/inference-visualization/SKILL.md`, `detectron2/sub-skills/deployment-export/SKILL.md`, `detectron2/sub-skills/extension-projects/SKILL.md`.

### `grounding-dino`

Role: GroundingDINO-specific guidance for installing the package, loading configs and checkpoints, running inference, interpreting boxes/phrases, and routing advanced workflows.
Read when: Signals include groundingdino imports, GroundingDINO_SwinT_OGC.py, GroundingDINO_SwinB_cfg.py, groundingdino_swint_ogc.pth, predict/annotate/load_model, box_threshold/text_threshold, token_spans, COCO zero-shot AP, FiftyOne pseudo-labeling, Gradio GroundingDINO demos, or Grounded-SAM handoffs.
Best for: Single-image text-prompt detection, Python API usage, token-span debugging, COCO-style evaluation, pseudo-label dataset export, and safe web/downstream integration wrappers for GroundingDINO.
Avoid when: Avoid for generic object detection unrelated to GroundingDINO, Hugging Face Transformers GroundingDINO APIs that intentionally bypass this repo package, full training/fine-tuning requests, or unrelated segmentation/image-generation models without GroundingDINO detections.
Useful entry points: `grounding-dino/SKILL.md`, `grounding-dino/sub-skills/inference/`, `grounding-dino/sub-skills/evaluation/`, `grounding-dino/sub-skills/dataset-annotation/`, `grounding-dino/sub-skills/integrations/`.

### `mmdetection`

Role: Use `mmdetection` when working with MMDetection 3.x for object detection, instance/panoptic segmentation, tracking-adjacent configs, model zoo configs, inference, visualization, training/testing commands, datasets, evaluation.
Read when: The request names `mmdetection` or asks for package-specific APIs, CLIs, configs, data/model artifacts, error messages, workflows, or repository maintenance that match this project.
Best for: configuration model zoo, customization extension, datasets evaluation, inference visualization, and training testing.
Avoid when: another repo skill in this scenario matches the user's task, package, model family, data format, serving backend, or workflow more directly.
Useful entry points: `mmdetection/SKILL.md`, `mmdetection/sub-skills/configuration-model-zoo/`, `mmdetection/sub-skills/customization-extension/`, `mmdetection/sub-skills/datasets-evaluation/`, `mmdetection/sub-skills/inference-visualization/`, `mmdetection/sub-skills/training-testing/`.

### `mmsegmentation`

Role: Provides self-contained routing, commands, APIs, and troubleshooting for MMSegmentation workflows.
Read when: User mentions MMSegmentation, mmseg, OpenMMLab segmentation, MMSegInferencer, SegDataSample, mmseg config files, dataset converters, IoUMetric, decode heads, or mmseg registry errors.
Best for: Semantic segmentation/depth inference, config and dataset setup, train/test command construction, metric/output formatting, custom model components, registry debugging, and checkpoint conversion planning.
Avoid when: The task is generic PyTorch training without MMSegmentation configs, a different OpenMMLab repo such as MMDetection/MMDeploy, or pure image annotation unrelated to mmseg APIs.
Useful entry points: `mmsegmentation/SKILL.md`, `mmsegmentation/sub-skills/inference/SKILL.md`, `mmsegmentation/sub-skills/data-configuration/SKILL.md`, `mmsegmentation/sub-skills/training-evaluation/SKILL.md`, `mmsegmentation/sub-skills/model-customization/SKILL.md`.

### `open-clip`

Role: Provides self-contained routing and workflow guidance for OpenCLIP model inference, evaluation, checkpoint diagnostics, and export planning.
Read when: open_clip, open_clip_torch, create_model, create_model_and_transforms, get_tokenizer, list_pretrained, CLIP, CoCa, ViT-B-32, QuickGELU, hf-hub:, local-dir:, zero-shot, retrieval, state_dict, Hugging Face Hub export.
Best for: Loading CLIP-style models, selecting pretrained tags, creating image/text embeddings, building zero-shot classifiers, diagnosing checkpoint keys, and routing conversion/export tasks.
Avoid when: The task is general PyTorch training unrelated to OpenCLIP, generic image classification without OpenCLIP APIs, or paper-to-skills recovery rather than repository usage.
Useful entry points: `open-clip/SKILL.md`, `open-clip/sub-skills/model-inference/SKILL.md`, `open-clip/sub-skills/evaluation-conversion/SKILL.md`.

### `pillow`

Role: Use this repo skill when working with Pillow (PIL fork) image processing: opening/saving images, transforms, formats, metadata, drawing/text, fonts, and custom image plugins.
Read when: The request names `pillow` or asks for package-specific APIs, CLIs, configs, data/model artifacts, error messages, workflows, or repository maintenance that match this project.
Best for: drawing and text, formats and metadata, image core, and plugins and extension.
Avoid when: another repo skill in this scenario matches the user's task, package, model family, data format, serving backend, or workflow more directly.
Useful entry points: `pillow/SKILL.md`, `pillow/sub-skills/drawing-and-text/`, `pillow/sub-skills/formats-and-metadata/`, `pillow/sub-skills/image-core/`, `pillow/sub-skills/plugins-and-extension/`.

### `segment-anything`

Role: Use Meta Segment Anything (SAM) for prompt-based segmentation, automatic mask generation, ONNX export, browser deployment, checkpoints, optional dependencies, and troubleshooting.
Read when: The request names `segment-anything` or asks for package-specific APIs, CLIs, configs, data/model artifacts, error messages, workflows, or repository maintenance that match this project.
Best for: automatic mask generation, onnx and browser, and prompted segmentation.
Avoid when: another repo skill in this scenario matches the user's task, package, model family, data format, serving backend, or workflow more directly.
Useful entry points: `segment-anything/SKILL.md`, `segment-anything/sub-skills/automatic-mask-generation/`, `segment-anything/sub-skills/onnx-and-browser/`, `segment-anything/sub-skills/prompted-segmentation/`.

### `tiatoolbox`

Role: Use `tiatoolbox` when a vision request specifically names TIAToolbox or pathology-image APIs rather than a generic CV framework.
Read when: User asks for TIAToolbox stain normalization, tissue masking, patch extraction, image augmentation, pathology segmentation, nucleus detection, or model output overlays.
Best for: Pathology-specific CV workflows that combine image I/O, preprocessing, pretrained model engines, annotation formats, and visualization.
Avoid when: Use a generic computer-vision skill for YOLO/SAM/OpenMMLab/TorchVision requests that do not involve TIAToolbox or pathology WSI workflows.
Useful entry points: `tiatoolbox/SKILL.md`, `tiatoolbox/sub-skills/image-preprocessing/SKILL.md`, `tiatoolbox/sub-skills/model-inference/SKILL.md`.

### `timm`

Role: Use PyTorch Image Models (timm) for model discovery, pretrained loading, transforms/data loaders, training APIs, repository CLI workflows, export/checkpoint interoperability, benchmarking/results, and reusable layers/components.
Read when: The request names `timm` or asks for package-specific APIs, CLIs, configs, data/model artifacts, error messages, workflows, or repository maintenance that match this project.
Best for: benchmarking and results, cli workflows, data pipelines, export and interoperability, layers and components, and 2 other focused workflows.
Avoid when: another repo skill in this scenario matches the user's task, package, model family, data format, serving backend, or workflow more directly.
Useful entry points: `timm/SKILL.md`, `timm/sub-skills/benchmarking-and-results/`, `timm/sub-skills/cli-workflows/`, `timm/sub-skills/data-pipelines/`, `timm/sub-skills/export-and-interoperability/`, `timm/sub-skills/layers-and-components/`, `2 more sub-skills`.

### `torchvision`

Role: Use `torchvision` when working with TorchVision models, weights, transforms, TVTensors, datasets, image IO, visualization utilities, vision ops, detection helpers, or official reference training workflows.
Read when: The request names `torchvision` or asks for package-specific APIs, CLIs, configs, data/model artifacts, error messages, workflows, or repository maintenance that match this project.
Best for: datasets io utils, models and weights, ops and detection, training references, and transforms and tv tensors.
Avoid when: another repo skill in this scenario matches the user's task, package, model family, data format, serving backend, or workflow more directly.
Useful entry points: `torchvision/SKILL.md`, `torchvision/sub-skills/datasets-io-utils/`, `torchvision/sub-skills/models-and-weights/`, `torchvision/sub-skills/ops-and-detection/`, `torchvision/sub-skills/training-references/`, `torchvision/sub-skills/transforms-and-tv-tensors/`.

### `ultralytics`

Role: Use `ultralytics` for Ultralytics YOLO package workflows: CLI/Python model usage, data/config setup, train/val, prediction/results, export/deployment, tracking/solutions, model-family selection, and repo development.
Read when: The request names `ultralytics` or asks for package-specific APIs, CLIs, configs, data/model artifacts, error messages, workflows, or repository maintenance that match this project.
Best for: data and configuration, export and deployment, inference and results, model families and tasks, repo development, and 2 other focused workflows.
Avoid when: another repo skill in this scenario matches the user's task, package, model family, data format, serving backend, or workflow more directly.
Useful entry points: `ultralytics/SKILL.md`, `ultralytics/sub-skills/data-and-configuration/`, `ultralytics/sub-skills/export-and-deployment/`, `ultralytics/sub-skills/inference-and-results/`, `ultralytics/sub-skills/model-families-and-tasks/`, `ultralytics/sub-skills/repo-development/`, `2 more sub-skills`.

<!-- DISCO_SCENARIO:computer-vision-modeling-and-augmentation:END -->

## How To Choose

Choose by the named package and task shape: augmentation for Albumentations, image primitives for Pillow/TorchVision/TIMM, detection or segmentation for Detectron2/MMDetection/MMSeg/SAM/GroundingDINO, and export only when tied to a vision model workflow. Choose `albumentations` when the request names `albumentations`, centers on building, debugging, serializing, and integrating Albumentations 2.x augmentation pipelines for images, masks, bboxes, keypoints, volumes, and PyTorch-style datasets, uses its APIs or CLIs, references its configs/artifacts/errors, or asks for repository workflows in computer vision modeling and augmentation. Choose `detectron2` for Detectron2-specific detection/segmentation work. For pure image preprocessing or general PyTorch model code, prefer a generic PyTorch/OpenCV skill unless the request depends on Detectron2 configs, catalogs, model zoo, trainers, structures, evaluators, or export APIs. Choose `detectron2` when training/evaluation depends on Detectron2 config keys, data catalogs, trainers, evaluators, or model zoo checkpoints. Pair the training route with data/config sub-skills when custom datasets or config overrides are involved. Choose `detectron2` for export/deployment tasks involving Detectron2 model inputs, `Instances`, official model families, or Detectron2 export helpers; use a generic deployment skill for unrelated model serving stacks.
