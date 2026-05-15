# Greenplum SQL Metadata And Shape

Use this file before returning non-trivial Greenplum SQL code.

`sql-quality-core` owns engine-agnostic SQL quality checks: source choice, repo-backed proof, driving grain, central join sanity, multi-row fact semantics, category-safe metrics, date-window semantics, smoke scale, and general validation mindset.

This file owns Greenplum-specific SQL metadata and shape checks: MPP metadata shape, distribution, partition pruning, CTE/materialization behavior, and Greenplum plan interpretation. Final task status, artifact readiness, approval gates, and proof-level wording belong to `agent-workflow-core`.

## Responsibility split

- `sql-quality-core` owns business SQL quality.
- `greenplum-sql` owns Greenplum syntax, MPP query shape, DDL choices, and Greenplum-specific plan interpretation.
- Use `db-access` for database access.

Use all applicable skills together for real Greenplum work.

## Metadata pass

Before drafting or finalizing non-trivial SQL against real Greenplum objects:

1. Identify every real source table, target table, external table, temp table, and important intermediate involved.
2. Inspect metadata through `db-access` when database access is needed:
   - columns and types;
   - distribution policy and distribution keys;
   - partition rules;
   - storage type (`heap`, `ao_row`, `ao_column`);
   - row volume, skew, and statistics freshness when available.
3. Use repo contracts, DDL, dbt YAML, migration files, or source definitions only when DB metadata is unavailable or the task is explicitly text-only.
4. If metadata is unavailable and the query depends on uncertain columns, distribution, or partitioning, state the limitation instead of guessing.

Metadata inspection is required because Greenplum SQL choices depend on MPP shape, not only on column names.

When the task requests a reasoning/eval artifact, record repo-backed evidence next to the selected sources:

- use exact local Greenplum DDL/model/contract paths for the selected live objects;
- do not use ClickHouse DDL mirrors or lower-layer lineage as proof for the selected Greenplum object;
- if an object is live but has no exact local path or explicit deployment mapping, label it `DB-only fallback` and explain why it is still used.

## What metadata should change

Use Greenplum metadata to choose:

- date filters that match partition rules;
- joins that align with distribution keys when large tables are involved;
- whether a lookup/enrichment side should be pre-aggregated or reduced to one row per key before joining;
- whether a heavy right-side history/enrichment table can be restricted to relevant left-side business keys before expensive aggregation or lookup work;
- whether a one-row `params` CTE should be cross-joined or pushed only into the CTEs that need it;
- whether casts are avoidable because real column types already match;
- whether `DISTRIBUTED BY`, `DISTRIBUTED RANDOMLY`, or `DISTRIBUTED REPLICATED` is appropriate for new DDL;
- whether `ANALYZE` / `VACUUM` should be part of a load or structural-change workflow.

For standalone smoke/ad-hoc SQL with a fixed chosen period, verify static partition pruning. If a params CTE prevents pruning, use explicit literals or another shape that preserves pruning.

## DDL/load syntax self-review

Before returning Greenplum DDL or load files:

- verify syntax against the expected Greenplum/PostgreSQL compatibility level, not generic modern PostgreSQL;
- verify staging tables have a deliberate storage, distribution, and partition shape for the intended swap/delete/insert mechanics;
- check that delete/truncate/exchange/swap keys match the declared rebuild grain and cannot leave stale rows;
- mark post-load target checks separately from read-only source checks;
- if self-review finds invalid syntax or incompatible staging shape, fix the artifact before reporting engine-check passed. Sandbox validation should prove runtime/result behavior, not catch issues visible in the final SQL text.

## Lightweight validation

Before returning a non-trivial production `SELECT`:

