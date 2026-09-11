# Workload And Query-History Sources

Use the selected access owner. The following names are known in the shared
`profi` contour; current availability, grants and freshness must be checked.
They are lookup knowledge, not proof of the state of another installation.
This skill needs no personal context document.

| Source | Use and limit |
| --- | --- |
| ClickHouse `monitoring.greenplum__queries_history` | Historical persisted GP query history; may lag behind fresh runs |
| `pg_catalog.pg_stat_activity` | Current sessions; other users' query text may be hidden as `<insufficient privilege>` |
| `gp_toolkit.gp_workfile_usage_per_query`, `gp_toolkit.gp_workfile_entries`, `gp_toolkit.gp_workfile_usage_per_segment`, `gp_toolkit.gp_workfile_mgr_used_diskspace` | Current spill/workfile evidence, subject to target version and grants |
| `session_state.session_level_memory_consumption` | May require an explicit grant; a past restriction is not a current denial |

Start with these sources when the contour matches, reusing sufficient current
evidence. `public.queries_history`, `queries_tail`, `gpmetrics` and external-table
variants are unconfirmed here; do not cycle through them without new configuration
or user evidence. If a known source is absent, use a confirmed equivalent or
bounded metadata discovery; report the exact source/grant blocker if unresolved.

Current sessions/spills do not prove completed-query history. Fresh direct GP
history requires a confirmed Greenplum source and access. Use a real bounded
history window and actual metrics, not values inferred from old proof notes.

Before constructing a history query, inspect the confirmed source's actual
column names/types and available time/job/query identifiers. Filter by the
narrowest useful interval and known identity before expensive text matching or
aggregation; LIMIT after a broad scan does not bound the work. If the query
fails or the metrics are unavailable, keep that measurement unknown rather
than retrying guessed columns or broadening to all history.

The ClickHouse bridge is narrow Greenplum workload telemetry; it does not replace
GP metadata, repo evidence or business lineage. Non-trivial SQL against the mirror
uses `clickhouse-sql` for its query shape. Repo-proven ClickHouse business/source
flow separately activates that engine owner.
