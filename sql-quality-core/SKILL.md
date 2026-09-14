---
name: sql-quality-core
description: Check SQL source choice, grain, joins, metrics, windows and evidence; combine engine and style checks into a standalone SQL result. Use with sql-style-core and the resolved engine owner.
---

# SQL Quality Core

Use this skill for every SQL writing, editing, review, optimization, validation, DDL, or data-artifact task.

This skill owns engine-agnostic SQL business semantics and quality gates. `sql-style-core` owns shared SQL style. Configured access tools and optional operational owners provide live evidence under their own policy; the SQL chain works with supplied evidence when no live access is available. Engine/dbt skills own target-specific SQL.

## Role

- Purpose: provide engine-agnostic SQL quality checks before any engine-specific SQL layer.
- Owns: source choice, driving grain, join sanity, independent fact aggregate combination, multi-row fact semantics, category-safe metrics, metric/window semantics, proxy timestamp coverage, duration/time-to-stage semantics, sequential funnel logic, mutable-source risk, smoke scale, validation mindset, required efficiency-evidence coverage, SQL-quality blockers, evidence/access boundaries and the combined SQL result status.
- Delegates to: `sql-style-core` for formatting, engine/dbt owners for their target-specific checks, and the available configured access tool or caller-selected operational owner for live operations.

## Hard Gates

1. **Skill chain gate.** Use this skill with `sql-style-core` and the resolved available engine owner. CH/GP entry points activate this complete SQL chain without workflow or private access dependencies. Add an available dbt owner for dbt-specific behavior; missing tooling bounds that claim.
2. **Database access gate.** Use the available configured tool under references/evidence_and_access.md and its policy for live proof. A caller-selected operational owner may supply that route. Without live access use supplied/repo evidence and state the limitation; no private skill is mandatory.
3. **Source/grain gate.** Do not draft, approve, or return non-trivial SQL until source choice, driving grain, central joins, and metric semantics have been considered.
4. **Independent facts gate.** When two or more fact aggregates are combined, name each fact grain and validate the final join/output grain. Do not approve a shape that can duplicate one fact's measures across another fact's dimensions.
5. **Date/window gate.** Do not claim full business-window coverage when filtering or validating through a proxy timestamp unless coverage is proven or the claim is downgraded to the proxy/guarded surface.
6. **Duration gate.** Duration and time-to-stage metrics must subtract from the actual lifecycle start timestamp, not from a truncated reporting bucket, unless the metric is explicitly bucket-relative.
7. **Business semantics gate.** Do not silently change source, grain, attribution, windows, categories, deduplication, funnel or mutable-source semantics. Resolve material uncertainty from supplied/repo/live evidence, or surface the question and bounded assumption before claiming correctness.
8. **Sequential/entity gate.** For funnels or child-entity metrics, each step and metric name must match the declared entity grain. If this check fails for a production-like artifact, SQL-quality-check fails.
9. **Validation gate.** Read `references/evidence_and_access.md` before proof, live access or returning non-trivial SQL. Use the lightest safe proof-capable checks or state what is missing. A static review, EXPLAIN or smoke proves only its named scope.
10. **Return gate.** Before returning any non-trivial SQL, ask whether there is an obvious safer, simpler, or cheaper semantics-preserving shape. Apply it or explain the tradeoff.
11. **Efficiency evidence gate.** Every SQL task requires an evidence-based efficiency assessment of the final SQL, including writing, edits, review, validation and DDL/load. Read `references/validation_and_self_review.md`; the engine owner interprets physical cost and alternatives. Reuse applicable exact evidence. Missing material proof leaves efficiency unproven and blocks an optimality claim; successful execution alone is insufficient.
12. **Self-review gate.** Before reporting SQL-quality-check passed for production-like SQL/DDL/load/validation artifacts, run this skill's Final Checklist against the final artifacts themselves. P1/P2 correctness, refresh, naming, or executability issues block pass and sandbox escalation.

## Workflow

1. Resolve source lineage and driving grain; load references for the affected semantic decisions.
2. Check central match/multiplication behavior, independent fact grains and metric/window/entity contracts against final SQL.
3. Use the smallest proof-capable window/case set. Reuse one exact output for multiple invariants when sufficient, keeping every claim's scope visible.
4. Run the Final Checklist and combine semantic, style and engine checks into the SQL result status with explicit proof limits. An optional project workflow may consume this result.

## Reference Triggers

- Read `references/evidence_and_access.md` for supplied/live evidence, access boundaries and final SQL status.
- Read `references/data_artifact_proof.md` for new marts, DDL/load/rebuild and production-like readiness.
- Read `references/data_artifact_checkpoint.md` when material source/grain/refresh/validation choices need a concrete proposal.

- Read `references/source_grain_and_joins.md` when source choice, lineage, grain, joins, unmatched rows, or row multiplication matter.
- Read `references/metrics_windows_and_funnels.md` when metrics use categories, dates/windows, lifecycle/funnel steps, child entities, mutable sources, or optimization candidates.
- Read `references/validation_and_self_review.md` in every SQL task before choosing proof or returning SQL/findings; efficiency evidence is required alongside semantic checks.
- Read `references/examples.md` when source choice, driving grain, or category-safe metric decisions need a compact example.

## Final Checklist

- Source/lineage and driving grain supported by repo/live evidence?
- Central joins have right-key/flag match coverage; independent fact aggregates cannot multiply measures?
- No fake representative rows; categories include material other/unknown cases?
- Business windows and proxy coverage honest; duration starts at lifecycle timestamp?
- Funnel steps follow accepted prior events, names match entity grain, mutable enrichment has refresh/reprocessing semantics?
- Bounded final-SQL checks and owner chain complete; P1/P2 blockers prevent pass?
- Final SQL efficiency supported by applicable evidence and assessed alternatives; missing proof explicit, no unsupported optimality claim?
