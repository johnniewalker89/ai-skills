# Examples

Short examples that define the preferred Greenplum style and idioms.

## Navigation

- [Aggregates and CTEs](#grouped-aggregate)
- [JOIN layouts](#short-join)
- [Filtering and expression layout](#heavy-enrichment-key-filter)
- [Runtime parameters and staging](#compact-runtime-settings-in-params-cte)
- [Greenplum DDL](#greenplum-create-table)

## Grouped aggregate

```sql
SELECT
      source.dt               AS dt
    , source.client_id        AS client_id
    , sum(source.revenue)     AS revenue
    , count(source.order_id)  AS n_order
FROM some_table source
WHERE 1 = 1
  AND source.dt >= DATE '2026-01-01'
  AND source.dt <  DATE '2026-02-01'
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

## `WITH` with params CTE plus subquery CTEs

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

## Short `JOIN`

```sql
FROM some_table source
LEFT JOIN other_table other ON source.client_id = other.client_id
WHERE 1 = 1
  AND source.dt >= DATE '2026-01-01'
```

## Multiline `JOIN`

```sql
FROM some_table source
LEFT JOIN other_table other ON source.client_id = other.client_id
                           AND source.dt = other.dt
LEFT JOIN third_table third ON other.geo_code = third.geo_code
                           AND other.country = third.country
WHERE 1 = 1
  AND source.dt >= DATE '2026-01-01'
  AND source.dt <  DATE '2026-02-01'
HAVING count(*) > 0
```

## Aligned `JOIN ... ON ...` chain

```sql
FROM orders
LEFT JOIN payments    ON orders.order_id = payments.order_id
LEFT JOIN order_items ON orders.order_id = order_items.order_id
LEFT JOIN refunds     ON orders.order_id = refunds.order_id
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

## Heavy enrichment key filter

When a narrow driving set exists, restrict heavy enrichment tables by relevant keys before expensive aggregation or joins.

```sql
WITH
   relevant_orders AS (
        SELECT
              orders.order_id AS order_id
        FROM orders
        GROUP BY orders.order_id
), pricing_ranked AS (
        SELECT
              source.order_id           AS order_id
            , source.pricing_ts         AS pricing_ts
            , source.price              AS price
            , row_number() OVER (
                  PARTITION BY source.order_id
                  ORDER BY source.pricing_ts DESC
                         , source.pricing_id DESC
              )                         AS rn
        FROM order_pricing source
        JOIN relevant_orders ON source.order_id = relevant_orders.order_id
), pricing AS (
        SELECT
              pricing_ranked.order_id   AS order_id
            , pricing_ranked.pricing_ts AS last_pricing_ts
            , pricing_ranked.price      AS price
        FROM pricing_ranked
        WHERE pricing_ranked.rn = 1
)
SELECT
      orders.order_id AS order_id
    , pricing.price   AS price
FROM orders
LEFT JOIN pricing ON orders.order_id = pricing.order_id
```

## Compact expression

```sql
SELECT
      coalesce(nullif(source.city, ''), 'None')                                         AS city
    , md5(coalesce(source.dt::TEXT, '') || '|' || coalesce(source.client_id::TEXT, '')) AS row_id
FROM some_table source
```

## Compact null-handling

```sql
SELECT
      coalesce(nullif(source.country, ''), 'None') AS country
    , coalesce(nullif(source.region, ''), 'None')  AS region
    , coalesce(nullif(source.city, ''), 'None')    AS city
FROM some_table source
```

## Compact `CASE`

```sql
SELECT
      CASE WHEN source.amount > 0 THEN source.amount ELSE 0 END AS amount_positive
    , CASE WHEN source.is_vip = 1 THEN 'vip' ELSE 'regular' END AS client_segment
FROM some_table source
```

## Expanded long expressions with aligned `AS`

```sql
SELECT
      coalesce(
          nullif(source.shop_name, '')
        , 'Unknown shop'
      )                                  AS shop_name
    , coalesce(
          nullif(source.shop_city, '')
        , 'Unknown city'
      )                                  AS shop_city
    , CASE
          WHEN coalesce(source.paid_amount, 0) = 0
              THEN 'no_payment'
          WHEN coalesce(source.paid_amount, 0) < source.order_amount * 0.5
              THEN 'partial_payment'
          WHEN coalesce(source.paid_amount, 0) >= source.order_amount
              THEN 'full_payment'
          ELSE 'other'
      END                                AS payment_bucket
FROM some_table source
```

## Do not keep one long expression single-line at the cost of huge padding

```sql
SELECT
      source.shop_id                     AS shop_id
    , coalesce(
          nullif(source.shop_name, '')
        , 'Unknown shop'
      )                                  AS shop_name
    , md5(
          coalesce(source.order_id::TEXT, '') || '|' ||
          source.shop_id::TEXT
      )                                  AS row_id
FROM some_table source
```

## Compact `greatest` / `least`

```sql
SELECT
      greatest(source.dt, coalesce(source.finish_dt, source.dt)) AS finish_dt
    , least(source.finish_dt, source.deadline_dt)                AS effective_deadline
FROM some_table source
```

## Compact technical key

```sql
SELECT
      source.dt                                       AS dt
    , source.client_id                                AS client_id
    , source.channel                                  AS channel
    , md5(coalesce(source.dt::TEXT, '') || '|' || coalesce(source.client_id::TEXT, '')
        || '|' || coalesce(source.channel::TEXT, '')) AS row_id
FROM some_table source
```

## Compact runtime settings in params CTE

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

## Runtime settings via params CTE

```sql
WITH
   params AS (
        SELECT
              current_setting('etl.dt_from')::DATE AS report_dt_from
            , current_setting('etl.dt_to')::DATE   AS report_dt_to
)
SELECT
      source.dt         AS dt
    , source.client_id  AS client_id
FROM some_table source
CROSS JOIN params
WHERE 1 = 1
  AND source.dt >= params.report_dt_from
  AND source.dt <  params.report_dt_to
```

## Staging flow sketch

```sql
CREATE TEMP TABLE tmp_source_data AS
SELECT
      source.order_id   AS order_id
    , source.client_id  AS client_id
    , source.amount     AS amount
FROM some_source source
WHERE 1 = 1
  AND source.dt >= DATE '2026-01-01'
  AND source.dt <  DATE '2026-02-01'
;

DELETE FROM target_table
WHERE 1 = 1
  AND dt >= DATE '2026-01-01'
  AND dt <  DATE '2026-02-01'
;

INSERT INTO target_table
SELECT
      tmp.order_id  AS order_id
    , tmp.client_id AS client_id
    , tmp.amount    AS amount
FROM tmp_source_data tmp
;

COMMIT;
```

## Greenplum `CREATE TABLE`

```sql
CREATE TABLE sandbox.some_metrics
(
      report_dt         DATE
    , client_id         BIGINT
    , channel           TEXT
    , revenue           NUMERIC(38, 6)
    , row_id            TEXT
)
WITH (appendoptimized = true, orientation = column, compresstype = zstd, compresslevel = 1)
DISTRIBUTED BY (client_id)
;
```

## Greenplum comments

```sql
COMMENT ON TABLE sandbox.some_metrics IS 'Aggregated order metrics by client and channel';

COMMENT ON COLUMN sandbox.some_metrics.report_dt IS 'Business report date';
COMMENT ON COLUMN sandbox.some_metrics.client_id IS 'Client identifier';
COMMENT ON COLUMN sandbox.some_metrics.revenue IS 'Revenue in source currency';
COMMENT ON COLUMN sandbox.some_metrics.row_id IS 'Technical row identifier';
```
