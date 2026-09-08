---
name: sql-quality-core
description: Check source choice, grain, joins, metrics, windows and lineage for every SQL write, edit, review or optimization. Use with agent-workflow-core, sql-style-core and the available target engine/dbt owners.
---

# SQL Quality Core

Use this skill for every SQL writing, editing, review, optimization, validation, DDL, or data-artifact task.

This skill owns engine-agnostic SQL business semantics and quality gates. `sql-style-core` owns shared SQL style. `db-access` owns direct database/OpenMetadata MCP access; a separately installed access skill may own a typed runtime database-read transport. Engine/dbt skills own target-specific SQL.

## Role

- Purpose: provide engine-agnostic SQL quality checks before any engine-specific SQL layer.
- Owns: source choice, driving grain, join sanity, independent fact aggregate combination, multi-row fact semantics, category-safe metrics, metric/window semantics, proxy timestamp coverage, duration/time-to-stage semantics, sequential funnel logic, mutable-source risk, smoke scale, validation mindset, and SQL-quality blockers.
- Delegates to: `agent-workflow-core` for delivery workflow/proof status, `sql-style-core` for shared SQL style, `db-access` for direct database/OpenMetadata MCP access, a separately installed typed runtime-read access owner when selected, and engine/dbt skills for target-specific rules.

## Hard Gates

1. **Skill chain gate.** Use `agent-workflow-core` first, this skill before any engine-specific SQL skill, `sql-style-core` for shared style, and every available matching engine/dbt skill for target-specific SQL. If no engine-specific skill exists for the resolved engine, keep the SQL core pair and state that boundary instead of inventing an owner.
2. **Database access gate.** Direct database/OpenMetadata MCP access must use `db-access`. A separate typed runtime-read route may be used only through its installed dedicated access owner, complete SQL dependency chain, and exact current approval contract. If no valid route is available, use repo evidence and state the limitation.
3. **Source/grain gate.** Do not draft, approve, or return non-trivial SQL until source choice, driving grain, central joins, and metric semantics have been considered.
4. **Independent facts gate.** When two or more fact aggregates are combined, name each fact grain and validate the final join/output grain. Do not approve a shape that can duplicate one fact's measures across another fact's dimensions.
5. **Date/window gate.** Do not claim full business-window coverage when filtering or validating through a proxy timestamp unless coverage is proven or the claim is downgraded to the proxy/guarded surface.
6. **Duration gate.** Duration and time-to-stage metrics must subtract from the actual lifecycle start timestamp, not from a truncated reporting bucket, unless the metric is explicitly bucket-relative.
7. **Business semantics gate.** Do not silently change source, grain, attribution, date/window, category, deduplication, funnel, or mutable-source semantics. If uncertain, surface the business-semantics risk through `agent-workflow-core`.
8. **Sequential/entity gate.** For funnels or child-entity metrics, each step and metric name must match the declared entity grain. If this check fails for a production-like artifact, SQL-quality-check fails.
9. **Validation gate.** Before returning non-trivial SQL, run the lightest safe SQL-quality validation or state the blocker. A plan/smoke only proves what it actually checks.
10. **Return gate.** Before returning any non-trivial SQL, ask whether there is an obvious safer, simpler, or cheaper semantics-preserving shape. Apply it or explain the tradeoff.
11. **Self-review gate.** Before reporting SQL-quality-check passed for production-like SQL/DDL/load/validation artifacts, run this skill's Final Checklist against the final artifacts themselves. P1/P2 correctness, refresh, naming, or executability issues block pass and sandbox escalation.

## Workflow

1. Resolve source lineage and driving grain; load references for the affected semantic decisions.
2. Check central match/multiplication behavior, independent fact grains and metric/window/entity contracts against final SQL.
3. Use the smallest proof-capable window/case set. Reuse one exact output for multiple invariants when sufficient, keeping every claim's scope visible.
4. Run the Final Checklist and hand SQL-quality pass/fail/blockers to workflow; this skill does not decide overall readiness.

## Reference Triggers

- Read `references/source_grain_and_joins.md` when source choice, lineage, grain, joins, unmatched rows, or row multiplication matter.
- Read `references/metrics_windows_and_funnels.md` when metrics use categories, dates/windows, lifecycle/funnel steps, child entities, mutable sources, or optimization candidates.
- Read `references/validation_and_self_review.md` before returning non-trivial SQL, reviewing production-like artifacts, validating SQL, or classifying SQL-quality blockers.
- Read `references/examples.md` when source choice, driving grain, or category-safe metric decisions need a compact example.

## Final Checklist

- Source/lineage and driving grain supported by repo/live evidence?
- Central joins have right-key/flag match coverage; independent fact aggregates cannot multiply measures?
- No fake representative rows; categories include material other/unknown cases?
- Business windows and proxy coverage honest; duration starts at lifecycle timestamp?
- Funnel steps follow accepted prior events, names match entity grain, mutable enrichment has refresh/reprocessing semantics?
- Bounded final-SQL checks and owner chain complete; P1/P2 blockers prevent pass?
