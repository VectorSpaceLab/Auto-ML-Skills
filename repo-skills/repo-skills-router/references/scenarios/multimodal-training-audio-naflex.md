# Multimodal Training, Audio, and NaFlex Workflows

## When To Read

OpenCLIP training commands, open_clip_train, CSV/WebDataset data, task-era TrainingTask wrappers, FSDP, torch.compile, CLAP audio, NaFlex, GenLIP, or GenLAP.

## Repo Skill Options

<!-- SKILLQED_SCENARIO:multimodal-training-audio-naflex:START -->
### `open-clip`

Role: Routes complex OpenCLIP training, audio, and variable-resolution/generative workflows to focused sub-skills with safe helper scripts.
Read when: open_clip_train.main, --dataset-type, --use-naflex, NaFlexDataConfig, CLAP-HTSAT, naflexclap, naflexgenlip, naflexgenlap, webdataset-audio, amp_bf16, FSDP, torchcompile-strategy.
Best for: Constructing training commands, validating data layouts, planning CLAP audio zero-shot, debugging NaFlex token-budget batches, and avoiding expensive or download-prone workflows by default.
Avoid when: The user only needs generic distributed training advice with no OpenCLIP-specific APIs, or asks to reproduce a research paper from scratch rather than use this repository package.
Useful entry points: `open-clip/SKILL.md`, `open-clip/sub-skills/training/SKILL.md`, `open-clip/sub-skills/audio-clap/SKILL.md`, `open-clip/sub-skills/naflex-generative/SKILL.md`.

<!-- SKILLQED_SCENARIO:multimodal-training-audio-naflex:END -->

## How To Choose

Use this scenario for OpenCLIP-specific training or multimodal audio/vision-language workflows that are not just model inference. Choose `open-clip` when OpenCLIP-specific parser flags, dict batches, audio transforms, NaFlex patch dictionaries, or GenLIP/GenLAP semantics matter more than generic PyTorch mechanics.
