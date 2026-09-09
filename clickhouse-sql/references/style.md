# ClickHouse Style Overlay

Use this file after `sql-style-core/references/style.md`. It contains only ClickHouse-specific or local ClickHouse style rules.

## Navigation

- [Expressions and aliases](#clickhouse-expressions-and-aliases)
- [Scalar and mixed WITH](#scalar-with-and-mixed-with)
- [Multiline expressions](#clickhouse-multiline-expressions)
- [DDL formatting](#clickhouse-ddl-formatting)

## ClickHouse Expressions And Aliases

- If business attributes were already defined earlier in the same `SELECT`, they may be reused in later technical expressions such as `row_id` when the result is clearer.
- Alias reuse inside one `SELECT` is allowed only after the reused alias was defined earlier in the same `SELECT`.
- Reusing aliases inside the same `SELECT` is allowed only when this is supported by ClickHouse and already matches project patterns.
- If an output alias has the same name as a source column, qualify every later expression or predicate that must still bind to the source column (for example, `source.clicks`) or choose a distinct alias. Do not rely on implicit ClickHouse name resolution for this case.
- Prefer ClickHouse-native type and null handling functions such as `toLowCardinality`, `nullIf`, `ifNull`, and `coalesce` according to existing project style.
- For hashing or technical ids, prefer existing project ClickHouse patterns such as `cityHash64(...)`.

Compact ClickHouse expressions are fine when they stay readable:

[Example 1](style_examples.md#example-1).

Compact nested array expressions are also acceptable when they remain auditable:

[Example 2](style_examples.md#example-2).

## Scalar WITH And Mixed WITH

- ClickHouse scalar `WITH` declarations use `expression AS alias`, not `alias AS expression`.
- In a scalar `WITH` chain, every next element starts on a new line with a leading comma and a `+1` space indent.
- In scalar `WITH` declarations, `AS` should align to one tab stop to the right of the longest expression in the block when readable.
- Declare values from `getSetting(...)` once in `WITH` and reuse them by aliases instead of repeating calls.
- In a mixed `WITH`, declare scalar values first and subquery CTEs after them.
- In a mixed `WITH`, the scalar section follows scalar-chain rules first, then the subquery CTE section follows common subquery-chain rules.
- In a mixed `WITH`, the first subquery CTE starts on a new line with a leading comma after the scalar declarations.
- After the first subquery CTE in a mixed `WITH`, each next subquery CTE starts as `), next_cte AS (` on the same line where the previous CTE closes.
- In a mixed `WITH`, scalar aliases may be reused inside subquery CTEs that appear later in the same `WITH` chain.
- Prefer keeping scalar `WITH` expressions on one line when they remain readable.
- If a scalar `WITH` expression becomes too long or materially hurts readability, it is acceptable to expand it across multiple lines and keep the alias aligned on the closing line.

Preferred scalar `WITH` pattern:

[Example 3](style_examples.md#example-3).

Allowed multiline scalar `WITH` pattern:

[Example 4](style_examples.md#example-4).

Preferred mixed `WITH` pattern:

[Example 5](style_examples.md#example-5).

## ClickHouse Multiline Expressions

- For multiline `multiIf(...)`, put conditions and branch values on separate lines when needed.
- Keep the closing `)` with `AS alias` on the final line of the full expression.
- For dictionary reads, expand nested `dictGet` / `toLowCardinality` / null handling when compact form hides the business fallback.

Preferred expanded dictionary expression:

[Example 6](style_examples.md#example-6).

Preferred expanded `multiIf(...)`:

[Example 7](style_examples.md#example-7).

## ClickHouse DDL Formatting

- Data types in ClickHouse DDL should follow the project type naming pattern and stay visually consistent inside one block.
- In `CREATE TABLE`, each column definition must start on a new line.
- In column lists for `CREATE TABLE`, use comma-leading formatting when that is the project pattern for the target object.
- Type names and important modifiers should stay visually aligned when the block remains readable.
- Table-level clauses such as `ENGINE`, `ORDER BY`, `PARTITION BY`, and `SETTINGS` must stay explicit.
- Multi-column `ALTER TABLE` statements such as `COMMENT COLUMN` chains should use comma-leading formatting when the statement spans multiple lines.
- If the local DDL pattern keeps the closing `;` on a separate line, preserve that pattern instead of collapsing it.

Preferred `CREATE TABLE` pattern:

[Example 8](style_examples.md#example-8).

Preferred multi-column comment alteration:

[Example 9](style_examples.md#example-9).
