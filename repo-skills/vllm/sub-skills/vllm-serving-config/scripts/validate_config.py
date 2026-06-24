#!/usr/bin/env python3
"""Run the root serve config validator."""

from __future__ import annotations

import runpy
import sys
from pathlib import Path


if __name__ == "__main__":
    root_scripts = Path(__file__).resolve().parents[3] / "scripts"
    sys.path.insert(0, str(root_scripts))
    runpy.run_path(str(root_scripts / "validate_serve_config.py"), run_name="__main__")
