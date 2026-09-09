---
name: agent-workflow-core
description: Run non-trivial Engineering tasks with task modes, saved context, exact local runtimes, retained approvals, proportionate proof and final delivery. Use before domain work; select normal or enhanced review without changing task mode.
---

# Agent Workflow Core

## Role

- Purpose: deliver Engineering work with enough evidence and the least necessary overhead.
- Owns: mode, context/environment/runtime, task snapshots, optional logs, planning, approval acquisition/retention, review depth, subagent model selection and approved coordination, subagent cost estimation/control by the main agent, quality-assessment handoff, proof framing and final delivery.
- Delegates to: the selected research owner for material external gaps; domain owners for correctness; operational owners for action/identity/session policy, execution and readback.

## Hard Gates

1. **Task mode gate.** Choose exactly one mode: `quick`, `focused`, `project`, `investigation`, `review`. For non-tiny work start with Режим: followed by the mode in backticks; put descriptive labels after that sentence. Correct an invalid mode before continuing. Choose by risk, scope, uncertainty, validation and rollback cost.
2. **Context bootstrap gate.** Restore context before continuing an established task or when a task id, durable-context request or enabled logging requires it. Otherwise create no durable context by default. Read `references/context_and_decisions.md` for restore/runtime and `references/context_maintenance.md` before durable writes. Ordinary delivery must not create, update, or reconcile a task-log review row or write anywhere in a configured skill-review/evaluation tree; a separate evaluator owns that tree.
3. **Local runtime resolution gate.** Before the first local runtime-backed command, including an incidental helper or validator, resolve the exact command/runtime from configured environment. Prefer the target repo/project runtime over a generic validation runtime; never probe or invoke an alias recorded as unavailable or forbidden. Discover only missing mappings.
4. **Agent-log gate.** Append an agent log only when explicitly requested or already enabled, inside the established context workspace. A task id alone does not enable logging.
5. **Owner and access gate.** Hand material external-context gaps to the selected research owner. Direct database/catalog MCP uses `db-access`; a separate typed runtime read requires its dedicated access owner and complete SQL chain. Never use raw database commands over SSH or an unavailable/denied contour as fallback authorization.
6. **Approval lifecycle gate.** Preserve explicit user intent and already granted authorization under instruction priority. The selected operational owner defines exact actions, sessions, identity, freshness, scope changes and readback. Prepare a concrete result before asking when approval is required; do not create a parallel action policy or ask again inside unchanged authorized scope. Client settings, full access and agent-supplied flags are not user consent. Scope expansion and expired or drifted bindings return to the owner.
7. **Project and artifact gate.** For project, production-like data artifacts, risky/destructive work, cleanup or unclear business rules, read `references/safety_and_stop_points.md` before the dependent step. Safe bounded reconnaissance may precede a concrete proposal. Retain existing implementation approval; separate repo artifacts from sandbox/database writes. Put code in the target repo, context in the configured memory workspace.
8. **Proof gate.** Read `references/validation_and_review.md` before selecting proof or delivering non-quick work. Domain owners determine sufficient evidence; budget never permits skipping it or overstating readiness. P1/P2 owner blockers prevent the dependent pass.
9. **Economy gate.** Reuse sufficient current evidence and already loaded instructions. Repeat a read/check only for changed inputs/state, incomplete evidence, freshness or a new risk; retain identity, permission and mandatory post-change readback. Select bounded tool results and inspect all required pages without silently dropping evidence.
10. **Review depth and subagents gate.** Depth is `normal` or `enhanced`, independent of task mode. Read `references/economy_and_review_depth.md` for enhanced review, any subagent proposal/launch or cost comparison; resolve host capabilities and unavailable-review limits there. Every subagent batch requires prior explicit user approval of tasks, count, models/effort and token/time budgets; general implementation approval never covers it. No automatic nested, replacement or expanded launches.
11. **Self-review gate.** Before final delivery or handoff, run the Final Checklist; fix owner blockers or state their effect on completion.

## Workflow

1. Restore only the context needed for the current decision; announce the minimal owner chain.
2. Confirm outcome, risks, approved scope and proof criteria. For focused work continue; for project work obtain missing approval only after the proposal is concrete.
3. Implement with the responsible owners. Keep uncertainty explicit; if new evidence changes a material boundary, update the plan.
4. Select the smallest proof-capable check set; inspect results and stop repeating unchanged green layers.
5. Update enabled snapshots/logs with decisions, exact evidence and unresolved work. Report result, strongest proof, limits and next required step concisely in the user's language.

## Reference Triggers

- `references/task_modes.md`: when mode choice is unclear.
- `references/context_and_decisions.md`: before established-task restore or environment/runtime lookup.
- `references/context_maintenance.md`: before creating/updating context, environment notes, task snapshots or enabled logs; not for read-only restore.
- `references/context_templates.md`: only when creating a context workspace/map, task snapshot or log from a template.
- `references/safety_and_stop_points.md`: before project checkpoints, new data artifacts, destructive cleanup, sandbox work or unresolved business decisions.
- `references/validation_and_review.md`: before proof selection, non-quick final delivery or readiness claims.
- `references/data_artifact_proof.md`: before SQL/dbt/data-pipeline or production-like proof selection/checkpoints.
- `references/economy_and_review_depth.md`: before enhanced review, proposing/launching subagents or comparing work cost.

## Final Checklist

- Valid mode, minimal complete owner chain, and exact configured mapping before runtime commands?
- Context/log updates inside the enabled workspace; zero writes under the configured skill-review/evaluation tree during ordinary delivery?
- Existing approval retained, concrete missing approval obtained, and operational scopes/bindings honored?
- Code destination, business assumptions and cleanup/use evidence resolved?
- All subagent launches inside the explicitly approved batch and budgets?
- Sufficient evidence reused, required checks/readback retained, owner blockers fixed or disclosed?
- Final claim matches actual proof; unresolved work and material self-review result visible?
