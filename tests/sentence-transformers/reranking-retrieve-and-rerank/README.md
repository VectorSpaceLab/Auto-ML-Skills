# Reranking Retrieve And Rerank

## User Persona
A search engineer with an existing lexical first-stage retriever.

## Scenario Coverage
- Skill area: reranking
- Capability: CrossEncoder reranking of candidate lists with original id mapping
- Difficulty: intermediate
- Prompt file: `user_request.txt`
- Expected references/scripts: `sub-skills/reranking/SKILL.md`, `sub-skills/reranking/references/workflows.md`, `sub-skills/reranking/scripts/rerank_candidates.py`
- Trigger expectation: The prompt says BM25, top 100 candidates, rerank, CrossEncoder, and original document IDs.

## Expected Successful Behavior
The agent should use `CrossEncoder.rank` or `predict` on the candidate texts only, explain that `corpus_id` is local to the candidate list, map back to original IDs, and return the top 10.

## Failure Signals
The response attempts dense retrieval instead of using BM25 candidates, loses original document IDs, scores the whole corpus, or mistakes local candidate indices for global IDs.
