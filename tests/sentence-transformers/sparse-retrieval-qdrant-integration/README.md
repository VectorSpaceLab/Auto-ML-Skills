# Sparse Qdrant Integration

## User Persona
A backend engineer integrating learned sparse retrieval with a vector database.

## Scenario Coverage
- Skill area: sparse-retrieval
- Capability: Qdrant sparse search helper, dependencies, reusable corpus index
- Difficulty: advanced
- Prompt file: `user_request.txt`
- Expected references/scripts: `sub-skills/sparse-retrieval/SKILL.md`, `sub-skills/sparse-retrieval/references/workflows.md`
- Trigger expectation: The prompt mentions SparseEncoder outputs, Qdrant, repeated queries, and index reuse.

## Expected Successful Behavior
The agent should mention `qdrant-client`, the need for an accessible Qdrant service, `semantic_search_qdrant`, retaining `corpus_index`, and only passing corpus embeddings when building the index.

## Failure Signals
The response rebuilds the index every query, omits service/client prerequisites, assumes local Qdrant exists, or gives dense vector-only Qdrant code.
