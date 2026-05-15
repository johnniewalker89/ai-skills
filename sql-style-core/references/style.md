# SQL Style

Use this file for common SQL code style and readability. Engine-specific skills may add stricter rules or exceptions.

## General Rules

- SQL keywords and logical operators should be upper-case.
- SQL functions should be lower-case when the local project style allows it.
- Data types should be upper-case.
- In multi-table queries, selected columns must have explicit sources.
- Columns inside expressions should keep explicit sources when omitting them makes lineage ambiguous.
- Column aliases must use `AS`.
- Plain columns do not need redundant aliases in simple local queries.
- In production or multi-table `SELECT`s, explicit plain-column aliases are acceptable when they define the output schema, preserve the common `AS` column, or make lineage clearer.
- Prefer ordering selected expressions from business-facing attributes to technical helper fields.

## Alignment And Compactness

- Keep one visual `AS` column across a `SELECT` block when the block remains readable.
- Do not preserve a common `AS` column by adding excessive horizontal padding to short expressions.
- Prefer compact expressions when the result is still easy to read.
- Expand an expression when compact form becomes hard to read, hides an important calculation step, breaks the common `AS` column, or creates excessive padding.
- If a multiline expression has an alias, keep `AS alias` on the final line of the full expression.

## SELECT Formatting

- Every `SELECT` expression starts on a new line.
- The first `SELECT` expression uses a `+6` space indent.
- Every next `SELECT` expression uses a `+4` space indent and starts with a leading comma.
- After the `SELECT` block, the next block usually starts without an extra blank line.
- Long boolean conditions should be aligned vertically when that improves readability.
- `UNION ALL` should be separated by a blank line above and below when that helps readability.

Preferred pattern:

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

## WITH And CTE Readability

- Use named CTEs or named expressions to explain meaningful calculation steps.
- For subquery CTEs, use `cte_name AS (...)`.
- Inside a subquery CTE, the inner query block starts with a 4-space indent from the line start.
- Do not indent nested `SELECT`, `FROM`, `WHERE`, or `GROUP BY` by 8 spaces just because they are inside a CTE.
- In a subquery CTE chain, the next CTE starts as `), next_cte AS (` on the same line where the previous CTE closes.
- Do not assign an extra alias to a CTE when referencing it in `FROM` or `JOIN`.
- Table aliases in `FROM` / `JOIN` should be written without `AS`.
- Prefer short meaningful table aliases from project patterns.

Preferred subquery CTE pattern:

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

## JOIN, WHERE, HAVING, GROUP BY

- Prefer `JOIN` over `INNER JOIN` when ordinary inner-join semantics are intended and no extra emphasis is needed.
- The first `ON` must stay on the same physical line as its `JOIN`.
- Never move the first `ON` to the next line, even for multiline join conditions.
- For multiline join conditions, put the first condition after `ON` on the `JOIN` line and put later conditions on following lines starting with `AND`.
- In a chain of adjacent `JOIN`s, align the `ON` keyword to the same visual column only when each `ON` still stays on its own `JOIN` line.
- Align continuation `AND` conditions under the join condition, not by moving `ON` to a separate line.
- In multiline `WHERE`, each next condition starts on a new line with `AND`.
- In multiline `HAVING`, each next condition starts on a new line with `AND`.
- `WHERE 1 = 1` and `HAVING` are acceptable when the filter block is multiline or likely to grow.
- For a short one-condition filter, direct `WHERE` without `1 = 1` is acceptable.
- For date and datetime windows, prefer half-open ranges: lower bound with `>=`, upper bound with `<`.
- In window filters, right-hand side values should be visually aligned when that stays readable.
- `GROUP BY` should explicitly repeat grouped columns instead of using positions.
- In multiline `GROUP BY`, each next grouped expression starts on a new line in comma-leading style.

Preferred aligned join chain:

```sql
FROM orders
LEFT JOIN payments    ON orders.order_id = payments.order_id
LEFT JOIN order_items ON orders.order_id = order_items.order_id
LEFT JOIN refunds     ON orders.order_id = refunds.order_id
```

Preferred multiline join condition:

```sql
FROM board_opens
LEFT JOIN board_events_by_project ON board_opens.board_search_id = board_events_by_project.board_search_id
                                 AND board_opens.prep_id = board_events_by_project.prep_id
```

## Multiline Expressions

- If an expression spans multiple lines, keep continuation lines structurally indented by nesting level.
- For multiline `CASE` expressions, keep `AS alias` on the final line of the full expression.
- Expand long calculation expressions when naming intermediate steps would make the business meaning easier to audit.

Example:

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
