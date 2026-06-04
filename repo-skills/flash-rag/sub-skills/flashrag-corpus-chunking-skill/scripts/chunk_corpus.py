#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "scripts"))
from fr_skill_common import load_jsonl


def simple_chunks(text: str, chunk_by: str, chunk_size: int) -> list[str]:
    if chunk_by == "sentence":
        units = [s.strip() for s in re.split(r"(?<=[.!?。！？])\s+", text) if s.strip()]
        chunks, buf = [], []
        for unit in units:
            buf.append(unit)
            if len(" ".join(buf).split()) >= chunk_size:
                chunks.append(" ".join(buf))
                buf = []
        if buf:
            chunks.append(" ".join(buf))
        return chunks or [text]
    words = text.split()
    return [" ".join(words[i : i + chunk_size]) for i in range(0, len(words), chunk_size)] or [text]


def fallback_chunk(input_path: Path, output_path: Path, chunk_by: str, chunk_size: int) -> None:
    rows = load_jsonl(input_path)
    output = []
    cid = 0
    for row in rows:
        contents = row["contents"]
        title, body = contents.split("\n", 1) if "\n" in contents else (row.get("title", str(row["id"])), contents)
        for chunk in simple_chunks(body, chunk_by, chunk_size):
            output.append({"id": cid, "doc_id": row["id"], "title": title, "contents": title + "\n" + chunk})
            cid += 1
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8") as f:
        for row in output:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")
    print(f"Done! Processed {len(rows)} documents into {len(output)} chunks.")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--chunk-by", choices=["token", "word", "sentence", "recursive"], default="word")
    parser.add_argument("--chunk-size", type=int, default=120)
    parser.add_argument("--tokenizer-name-or-path", default="o200k_base")
    parser.add_argument("--fallback-simple", action="store_true", help="Accepted for compatibility; the bundled script always uses the self-contained fallback.")
    parser.add_argument("--python", default=sys.executable)
    args = parser.parse_args()
    fallback_chunk(args.input, args.output, args.chunk_by, args.chunk_size)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
