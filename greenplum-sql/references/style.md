# Greenplum Style Overlay

Use this file after `sql-style-core/references/style.md`. It contains only Greenplum-specific or local Greenplum style rules.

## Navigation

- [Expressions and aliases](#greenplum-expressions-and-aliases)
- [WITH and runtime parameters](#with-and-runtime-parameters)
- [Multiline expressions](#greenplum-multiline-expressions)
- [DDL formatting](#greenplum-ddl-formatting)

## Greenplum Expressions And Aliases

- Do not reuse a newly defined alias inside the same `SELECT` list.
- If a derived value is needed by another expression, move it into an inner CTE/subquery or repeat the expression when it is still simple.
- Use PostgreSQL/Greenplum casts consistently with existing project style, including `::DATE`, `::TEXT`, and `NUMERIC(...)` patterns.

Compact Greenplum expressions are fine when they stay readable:

[Example 1](style_examples.md#example-1).

Compact null handling is also acceptable:

[Example 2](style_examples.md#example-2).

## WITH And Runtime Parameters

- Greenplum does not support ClickHouse-style scalar `WITH` declarations such as `expression AS alias` before `SELECT`.
- In Greenplum, use only subquery CTEs in `WITH`.
- When runtime parameters are needed, declare them in a one-row CTE such as `params AS (SELECT ...)`.
- Place a params CTE first in the `WITH` chain when later CTEs depend on it.
- Reuse params values through `FROM params`, `CROSS JOIN params`, or another explicit join pattern inside downstream CTEs.
- For standalone smoke/ad-hoc SQL with a fixed chosen period, verify plan pruning through the selected access owner when live access is needed and available; if a params CTE prevents static partition pruning, use explicit literals or another shape that preserves pruning.

Compact runtime conversion inside a one-row params CTE:

[Example 3](style_examples.md#example-3).

## Greenplum Multiline Expressions

- Expand long `coalesce` / `nullif` / `CASE` expressions when compact form hides fallback semantics.
- For md5 technical ids, keep concatenated parts auditable and source-qualified.

Preferred expanded null-handling expression:

[Example 4](style_examples.md#example-4).

Preferred expanded `CASE` with technical id:

[Example 5](style_examples.md#example-5).

## Greenplum DDL Formatting

- Before editing DDL, inspect a neighboring object of the same DB and object type when one is available in the repo.
- In Greenplum `CREATE TABLE`, each column definition must start on a new line.
- In column lists for `CREATE TABLE`, use comma-leading formatting when that is the project pattern for the target object.
- Type names and important modifiers should stay visually aligned when the block remains readable.
- `COMMENT ON TABLE` and `COMMENT ON COLUMN` should be separate statements.
- Column descriptions should stay within a single SQL statement unless multiline text is truly needed.
- Table parameters such as `WITH (...)` should stay on one line when readability is not harmed.
- Physical design clauses such as `DISTRIBUTED BY` must be explicit and intentional.

Preferred `CREATE TABLE` pattern:

[Example 6](style_examples.md#example-6).
