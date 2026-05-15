# ClickHouse Style Overlay

Use this file after `sql-style-core/references/style.md`. It contains only ClickHouse-specific or local ClickHouse style rules.

## ClickHouse Expressions And Aliases

- SQL functions should be lower-case.
- Data types before and after conversions should be upper-case.
- If business attributes were already defined earlier in the same `SELECT`, they may be reused in later technical expressions such as `row_id` when the result is clearer.
- Alias reuse inside one `SELECT` is allowed only after the reused alias was defined earlier in the same `SELECT`.
- Reusing aliases inside the same `SELECT` is allowed only when this is supported by ClickHouse and already matches project patterns.
- Prefer ClickHouse-native type and null handling functions such as `toLowCardinality`, `nullIf`, `ifNull`, and `coalesce` according to existing project style.
- For hashing or technical ids, prefer existing project ClickHouse patterns such as `cityHash64(...)`.

Compact ClickHouse expressions are fine when they stay readable:

```sql
SELECT
      toLowCardinality(coalesce(nullIf(source.city, ''), 'None')) AS city
    , cityHash64(source.dt, source.client_id, source.channel)     AS row_id
FROM some_table source
```

Compact nested array expressions are also acceptable when they remain auditable:

```sql
SELECT
      arrayFilter(x -> x NOT IN ('ru', 'russia', 'bel', 'kz'),
                  arrayMap(x -> x IN ('moscow', 'mos') ? 'msk' : x,
                           arrayIntersect(arr_sp, arr_def_geo_code))) AS arr_geo
FROM some_table source
```

## Scalar WITH And Mixed WITH

- ClickHouse scalar `WITH` declarations use `expression AS alias`, not `alias AS expression`.
- In a scalar `WITH` chain, every next element starts on a new line with a leading comma and a `+1` space indent.
- In scalar `WITH` declarations, `AS` should align to one tab stop to the right of the longest expression in the block when readable.
- Declare values from `getSetting(...)` once in `WITH` and reuse them by aliases instead of repeating calls.
- In a mixed `WITH`, declare scalar values first and subquery CTEs after them.
- In a mixed `WITH`, the scalar section follows scalar-chain rules first, then the subquery CTE section follows common subquery-chain rules.
- In a mixed `WITH`, the first subquery CTE starts on a new line with a leading comma after the scalar declarations.
- After the first subquery CTE in a mixed `WITH`, each next subquery CTE starts as `), next_cte AS (` on the same line where the previous CTE closes.
- In a mixed `WITH`, scalar aliases may be reused inside subquery CTEs that appear later in the same `WITH` chain.
- Prefer keeping scalar `WITH` expressions on one line when they remain readable.
- If a scalar `WITH` expression becomes too long or materially hurts readability, it is acceptable to expand it across multiple lines and keep the alias aligned on the closing line.

Preferred scalar `WITH` pattern:

```sql
WITH
   toDate(getSetting('custom_dt_from')) AS report_dt_from
 , toDate(getSetting('custom_dt_to'))   AS report_dt_to
SELECT
      source.dt         AS dt
    , source.client_id  AS client_id
FROM some_table source
WHERE 1 = 1
  AND source.dt >= report_dt_from
  AND source.dt <  report_dt_to
```

Allowed multiline scalar `WITH` pattern:

```sql
WITH
   toLowCardinality(coalesce(nullIf(source.city, ''), 'None'))      AS city_normalized
 , arrayFilter(x -> x NOT IN ('ru', 'russia', 'bel', 'kz'),
               arrayMap(x -> x IN ('moscow', 'mos') ? 'msk' : x,
                        arrayIntersect(arr_sp, arr_def_geo_code)))  AS arr_geo
SELECT
      city_normalized AS city_normalized
    , arr_geo         AS arr_geo
FROM some_table source
```

Preferred mixed `WITH` pattern:

```sql
WITH
   toDate(getSetting('custom_dt_from')) AS report_dt_from
 , toDate(getSetting('custom_dt_to'))   AS report_dt_to
 , orders AS (
    SELECT
          source.order_id   AS order_id
        , source.client_id  AS client_id
        , source.dt         AS dt
    FROM some_orders source
    WHERE 1 = 1
      AND source.dt >= report_dt_from
      AND source.dt <  report_dt_to
), revenue AS (
    SELECT
          source.order_id     AS order_id
        , sum(source.amount)  AS revenue
    FROM some_payments source
    WHERE 1 = 1
      AND source.dt >= report_dt_from
      AND source.dt <  report_dt_to
    GROUP BY source.order_id
)
SELECT
      orders.client_id      AS client_id
    , sum(revenue.revenue)  AS revenue
FROM orders
LEFT JOIN revenue ON orders.order_id = revenue.order_id
GROUP BY orders.client_id
```

## ClickHouse Multiline Expressions

- For multiline `multiIf(...)`, put conditions and branch values on separate lines when needed.
- Keep the closing `)` with `AS alias` on the final line of the full expression.
- For dictionary reads, expand nested `dictGet` / `toLowCardinality` / null handling when compact form hides the business fallback.

Preferred expanded dictionary expression:

```sql
SELECT
      toLowCardinality(
          coalesce(
              nullIf(dictGet('dicts.dim_shop', 'shop_name', toUInt64(source.shop_id)), '')
            , 'Unknown shop'
          )
      )                                  AS shop_name
    , toLowCardinality(
          coalesce(
              nullIf(dictGet('dicts.dim_shop', 'city_name', toUInt64(source.shop_id)), '')
            , 'Unknown city'
          )
      )                                  AS shop_city
FROM some_table source
```

Preferred expanded `multiIf(...)`:

```sql
SELECT
      multiIf(
          ifNull(source.paid_amount, 0.) = 0.
        , 'no_payment'
        , ifNull(source.paid_amount, 0.) < source.order_amount * 0.5
        , 'partial_payment'
        , ifNull(source.paid_amount, 0.) >= source.order_amount
        , 'full_payment'
        , 'other'
      )                                  AS payment_bucket
    , cityHash64(source.order_id, payment_bucket) AS row_id
FROM some_table source
```

## ClickHouse DDL Formatting

- Data types in ClickHouse DDL should follow the project type naming pattern and stay visually consistent inside one block.
- In `CREATE TABLE`, each column definition must start on a new line.
- In column lists for `CREATE TABLE`, use comma-leading formatting when that is the project pattern for the target object.
- Type names and important modifiers should stay visually aligned when the block remains readable.
- Table-level clauses such as `ENGINE`, `ORDER BY`, `PARTITION BY`, and `SETTINGS` must stay explicit.
- Multi-column `ALTER TABLE` statements such as `COMMENT COLUMN` chains should use comma-leading formatting when the statement spans multiple lines.
- If the local DDL pattern keeps the closing `;` on a separate line, preserve that pattern instead of collapsing it.

Preferred `CREATE TABLE` pattern:

```sql
CREATE TABLE mart.some_metrics
(
      report_dt         Date
    , client_id         UInt64
    , channel           LowCardinality(String)
    , revenue           Decimal(38, 6)
    , row_id            UInt64
)
ENGINE = MergeTree
ORDER BY (report_dt, client_id)
PARTITION BY toYYYYMM(report_dt)
SETTINGS index_granularity = 8192
;
```

Preferred multi-column comment alteration:

```sql
ALTER TABLE mart.some_metrics
    COMMENT COLUMN report_dt 'Business report date'
  , COMMENT COLUMN client_id 'Client identifier'
  , COMMENT COLUMN revenue   'Revenue in source currency'
  , COMMENT COLUMN row_id    'Technical row identifier'
;
```
