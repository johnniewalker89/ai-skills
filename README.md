# AI Skills

Open beta package of portable Codex skills for SQL/data work.

## Included skills

- `agent-workflow-core` - task mode, planning, context, stop-points, validation wording, self-review.
- `sql-quality-core` - engine-agnostic SQL quality rules: grain, joins, windows, category-safe metrics, proof mindset.
- `sql-style-core` - shared SQL readability and formatting rules.
- `clickhouse-sql` - ClickHouse-specific SQL guidance.
- `greenplum-sql` - Greenplum-specific SQL guidance.
- `db-access` - rules for using already configured database MCP tools safely.

Not included in this release: internal autotest/evaluation tools, authoring standards, private task context, run logs, and local environment files.

## Install

For Codex-style runtimes, copy the skill folders from this repo into:

```text
$CODEX_HOME/skills/
```

Or give an agent this repository URL/folder and ask:

```text
Install skills from this repository.
```

See `PORTABLE_SETUP.md` for a Russian quick start and expected runtime assumptions.

## Runtime assumptions

- The agent runtime already has the database MCP tools configured when database access is needed.
- The skills do not contain credentials, local task snapshots, or private paths.
- Local task context should live outside this repository.

## Feedback

Pull requests are welcome as feedback carriers: notes, agent logs, failed prompts, diffs, and reproducible examples.

The `main` branch is a locked release channel. Opening PRs is expected; merging to `main` is intentionally blocked until the release gate is changed by the maintainer.
