# Iteration 2 Review

## Scope

- Rechecked SGLang public-facing capability coverage against source docs, examples, server routes, and CLI/server arguments.
- Expanded existing router/sub-skills instead of adding detail to the root skill.
- Kept public examples self-contained with public IDs or placeholders.

## Coverage Added

- OpenAI Responses API routing and reference notes, including retrieve/cancel routes and distinction from chat completions.
- Offline Engine/native generation details, including multimodal fields, PD bootstrap/routing fields, and the smoke helper's memory/context guardrails.
- Tool/reasoning reference coverage for Responses-style tools and built-in tool-server safety notes.
- Expert parallel and DeepEP/MoE operational knobs in distributed topology reference.
- Video URL payloads, native `video_data`, language frontend `sgl.video`, audio transcription/realtime transcription, and diffusion environment variable groups.
- Retrieval/ranking notes for multimodal rerank and tokenization utilities.
- Environment variable coverage for readiness, speculative scheduling, and diffusion.

## Validation Notes

- The earlier NFS-based environment import/model-load checks were not counted as passing.
- Per updated instruction, no further NFS environment import or model-load validation was run in this iteration.
- Public structure, link, script help, bytecode compile, and local-path leak checks were rerun using non-SGLang-importing local commands.
- Real SGLang offline generation was rerun from an isolated local verification environment with `sglang==0.5.10.post1` and a local Qwen3-0.6B model copy.
- Offline command shape: `python run_offline_smoke.py --model <LOCAL_MODEL_COPY> --report-model-name Qwen3-0.6B --prompt 'Reply OK.' --max-new-tokens 4 --context-length 512 --mem-fraction-static 0.25 --dtype auto --out <LOCAL_REPORT_JSON>`.
- Offline result: `PASS`. The script imported SGLang, loaded the model through `sgl.Engine`, generated one 4-token response, wrote a JSON report with `ok: true`, and shut down cleanly.
- Real SGLang OpenAI-compatible server smoke was rerun with the same local Qwen3-0.6B model copy.
- Server command shape: `python server_helper.py start --model <LOCAL_MODEL_COPY> --served-model-name Qwen3-0.6B --host 127.0.0.1 --port <LOCAL_PORT> --extra-arg --context-length --extra-arg 512 --extra-arg --mem-fraction-static --extra-arg 0.25 --extra-arg --disable-cuda-graph`, followed by `python openai_client_smoke.py --base-url http://127.0.0.1:<LOCAL_PORT>/v1 --model Qwen3-0.6B --chat --max-tokens 4`.
- Server result: `PASS`. `/v1/models` and `/v1/chat/completions` returned successfully; `/health` returned healthy after warmup; the helper stopped the managed process group.

## Open Items

- Multi-node, PD, EP, HiCache, diffusion, and production observability examples remain structurally validated only; real deployment depends on cluster/hardware setup.