- Prefer `EXPLAIN` through `db-access` for the drafted query when database access is needed and available.
- Use `EXPLAIN ANALYZE` only through `db-access` and only on constrained inputs or when execution is safe; do not run a heavy full query just to prove syntax or confidence.
- Interpret the plan. A successful `EXPLAIN` only proves the query can be planned; it does not prove the shape is acceptable or make the task ready.
- Check the optimizer line. `Optimizer: Pivotal Optimizer (GPORCA)` is expected for most analytic work. If the plan uses `Optimizer: Postgres query optimizer`, name the fallback and inspect whether a GPORCA-friendly rewrite is available.
- Check `Motion` nodes explicitly: `Redistribute Motion`, `Broadcast Motion`, and `Gather Motion`.
- Check whether large joins are distribution-compatible or force unnecessary data movement.
- Check row estimates and where the largest row-volume nodes are.
- Check whether partition pruning is present when the query should restrict partitions.
- Treat large `Seq Scan` nodes as a signal to verify filters, partitioning, and statistics.
- For partitioned history tables, treat "all partitions" as a specific signal: compare it with the narrowest semantically valid window and the number of additional business keys gained.
- Check `Shared Scan`, `Materialize`, and CTE boundaries explicitly; they can be acceptable, but they are plan features to interpret, not background noise.
- Compare row estimates with cheap actual counts for the driving window when possible. A large mismatch is a signal to question statistics, plan shape, and whether a smoke query is still lightweight.
- Name the largest scans or joins when they are material to the query shape, and decide whether they are accepted, reduced, or rewritten.
- For history/event tables with their own timestamp, do not treat a key-filtered all-history scan as the normal smoke coverage/category branch. Use a bounded timestamp-window branch for smoke coverage/categories, and a separate explicitly named all-history branch only for pointer/reference semantics when ids can point outside the smoke window.
- A plan interpretation is incomplete if it only mentions partition pruning or generic "expected Motion". At minimum, include approximate numbers for the top material full scans by table, the largest intermediate row estimates, repeated/reused source estimates, major `Motion`, `Shared Scan` / `Materialize` points, and whether each surprising item is accepted or rewritten.
- Do not round the EXPLAIN summary down to qualitative language. Write row-volume signals as concrete approximations, for example `order_service Seq Scan ~23M rows`, `client Seq Scan ~5M rows`, `Gather Motion ~190k rows`, or `orders_base estimate ~1.6M vs actual ~29k`.
- If a full scan exceeds the constrained driving set by orders of magnitude, first try key-filtering, partition pruning, distribution-compatible joins, or pre-aggregation before accepting it as a smoke tradeoff.
- Do not treat `EXPLAIN` as passed until surprising scans, repeated source reads, materialization points, bad estimates, and major Motion nodes are interpreted as acceptable for the constrained task or fixed.
- If a result check is useful, run a constrained check through `db-access`, such as a narrow date window, `LIMIT`, aggregate row counts, or metadata-only checks.
- For heavy enrichment tables, compare unfiltered date-window row counts with row counts after applying relevant business keys when a cheap count is possible through `db-access`.
- If a reusable heavy fact/history CTE is later joined to a constrained driving set, push the driving-key filter into that CTE when semantics allow it. Do not materialize a broad date-window CTE first and reduce it only in downstream CTEs unless the wider scan is measured and accepted.
- If validation cannot be run because `db-access` is unavailable, the query is text-only, or execution would be too risky, say so briefly.

For optimization tasks, also inspect skew/statistics via system views or `gp_toolkit` through `db-access` when available; see `optimization.md`.

## Workload and query-log evidence

For Greenplum runtime/workload investigations in our environment, use confirmed telemetry sources only.

This is narrow telemetry only. It may be used only to inspect Greenplum query-history/workload evidence. It must not be used to pull ClickHouse business sources, infer Greenplum business logic, or replace Greenplum metadata/repo evidence.

This restriction does not block normal repo-backed cross-engine lineage/source-flow analysis. If repo evidence proves that a Greenplum object is loaded from ClickHouse, analyze that source flow with `clickhouse-sql` and keep it separate from telemetry evidence.

Known historical source:

- `monitoring.greenplum__queries_history` is a historical persisted copy in ClickHouse and may lag behind fresh runs.

Confirmed fresh/live Greenplum signals in `profi`:

