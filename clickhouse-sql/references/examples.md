# Examples

Short examples that define the preferred ClickHouse style and idioms.

## Grouped aggregate

```sql
SELECT
      source.dt               AS dt
    , source.client_id        AS client_id
    , sum(source.revenue)     AS revenue
    , count(source.order_id)  AS n_order
FROM some_table source
WHERE 1 = 1
  AND source.dt >= toDate('2026-01-01')
  AND source.dt <  toDate('2026-02-01')
GROUP BY source.dt
       , source.client_id
```

## `WITH` / CTE formatting

```sql
WITH
   orders AS (
        SELECT
              source.order_id     AS order_id
            , source.client_id    AS client_id
        FROM some_orders source
), revenue AS (
        SELECT
              source.order_id     AS order_id
            , sum(source.amount)  AS revenue
        FROM some_payments source
        GROUP BY source.order_id
)
SELECT
      orders.client_id            AS client_id
    , sum(revenue.revenue)        AS revenue
FROM orders
LEFT JOIN revenue ON orders.order_id = revenue.order_id
GROUP BY orders.client_id
```

## Mixed `WITH`: scalar plus subquery CTEs

```sql
WITH
   toDate(getSetting('custom_dt_from')) AS report_dt_from
 , toDate(getSetting('custom_dt_to'))   AS report_dt_to
 , orders AS (
        SELECT
              source.order_id     AS order_id
            , source.client_id    AS client_id
            , source.dt           AS dt
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
      orders.client_id            AS client_id
    , sum(revenue.revenue)        AS revenue
FROM orders
LEFT JOIN revenue ON orders.order_id = revenue.order_id
GROUP BY orders.client_id
```

## Short `JOIN`

```sql
FROM some_table source
LEFT JOIN other_table other ON source.client_id = other.client_id
WHERE 1 = 1
  AND source.dt >= toDate('2026-01-01')
```

## Multiline `JOIN`

```sql
FROM some_table source
LEFT JOIN other_table other ON source.client_id = other.client_id
                           AND source.dt = other.dt
LEFT JOIN third_table third ON other.geo_code = third.geo_code
                           AND other.country = third.country
WHERE 1 = 1
  AND source.dt >= toDate('2026-01-01')
  AND source.dt <  toDate('2026-02-01')
HAVING count() > 0
```

## Mixed `JOIN` and `LEFT JOIN` alignment

```sql
FROM orders_base
JOIN offers_base        ON orders_base.order_id = offers_base.order_id
                       AND offers_base.offer_status <> 'deleted'
LEFT JOIN payments_base ON offers_base.offer_id = payments_base.offer_id
```

## Explicit `GROUP BY`

```sql
GROUP BY source.dt
       , source.client_id
       , source.channel
```

## Compact expression

```sql
SELECT
      toLowCardinality(coalesce(nullIf(source.city, ''), 'None')) AS city
    , cityHash64(source.dt, source.client_id, source.channel)     AS row_id
FROM some_table source
```

## Compact array pattern

```sql
SELECT
      arrayFilter(x -> x NOT IN ('ru', 'russia', 'bel', 'kz'),
                  arrayMap(x -> x IN ('moscow', 'mos') ? 'msk' : x,
                           arrayIntersect(arr_sp, arr_def_geo_code))) AS arr_geo
FROM some_table source
```

## Native latest-row aggregate before window

```sql
SELECT
      source.client_id                                            AS client_id
    , argMax(source.status, tuple(source.updated_at, source.id))  AS last_status
    , max(source.updated_at)                                      AS last_status_at
FROM client_status source
GROUP BY source.client_id
```

## Deterministic `ASOF JOIN`

Before this shape, check duplicate rows in `pricing_raw` by `(order_id, order_pricer_ts)`. If duplicates exist, reduce them with a stable id before the `ASOF JOIN`.

```sql
WITH
   relevant_orders AS (
        SELECT
              orders.order_id AS order_id
        FROM orders
        GROUP BY orders.order_id
), pricing AS (
        SELECT
              source.order_id                                      AS order_id
            , source.order_pricer_ts                               AS order_pricer_ts
            , argMax(source.order_pricing_value,
                     source.order_pricing_id)                      AS order_pricing_value
            , argMax(source.wprice, source.order_pricing_id)        AS wprice
        FROM pricing_raw source
        LEFT SEMI JOIN relevant_orders USING (order_id)
        WHERE 1 = 1
          AND source.order_pricer_ts >= toDateTime('2026-01-01 00:00:00')
          AND source.order_pricer_ts <  toDateTime('2026-02-01 00:00:00')
        GROUP BY source.order_id
               , source.order_pricer_ts
        ORDER BY source.order_id
               , source.order_pricer_ts
)
SELECT
      orders.order_id             AS order_id
    , orders.received_ts          AS received_ts
    , pricing.order_pricer_ts     AS order_pricer_ts
    , pricing.order_pricing_value AS order_pricing_value
    , pricing.wprice              AS wprice
FROM orders
ASOF LEFT JOIN pricing ON orders.order_id = pricing.order_id
                      AND orders.received_ts >= pricing.order_pricer_ts
```

