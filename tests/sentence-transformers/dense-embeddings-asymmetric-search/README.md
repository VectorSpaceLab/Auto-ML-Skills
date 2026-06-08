# Dense Asymmetric Search

## User Persona
A developer who knows they need semantic search but does not know the `SentenceTransformer` retrieval-specific APIs.

## Scenario Coverage
- Skill area: dense-embeddings
- Capability: asymmetric semantic search with `encode_query`, `encode_document`, and `semantic_search`
- Difficulty: basic
- Prompt file: `user_request.txt`
- Expected references/scripts: `sub-skills/dense-embeddings/SKILL.md`, `sub-skills/dense-embeddings/references/workflows.md`, `sub-skills/dense-embeddings/scripts/dense_semantic_search.py`
- Trigger expectation: The prompt mentions sentence-transformers, semantic search, short questions, and longer FAQ answers.

## Expected Successful Behavior
The agent should choose `SentenceTransformer`, use `encode_query` for questions and `encode_document` for answers, call `semantic_search`, preserve corpus ids, and provide or adapt the bundled script.

## Failure Signals
The response uses `CrossEncoder` over the full corpus, uses plain `encode` without discussing prompts, omits top-k result mapping, relies on original repo paths, or leaks local environment details.
