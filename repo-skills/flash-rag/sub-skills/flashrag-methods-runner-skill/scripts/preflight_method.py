#!/usr/bin/env python3
from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "scripts"))
from fr_skill_common import read_simple_yaml


HEAVY_METHODS = {
    "AAR-contriever",
    "AAR-ANCE",
    "llmlingua",
    "recomp",
    "selective-context",
    "ret-robust",
    "selfrag",
    "trace",
    "adaptive",
    "rqrag",
    "r1-searcher",
    "search-r1",
    "autorefine",
    "o2-searcher",
    "rearag",
    "corag",
    "simpledeepsearcher",
}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--split", default="test")
    args = parser.parse_args()
    cfg = read_simple_yaml(args.config)
    method = str(cfg.get("method_name"))
    data_file = Path(str(cfg["data_dir"])) / str(cfg["dataset_name"]) / f"{args.split}.jsonl"
    if not data_file.is_file():
        print(f"warning: dataset split not found for real run: {data_file}")
    if method in HEAVY_METHODS:
        print(f"warning: {method} normally requires external model/checkpoint dependencies; run fake smoke first")
    print(f"method: {method}")
    print(f"dataset_file: {data_file}")
    print("note: real named-method runs are not exposed as a stable package CLI; use run_fake_method.py for smoke tests or vendor an adapted public methods runner into the working project.")
    print("valid: true")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
