# Optimization

Use this file when the task is about speeding up or diagnosing Greenplum SQL.

## Diagnostic workflow

- Do not rewrite a query blindly. Start from the actual plan.
- For non-trivial production `SELECT`s, do not wait for an explicit optimization request: inspect metadata and run lightweight validation through `db-access` when database access is needed and available; see `sql_readiness.md`.
- For Greenplum, first use `EXPLAIN` through `db-access`; use `EXPLAIN ANALYZE` only when `db-access` and task safety allow it.
- Check the final optimizer line in every material `EXPLAIN`: prefer `Optimizer: Pivotal Optimizer (GPORCA)`. If it says `Optimizer: Postgres query optimizer`, treat this as a performance finding and identify the feature that likely forced legacy planning.
- If configured MCP permissions block `EXPLAIN` or metadata for a referenced schema, stop at the `db-access` boundary, record the exact blocked schema/object, and mark the validation as partial. Do not call an optimization proven when the material plan is unavailable.
- When reading `EXPLAIN ANALYZE`, check at least:
  - whether there is `Motion`
  - where the most expensive steps are
  - whether there is skew across segments
  - whether there is a full `Seq Scan` where narrower reading was expected
- When needed, use system views and `gp_toolkit` through `db-access` to inspect skew and distribution instead of guessing.
- Read the plan, not only its exit status. Extra `Redistribute Motion`, broad `Broadcast Motion`, missing partition pruning, large `Seq Scan`, suspicious row estimates, or CTE materialization boundaries are findings to address or explicitly accept.
- For smoke and validation queries, compare important plan estimates with cheap actual counts for the chosen window. If the plan estimates millions of rows for a narrow smoke window with tens of thousands of actual rows, call that out and decide whether statistics, filters, or query shape need attention.
- Treat `Shared Scan` and `Materialize` as named plan features. They are often normal with CTEs, but a large shared CTE reused across several fact joins can become the main cost center.
- Generic statements such as "partition pruning works" are not enough when the plan also has large scans, repeated source reads, suspicious estimates, `Shared Scan` / `Materialize`, or major `Motion` nodes. Address those findings or explicitly accept them as tradeoffs.
- If pruning improves after a rewrite, still inspect the rest of the plan; better partition selection does not by itself make a query shape acceptable.

## GPORCA vs legacy planner

GPORCA is normally preferred for analytic Greenplum SQL. Legacy `Postgres query optimizer` plans are not automatically wrong, but they lose GPORCA's MPP-aware planning and must be called out in optimization/review work.

Hard fallback patterns verified on the local Greenplum 6.25 contour:

- row/tuple expressions, for example `SELECT (1, 2)`;
- tuple-shaped technical hashes or row expressions inside heavy projection/join/hash paths, such as `md5_hash((uuid, segment_id, key_id)::text)`. Local proof exists on multiple objects: tuple-text hash returned `Optimizer: Postgres query optimizer`, while an explicit `concat(...)` text shape returned GPORCA. Treat any rewrite as semantics-sensitive because delimiters, nulls, numeric/text formatting, and old row-text output must match;
- `count(alias.*)`; use `count(*)` or `count(1)` instead;
- ordered-set percentiles such as `percentile_disc(...) WITHIN GROUP (...)` and `percentile_cont(...) WITHIN GROUP (...)`;
- `LATERAL` joins; prefer a normal join shape with explicit inequality/key conditions when it preserves semantics.

Soft warning patterns:

- `SELECT DISTINCT ON (...)` is plan-sensitive: simple local tests can stay on GPORCA, while real plans may still introduce costly `Unique`, sort, and `Motion` shapes. Verify with `EXPLAIN`; prefer `row_number() OVER (PARTITION BY ... ORDER BY ...)` plus `WHERE rn = 1` when semantics and tie-breaks match;
- complex `UNION` / `UNION ALL` query shapes can be planner-sensitive; simple local tests stayed on GPORCA, so verify with `EXPLAIN` instead of banning them;
- array element access is not always a fallback by itself, but array-heavy expressions should be checked with `EXPLAIN`;
- missing or stale statistics can make plans poor even when GPORCA is used. Treat stale stats as a first hypothesis for bad estimates; check `ANALYZE` needs through allowed metadata/system views when available.

