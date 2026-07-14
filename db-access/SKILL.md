---
name: db-access
description: Use for ClickHouse, Greenplum, BI OpenMetadata/catalog, or other database access through already configured MCP database tools/servers. Apply when a task needs database metadata, schema/table/column inspection, DDL reading, read-only query checks, privileged introspection, sandbox writes, catalog search, lineage, or any database access. Use `profi-mcp` for ordinary ClickHouse/Greenplum read-only access and `bi_metadata`/`mcp-bi-metadata` for BI catalog/OpenMetadata read-only access. Use `privileged_access_mcp_*` only after explicit approval for the exact privileged contour/action/target. If the needed configured MCP is unavailable, stop and ask the user what to do next.
---

# DB Access

Use this skill as the single shared database access contract.

## Role

- Purpose: provide the shared database access boundary for already configured MCP database/catalog tools.
- Owns: MCP-first database access, default vs privileged MCP routing, metadata/catalog/query access, privileged-action approvals, and access-related blockers.
- Delegates to: `agent-workflow-core` for task mode/approval workflow and domain skills for interpreting database findings.

## Hard Gates

1. Use `agent-workflow-core` first for task mode and stop-points.
2. Use already configured MCP database tools/servers only; do not use any other database access path.
3. Use `profi-mcp` first for ordinary ClickHouse/Greenplum metadata, DDL reading, `SELECT`, `EXPLAIN`, and smoke checks.
4. Use `bi_metadata`/`mcp-bi-metadata` first for BI catalog/OpenMetadata search, table FQN/columns/owners/tags/domains, database services/schemas, and lineage. Do not use `profi-mcp` or legacy `OpenMetaData__*` tools for OpenMetadata catalog work while the dedicated BI metadata MCP is configured.
5. Use `privileged_access_mcp_*` only after explicit approval for the exact contour, action type, target set, and rollback/cleanup expectation when relevant. Approval must be current to the task step; do not infer it from a general "continue", repo-edit approval, read-only proof request, old sandbox approval, or default MCP outage.
6. If the needed default or privileged MCP is unavailable, stop and ask the user what to do next. Do not install, repair, or change MCP/database configuration from this skill.
7. Never print, copy, or store credentials, passwords, tokens, writable-schema secrets, or admin paths.
8. For potentially long privileged actions, prefer configured async privileged tools when available: start the query, poll status, and keep the returned query/job id for cleanup/cancel evidence. Do not rely on a single long blocking tool call as the control mechanism.
9. Do not assume one MCP user/session can cancel another MCP user/session's query. The configured async flow is expected to control only its own returned query/job ids; cancelling queries started outside that flow needs separate database permission. If a kill/cancel operation fails, report the access blocker instead of retrying through unrelated access paths.
10. Do not call `OpenMetaData__*` tools. Use the dedicated `bi_metadata` MCP for OpenMetadata catalog work, or report a missing configured MCP blocker.
11. Before reporting database-access pass, blocker, escalation need, or privileged-action readiness, run the final checklist.

## Configured MCP Access

Use the host agent's already configured `profi-mcp` tools for ordinary read-only ClickHouse/Greenplum database access. Common tool namespaces are:

- ClickHouse: `Clickhouse__*`
- Greenplum: `GreenPlum__*`

Use the configured `bi_metadata` MCP tools for BI OpenMetadata catalog access:

- `bi_metadata_search`
- `bi_metadata_list_tables`
- `bi_metadata_get_table_by_fqn`
- `bi_metadata_get_table_by_id`
- `bi_metadata_table_lineage_by_fqn`
- `bi_metadata_list_database_services`
- `bi_metadata_list_databases`
- `bi_metadata_list_database_schemas`

Do not use `OpenMetaData__*`; those legacy tools are not the supported catalog path.

If the needed default MCP database access is not available in the current host agent, state that configured MCP access is unavailable and ask the user what to do next. Do not switch to direct access or change tool configuration from this skill.

## Privileged MCP Access

Use `privileged_access_mcp_*` only for approved privileged introspection or state-changing actions.

Required approval shape:

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

## Final Checklist

- Did I use only `profi-mcp`, `bi_metadata`, or approved `privileged_access_mcp_*` tools?
- Did I use `profi-mcp` first for ClickHouse/Greenplum read-only access unless privileged access was explicitly approved?
- Did I use `bi_metadata` first for BI OpenMetadata/catalog access?
- If privileged access was used, did approval name the contour, action, and target set?
- Did I avoid treating a default MCP outage, old approval, repo-edit approval, or abstract sandbox request as privileged-action approval?
- Did I use the matching `privileged_access_mcp_*` tool and stay inside the approved target set?
- For long privileged actions, did I use async start/status/cancel when available instead of a single blocking call?
- Did I avoid claiming I can kill another MCP user's query unless the current contour actually has `KILL QUERY` permission for it?
- Did I avoid every non-MCP database access path?
- Did I avoid `OpenMetaData__*` completely?
- Did I avoid installing, repairing, or changing MCP/database configuration from this skill?
- Did I avoid exposing or storing credentials, tokens, writable schemas, or admin paths?
- Did I report blockers, proof, and cleanup state accurately?
