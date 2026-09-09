# Style Examples

Read only the example needed to resolve a concrete formatting question. The required rules remain in `style.md`; these examples add no new invariant.

## Navigation

- [Example 1](#example-1), [2](#example-2), [3](#example-3)
- [Example 4](#example-4), [5](#example-5), [6](#example-6)
- [Example 7](#example-7), [8](#example-8), [9](#example-9)

## Example 1

```sql
SELECT
      toLowCardinality(coalesce(nullIf(source.city, ''), 'None')) AS city
    , cityHash64(source.dt, source.client_id, source.channel)     AS row_id
FROM some_table source
```

## Example 2

```sql
SELECT
      arrayFilter(x -> x NOT IN ('ru', 'russia', 'bel', 'kz'),
                  arrayMap(x -> x IN ('moscow', 'mos') ? 'msk' : x,
                           arrayIntersect(arr_sp, arr_def_geo_code))) AS arr_geo
FROM some_table source
```

## Example 3

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

## Example 4

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

## Example 5

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

## Example 6

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

## Example 7

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

## Example 8

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

## Example 9

```sql
ALTER TABLE mart.some_metrics
    COMMENT COLUMN report_dt 'Business report date'
  , COMMENT COLUMN client_id 'Client identifier'
  , COMMENT COLUMN revenue   'Revenue in source currency'
  , COMMENT COLUMN row_id    'Technical row identifier'
;
```
