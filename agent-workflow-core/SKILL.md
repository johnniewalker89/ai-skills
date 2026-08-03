---
name: agent-workflow-core
description: Mandatory task delivery workflow for non-trivial engineering, data, SQL, dbt, investigation, review, or project work. Use to choose and announce task mode, restore saved local context, hand material external-context gaps to an available research owner, decide when to plan and align with the user, handle unclear business rules, maintain task context, self-review before delivery, and explain rationale/tradeoffs calmly when questioned. Must be used by ClickHouse, Greenplum, and dbt workflow skills.
---

# Agent Workflow Core

Use this skill as the top-level delivery layer for real work, before domain-specific skills.

This skill owns how to run the task. Other skills own domain rules, SQL style, database access, dbt project details, code syntax, and tool details.

Direct database/OpenMetadata MCP access must go through `db-access`. A separate database path is allowed only when an installed dedicated access skill owns a typed read-only tool and an exact current-approval contract; raw database commands over SSH remain forbidden.

## Role

- Purpose: provide the top-level delivery workflow for non-trivial engineering, data, SQL, dbt, investigation, review, or project work.
- Owns: task mode, local context workspace, `environment.md` lifecycle, task snapshots, optional agent logs, planning, stop/approval behavior, validation framing, and final self-review.
- Delegates to: the context-research owner selected by the entry skill for bounded external discovery, entry/domain skills for domain work, `db-access` for direct database/OpenMetadata MCP access, and any separately installed typed runtime-read access owner plus its required SQL chain.

## Hard Gates

These gates are mandatory. If a gate applies, read the named reference before acting. Do not treat references as optional background.

1. **Task mode gate.** Choose exactly one allowed mode: `quick`, `focused`, `project`, `investigation`, or `review`. The mode token is a closed enum: do not append or prepend qualifiers, checklist names, phases, or task labels. `quick-check`, `edit`, `implementation`, `analysis`, `audit`, `research`, `review-pass`, `короткий design review`, and similar variants are invalid even if they feel descriptive. If an invalid mode is announced or suggested by the user, correct it to the nearest allowed mode explicitly before tool work or file edits continue. Choose the lightest safe mode by risk, blast radius, business impact, validation cost, rollback/cleanup complexity, and ambiguity. For non-tiny work, the first user-facing update must start with `Режим:` plus exactly one allowed mode value in backticks, for example: Режим: `review`. Plain text such as "Режим: review", descriptive forms such as "Режим: короткий design review", and suffixed forms such as "Режим: `quick-check`" are not sufficient. Put descriptive subtype text only after the valid mode sentence. Read `references/task_modes.md` when mode choice is not obvious.
2. **Context bootstrap gate.** Establish or restore local task context before domain work when the user provides a task id, explicitly asks for durable context or agent logging, or asks to continue an established context-backed task. Without a task id or explicit context request, do not create new task context by default; work autonomously and update no durable context unless a later user instruction enables it. Read `references/context_and_decisions.md` before context work, `environment.md` work, agent-log work, or continuing an established context task.
3. **External context research gate.** Keep saved-context bootstrap and task-file lifecycle in this skill. When missing requirements, prior decisions, ownership, project documentation, table meaning, lineage, or discussion history can materially change the work, delegate to an available context-research owner selected by the entry skill instead of performing broad external discovery from this core. If none is available, report the evidence gap.
4. **Agent-log gate.** Agent logs are optional. A task id alone does not enable agent logging. Create or append `agent_logs/<TASK_ID>.agent_log.md` only when agent logging was explicitly requested or already established, and only inside the established context workspace.
5. **Database access gate.** Use `db-access` for direct MCP metadata, DDL, `EXPLAIN`, query-log checks, smoke queries, privileged introspection, and OpenMetadata. A non-`db-access` route is valid only when a separately installed access owner defines a typed read-only tool, its complete SQL dependency chain, and exact current approval for the call. A missing or denied contour never authorizes raw SSH database commands.
6. **Privileged/sandbox action gate.** Before any database state-changing action, sandbox CTAS/materialization, cleanup/drop, rebuild, recalculation, or `privileged_access_mcp_*` use, the current task must have explicit approval for the exact database contour, action type, target set, and cleanup/rollback expectation. General approval to continue, edit repo files, prove an idea, or use a sandbox is not enough for privileged database actions. A default MCP outage or timeout is a blocker/escalation question, not permission to switch contours.
7. **Project gate.** For `project` mode, risky/expensive work, destructive/hard-to-reverse work, unclear business rules, or cross-system work, read `references/safety_and_stop_points.md` before implementation or approval requests.
8. **New production-like data artifact gate.** For new marts, models, tables, reports, data contracts, or test/sandbox equivalents of production-like artifacts, choose `project` mode and read both `references/safety_and_stop_points.md` and `references/validation_and_review.md` before creating solution artifacts or asking for approval.
9. **Artifact destination gate.** Code artifacts belong in the target repo/workspace after approval. The context workspace is for task notes, agent logs, decisions, and evidence unless the user explicitly asks for a context-only draft/package. Read `references/safety_and_stop_points.md` before creating solution artifacts.
10. **Cleanup/deletion usage-proof gate.** For repo cleanup, deletion, deprecation, DAG/report/job removal, live cleanup/drop lists, or hard-to-reverse cleanup recommendations, read `references/safety_and_stop_points.md` before editing or recommending removal. Prove ownership and usage with read-only evidence first; keep repo cleanup separate from live state changes.
11. **Validation/proof gate.** Before final delivery for `focused`, `project`, `investigation`, `review`, SQL/dbt/data-pipeline work, or production-like artifacts, read `references/validation_and_review.md`. Final status must match the strongest completed proof level.
12. **Commit/push gate.** Never commit or push repository changes without explicit user approval for that exact commit/push. Inspect status/diff first and include only intended files. Before any push, verify current branch, upstream, and exact remote target; if a feature branch tracks the default branch such as `origin/master` or `origin/main`, stop and fix/ask before pushing.

