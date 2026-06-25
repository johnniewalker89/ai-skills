# Anti-Patterns

Use this file as a quick filter before returning ClickHouse SQL.

For engine-agnostic SQL quality anti-patterns, use `sql-quality-core` first.

## ClickHouse anti-patterns

- Do not generate generic cross-database SQL when a clearer ClickHouse-native pattern exists.
- Do not return non-trivial SQL against real tables without checking metadata first through `db-access` when database access is needed, or through repo contracts when DB access is unavailable.
- Do not return non-trivial ClickHouse SQL before applying the native-shape review pass from `native_shape.md`.
- Do not execute a heavy production `SELECT` fully just to validate code; when database access is needed and available, prefer `EXPLAIN` through `db-access` or constrained checks through `db-access`.
- Do not treat a successful `EXPLAIN` through `db-access` as validation until the plan shape has been interpreted.
- Do not keep generic SQL constructs just because they are familiar from other databases.
- Do not copy Greenplum or Postgres idioms into ClickHouse without confirming that the pattern is valid and local.
- Do not use `current_setting(...)` in ClickHouse marts when the local pattern is `getSetting(...)`.
- Do not use a closed interval or `BETWEEN` for standard date-window filters when the project pattern is half-open `>= dt_from` and `< dt_to`.
- Do not use `FROM table FINAL AS alias`; review `FINAL` alias placement before live execution.

## Query anti-patterns

- `SELECT *` on wide tables without a real need.
- `FINAL` without explicit necessity.
- Assuming ClickHouse engine, key shape, right-side uniqueness, or column types without checking metadata or repo contracts.
- Replacing `FINAL` with `GROUP BY ... HAVING sum(sign) > 0` on collapsing engines without proving the output grain and selected columns are equivalent.
- Treating a ClickHouse CTE as materialized when it may be inlined and scanned repeatedly.
- Ignoring repeated heavy `ReadFromMergeTree` nodes after `EXPLAIN` through `db-access`.
- Interpreting `EXPLAIN` through `db-access` for a query with reused CTEs/subqueries without checking whether the same heavy table is read more than once.
- Treating `EXPLAIN` parts pruning as enough while ignoring granules, primary-key conditions, or all-granule reads within selected partitions.
- Hiding a partition key inside a dynamic predicate such as `has(array, dt)` and assuming ClickHouse can prune partitions. Prove pruning with `EXPLAIN indexes = 1` or rewrite to an explicit partition-prunable shape.
- Raw `ASOF JOIN` over a history table before checking duplicate `(equality keys, as-of timestamp)` rows or building a deterministic tie-break.
- Aggregating or ASOF-joining a whole history date window before checking whether relevant business keys can filter it down.
- Removing a selective key filter from a heavy history/enrichment table just to avoid CTE inlining without comparing row counts or trying another shape.
- Heavy `JOIN` when `dictGet(...)` would be enough.
- Ordinary `LEFT JOIN` when `LEFT ANY JOIN`, `LEFT SEMI JOIN`, `LEFT ANTI JOIN`, `dictGet(...)`, or pre-aggregation better matches the business intent.
- `IN (SELECT ...)`, `NOT IN (SELECT ...)`, or left join plus `IS NULL` when `LEFT SEMI JOIN` or `LEFT ANTI JOIN` expresses the same intent more directly.
- Claiming that ClickHouse `LEFT SEMI JOIN` cannot expose right-side columns. It can; the real question is whether projecting those columns has deterministic enrichment semantics for the checked right-side grain.
- Using `LEFT SEMI JOIN` as a shortcut enrichment join for right-side attributes when the right side can have multiple matching rows and no deterministic row-choice rule is defined.
- Putting a heavy `FINAL` reader or large fact on the filled right side of `LEFT SEMI JOIN` without plan/query-log evidence that the shape is safe.
- Window functions before rejecting `argMax` / `argMin`, aggregate-based, or array-based solutions.
- `SELECT DISTINCT` before checking whether the real grain should be expressed through `GROUP BY`, `argMax` / `argMin`, or engine-aware reader logic.
- `quantileExact` on large grouped production data unless exact percentile semantics are explicitly required.
- Reading heavy string, JSON-like, or rarely needed columns before filtering.
- Blind `CAST` in `JOIN` or `WHERE` without verifying real types.
- Repeating the same `getSetting(...)` call throughout the query instead of declaring it once in `WITH`.
- Joining to a lookup subquery or table when dictionary enrichment through `dictGet(...)` is the simpler local pattern.
- Doing business mapping directly inside raw dictionary lookups when the cleaner pattern is `raw lookup in WITH -> business mapping in SELECT`.

## ClickHouse style overlay anti-patterns

- Reusing an alias inside `SELECT` before it is defined earlier in the same `SELECT`.
- Writing scalar `WITH` declarations as `alias AS expression` instead of `expression AS alias`.
- Mixing scalar `WITH` and subquery CTE separator patterns in the same chain.

## Schema anti-patterns

- Adding `Nullable` to new fields without real business need.
- Changing `ENGINE`, deduplication, or history semantics in MergeTree-family tables without validating the effect on readers.
