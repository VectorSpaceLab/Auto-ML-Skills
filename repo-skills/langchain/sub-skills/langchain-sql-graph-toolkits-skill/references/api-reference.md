# SQL Graph API Reference

## SQL Query Chain

```python
from langchain_classic.chains import create_sql_query_chain
from langchain_community.utilities import SQLDatabase
```

Verified signatures:

```text
create_sql_query_chain(llm, db, prompt=None, k=5, *, get_col_comments=None)
SQLDatabase(engine, schema=None, metadata=None, ignore_tables=None, include_tables=None, ...)
```

Example:

```python
db = SQLDatabase.from_uri("sqlite:///app.db", include_tables=["users"])
chain = create_sql_query_chain(llm, db)
sql = chain.invoke({"question": "How many users signed up today?"})
```

The chain generates SQL text. Execution is a separate decision.

## SQL Toolkits

Common classic/community symbols include:

```python
from langchain_community.agent_toolkits.sql.toolkit import SQLDatabaseToolkit
from langchain_community.agent_toolkits.sql.base import create_sql_agent
from langchain_community.tools import InfoSQLDatabaseTool, ListSQLDatabaseTool
```

These are useful for SQL agents but require careful DB permissions and tool allowlisting.

## Graph QA

Graph QA shims such as `GraphCypherQAChain` moved into community integrations. They typically require a graph database driver and credentials. Treat generated Cypher like generated SQL: review and constrain before execution.

## Package Boundary

`langchain-classic` exposes shims for many classic chains. `langchain-community` or standalone integration packages provide database utilities and toolkits.
