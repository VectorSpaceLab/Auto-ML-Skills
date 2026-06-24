#!/usr/bin/env python3
"""Run the root OpenAI-compatible client smoke helper."""

from __future__ import annotations

import runpy
import sys
from pathlib import Path


if __name__ == "__main__":
    root_scripts = Path(__file__).resolve().parents[3] / "scripts"
    sys.path.insert(0, str(root_scripts))
    runpy.run_path(str(root_scripts / "openai_client_smoke.py"), run_name="__main__")
