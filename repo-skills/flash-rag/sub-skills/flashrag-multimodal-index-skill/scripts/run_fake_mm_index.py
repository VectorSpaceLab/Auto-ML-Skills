#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--command", type=Path, required=True)
    parser.add_argument("--summary", type=Path, required=True)
    args = parser.parse_args()
    payload = json.loads(args.command.read_text(encoding="utf-8"))
    corpus = Path(payload["corpus"])
    index_dir = Path(payload["index_dir"])
    index_dir.mkdir(parents=True, exist_ok=True)
    rows = [json.loads(line) for line in corpus.read_text(encoding="utf-8").splitlines() if line.strip()]
    vectors = []
    for row in rows:
        text = str(row.get("contents") or row.get("text") or row.get("caption") or row.get("question") or "")
        digest = hashlib.sha1(text.encode("utf-8")).hexdigest()
        vectors.append({"id": row.get("id", digest[:12]), "hash": digest, "image": row.get("image") or row.get("image_path")})
    (index_dir / "fake_mm_index.json").write_text(json.dumps(vectors, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    result = {"index_dir": str(index_dir), "records": len(rows), "retrieval_method": payload["retrieval_method"], "fake_index": str(index_dir / "fake_mm_index.json")}
    args.summary.parent.mkdir(parents=True, exist_ok=True)
    args.summary.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, indent=2))
    print(f"valid: {str(len(rows) > 0).lower()}")
    return 0 if rows else 1


if __name__ == "__main__":
    raise SystemExit(main())
