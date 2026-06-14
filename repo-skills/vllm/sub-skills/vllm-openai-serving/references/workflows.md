# OpenAI-Compatible Serving Workflows

## Minimal Server

```bash
vllm serve Qwen/Qwen3-0.6B \
  --host 127.0.0.1 \
  --port 8000 \
  --generation-config vllm
```

Use `--api-key` or `VLLM_API_KEY` when the server should require authorization. Use `--served-model-name` when clients need a stable model alias.

## Lifecycle

1. Choose an output directory and free localhost port.
2. Start with `scripts/start_server.py` or root `scripts/start_openai_server.sh`.
3. Wait for `GET /health`.
4. Query `GET /v1/models`.
5. Run the requested endpoint smoke.
6. Save server command, PID, logs, request JSON, and response JSON.
7. Shut down unless the user asks to keep serving.

## Common Commands

```bash
curl -fsS http://127.0.0.1:8000/health
curl -fsS http://127.0.0.1:8000/v1/models
python ../../scripts/openai_client_smoke.py --base-url http://127.0.0.1:8000 --list-models
```

Chat:

```bash
python ../../scripts/openai_client_smoke.py \
  --base-url http://127.0.0.1:8000 \
  --model Qwen/Qwen3-0.6B \
  --chat
```

## Logs

Capture stdout/stderr to a file. If startup fails, inspect:

- model download/access
- dtype and quantization compatibility
- GPU memory
- tensor parallel size versus visible GPU count
- chat template and tokenizer errors
- unsupported architecture
