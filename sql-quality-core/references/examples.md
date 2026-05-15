# SQL Quality Core Examples

Use these examples only for engine-agnostic reasoning. Apply the target engine skill for final syntax, functions, and plan interpretation.

## Source candidate matrix

When source choice is non-obvious, compare exact-name and business-keyword candidates before writing SQL.

```md
| Candidate | Repo path | Live DB | Grain | Join keys | Freshness / shape | Decision |
|---|---|---|---|---|---|---|
| mart.some_exact_source | dbt/models/mart/some_exact_source.sql | no | event | order_id | not deployed | reject: repo-vs-DB mismatch |
| mart.some_business_source | dbt/models/mart/some_business_source.sql | yes | order | order_id | fresh | select: verified repo-backed live fit |
| mart.some_live_helper | none found | yes | order | order_id | plausible | fallback only: DB-only/artifact-risk |
```

Prefer the verified repo-backed live candidate that fits the requested grain and join keys. Use a DB-only candidate only when no repo-backed live source fits, and record the risk.

## Business-grain report

When the task is about a concrete business entity, drive the final aggregation from matched rows of that entity. Do not start from a broader source unless unmatched coverage is an explicit metric.

```sql
WITH
   matched_orders AS (
        SELECT
              orders.order_id      AS order_id
            , orders.client_id     AS client_id
            , orders.created_at    AS created_at
            , source.channel       AS channel
        FROM source_events source
        JOIN orders ON source.session_id = orders.session_id
)
SELECT
      CAST(matched_orders.created_at AS DATE) AS report_dt
    , matched_orders.channel                  AS channel
    , count(*)                                AS n_order
FROM matched_orders
GROUP BY CAST(matched_orders.created_at AS DATE)
       , matched_orders.channel
```

## Category-safe metrics

When a fact has different semantic categories, avoid one generic value metric unless the category mix is intentional and named.

```sql
SELECT
      pricing.order_id                                                        AS order_id
    , count(*)                                                                AS n_pricing_row
    , count(*) FILTER (WHERE pricing.pricing_type = 'lg')                     AS n_lg_pricing_row
    , avg(pricing.price) FILTER (WHERE pricing.pricing_type = 'lg')           AS avg_lg_price
    , count(*) FILTER (WHERE pricing.pricing_type = 'tml')                    AS n_tml_pricing_row
    , avg(pricing.price) FILTER (WHERE pricing.pricing_type = 'tml')          AS avg_tml_price
    , avg(pricing.price) FILTER (WHERE pricing.pricing_type IN ('lg', 'tml')) AS avg_lg_tml_all_types_price
FROM pricing
GROUP BY pricing.order_id
```

Before using literals such as `'lg'` or `'tml'`, check actual categories in the selected data and update metric names/constants from that check.
