# Environment Workflows

Read this for the concrete setup and launch sequence before starting a slime job.

## Docker Workflow

Use the public Docker image for production-style work:

```bash
docker pull slimerl/slime:latest
docker run --rm --gpus all --ipc=host --shm-size=16g \
  --ulimit memlock=-1 --ulimit stack=67108864 \
  -it slimerl/slime:latest /bin/bash
```

Then install the desired slime checkout:

```bash
git clone https://github.com/THUDM/slime.git
cd slime
pip install -e . --no-deps
```

The `--no-deps` update matters because Docker already pins CUDA-native dependencies.

## Source Workflow

Use source install when Docker is not available:

```bash
git clone https://github.com/THUDM/slime.git
cd slime
pip install -r requirements.txt
pip install -e . --no-deps
```

This is only the Python package layer. Training also needs a compatible SGLang stack and a full Megatron-LM checkout:

```bash
export PYTHONPATH=/path/to/Megatron-LM:${PYTHONPATH}
python /path/to/skill/slime/scripts/check_env.py --strict-train
```

## Ray Launch Pattern

Start a Ray head:

```bash
ray start --head \
  --node-ip-address 127.0.0.1 \
  --num-gpus 8 \
  --disable-usage-stats \
  --dashboard-host=0.0.0.0 \
  --dashboard-port=8265
```

Submit a job with the full Megatron-LM path in runtime env:

```bash
ray job submit --address="http://127.0.0.1:8265" \
  --runtime-env-json='{"env_vars":{"PYTHONPATH":"/path/to/Megatron-LM","CUDA_DEVICE_MAX_CONNECTIONS":"1"}}' \
  -- python /path/to/skill/slime/scripts/run_slime_train.py ...
```

Use `run_slime_train_async.py` for async paths.

## Clean Rerun Pattern

Only do this when it is safe to terminate local Ray/SGLang jobs:

```bash
ray stop --force || true
pkill -f sglang || true
```

Avoid `pkill -f python` on shared machines unless the user explicitly owns all Python jobs on that node.
