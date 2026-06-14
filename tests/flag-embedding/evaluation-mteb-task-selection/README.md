# Evaluation MTEB Task Selection

## User Persona
Benchmark user running a narrow smoke-sized MTEB subset.

## Scenario Coverage
- Skill area: evaluation
- Capability: MTEB task selection and JSON output
- Difficulty: basic
- Prompt file: `user_request.txt`
- Expected references/scripts: `sub-skills/evaluation/SKILL.md`, `sub-skills/evaluation/references/cli-reference.md`
- Trigger expectation: The prompt names MTEB, BGE-M3, and task selection.

## Expected Successful Behavior
The agent should install `mteb`, run `python -m FlagEmbedding.evaluation.mteb` with `--tasks NFCorpus SciDocsRR`, `--devices cuda:0`, `--embedder_name_or_path BAAI/bge-m3`, and a JSON `--eval_output_path`.

## Failure Signals
The agent defaults to all MTEB tasks, uses markdown output, omits device selection, or adds reranker flags to MTEB without reason.
