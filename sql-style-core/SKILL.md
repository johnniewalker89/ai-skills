---
name: sql-style-core
description: Mandatory engine-agnostic SQL style and readability layer. MUST be used for every SQL writing, editing, review, or optimization task together with `agent-workflow-core` and `sql-quality-core`, before applying ClickHouse, Greenplum, dbt, or other engine-specific SQL skills. Covers formatting/layout, aliases, source qualification, compact vs expanded expressions, named CTE/expression readability, and formatting-only self-review without engine-specific syntax.
---

# SQL Style Core

Use this skill for SQL code style and readability in every SQL writing, editing, review, or optimization task.

This skill owns engine-agnostic SQL style. `sql-quality-core` owns SQL business semantics. Engine-specific skills own engine syntax, runtime behavior, and engine-specific style overlays.

Direct database/OpenMetadata MCP access must go through `db-access`; a separately installed typed runtime-read route instead follows its dedicated access owner and exact approval contract.

## Role

- Purpose: provide engine-agnostic SQL style and readability checks.
- Owns: SQL formatting/layout, source qualification, aliases, common `AS` alignment, compact vs expanded expression choice, named CTE/expression readability, and formatting-only self-review.
- Delegates to: `agent-workflow-core` for delivery workflow, `sql-quality-core` for SQL semantics, `db-access` for direct database/OpenMetadata MCP access, a separately installed typed runtime-read access owner when selected, and engine/dbt skills for target-specific rules.

## Hard Gates

1. **Skill-chain gate.** Use `agent-workflow-core` first and `sql-quality-core` before or alongside this style pass.
2. **Reference gate.** Read `references/style.md` for SQL writing, editing, or review tasks.
3. **Target-owner gate.** Identify the target engine before SQL writing, editing, review, or optimization and include its available engine owner; add the matching dbt owner when the SQL is inside a dbt model/project. For MySQL or PostgreSQL, where no engine-specific skill exists, use the SQL core pair and document that boundary. Do not treat a style pass as a complete SQL review without the applicable owners.
4. **Style-only gate.** Do not change business semantics from this skill. Route semantic concerns to `sql-quality-core` and engine/dbt concerns to their target owners.
5. **Self-review gate.** Before returning SQL, run this skill's Final Checklist as a formatting-only self-review after semantic and engine-specific checks are complete.

## Workflow

1. Always use `agent-workflow-core` first for task mode and delivery rules.
2. Always use `sql-quality-core` before or alongside this skill for SQL semantics.
3. Identify and activate the target engine owner and, when applicable, the matching dbt owner; apply this skill before their target-specific style overlays.
4. Read `references/style.md` for SQL writing, editing, or review tasks.
5. Before returning SQL, run this skill's Final Checklist as a formatting-only self-review after semantic and engine-specific checks are complete.

## Reference Triggers

- Read `references/style.md` for common SQL formatting, aliases, source qualification, compactness, CTE readability, joins, filters, grouping, and multiline expressions.

## Final Checklist

- Did I use `agent-workflow-core`, `sql-quality-core`, every available target engine/dbt owner, and the explicit MySQL/PostgreSQL no-engine-owner boundary when applicable?
- Did every selected column in a multi-table query have a clear source?
- Did aliases use `AS` and preserve a readable common `AS` column where practical?
- Did I use comma-leading formatting consistently for `SELECT`, `WITH`, and multiline `GROUP BY` blocks?
- Did long expressions expand only when compact form hurt readability or broke alignment?
- Did named CTEs or expressions explain meaningful calculation steps instead of hiding business logic in repeated inline expressions?
- Did I avoid re-aliasing CTEs unnecessarily in `FROM` / `JOIN`?
- Did I keep the first `ON` on the same physical line as its `JOIN`, with later join conditions continuing on `AND` lines?
- Did I run a separate formatting-only self-review after semantic and engine-specific review?
