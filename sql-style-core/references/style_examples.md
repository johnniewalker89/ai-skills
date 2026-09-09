# Style Examples

Read only the example needed to resolve a concrete formatting question. The required rules remain in `style.md`; these examples add no new invariant.

## Example 1

```sql
SELECT
      source.dt               AS dt
    , source.client_id        AS client_id
    , sum(source.revenue)     AS revenue
    , count(source.order_id)  AS n_order
FROM some_table source
WHERE 1=1
  AND source.dt >= DATE '2026-01-01'
  AND source.dt <  DATE '2026-02-01'
GROUP BY source.dt
       , source.client_id
```

## Example 2

```sql
WITH
   orders AS (
    SELECT
          source.order_id   AS order_id
        , source.client_id  AS client_id
    FROM some_orders source
), revenue AS (
    SELECT
          source.order_id     AS order_id
        , sum(source.amount)  AS revenue
    FROM some_payments source
    GROUP BY source.order_id
)
SELECT
      orders.client_id      AS client_id
    , sum(revenue.revenue)  AS revenue
FROM orders
LEFT JOIN revenue ON orders.order_id = revenue.order_id
GROUP BY orders.client_id
```

## Example 3

```sql
FROM orders
LEFT JOIN payments    ON orders.order_id = payments.order_id
LEFT JOIN order_items ON orders.order_id = order_items.order_id
LEFT JOIN refunds     ON orders.order_id = refunds.order_id
```

## Example 4

```sql
FROM board_opens
LEFT JOIN board_events_by_project ON board_opens.board_search_id = board_events_by_project.board_search_id
                                 AND board_opens.prep_id = board_events_by_project.prep_id
```

## Example 5

```sql
SELECT
      CASE
          WHEN coalesce(source.paid_amount, 0) = 0
              THEN 'no_payment'
          WHEN coalesce(source.paid_amount, 0) < source.order_amount * 0.5
              THEN 'partial_payment'
          WHEN coalesce(source.paid_amount, 0) >= source.order_amount
              THEN 'full_payment'
          ELSE 'other'
      END AS payment_bucket
FROM some_table source
```
