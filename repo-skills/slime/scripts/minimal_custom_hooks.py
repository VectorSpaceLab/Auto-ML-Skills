"""Minimal slime custom hook implementations for copying into a project.

These functions are examples of signatures and return shapes. They are safe to
read and adapt; they are not task-specific reward logic.
"""

from __future__ import annotations

import copy
from typing import Any

from slime.rollout.base_types import RolloutFnEvalOutput, RolloutFnTrainOutput
from slime.rollout.filter_hub.base_types import DynamicFilterOutput
from slime.utils.types import Sample


def generate_rollout(args, rollout_id, data_source, evaluation=False):
    """Full rollout replacement signature used by --rollout-function-path."""
    groups = data_source.get_samples(args.rollout_batch_size)
    if evaluation:
        data = {
            "custom": {
                "rewards": [0.0 for group in groups for _ in group],
                "truncated": [0 for group in groups for _ in group],
                "samples": [sample for group in groups for sample in group],
            }
        }
        return RolloutFnEvalOutput(data=data, metrics={})

    for group in groups:
        for sample in group:
            sample.tokens = sample.tokens or [0, 1]
            sample.response_length = sample.response_length or 1
            sample.reward = 0.0 if sample.reward is None else sample.reward
            sample.status = Sample.Status.COMPLETED
    return RolloutFnTrainOutput(samples=groups, metrics={})


async def custom_generate(args, sample: Sample, sampling_params: dict[str, Any]) -> Sample:
    """Per-sample generation replacement used by --custom-generate-function-path."""
    generated = copy.copy(sample)
    generated.response = generated.response or ""
    generated.tokens = generated.tokens or [0, 1]
    generated.response_length = max(generated.response_length, 1)
    generated.status = Sample.Status.COMPLETED
    return generated


async def custom_rm(args, sample: Sample) -> float:
    """Single-sample reward function used by --custom-rm-path."""
    return 1.0 if sample.status == Sample.Status.COMPLETED else 0.0


async def batched_custom_rm(args, samples: list[Sample]) -> list[float]:
    """Group reward function used by --custom-rm-path with --group-rm."""
    return [1.0 if sample.status == Sample.Status.COMPLETED else 0.0 for sample in samples]


def dynamic_filter(args, samples: list[Sample], **kwargs) -> DynamicFilterOutput:
    """Dynamic sampling filter used by --dynamic-sampling-filter-path."""
    rewards = [float(sample.reward or 0.0) for sample in samples]
    keep = len(set(rewards)) > 1
    return DynamicFilterOutput(keep=keep, reason=None if keep else "constant_reward")


def buffer_filter(args, rollout_id, buffer: list[list[Sample]], num_samples: int) -> list[list[Sample]]:
    """Buffer selection hook used by --buffer-filter-path."""
    return buffer[:num_samples]


def rollout_sample_filter(args, groups: list[list[Sample]]) -> None:
    """In-place sample masking hook used by --rollout-sample-filter-path."""
    for group in groups:
        for sample in group:
            sample.remove_sample = sample.status in {Sample.Status.ABORTED, Sample.Status.FAILED}


def reward_post_process(args, samples):
    """Reward post-process hook used by --custom-reward-post-process-path."""
    flat = [sample for group in samples for sample in group] if samples and isinstance(samples[0], list) else samples
    raw = [float(sample.reward or 0.0) for sample in flat]
    return raw, raw


def convert_samples_to_train_data(args, samples):
    """Minimal train-data conversion shape for --custom-convert-samples-to-train-data-path."""
    flat = [sample for group in samples for sample in group] if samples and isinstance(samples[0], list) else samples
    return {
        "tokens": [sample.tokens for sample in flat],
        "response_lengths": [sample.response_length for sample in flat],
        "rewards": [float(sample.reward or 0.0) for sample in flat],
        "raw_reward": [float(sample.reward or 0.0) for sample in flat],
        "truncated": [int(sample.status == Sample.Status.TRUNCATED) for sample in flat],
        "sample_indices": [sample.index for sample in flat],
        "loss_masks": [sample.loss_mask or [1] * sample.response_length for sample in flat],
    }