For tuple-hash rewrites, do not stop at "concat returns GPORCA". Save compact before/after `EXPLAIN` anchors and require an equality check on representative rows before calling the rewrite safe for production.

## Core optimization mindset

- In Greenplum, first reduce the amount of data moved between segments, not only local operator cost.
- Treat `Motion` as a major signal in the plan. Extra `Redistribute Motion` or `Broadcast Motion` should be investigated explicitly.
- For heavy `JOIN`s, first test whether performance improves by:
  - pre-aggregating before `JOIN`
  - shrinking the right side earlier
  - moving filters earlier in the plan
  - choosing a more suitable `DISTRIBUTED BY`
- If a large table is filtered by a date range or another natural key, check whether partition pruning actually happens.
- If partition pruning does not happen, treat the issue as structural as well as query-level.
- When a narrow driving set exists, try to filter heavy history/enrichment tables by those keys before aggregation, sorting, or joining.
- When widening a history/enrichment scan for completeness, compare business keys gained with extra rows and partitions read. Prefer a bounded/key-filtered scan with an explicit tail metric for smoke work, a narrow exact fallback for accuracy-critical work, and a full scan only when it is the correct semantic shape.
- For fallback/enrichment branches on partitioned sources, compare partition selectors against the driving period. If the driving table prunes to a small period but the fallback source selects all partitions, treat that as a Greenplum plan finding. Candidate rewrites include a safe date envelope around the driving period plus freshness margin, staging a relevant key set, or a narrow fallback map; preserve fallback priority and prove the envelope does not drop required late matches.
- After `sql-quality-core` has defined fact semantics, make the Greenplum shape match it with pre-aggregation, key filtering, or a deterministic single-row reduction.
- When using `row_number()` as the Greenplum reduction shape, verify that the chosen `ORDER BY` removes ties in the data.

## Distribution, skew, and repeated heavy work

- `DISTRIBUTED BY` is part of performance, not just DDL.
- Evaluate a distribution key by join frequency, distribution uniformity, and skew risk.
- If a heavy aggregation is repeated often, consider not only rewriting the query but also materializing the result into an intermediate or final table.
- Greenplum CTEs can act as optimization fences. For heavy CTEs, check whether a subquery, temp table with a suitable distribution key, or a different flow gives a better plan.
- If a heavy non-partitioned table must be scanned for a smoke report, name the scan and either shrink it by driving keys or explicitly accept it as the cost of the requested relationship.

## Statistics and maintenance

- Do not assume an index will automatically save a heavy analytic table.
- After meaningful data or structural changes, check whether `ANALYZE` is needed.
- If the plan looks unreasonable for the actual data, stale statistics should be one of the first hypotheses.
- After large `DELETE`, `UPDATE`, `INSERT`, or rebuild operations, check whether `VACUUM` and `ANALYZE` are needed.
- For partitioned targets, a full `DELETE FROM target` or full rebuild is a Greenplum physical/runtime finding. Compare it with the partition key and the intended refresh window. A partition/window refresh can be a strong candidate, but only after proving the source freshness contract: late-changing attribution, forecast, revenue, service, or mapping inputs may require a wider refresh or full rebuild.

## What to verify after optimization

- Check not only elapsed time but also how the execution plan changed.
- For key-filter rewrites, compare source rows before and after the key filter when a cheap count is possible through `db-access`.
- For bounded-history rewrites, compare coverage before and after widening as well as partition/row volume. A faster query that silently drops required keys is wrong; a full-history query that recovers only a tiny tail may still be a poor smoke shape.
- The minimum verification set should include:
  - `EXPLAIN` / `EXPLAIN ANALYZE` before and after
  - number and type of `Motion`
  - row volume on large plan nodes
  - presence or absence of partition pruning
  - correctness on a control sample
- If the optimization changes distribution, staging flow, pre-aggregation, or external load pattern, verify separately that grain, update key, and business result did not change.
- If the optimization changes a partitioned-target refresh from full rebuild to window/partition refresh, verify changed-source coverage, late-arriving updates, partition delete/insert shape, and downstream export assumptions before calling it production-safe.
