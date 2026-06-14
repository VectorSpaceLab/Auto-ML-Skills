# New Method And PR Checklist

Use this reference for PEFT repository changes.

## AI-Assisted Contribution Policy

Breaching PEFT's AI contribution guidelines can result in automatic banning.

Required for AI-assisted patches:

- A human submitter must understand and defend the change end to end.
- The human submitter is responsible for reviewing every changed line and running relevant tests.
- PR descriptions must include a link to issue discussion and maintainer coordination/approval, tests run and pass/fail status, and a clear statement that AI assistance was used.

Before coding a PR:

- Check for overlapping open PRs and issue ownership.
- Ask before working on an existing issue and proceed only after maintainer approval.
- For a new feature, create an issue and get approval first.
- Do not open one-off tiny busywork PRs.
- If preparing a real upstream PR, verify the current upstream contribution guide because repository policy can change.

## Add A New PEFT Method

Core steps:

1. Open or use an approved proposal issue.
2. Link the method paper or stable primary reference.
3. Add a new `PeftType` entry in `src/peft/utils/peft_types.py`.
4. Create `src/peft/tuners/<method>/` with files such as `config.py`, `model.py`, `layer.py`, and `__init__.py`.
5. Register the method in the tuner package with `register_peft_method(...)`.
6. Export config/model classes from `src/peft/tuners/__init__.py` and `src/peft/__init__.py`.
7. If the method needs default target modules for Transformers models, add mappings in `src/peft/utils/constants.py`.
8. Add the method to test matrices, especially `tests/test_custom_models.py`.
9. Add package reference docs under `docs/source/package_reference/` and register them in `docs/source/_toctree.yml`.
10. Add a runnable example when the method is user-facing.
11. Check benchmark settings where relevant.
12. Run focused tests and `make style`.

## Method Registration

`register_peft_method` requires:

- Lowercase unique `name`.
- A matching uppercase `PeftType` enum entry.
- Config class.
- Model class, unless the method is prompt-learning style.
- Unique prefix, defaulting to `<name>_`.
- `is_mixed_compatible=True` only if the method has been tested with `PeftMixedModel`.

Skeleton:

```python
from peft.utils import register_peft_method

register_peft_method(
    name="my_method",
    config_cls=MyMethodConfig,
    model_cls=MyMethodModel,
    prefix="my_method_",
    is_mixed_compatible=False,
)
```

## Tests

For a new method, start with `tests/test_custom_models.py` because it provides broad, fast coverage across custom module types and common adapter operations.

Add or update tests for:

- Config serialization: `to_dict`, `save_pretrained`, `from_pretrained`, `from_json_file`.
- Valid and invalid `TaskType`.
- Forward/backward pass on a small model.
- Save/load adapter.
- Merge/unmerge if supported.
- Disable adapter if supported.
- Multiple adapters and `set_adapter` if supported.
- Quantization if claimed.
- GPU behavior only in GPU test files when GPU is required.

Focused commands:

```bash
pytest tests/test_custom_models.py -k "<method-name>" -v
pytest tests/ -k "<method-name>"
make style
```

Ensure the pytest selector does not deselect all tests.

## Bug Fixes

Implement the regression test first and confirm it fails against the pre-fix code. Then implement the fix and confirm the test passes.

Place tests in the existing file that matches the behavior:

- Config serialization: `tests/test_config.py`.
- Mapping/wrapping behavior: `tests/test_mapping.py`.
- Custom models and adapter operations: `tests/test_custom_models.py`.
- Quantization: `tests/test_quantization.py` or GPU tests when required.
- GPU examples: `tests/test_gpu_examples.py`.

## Style And Compatibility

Run:

```bash
make style
```

Use the ruff version pinned by repository metadata. If the formatter touches unrelated files, the local ruff/config is likely wrong; undo unrelated formatting churn.

Maintain compatibility with supported Python versions and recent PyTorch releases. Avoid code that relies on unsupported Python syntax or new Transformers-only APIs unless guarded.

For Transformers compatibility issues, add version guards rather than assuming the latest Transformers.
