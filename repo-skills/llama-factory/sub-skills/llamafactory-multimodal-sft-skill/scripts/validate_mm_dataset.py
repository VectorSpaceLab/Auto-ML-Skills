#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path


MEDIA_KEYS = {"images", "videos", "audios", "image", "video", "audio"}


def load_records(path: Path):
    text = path.read_text(encoding="utf-8").strip()
    if not text:
        return []
    if path.suffix == ".jsonl":
        return [json.loads(line) for line in text.splitlines() if line.strip()]
    data = json.loads(text)
    return data if isinstance(data, list) else [data]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dataset-dir", type=Path, required=True)
    parser.add_argument("--dataset", required=True, help="Dataset name from dataset_info.json or direct JSON/JSONL path")
    parser.add_argument("--max-records", type=int, default=20)
    args = parser.parse_args()
    dataset_info = args.dataset_dir / "dataset_info.json"
    path = Path(args.dataset)
    if not path.exists():
        info = json.loads(dataset_info.read_text(encoding="utf-8"))
        entry = info.get(args.dataset)
        if not entry:
            print("valid: false")
            print(f"- dataset not found in dataset_info.json: {args.dataset}")
            return 1
        path = args.dataset_dir / entry["file_name"]
    records = load_records(path)
    print(f"dataset_path: {path}")
    print(f"records: {len(records)}")
    errors: list[str] = []
    media_refs = 0
    for idx, rec in enumerate(records[: args.max_records]):
        text = json.dumps(rec, ensure_ascii=False)
        if any(k in rec for k in MEDIA_KEYS) or any(token in text for token in ["image_url", "video_url", "audio_url", "<image>", "<video>", "<audio>"]):
            media_refs += 1
    if not records:
        errors.append("dataset is empty")
    if media_refs == 0:
        errors.append("no obvious media fields/tokens found in sampled records")
    print(f"sampled_media_records: {media_refs}")
    print(f"valid: {str(not errors).lower()}")
    for error in errors:
        print(f"- {error}")
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
