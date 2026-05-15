# Source, Grain, And Joins

Use this reference for source choice, lineage explanation, driving grain, joins, match coverage, and row multiplication.

## Source Choice And Lineage

Before choosing source tables:

- search candidates by exact object names and by business keywords from the task;
- identify the canonical source from repo contracts, model SQL/YAML, checked-in DDL, source definitions, lineage, or existing project patterns;
- identify live DB candidates when `db-access` metadata is available;
- prefer candidates present in both repo and live DB when they fit the requested grain and join keys;
- call a candidate repo-backed only after verifying a concrete local path for that exact object or an explicit checked-in alias/deployment mapping;
- treat comments, similar names, downstream mentions, or another engine's DDL as hints, not repo-backed proof;
- treat DB-only live objects as fallback, not the default;
- if repo/task expectations and DB state disagree, state the mismatch and do not silently substitute a convenient live object.
- if a selected source is unavailable through `db-access`, choose an alternative only when it preserves the requested business entity, grain, attribution, metric semantics, and validation surface. A live-accessible surrogate is not a valid replacement merely because it can be queried.

When source choice is non-obvious, keep a compact candidate matrix in notes: candidate, repo path, live presence, grain, join keys, freshness, and selected/rejected reason.

When explaining a table, mart, chain, lineage, source flow, or business logic:

- identify the target object, checked-in DDL/contract, build SQL/model, schedule/orchestration config, and downstream export/consumer configs when they exist;
- list direct SQL sources and classify each as raw/source, dictionary/lookup, mart/model, mirror/export, or unknown;
- do not stop at the first `FROM` when a direct source is itself a mart/model/mirror and the user asked for a chain;
- treat material mart/model sources as possible cross-engine mirrors when repo patterns suggest transfers or load scripts between contours;
- follow material direct sources at least one repo-backed layer deeper, or state why the deeper layer is outside scope, unavailable, ambiguous, or not needed;
- pull the relevant engine skill only when repo-backed lineage reaches another engine layer;
- separate repo-backed lineage facts from live DB metadata and validation facts.

Include material lineage findings in the final chain summary; do not leave cross-engine mirrors, transfer jobs, or deeper material layers only in notes/logs.

## Driving Grain

Before the final `FROM`, name the business grain: orders, sessions, payments, events, users, accounts, rows loaded, or another entity.

- Drive the query from the requested business entity, not from a broader source that merely can join to it.
- If the task names a business relation, keep that relation in the source flow when available.
- Prefer the project-owned business entity or mart layer over a lower raw/link layer when both are live and repo-backed.
- Use a raw/link layer only when the task asks for raw relationships, the mart is unavailable, or the mart loses required fields; preserve or rebuild normalized business semantics explicitly.
- If the canonical fact for a response, payment, assignment, or other lifecycle entity is unavailable, do not substitute invitation/click/event streams as that entity unless the artifact names the surrogate/cohort semantics and validates the changed meaning.
- Do not use `HAVING matched_count > 0` to hide wrong driving grain; unmatched rows can remain inside groups that also have matches.

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

For independent fact aggregates combined into one output, such as demand and supply, orders and inventory, or events and capacity:

- name the grain of each pre-aggregated fact before the final join;
- make the final join keys cover every dimension that should preserve metric additivity, or explicitly keep unmatched dimensions as separate rows with non-duplicating measures;
- if the final output grain includes a dimension that only one fact family naturally has, do not stretch other fact-family measures across that dimension;
- either keep each fact family's measures in additive-safe blocks, use an explicitly approved allocation rule, or label the result as non-additive for that dimension;
- do not join facts on a coarser key and then sum measures from both sides unless a reconciliation proves the coarser join is one-to-one for the selected window;
- validate the final output grain, not only each source-side aggregate. A smoke that proves both sources return rows does not prove the combined result is safe;
- if the final join can repeat a measure across another fact's segments, SQL-quality-check fails for production-like artifacts and the object must be held/reworked below sandbox handoff until the grain, allocation, or non-additive semantics are explicit and validated.
