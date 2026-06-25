# Native Shape

Use this file before returning any non-trivial ClickHouse SQL.

The goal is not to force every ClickHouse feature into every query. The goal is to make generic SQL unacceptable until ClickHouse-native alternatives have been considered and rejected for a concrete reason.

## Mandatory pass

Before finalizing SQL, classify every non-trivial query shape by business intent. This is a local review pass; database checks mentioned here still go through `db-access`.

- joins and lookup enrichment after `sql-quality-core` defines the intended business grain and unmatched-row behavior;
- `ASOF JOIN` and "latest state at event time" enrichment;
- `IN (SELECT ...)`, `EXISTS`, `NOT IN`, and anti-filters;
- window functions;
- "latest row", "first row", "best row", and deduplication logic;
- sequence logic inside a group;
- `DISTINCT`;
- `FINAL`;
- heavy filters, `PREWHERE` opportunities, and wide table reads.

For each shape:

1. Identify the business intent.
2. Check the ClickHouse-native alternatives below.
3. Use the native alternative when it preserves semantics.
4. Keep generic SQL only when the native alternative would change results, is unsupported on the target contour, or is worse for the actual local data shape.

## Decision table

| Intent | Prefer first | Generic form to challenge | Keep generic only when |
|---|---|---|---|
| Report by a concrete business entity | drive the final query from that entity's matched rows | broad outer base plus `HAVING matched_count > 0` | unmatched coverage is explicitly part of the report and metrics are conditional |
| One current/latest/best row per group | `argMax`, `argMin`, aggregation with explicit tie-break tuple | `row_number() OVER (...) = 1` | true row-level window semantics are required or aggregate rewrite changes the selected row |
| One value per group chosen by ordering | `argMax(value, order_key)` / `argMin(value, order_key)` | window rank, self-join to max timestamp | ties or multi-row output are business-significant |
| Latest state at another event timestamp with a unique right side | `ASOF JOIN` over `(equality keys, as-of timestamp)` after uniqueness is proved | self-join to max timestamp, window rank before join | row-level semantics require a different pattern |
| Latest state at another event timestamp with duplicate right-side timestamps | pre-reduce duplicates with a stable tie-break, then `ASOF JOIN` | raw `ASOF JOIN` over duplicate `(key, timestamp)` rows | duplicate rows are business-significant and another row-preserving pattern is required |
| Ordered sequence inside a group | `groupArray` with `arraySort`, `arrayReverseSort`, `arrayMap`, `arrayFilter`, `arrayEnumerate`, `arrayZip` | many window functions over the same partition | groups are too large, memory risk is unacceptable, or row-level output is required |
| Existence filter on right side | `LEFT SEMI JOIN` | `WHERE key IN (SELECT key ...)`, `EXISTS` | right side is tiny constant data, tuple membership is clearer, or local testing shows the subquery form is better |
| Absence filter on right side | `LEFT ANTI JOIN` | `NOT IN (SELECT ...)`, `NOT EXISTS`, left join plus `IS NULL` | null semantics or business rules require the generic form |
| Lookup enrichment by dictionary key | `dictGet(...)` | lookup `JOIN` | there is no suitable dictionary or the lookup logic is more complex than dictionary lookup |
| Lookup enrichment by table with non-meaningful duplicates | `LEFT ANY JOIN` after reducing the right side if needed | ordinary `LEFT JOIN` | duplicate right-side rows are business-significant or deterministic choice must be built first |
| Lookup enrichment from a one-row-per-key CTE/subquery | `LEFT ANY JOIN` | ordinary `LEFT JOIN` | duplicate right-side rows are intentionally significant and the final grain expects row multiplication |
| Match/unmatched metrics after outer lookup | explicit `toUInt8(1)` match flag from the right side | `right_col IS NULL` / `IS NOT NULL` after `LEFT JOIN` | `join_use_nulls = 1` is deliberately set and validated |
| Large lookup/dimension table for a narrow driving set | key-filter/reduce the lookup to driving keys, then `LEFT ANY JOIN` | scanning the whole lookup table before join | right side is small, dictionary-like, or measured full scan is acceptable |
| Pointer/reference-id existence check | collect distinct relevant ids, then use one key-filtered referenced-table CTE | several unfiltered joins to the referenced table | check is intentionally all-history, named as such, and scan cost is accepted |
| Heavy history/enrichment table used after a narrow driving set | key-filter with `LEFT SEMI JOIN` before aggregation, `ASOF JOIN`, or lookup enrichment | scanning and grouping the whole date window before joining | key filtering would change semantics, the driving key set is not selective, or measured plan shows no benefit |
| Heavy date-partitioned fact for smoke/lifecycle metrics | bounded date window plus key filter, with outside-window/missing metrics when useful | key-only all-history fact scan | the metric is intentionally all-history and named/justified as such |
| Same heavy fact used for smoke coverage and pointer checks | two branches: bounded coverage/categories, plus explicitly named all-history pointer check | one all-history branch used for both coverage and pointer checks | the task explicitly asks for all-history coverage and the output names it that way |
| Heavy fact joined to a unique driving CTE while using driving columns | `ANY INNER JOIN` or `LEFT SEMI JOIN` after proving the driving side is unique at the join key | plain `JOIN` | right-side multiplicity is intentional and part of the output grain |
| Category-specific metrics on enum-like fields | metrics for every material category plus optional `other_*` / `null_*` | metrics for only the categories guessed from memory | omitted categories are immaterial by actual data check or task scope |
| Many-to-many relationship | ordinary `JOIN` | forced `ANY` join | right-side multiplicity is part of the result |
| Deduplication | aggregation by the real grain, `argMax` / `argMin`, or engine-aware reader logic | `SELECT DISTINCT` | the whole selected tuple is truly the business grain |
| Read latest MergeTree state | table-specific reader pattern, carefully justified `FINAL` | casual `FINAL`, unsafe manual collapse | correctness requires merged state and no cheaper validated local reader pattern exists |
| Percentiles on large groups | approximate quantile family used by the project, for example `quantileTDigest` | `quantileExact` | exact percentile is explicitly required and memory cost is acceptable |
| Selective filtering on wide tables | filters aligned with `PARTITION BY` / `ORDER BY`, `PREWHERE` when appropriate | late filtering after heavy reads | filter cannot be pushed or tested plan shows no benefit |

