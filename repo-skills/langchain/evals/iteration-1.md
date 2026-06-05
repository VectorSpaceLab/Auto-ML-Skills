# Iteration 1

Date: 2026-06-05

## Scope

Expanded the LangChain repo skill from the initial core workflow set into a broader public-ready tree with 23 sub-skills. The expansion added local Hugging Face model validation, advanced retrievers, cache/rate/usage, stores/docstores, local evaluators, SQL/graph toolkits, OpenAPI/HTTP tools, and security/sandbox coverage, while keeping root `SKILL.md` as a router.

## Coverage Added

- Local HF/Qwen-style model validation: `langchain-local-hf-models-skill`.
- Advanced retrievers: `ParentDocumentRetriever`, `EnsembleRetriever`, `MultiQueryRetriever`, `SelfQueryRetriever`, compression/rerank boundaries.
- Cache/rate/usage: `InMemoryCache`, `InMemoryRateLimiter`, `UsageMetadataCallbackHandler`.
- Stores/docstores: `InMemoryStore`, `InMemoryByteStore`, `create_kv_docstore`.
- Local evaluators: exact match, regex, JSON validity, optional string distance.
- SQL/graph toolkits: `SQLDatabase`, `create_sql_query_chain`, read-only/allowlist safety.
- OpenAPI/HTTP tools and security sandbox: offline spec audit, SSRF policy, dangerous tool scanning.
- Existing later-generated sub-skills were connected into the root router and coverage matrix.

## Script And Structure Validation

- `python langchain/scripts/validate_skill_tree.py --json`: PASS.
- Public local-path leak scan excluding `evals/`: PASS.
- `/tmp/langskill-verify-py311/bin/python langchain/scripts/run_all_smokes.py --json`: PASS, 19/19 no-key smoke scripts.
- Root router and `references/coverage-matrix.md` now enumerate all 23 sub-skills.

## Qwen3-0.6B Validation

Requirement correction from user: use `/share/project/yuyang/model/Qwen3-0.6B` instead of the earlier 0.9B/Falcon fallback. The earlier Falcon/deterministic notes are obsolete.

Runtime used:

- Model: `/share/project/yuyang/model/Qwen3-0.6B`.
- Python: `/opt/conda/bin/python3.11`.
- Runtime packages: `transformers 4.57.3`, `torch 2.5.1+cu124`.
- Method: real Qwen3-0.6B generation with only generated public `SKILL.md` excerpts. No source checkout, no research notes.

Prompts covered:

- Local HF/Qwen model smoke test.
- Advanced parent-document and ensemble retrievers.
- Cache/rate/usage metadata validation.
- SQL query generation safety.

Result: PASS 4/4 after refinement. Initial Qwen outputs routed correctly but omitted some critical exact tokens such as `--model-path`, `EnsembleRetriever`, and `DeterministicFakeEmbedding`. The relevant sub-skill `SKILL.md` files now include concise answer templates so a small model can answer without opening references.

## Publication Note

`SKILL.md`, `sub-skills/`, `references/`, and `scripts/` are public skill content. The `evals/` directory is a development artifact and may mention local validation paths or prompt grades; exclude it from public packaging unless intentionally publishing the eval suite.

## Real Local Qwen Script Smoke

Additional runtime smoke after the Qwen answer eval:

- Built an isolated temporary venv that reused the conda Torch/Transformers installation and installed `langchain-huggingface`.
- Ran `langchain/sub-skills/langchain-local-hf-models-skill/scripts/smoke_local_hf_model.py --model-path ... --max-new-tokens 8`.
- Result: PASS. Raw Transformers generation and `HuggingFacePipeline` generation both returned non-empty text on CUDA.
