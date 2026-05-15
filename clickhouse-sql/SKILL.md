---
name: clickhouse-sql
description: Use when writing, editing, reviewing, or optimizing ClickHouse SQL queries. MUST be used together with `agent-workflow-core`, `sql-quality-core`, and `sql-style-core` for every ClickHouse SQL writing, editing, review, or optimization task. Apply ClickHouse-native idioms and performance-oriented query patterns on top of the shared SQL quality/style core. Avoid generic SQL when a clearer or faster ClickHouse-specific pattern exists. Use `db-access` when database access is needed.
---

# ClickHouse SQL

Use this skill for ClickHouse SQL work in repositories that follow our database conventions.

## Role

- Purpose: handle ClickHouse SQL writing, review, and optimization.
- Owns: ClickHouse syntax/functions, native query shape, engine correctness, MergeTree/partition/order choices, physical pruning evidence for chosen filters, metadata/plan interpretation, repeated heavy-source reads, `EXPLAIN indexes`, temporary/staging table shape, and engine-local style overlays.
- Delegates to: `agent-workflow-core` for delivery workflow and proof wording, `sql-quality-core` for SQL semantics, `sql-style-core` for shared SQL style, and `db-access` for any database access.

## Hard Gates

1. **Skill-chain gate.** Always use `agent-workflow-core`, `sql-quality-core`, and `sql-style-core` before applying ClickHouse-specific rules. Use `db-access` for metadata, DDL, query-log, `EXPLAIN`, smoke, or any live database access.
2. **Reference gate.** Read `references/style.md` for any ClickHouse writing, editing, or review. For any non-trivial writing, editing, review, or optimization, also read `references/sql_readiness.md` and `references/native_shape.md`. Read the other references only when their trigger applies.
3. **Metadata gate.** Before final SQL against real tables, inspect table columns, types, engine, `ORDER BY`, `PARTITION BY`, and relevant row-volume shape through `db-access` when available, or repo contracts/source definitions when DB access is unavailable.
4. **Source-shape gate.** For ClickHouse mart, DDL/load, or production-like SELECT design, run the physical source-shape check from `references/sql_readiness.md`: compare the chosen filters to each heavy source's `PARTITION BY`, primary/sorting key, and prunable predicate shape. If a proxy timestamp guard is used, report ClickHouse pruning evidence and route business-window coverage to `sql-quality-core`; do not call full coverage proven from pruning alone.
5. **Native-shape gate.** For every non-trivial query, run the ClickHouse-native shape pass from `references/native_shape.md`. Challenge generic joins, subqueries, windows, deduplication, lookup enrichment, `DISTINCT`, `FINAL`, repeated CTE reads, and heavy filters against native alternatives without changing business semantics.
6. **Load-readiness gate.** Before handing a ClickHouse DDL/load/rebuild artifact back to the workflow layer, run the load-readiness checks from `references/sql_readiness.md`: syntax, target engine/partition, staging shape, refresh mechanics, repeated heavy-source reads, lookup scans, approved event/window semantics, and physical source-shape fit. Report pass/fail/blockers; this skill does not decide final proof status or sandbox need.
7. **Validation gate.** For non-trivial production `SELECT`s, route lightweight validation through `db-access` when database access is needed and available. Prefer `EXPLAIN indexes = 1` or `EXPLAIN PLAN`; execute bounded smoke only when safe. Interpret the plan, not only its success.
8. **Telemetry gate.** `system.query_log` is the freshest ClickHouse runtime source in our environment. `monitoring.clickhouse__query_log` is a historical persisted copy and may lag. Treat both as telemetry only, not business data or a replacement for DDL/source/plan evidence.
9. **Lineage gate.** For lineage/business-logic explanations, ClickHouse mirror evidence is only evidence after the `sql-quality-core` lineage pass. If repo evidence reaches another engine, use that engine skill for that layer.

## Workflow

1. Establish task mode and delivery rules through `agent-workflow-core`.
2. Run the shared SQL semantic and style passes through `sql-quality-core` and `sql-style-core`.
3. Identify the task type: writing, editing, review, optimization, DDL, load, or lineage.
4. Load the mandatory references from the hard gates, then any task-specific reference listed below.
5. Inspect metadata/DDL and draft SQL only after grain, business semantics, and refresh scope are clear.
6. Run ClickHouse native-shape, load-readiness, validation, and style-overlay self-review before returning SQL or findings.
7. If the user requested a reasoning/evidence artifact, save the material validation summary there: smoke counts, parts/granules or primary-key conditions, repeated `ReadFromMergeTree`, heavy scan shape, and accept/rewrite decisions.

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

- Did I use the required skill chain and `db-access` for all database access?
- Did I read every reference required by the hard gates that matched this task?
- Did I inspect or explicitly fallback for ClickHouse metadata: columns, types, engine, `ORDER BY`, `PARTITION BY`, and row-volume shape?
- Did I compare chosen filters with source `PARTITION BY`/primary-key pruning shape, and avoid treating pruning evidence as business-window coverage proof?
- Did I complete the native-shape pass and challenge generic SQL where ClickHouse has a safer/faster primitive?
- For DDL/load/rebuild work, did I prove target/staging/partition/refresh mechanics avoid stale or partial-partition results?
- For non-trivial SQL, did I run or explicitly block `EXPLAIN`/bounded validation and interpret repeated reads, primary-key/granule pruning, and heavy scans?
- Did I keep query-log sources as telemetry only and avoid using mirrors as business proof without lineage evidence?
- Did I return to `sql-style-core` plus the ClickHouse style overlay before final SQL?
- If a blocker remains in this skill's `Owns` area, did I stop or downgrade instead of reporting engine-check passed?
