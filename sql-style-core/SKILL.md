---
name: sql-style-core
description: Apply shared SQL formatting and readability with sql-quality-core and the resolved engine owner. Formatting changes preserve business semantics; no workflow or access dependency.
---

# SQL Style Core

Use this skill for SQL code style and readability in every SQL writing, editing, review, or optimization task.

This skill owns engine-agnostic SQL style. `sql-quality-core` owns SQL business semantics. Engine-specific skills own engine syntax, runtime behavior, and engine-specific style overlays.


## Role

- Purpose: provide engine-agnostic SQL style and readability checks.
- Owns: SQL formatting/layout, source qualification, aliases, common `AS` alignment, compact vs expanded expression choice, named CTE/expression readability, and formatting-only self-review.
- Delegates to: `sql-quality-core` for semantics/evidence/result status and engine owners for target-specific style overlays. This style pass owns no transport or access policy.

## Hard Gates

1. **Skill-chain gate.** Apply alongside `sql-quality-core` and the resolved engine owner. No generic workflow or database-access skill is required for formatting.
2. **Reference gate.** Read `references/style.md` for SQL writing, editing, or review tasks.
3. **Target-owner gate.** Identify the target engine before SQL writing, editing, review, or optimization and include its available engine owner; add an available matching dbt owner for dbt-specific semantics. For MySQL or PostgreSQL, where no engine-specific skill exists, use the SQL core pair and document that boundary. Do not treat a style pass as a complete SQL review without the applicable owners.
4. **Style-only gate.** Do not change business semantics from this skill. Route semantic concerns to `sql-quality-core` and engine/dbt concerns to their target owners.
5. **Self-review gate.** Before returning SQL, run this skill's Final Checklist as a formatting-only self-review after semantic and engine-specific checks are complete.

## Workflow

1. Apply the shared style reference to the final semantic shape, then the target owner's overlay.
2. For formatting-only changes, verify the changed SQL surface once and reuse semantic proof only when unaffected.
3. Run the formatting-only Final Checklist before returning SQL.

## Reference Triggers

- Read `references/style_examples.md` only when a concrete formatting example is needed; choose the matching example, not the whole collection.

- Read `references/style.md` for common SQL formatting, aliases, source qualification, compactness, CTE readability, joins, filters, grouping, and multiline expressions.

## Final Checklist

- Required SQL companions and every available target engine/dbt owner present?
- Qualified multi-table columns, readable AS alignment and comma-leading layout?
- Expression expansion and named CTEs improve readability; no unnecessary CTE re-aliasing?
- First ON shares its JOIN line, later conditions use AND lines?
- Formatting-only pass preserved meaning after semantic/engine checks?
