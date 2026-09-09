---
name: greenplum-sql
description: Write, review and optimize Greenplum SQL/DDL with MPP, distribution, partitioning and load-readiness proof. Use with agent-workflow-core, sql-quality-core and sql-style-core; access follows its selected owner.
---

# Greenplum SQL

Use this skill for Greenplum SQL/DDL work in repositories that follow our database conventions.

## Role

- Purpose: handle Greenplum SQL/DDL writing, review, and optimization.
- Owns: Greenplum compatibility, MPP-aware query shape, distribution, storage, partitioning, metadata/plan interpretation, MPP plan/Motion, stats/`ANALYZE` implications, GP-compatible DDL/DML patterns, Greenplum workload telemetry routing, and engine-local style overlays.
- Delegates to: `agent-workflow-core` for delivery/proof wording, `sql-quality-core` for SQL semantics, `sql-style-core` for shared style, `db-access` for direct database MCP access, and a separately installed typed runtime-read access owner when selected.

## Hard Gates

1. **Skill-chain gate.** Always use `agent-workflow-core`, `sql-quality-core`, and `sql-style-core` before Greenplum rules. Use `db-access` for direct MCP metadata, DDL, query-log, `EXPLAIN`, smoke, or live access. If an installed dedicated access skill owns a typed runtime-read route, follow its exact approval/tool contract instead; do not add `db-access` only for that separate route.
2. **Reference gate.** Read `references/style.md` for any Greenplum writing, editing, or review. For any non-trivial writing, editing, review, optimization, DDL, or load task, also read `references/sql_readiness.md`. Read the other references only when their trigger applies.
3. **Metadata gate.** Before final SQL against real tables, inspect columns, types, distribution, partitions, storage, and relevant volume/statistics through the selected access owner when available, or use repo contracts/source definitions when live access is unavailable.
4. **MPP plan gate.** For non-trivial production `SELECT`s, route lightweight validation through the selected access owner when available. Prefer `EXPLAIN`; use constrained `EXPLAIN ANALYZE` only when safe. Interpret optimizer choice, `Motion`, distribution compatibility, row estimates, partition pruning, repeated scans, `Shared Scan`/`Materialize`, and large scans with approximate row-volume signals.
5. **Load-readiness gate.** Before handing a Greenplum DDL/load/rebuild artifact back to the workflow layer, run the load-readiness checks from `references/load_readiness.md`: syntax, storage/distribution/partition shape, staging compatibility, insert/delete/truncate/swap mechanics, stats/`ANALYZE`, repeated heavy scans, and approved event/window semantics. Report pass/fail/blockers; this skill does not decide final proof status or sandbox need.
6. **Efficiency and telemetry gate.** In every SQL task, apply the relevant diagnostic/plan sections of `references/optimization.md` to support the SQL-quality efficiency gate. For workload/history evidence, read known sources in `references/telemetry.md`; no personal context document is required. Verify grants, coverage and freshness; a mirror does not prove fresh direct Greenplum history or replace metadata/business lineage.
7. **Lineage gate.** Repo-backed cross-engine source flow is not telemetry. If repo evidence proves a Greenplum object is loaded from ClickHouse, analyze that source layer through `clickhouse-sql`; keep Greenplum target metadata, DDL, and plan evidence in this skill.
8. **Evidence-artifact gate.** If the user requested a reasoning/evidence artifact, include exact Greenplum repo-backed paths or a clear `DB-only fallback`, plus concrete plan/validation signals. Do not use another engine's DDL as proof for a live Greenplum object.
9. **Self-review gate.** Before returning SQL or findings or reporting engine-check passed, run this skill's Final Checklist. If it finds a blocker in this skill's `Owns` area, fix it or stop/downgrade the result.

## Workflow

1. Resolve SQL scope and current target metadata with the shared SQL owners.
2. Check MPP plan and relevant DDL/load/refresh mechanics; reuse unchanged metadata/plan evidence for the same scope.
3. Keep the ClickHouse query-history bridge narrow telemetry with freshness limits; cross-engine business lineage uses its engine owner.
4. Run the Final Checklist and report concrete plan evidence, repo paths or DB-only fallback.

## Reference Triggers

- Read `references/telemetry.md` before selecting or interpreting Greenplum workload/query-history sources, including a configured cross-engine mirror.

- Read `references/load_readiness.md` before DDL/load/rebuild/staging or partition-replacement design, review or handoff.

- Read `references/style_examples.md` only when a concrete formatting example is needed; choose the matching example, not the whole collection.

- Read `references/style.md` for Greenplum-specific/local formatting and layout.
- Read `references/sql_readiness.md` for common metadata, MPP/SELECT shape and lightweight validation.
- Read `references/idioms.md` when choosing Greenplum-compatible functions, runtime settings, load patterns, or SQL idioms.
- Read the applicable sections of `references/optimization.md` for every SQL task's efficiency evidence; distribution, skew, partition refresh and planner details follow the actual query/load scope.
- Read `references/anti_patterns.md` when reviewing risky SQL or explaining why a shape is weak.
- Read `references/examples.md` only when a project-shaped example is useful.

## Greenplum Lineage Evidence

- Check repo evidence such as `jobs/*2greenplum/`, `jobs/*clickhouse*/`, `ddl/greenplum/`, `ddl/clickhouse/`, and project load scripts using patterns such as `public.insert_from_clickhouse(...)` before treating a material Greenplum source as terminal.
- If repo evidence crosses engines, use the relevant engine skill for that layer.
- If ClickHouse is a proven upstream source, analyze the source flow with `clickhouse-sql` while keeping Greenplum target metadata, DDL, and plan evidence in Greenplum.

## Final Checklist

- Required SQL/access chain, references, target metadata/statistics or fallback established?
- MPP plan covers optimizer/Motion/distribution, pruning, estimates, reuse and heavy scans?
- Load/staging/storage/partition refresh and ANALYZE implications resolved?
- Telemetry bridge kept separate from target metadata and business lineage?
- Final common/engine style checked; owner blockers prevent pass?
