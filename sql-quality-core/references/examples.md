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

This example counts orders per observed channel membership. `orders` must have
one row per non-NULL `order_id`; repeated events for a session/channel are reduced
to one membership before joining from orders. The intermediate grain is
`order_id` / `channel`, and the output is order date / channel.

An order observed in several channels contributes once to each. Channel totals
overlap and must not be summed as a global unique-order total. For exclusive
attribution, first establish a business-approved unique order-to-channel mapping;
do not choose an arbitrary channel or hide the ambiguity with `DISTINCT`.

A NULL channel remains a separate unknown membership. Only orders with a matching
source session are included; unmatched-order coverage needs a separate metric.

```sql
WITH
   session_channels AS (
    SELECT
          source_events.session_id AS session_id
        , source_events.channel    AS channel
    FROM source_events
    GROUP BY source_events.session_id
           , source_events.channel
), order_channels AS (
    SELECT
          orders.order_id                 AS order_id
        , CAST(orders.created_at AS DATE) AS report_dt
        , session_channels.channel        AS channel
    FROM orders
    JOIN session_channels ON orders.session_id = session_channels.session_id
)
SELECT
      order_channels.report_dt AS report_dt
    , order_channels.channel   AS channel
    , count(*)                 AS n_order_per_channel
FROM order_channels
GROUP BY order_channels.report_dt
       , order_channels.channel
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
