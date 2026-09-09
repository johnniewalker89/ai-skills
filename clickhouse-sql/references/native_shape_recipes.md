# Native Shape Code Examples

Optional examples only. Apply all mandatory checks in `native_shape.md` first;
these examples do not add independent requirements or override its exceptions.

## Navigation

- [Latest row per group: example 1](#example-1)
- [Latest row per group: example 2](#example-2)
- [Latest row per group: example 3](#example-3)
- [Key-filter large lookup and reference checks: example 4](#example-4)
- [Key-filter large lookup and reference checks: example 5](#example-5)
- [Existence filtering: example 6](#example-6)
- [Existence filtering: example 7](#example-7)
- [Absence filtering: example 8](#example-8)
- [Lookup enrichment: example 9](#example-9)
- [Lookup enrichment: example 10](#example-10)
- [Sequence logic: example 11](#example-11)

## Example 1

Latest row per group — Prefer:

```sql
SELECT
      source.client_id                         AS client_id
    , argMax(source.status, source.updated_at) AS last_status
FROM client_status source
GROUP BY source.client_id
```


## Example 2

Latest row per group — Challenge:

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


## Example 3

Latest row per group — If tie behavior matters, express it explicitly:

```sql
argMax(source.status, tuple(source.updated_at, source.event_id)) AS last_status
```


## Example 4

Key-filter large lookup and reference checks — Prefer:

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


## Example 5

Key-filter large lookup and reference checks — Shared pointer-id set.

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


## Example 6

Existence filtering — Prefer `LEFT SEMI JOIN` when the right side is used only to keep matching left rows:

```sql
SELECT
      orders.order_id  AS order_id
    , orders.client_id AS client_id
FROM orders
LEFT SEMI JOIN active_clients ON orders.client_id = active_clients.client_id
```


## Example 7

Existence filtering — Challenge:

```sql
WHERE orders.client_id IN (
    SELECT client_id
    FROM active_clients
)
```


## Example 8

Absence filtering — Prefer `LEFT ANTI JOIN` when the right side is used only to remove matching left rows:

```sql
SELECT
      orders.order_id  AS order_id
    , orders.client_id AS client_id
FROM orders
LEFT ANTI JOIN blocked_clients ON orders.client_id = blocked_clients.client_id
```


## Example 9

Lookup enrichment — Table lookup with LEFT ANY JOIN.

```sql
SELECT
      orders.order_id     AS order_id
    , orders.client_id    AS client_id
    , clients.client_name AS client_name
FROM orders
LEFT ANY JOIN dim_client clients ON orders.client_id = clients.client_id
```


## Example 10

Lookup enrichment — Explicit match flag for matched/unmatched metrics.

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


## Example 11

Sequence logic — For sequence logic inside a group, prefer an array-shaped solution before stacking windows:

```sql
SELECT
      source.client_id                                            AS client_id
    , arrayMap(x -> x.2,
               arraySort(x -> x.1,
                         groupArray((source.event_at, source.status)))) AS status_path
FROM client_events source
GROUP BY source.client_id
```
