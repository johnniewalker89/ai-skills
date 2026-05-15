# Greenplum Style Overlay

Use this file after `sql-style-core/references/style.md`. It contains only Greenplum-specific or local Greenplum style rules.

## Greenplum Expressions And Aliases

- SQL functions should be lower-case.
- Data types in SQL and DDL should be upper-case.
- Do not reuse a newly defined alias inside the same `SELECT` list.
- If a derived value is needed by another expression, move it into an inner CTE/subquery or repeat the expression when it is still simple.
- Use PostgreSQL/Greenplum casts consistently with existing project style, including `::DATE`, `::TEXT`, and `NUMERIC(...)` patterns.

Compact Greenplum expressions are fine when they stay readable:

```sql
SELECT
      coalesce(nullif(source.city, ''), 'None')                                          AS city
    , md5(coalesce(source.dt::TEXT, '') || '|' || coalesce(source.client_id::TEXT, ''))  AS row_id
FROM some_table source
```

Compact null handling is also acceptable:

```sql
SELECT
      coalesce(nullif(source.country, ''), 'None') AS country
    , coalesce(nullif(source.region, ''), 'None')  AS region
FROM some_table source
```

## WITH And Runtime Parameters

- Greenplum does not support ClickHouse-style scalar `WITH` declarations such as `expression AS alias` before `SELECT`.
- In Greenplum, use only subquery CTEs in `WITH`.
- When runtime parameters are needed, declare them in a one-row CTE such as `params AS (SELECT ...)`.
- Place a params CTE first in the `WITH` chain when later CTEs depend on it.
- Reuse params values through `FROM params`, `CROSS JOIN params`, or another explicit join pattern inside downstream CTEs.
- For standalone smoke/ad-hoc SQL with a fixed chosen period, verify plan pruning through `db-access` when database access is needed and available; if a params CTE prevents static partition pruning, use explicit literals or another shape that preserves pruning.

Compact runtime conversion inside a one-row params CTE:

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

## Greenplum Multiline Expressions

- For multiline function or `CASE` expressions, keep `AS alias` on the final line of the full expression.
- Expand long `coalesce` / `nullif` / `CASE` expressions when compact form hides fallback semantics.
- For md5 technical ids, keep concatenated parts auditable and source-qualified.

Preferred expanded null-handling expression:

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

Preferred expanded `CASE` with technical id:

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

## Greenplum DDL Formatting

- Before editing DDL, inspect a neighboring object of the same DB and object type when one is available in the repo.
- In Greenplum `CREATE TABLE`, each column definition must start on a new line.
- In column lists for `CREATE TABLE`, use comma-leading formatting when that is the project pattern for the target object.
- Type names and important modifiers should stay visually aligned when the block remains readable.
- `COMMENT ON TABLE` and `COMMENT ON COLUMN` should be separate statements.
- Column descriptions should stay within a single SQL statement unless multiline text is truly needed.
- Table parameters such as `WITH (...)` should stay on one line when readability is not harmed.
- Physical design clauses such as `DISTRIBUTED BY` must be explicit and intentional.

Preferred `CREATE TABLE` pattern:

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
