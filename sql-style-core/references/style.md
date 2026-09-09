# SQL Style

Use this file for common SQL code style and readability. Engine-specific skills may add stricter rules or exceptions.

## Navigation

- [General rules](#general-rules)
- [Alignment and compactness](#alignment-and-compactness)
- [SELECT formatting](#select-formatting)
- [WITH and CTE readability](#with-and-cte-readability)
- [JOIN and clause layout](#join-where-having-group-by)
- [Multiline expressions](#multiline-expressions)

## General Rules

- SQL keywords and logical operators should be upper-case.
- SQL functions should be lower-case when the local project style allows it.
- Data types should be upper-case.
- In multi-table queries, selected columns must have explicit sources.
- Columns inside expressions should keep explicit sources when omitting them makes lineage ambiguous.
- Column aliases must use `AS`.
- Plain columns do not need redundant aliases in simple local queries.
- In production or multi-table `SELECT`s, explicit plain-column aliases are acceptable when they define the output schema, preserve the common `AS` column, or make lineage clearer.
- Prefer ordering selected expressions from business-facing attributes to technical helper fields.

## Alignment And Compactness

- Keep one visual `AS` column across a `SELECT` block when the block remains readable.
- Do not preserve a common `AS` column by adding excessive horizontal padding to short expressions.
- Prefer compact expressions when the result is still easy to read.
- Expand an expression when compact form becomes hard to read, hides an important calculation step, breaks the common `AS` column, or creates excessive padding.
- If a multiline expression has an alias, keep `AS alias` on the final line of the full expression.

## SELECT Formatting

- Every `SELECT` expression starts on a new line.
- The first `SELECT` expression uses a `+6` space indent.
- Every next `SELECT` expression uses a `+4` space indent and starts with a leading comma.
- After the `SELECT` block, the next block usually starts without an extra blank line.
- Long boolean conditions should be aligned vertically when that improves readability.
- `UNION ALL` should be separated by a blank line above and below when that helps readability.

Preferred pattern:

[Example 1](style_examples.md#example-1).

## WITH And CTE Readability

- Use named CTEs or named expressions to explain meaningful calculation steps.
- For subquery CTEs, use `cte_name AS (...)`.
- Inside a subquery CTE, the inner query block starts with a 4-space indent from the line start.
- Do not indent nested `SELECT`, `FROM`, `WHERE`, or `GROUP BY` by 8 spaces just because they are inside a CTE.
- In a subquery CTE chain, the next CTE starts as `), next_cte AS (` on the same line where the previous CTE closes.
- Do not assign an extra alias to a CTE when referencing it in `FROM` or `JOIN`.
- Table aliases in `FROM` / `JOIN` should be written without `AS`.
- Prefer short meaningful table aliases from project patterns.

Preferred subquery CTE pattern:

[Example 2](style_examples.md#example-2).

## JOIN, WHERE, HAVING, GROUP BY

- Prefer `JOIN` over `INNER JOIN` when ordinary inner-join semantics are intended and no extra emphasis is needed.
- The first `ON` must stay on the same physical line as its `JOIN`.
- Never move the first `ON` to the next line, even for multiline join conditions.
- For multiline join conditions, put the first condition after `ON` on the `JOIN` line and put later conditions on following lines starting with `AND`.
- In a chain of adjacent `JOIN`s, align the `ON` keyword to the same visual column only when each `ON` still stays on its own `JOIN` line.
- Align continuation `AND` conditions under the join condition, not by moving `ON` to a separate line.
- In multiline `WHERE`, each next condition starts on a new line with `AND`.
- In multiline `HAVING`, each next condition starts on a new line with `AND`.
- `WHERE 1=1` and `HAVING` are acceptable when the filter block is multiline or likely to grow.
- For a short one-condition filter, direct `WHERE` without `1=1` is acceptable.
- For date and datetime windows, prefer half-open ranges: lower bound with `>=`, upper bound with `<`.
- In window filters, right-hand side values should be visually aligned when that stays readable.
- `GROUP BY` should explicitly repeat grouped columns instead of using positions.
- In multiline `GROUP BY`, each next grouped expression starts on a new line in comma-leading style.

Preferred aligned join chain:

[Example 3](style_examples.md#example-3).

Preferred multiline join condition:

[Example 4](style_examples.md#example-4).

## Multiline Expressions

- If an expression spans multiple lines, keep continuation lines structurally indented by nesting level.
- For multiline `CASE` expressions, keep `AS alias` on the final line of the full expression.
- Expand long calculation expressions when naming intermediate steps would make the business meaning easier to audit.

Example:

[Example 5](style_examples.md#example-5).
