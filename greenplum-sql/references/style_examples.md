# Style Examples

Read only the example needed to resolve a concrete formatting question. The required rules remain in `style.md`; these examples add no new invariant.

## Example 1

```sql
SELECT
      coalesce(nullif(source.city, ''), 'None')                                          AS city
    , md5(coalesce(source.dt::TEXT, '') || '|' || coalesce(source.client_id::TEXT, ''))  AS row_id
FROM some_table source
```

## Example 2

```sql
SELECT
      coalesce(nullif(source.country, ''), 'None') AS country
    , coalesce(nullif(source.region, ''), 'None')  AS region
FROM some_table source
```

## Example 3

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

## Example 4

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
FROM some_table source
```

## Example 5

```sql
WITH
   payments AS (
    SELECT
          source.order_id AS order_id
        , source.shop_id  AS shop_id
        , CASE
              WHEN coalesce(source.paid_amount, 0) = 0
                  THEN 'no_payment'
              WHEN coalesce(source.paid_amount, 0) < source.order_amount * 0.5
                  THEN 'partial_payment'
              WHEN coalesce(source.paid_amount, 0) >= source.order_amount
                  THEN 'full_payment'
              ELSE 'other'
          END             AS payment_bucket
    FROM some_table source
)
SELECT
      payments.payment_bucket AS payment_bucket
    , md5(
          coalesce(payments.order_id::TEXT, '')       || '|' ||
          coalesce(payments.shop_id::TEXT, '')        || '|' ||
          coalesce(payments.payment_bucket::TEXT, '')
      )                       AS row_id
FROM payments
```

## Example 6

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
