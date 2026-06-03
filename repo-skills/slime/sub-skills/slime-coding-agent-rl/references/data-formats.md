# Coding-Agent Data Formats

Read this when preparing JSONL for coding-agent RL.

## Required JSONL Shape

Each row should contain:

```json
{
  "prompt": "Issue or task text",
  "label": "instance-or-grader-label",
  "metadata": {
    "image": "sandbox-image-or-routing-key",
    "workdir": "/workspace/repo",
    "problem_statement": "Full issue body",
    "eval_cmd": "pytest -x tests/..."
  }
}
```

Use `--input-key prompt --label-key label --metadata-key metadata`.

## Grader Options

Use exactly one primary grading path when possible:

- `metadata.eval_cmd`: shell command where exit code 0 means solved.
- `metadata.swepro`: structured SWE-bench Pro style harness metadata.
- `metadata.remote_env_info.f2p_script`: can be adapted into an eval command when present.

## Sandbox Metadata

The sandbox metadata must include the key used by the sandbox provider to select an image or environment. Keep secrets and provider-specific credentials outside the JSONL when possible; pass them through environment variables or secret stores.

## Validation

Run:

```bash
python scripts/validate_swe_jsonl.py --input train.jsonl
```

The validator checks row count, required top-level keys, metadata object shape, workdir, problem text, and presence of at least one grader.
