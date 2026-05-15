# Metrics, Windows, And Funnels

Use this reference for multi-row facts, categories, date/window semantics, sequential funnels, child-entity metrics, mutable sources, and optimization-risk classification.

## Multi-Row Facts And Categories

Treat multi-row facts as facts, not one-row lookups.

- Do not build a fake representative row with independent `min(...)` / `max(...)` over unrelated columns.
- If output needs attributes from one row, choose one whole row with a deterministic rule and a tie-break that actually distinguishes candidates.
- Do not collapse a multi-category fact with `max(type)` plus `max(value)`.
- Do not publish generic aggregates such as `avg(value)`, `max(price)`, or `sum(amount)` across semantic categories unless the category mix itself is the intended metric and the output name says so.
- Prefer category-specific metrics, an explicit category filter, or a deliberately named `*_all_types_*` / `*_all_categories_*` metric after checking actual categories.
- If an output already includes category distribution, a neighboring generic category-mixed aggregate still needs an `*_all_types_*` / `*_all_categories_*` name or should be dropped; the distribution does not make the generic metric self-explanatory.
- If category-specific metrics are used, cover every material category found in the chosen window, or include explicit `other_*` / `unknown_*` metrics.
- Apply the same rule to category-dependent attributes; shared attributes are safe only after checking they are invariant across categories.

## Date Windows And Filters

Date predicates are metric semantics, not only performance filters.

- Decide whether a right-side fact window means same-day activity, first-N-day lifecycle, all activity for selected keys, current/latest state, or another business concept.
- For first-N-day or lifecycle metrics, apply both bounds in every affected metric: `fact_ts >= event_ts` and `fact_ts < event_ts + interval`.
- Reflect intentional windows in metric names such as `same_day_*`, `*_30d`, `*_asof_*`, or `*_all_history`.
- Separate bounded smoke coverage/category checks from intentional all-history pointer/reference checks.
- An all-history pointer/reference branch must not be the only coverage/category metric for a smoke task. If bounded coverage is skipped, the output and notes must say it is not a bounded smoke coverage check, name it `*_all_history`, and record the business reason plus row/partition cost.
- Do not silently drop a small tail of business keys for performance in money, audit, reconciliation, contractual, or other accuracy-critical reports.
- For smoke/basic analytics, a bounded scan plus explicit missing/outside-window metric can be acceptable when the tail is immaterial.
- If a full-history scan is considered, compare gained business-key coverage with added rows/partitions or plan cost.

If validation or performance uses a proxy timestamp different from the business timestamp:

- name both timestamps and the intended business window;
- prove that the proxy window covers every row that can belong to the business window, or expose outside-proxy counts/missing metrics;
- otherwise downgrade the proof claim to the proxy/guarded surface and block full business-window readiness;
- do not let engine-specific partition pruning evidence replace business-window coverage evidence.

For concrete filters and literals:

- check actual values for enum-like filters and metric literals;
- update final SQL constants and metric names when actual values differ from the draft;
- do not leave enum/date discoveries only in notes if they affect final SQL.

For duration and time-to-stage metrics:

- subtract from the actual lifecycle start timestamp, such as `received_ts`, `created_at`, `event_ts`, or `zayavka_ts`;
- do not subtract from a truncated bucket such as `dt`, `report_dt`, `toDate(...)`, or `date_trunc(...)` unless the metric is explicitly bucket-relative and named that way;
- apply lower-bound sanity where needed so negative durations do not silently enter averages.

## Sequential Funnels And Entity Metrics

When a requested metric is a funnel, lifecycle, or "reached step" chain, model each step as occurring after the previous step for the same declared entity grain.

- Do not compute independent `minIf(...)` timestamps for every step and only compare them at the end when later valid events may exist after an earlier invalid event.
- For each step, derive the next step from events constrained by the previous accepted step timestamp, or prove independent first timestamps are equivalent for the source.
- The chain grain must be explicit: session, user, board search, order, payment, or another entity. Join and aggregation keys must preserve that grain.
- If the business says "view -> click -> response", a response before the accepted click does not count, but a later response after the accepted click can count.
- If the funnel can happen for multiple child entities inside the parent grain, decide whether metrics are parent-level flags, child-entity counts, event counts, or first-child metrics.
- Metric names must match that decision. Names such as `n_orders_viewed`, `n_orders_clicked`, or `n_orders_responded` imply all qualifying child entities. If only the first child is counted, name it `n_first_*`.
- For project/category attribution in a multi-child parent, state whether attribution is first child, all child entities, fractional, primary category, or unknown. Do not silently collapse mixed-category parents into the first child unless that is the approved business rule.

For build-from-scratch marts, this is a release-quality gate. If a final artifact has a sequential funnel or child-entity metric and this check has not passed, do not report SQL-quality-check passed and do not move to sandbox validation.

## Mutable Sources And Reprocessing

When proposing incrementalization, window rebuilds, snapshots, materialized intermediates, pre-aggregates, or shortcuts that avoid full history:

- identify whether each affected source is append-only, late-arriving, or mutable after the primary event;
- for mutable business facts such as revenue, status, forecast, attribution, reviews, balances, or cancellations, do not assume event timestamp is the only safe reprocessing key;
- treat current-state enrichment tables, profile attributes, dimensions, dictionaries, and mappings as mutable when they can rewrite historical output;
- decide whether historical rows should be recalculated with current attributes or frozen as-of the event time before declaring a window rewrite safe;
- if a source filter uses an update-aware expression such as `greatest(updated_at, event_ts)`, do not replace it with event timestamp alone unless freshness/update contract and duplicate-handling are proven;
- check or ask for the freshness/update contract: which timestamp or process makes changed rows visible, how late changes can arrive, and which target partitions or keys must be rebuilt;
- if no contract is known, surface a standalone `Бизнес-семантика:` risk through `agent-workflow-core`;
- for money or attribution metrics, treat "late changes are possible" as a blocker for declaring an incremental/window rewrite safe.

Risk patterns:

- joining order-created events to a mutable orders mart can make revenue metrics change long after order creation;
- joining an event aggregate to a current profile/dimension table can intentionally rewrite historical rows when attributes change, so the model must define current-state restatement vs as-of attributes.

## Optimization Risk Classification

When reviewing or proposing SQL optimizations, separate candidates by risk:

- semantics-preserving query-shape rewrites, where equivalence can be checked with read-only counts or `EXCEPT`-style comparisons;
- business-semantic rewrites, where source choice, grain, windows, tie-breaks, mutable facts, or attribution rules may change;
- physical/runtime changes such as projections, materialized intermediates, staging tables, data-placement choices, partitions, or engine-specific maintenance/statistics operations.

For every business-semantic rewrite, use `agent-workflow-core` to surface a standalone `Бизнес-семантика:` line before calling the candidate safe. For physical/runtime changes, state the SQL-quality risk and missing evidence; let `agent-workflow-core` decide approval, final proof status, and extended sandbox validation.
