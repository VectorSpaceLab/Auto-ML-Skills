# SQL Graph Safety

## Default Safety Rules

- Use read-only database credentials.
- Restrict visible tables with `include_tables` or `ignore_tables`.
- Limit sample rows and avoid exposing sensitive columns in prompts.
- Do not execute generated SQL automatically in a production database.
- Log generated SQL and require human review for high-risk operations.

## Allowlisted Execution

If the user explicitly wants automatic execution:

1. Parse or inspect the generated SQL.
2. Allow only `SELECT` by default.
3. Reject semicolons followed by more statements.
4. Reject DDL/DML keywords such as `DROP`, `DELETE`, `UPDATE`, `INSERT`, `ALTER`, `CREATE`.
5. Run against a read-only user or replica.

## SQLite Smoke

Use a temporary SQLite file, not an in-memory URI, when a workflow may open multiple connections. In-memory SQLite databases are connection-local by default.

## Graph Query Safety

Generated Cypher or graph queries can read or mutate graph state depending on database permissions. Use read-only users and restrict graph/schema exposure.
