# ClickHouse SQL Metadata And Shape

Use this file before returning non-trivial ClickHouse SQL code.

`sql-quality-core` owns engine-agnostic SQL quality checks: source choice, repo-backed proof, driving grain, central join sanity, multi-row fact semantics, category-safe metrics, date-window semantics, proxy timestamp coverage, smoke scale, and general validation mindset.

This file owns ClickHouse-specific SQL metadata and shape checks: table metadata shape, MergeTree semantics, native primitives, physical pruning evidence, and ClickHouse plan interpretation. Final task status, artifact readiness, approval gates, and proof-level wording belong to `agent-workflow-core`.

Precondition: apply `agent-workflow-core` first for task delivery, local context, and `environment.md` rules. If metadata inspection, `EXPLAIN`, query log checks, or bounded validation need database access, use `db-access`.

## Responsibility split

- `sql-quality-core` owns business SQL quality.
- `clickhouse-sql` owns ClickHouse syntax, native query shape, engine correctness, physical pruning evidence, and ClickHouse-specific plan interpretation.
- Use `db-access` for database access, including metadata, `EXPLAIN`, query log checks, and bounded validation queries.

Use all applicable skills together for real ClickHouse work.

## Metadata pass

Before drafting or finalizing non-trivial SQL against real ClickHouse objects:

1. Identify every real source table, dictionary, and target table involved.
2. Inspect metadata through `db-access` when database access is needed:
   - columns and types;
   - engine;
   - `ORDER BY`;
   - `PARTITION BY`;
   - primary-key shape and row volume when available.
3. Use repo contracts, dbt YAML, compiled SQL, local DDL, or source definitions only when DB metadata is unavailable or the task is explicitly text-only.
4. If metadata is unavailable and the query depends on uncertain columns, engine, keys, or partitions, state the limitation instead of guessing.

Metadata inspection is required because ClickHouse SQL choices depend on table shape, not only on column names.

## Physical Source-Shape Fit

Before designing or validating a ClickHouse mart, DDL/load, or production-like SELECT over heavy sources:

- name the business timestamp/window that defines the requested rows;
- compare it to each heavy source's `PARTITION BY`, primary key, and `ORDER BY` shape;
- identify the predicate that ClickHouse can actually use for partition/key pruning;
- run or record `EXPLAIN indexes = 1` evidence for the proposed bounded predicate when database access is available;
- if the business timestamp differs from the physical partition-driving timestamp, record the proxy/guard predicate and its pruning evidence, then rely on `sql-quality-core` for business-window coverage;
- do not treat a bounded result sample as engine-ready when the plan still reads all parts/granules of a heavy source for the chosen business window.

Example: if a response-quality mart is defined by `zayavka_ts`, but the candidate source partitions by `order_received_ts`, a guard on `order_received_ts` can be valid ClickHouse pruning evidence. It is not full response-date coverage proof unless `sql-quality-core` coverage checks prove that the guard does not exclude valid `zayavka_ts` rows.

For ClickHouse mart-build candidates where the business timestamp differs from the physical partition-driving timestamp, do not stop at "proxy guard is faster" or "business timestamp is expensive." Before marking the candidate review-ready, save one of these proof paths in object-local evidence:

- business-timestamp path: `EXPLAIN indexes = 1` plus bounded smoke on the business timestamp, if safe enough for the contour;
- proxy-coverage path: a bounded proxy guard plus explicit outside-proxy coverage counts for the business window and the proposed rebuild window;
- held path: rejected proof designs with the concrete cost/blocker, and an object status below sandbox handoff.

Do not mark such a candidate `read_only_validated` for a response-date or event-date mart when only a proxy/cohort surface was proven. Either make the output semantics explicitly cohort/proxy-scoped, prove coverage for the business window, or hold the object.

## What metadata should change

Use ClickHouse metadata to choose:

- date filters that match `PARTITION BY`;
- key-aware joins that respect `ORDER BY` and table grain;
- `LEFT ANY JOIN`, `LEFT SEMI JOIN`, `LEFT ANTI JOIN`, or pre-aggregation when right-side multiplicity allows it;
- whether a heavy history/enrichment table can be restricted to relevant left-side business keys before expensive aggregation or lookup work;
- whether a large lookup, dimension, or reference table can be restricted to the narrow driving key set before building a lookup join;
- whether pointer/reference-id checks can use one distinct relevant-id CTE instead of repeated scans of the referenced table;
- `argMax` / `argMin` tie-break tuples using real timestamp and id columns;
- whether `ASOF JOIN` has a deterministic right side at `(equality keys, as-of timestamp)`, and which stable id should break ties when it does not;
- whether `FINAL` is necessary for `ReplacingMergeTree`, `CollapsingMergeTree`, or `VersionedCollapsingMergeTree`;
- whether `PREWHERE` is worth considering on wide tables with selective filters;
- whether casts are avoidable because real column types already match.

For smoke or lifecycle checks on heavy fact/history tables with date partitioning, a key filter alone is not enough unless the metric is intentionally all-history. Prefer a bounded date window plus explicit outside-window or missing metrics. If full history is the correct semantic shape, name the metric `*_all_history` or equivalent and compare/accept the added scan cost.

