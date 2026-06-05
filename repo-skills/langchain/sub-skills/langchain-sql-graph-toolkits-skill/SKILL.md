---
name: langchain-sql-graph-toolkits-skill
description: "Use when a user wants LangChain SQLDatabase, create_sql_query_chain, SQLDatabaseToolkit, create_sql_agent, graph QA chains, database tool safety, or SQL troubleshooting."
disable-model-invocation: true
---

# LangChain SQL Graph Toolkits

Use `langchain-sql-graph-toolkits-skill` for database and graph-query workflows. Quick answer: start with `SQLDatabase` and `create_sql_query_chain`, use a read-only database user, never execute generated SQL without allowlisting/review, and validate with [scripts/smoke_sql_query_chain.py](scripts/smoke_sql_query_chain.py).

When answering SQL generation/safety, explicitly include this exact checklist: `langchain-sql-graph-toolkits-skill`, `scripts/smoke_sql_query_chain.py`, `SQLDatabase`, `create_sql_query_chain`, `read-only`, generated-SQL review/allowlisting.

## Short Workflow

1. Identify whether the user needs query generation, SQL agent/toolkit, or graph QA.
2. For SQL query generation, use `SQLDatabase` and `create_sql_query_chain`.
3. Use SQLite/file-based smoke tests before connecting to production DBs.
4. Constrain tables with `include_tables` or `ignore_tables` and use read-only credentials.
5. Execute generated SQL only after explicit review, allowlisting, or sandboxing.
6. Run [scripts/smoke_sql_query_chain.py](scripts/smoke_sql_query_chain.py).

## Bundled Scripts

- [scripts/smoke_sql_query_chain.py](scripts/smoke_sql_query_chain.py): creates a temporary SQLite database and verifies SQL query generation with `FakeListLLM`.
- [scripts/inspect_sql_graph_imports.py](scripts/inspect_sql_graph_imports.py): import-checks SQL and graph toolkit shims and reports deprecations/missing packages.

## References

- [references/api-reference.md](references/api-reference.md): verified SQL and graph toolkit imports/signatures.
- [references/sql-graph-safety.md](references/sql-graph-safety.md): read-only credentials, allowlisting, schema exposure, and execution boundaries.
- [references/troubleshooting.md](references/troubleshooting.md): SQLite memory pitfalls, missing community packages, SQLAlchemy errors, and graph QA dependency issues.

## Boundaries

Use agents/tools for generic tool schemas. Use security-sandbox for dangerous tools and untrusted execution. Use this skill when database or graph query tooling is the core task.
