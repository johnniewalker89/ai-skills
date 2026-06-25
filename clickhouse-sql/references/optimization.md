# Optimization

Use this file when the task is about speeding up or diagnosing ClickHouse SQL.

## Diagnostic workflow

- Apply `agent-workflow-core` first for task mode, local context, and delivery rules.
- For non-trivial production `SELECT`s, do not wait for an explicit optimization request: inspect metadata and run lightweight validation through `db-access` when database access is needed and available; see `sql_readiness.md`.
- Do not rewrite a query blindly. Start from actual metrics in `system.query_log` when `db-access` makes those metrics available.
- For mart/build optimization, search `system.query_log` with more than one marker before saying no production run exists:
  - exact target write shape such as `INSERT INTO <database>.<table>` or `INSERT INTO <table>`;
  - target table name alone, excluding `system.query_log`, metadata-only tools, `DESCRIBE`, `SHOW CREATE`, `system.tables`, and `system.columns`;
  - staging/temp write shapes from the build SQL, such as `_target__temp`, `_target__tmp`, or the table named in `REPLACE PARTITION ... FROM <temp_table>`;
  - repo/build comments when present, such as `@MART`, `@DAG`, or job-specific markers.
- If the build writes to a temp/staging table and then swaps partitions into the target, treat the temp-table insert as material runtime evidence for the target build.
- Before accepting a temp/staging plus `REPLACE PARTITION` build shape, verify the target `PARTITION BY` expression against the temp-table row coverage. Replacing a monthly partition with a one-day temp result is a correctness bug, not an optimization tradeoff.
- If any candidate write query is found, summarize recent runtime evidence: last run time, run count/window, duration, read rows/bytes, written rows/bytes, and related follow-up actions such as `OPTIMIZE TABLE ... FINAL`.
- Do not conclude "no real runtime" from a metadata-heavy result page; inspect the filtered query text and metrics for writes to the target.
- For the first pass, check at least:
  - `query_duration_ms`
  - `read_rows`
  - `read_bytes`
  - `memory_usage`
- For optimization review of an existing ClickHouse mart/build/query, run `EXPLAIN` through `db-access` for the current query or for the key expensive subquery/branch when database access is available and execution is safe. If `EXPLAIN` is skipped, record the concrete blocker in the final answer or requested evidence artifact; do not silently replace plan review with metadata/query_log only.
- Before returning substantial new or changed SQL, run `EXPLAIN` through `db-access` when database access is needed, `db-access` validation is available, and execution is safe.
- Read the `EXPLAIN` output, not only its exit status. Repeated heavy `ReadFromMergeTree` nodes, repeated `FINAL` scans, missing partition pruning, `PrimaryKey Condition: true` on large tables, or all-granule reads inside selected partitions are findings to address or explicitly accept.
- For plan and index-reading diagnostics, prefer:
  - `EXPLAIN indexes = 1`
  - `EXPLAIN PLAN`
  - `EXPLAIN PIPELINE`
- Change one thing at a time so the effect is attributable.

## Core optimization mindset

- In ClickHouse, first optimize for lower read volume, not only for fewer rows in the final output.
- Do not trade correctness for speed: engine semantics, deduplication, and collapsing logic must remain valid before optimizing cost.
- Check whether the main filters align with the table `ORDER BY`.
- Check whether the query gets pruning by `PARTITION BY`.
- If the partition filter is hidden inside a dynamic/function-wrapped predicate such as `has(partitions_to_update, dt)`, do not assume pruning works. Test a partition-prunable shape such as explicit bounds, `dt IN (...)`, or a `SEMI JOIN`/key-filter shape with `EXPLAIN indexes = 1`, and compare selected parts/granules.
- When a narrow driving set exists, try to filter heavy history/enrichment tables by those keys before aggregation, sorting, or joining.
- For wide tables and selective filters, verify whether `PREWHERE` is effective.
- For `ORDER BY ... LIMIT N`, avoid reading heavy columns before sorting unless they are truly needed.
- In Top-N style queries, try not to force ClickHouse to read wide payload columns early.
- Remember that CTEs may be inlined; repeated references to a heavy CTE can mean repeated scans.

## Query-shape guidance

- Before finalizing a query, run the native-shape pass from `native_shape.md`; optimization starts with choosing the right ClickHouse primitive for the business intent.
- Prefer aggregation over a window function when the logic allows it.
- For "one best row per group", consider `argMax` / `argMin` before windows.
- For sequence logic inside a group, consider array patterns before windows, but check memory pressure on large groups.
- Avoid `SELECT *` in heavy queries and production marts when not all columns are needed.
- Avoid unnecessary `CAST` and type conversions, especially in `JOIN` and `WHERE`, without verifying real column types first.
- Prefer approximate quantile functions for large production grouped data unless the task explicitly requires exact percentiles.
- For new fields and DDL, avoid `Nullable` when a meaningful `DEFAULT` can express the business meaning, because `Nullable` adds overhead.

## Join optimization

- Do not keep an ordinary `LEFT JOIN` by habit. First classify whether the right side is enrichment, existence filtering, absence filtering, or true many-to-many expansion.
- Before keeping a heavy `JOIN`, check whether the right side can be reduced first.
- Before aggregating a heavy right side for later enrichment, check whether a `LEFT SEMI JOIN` against relevant keys can shrink it first.
- Consider pre-aggregation before `JOIN`.
- Consider replacing a lookup `JOIN` with `dictGet(...)`.
- Consider whether `ANY`, `SEMI`, or `ANTI` semantics better match the business logic and avoid extra work.
- For `LEFT SEMI JOIN`, verify which side is physically filled/built when one side is heavy, especially around `FINAL` readers. A semantically equivalent side swap can be the difference between a normal run and a memory-limit failure.

## Storage-level options

- If a query is regularly slow and SQL cleanup is not enough, consider storage-level changes too.
- Data skipping indexes help only when they can skip enough granules; do not treat them like row-based secondary indexes.
- Consider projections when one table needs faster reads via another sort order or pre-aggregation without changing query text.
- Consider materialized views when expensive aggregation, denormalization, filtering, or multi-step transformation should move from query time to insert time.
- Do not use projections as a replacement for materialized views when the task requires `JOIN`, complex transformation, `WHERE` in projection definition, or mandatory `FINAL`.

## What to verify after optimization

- Check not only elapsed time but also the change in read volume.
- For key-filter rewrites, compare source rows before and after the key filter when a cheap count is possible through `db-access`.
- The minimum verification set should include:
  - `query_duration_ms`
  - `read_rows`
  - `read_bytes`
  - `memory_usage`
  - plan changes in `EXPLAIN` output obtained through `db-access` when database access is needed
- If the query uses `FINAL`, deduplication, `ANY` semantics, dictionaries, or a rewrite from windows to aggregates or arrays, verify separately that the business result did not change.