- `pg_catalog.pg_stat_activity` for current sessions; other users' query text may be hidden as `<insufficient privilege>`.
- `gp_toolkit.gp_workfile_usage_per_query`, `gp_toolkit.gp_workfile_entries`, `gp_toolkit.gp_workfile_usage_per_segment`, and `gp_toolkit.gp_workfile_mgr_used_diskspace` for current spill/workfile evidence.

Known blockers in `profi` until grants/sources change:

- `session_state.session_level_memory_consumption` may require an explicit grant.
- Do not hunt through ad hoc `public.queries_history`, `queries_tail`, `gpmetrics`, or external-table variants unless the user or environment documentation confirms them for this contour.

Fresh direct Greenplum query history requires a confirmed Greenplum source and grants. If it is required and unavailable, record the blocker instead of cycling through unconfirmed schemas or using ClickHouse external tables as a shortcut.

Rules:

- Use `db-access` for live query-log checks.
- If querying the ClickHouse mirror requires non-trivial SQL, use `clickhouse-sql` for that query shape and interpretation.
- Verify current privileges before relying on the source.
- If SELECT is blocked, record the exact table/grant blocker.
- Never invent workload metrics from old proof notes, registry entries, or intuition; use a real bounded query-history window from the task request or the owning workflow/evaluation layer.

## CTE and materialization awareness

Greenplum 6 inherits PostgreSQL 9.4-era CTE behavior: CTEs can act as optimization fences and may force materialization instead of letting predicates push down.

- Treat every reused expensive CTE or derived subquery as a possible materialization, spill, or motion point.
- Before finalizing, list reused CTEs/subqueries that contain heavy scans, aggregations, window functions, or central joins.
- Check `EXPLAIN` through `db-access` for materialize/spill-like plan shape, repeated expensive subplans, and extra `Motion` around CTE boundaries.
- Avoid forcing a large CTE boundary when the same logic can be expressed as a predicate-pushed subquery or a staged temp table with clear distribution.
- If a CTE is intentionally used as a readable or reusable boundary, mention the tradeoff when it is material to performance.
- When a shared driving CTE is reused to key-filter several large facts, verify the plan does not turn that readability boundary into an outsized materialization or row-estimate problem.
- Small dimension/filter/params CTEs are fine to reuse.

## Greenplum red flags

Pause and re-check metadata, MPP shape, or validation if the query has:

- `SELECT *`;
- casts in `JOIN` or `WHERE`;
- a heavy `JOIN` without checking distribution keys or row reduction;
- a broad table scan without partition/date filters where the task should be narrow;
- DDL or load syntax that assumes modern PostgreSQL features not proven available in the target Greenplum version;
- staging tables whose distribution, partition, or storage shape is implicit and unproven for the load mechanics;
- a params CTE that prevents static partition pruning in standalone fixed-period SQL;
- all partitions selected on a partitioned history table without a semantic reason;
- all-history history/event scans used as ordinary smoke coverage/category metrics instead of explicitly named pointer/reference checks;
- reusable heavy fact/history CTEs that scan a broad date window before applying an available selective driving-key filter downstream;
- a large `Seq Scan` that exceeds the constrained driving set by orders of magnitude;
- major `Broadcast Motion` / `Redistribute Motion` not considered in the plan;
- `Shared Scan` / `Materialize` / reused CTEs around heavy branches without an explicit accept/rewrite decision;
- suspicious row estimates that differ sharply from cheap actual counts for the selected window;
- validation counts copied from an earlier draft after the query's period, source table, pruning predicates, or join shape changed;
- `EXPLAIN` summaries that mention only "planned successfully" or only partition pruning while ignoring `Motion`, distribution, large scans, materialization, or row estimates;
- `EXPLAIN` summaries that omit whether the plan used GPORCA or the legacy Postgres query optimizer;
- GPORCA fallback patterns such as row/tuple expressions, `count(alias.*)`, ordered-set percentiles, or `LATERAL` in heavy analytic SQL;
- plan-sensitive patterns such as `DISTINCT ON`, complex `UNION`, or array-heavy expressions without an actual `EXPLAIN`;
- assumptions about one row per Greenplum key that were not verified from metadata, repo contracts, or business logic.
