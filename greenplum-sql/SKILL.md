---
name: greenplum-sql
description: Use when writing, editing, reviewing, or optimizing Greenplum SQL queries or DDL. MUST be used together with `agent-workflow-core`, `sql-quality-core`, and `sql-style-core` for every Greenplum SQL writing, editing, review, or optimization task. Apply Greenplum-compatible idioms and MPP-aware performance patterns on top of the shared SQL quality/style core. Avoid copying generic PostgreSQL solutions without checking Greenplum-specific execution behavior. Use `db-access` when database access is needed.
---

# Greenplum SQL

Use this skill for Greenplum SQL/DDL work in repositories that follow our database conventions.

## Role

- Purpose: handle Greenplum SQL/DDL writing, review, and optimization.
- Owns: Greenplum compatibility, MPP-aware query shape, distribution, storage, partitioning, metadata/plan interpretation, MPP plan/Motion, stats/`ANALYZE` implications, GP-compatible DDL/DML patterns, Greenplum workload telemetry routing, and engine-local style overlays.
- Delegates to: `agent-workflow-core` for delivery workflow and proof wording, `sql-quality-core` for SQL semantics, `sql-style-core` for shared SQL style, and `db-access` for any database access.

## Hard Gates

1. **Skill-chain gate.** Always use `agent-workflow-core`, `sql-quality-core`, and `sql-style-core` before applying Greenplum-specific rules. Use `db-access` for metadata, DDL, query-log, `EXPLAIN`, smoke, or any live database access.
2. **Reference gate.** Read `references/style.md` for any Greenplum writing, editing, or review. For any non-trivial writing, editing, review, optimization, DDL, or load task, also read `references/sql_readiness.md`. Read the other references only when their trigger applies.
3. **Metadata gate.** Before final SQL against real tables, inspect columns, types, distribution policy, partition rules, storage type, and relevant row-volume/statistics through `db-access` when available, or repo contracts/source definitions when DB access is unavailable.
4. **MPP plan gate.** For non-trivial production `SELECT`s, route lightweight validation through `db-access` when database access is needed and available. Prefer `EXPLAIN`; use constrained `EXPLAIN ANALYZE` only when safe. Interpret optimizer choice, `Motion`, distribution compatibility, row estimates, partition pruning, repeated scans, `Shared Scan`/`Materialize`, and large scans with approximate row-volume signals.
5. **Load-readiness gate.** Before handing a Greenplum DDL/load/rebuild artifact back to the workflow layer, run the load-readiness checks from `references/sql_readiness.md`: syntax, storage/distribution/partition shape, staging compatibility, insert/delete/truncate/swap mechanics, stats/`ANALYZE`, repeated heavy scans, and approved event/window semantics. Report pass/fail/blockers; this skill does not decide final proof status or sandbox need.
6. **Telemetry gate.** For Greenplum workload history in our environment, use only the confirmed telemetry sources in `references/sql_readiness.md`. Fresh Greenplum signals in `profi` are limited to confirmed live views; missing grants/sources are blockers. Use telemetry only as Greenplum workload evidence, not as ClickHouse business data, Greenplum metadata, repo evidence, or a shortcut around missing direct Greenplum logs.
7. **Lineage gate.** Repo-backed cross-engine source flow is not telemetry. If repo evidence proves a Greenplum object is loaded from ClickHouse, analyze that source layer through `clickhouse-sql`; keep Greenplum target metadata, DDL, and plan evidence in this skill.
8. **Evidence-artifact gate.** If the user requested a reasoning/evidence artifact, include exact Greenplum repo-backed paths or a clear `DB-only fallback`, plus concrete plan/validation signals. Do not use another engine's DDL as proof for a live Greenplum object.

## Workflow

1. Establish task mode and delivery rules through `agent-workflow-core`.
2. Run the shared SQL semantic and style passes through `sql-quality-core` and `sql-style-core`.
3. Identify the task type: writing, editing, review, optimization, DDL, load, runtime investigation, or lineage.
4. Load the mandatory references from the hard gates, then any task-specific reference listed below.
5. Inspect metadata/DDL and draft SQL only after grain, business semantics, refresh scope, and MPP shape are clear.
6. Run Greenplum metadata, MPP-plan, load-readiness, validation, and style-overlay self-review before returning SQL or findings.
7. If the task touches Greenplum runtime history, keep the ClickHouse telemetry bridge narrow and call out freshness lag or missing fresh-log blockers.

## Reference Triggers

- Read `references/style.md` for Greenplum-specific/local formatting and layout.
- Read `references/sql_readiness.md` for metadata, MPP shape, load-readiness, telemetry routing, and lightweight validation.
- Read `references/idioms.md` when choosing Greenplum-compatible functions, runtime settings, load patterns, or SQL idioms.
- Read `references/optimization.md` for performance work, `EXPLAIN`/`EXPLAIN ANALYZE`, distribution, skew, statistics, partition refresh, and GPORCA concerns.
- Read `references/anti_patterns.md` when reviewing risky SQL or explaining why a shape is weak.
- Read `references/examples.md` only when a project-shaped example is useful.

## Greenplum Lineage Evidence

- Check repo evidence such as `jobs/*2greenplum/`, `jobs/*clickhouse*/`, `ddl/greenplum/`, `ddl/clickhouse/`, and project load scripts using patterns such as `public.insert_from_clickhouse(...)` before treating a material Greenplum source as terminal.
- If repo evidence crosses engines, use the relevant engine skill for that layer.
- If ClickHouse is a proven upstream source, analyze the source flow with `clickhouse-sql` while keeping Greenplum target metadata, DDL, and plan evidence in Greenplum.

## Final Checklist

- Did I use the required skill chain and `db-access` for all database access?
- Did I read every reference required by the hard gates that matched this task?
- Did I inspect or explicitly fallback for Greenplum metadata: columns, types, distribution, partitioning, storage, and row-volume/statistics?
- Did I interpret the MPP plan with optimizer choice, `Motion`, distribution, partition pruning, materialization/reuse, estimates, and largest scans instead of only saying the query planned?
- For DDL/load/rebuild work, did I prove storage/distribution/partition/refresh mechanics avoid stale or full-target mistakes and include needed stats/`ANALYZE` points?
- Did I keep Greenplum query-history in ClickHouse as narrow telemetry only, without replacing Greenplum metadata/repo evidence or business lineage?
- Did I keep cross-engine lineage separate from telemetry and use the relevant engine skill for upstream source layers?
- Did I return to `sql-style-core` plus the Greenplum style overlay before final SQL?
- If a blocker remains in this skill's `Owns` area, did I stop or downgrade instead of reporting engine-check passed?