## New Production-Like Data Artifacts

This gate applies before any solution SQL/DDL/config/task note that embodies a proposed new artifact.

- Do safe bounded read-only reconnaissance after any required context bootstrap when it is needed to make the proposal concrete. Do not ask the user to approve the agent's first look at local files, metadata, existing contracts, or safe small read-only probes.
- Stop before implementation artifacts, sandbox actions, expensive validation, writes, unclear business semantics, or readiness/proof claims.
- Save the full mandatory checkpoint from `references/safety_and_stop_points.md` in the task note or agent log before asking for artifact approval.
- In chat, provide only the decision-grade summary required by `references/validation_and_review.md`.
- Keep repository-artifact approval separate from sandbox/write approval. After artifacts exist, run artifact self-review plus available read-only validation, then ask separately for sandbox validation only if still needed.

## Contract

1. Restore the minimum saved local context before acting when the task depends on repo state, prior decisions, database contour, or existing implementation. Use durable task context only when the context bootstrap gate enables it; hand material external context gaps to the research owner selected by the entry skill.
2. For `focused`, `project`, `review`, and long `investigation` tasks with a task id or established context files, update durable task context unless there is a clear reason not to.
3. For `focused`, show a short approach and continue unless risk, ambiguity, destructive work, or expensive validation appears.
4. For `project`, do safe bounded read-only reconnaissance when it can make the plan concrete, present proof strategy and stop-points, then wait for explicit approval before implementation, generated artifacts, sandbox actions, expensive validation, writes, or readiness claims.
5. For unclear business rules, propose recommended defaults with impact when evidence supports them; do not silently invent semantics.
6. For destructive or hard-to-reverse goals, prefer a safer/reversible path first; manual destructive actions require exact approval for action, contour, target set, evidence, and rollback/cleanup.
7. For cleanup or deletion, do not remove artifacts based only on task description or stale metadata. Check repo callers, runtime/live usage, manual/API trigger paths, owner exceptions, rollback path, and telemetry limits first.
8. When the user asks "why", explain rationale, tradeoffs, evidence, and what would change the choice.
9. Before final delivery, run this skill's Final Checklist and self-review scope, changed files, validation, residual risks, and newest user instructions. After implementation, make the material self-review result visible in the final response.

## Reference Triggers

- Read `references/task_modes.md` when mode choice is not obvious or the task is not `quick`.
- Read `references/context_and_decisions.md` before task context updates, `environment.md` work, agent-log work, or continuing an established context-backed task.
- Read `references/safety_and_stop_points.md` for `project` work, production-like artifact gates, artifact destination, staged approvals, destructive/hard-to-reverse work, cleanup/deletion usage proof, sandbox validation approval, or unclear business rules.
- Read `references/validation_and_review.md` before final delivery, validation-mode decisions, proof-level wording, sandbox-proof questions, business-semantics warnings, or rationale/handoff responses.

## Communication Rules

- Default to concise answers in the user's language.
- For non-tiny work, start the first user-facing update with the chosen mode and highlight exactly one allowed mode value in backticks, for example: Режим: `review`. Put skills/plan/context after that sentence, not before it. Put task subtypes such as check, edit, assessment, or proof in the following prose, not inside the mode token.
- When business-semantics risk is relevant, make it a standalone line and emphasize only the label, for example: `Бизнес-семантика:` возможное отклонение от бизнес-правил; эквивалентность не доказана.
- Put detailed table names, exact counts, query text, long rejected-alternative reasoning, and technical traces in the task note or agent log; in chat give the decision-grade summary.
- If new evidence changes risk, scope, targets, or validation cost, say so and update the plan before acting further.

## Final Checklist

- Did I apply every hard gate that matched the task?
- Did I use only an allowed task mode: `quick`, `focused`, `project`, `investigation`, or `review`, with no suffixes or phase labels inside the mode token?
- If I announced an invalid mode, did I correct it immediately before continuing?
- If the work was non-tiny, did my first user-facing update start with `Режим:` before skills or plan, with the mode value in backticks?
- Did I establish or update durable context only when task id, explicit context request, agent logging, or established context required it?
- Did I keep saved-context lifecycle here and route material external context discovery to an available research owner rather than implementing it in this core?
- Did direct database/OpenMetadata MCP access go through `db-access`, and any separately selected typed runtime database read go through its dedicated access owner, exact approval contract, and SQL chain?
- Before any sandbox write, cleanup, rebuild, or privileged database action, did I have exact current approval for contour, action, target set, and cleanup/rollback expectation?
- Before any commit/push, did I verify branch, upstream, exact remote target, and repo-specific user workflow?
- Did I keep code artifacts in the target repo/workspace unless a context-only output was requested?
- Did I keep repo-artifact approval separate from sandbox/write approval?
- For cleanup/deletion, did I prove ownership and usage limits before removing or recommending removal, and keep live state changes as a separate approved step?
- Did I avoid silently deciding unclear business rules?
- Did I validate with the lightest proof-capable mode and word the final status honestly?
- Did I update durable context or state why it was not needed?
