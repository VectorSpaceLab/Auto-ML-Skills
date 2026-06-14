# SQL Graph Troubleshooting

## `no such table` With SQLite Memory Database

`sqlite:///:memory:` is per connection. `SQLDatabase` may open a separate connection for schema/sample rows. Use a temporary file path such as `sqlite:///path/to/demo.db` for smoke tests.

## `langchain_community` Import Warning

Some community package APIs are being sunset or moved to standalone integrations. Follow the current package warning and prefer standalone integration packages when available.

## Generated SQL Is Unsafe

Do not execute it. Add table restrictions, prompt constraints, parsing/allowlisting, and read-only credentials.

## Graph QA Import Fails

Install the community or graph database integration package and the database driver. Validate imports before connecting to a live graph database.

## Chain Output Includes Markdown

Prompt the model to output SQL only, then strip code fences cautiously. Never rely on stripping as a safety mechanism.
