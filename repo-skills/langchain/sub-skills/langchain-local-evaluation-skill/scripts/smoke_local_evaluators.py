#!/usr/bin/env python3
"""No-service smoke for LangChain local evaluators."""

from __future__ import annotations

import importlib.util
import json
import re


def main() -> int:
    from langchain_classic.evaluation import (
        ExactMatchStringEvaluator,
        JsonValidityEvaluator,
        RegexMatchStringEvaluator,
    )

    exact = ExactMatchStringEvaluator(ignore_case=True).evaluate_strings(
        prediction="Answer",
        reference="answer",
    )
    regex = RegexMatchStringEvaluator(flags=re.IGNORECASE).evaluate_strings(
        prediction="ticket-123",
        reference=r"ticket-\d+",
    )
    json_valid = JsonValidityEvaluator().evaluate_strings(prediction='{"ok": true}')
    json_invalid = JsonValidityEvaluator().evaluate_strings(prediction="{not json")

    distance = None
    if importlib.util.find_spec("rapidfuzz"):
        from langchain_classic.evaluation import StringDistanceEvalChain

        distance = StringDistanceEvalChain().evaluate_strings(
            prediction="abc",
            reference="abd",
        )

    result = {
        "exact": exact,
        "regex": regex,
        "json_valid": json_valid,
        "json_invalid": json_invalid,
        "distance": distance,
        "rapidfuzz_available": importlib.util.find_spec("rapidfuzz") is not None,
    }
    result["pass"] = (
        exact.get("score") == 1
        and regex.get("score") == 1
        and json_valid.get("score") == 1
        and json_invalid.get("score") == 0
    )
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
