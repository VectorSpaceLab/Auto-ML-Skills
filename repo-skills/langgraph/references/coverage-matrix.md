# Coverage Matrix

| Capability | Covered by | Public APIs / commands | Smoke script |
| --- | --- | --- | --- |
| StateGraph build/compile/invoke | `langgraph-graph-state-skill` | `StateGraph`, `START`, `END`, `compile`, `invoke` | `sub-skills/langgraph-graph-state-skill/scripts/smoke_graph_state.py` |
| Message state and reducers | `langgraph-graph-state-skill` | `Annotated`, custom reducer, `add_messages`, `MessagesState`, `MessageGraph` | `sub-skills/langgraph-graph-state-skill/scripts/smoke_graph_state.py` |
| Edges and conditional routing | `langgraph-graph-state-skill` | `add_edge`, `add_conditional_edges`, `path_map` | `sub-skills/langgraph-graph-state-skill/scripts/smoke_graph_state.py` |
| Graph visualization and introspection | `langgraph-graph-visualization-introspection-skill` | `get_graph`, `to_json`, `draw_mermaid`, `xray`, `destinations` | `sub-skills/langgraph-graph-visualization-introspection-skill/scripts/smoke_graph_visualization.py` |
| Dynamic routing and fan-out | `langgraph-graph-state-skill`, `langgraph-subgraphs-multi-agent-skill` | `Command`, `Send` | `sub-skills/langgraph-subgraphs-multi-agent-skill/scripts/smoke_subgraph_multiagent.py` |
| Node retry/cache/timeout/defer policy | `langgraph-node-policy-cache-retry-timeout-skill` | `RetryPolicy`, `CachePolicy`, `InMemoryCache`, `clear_cache` | `sub-skills/langgraph-node-policy-cache-retry-timeout-skill/scripts/smoke_node_policy_cache_retry_timeout.py` |
| Checkpoint memory | `langgraph-checkpoint-interrupt-skill` | `InMemorySaver`, `compile(checkpointer=...)`, `thread_id` | `sub-skills/langgraph-checkpoint-interrupt-skill/scripts/smoke_checkpoint_interrupt.py` |
| Persistence backends | `langgraph-persistence-backends-skill` | `InMemorySaver`, `SqliteSaver`, `PostgresSaver`, async savers | `sub-skills/langgraph-persistence-backends-skill/scripts/check_persistence_backends.py`, `smoke_inmemory_persistence.py` |
| Checkpoint serialization and security | `langgraph-checkpoint-serde-security-skill` | `JsonPlusSerializer`, `EncryptedSerializer`, strict/allowlisted serde | `sub-skills/langgraph-checkpoint-serde-security-skill/scripts/check_checkpoint_serde_security.py` |
| Human-in-the-loop | `langgraph-checkpoint-interrupt-skill` | `interrupt`, `Command(resume=...)`, `get_state` | `sub-skills/langgraph-checkpoint-interrupt-skill/scripts/smoke_checkpoint_interrupt.py` |
| Agent Inbox schema interrupts | `langgraph-human-inbox-interrupt-skill` | `HumanInterrupt`, `HumanResponse`, `interrupt([request])`, list resume | `sub-skills/langgraph-human-inbox-interrupt-skill/scripts/smoke_human_interrupt_schema.py` |
| Prebuilt tools and ReAct agent | `langgraph-prebuilt-tools-agent-skill` | `ToolNode`, `tools_condition`, `create_react_agent` | `sub-skills/langgraph-prebuilt-tools-agent-skill/scripts/smoke_prebuilt_tools.py` |
| Advanced prebuilt agent customization | `langgraph-prebuilt-advanced-agent-skill` | `response_format`, `pre_model_hook`, `post_model_hook`, `wrap_tool_call` | `sub-skills/langgraph-prebuilt-advanced-agent-skill/scripts/smoke_toolnode_wrap_tool_call.py` |
| Streaming and async | `langgraph-streaming-async-skill` | `stream`, `astream`, `stream_events`, `astream_events`, stream modes | `sub-skills/langgraph-streaming-async-skill/scripts/smoke_streaming_async.py` |
| Subgraphs and multi-agent patterns | `langgraph-subgraphs-multi-agent-skill` | compiled subgraph as node, `Command.PARENT`, `Send` | `sub-skills/langgraph-subgraphs-multi-agent-skill/scripts/smoke_subgraph_multiagent.py` |
| Runtime context and store injection | `langgraph-store-runtime-context-skill` | `Runtime`, `InMemoryStore`, injected state/store patterns | `sub-skills/langgraph-store-runtime-context-skill/scripts/smoke_store_runtime.py` |
| Semantic store memory | `langgraph-semantic-store-memory-skill` | `InMemoryStore.put/get/search/list_namespaces`, namespaces, TTL support checks | `sub-skills/langgraph-semantic-store-memory-skill/scripts/smoke_store_search_memory.py` |
| Functional API | `langgraph-functional-api-skill` | `langgraph.func`, `@task`, `@entrypoint` | `sub-skills/langgraph-functional-api-skill/scripts/inspect_functional_api.py` |
| State debug and time travel | `langgraph-state-debug-time-travel-skill` | `get_state`, `get_state_history`, `update_state` | `sub-skills/langgraph-state-debug-time-travel-skill/scripts/smoke_state_debug.py` |
| Local LLM graph-node validation | `langgraph-local-llm-validation-skill` | `StateGraph` node calls raw Transformers generation | `sub-skills/langgraph-local-llm-validation-skill/scripts/check_local_llm_env.py`, `smoke_local_llm_stategraph.py` |
| Platform, Studio, CLI, dev server | `langgraph-platform-cli-skill` | `langgraph dev`, `langgraph build`, `langgraph.json` | `sub-skills/langgraph-platform-cli-skill/scripts/validate_langgraph_json.py` |
| Deployment configuration | `langgraph-deployment-config-skill` | `langgraph.json`, dependencies, env, auth, server config | `sub-skills/langgraph-deployment-config-skill/scripts/audit_deployment_config.py` |
| Remote SDK | `langgraph-remote-sdk-skill` | `langgraph_sdk.get_client`, threads, runs, stream, auth | `sub-skills/langgraph-remote-sdk-skill/scripts/check_remote_sdk.py` |
| Installation and common pitfalls | `langgraph-configuration-troubleshooting-skill` | package imports, deprecated APIs, config rules | `sub-skills/langgraph-configuration-troubleshooting-skill/scripts/check_common_pitfalls.py` |
