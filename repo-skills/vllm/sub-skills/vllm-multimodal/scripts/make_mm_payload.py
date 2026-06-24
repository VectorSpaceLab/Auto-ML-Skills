#!/usr/bin/env python3
"""Create a multimodal OpenAI chat payload for vLLM."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--model", required=True)
    parser.add_argument("--media-url", required=False)
    parser.add_argument("--media-type", choices=["image_url", "audio_url", "video_url"], default="image_url")
    parser.add_argument("--endpoint", choices=["chat", "transcription", "translation", "realtime-note"], default="chat")
    parser.add_argument("--prompt", default="Describe this media briefly.")
    parser.add_argument("--out", required=True)
    args = parser.parse_args()
    if args.endpoint == "chat":
        if not args.media_url:
            parser.error("--media-url is required for chat payloads")
        content = [{"type": "text", "text": args.prompt}]
        content.append({"type": args.media_type, args.media_type: {"url": args.media_url}})
        payload = {"model": args.model, "messages": [{"role": "user", "content": content}], "max_tokens": 64}
    elif args.endpoint in {"transcription", "translation"}:
        payload = {
            "endpoint": f"/v1/audio/{args.endpoint}s",
            "model": args.model,
            "multipart_form": {
                "file": args.media_url or "path/to/audio.wav",
                "model": args.model,
            },
            "note": "Use multipart/form-data with an ASR-capable model and vllm[audio] installed.",
        }
    else:
        payload = {
            "endpoint": "ws://host/v1/realtime",
            "model": args.model,
            "events": [
                {"type": "session.update", "model": args.model},
                {"type": "input_audio_buffer.append", "audio": "<base64-pcm16-16khz-mono>"},
                {"type": "input_audio_buffer.commit", "final": False},
            ],
            "note": "Realtime ASR uses WebSocket events, not an OpenAI chat payload.",
        }
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(str(out))


if __name__ == "__main__":
    main()
