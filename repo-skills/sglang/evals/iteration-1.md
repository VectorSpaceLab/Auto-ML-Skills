# Iteration 1 Evals

Development-only artifacts; not linked from SKILL.md.

## Eval Prompts

- `openai-server-smoke`: Use this repo skill to start a local SGLang OpenAI-compatible server with a small public model placeholder, validate health and `/v1/models`, run one chat request if a model is available, then shut it down.
- `structured-json`: Use this repo skill to build a native `/generate` payload that returns a JSON object with city and date fields, validate the constraint, and explain regex/json_schema exclusivity.
- `distributed-router-plan`: Use this repo skill to plan a two-worker SGLang router deployment with cache-aware routing, Prometheus metrics, and health checks.

## Expected Outcomes

- Router selects only the nearest sub-skill and the linked references/scripts.
- YAML frontmatter descriptions are double-quoted and `disable-model-invocation: true` is present.
- Public examples use `<MODEL_ID>` or public IDs; no creator-local paths appear in skill docs or scripts.
- Server workflows include health checks and shutdown.
- Structured output workflow validates local constraints before runtime calls.

## Residual Risk

- Real GPU smoke depends on hardware/model availability.
- Multi-node/router/PD examples require deployment-specific networking and cannot be fully evaluated offline.

## Parent Validation Addendum

- A follow-up real-model validation attempted to resolve public 0.9B-class models including `refinefuture-ai/Qwen3-Lite-3B-0.9B`; Hugging Face access timed out even after enabling the provided proxy script.
- A fallback real offline smoke attempted to load an existing local Qwen3-0.6B checkpoint through the generated `run_offline_smoke.py`.
- A separate `/tmp` import check verified `import sglang` succeeds and exposes `Runtime`.
- The runtime process then entered an uninterruptible I/O state while constructing `sglang.Runtime(...)` for the local Qwen3-0.6B checkpoint, before producing generation output. No managed server or model process was left running after termination.
- That NFS-based result was later discarded because the inspection environment lived on a network filesystem and entered kernel RPC wait.
- The real SGLang offline smoke was rerun from an isolated local verification environment with `sglang==0.5.10.post1` and a local Qwen3-0.6B model copy.
- Command shape: `python run_offline_smoke.py --model <LOCAL_MODEL_COPY> --report-model-name Qwen3-0.6B --prompt 'Reply OK.' --max-new-tokens 4 --context-length 512 --mem-fraction-static 0.25 --dtype auto --out <LOCAL_REPORT_JSON>`.
- Result: `PASS`. The script imported SGLang, loaded the model through `sgl.Engine`, generated one 4-token response, wrote a JSON report with `ok: true`, and shut down cleanly. GPUs were free afterward.
- The public skill content still uses public model IDs or caller-provided models; local verification paths are intentionally omitted from publishable files.
