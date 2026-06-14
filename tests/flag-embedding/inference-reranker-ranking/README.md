# Inference Reranker Ranking

## User Persona
RAG engineer integrating a reranker after first-stage retrieval.

## Scenario Coverage
- Skill area: inference
- Capability: reranker scoring, normalized scores, ranking, memory guidance
- Difficulty: intermediate
- Prompt file: `user_request.txt`
- Expected references/scripts: `sub-skills/inference/SKILL.md`, `sub-skills/inference/references/workflows.md`, `sub-skills/inference/references/api-reference.md`, `sub-skills/inference/references/troubleshooting.md`
- Trigger expectation: The prompt names reranking and a BGE reranker model.

## Expected Successful Behavior
The agent should use `FlagAutoReranker.from_finetuned`, build `[query, passage]` pairs, call `compute_score(..., normalize=True)`, sort descending, and mention reducing `rerank_top_k`, batch size, max length, or model size for memory issues.

## Failure Signals
The agent uses embedder vectors instead of reranker scores, omits normalization, returns unsorted scores, or suggests full benchmark evaluation instead of inference.
