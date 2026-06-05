#!/usr/bin/env python3
"""Create a multimodal OpenAI chat payload for vLLM."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--model", required=True)
    parser.add_argument("--media-url", required=True)
    parser.add_argument("--media-type", choices=["image_url", "audio_url", "video_url"], default="image_url")
    parser.add_argument("--prompt", default="Describe this media briefly.")
    parser.add_argument("--out", required=True)
    args = parser.parse_args()
    content = [{"type": "text", "text": args.prompt}]
    content.append({"type": args.media_type, args.media_type: {"url": args.media_url}})
    payload = {"model": args.model, "messages": [{"role": "user", "content": content}], "max_tokens": 64}
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(str(out))


if __name__ == "__main__":
    main()
