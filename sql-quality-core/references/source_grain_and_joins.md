# Source, Grain, And Joins

Use this reference for source choice, lineage explanation, driving grain, joins, match coverage, and row multiplication.

## Navigation

- [Source choice](#source-choice-and-lineage), [driving grain](#driving-grain)
- [Before/after value flow](#beforeafter-value-flow)
- [Hierarchical membership](#hierarchical-membership)
- [Reconciliation and backfill](#reconciliation-and-backfill), [joins](#joins-and-match-sanity)

## Source Choice And Lineage

Before choosing source tables:

- search candidates by exact object names and by business keywords from the task;
- when catalog access is available, search OpenMetadata through the selected configured access tool for candidate tables, owners, tags/domains, column names, descriptions, and lineage before settling on a non-obvious source;
- identify the canonical source from repo contracts, model SQL/YAML, checked-in DDL, source definitions, lineage, or existing project patterns;
- identify live DB candidates when metadata is available through the selected access owner;
- prefer candidates present in both repo and live DB when they fit the requested grain and join keys;
- call a candidate repo-backed only after verifying a concrete local path for that exact object or an explicit checked-in alias/deployment mapping;
- treat comments, similar names, downstream mentions, or another engine's DDL as hints, not repo-backed proof;
- treat DB-only live objects as fallback, not the default;
- if repo/task expectations and DB state disagree, state the mismatch and do not silently substitute a convenient live object.
- if a selected source is unavailable through the selected access owner, choose an alternative only when it preserves the requested business entity, grain, attribution, metric semantics, and validation surface. A live-accessible surrogate is not a valid replacement merely because it can be queried.

When source choice is non-obvious, keep a compact candidate matrix in notes: candidate, repo path, live presence, grain, join keys, freshness, and selected/rejected reason.

For a source replacement, compare eligible business keys and relevant attributes
on the same input state. Matching column names/types does not prove matching
population: downstream eligibility, filtering and deduplication may be missing
from the lower source. Preserve those rules or make the intentional change explicit
before comparing derived metrics; a matching aggregate can hide different keys.

When explaining a table, mart, chain, lineage, source flow, or business logic:

- identify the target object, checked-in DDL/contract, build SQL/model, schedule/orchestration config, and downstream export/consumer configs when they exist;
- use OpenMetadata details/lineage through the selected configured access tool when the table is present in the catalog, and label catalog-only facts separately from repo-backed and live-DB facts;
- list direct SQL sources and classify each as raw/source, dictionary/lookup, mart/model, mirror/export, or unknown;
- do not stop at the first `FROM` when a direct source is itself a mart/model/mirror and the user asked for a chain;
- treat material mart/model sources as possible cross-engine mirrors when repo patterns suggest transfers or load scripts between contours;
- follow material direct sources at least one repo-backed layer deeper, or state why the deeper layer is outside scope, unavailable, ambiguous, or not needed;
- pull the relevant engine skill only when repo-backed lineage reaches another engine layer;
- separate repo-backed lineage facts from live DB metadata and validation facts.

Include material lineage findings in the final chain summary; do not leave cross-engine mirrors, transfer jobs, or deeper material layers only in notes/logs.

## Before/After Value Flow

Before explaining a metric or value-flow change, map both versions through the
producer value, consumer publication and downstream calculation using sufficient
saved or repository evidence. Bind each mapping to its version or time; keep an
unavailable mapping explicit rather than reconstructing it from a shared name.

For each layer, record the value's meaning and expression and distinguish changed
from unchanged behavior. Include grain/population, slice selection, units,
sign handling and NULL/default/fallback rules where they affect that meaning.
A consumer field name alone does not establish the same quantity across versions.

Describe the changed layer without assigning its change to another layer. An
unchanged downstream expression can produce a different result from changed input
values or meaning; it is not a new formula. Trace where a sign or default first
arises instead of attributing it to a consumer that only passes the value through.

Separate the contract-supported effect from a measured row/result difference.
For a claim about the actual discrepancy or its history, apply **Causal claims for
discrepancies** in `evidence_and_access.md`; the mapping alone is not causal proof.

## Driving Grain

Before the final `FROM`, name the business grain: orders, sessions, payments, events, users, accounts, rows loaded, or another entity.

- Drive the query from the requested business entity, not from a broader source that merely can join to it.
- If the task names a business relation, keep that relation in the source flow when available.
- Prefer the project-owned business entity or mart layer over a lower raw/link layer when both are live and repo-backed.
- Use a raw/link layer only when the task asks for raw relationships, the mart is unavailable, or the mart loses required fields; preserve or rebuild normalized business semantics explicitly.
- If the canonical fact for a response, payment, assignment, or other lifecycle entity is unavailable, do not substitute invitation/click/event streams as that entity unless the artifact names the surrogate/cohort semantics and validates the changed meaning.
- Do not use `HAVING matched_count > 0` to hide wrong driving grain; unmatched rows can remain inside groups that also have matches.

## Hierarchical Membership

Apply before drafting hierarchy-dependent eligibility predicates or display paths.
Bind node identity, parent relationships and root markers to the source contract;
keep the relationship graph separate from the eligible set and its presentation.

Establish which ownership, archive and technical-node rules apply to a node alone
or to its descendants. A child's NULL ownership attribute does not establish that
it is outside an owned ancestor's subtree. An include-owned option changes only
that agreed scope; it must not silently admit independently excluded nodes.

Resolve inherited membership on the relevant relationship graph before filtering
away roots or intermediate nodes. Use recursive closure, authoritative ancestry
or another proven equivalent representation. Filtering each row's own attribute,
or traversing only the already filtered graph, can lose the inheritance boundary.
Distinguish a genuinely missing parent from one excluded by the current scope;
retain unresolved ancestry or cycle limitations instead of claiming complete scope.

Derive the eligible node IDs before building their paths. A path traversal seeded
only from physical roots can drop an eligible orphan or a node whose parent is
outside the visible catalog. Where those nodes are permitted, start a display
root there without resetting inherited exclusions. Preserve the accepted full
or visible-scope path meaning; path reachability is not an eligibility rule.

Check exact membership for an owned root, child with NULL local ownership and a
deeper descendant; an eligible shared orphan; and relevant archive/technical
boundaries, including nullable type fields. Verify each supported inclusion mode
and bind list and summary consumers to the same eligible IDs. Compare IDs and
completeness, not only non-empty output or matching grand totals. Reuse sufficient
saved source/result proof; live operations and engine execution retain their owners.

## Reconciliation And Backfill

Before choosing a diff or missing-row insert, define equality separately for each
target: logical identity/comparison fields, fields excluded or checked separately,
set versus multiset semantics, and the compared population/window. Matching schemas
do not establish matching row meaning. Use full-row equality when all compared
values belong to the accepted equality contract; independently generated ingestion
timestamps or transport metadata can otherwise create false missing rows. Do not
exclude a field merely because it looks technical: justify its role and retain
separate checks for material payload/derived values outside the identity.

Separate occurrence identity used to count missing rows from payload correctness.
When the contract identifies an occurrence by its source payload or event key,
check parsed, enriched or other derived values separately against their accepted
mapping; do not silently extend identity with those values. An occurrence already
represented under that identity but carrying different derived values is a payload
discrepancy, not another missing occurrence to insert. Classify that discrepancy
and establish the repair scope separately. Composite or full-row identity remains
valid when the contract makes those fields part of occurrence identity itself.

Use supplied evidence for both missing counts and material separate payload checks
before claiming reconciliation is correct. If payload checks are only proposed or
the evidence cannot distinguish mapping drift, state that limit; correct counts
alone do not validate the mapping.

Preserve the accepted occurrence counts. For multiset backfill, missing occurrences
are the positive source-minus-target count at that comparison grain; DISTINCT or
an existence-only anti-join cannot recover a partially present count. Select only
those missing occurrences under the accepted payload mapping. Content equality
alone cannot distinguish a legitimate repeat from redelivery without supporting
identity or delivery evidence; do not silently convert reconciliation into deduplication.

Bind preview, write and readback to an established source slice and account for
changes on the matching target surface. Re-evaluate the missing set when relevant
state changes; a preview or a single insert is not a concurrency/retry guarantee.
Zero source-minus-target means the compared source occurrences are represented;
target extras require a separate reverse comparison within its applicable scope.
Even two-way equality proves only the declared slice and equality contract, not
upstream completeness, global deduplication or exactly-once delivery.

## Joins And Match Sanity

For central joins:

- decide whether unmatched left rows should be preserved or excluded;
- count left rows, matched rows, unmatched rows, and distinct business keys;
- count matches from a right-side key or explicit match flag, not from the left-side join key;
- treat large unmatched ratios as semantic signals, not only data quality trivia;
- after changing source, join type, date literals, or pruning filters, rerun affected sanity counts against the final shape.

For lookup/enrichment joins:

- verify right-side uniqueness at the intended key when attributes are projected;
- if the right side can duplicate rows, define whether duplicates are business facts, lookup noise, or candidates for deterministic row choice;
- avoid accidental row multiplication by pre-aggregating, reducing, or choosing a join primitive that matches the engine and business intent.

For fallback or snapshot selection, distinguish three cases: no usable slice,
a usable slice with a missing entity, and a present entity with a NULL value.
Resolve whether the source is chosen per entity or for the whole slice/run.
Row-level `coalesce(new, legacy)` does not implement a whole-slice switch;
slice date, eligibility and missing-row defaults belong to the accepted contract.

For independent fact aggregates combined into one output, such as demand and supply, orders and inventory, or events and capacity:

- name the grain of each pre-aggregated fact before the final join;
- make the final join keys cover every dimension that should preserve metric additivity, or explicitly keep unmatched dimensions as separate rows with non-duplicating measures;
- if the final output grain includes a dimension that only one fact family naturally has, do not stretch other fact-family measures across that dimension;
- either keep each fact family's measures in additive-safe blocks, use an explicitly approved allocation rule, or label the result as non-additive for that dimension;
- do not join facts on a coarser key and then sum measures from both sides unless a reconciliation proves the coarser join is one-to-one for the selected window;
- validate the final output grain, not only each source-side aggregate. A smoke that proves both sources return rows does not prove the combined result is safe;
- if the final join can repeat a measure across another fact's segments, SQL-quality-check fails for production-like artifacts and the object must be held/reworked below sandbox handoff until the grain, allocation, or non-additive semantics are explicit and validated.

For build-from-scratch marts, detecting a repeated-measure risk is not the end of the design attempt. Before holding the object, try a bounded recovery design that preserves business intent:

- aggregate both fact families to their common additive grain;
- introduce an explicit allocation rule with source-side control totals;
- remove or rename the dimension that would make a measure non-additive;
- keep measures in separate additive-safe blocks with names that prevent cross-segment summing.

Any recovery that allocates or narrows semantics must be validated against source-side controls. At minimum, prove that final totals reconcile to the accepted source totals for the checked window and name which dimensions are additive, allocated, or non-additive. If this proof is missing, the object stays below sandbox handoff.