## Native existence filter before `IN (SELECT ...)`

```sql
SELECT
      orders.order_id  AS order_id
    , orders.client_id AS client_id
FROM orders
LEFT SEMI JOIN active_clients ON orders.client_id = active_clients.client_id
WHERE 1 = 1
  AND orders.dt >= toDate('2026-01-01')
```

`LEFT SEMI JOIN` can project right-side columns in ClickHouse, so this is syntactically possible:

```sql
SELECT
      orders.order_id       AS order_id
    , active_clients.status AS client_status
FROM orders
LEFT SEMI JOIN active_clients ON orders.client_id = active_clients.client_id
```

Use that only after checking that `active_clients` is unique or deterministic at `client_id`. For lookup-style enrichment with possible duplicates, prefer a deterministic reduce plus `LEFT ANY JOIN`.

## Native lookup join before ordinary `LEFT JOIN`

```sql
SELECT
      orders.order_id     AS order_id
    , orders.client_id    AS client_id
    , clients.client_name AS client_name
FROM orders
LEFT ANY JOIN dim_client clients ON orders.client_id = clients.client_id
```

## Reusable runtime settings in `WITH`

```sql
WITH
   toDate(getSetting('custom_dt_from')) AS report_dt_from
 , toDate(getSetting('custom_dt_to'))   AS report_dt_to
SELECT
      source.dt                         AS dt
    , source.client_id                  AS client_id
FROM some_table source
WHERE 1 = 1
  AND source.dt >= report_dt_from
  AND source.dt <  report_dt_to
```

## Dictionary enrichment

```sql
WITH
   normalizeGeoCode(source.geo_code)                                                  AS normalized_geo_code
 , nullIf(dictGet('dicts.dim_common__gity', 'gity_name', normalized_geo_code), '')    AS dict_gity_name
 , nullIf(dictGet('dicts.dim_common__gity', 'country_name', normalized_geo_code), '') AS dict_country_name
 , nullIf(dictGet('dicts.dim_common__gity', 'gity_type', normalized_geo_code), '')    AS dict_gity_type
SELECT
      toLowCardinality(multiIf(normalized_geo_code IN ('ru', 'russia', 'by', 'kz', 'ua'),
                               'None',
                               coalesce(dict_gity_name, 'None'))) AS campaign_city
    , toLowCardinality(coalesce(dict_country_name, 'None'))       AS campaign_country
    , toLowCardinality(coalesce(dict_gity_type, 'None'))          AS campaign_geo_macro
FROM some_table source
```

## Expanded long expressions with aligned `AS`

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
    , multiIf(
          ifNull(source.paid_amount, 0.) = 0.
        , 'no_payment'
        , ifNull(source.paid_amount, 0.) < source.order_amount * 0.5
        , 'partial_payment'
        , ifNull(source.paid_amount, 0.) >= source.order_amount
        , 'full_payment'
        , 'other'
      )                                  AS payment_bucket
FROM some_table source
```

## Do not keep one long expression single-line at the cost of huge padding

```sql
SELECT
      source.shop_id                     AS shop_id
    , toLowCardinality(
          coalesce(
              nullIf(dictGet('dicts.dim_shop', 'shop_name', toUInt64(source.shop_id)), '')
            , 'Unknown shop'
          )
      )                                  AS shop_name
    , cityHash64(source.order_id, shop_id) AS row_id
FROM some_table source
```

## Alias reuse inside one `SELECT`

```sql
SELECT
      source.dt                         AS dt
    , toLowCardinality(source.channel)  AS channel
    , toLowCardinality(source.platform) AS platform
    , cityHash64(dt, channel, platform) AS row_id
FROM some_table source
```

## ClickHouse `CREATE TABLE`

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

## ClickHouse multi-column comment alteration

```sql
ALTER TABLE mart.some_metrics
    COMMENT COLUMN report_dt 'Business report date'
  , COMMENT COLUMN client_id 'Client identifier'
  , COMMENT COLUMN revenue   'Revenue in source currency'
  , COMMENT COLUMN row_id    'Technical row identifier'
;
```
