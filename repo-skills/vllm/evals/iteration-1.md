# vLLM Skill Iteration 1

## Evaluation Prompts

- `offline-smoke`: Use the vLLM repo skill to prepare and optionally run a small offline generation smoke test with a public 0.6B-0.9B class model, saving prompts and outputs.
- `server-client`: Use the vLLM repo skill to start an OpenAI-compatible localhost server, check health and models, run a chat request, and shut it down.
- `advanced-routing`: Use the vLLM repo skill to decide where to handle a request involving LoRA, guided JSON outputs, embeddings, Ray tensor parallel serving, and benchmark comparison.

## Iteration Notes

- Root `SKILL.md` is a router and links only bundled public-ready references/scripts.
- Sub-skills are normalized lowercase-hyphen directories and frontmatter names match basenames.
- Scripts are deterministic helpers and support `--help` without model loading.
- Public examples prefer `Qwen/Qwen3-0.6B` or caller-provided model IDs; local model paths and inspection environment paths are intentionally excluded from skill docs.
- Known limitation: real model/server smoke requires accelerator/model access and may be skipped by future agents when unavailable.

## Parent Validation Addendum

- A follow-up real-model validation initially attempted to resolve public 0.9B-class models including `refinefuture-ai/Qwen3-Lite-3B-0.9B`; Hugging Face access timed out even after enabling the provided proxy script.
- Direct validation through the inspection environment was discarded because the environment resides on a network filesystem and imports entered kernel RPC wait.
- The real vLLM offline smoke was rerun from an isolated local verification environment with `vllm==0.19.0` and a local Qwen3-0.6B model copy.
- Command shape: `python run_offline_smoke.py --model <LOCAL_MODEL_COPY> --report-model-name Qwen3-0.6B --prompt 'Reply OK.' --max-tokens 4 --temperature 0 --generation-config vllm --max-model-len 512 --gpu-memory-utilization 0.25 --enforce-eager --out <LOCAL_REPORT_JSON>`.
- Result: `PASS`. The script imported vLLM, loaded the model, generated one 4-token response, wrote a JSON report with `ok: true`, and shut the engine down cleanly. GPUs were free afterward.
- The real vLLM OpenAI-compatible server smoke was also rerun with the same local Qwen3-0.6B model copy.
- Command shape: `python start_server.py start --model <LOCAL_MODEL_COPY> --served-model-name Qwen3-0.6B --host 127.0.0.1 --port <LOCAL_PORT> --extra-arg --max-model-len --extra-arg 512 --extra-arg --gpu-memory-utilization --extra-arg 0.25 --extra-arg --enforce-eager`, followed by `python client_smoke.py --base-url http://127.0.0.1:<LOCAL_PORT>/v1 --model Qwen3-0.6B --chat --max-tokens 4`.
- Result: `PASS`. The managed server reached health, `/v1/models` returned the served model, `/v1/chat/completions` returned a short response, and the helper stopped the process group.
- The public skill content still uses public model IDs or caller-provided models; local verification paths are intentionally omitted from publishable files.
