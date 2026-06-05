#!/usr/bin/env python3
"""Validate basic multimodal chat payload structure."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from urllib.parse import urlparse


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("payload")
    args = parser.parse_args()
    data = json.loads(Path(args.payload).read_text(encoding="utf-8"))
    issues = []
    messages = data.get("messages")
    if not isinstance(messages, list) or not messages:
        issues.append("messages must be a non-empty list")
    else:
        content = messages[0].get("content")
        if not isinstance(content, list):
            issues.append("first message content should be a list for multimodal chat")
        else:
            media_items = [item for item in content if isinstance(item, dict) and item.get("type", "").endswith("_url")]
            if not media_items:
                issues.append("no media URL content item found")
            for item in media_items:
                key = item["type"]
                url = item.get(key, {}).get("url")
                if not url or urlparse(url).scheme not in {"http", "https", "data", "file"}:
                    issues.append(f"invalid media url for {key}: {url}")
    print(json.dumps({"valid": not issues, "issues": issues}, indent=2))
    if issues:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
