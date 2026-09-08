# Privileged Direct MCP Access

Read before privileged approval, query execution or cleanup.

Use `privileged_access_mcp_*` only for approved privileged introspection or state-changing actions.

Required approval shape:

- source: a fresh visible user message in the current chat after this exact checkpoint;
- contour/engine, for example `privileged_access_mcp_clickhouse` or `privileged_access_mcp_greenplum`;
- action type: privileged read, DDL, DML, rebuild, cleanup, or another state-changing action;
- target set: database/schema/table/query scope;
- rollback/cleanup expectation when the action creates, changes, or removes state.

If ordinary `profi-mcp` access fails or is too limited, report the blocker and ask whether to use the privileged contour. The outage itself does not approve privileged access.

After approval:

1. Use only the matching `privileged_access_mcp_*` tool.
2. Keep actions inside the approved target set.
3. If any generated SQL, target, cleanup, or dependency resolves outside approval, stop.
4. Record the approved contour/action/target set in the task note, agent log, or final handoff before or with the first privileged action.
5. Report the proof and cleanup result honestly.

For long-running sandbox writes or expensive proof checks, use async privileged MCP tools when they are configured:

- ClickHouse: `start_async_query`, `get_query_status`, `kill_query`; keep the returned `query_id`.
- Greenplum: `start_async_query`, `get_query_status`, `cancel_query`; keep the returned `job_id`.

The returned id is the cancellable handle for that privileged flow's own query. If async tools are unavailable, keep the query bounded enough for a normal tool call or stop with a blocker.
