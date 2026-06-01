# Contributing Standards

Use this when modifying TRL source or reviewing a PR.

## Main Code Vs Experimental Code

Main code:

- Stable.
- Consistent.
- Well-tested.
- Avoids large risky changes without strong justification.

Experimental code:

- Lives under `trl.experimental`.
- May change or be removed without deprecation.
- Can be less stable or less thoroughly tested.
- Should still receive small consistency improvements when low risk.
- Should not receive broad refactors unless the task explicitly asks.

## Simplicity

TRL prefers lean, direct code:

- Avoid registries, factories, plugin systems, or new helper layers unless the existing code already uses that pattern.
- Prefer straightforward inline code over a general abstraction.
- Do not add defensive branches or configuration knobs for hypothetical cases.
- Avoid `hasattr` and `getattr` as disguised version checks; use explicit version checks when needed.
- When in doubt, write less code.

## Trainer Duplication Is Intentional

Do not refactor duplicated trainer logic into a base class just because it is duplicated. TRL values trainer readability and isolated evolution. The base trainer should remain minimal.

Consistency is still mandatory. If a duplicated pattern changes in one trainer, apply equivalent changes to all relevant trainers.

## Paper Implementations

If a PR implements a method, algorithm, or training approach from a paper:

- Add a subsection to `docs/source/paper_index.md`.
- Use `https://huggingface.co/papers/<id>` links.
- Include enough config guidance for users to map the paper to TRL.

Reviewers should flag missing paper-index updates.

## Docstring Style

TRL docstrings use Hugging Face style, not Google or NumPy style.

Rules:

- Types appear in backticks inside parentheses: ``(`str`)``.
- Optional parameters are marked with `*optional*`.
- Defaults use `defaults to <value>`.
- If default is `None`, prefer ``(`str`, *optional*)`` rather than verbose `or None` default text.
- Union types use `or`.
- Class references use forms such as [`~transformers.PreTrainedModel`].
- Class docstrings may group parameters with headers like `> Parameters for X:`.

Example:

```python
def method(self, param1: str, param2: int = 1, param3: float | None = None):
    """
    Brief one-line description.

    Args:
        param1 (`str`):
            Description.
        param2 (`int`, *optional*, defaults to `1`):
            Description.
        param3 (`float`, *optional*):
            Description.
    """
```

## Development Setup

```bash
pip install -e ".[dev]"
```

Useful checks:

```bash
pytest tests/test_sft_trainer.py
pytest tests/test_dpo_trainer.py
pytest tests/test_grpo_trainer.py
pytest tests/test_data_utils.py
pytest tests/test_cli.py
make precommit
```

Run focused tests first, then broaden based on touched behavior.

## Bug Reports

For reproducible bug reports, gather:

- OS, Python, PyTorch, TRL, Transformers versions.
- `trl env` output.
- A snippet that reproduces in under 30 seconds when possible.
- Full traceback.