When the same heavy table is used both for smoke coverage/categories and for pointer/reference-id validation, split the shapes. Use a bounded date window for smoke coverage/category metrics, and a separate key-filtered `*_all_history` branch only for pointer/reference checks that truly need historical ids. Do not let the all-history branch become the only pricing/fact coverage metric by accident.

For `order_pricing`-like tables this is mandatory in smoke SQL: `pricing_coverage` / `pricing_categories` should be bounded by the pricing timestamp window, while `order_pricing_id` / `last_order_pricing_id` reference checks may use an explicitly named all-history branch. If the bounded branch misses keys that all-history finds, report `outside_window` / `all_history_only` counts instead of replacing bounded coverage with all-history coverage.

## Engine correctness

Correctness comes before avoiding expensive engine readers.

- Do not remove `FINAL` from `ReplacingMergeTree`, `CollapsingMergeTree`, or `VersionedCollapsingMergeTree` just because `FINAL` is expensive.
- Prefer the existing local reader pattern from repo models for the same table unless there is a measured reason to change it.
- Manual replacement for `FINAL` is allowed only when the selected output grain and selected columns are explicitly preserved.
- For `VersionedCollapsingMergeTree`, a plain `GROUP BY ... HAVING sum(sign) > 0` is not a general reader. It is acceptable only for existence/key filtering or when every selected field is correctly aggregated for the target business grain.
- If manual collapsing is used instead of `FINAL`, validate equivalence on a constrained window or state the semantic assumption.
- If the table may already be compacted, that does not by itself prove a manual reader is correct; it only affects current physical state.

## Partition replacement safety

For any build that writes a temp/staging table and swaps data with `REPLACE PARTITION`:

- write staging DDL with an explicit MergeTree-compatible engine, `PARTITION BY`, and `ORDER BY`, or prove that `CREATE TABLE ... AS target` inherits an exactly compatible physical shape on the target ClickHouse version;
- inspect the target table `PARTITION BY` expression before finalizing the load SQL;
- compare the partition expression with the rows materialized into the temp table;
- ensure the temp table contains the full target partition being replaced, not only the current logical refresh slice;
- a daily build must not run `REPLACE PARTITION toYYYYMM(report_dt)` against a monthly-partitioned target unless it materializes the full month;
- if the intended refresh grain is daily, prefer a daily target partition such as `event_dt`/`toYYYYMMDD(event_dt)`, or change the build to reconstruct the full monthly partition;
- record the decision in the validation notes when designing a new mart or changing a partitioned load.

For existence checks, name the CTE as an active-key filter and select only the key fields needed downstream.

## DDL/load syntax self-review

Before returning ClickHouse DDL or load files:

- verify all DDL syntax is ClickHouse-native for the expected version, including table comments, column comments, codecs, TTL, settings, temporary table syntax, and `CREATE TABLE ... AS ...` behavior;
- do not use nonstandard quoting forms such as dollar-quoted comments unless the target ClickHouse version is proven to accept them;
- if `db-access` can safely run a parse-only or bounded DDL/load check in an approved sandbox, use it when the workflow layer has approved that validation; otherwise mark syntax/runtime proof as unproven and report the engine-check blocker;
- if a self-review finds invalid DDL/load syntax, fix the artifact before reporting engine-check passed. Sandbox validation is not a place to discover mistakes the agent can catch by reading the final code.

## Lightweight validation

Before returning a non-trivial production `SELECT`:

