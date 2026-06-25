# Materials Science and Crystal Structure Workflows

## When To Read

Computational materials, crystal structures, entries and phase stability, Materials Project data, surfaces/interfaces, diffraction/spectra, VASP-oriented pymatgen CLIs, and materials-analysis Python workflows.

## Repo Skill Options

<!-- SKILLQED_SCENARIO:materials-science-and-crystal-structure-workflows:START -->
### `pymatgen`

Role: Provides self-contained routing and workflow references for using pymatgen APIs and CLIs safely across major computational materials workflows.
Read when: pymatgen, pymatgen-core, Structure, Molecule, Lattice, CrystalNN, ComputedEntry, MPRester, Materials Project, Pourbaix, WulffShape, XRDCalculator, pmg, .pmgrc.yaml, POTCAR.
Best for: Structure/local-environment analysis, compatibility-corrected entries, battery and Borg workflows, external materials data planning, surfaces/interfaces/electrochemistry, spectra/diffraction/visualization, and command-line/configuration safety.
Avoid when: The task is generic molecular drug-discovery chemistry, molecular generative modeling, non-materials simulation trajectories, or package development unrelated to pymatgen APIs/CLIs.
Useful entry points: `pymatgen/SKILL.md`, `pymatgen/sub-skills/structures-local-environments-and-transformations/SKILL.md`, `pymatgen/sub-skills/entries-thermodynamics-and-batteries/SKILL.md`, `pymatgen/sub-skills/external-data-access/SKILL.md`, `pymatgen/sub-skills/surfaces-interfaces-and-electrochemistry/SKILL.md`, `pymatgen/sub-skills/spectra-diffraction-and-visualization/SKILL.md`, `pymatgen/sub-skills/cli-and-configuration/SKILL.md`.

<!-- SKILLQED_SCENARIO:materials-science-and-crystal-structure-workflows:END -->

## How To Choose

Use this scenario when the user names pymatgen or asks for materials-science structure, thermodynamics, external materials data, or crystallographic analysis rather than molecular drug-discovery chemistry or generic array/data workflows. Choose `pymatgen` when the request names pymatgen or materials/crystal/phase/stability terms. Use the external-data sub-skill before live API calls, the CLI/config sub-skill before persistent settings or POTCAR operations, and the domain sub-skill that owns the resulting analysis.
