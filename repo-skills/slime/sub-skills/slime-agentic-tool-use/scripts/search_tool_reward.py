"""Minimal reward scaffold for search/tool tasks."""

from __future__ import annotations

from slime.utils.types import Sample


async def reward(args, sample: Sample) -> float:
    label = sample.label
    if label is None:
        return 0.0
    return 1.0 if str(label).strip().lower() in sample.response.strip().lower() else 0.0