## Required rejection checks

A query shape is not acceptable if it contains any of these constructs without a semantic reason:

- `OVER (...)`;
- final query driven by a broader entity than the requested report grain without an explicit reason;
- central outer join whose unmatched rows are included in aggregate metrics without conditional aggregation;
- `ASOF JOIN` whose right side is not proved unique at `(equality keys, as-of timestamp)` and is not reduced with a stable tie-break;
- heavy history/enrichment table aggregated or ASOF-joined before checking whether it can be restricted to relevant business keys;
- large lookup/dimension/reference table scanned whole before a lookup join when a narrow driving key set exists;
- several unfiltered pointer/reference checks against the same large referenced table;
- heavy date-partitioned fact read as all-history when the task is smoke/lifecycle and the metric is not named or justified as all-history;
- one all-history branch used for both smoke coverage/category metrics and pointer/reference checks on a heavy date-partitioned fact;
- plain `JOIN` to a driving CTE when the right side should be unique and multiplicity is not part of the result;
- category-specific metrics that omit material actual values from the checked data without an `other_*` metric;
- ordinary `LEFT JOIN` to a lookup-shaped right side;
- ordinary `LEFT JOIN` to a right side already reduced to one row per key;
- matched/unmatched counts based on `right_col IS NULL` after ClickHouse outer joins with default joined values;
- `WHERE ... IN (SELECT ...)`;
- `NOT IN (SELECT ...)`;
- `SELECT DISTINCT`;
- `FINAL`;
- manual `GROUP BY ... HAVING sum(sign) > 0` used as a replacement for engine semantics without proving the selected grain;
- `quantileExact` on production-sized grouped data without an exactness requirement;
- `SELECT *` on a production mart or wide table.

Do not print a long explanation for every rejected alternative unless the user asked for reasoning. Still perform the check before returning SQL.

## Preferred rewrites

### Latest row per group

Prefer:

```sql
SELECT
      source.client_id                         AS client_id
    , argMax(source.status, source.updated_at) AS last_status
FROM client_status source
GROUP BY source.client_id
```

Challenge:

```sql
SELECT
      ranked.client_id AS client_id
    , ranked.status    AS last_status
FROM (
    SELECT
          source.client_id                                                AS client_id
        , source.status                                                   AS status
        , row_number() OVER (PARTITION BY source.client_id
                             ORDER BY source.updated_at DESC)             AS rn
    FROM client_status source
) ranked
WHERE ranked.rn = 1
```

If tie behavior matters, express it explicitly:

```sql
argMax(source.status, tuple(source.updated_at, source.event_id)) AS last_status
```

### Latest row as of another timestamp

For "last state before event time" logic, `ASOF JOIN` is a good ClickHouse-native primitive only when the right side has deterministic shape.

Before using `ASOF JOIN`:

- verify the right side is unique at `(equality keys, as-of timestamp)`, or reduce it first;
- restrict the right-side history table to relevant left-side business keys before reduction when that preserves semantics;
- if duplicate timestamps exist, choose a stable tie-break such as `argMax(value, tuple(asof_ts, stable_id))` or pre-aggregate duplicate `(key, asof_ts)` rows with `argMax(value, stable_id)`;
- remember that `ORDER BY key, asof_ts` does not choose deterministically between rows with the same timestamp.

