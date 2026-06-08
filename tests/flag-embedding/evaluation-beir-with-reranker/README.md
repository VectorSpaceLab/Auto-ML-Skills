# Evaluation BEIR With Reranker

## User Persona
Benchmark user comparing retrieval and reranking quality.

## Scenario Coverage
- Skill area: evaluation
- Capability: BEIR CLI, embedder plus reranker, metrics, dependencies
- Difficulty: intermediate
- Prompt file: `user_request.txt`
- Expected references/scripts: `sub-skills/evaluation/SKILL.md`, `sub-skills/evaluation/references/cli-reference.md`, `sub-skills/evaluation/references/troubleshooting.md`
- Trigger expectation: The prompt names BEIR, BGE-M3, reranker, and metrics.

## Expected Successful Behavior
The agent should provide a `python -m FlagEmbedding.evaluation.beir` command with dataset names, output paths, metrics, embedder/reranker ids, devices/cache placeholders, and install notes for `beir`, metrics packages, and FAISS.

## Failure Signals
The agent uses the wrong module, omits reranker flags, confuses `--cache_dir` and `--cache_path`, or ignores metric/output requirements.
