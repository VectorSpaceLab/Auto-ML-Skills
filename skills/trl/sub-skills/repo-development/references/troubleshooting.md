# Repo Development Troubleshooting

## Tests Fail Because Import Uses Installed TRL

For source development, install editable:

```bash
pip install -e ".[dev]"
python -c "import trl; print(trl.__file__)"
```

Confirm `trl.__file__` points at the checkout.

## One Trainer Test Fails After Changing Another

Search duplicated logic. A change in GRPO often implies equivalent changes in RLOO or experimental online trainers. A change in DPO preprocessing may affect RewardTrainer and experimental preference trainers.

## Reviewer Flags Missing `paper_index.md`

If the PR implements a paper-backed method, add a subsection to `docs/source/paper_index.md`. Use Hugging Face paper links, not arXiv links.

## Doc Build Or Style Fails

Check docstring style:

- Backtick types inside parentheses.
- `*optional*` marker.
- `defaults to`.
- `or` for unions.
- Hugging Face class references.

Do not convert nearby docstrings to Google or NumPy style.

## Ruff Or Precommit Fails

Run:

```bash
make precommit
```

or inspect `pyproject.toml` for Ruff configuration. Examples and scripts may allow `print`, but source modules generally should not.

## Experimental API Warning In Tests

If tests intentionally import experimental APIs, set the expected warning behavior in the test. Do not globally silence warnings without checking local conventions.

## Avoiding Over-Abstraction

If a change starts creating registries, factories, or shared trainer base methods, stop and re-check the local design. TRL intentionally keeps trainers self-contained.