If the task asks for "latest pricing/status/state at received/event time", this check is mandatory even when the query compiles and returns rows.

### Key-filter heavy enrichment before reducing it

When a query first builds a narrow set of business keys and then enriches it from a large history or lookup table, try to push those keys into the heavy table before expensive work:

- build a key-only CTE such as `relevant_orders` or `active_clients`;
- apply `LEFT SEMI JOIN relevant_orders USING (order_id)` to the heavy history table before `GROUP BY`, `argMax`, `ASOF JOIN`, or wide lookup enrichment;
- compare the filtered row count against the unfiltered date-window row count for smoke/test tasks when `db-access` validation is available;
- if the table's `ORDER BY` starts with the key, check through `db-access` whether `EXPLAIN` improves primary-key/granule pruning.
- If the key filter causes repeated CTE reads, do not remove it as the default fix. Prefer a one-flow rewrite, a minimal key-only subquery, or a documented row-count tradeoff.

Do not add the key filter if it would remove rows that are required for the business result. If the filter is intentionally skipped on a heavy table, state the reason and compare unfiltered versus key-filtered row counts when `db-access` validation is available.

For smoke or lifecycle checks, combine the key filter with the narrowest semantically valid date window when the heavy table is date-partitioned. A key-only scan across all history is acceptable only when the metric is explicitly all-history and the added scan is justified.

### Key-filter large lookup and reference checks

Do not reserve key-filtering only for fact/history tables. If the driving set contains a narrow list of lookup keys, filter large lookup, dimension, or reference right sides before the lookup join unless the table is known small or the full scan is measured and accepted.

Prefer:

```sql
WITH
   orders_day AS (
    SELECT
          orders.order_id     AS order_id
        , orders.client_id    AS client_id
    FROM mart_product.orders orders
    WHERE orders.received_ts >= toDateTime('2026-04-29 00:00:00')
      AND orders.received_ts <  toDateTime('2026-04-30 00:00:00')
), order_clients AS (
    SELECT DISTINCT
          orders_day.client_id AS client_id
    FROM orders_day
), clients AS (
    SELECT
          client.client_id AS client_id
        , client.segment   AS segment
    FROM mart_product.client client
    LEFT SEMI JOIN order_clients ON client.client_id = order_clients.client_id
)
SELECT
      orders_day.order_id AS order_id
    , clients.segment     AS segment
FROM orders_day
LEFT ANY JOIN clients ON orders_day.client_id = clients.client_id
```

For pointer/reference checks, collect all relevant pointer ids once, then check the referenced table once:

```sql
WITH
   orders_day AS (
    SELECT
          orders.order_id              AS order_id
        , orders.order_pricing_id      AS order_pricing_id
        , orders.last_order_pricing_id AS last_order_pricing_id
    FROM mart_product.orders orders
    WHERE orders.received_ts >= toDateTime('2026-04-29 00:00:00')
      AND orders.received_ts <  toDateTime('2026-04-30 00:00:00')
), relevant_pricing_ids AS (
    SELECT DISTINCT
          orders_day.order_pricing_id AS order_pricing_id
    FROM orders_day
    WHERE orders_day.order_pricing_id IS NOT NULL

    UNION DISTINCT

    SELECT DISTINCT
          orders_day.last_order_pricing_id AS order_pricing_id
    FROM orders_day
    WHERE orders_day.last_order_pricing_id IS NOT NULL
), referenced_pricing_ids AS (
    SELECT DISTINCT
          pricing.order_pricing_id AS order_pricing_id
        , toUInt8(1)               AS has_pricing_id
    FROM mart_product.order_pricing pricing
    LEFT SEMI JOIN relevant_pricing_ids ON pricing.order_pricing_id = relevant_pricing_ids.order_pricing_id
)
SELECT
      count()                                            AS n_orders
    , countIf(referenced_pricing_ids.has_pricing_id = 1) AS n_order_pricing_id_found
FROM orders_day
LEFT ANY JOIN referenced_pricing_ids ON orders_day.order_pricing_id = referenced_pricing_ids.order_pricing_id
```

If the referenced table cannot be pruned by the pointer key and the check intentionally scans history, name the metric or CTE as `*_all_history` and record the scan tradeoff in validation notes.

If the same referenced/history table also supplies smoke coverage or category metrics, do not reuse the all-history pointer branch for those metrics. Add a bounded coverage branch first, then compare it with the all-history pointer branch:

