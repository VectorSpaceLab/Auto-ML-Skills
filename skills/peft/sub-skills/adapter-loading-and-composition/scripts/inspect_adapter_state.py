#!/usr/bin/env python
"""Print PEFT adapter state for a model object in a user script.

This helper is meant to be copied or imported into a debugging script where a
variable named `model` already exists. It does not load models itself.

Example:
    from inspect_adapter_state import describe_peft_model
    print(describe_peft_model(model))
"""

from __future__ import annotations

from dataclasses import asdict, is_dataclass
import json


def _to_jsonable(value):
    if is_dataclass(value):
        return asdict(value)
    if isinstance(value, (list, tuple)):
        return [_to_jsonable(item) for item in value]
    if isinstance(value, dict):
        return {str(key): _to_jsonable(item) for key, item in value.items()}
    return value


def describe_peft_model(model) -> str:
    """Return a JSON report for PEFT adapter status on `model`."""

    report = {
        "model_class": type(model).__module__ + "." + type(model).__name__,
        "has_get_model_status": hasattr(model, "get_model_status"),
        "has_get_layer_status": hasattr(model, "get_layer_status"),
        "model_status": None,
        "layer_status": None,
        "errors": [],
    }

    if hasattr(model, "get_model_status"):
        try:
            report["model_status"] = _to_jsonable(model.get_model_status())
        except Exception as exc:
            report["errors"].append(f"get_model_status failed: {type(exc).__name__}: {exc}")

    if hasattr(model, "get_layer_status"):
        try:
            report["layer_status"] = _to_jsonable(model.get_layer_status())
        except Exception as exc:
            report["errors"].append(f"get_layer_status failed: {type(exc).__name__}: {exc}")

    return json.dumps(report, indent=2, sort_keys=True)
