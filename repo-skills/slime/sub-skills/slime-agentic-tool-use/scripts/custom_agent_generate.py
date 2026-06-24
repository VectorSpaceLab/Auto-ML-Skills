"""Minimal custom-generate skeleton for agentic slime rollouts."""

from __future__ import annotations

from slime.utils.types import Sample


async def generate(args, sample: Sample, sampling_params: dict) -> Sample:
    """Replace this body with a tool/RAG/environment loop.

    Keep tokens from the rollout model. Do not rebuild the final training sample
    by retokenizing a rendered conversation string unless you intentionally mask
    the retokenized parts.
    """
    # Example placeholder: mark the sample failed until real generation is added.
    sample.response = ""
    sample.tokens = sample.tokens or []
    sample.response_length = 0
    sample.reward = 0.0
    sample.status = Sample.Status.FAILED
    return sample
