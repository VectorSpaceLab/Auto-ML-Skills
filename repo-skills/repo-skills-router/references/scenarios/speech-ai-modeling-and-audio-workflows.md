# Speech AI Modeling and Audio Workflows

## When To Read

Speech AI tasks involving ASR, transcription, TTS, vocoders, G2P, speaker diarization, VAD, forced alignment, audio enhancement/restoration, speech language models, voice agents, speech manifests, or speech-model repository maintenance.

## Repo Skill Options

<!-- DISCO_SCENARIO:speech-ai-modeling-and-audio-workflows:START -->
### `nemo`

Role: Guides NVIDIA NeMo Speech usage and maintenance across ASR, TTS, audio processing, SpeechLM2, speaker diarization, shared data tools, and repo-development workflows.
Read when: The request names NeMo, nemo-toolkit, NVIDIA NeMo Speech, Parakeet, Canary, FastPitch, HiFi-GAN, MagpieTTS, SALM, SpeechLM2, Nemotron VoiceChat, Sortformer, NeMo Forced Aligner, NeMo JSON manifests, Lhotse dynamic batching, tarred audio datasets, Hydra NeMo configs, .nemo checkpoints, speech transcription, text-to-speech synthesis, speaker diarization, VAD, forced alignment, audio enhancement/restoration, ASR evaluation, speech tokenizer creation, or NeMo repository tests/docs/style.
Best for: NeMo-specific ASR inference/fine-tuning/streaming, TTS synthesis and finetuning, audio-to-audio workflows, SpeechLM2 and voice-agent configs, speaker/diarization/forced-alignment tasks, NeMo data tooling, and safe repository development guidance.
Avoid when: Use a generic PyTorch, Lightning, Transformers, vLLM, dataset-processing, or audio library skill when the task does not involve NeMo APIs, NeMo configs, NeMo model families, NeMo data formats, or this repository's maintenance workflow.
Useful entry points: `nemo/SKILL.md`, `nemo/sub-skills/asr/SKILL.md`, `nemo/sub-skills/tts/SKILL.md`, `nemo/sub-skills/audio/SKILL.md`, `nemo/sub-skills/speechlm2/SKILL.md`, `nemo/sub-skills/speaker-diarization/SKILL.md`, `nemo/sub-skills/data-tools/SKILL.md`, `nemo/sub-skills/repo-development/SKILL.md`.

### `unilm`

Role: Use unilm to plan and troubleshoot UniLM speech/audio model workflows while keeping heavyweight fairseq/checkpoint runs gated.
Read when: Requests mention WavLM, BEATs, SpeechT5, SpeechLM, VALL-E, 16 kHz audio, speech manifests, fairseq speech tasks, ASR, speech translation, TTS, voice conversion, speaker representation, audio checkpoints, or sample-rate mismatch.
Best for: Input validation, checkpoint/data planning, and safe command shaping for UniLM speech/audio projects.
Avoid when: Use a dedicated speech framework skill when the request targets another package such as NeMo, Whisper, ESPnet, or pyannote rather than UniLM speech projects.
Useful entry points: `unilm/SKILL.md`, `unilm/sub-skills/multimodal-generation/SKILL.md`.

<!-- DISCO_SCENARIO:speech-ai-modeling-and-audio-workflows:END -->

## How To Choose

Choose the repo skill whose speech/audio framework, model family, data format, runtime, or repository workflow most directly matches the request; use package names, checkpoint formats, manifest fields, and task terms such as ASR, TTS, diarization, VAD, forced alignment, SpeechLM, voice-agent, or audio enhancement as strong signals. Choose `nemo` when the user needs NVIDIA NeMo Speech APIs, Hydra configs, .nemo checkpoints, speech/audio manifests, model examples, troubleshooting, or repository maintenance. Within `nemo`, route ASR to `asr`, TTS to `tts`, audio enhancement/restoration to `audio`, SALM/SpeechLM2/Nemotron VoiceChat to `speechlm2`, diarization/VAD/forced alignment to `speaker-diarization`, shared manifests/Lhotse/tarred-data/tokenizer/evaluator tools to `data-tools`, and source edits/tests/docs/build guidance to `repo-development`. Choose unilm when speech/audio workflow terms are tied to WavLM, BEATs, SpeechT5, SpeechLM, or VALL-E.
