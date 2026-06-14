# Meta Skills

This directory contains two meta skills for building repository-specific Agent
Skills from local machine learning repositories:

- `prepare-env-for-create-skill-for-a-repo`: prepares and verifies a temporary
  conda Python environment with the target repository package installed.
- `create-skill-for-a-repo`: inspects the target repository and the verified
  Python environment, then creates a self-contained repo-specific skill plus
  usability test cases.

Use both skills together when you want an agent such as Claude Code, Codex,
Cursor, or another coding assistant to learn how to work with a specific repo.

## Install

Clone this repository:

```bash
git clone https://github.com/VectorSpaceLab/Auto-ML-Skills.git
cd Auto-ML-Skills
```

Install both meta skills into the user-level skills directory used by your
agent.

For Codex and other agents that follow the [skills.sh](https://www.skills.sh/) convention:

```bash
mkdir -p ~/.agents/skills
cp -R meta-skills/prepare-env-for-create-skill-for-a-repo ~/.agents/skills/
cp -R meta-skills/create-skill-for-a-repo ~/.agents/skills/
```

For Claude Code:

```bash
mkdir -p ~/.claude/skills
cp -R meta-skills/prepare-env-for-create-skill-for-a-repo ~/.claude/skills/
cp -R meta-skills/create-skill-for-a-repo ~/.claude/skills/
```

After installing, restart the agent session so it reloads the available skills.

## Usage

The normal flow is:

1. Clone the repository you want to create a skill for.
2. `cd` into that repository.
3. Start Claude Code, Codex, Cursor, or another coding agent from the repo root.
4. Ask the agent to prepare the Python environment and then create the repo skill.

Example (Codex):

```text
/goal $create-skill-for-a-repo First install the conda python env at: <PATH>, and then use this env to create skill for this repo.
```

Replace `<PATH>` with the conda environment prefix you want the agent to create
or reuse, for example:

```text
/goal $create-skill-for-a-repo First install the conda python env at: /home/me/conda-envs/my-repo-skill-env, and then use this env to create skill for this repo.
```

If your agent does not support `/goal` or `$skill-name` syntax, use the same
request in natural language:

```text
Use the create-skill-for-a-repo meta skill. First install and verify a conda
Python environment at <PATH> for this repository, then use that environment to
create a repo-specific skill for this repo.
```

The agent should first run the environment-preparation workflow, verify that the
target package imports correctly, and then hand the verified environment details
to `create-skill-for-a-repo`. The final output should include the generated
skill directory, usability test cases, and a short creation report.

## What's Next

After the agent finishes, read its final output to confirm where the skill was
created and what repository evidence, environment checks, and generation steps
were completed.

The generated skill should also have a sibling test-case directory containing
several automatically created usability test cases. Use those cases later to
test whether the new skill is understandable and useful for future agents.
