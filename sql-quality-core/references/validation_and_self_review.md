# Validation And Self-Review

Use this reference before returning non-trivial SQL, reviewing production-like artifacts, validating SQL, or classifying SQL-quality blockers.

## Smoke Scale

When the task lets you choose a smoke period:

- start with a narrow complete period that is non-empty and exercises required joins, such as an hour or a day;
- widen only when relationships are sparse, lifecycle semantics require it, or representativeness is part of the task;
- do not choose a month-sized or otherwise large smoke window by default;
- if a broad window is intentional, state why and verify the plan remains acceptable.

## Validation Mindset

Before returning or approving non-trivial SQL:

- validate the central business relationship separately from final non-emptiness;
- run lightweight validation when the selected access owner is available and safe: metadata checks, constrained counts, `LIMIT`, aggregate sanity checks, or an execution plan;
- treat a successful plan as "can be planned", not "ready";
- interpret the plan with the engine-specific skill: largest scans, largest estimates, repeated work, materialization/reuse, partition/key pruning, and surprising data movement where applicable;
- decide whether surprising plan items are accepted, reduced, or rewritten;
- after changing the final query window, sources, joins, filters, or category logic, rerun affected sanity counts and keep notes/evidence artifacts aligned with the final SQL, not an earlier draft;
- if validation cannot run, state why and identify the remaining risk.

## Cleanup And Repair Validation

For cleanup, deduplication, repair, backfill, or negative-row recovery plans, validate the declared repair grain, not only the removal predicate.

Before calling the repair sufficient:

- prove the bad-row/drop predicate is gone from the repaired source and target surfaces;
- prove same-grain duplicate keys are absent after repair, even when cross-entity overlap is already fixed;
- reconcile the accepted source/repair surface to the affected target or aggregate totals for the declared windows/partitions;
- separate raw/source repair checks from finalized/aggregate target checks when the target is built from the raw surface;
- if the repair intentionally removes rows outside pairwise overlap, name that business decision and validate the resulting totals.

## Default SQL Return Gate

Before returning any non-trivial SQL to the user, run a final SQL-quality self-review. For small one-off snippets this can be a lightweight mental pass; for production-like queries, marts, loads, DDL, or validation suites it is a real gate.

Ask whether there is an obvious safer, simpler, or more efficient semantics-preserving shape. If yes, apply it or explain why it is not appropriate. If an improvement would change business semantics, require explicit business-semantic attention through `agent-workflow-core`. If it needs engine-specific proof or sandbox work, delegate that part to the engine skill and `agent-workflow-core`.

## Final SQL Self-Review Gate

Before returning production-like SQL/DDL/load/validation artifacts as SQL-quality-check passed, review the final artifacts themselves, not an earlier prototype. Report pass/fail and blockers to `agent-workflow-core`; do not decide final proof status or sandbox escalation from this skill.

Ask:

- Is every returned DDL/load/validation artifact syntactically valid for the target engine, or explicitly marked unvalidated with a concrete blocker?
- Does the load/refresh strategy truly replace or remove stale target rows at the declared rebuild grain?
- Do metric names and calculations match the approved business flow, window, and entity grain?
- Do metric names, comments, and validation notes distinguish session-level, event-level, order-level, and sequential funnel semantics?
- For sequential funnels, does each step search from the previously accepted step, not from an independent global first event that can hide later valid events?
- For child-entity metrics inside a parent funnel, do names such as `orders_*` count all qualifying child entities, or are first-child metrics explicitly named?
- Are event-count, entity-count, and sequential funnel metrics separated or clearly named?
- Are dimensions and reconciliation sources semantically aligned? If the load derives a dimension from one source but validation compares another source or legacy mapping, label it as semantic drift rather than proof of equality.
- Are unknown/other categories handled explicitly instead of being folded into a valid business bucket?
- Are validation queries executable for the stated proof level, with read-only source checks separated from post-load/extended-sandbox target-table checks?
- Is there an obvious simpler, safer, or more efficient shape that preserves semantics?

If this self-review finds a P1/P2 correctness, refresh, or executability issue, do not treat the SQL-quality check as passed. State that the next SQL step is to revise the artifacts, then run the relevant read-only SQL validation again; let `agent-workflow-core` choose the user-facing proof status and next approval step.
