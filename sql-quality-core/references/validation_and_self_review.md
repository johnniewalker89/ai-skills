# Validation And Self-Review

Use this reference in every SQL task before selecting proof or returning SQL/findings.

## Navigation

- [Efficiency evidence](#efficiency-evidence-for-every-sql-task) and [smoke scale](#smoke-scale)
- [Whole-statement binding](#whole-statement-binding), [claim binding](#validation-claim-binding) and [validation mindset](#validation-mindset)
- [Repair validation](#cleanup-and-repair-validation), [return gate](#default-sql-return-gate) and [final self-review](#final-sql-self-review-gate)

## Efficiency Evidence For Every SQL Task

Assess the efficiency of the final SQL while preserving its required semantics.
The engine owner interprets the physical checks; this skill requires their coverage.

- Bind evidence to final SQL, settings, source shape, data window and relevant scale.
  Use plans, current metadata/statistics, measured query history or bounded execution
  as needed to assess scans/pruning, joins, sort/aggregate cost and repeated work.
- Compare like-for-like work: the same input population/window and measured stages.
  An INSERT-only duration and a whole task including setup, cleanup or maintenance
  are different measurements, not a demonstrated speedup.
- Interpret the evidence and assess plausible cheaper alternatives. Explain the
  accepted shape or tradeoff; a valid query, small LIMIT or successful run alone
  does not prove efficiency. Avoid claiming a global optimum from a bounded check.
- For a simple expression with no material data access, a concrete explanation of
  its work and relevant alternatives can suffice; a short task still needs evidence.
  For formatting-only changes, reuse applicable proof for unchanged SQL semantics.
- Reuse current sufficient evidence. Query logs are needed when runtime history,
  observed cost or a before/after performance claim requires them; engine skills
  contain known sources. Do not fetch logs mechanically when they cannot answer
  the question or replace required plan/result proof with a log entry.
- If necessary plan/metadata/runtime evidence is unavailable, identify the exact
  gap and keep efficiency unproven. A correctness pass does not close that gap;
  approval, access and sandbox boundaries remain with their owners.

## Smoke Scale

When the task lets you choose a smoke period:

- start with a narrow complete period that is non-empty and exercises required joins, such as an hour or a day;
- widen only when relationships are sparse, lifecycle semantics require it, or representativeness is part of the task;
- do not choose a month-sized or otherwise large smoke window by default;
- if a broad window is intentional, state why and verify the plan remains acceptable.

## Whole-Statement Binding

Apply before a readiness conclusion or SQL pass after changing sources, JOINs or
SQL rendering, including SQL embedded in another language. Inspect the complete
statement the caller will send, with representative parameters where relevant;
include inherited SELECT, ON, WHERE, grouping and ordering expressions. A review
of the added fragment does not validate the surrounding query.

Bind relevant tables, aliases and column references to available current schema
or DDL evidence for that target. Check each query scope using the engine's name
and output-alias resolution rules. A newly joined source can make an unchanged
reference ambiguous or change which entity a filter addresses. Resolve collisions
from the intended business source; an arbitrary prefix or the first matching
column is not a semantics-preserving fix. Qualification/layout conventions remain
with `sql-style-core`; available engine owners interpret target-specific binding.

Use the lightest adequate evidence for the claim: schema-backed static binding,
an applicable saved plan, or an authorized bounded target-engine check. Bind it
to the final rendered statement, rather than a separately rewritten approximation.
Host-language parsing/compilation, a mocked query call and assertions for SQL
substrings prove their own surface; they do not prove SQL name resolution or
execution. Another engine's synthetic schema can expose a risk, but does not prove
the actual target schema, runtime statement or target-engine success.

For a regression, choose an observation that distinguishes the invalid original
statement from the corrected final statement. Include an affected inherited
clause when a source/JOIN change caused the defect; finding the new JOIN/filter
text is not that observation. Reuse sufficient saved checks instead of rerunning
unchanged proof.

With incomplete schema, final-render or target-engine evidence, retain a useful
bounded review and identify the missing fact. Do not invent source columns,
declare SQL executable, or claim SQL pass with an unresolved P1/P2 binding issue.
This procedure grants no live access and does not require a live query for every
simple expression; the existing evidence/access and efficiency contracts apply.

## Validation Claim Binding

Before reporting testing completeness or SQL readiness:

1. Link each material claim to the actual submitted SQL or its content hash,
   rendered parameters/relevant settings, target connection/runtime, check stage
   and outcome, and available query ID or captured result. Keep missing fields
   explicit; a query ID alone does not identify the source statement.
2. Compare the executed statement with the final artifact. A changed aggregation
   invalidates the previous execution proof for the new SQL even when row counts
   coincide. Reuse proof for unchanged semantics only within its demonstrated
   scope; a related query is evidence about that query.
3. If the required SELECT failed or was not executed, retain that record and mark
   runtime proof unproven. Passing unit/parser/import or EXPLAIN checks covers
   only those stages. A later matching successful SELECT proves its own SQL,
   parameters and runtime; it does not turn earlier failures into passes or prove
   another service connection, semantic equivalence or efficiency.

Use sufficient saved evidence; this procedure requires no extra live run or test
suite. State the remaining proof gap instead of a blanket "everything tested".

## Validation Mindset

For changed contracts, name the comparison surface and remaining limits alongside
the claim bindings.

Component comparisons, invariant checks, and old/new final-output comparisons
prove different claims. A compositional equivalence argument must also cover
joining, multiplicity, defaults, precision and final assembly; name it as such,
not as an executed end-to-end diff.

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

- when removing invalid rows, prove the bad-row/drop predicate is gone from the repaired source and target surfaces;
- validate occurrence counts at the declared repair grain; require duplicate-key absence only when uniqueness is part of the accepted contract, and preserve legitimate repeats in multiset backfill;
- reconcile the accepted source/repair surface to the affected target or aggregate totals for the declared windows/partitions;
- separate raw/source repair checks from finalized/aggregate target checks when the target is built from the raw surface;
- if the repair intentionally removes rows outside pairwise overlap, name that business decision and validate the resulting totals.

## Default SQL Return Gate

Before returning any non-trivial SQL to the user, run a final SQL-quality self-review. For small one-off snippets this can be a lightweight mental pass; for production-like queries, marts, loads, DDL, or validation suites it is a real gate.

Ask whether there is an obvious safer, simpler, or more efficient semantics-preserving shape. If yes, apply it or explain why it is not appropriate. If an improvement would change business semantics, surface the changed business rule and missing equivalence evidence. If it needs engine-specific proof or sandbox work, use the engine owner for physical proof and the selected operational contract for sandbox actions.

## Final SQL Self-Review Gate

Before returning production-like SQL/DDL/load/validation artifacts as SQL-quality-check passed, review the final artifacts themselves, not an earlier prototype. Report pass/fail and blockers to `sql-quality-core`; combine final SQL proof from these checks and the engine/style results; sandbox execution remains subject to its operational authorization.

Ask:

- Is every returned DDL/load/validation artifact syntactically valid for the target engine, or explicitly marked unvalidated with a concrete blocker?
- Does the load/refresh strategy truly replace or remove stale target rows at the declared rebuild grain?
- Do metric names and calculations match the approved business flow, window, and entity grain?
- Do metric names, comments, and validation notes distinguish session-level, event-level, order-level, and sequential funnel semantics?
- For sequential funnels, does each step search from the previously accepted step, not from an independent global first event that can hide later valid events?
- For child-entity metrics inside a parent funnel, do names such as `orders_*` count all qualifying child entities, or are first-child metrics explicitly named?
- Are event-count, entity-count, and sequential funnel metrics separated or clearly named?
- For discrepancy explanations, are causal predictions checked on the affected population, with retention boundaries and unproven history explicit?
- Are dimensions and reconciliation sources semantically aligned? If the load derives a dimension from one source but validation compares another source or legacy mapping, label it as semantic drift rather than proof of equality.
- Are unknown/other categories handled explicitly instead of being folded into a valid business bucket?
- Are validation queries executable for the stated proof level, with read-only source checks separated from post-load/extended-sandbox target-table checks?
- Is there an obvious simpler, safer, or more efficient shape that preserves semantics?

If this self-review finds a P1/P2 correctness, refresh, or executability issue, do not treat the SQL-quality check as passed. State that the next SQL step is to revise the artifacts, then run the relevant read-only SQL validation again; let `sql-quality-core` choose the user-facing proof status and next approval step.
