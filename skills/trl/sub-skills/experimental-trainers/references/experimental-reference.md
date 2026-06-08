# Experimental Reference

Read this before using or modifying TRL experimental trainers.

## What Experimental Means

The `trl.experimental` package warns that APIs are unstable and may change or be removed without notice. This affects imports, constructor signatures, config names, dataset processing, metrics, and CLI compatibility.

Use experimental code when:

- The user names the algorithm and accepts instability.
- The requested method is only available under `trl.experimental`.
- You are working inside the TRL repository and the change is explicitly scoped to experimental code.

Prefer stable trainers when they satisfy the user request.

## Common Experimental Areas

The source tree includes experimental packages for methods such as:

- `a2po`
- `async_grpo`
- `bco`
- `cpo`
- `distillation`
- `dppo`
- `gfpo`
- `gkd`
- `gold`
- `grpo_with_replay_buffer`
- `gspo_token`
- `kto`
- `minillm`
- `nash_md`
- `online_dpo`
- `openenv`
- `openreward`
- `orpo`
- `papo`
- `ppo`
- `prm`
- `sdft`
- `sdpo`
- `ssd`
- `tpo`
- `xpo`

This catalog comes from the repository tree, not from a guarantee that every package is importable in every installed environment.

## Verification Pattern

```python
import importlib
import inspect

module = importlib.import_module("trl.experimental.kto")
print(module)
for name in ["KTOConfig", "KTOTrainer"]:
    obj = getattr(module, name)
    print(name, inspect.signature(obj.__init__))
```

If an import requires optional dependencies, install the documented extra or package and retry. Do not use `hasattr`/`getattr` as a disguised version check in TRL repository code; use explicit version comparisons or direct imports where appropriate.

## Data And CLI Notes

Some experimental methods have CLI commands or docs, but Python imports may still be experimental. For example, `trl kto` exists while docs state `KTOTrainer` and `KTOConfig` moved to `trl.experimental.kto`.

Always check both:

```bash
trl kto --help
```

and:

```python
from trl.experimental.kto import KTOConfig, KTOTrainer
```

## Paper Index Requirement

Inside the TRL repository, if a PR implements a method, algorithm, or training approach from a research paper, it must add a corresponding subsection to `docs/source/paper_index.md`.

When reviewing, treat a missing `paper_index.md` update as a concrete finding for paper-backed implementations.

Paper links should use `https://huggingface.co/papers/<id>` rather than arXiv `abs` URLs.

## Consistency Requirement

TRL intentionally duplicates trainer logic rather than centralizing it. When experimental code copies logic from another trainer:

- Keep variable names aligned.
- Keep comments word-for-word when logic is identical.
- Keep branch order and control flow aligned.
- Diverge only when the trainer's semantics require it.
- Do not silently fix a duplicated bug in only one trainer; report it or fix all aligned copies in a dedicated change.
