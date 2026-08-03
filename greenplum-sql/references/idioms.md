# Idioms

Use this file when the task is about Greenplum-specific query writing, runtime patterns, or DDL concerns rather than only formatting.

## Navigation

- [Compatibility mindset](#compatibility-mindset)
- [Runtime settings and windows](#runtime-settings-and-windows)
- [Greenplum vs generic PostgreSQL](#think-in-greenplum-not-generic-postgresql)
- [Distribution and small tables](#distribution-and-small-tables)
- [Loading from ClickHouse](#loading-from-clickhouse)

## Compatibility mindset

- Treat the working Greenplum contour as compatible with `Greenplum 6.25.1` on top of `PostgreSQL 9.4.26` until proven otherwise.
- Do not automatically bring syntax or features from newer PostgreSQL versions into Greenplum without checking actual support.
- If there is doubt whether a construct is valid, verify it against a local query or an existing project pattern.

## Runtime settings and windows

- In Greenplum mart or DAG contexts, prefer `current_setting('etl....')` for runtime window parameters.
- Convert values from `current_setting(...)` to the target type right next to the declaration, for example `::DATE` or `::TIMESTAMP`.
- Greenplum does not support ClickHouse-style scalar `WITH` declarations. Wrap runtime settings in a one-row CTE such as `params AS (SELECT ...)`.
- Keep the params CTE compact when it stays readable.
- Do not copy ClickHouse `getSetting(...)` patterns into Greenplum queries.
- The params CTE pattern is preferred for mart, DAG, and runtime-parameterized SQL. For standalone smoke/ad-hoc SQL with a fixed chosen period, route `EXPLAIN` through the selected access owner when live access is needed and available: if params prevent static partition pruning, use explicit literals or another shape that preserves pruning.

Preferred params pattern:

```sql
WITH
   params AS (
        SELECT
              current_setting('etl.dt_from')::DATE AS report_dt_from
            , current_setting('etl.dt_to')::DATE   AS report_dt_to
)
SELECT
      source.dt               AS dt
    , source.client_id        AS client_id
FROM some_table source
CROSS JOIN params
WHERE 1 = 1
  AND source.dt >= params.report_dt_from
  AND source.dt <  params.report_dt_to
```

Minimal reusable pattern:

```sql
WITH
   params AS (
        SELECT
              current_setting('etl.dt_from')::DATE AS report_dt_from
            , current_setting('etl.dt_to')::DATE   AS report_dt_to
)
SELECT
      params.report_dt_from AS report_dt_from
    , params.report_dt_to   AS report_dt_to
FROM params
```

Preferred mixed pattern:

```sql
WITH
   params AS (
        SELECT
              current_setting('etl.dt_from')::DATE AS report_dt_from
            , current_setting('etl.dt_to')::DATE   AS report_dt_to
), orders AS (
        SELECT
              source.order_id     AS order_id
            , source.client_id    AS client_id
            , source.dt           AS dt
        FROM some_orders source
        CROSS JOIN params
        WHERE 1 = 1
          AND source.dt >= params.report_dt_from
          AND source.dt <  params.report_dt_to
), revenue AS (
        SELECT
              source.order_id     AS order_id
            , sum(source.amount)  AS revenue
        FROM some_payments source
        CROSS JOIN params
        WHERE 1 = 1
          AND source.dt >= params.report_dt_from
          AND source.dt <  params.report_dt_to
        GROUP BY source.order_id
)
SELECT
      orders.client_id            AS client_id
    , sum(revenue.revenue)        AS revenue
FROM orders
LEFT JOIN revenue ON orders.order_id = revenue.order_id
GROUP BY orders.client_id
```

For standalone validation with fixed dates, literal partition predicates are acceptable when they produce a better plan than a params CTE.

## Think in Greenplum, not generic PostgreSQL

- Reason not only about SQL text but also about segment execution, `Motion`, distribution, partition pruning, and skew.
- When changing DDL, treat `DISTRIBUTED BY` as part of query performance, not just as a storage attribute.
- Do not change `DISTRIBUTED BY` casually without understanding join keys, skew, and downstream behavior.
- Keep SQL compact by default. Expand expressions only when extra vertical structure adds real readability or makes MPP behavior easier to reason about.
- Prefer compact everyday patterns for null-handling, runtime casts, and technical keys when the one-line form remains readable.

## Distribution and small tables

- If join keys of large tables are not distribution-compatible, expect extra `Motion`.
- For truly small lookup tables, consider `DISTRIBUTED REPLICATED` when it matches the local pattern and reduces join cost.

## Loading from ClickHouse

- For Greenplum mart or ODS scripts physically loaded from ClickHouse, first consider the existing project pattern through `public.insert_from_clickhouse(...)`.
- If such a pipeline already exists, preserve its step structure unless there is a strong reason to change it.

Preferred flow:

- `CREATE TEMP TABLE ...`
- load raw data into temp via `public.insert_from_clickhouse(...)`
- build final temp or increment
- `DELETE` / `INSERT` into the target table
- `COMMIT`
- `VACUUM` if it is already part of the existing pattern
