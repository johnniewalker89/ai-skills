---
name: clickhouse-sql
description: Write, review and optimize ClickHouse SQL and DDL with native shapes, physical pruning and load-readiness proof. Use with agent-workflow-core, sql-quality-core and sql-style-core; access follows its selected owner.
---

# ClickHouse SQL

Use this skill for ClickHouse SQL work in repositories that follow our database conventions.

## Role

- Purpose: handle ClickHouse SQL writing, review, and optimization.
- Owns: ClickHouse syntax/functions, alias/name resolution, native query shape, engine correctness, MergeTree/partition/order choices, physical pruning evidence for chosen filters, metadata/plan interpretation, repeated heavy-source reads, `EXPLAIN indexes`, temporary/staging table shape, and engine-local style overlays.
- Delegates to: `agent-workflow-core` for delivery/proof wording, `sql-quality-core` for SQL semantics, `sql-style-core` for shared style, `db-access` for direct database MCP access, and a separately installed typed runtime-read access owner when selected.

## Hard Gates

1. **Skill-chain gate.** Always use `agent-workflow-core`, `sql-quality-core`, and `sql-style-core` before ClickHouse rules. Use `db-access` for direct MCP metadata, DDL, query-log, `EXPLAIN`, smoke, or live access. If an installed dedicated access skill owns a typed runtime-read route, follow its exact approval/tool contract instead; do not add `db-access` only for that separate route.
2. **Reference gate.** Read `references/style.md` for any ClickHouse writing, editing, or review. For any non-trivial writing, editing, review, or optimization, also read `references/sql_readiness.md` and `references/native_shape.md`. Read the other references only when their trigger applies.
3. **Metadata gate.** Before final SQL against real tables, inspect columns, types, engine, `ORDER BY`, `PARTITION BY`, and relevant volume through the selected access owner when available, or use repo contracts/source definitions when live access is unavailable.
4. **Source-shape gate.** For ClickHouse mart, DDL/load, or production-like SELECT design, run the physical source-shape check from `references/sql_readiness.md`: compare the chosen filters to each heavy source's `PARTITION BY`, primary/sorting key, and prunable predicate shape. If a proxy timestamp guard is used, report ClickHouse pruning evidence and route business-window coverage to `sql-quality-core`; do not call full coverage proven from pruning alone.
5. **Native-shape gate.** For every non-trivial query, run the ClickHouse-native shape pass from `references/native_shape.md`. Challenge generic joins, subqueries, windows, deduplication, lookup enrichment, `DISTINCT`, `FINAL`, repeated CTE reads, and heavy filters against native alternatives without changing business semantics.
6. **Load-readiness gate.** Before handing a ClickHouse DDL/load/rebuild artifact back to the workflow layer, run the load-readiness checks from `references/sql_readiness.md`: syntax, target engine/partition, staging shape, refresh mechanics, repeated heavy-source reads, lookup scans, approved event/window semantics, and physical source-shape fit. Report pass/fail/blockers; this skill does not decide final proof status or sandbox need.
7. **Validation gate.** For non-trivial production `SELECT`s, route lightweight validation through the selected access owner when available. Prefer `EXPLAIN indexes = 1` or `EXPLAIN PLAN`; execute bounded smoke only when safe. Interpret the plan, not only its success.
8. **Telemetry gate.** `system.query_log` is the freshest ClickHouse runtime source in our environment. `monitoring.clickhouse__query_log` is a historical persisted copy and may lag. Treat both as telemetry only, not business data or a replacement for DDL/source/plan evidence.
9. **Lineage gate.** For lineage/business-logic explanations, ClickHouse mirror evidence is only evidence after the `sql-quality-core` lineage pass. If repo evidence reaches another engine, use that engine skill for that layer.
10. **Self-review gate.** Before returning SQL or findings or reporting engine-check passed, run this skill's Final Checklist. If it finds a blocker in this skill's `Owns` area, fix it or stop/downgrade the result.

## Workflow

1. Resolve SQL scope and current metadata/source contracts with the shared SQL owners.
2. Apply native-shape and relevant load-readiness checks, then inspect the bounded plan/output.
3. Reuse unchanged DDL and exact plan evidence across checks; refresh after query/settings/source changes or when freshness requires it.
4. Save requested evidence artifacts with smoke/parts/granules, repeated ReadFromMergeTree, heavy scans and accept/rewrite decisions; run the Final Checklist.

## Reference Triggers

- Read `references/style.md` for ClickHouse-specific/local formatting and layout.
- Read `references/sql_readiness.md` for metadata, engine shape, load-readiness, and lightweight validation.
- Read `references/native_shape.md` for the mandatory native-shape pass.
- Read `references/idioms.md` when choosing ClickHouse functions, joins, settings, or runtime idioms.
- Read `references/optimization.md` for performance work, query-log evidence, explain-based rewrites, projections, indexes, and materialized view choices.
- Read `references/anti_patterns.md` when reviewing risky SQL or explaining why a shape is weak.
- Read `references/examples.md` only when a project-shaped example is useful.

## ClickHouse Lineage Evidence

- Check repo evidence such as `jobs/greenplum2clickhouse/`, `jobs/*2clickhouse/`, `ddl/clickhouse/`, `ddl/greenplum/`, and `marts/greenplum/` before treating a material ClickHouse source as terminal.
- If evidence crosses engines, use the relevant engine skill for that layer.

## Final Checklist

- Mandatory SQL/access chain and references applied; metadata or fallback explicit?
- Filters fit PARTITION BY/primary/sorting keys; pruning not misreported as business-window coverage?
- Native alternatives and repeated heavy reads checked without changing semantics?
- DDL/staging/partition refresh prevents stale or partial results?
- EXPLAIN/bounded proof interpreted; query logs remain telemetry and cross-engine lineage uses its owner?
- Final style and alias binding clear: avoid ambiguous same-name output aliases or qualify intended source references?
- Owner blockers fixed or result downgraded?
