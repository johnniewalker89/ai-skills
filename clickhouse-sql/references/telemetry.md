# Query-History Sources

Use the selected access owner and start with these known sources when they match
the configured service contour. This skill needs no personal context document.

| Source | Use and limit |
| --- | --- |
| `system.query_log` | ClickHouse runtime query history; verify availability, host/cluster coverage and actual time range |
| `monitoring.clickhouse__query_log` | Known historical persisted copy in the shared `profi` contour; may lag behind fresh runs |

Use the known source directly when applicable; reuse sufficient current evidence.
Verify effective privileges, coverage and freshness before relying on metrics.
Distinguish event time from collection time. These names do not establish current
availability or grants on another installation. If a source is absent, use the
confirmed configured equivalent or bounded metadata discovery; record a material
source/grant gap instead of probing guessed schemas repeatedly.

Query logs are telemetry, not business data. They do not replace source DDL,
business lineage, plan interpretation or result correctness. Use a bounded
query-history window and actual metrics; no values inferred from old proof notes.
