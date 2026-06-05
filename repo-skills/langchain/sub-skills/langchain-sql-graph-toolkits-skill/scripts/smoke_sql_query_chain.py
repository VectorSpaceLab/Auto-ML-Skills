#!/usr/bin/env python3
"""No-key smoke for SQLDatabase and create_sql_query_chain."""

from __future__ import annotations

import json
import re
import tempfile
from pathlib import Path

from sqlalchemy import create_engine, text


UNSAFE = re.compile(r"\b(drop|delete|update|insert|alter|create|truncate)\b", re.IGNORECASE)


def main() -> int:
    from langchain_classic.chains import create_sql_query_chain
    from langchain_core.language_models.fake import FakeListLLM
    from langchain_community.utilities import SQLDatabase

    with tempfile.TemporaryDirectory() as tmpdir:
        db_path = Path(tmpdir) / "demo.db"
        engine = create_engine(f"sqlite:///{db_path}")
        with engine.begin() as conn:
            conn.execute(text("CREATE TABLE users (id INTEGER, name TEXT);"))
            conn.execute(text("INSERT INTO users VALUES (1, 'Ada');"))

        db = SQLDatabase.from_uri(f"sqlite:///{db_path}", include_tables=["users"])
        llm = FakeListLLM(responses=["SELECT name FROM users WHERE id = 1;"])
        chain = create_sql_query_chain(llm, db)
        sql = chain.invoke({"question": "What is the name for user id 1?"})

    select_only = sql.strip().lower().startswith("select") and not UNSAFE.search(sql)
    result = {
        "sql": sql,
        "select_only": select_only,
        "mentions_users": "users" in sql.lower(),
    }
    result["pass"] = bool(select_only and result["mentions_users"])
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
