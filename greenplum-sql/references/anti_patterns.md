# Anti-Patterns

Use this file as a quick filter before returning Greenplum SQL.

For engine-agnostic SQL quality anti-patterns, use `sql-quality-core` first.

## Greenplum anti-patterns

- Do not copy modern PostgreSQL syntax or planner expectations into Greenplum without checking compatibility.
- Do not copy ClickHouse runtime patterns such as `getSetting(...)` into Greenplum.
- Do not return non-trivial SQL against real tables without checking metadata first through `db-access` when database access is needed, or through repo contracts when DB access is unavailable.
- Do not treat a successful `EXPLAIN` as validation until the MPP plan shape has been interpreted.
- Do not ignore the optimizer line in `EXPLAIN`. `Optimizer: Postgres query optimizer` is a material finding for Greenplum optimization/review work; name the likely fallback feature or state that it is unknown.
- Do not summarize `EXPLAIN` only as "planned", "partition pruning works", or "Motion is expected"; name the largest scans, materialization points, major motions, and suspicious row estimates.
- Do not leave surprising EXPLAIN observations unaddressed. Large scans, repeated scans, materialization points, bad estimates, or major Motion should be fixed or explicitly accepted as tradeoffs.

## Query anti-patterns

- Heavy `JOIN` without first checking whether pre-aggregation, shrinking the right side, or filter pushdown would help.
- Ignoring `Motion` in a heavy plan.
- Ignoring distribution keys, partition rules, storage type, or stale statistics when they affect the query.
- Full-deleting or fully rebuilding a partitioned target without checking whether the partition key supports a safe refresh window. Do not propose a partition/window refresh unless late-changing source semantics and downstream export assumptions are named.
- Aggregating a whole heavy enrichment/history table before checking whether relevant business keys can filter it down.
- Letting a fallback/enrichment branch scan every partition while the driving period is narrow, without naming the partition-selector mismatch and testing a safe date envelope, relevant-key stage, or narrow fallback map.
- Treating a CTE as a free readability boundary when it may force materialization, extra `Motion`, or missed predicate pushdown.
- Assuming an index alone will save a heavy analytic table.
- Blind `CAST` in `JOIN` or `WHERE` without verifying real types.
- Repeating the same `current_setting(...)` cast throughout the query instead of declaring it once in `WITH`.
- Using a closed interval or `BETWEEN` for a standard date window when the project pattern is half-open `>= dt_from` and `< dt_to`.
- Writing `md5(a, b)` or another multi-argument hash call that is not valid Greenplum syntax.
- Building a technical hash key without `coalesce(...)` when any component may be nullable and would null out the whole hash.
- Writing ClickHouse-style scalar `WITH` declarations such as `current_setting(...) AS report_dt_from` instead of wrapping runtime settings in a one-row params CTE.
- Using `count(alias.*)`; use `count(*)` or `count(1)`.
- Using row/tuple expressions such as `SELECT (a, b)` in analytic SQL.
- Using tuple-shaped hash text such as `md5_hash((a, b, c)::text)` in heavy analytic SQL, especially in projection/join/hash paths. This shape has repeatedly forced the legacy optimizer in local proof cases. Prefer a GPORCA-friendly explicit text shape only after saving before/after `EXPLAIN` anchors and proving the resulting hash contract is identical; surface `Бизнес-семантика:` when null/delimiter/text-format behavior is not proven.
- Using `SELECT DISTINCT ON (...)` in heavy analytic SQL without checking the actual plan; prefer `row_number() OVER (...)` plus a deterministic filter when semantics and tie-breaks match.
- Using `LATERAL` joins without proving the legacy-planner tradeoff is acceptable; prefer normal joins with explicit key/range predicates when possible.
- Using ordered-set percentiles such as `percentile_disc` / `percentile_cont` inline in a heavy query without checking the optimizer fallback and considering a staged/precomputed percentile flow.

## Greenplum style overlay anti-patterns

- Reusing a newly defined alias inside the same `SELECT` list instead of using an inner CTE/subquery.

## Physical design anti-patterns

- Changing `DISTRIBUTED BY` without understanding downstream joins, skew, and execution behavior.
- Working with heavily changed large tables without checking `ANALYZE` / `VACUUM`.
- Refactoring a script that already contains an explicit `COMMIT` and silently removing the transaction boundary.
