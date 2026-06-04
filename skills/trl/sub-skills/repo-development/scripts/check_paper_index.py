#!/usr/bin/env python
"""Check paper_index.md for paper link style.

Run from a TRL checkout or pass --path. This script checks for arXiv abs links
and reports Hugging Face paper links.

Example:
    python scripts/check_paper_index.py --path docs/source/paper_index.md
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--path", type=Path, default=Path("docs/source/paper_index.md"))
    args = parser.parse_args()

    text = args.path.read_text(encoding="utf-8")
    arxiv = sorted(set(re.findall(r"https://arxiv\.org/abs/[^\s)]+", text)))
    hf = sorted(set(re.findall(r"https://huggingface\.co/papers/[^\s)]+", text)))

    print(f"Hugging Face paper links: {len(hf)}")
    for link in hf[:20]:
        print(f"  {link}")
    if len(hf) > 20:
        print(f"  ... {len(hf) - 20} more")

    if arxiv:
        print("arXiv abs links should be converted:")
        for link in arxiv:
            print(f"  {link}")
        return 1
    print("paper index link style ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
