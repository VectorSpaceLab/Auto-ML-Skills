# Scientific Python Data Workflows

## When To Read

NumPy-style array analysis combined with molecular simulation trajectories, coordinate transformations, or per-frame scientific computations in Python.

## Repo Skill Options

<!-- DISCO_SCENARIO:scientific-python-data-workflows:START -->
### `mdanalysis`

Role: Explains how MDAnalysis exposes molecular data as arrays and per-frame objects for scientific Python workflows.
Read when: User asks for trajectory loops, per-frame distance calculations, custom AnalysisBase classes, NumPy coordinate arrays, periodic box handling, or writing derived molecular data outputs.
Best for: Building robust scientific Python scripts around molecular trajectory data where MDAnalysis is the data access and analysis layer.
Avoid when: The data is not molecular simulation data, no MDAnalysis APIs are involved, or a generic NumPy/Pandas workflow is sufficient.
Useful entry points: `mdanalysis/SKILL.md`, `mdanalysis/sub-skills/analysis-workflows/SKILL.md`, `mdanalysis/sub-skills/transformations-writing/SKILL.md`.

<!-- DISCO_SCENARIO:scientific-python-data-workflows:END -->

## How To Choose

Use this scenario when the task is scientific data analysis rather than chemistry modeling, drug discovery, or general data pipelines. Use `mdanalysis` when the scientific Python task depends on MDAnalysis trajectory, topology, or AtomGroup semantics; otherwise use a generic scientific Python skill.
