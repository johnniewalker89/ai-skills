---
name: sql-style-core
description: Mandatory engine-agnostic SQL style and readability layer. MUST be used for every SQL writing, editing, review, or optimization task together with `agent-workflow-core` and `sql-quality-core`, before applying ClickHouse, Greenplum, dbt, or other engine-specific SQL skills. Covers formatting/layout, aliases, source qualification, compact vs expanded expressions, named CTE/expression readability, and formatting-only self-review without engine-specific syntax.
---

# SQL Style Core

Use this skill for SQL code style and readability in every SQL writing, editing, review, or optimization task.

This skill owns engine-agnostic SQL style. `sql-quality-core` owns SQL business semantics. Engine-specific skills own engine syntax, runtime behavior, and engine-specific style overlays.

Any database access must go through `db-access`.

## Role

- Purpose: provide engine-agnostic SQL style and readability checks.
- Owns: SQL formatting/layout, source qualification, aliases, common `AS` alignment, compact vs expanded expression choice, named CTE/expression readability, and formatting-only self-review.
- Delegates to: `agent-workflow-core` for delivery workflow, `sql-quality-core` for SQL semantics, `db-access` for database access, and engine/dbt skills for engine-specific rules.

## Hard Gates

1. **Skill-chain gate.** Use `agent-workflow-core` first and `sql-quality-core` before or alongside this style pass.
2. **Reference gate.** Read `references/style.md` for SQL writing, editing, or review tasks.
3. **Style-only gate.** Do not change business semantics from this skill. Route semantic concerns to `sql-quality-core` and engine concerns to the target engine skill.
4. **Self-review gate.** Before returning SQL, run a formatting-only self-review after semantic and engine-specific checks are complete.

## Workflow

1. Always use `agent-workflow-core` first for task mode and delivery rules.
2. Always use `sql-quality-core` before or alongside this skill for SQL semantics.
3. Apply this skill before engine-specific SQL skills, then apply the target engine style overlay.
4. Read `references/style.md` for SQL writing, editing, or review tasks.
5. Before returning SQL, run a formatting-only self-review after semantic and engine-specific checks are complete.

## Reference Triggers

- Read `references/style.md` for common SQL formatting, aliases, source qualification, compactness, CTE readability, joins, filters, grouping, and multiline expressions.

## Final Checklist

- Did I use `agent-workflow-core` and `sql-quality-core` with this style pass?
- Did every selected column in a multi-table query have a clear source?
- Did aliases use `AS` and preserve a readable common `AS` column where practical?
- Did I use comma-leading formatting consistently for `SELECT`, `WITH`, and multiline `GROUP BY` blocks?
- Did long expressions expand only when compact form hurt readability or broke alignment?
- Did named CTEs or expressions explain meaningful calculation steps instead of hiding business logic in repeated inline expressions?
- Did I avoid re-aliasing CTEs unnecessarily in `FROM` / `JOIN`?
- Did I keep the first `ON` on the same physical line as its `JOIN`, with later join conditions continuing on `AND` lines?
- Did I run a separate formatting-only self-review after semantic and engine-specific review?
