# Store Runtime Workflows

## Cross-Thread Memory

1. Choose a namespace convention such as `(tenant_id, user_id, "memories")`.
2. Store stable memory objects with ids and metadata.
3. Search or retrieve memories in nodes/tools.
4. Keep checkpoint state separate from long-lived memory.

## Tool Injection

When using `ToolNode`, hide internal store/state arguments from model-facing schemas by using the prebuilt injected argument patterns supported by the installed version.

## Runtime Context

Use runtime context for per-run values such as user id, tenant id, locale, policy flags, or request metadata that nodes need but should not be model-generated.
