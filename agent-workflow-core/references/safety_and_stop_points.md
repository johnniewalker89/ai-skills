# Safety And Stop Points

Use this reference for `project` work, destructive/hard-to-reverse goals, risky/expensive actions, unclear business rules, production-like validation assumptions, or extended sandbox validation.

## Project Gate

For `project` mode, first restore context and do safe bounded read-only reconnaissance when needed. Do not make the user approve the agent's first look at local files, metadata, existing contracts, or small bounded read-only checks when they are necessary to form a concrete proposal.

Present the following before implementation:

- current facts and restored context;
- proposed stages and ownership boundary;
- for cross-system or multi-artifact work: source/contour map, orchestration vs business-logic ownership boundary, unresolved business rules, and validation responsibilities;
- proof strategy/evidence boundary and comparison window when relevant;
- expected artifacts;
- expensive/destructive actions, if any;
- cleanup/rollback considerations;
- open questions and assumptions, with a recommended default and short impact for each business question when the evidence supports one.

For production-like data artifacts, the proof strategy/evidence boundary must say:

- evidence already collected during safe reconnaissance;
- checks still planned after approval;
- what read-only evidence can prove;
- what read-only evidence cannot prove;
- what would trigger Extended Sandbox Validation;
- what evidence/artifacts will be saved for later review;
- success criteria for the next stage.

Use this mandatory checkpoint shape for new production-like data artifacts. Keep the section labels in the task note or agent log. If a section is unknown or not applicable, include it anyway and write `unknown`, `not applicable`, or the exact blocker.

```text
Checkpoint:
- Selected sources:
- Rejected alternatives:
- Proposed grain:
- Refresh/reprocessing:
- Attribution/window semantics:
- Business semantics/open decisions:
- Expected artifacts:
- Stop-points:
- Sandbox/cleanup:

Proof strategy/evidence boundary:
- Evidence already collected:
- Checks still planned:
- What read-only proves:
- What read-only does not prove:
- Extended Sandbox Validation trigger:
- Evidence/artifacts to save:
- Success criteria:
```

After presenting the plan, stop and wait for explicit user approval such as "go", "continue", "approved", "согласен", "продолжай", or an equivalent instruction.

Do not bundle approval gates. Approval for creating repository artifacts is not approval for sandbox validation, database writes, expensive runs, commits, or pushes. If both are likely needed, ask first for the next concrete step only; after that step and its self-review/read-only validation, ask separately for sandbox/write actions.

Safe autonomous reconnaissance may include:

- local repo/source search and reading existing code/contracts;
- database metadata through `db-access`;
- small bounded `SELECT`/count/profile checks;
- lightweight equivalent queries, bounded output checks, aggregate comparisons, or invariant checks;
- bounded `EXPLAIN` or query-log checks that are not expensive and do not change state.

Stop before reconnaissance when it would require:

- writes, DDL/DML, object creation, rebuilds, recalculations, or cleanup;
- privileged/escalated access not already approved for the current task;
- broad/unbounded production scans or long-running checks;
- choosing an unclear business rule as implementation logic.

Do not start any of the following before approval:

- code edits or config edits that implement the proposed solution;
- generated validation artifacts;
- sandbox validation artifacts or database validation objects;
- commands that write, create, rebuild, or recalculate external system state;
- DDL/DML;
- long validation queries or large recalculations;
- migrations;
- destructive or hard-to-reverse actions.

Creating files that embody the proposed solution counts as implementation, even if they are temporary or validation artifacts.

## Artifact Destination

The local context workspace is for task notes, agent logs, decisions, and evidence. Do not use it as the default destination for code just because it exists.

Code artifacts such as SQL, DDL, YAML, Python, dbt models, tests, or configs belong in the target repository or target workspace that the task asks to change, following existing conventions and paths, after any required approval.

Use the context workspace for solution code only when the user explicitly asks for a design draft, review/evidence package, MR package, or context-only output, or when no target repository/workspace is part of the task.

Separate production database writes from repository edits: "no production writes" blocks database DDL/DML or other live-environment mutations, but does not automatically forbid code edits in the repo unless the user says not to touch the repo.

Never commit or push repository changes without explicit user approval for that commit/push.

The checkpoint should name the intended code destination when files will be created or edited: target repo paths, target workspace paths, or context-only draft/package.

## Extended Sandbox Validation

Use read-only validation first. If validation requires database writes, object creation, rebuilds, recalculation, or cleanup, treat it as extended sandbox validation.

Extended sandbox validation always requires explicit user approval before any sandbox action. This applies even when the target is a test schema, temporary table, local-looking dbt target, or supposedly isolated validation contour.

Before running it, define the sandbox contour, exact target set, short validation window, comparison baseline, expected artifacts, `db-access` escalation path, and cleanup/rollback plan. Then stop for explicit approval.

Approval for repository edits, read-only validation, or the abstract idea of "sandbox proof" is not approval to use privileged database tools. If the proof requires `privileged_access_mcp_*`, ask for that exact contour, action type, target set, and cleanup/rollback expectation before the first privileged call. If ordinary MCP access is down or times out, stop and ask whether to switch to the privileged contour; do not infer that switch from the outage.

## Business Rules

When business rules are unclear:

- state the uncertainty;
- offer concrete interpretations or options;
- recommend a default when local evidence, existing conventions, or the task goal make one defensible;
- explain the impact of each option when useful;
- ask only the questions that cannot be resolved from local context;
- do not turn an unchecked hypothesis into implementation logic.

## Destructive Or Hard-To-Reverse Goals

Do not make the destructive operation the default next step. First look for a safer/reversible path when one exists:

- config/MR/change request;
- dry-run;
- checker or dry-run;
- disable/quarantine instead of delete;
- backup/export/snapshot;
- staged rollout;
- read-only target validation;
- explicit rollback or cleanup procedure.

Manual destructive actions require explicit approval for:

- exact action;
- contour/environment;
- target set;
- validation evidence;
- safer alternatives considered;
- rollback/cleanup plan.

Examples of manual destructive actions:

- `DROP`;
- `DELETE`;
- `TRUNCATE`;
- removing users/roles/schemas/databases;
- removing entries from equivalent operational state.

If the user asks for a destructive outcome but a config-driven or MR-driven workflow exists, propose that safer path first. Escalate to manual destructive action only when the user explicitly approves it or when the safer path is unavailable and the user accepts the risk.

Cleanup after a proof is a separate state-changing action unless it was explicitly included in the approved target set and timing. If the user asked to leave proof objects for review, wait for a new cleanup approval.

## Approval Hygiene

Approval must be specific enough to bind the next action. If approval is vague and the action is expensive, destructive, or cross-system, restate the exact next step before acting.

If new evidence changes risk, scope, targets, or validation cost after approval, stop and update the plan.
