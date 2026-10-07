# SQL Evidence And Access

Read before selecting proof, invoking a live tool or returning non-trivial SQL.
The standalone chain is the resolved engine owner plus sql-quality-core and
sql-style-core. It requires no workflow, context repository, personal standard,
particular MCP or installed private access skill.

## Supplied Evidence

Use supplied SQL, DDL, schema/lineage, repository contracts and plan/output evidence.
Resolve the intended metric/grain/window and target engine. Missing information
is an explicit assumption/question or an unproven claim, never an invented schema.
With no live access, deliver the useful static review/query and state its limits;
do not call execution, result correctness or performance measured. Ask for only
material missing metadata. A provided EXPLAIN is bounded evidence of its stated
query/settings/environment, not permission to query that database.

## Causal claims for discrepancies

Before explaining a before/after or source/target discrepancy, use sufficient
saved evidence first and distinguish the measured delta, a mechanism that could
produce it, and the historical cause of that state:

- Bind the comparison to the accepted grain, population/window, metric semantics
  and observed source/target versions or times. Use the source/grain contract for
  identity and multiplicity; the engine owner establishes relevant execution
  context. Separate retention/TTL boundaries or other non-overlapping data from
  the comparable slice; justify any exclusion and retain its measured difference.
- Locate the delta in the relevant cohorts, keys or periods and quantify their
  contributions and unexplained remainder. Matching grand totals alone cannot
  explain offsetting differences; do not substitute current source/rebuilt equality
  for evidence of the earlier source or target state.
- For each proposed cause, state its observable prediction and check which rows
  or measures in the compared population it would affect. If an adequate check
  finds zero affected rows for a nonzero delta, reject that explanation for the
  checked scope. Partial or unavailable coverage leaves the hypothesis unproven;
  it does not establish zero impact elsewhere. Do not reuse a refuted hypothesis.
- A changed filter, unchanged aggregate formula, model-creation commit or nearby
  deployment date may identify a candidate mechanism or temporal correlation;
  none alone proves that it produced this delta or that a backfill did or did not
  run. Historical execution claims need applicable retained execution/state
  evidence or a reconstruction that covers the relevant old inputs and behavior.
- Report what is measured, which mechanisms were supported or ruled out, and
  which historical cause remains unknown. Preserve proven cohort/retention facts
  without turning missing history into an invented cause. Request only the
  missing evidence that can resolve a material claim; do not fetch logs or rerun
  checks when sufficient proof is already supplied or unavailable history cannot
  be recovered through that check. Live operations retain their access policy.

## Available Live Tools

If live checks are needed, use the user's configured and available database/catalog
tool under its existing access policy. In an environment with operational skills,
the caller supplies the selected owner; standalone use follows the available tool
contract directly. Verify non-secret service/cluster/environment and database/schema
where exposed. Matching names or a successful query alone do not establish identity.

Prefer bounded metadata, EXPLAIN and proof-capable read-only checks when safe.
EXPLAIN ANALYZE executes work; neither a SELECT nor read-only label guarantees cheap
execution. Use query limits/windows appropriate to the evidence needed and available
capability. Missing identity/privilege/availability bounds the claim and operation.
Do not switch to another account, privileged contour or install/repair a connector
because access failed. Missing live access does not block supplied-evidence review.

Before writes, rebuilds, expensive checks or cleanup, satisfy the exact operational
authorization for contour/action/target and recovery. Source-edit permission is not
live DB permission. Retain existing authorization for unchanged actions; no task
mode creates extra consent. Start/poll/cancel only through supported tools and retain
their own query handles. On ambiguous result read state before retrying.

## SQL Result Contract

sql-quality-core combines semantic, style and engine findings into the SQL result;
an optional project workflow consumes it without becoming a required dependency.
Distinguish supplied-evidence/static review, executed bounded checks, approved
sandbox proof and production acceptance. For each material claim name comparison
surface, scope, applicability and missing evidence. P1/P2 SQL correctness or
executability blockers prevent SQL pass. An optimality claim requires engine evidence
and considered alternatives; execution success alone is insufficient.

Read data_artifact_proof.md for new marts, DDL/load/rebuild or a production-readiness
claim. It specifies proof, not permission to access systems. The engine owner defines
physical/readiness checks; style owns formatting only. Report what was delivered,
strongest completed proof and remaining limitation in the user's language.
