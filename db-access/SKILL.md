---
name: db-access
description: Access configured direct database and OpenMetadata MCP for metadata, catalog, bounded queries and approved privileged work. Use with agent-workflow-core; a separately owned typed runtime database read does not activate this skill.
---

# DB Access

Use this skill as the single shared direct database/OpenMetadata MCP access contract.

The public/open-beta baseline requires only configured `profi-mcp` access for ordinary read-only ClickHouse/Greenplum work. Other database or catalog contours are optional and are used only when already configured; their absence does not block that baseline.

## Role

- Purpose: provide the direct database/OpenMetadata access boundary for already configured database/catalog MCP tools.
- Owns: direct MCP database access, configured contour and effective connection identity, default vs privileged MCP routing, metadata/catalog/query access, privileged-action approvals, and direct-access blockers.
- Delegates to: `agent-workflow-core` for task mode/approval workflow and domain skills for interpreting database findings.

## Hard Gates

1. Use `agent-workflow-core` first for task mode and stop-points.
2. Use already configured direct database/catalog MCP tools only. A separately installed access skill may own a typed remote-runtime database-read route; do not add this skill for that route unless the task also needs direct DB/OpenMetadata MCP access.
3. Use `profi-mcp` first for ordinary ClickHouse/Greenplum metadata, DDL reading, `SELECT`, `EXPLAIN`, and smoke checks.
4. Before an environment-scoped pass or readiness claim, identify the configured MCP contour/tool and the available non-secret effective connection identity: service/cluster/environment plus database/schema where exposed. A successful query or matching database/schema name alone is not environment proof. If identity cannot be established, scope the claim to the selected configured contour and report the unknown.
5. Use the configured `bi_metadata`/OpenMetadata MCP first for BI catalog/OpenMetadata search, table FQN/columns/owners/tags/domains, database services/schemas, and lineage. Use read-only tools such as `search_metadata`, `semantic_search`, `get_entity_details`, `get_entity_lineage`, `root_cause_analysis`, and `get_test_definitions`. Do not use `profi-mcp` or legacy `OpenMetaData__*` tools for OpenMetadata catalog work while the dedicated BI metadata MCP is configured.
6. Use `privileged_access_mcp_*` only after a fresh visible user message in the current chat approves the exact contour, action type, target set, and rollback/cleanup expectation when relevant. A short `да` or `continue` counts only as the direct answer to that unchanged checkpoint. Local full-access/client auto-approval, `functions.exec`, an agent-supplied `approved=true` or equivalent tool argument, repo-edit approval, old sandbox approval, another target's session, or default MCP outage is not consent.
7. If the needed default or privileged MCP is unavailable, stop and ask the user what to do next. Do not install, repair, or change MCP/database configuration from this skill.
8. Never print, copy, or store credentials, passwords, tokens, writable-schema secrets, or admin paths.
9. For potentially long privileged actions, prefer configured async privileged tools when available: start the query, poll status, and keep the returned query/job id for cleanup/cancel evidence. Do not rely on a single long blocking tool call as the control mechanism.
10. Do not assume one MCP user/session can cancel another MCP user/session's query. The configured async flow is expected to control only its own returned query/job ids; cancelling queries started outside that flow needs separate database permission. If a kill/cancel operation fails, report the access blocker instead of retrying through unrelated access paths.
11. Do not call `OpenMetaData__*` tools. Use the dedicated `bi_metadata`/OpenMetadata MCP for OpenMetadata catalog work, or report a missing configured MCP blocker.
12. OpenMetadata write/admin tools such as `create_lineage`, `create_test_case`, `create_glossary`, `create_glossary_term`, and `patch_entity` are state-changing. Use them only after the same fresh visible user message in the current chat approves the exact action and target entity; a client/tool approval flag is not proof.
13. Before reporting database-access pass, blocker, escalation need, or privileged-action readiness, run the final checklist.

## Workflow

1. Resolve the configured contour and effective non-secret identity.
2. Use bounded `profi-mcp` Clickhouse__/GreenPlum__ reads for database evidence, or `bi_metadata` for catalog evidence.
3. Read the matching procedure for catalog discovery or privileged work. Reuse sufficient current metadata; page only until the required coverage is complete.
4. Interpret results with domain owners; report access, evidence and cleanup limits after the Final Checklist.

## Reference Triggers

- Read `references/catalog.md` for OpenMetadata source discovery, details, lineage or root cause; do not repeat catalog discovery when current known identities/evidence suffice.
- Read `references/privileged.md` before privileged approval/execution or async cleanup/cancel.

## Final Checklist

- Allowed configured direct MCP used; establish non-secret contour/connection identity before environment claims?
- Catalog uses bi_metadata and unchanged returned FQNs; catalog meaning kept separate from live proof?
- Privileged or catalog-write actions have exact contour/action/target approval; no outage-based escalation?
- Async handles control only their own queries; cleanup and blockers reported?
- No non-MCP fallback, legacy OpenMetaData__*, configuration repair or secret output?
- Separate typed runtime reads remain with their dedicated owner and SQL chain?
