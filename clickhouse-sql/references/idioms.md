# Idioms

Use this file when the task is about ClickHouse-native query writing rather than only formatting.

## Navigation

- [Compatibility mindset](#compatibility-mindset)
- [Native ClickHouse thinking](#think-in-clickhouse-not-generic-sql)
- [Runtime settings](#runtime-settings-in-marts)
- [Native expression patterns](#native-expression-patterns)
- [Latest-row, ASOF, array, and dictionary patterns](#argmax--argmin-before-windows)

## Compatibility mindset

- Treat the working ClickHouse contour as compatible with `25.3.6.56` until proven otherwise.
- If there is doubt about a function, a `JOIN` form, `SETTINGS`, `FINAL`, or another ClickHouse-specific feature, verify it by actual execution before relying on it.
- Prefer confirmed local project patterns over generic knowledge from other databases.
- Do not automatically transfer habits from Greenplum or Postgres into ClickHouse.

## Think in ClickHouse, not generic SQL

- Reason not only about SQL text but also about engine behavior, `ORDER BY`, `PARTITION BY`, deduplication, and dictionaries.
- When changing ClickHouse DDL, check that the change does not break the meaning of `ENGINE`, `ORDER BY`, `PARTITION BY`, `sign`, `ver`, or other engine fields.
- For `VersionedCollapsingMergeTree`, `CollapsingMergeTree`, `ReplacingMergeTree`, and similar engines, do not change incremental or deduplication logic without checking reader queries and actual results.

## Runtime settings in marts

- In ClickHouse marts, prefer `getSetting(...)` when that is the local pattern.
- Do not copy `current_setting(...)` from Greenplum or Postgres into ClickHouse marts.
- If a runtime window is passed through settings, convert it to the target type next to the declaration, for example `toDate(getSetting(...))`.
- Declare values from `getSetting(...)` once in `WITH` and reuse them by aliases instead of repeating the call throughout the query.
- For scalar `WITH` declarations, prefer `expression AS alias`.

Preferred pattern:

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

Preferred mixed pattern:

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

## Native expression patterns

- Before finalizing non-trivial SQL, run the native-shape pass from `native_shape.md`; ClickHouse-native constructs should be selected by business intent, not added only during explicit optimization tasks.
- Reusing aliases inside the same `SELECT` is acceptable when ClickHouse supports it and the project already uses this pattern.
- Prefer `toLowCardinality(...)` for fields that are naturally low-cardinality and are already modeled that way in the project.
- Use explicit ClickHouse join semantics when they match the task. `LEFT ANY JOIN`, `LEFT SEMI JOIN`, and `LEFT ANTI JOIN` should be written in full.

Example of allowed alias reuse:

```sql
SELECT
      source.dt                         AS dt
    , toLowCardinality(source.channel)  AS channel
    , toLowCardinality(source.platform) AS platform
    , cityHash64(dt, channel, platform) AS row_id
FROM some_table source
```

## `argMax` / `argMin` before windows

- For tasks like "take the latest", "take the first", or "take the value with the max flag inside a group", first consider `argMax` or `argMin` instead of a window function.
- If deterministic tie-break behavior matters, specify it explicitly, for example through `Tuple(...)`.
- If the problem can be expressed as aggregation instead of a window without losing meaning, prefer the simpler aggregate-based approach.

## `ASOF JOIN` for latest-at-time enrichment

- `ASOF JOIN` is appropriate for "last known row at event time" only after the right side is sorted and deterministic at the join grain.
- Before using `ASOF JOIN`, check whether the right side has duplicate `(equality keys, as-of timestamp)` rows.
- If duplicates exist, reduce them first with a stable id, for example `argMax(value, stable_id)` within `(key, asof_ts)`, or choose values with `argMax(value, tuple(asof_ts, stable_id))` when aggregation by event grain is clearer.
- Do not rely on `ORDER BY key, asof_ts` to pick a meaningful row among equal timestamps.

## Array patterns before windows

- If the task is not about one value per group but about a sequence inside a group, consider array-based patterns before window functions.
- Useful building blocks include `groupArray`, `arraySort`, `arrayReverseSort`, `arrayMap`, `arrayFilter`, `arrayEnumerate`, and `arrayZip`.
- Array patterns are especially useful when you need ordered history, neighboring elements, state transitions, or short sequence post-processing inside a grouped result.
- If the array solution turns into an unreadable chain of `array*` functions, stop and reassess whether the window function is actually clearer.

Use this rule of thumb:

- One value per group: first consider `argMax` / `argMin`.
- Sequence logic inside a group: first consider an array pattern.
- True row-level window semantics without natural collapse into a group: a window function is acceptable.

## Dictionaries before lookup joins

- For lookup enrichment by dictionary key, first consider `dictGet(...)` if the dictionary already exists and covers the required fields.
- If `dictGet(...)` is used for several attributes or followed by business rules, fetch the raw dictionary values in `WITH` and build final business fields in `SELECT`.
- For dictionary-based enrichment, prefer the flow `raw lookup in WITH -> business mapping in SELECT`.
- `LEFT ANY JOIN` to a lookup table should be used instead of `dictGet(...)` only when there is no ready dictionary, the lookup is not by dictionary key, or a more complex key/logic is required.

Preferred pattern:

```sql
WITH
   normalizeGeoCode(source.geo_code)                                                  AS normalized_geo_code
 , nullIf(dictGet('dicts.dim_common__gity', 'gity_name', normalized_geo_code), '')    AS dict_gity_name
 , nullIf(dictGet('dicts.dim_common__gity', 'country_name', normalized_geo_code), '') AS dict_country_name
 , nullIf(dictGet('dicts.dim_common__gity', 'gity_type', normalized_geo_code), '')    AS dict_gity_type
SELECT
      toLowCardinality(multiIf(normalized_geo_code IN ('ru', 'russia', 'by', 'kz', 'ua'),
                                'None',
                                coalesce(dict_gity_name, 'None')))  AS campaign_city
    , toLowCardinality(coalesce(dict_country_name, 'None'))         AS campaign_country
    , toLowCardinality(coalesce(dict_gity_type, 'None'))            AS campaign_geo_macro
FROM some_table source
```
