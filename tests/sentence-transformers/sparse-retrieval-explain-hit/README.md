# Sparse Explain Hit

## User Persona
A search developer evaluating sparse retrieval interpretability.

## Scenario Coverage
- Skill area: sparse-retrieval
- Capability: sparse semantic search plus `intersection` and `decode`
- Difficulty: intermediate
- Prompt file: `user_request.txt`
- Expected references/scripts: `sub-skills/sparse-retrieval/SKILL.md`, `sub-skills/sparse-retrieval/references/workflows.md`, `sub-skills/sparse-retrieval/scripts/sparse_semantic_search.py`
- Trigger expectation: The prompt names SparseEncoder/SPLADE and asks for active token explanation.

## Expected Successful Behavior
The agent should encode documents with `encode_document`, queries with `encode_query`, use sparse tensors, search with `score_function=model.similarity`, then call `intersection` and `decode` for influential tokens.

## Failure Signals
The response uses dense embeddings only, omits sparse tensor conversion, cannot explain active tokens, or treats sparse dimensions as plain dense vector positions without decoding.