- Prefer `EXPLAIN indexes = 1` or `EXPLAIN PLAN` for the drafted query.
- Use `EXPLAIN PIPELINE` when pipeline shape matters.
- Interpret the plan. A successful `EXPLAIN` only proves the query can be planned; it does not prove the shape is acceptable or make the task ready.
- When interpreting `EXPLAIN indexes = 1`, look beyond selected parts. Check granules read, primary-key conditions, and whether heavy tables still show `PrimaryKey Condition: true` or read all granules inside selected partitions.
- If the query reuses CTEs or derived subqueries, scan the plan for repeated `ReadFromMergeTree` nodes for the same heavy tables, especially `FINAL` readers and central join branches.
- Do not execute a heavy full query just to prove syntax or confidence.
- For bounded smoke or validation SQL that the agent creates itself, `EXPLAIN` alone is not enough. After the plan is acceptable, run the final aggregate/query on the constrained window unless it is unsafe, exceeds the contour's practical limits, or the user explicitly asked for text-only SQL. If skipped, state the concrete blocker.
- If a result check is useful, run a constrained check through `db-access`, such as a narrow date window, `LIMIT`, aggregated row counts, or metadata-only checks.
- For heavy enrichment tables, compare unfiltered date-window row counts with row counts after applying relevant business keys when a cheap count is possible through `db-access`.
- For large lookup, dimension, or reference tables, key-filter the right side to the driving keys when the left set is narrow. Keep a full lookup scan only when the table is genuinely small, dictionary-like, or the full scan is measured and accepted.
- For pointer/reference-id checks, collect the relevant ids from the driving rows, deduplicate them, and check the referenced table through one key-filtered CTE. Do not run several unfiltered full-table lookups against the same referenced table for separate pointer columns.
- Pointer/reference validation is not a substitute for bounded smoke coverage. If a query reports both pricing/fact coverage and pointer existence from the same heavy table, check that the coverage branch is bounded and the pointer branch is explicitly named all-history when it scans history.
- For outer-join match metrics, project an explicit right-side flag such as `toUInt8(1) AS has_client_match` from the reduced right side and count that flag after the join. Do not infer unmatched rows from `right_col IS NULL` unless `join_use_nulls = 1` is deliberately set and validated.
- If a selective key filter creates repeated CTE reads, do not drop the key filter as the first fix. Compare unfiltered vs key-filtered row counts, then try a one-flow rewrite, a minimal key-only subquery, or an explicitly accepted tradeoff.
- If the user requested an eval/reasoning artifact, record the material validation signals in that artifact: final smoke result counts, `EXPLAIN` parts/granules/primary-key conditions, repeated `ReadFromMergeTree`, heavy-table scan shape, and accept/rewrite decisions. Do not create such an artifact unless the user asked for it.
- Do not write that `EXPLAIN` was "not saved" or "not run" as an acceptable validation state in an eval/reasoning artifact. If `EXPLAIN` is absent, record the concrete blocker or error; if the final smoke query executed, `EXPLAIN indexes = 1` should normally execute too.
- If validation cannot be run because `db-access` is unavailable, the query is text-only, or execution would be too risky, say so briefly.

For optimization tasks, also use `system.query_log` metrics when available; see `optimization.md`.

## CTE reuse and inlining

ClickHouse CTEs are query text abstractions, not guaranteed materialized temp results.

- Treat every reused expensive CTE or derived subquery as a possible repeated scan.
- Before finalizing, list reused CTEs/subqueries that contain `FINAL`, heavy MergeTree reads, or central joins.
- Check `EXPLAIN` output obtained through `db-access` for duplicated `ReadFromMergeTree` nodes when one of those CTEs/subqueries is referenced more than once.
- Do not treat `EXPLAIN` as passed until duplicated heavy reads are interpreted as either acceptable for the constrained task or fixed.
- Avoid reusing heavy CTEs multiple times in standalone `SELECT`s when the same logic can be expressed in one flow.
- If `EXPLAIN indexes = 1` shows repeated reads of heavy CTEs or repeated `FINAL` scans, rewrite the query or explicitly state why the repeated reads are acceptable.
- If repeated scans are unavoidable, mention the tradeoff or propose a materialized intermediate table/model when the task allows it.
- Small dimension/filter CTEs are fine to reuse.

## ClickHouse red flags

Pause and re-check metadata, native shape, or validation if the query has:

- `SELECT *`;
- casts in `JOIN` or `WHERE`;
- `FINAL`;
- window functions where `argMax`, `argMin`, arrays, or pre-aggregation may fit better;
- ordinary `LEFT JOIN` to a lookup-shaped table;
- ordinary `LEFT JOIN` to a right side already reduced to one row per key, where `LEFT ANY JOIN` expresses the intended lookup and protects against accidental multiplication;
- `IN (SELECT ...)` where a semi-join or key-filter shape may be clearer;
- the same heavy CTE referenced more than once;
- broad MergeTree reads without partition/date filters;
- DDL comments or string literals written with syntax not proven valid for the target ClickHouse version;
- staging tables for `REPLACE PARTITION` whose engine, partition, or order shape is implicit and unproven;
- `REPLACE PARTITION` whose target partition is wider than the rows materialized in the temp table;
- heavy history/enrichment tables read by date only even though a selective business-key set is available;
- large lookup/dimension/reference tables read whole even though the driving key set is narrow and selective;
- repeated unfiltered pointer/reference checks against the same large referenced table;
- match/unmatched metrics after `LEFT JOIN` / `LEFT ANY JOIN` that use `right_col IS NULL` or `IS NOT NULL` on non-Nullable right-side columns under default `join_use_nulls = 0`;
- heavy fact/history tables read by business keys only while skipping a semantically relevant date partition window for smoke/lifecycle checks;
- all-history metrics that are not named as all-history and not justified by the task;
- category-specific metrics that use guessed enum values without checking the actual material values for the chosen window;
- removing a selective key filter from a heavy history/enrichment table only to avoid CTE inlining, without row-count comparison or another rewrite attempt;
- `EXPLAIN` summaries that mention only parts and ignore granules, primary-key conditions, or all-granule reads within selected partitions;
- `EXPLAIN` summaries for queries with reused CTEs/subqueries that do not mention repeated `ReadFromMergeTree` checks;
- eval/reasoning artifacts that omit `EXPLAIN` without a concrete blocker;
- `ASOF JOIN` without a right-side duplicate check or deterministic tie-break;
- assumptions about one row per ClickHouse key that were not verified from metadata, repo contracts, or business logic.