- `n_orders_with_pricing_bounded` / category counts use `order_pricer_ts` or the relevant event timestamp window;
- `n_orders_with_pricing_all_history` or pointer-id found counts use the all-history branch only when the task needs current/historical references;
- `n_orders_pricing_outside_window` makes the tail visible instead of silently replacing bounded smoke with all-history coverage.

### Driving CTE joins that need driving columns

When a heavy fact joins to a constrained driving CTE and needs columns from that CTE, do not keep plain `JOIN` by habit. If the driving CTE is one row per business key, prefer `ANY INNER JOIN` or `LEFT SEMI JOIN` after proving uniqueness at that key. Keep plain `JOIN` only when driving-side duplicates are business-significant and should multiply the fact rows.

### Existence filtering

Prefer `LEFT SEMI JOIN` when the right side is used only to keep matching left rows:

```sql
SELECT
      orders.order_id  AS order_id
    , orders.client_id AS client_id
FROM orders
LEFT SEMI JOIN active_clients ON orders.client_id = active_clients.client_id
```

ClickHouse allows selecting columns from the right side of `LEFT SEMI JOIN`. Do not claim those columns are unavailable. However, when right-side columns are part of the output semantics, do not treat `SEMI` as a generic enrichment join by habit:

- if the right side is unique at the join key and `SEMI` is kept, note that the right attributes are deterministic for the checked data;
- if the right side can have duplicates, use `LEFT ANY JOIN` after deterministic reduction, `argMax`/pre-aggregation, or another row-choice pattern that matches the business meaning;
- if the right side is used only for membership, project only left-side columns to make the intent obvious.

For production-sized `LEFT SEMI JOIN`, also check the physical side. ClickHouse may spend memory filling/building the right side. If the right side is a heavy `FINAL` reader, large fact, or expensive CTE, use `EXPLAIN`/query-log evidence when available, or flip/rewrite the join so the heavy branch is not the filled right side while preserving the intended left-row output.

Challenge:

```sql
WHERE orders.client_id IN (
    SELECT client_id
    FROM active_clients
)
```

### Absence filtering

Prefer `LEFT ANTI JOIN` when the right side is used only to remove matching left rows:

```sql
SELECT
      orders.order_id  AS order_id
    , orders.client_id AS client_id
FROM orders
LEFT ANTI JOIN blocked_clients ON orders.client_id = blocked_clients.client_id
```

### Lookup enrichment

Prefer `dictGet(...)` for ready dictionaries. Prefer `LEFT ANY JOIN` for lookup-shaped tables when duplicate right-side rows are not meaningful:

```sql
SELECT
      orders.order_id     AS order_id
    , orders.client_id    AS client_id
    , clients.client_name AS client_name
FROM orders
LEFT ANY JOIN dim_client clients ON orders.client_id = clients.client_id
```

If the right side can contain several business-significant rows per key, do not use `ANY`. Pre-aggregate or select the correct row first, for example with `argMax`, then join to that reduced result.

If a `LEFT JOIN` is kept only to preserve unmatched left rows, still challenge it with `LEFT ANY JOIN`. `LEFT ANY JOIN` also preserves unmatched rows and avoids accidental multiplication when the right side should be one row per key.

For match metrics after an outer join, do not count `right_col IS NULL` / `IS NOT NULL` on ordinary right-side columns. With ClickHouse default `join_use_nulls = 0`, unmatched non-Nullable right columns are filled with type defaults such as `0`, so `right_id IS NOT NULL` can be true even for misses. Add an explicit match flag inside the right side:

```sql
WITH
   orders_day AS (
    SELECT
          orders.order_id  AS order_id
        , orders.client_id AS client_id
    FROM mart_product.orders orders
    WHERE orders.received_ts >= toDateTime('2026-04-29 00:00:00')
      AND orders.received_ts <  toDateTime('2026-04-30 00:00:00')
), clients AS (
    SELECT
          client.client_id AS client_id
        , client.segment   AS segment
        , toUInt8(1)       AS has_client_match
    FROM mart_product.client client
    LEFT SEMI JOIN orders_day ON client.client_id = orders_day.client_id
)
SELECT
      count()                                                AS n_orders
    , sum(ifNull(clients.has_client_match, 0))               AS n_orders_with_client
    , count() - sum(ifNull(clients.has_client_match, 0))     AS n_orders_without_client
FROM orders_day
LEFT ANY JOIN clients ON orders_day.client_id = clients.client_id
```

### Sequence logic

For sequence logic inside a group, prefer an array-shaped solution before stacking windows:

```sql
SELECT
      source.client_id                                            AS client_id
    , arrayMap(x -> x.2,
               arraySort(x -> x.1,
                         groupArray((source.event_at, source.status)))) AS status_path
FROM client_events source
GROUP BY source.client_id
```

Use a window function when the required output remains row-level or the grouped arrays would be too large.
