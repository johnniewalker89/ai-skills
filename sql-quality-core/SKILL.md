---
name: sql-quality-core
description: Mandatory engine-agnostic SQL quality framework. MUST be used for every SQL writing, editing, review, or optimization task before applying ClickHouse, Greenplum, dbt, or other engine-specific SQL skills. Always use with `agent-workflow-core` as the base workflow layer for task mode and delivery rules and `sql-style-core` as the shared SQL style layer. Covers source choice, driving grain, join sanity, multi-row fact semantics, category-safe metrics, date/window and proxy timestamp coverage, duration/time-to-stage semantics, smoke scale, and validation mindset without engine-specific syntax or formatting rules.
---

# SQL Quality Core

Use this skill for every SQL writing, editing, review, optimization, validation, DDL, or data-artifact task.

This skill owns engine-agnostic SQL business semantics and quality gates. `sql-style-core` owns shared SQL style. `db-access` owns database access. Engine/dbt skills own syntax, native idioms, physical execution details, engine-specific style overlays, and plan interpretation.

## Role

- Purpose: provide engine-agnostic SQL quality checks before any engine-specific SQL layer.
- Owns: source choice, driving grain, join sanity, independent fact aggregate combination, multi-row fact semantics, category-safe metrics, metric/window semantics, proxy timestamp coverage, duration/time-to-stage semantics, sequential funnel logic, mutable-source risk, smoke scale, validation mindset, and SQL-quality blockers.
- Delegates to: `agent-workflow-core` for delivery workflow/proof status, `sql-style-core` for shared SQL style, `db-access` for database access, and engine/dbt skills for engine-specific rules.

## Hard Gates

1. **Skill chain gate.** Use `agent-workflow-core` first, this skill before any engine-specific SQL skill, `sql-style-core` for shared style, and the matching engine/dbt skill for target-specific SQL.
2. **Database access gate.** Any database access for SQL work must go through `db-access`. If unavailable, use repo contracts/models/DDL and state the limitation.
3. **Source/grain gate.** Do not draft, approve, or return non-trivial SQL until source choice, driving grain, central joins, and metric semantics have been considered.
4. **Independent facts gate.** When two or more fact aggregates are combined, name each fact grain and validate the final join/output grain. Do not approve a shape that can duplicate one fact's measures across another fact's dimensions.
5. **Date/window gate.** Do not claim full business-window coverage when filtering or validating through a proxy timestamp unless coverage is proven or the claim is downgraded to the proxy/guarded surface.
6. **Duration gate.** Duration and time-to-stage metrics must subtract from the actual lifecycle start timestamp, not from a truncated reporting bucket, unless the metric is explicitly bucket-relative.
7. **Business semantics gate.** Do not silently change source, grain, attribution, date/window, category, deduplication, funnel, or mutable-source semantics. If uncertain, surface the business-semantics risk through `agent-workflow-core`.
8. **Sequential/entity gate.** For funnels or child-entity metrics, each step and metric name must match the declared entity grain. If this check fails for a production-like artifact, SQL-quality-check fails.
9. **Validation gate.** Before returning non-trivial SQL, run the lightest safe SQL-quality validation or state the blocker. A plan/smoke only proves what it actually checks.
10. **Return gate.** Before returning any non-trivial SQL, ask whether there is an obvious safer, simpler, or cheaper semantics-preserving shape. Apply it or explain the tradeoff.
11. **Self-review gate.** Before reporting SQL-quality-check passed for production-like SQL/DDL/load/validation artifacts, review the final artifacts themselves. P1/P2 correctness, refresh, naming, or executability issues block pass and sandbox escalation.

## Workflow

1. Identify whether the task is writing, editing, review, optimization, DDL, validation, lineage, or explanation.
2. Identify the target engine and activate the matching engine/dbt skill.
3. Choose or verify sources, source lineage, and repo/live evidence.
4. Name the driving business grain and make joins preserve that grain.
5. For combined fact aggregates, name each fact grain and prove the final output grain does not duplicate measures.
6. Check metric semantics: categories, windows, proxy timestamp coverage, durations, mutable sources, funnel sequence, and entity level.
7. Choose bounded validation that can check the requested behavior within the current access boundary.
8. Run final SQL self-review and report SQL-quality pass/fail/blockers to `agent-workflow-core`; do not decide final proof status from this skill.

## Reference Triggers

- Read `references/source_grain_and_joins.md` when source choice, lineage, grain, joins, unmatched rows, or row multiplication matter.
- Read `references/metrics_windows_and_funnels.md` when metrics use categories, dates/windows, lifecycle/funnel steps, child entities, mutable sources, or optimization candidates.
- Read `references/validation_and_self_review.md` before returning non-trivial SQL, reviewing production-like artifacts, validating SQL, or classifying SQL-quality blockers.
- Read `references/examples.md` when source choice, driving grain, or category-safe metric decisions need a compact example.

## Final Checklist

- Did I apply the required skill chain and keep database access inside `db-access`?
- Did I choose sources by business semantics, repo-backed proof, live DB state, grain, and join keys?
- Did I name the driving grain and make central joins match it?
- For independent fact aggregates, did I name each fact grain and validate that final join/output grain cannot duplicate measures?
- Did I validate central match coverage with right-side keys or explicit match flags?
- Did I avoid fake representative rows from independent aggregates over multi-row facts?
- Did category-specific metrics cover material categories or include `other_*` / `unknown_*`?
- Did date/window logic express business semantics and use both lower and upper lifecycle bounds when needed?
- If a proxy timestamp/filter was used for validation or performance, did I prove full business-window coverage or downgrade the claim to the proxy/guarded surface?
- Did duration/time-to-stage metrics subtract from the actual lifecycle start timestamp, not a truncated bucket?
- Did sequential funnel logic search each step from the accepted previous step?
- Did child-entity metric names match whether all children or only first children are counted?
- Did mutable-source or current-state enrichment risk get an explicit freshness/reprocessing contract or business-semantics warning?
- Did smoke scale stay bounded unless a broader window was justified?
- Did final SQL self-review pass without P1/P2 issues before I reported SQL-quality-check passed?
