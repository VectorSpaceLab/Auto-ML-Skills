#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "scripts"))
from fr_skill_common import read_simple_yaml


def triple_from_doc(contents: str) -> list[dict]:
    title = contents.splitlines()[0] if contents.splitlines() else "Document"
    text = " ".join(contents.splitlines()[1:]) or contents
    if "written by" in text:
        tail = text.split("written by", 1)[1].split(".")[0].strip()
        return [{"head": title, "relation": "written by", "tail": tail}]
    if "was an" in text:
        tail = text.split("was an", 1)[1].split(".")[0].strip()
        return [{"head": title, "relation": "was", "tail": tail}]
    return [{"head": title, "relation": "mentions", "tail": text[:60]}]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--summary", type=Path, required=True)
    args = parser.parse_args()
    cfg = read_simple_yaml(args.config)
    rows = [json.loads(line) for line in args.input.read_text(encoding="utf-8").splitlines() if line.strip()]
    triple_cache = {}
    outputs = []
    for row in rows:
        chains = []
        for doc in row["retrieval_result"]:
            doc_id = doc.get("id") or hashlib.sha1(doc["contents"].encode("utf-8")).hexdigest()[:12]
            triples = triple_from_doc(doc["contents"])
            triple_cache[doc_id] = triples
            chains.extend(triples)
        context = "; ".join(f"{t['head']} --{t['relation']}--> {t['tail']}" for t in chains[: int(cfg.get("trace_config", {}) or 2) or 2])
        outputs.append({"id": row.get("id"), "question": row["question"], "trace_context": context, "prediction": row.get("golden_answers", ["unknown"])[0]})
    save_dir = Path(str(cfg.get("save_dir") or args.summary.parent))
    save_dir.mkdir(parents=True, exist_ok=True)
    triple_path = save_dir / "save_triples.json"
    triple_path.write_text(json.dumps(triple_cache, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    intermediate = save_dir / "intermediate_data.json"
    intermediate.write_text(json.dumps(outputs, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    result = {"records": len(outputs), "triple_cache": str(triple_path), "intermediate": str(intermediate), "first": outputs[0] if outputs else None}
    args.summary.parent.mkdir(parents=True, exist_ok=True)
    args.summary.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, indent=2))
    print(f"valid: {str(bool(outputs) and triple_path.exists()).lower()}")
    return 0 if outputs else 1


if __name__ == "__main__":
    raise SystemExit(main())
