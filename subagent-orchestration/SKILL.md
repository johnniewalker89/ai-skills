---
name: subagent-orchestration
description: Plan, budget, coordinate and recover Engineering subagent work with approved scope, useful saved results and progress control. Use with agent-workflow-core before proposing or managing agents, including delegation discovered mid-task; ordinary single-agent work does not need it.
---

# Subagent Orchestration

## Role

- Purpose: improve result quality through bounded, explicitly approved work that adds useful evidence or an independent check of a risky result.
- Owns: delegation feasibility, role/task decomposition, model/effort selection, subagent cost forecasts and headroom, exact batch approval/retention, saved-result checkpoints, monitoring, interruption/recovery and result reconciliation.
- Delegates to: `agent-workflow-core` for task context, runtime resolution, review depth, general approval lifecycle and final delivery; domain owners for task correctness and acceptance; configured tools for execution and observations.

## Hard Gates

1. **Entry gate.** Use `agent-workflow-core` as the companion. Direct invocation works without a navigator; if workflow already selected this skill, continue without routing back. Activate before proposing, budgeting, launching or managing subagents, including mid-task delegation. A worker doing only its assigned domain task does not inherit this orchestration chain.
2. **Feasibility gate.** Read `references/planning_and_budget.md` before a proposal or material replanning. Identify a bounded question and extra proof worth the cost; verify available host controls. Use sufficient direct checks when delegation adds no necessary value or is unavailable. Do not launch agents to estimate agent cost.
3. **Budget gate.** Estimate and control only subagents, excluding the main agent. Present their forecast, 25% headroom above its upper bound, final ceiling and time in plain language using one consistent token metric. Explain and obtain agreement for any larger margin; do not inherit an earlier exception. Keep cache-inclusive telemetry separate from the user budget and honor the detailed contract in `references/planning_and_budget.md`.
4. **Approval gate.** Every batch requires explicit prior user approval of tasks, count, model/effort and token/time budgets. General implementation permission is insufficient. Reuse unchanged approved scope; no automatic nested, replacement, retry or expanded launch. Test-specific bindings and access approvals remain with their respective owners.
5. **Saved-result and logging gate.** Read `references/execution_and_recovery.md` before launch or control. Plan a growing domain report, an early useful-result checkpoint and a verified write path. Apply workflow's shared agent-logs flag: only when enabled, read `references/run_logging.md`, initialize the approved attempt log before launch and maintain its facts index. With logging off, no audit log/index is required; useful work results are still required. Counters, file presence and activity are not proof of useful progress.
6. **Control gate.** Verify child identity and monitor usage plus semantic progress. Inspect the first write failure or missed report checkpoint promptly. Use work → finishing → save/readback → delivery; signal finishing before the hard boundary so the child stops new research and saves findings, gaps and a continuation point. Forecast crossing alone is not interruption. Honor agreed stop/access boundaries and control latency; no automatic extension or follow-up after an immediate stop.
7. **Reconciliation gate.** Assess saved artifacts against the agreed criteria, not agent confidence. Preserve failed-attempt cost and evidence limits; missing output does not authorize a restart. Workflow owns final delivery and proof wording; self-review is not independent review.
8. **Calibration gate.** Distinguish useful completion in headroom from an accurate base forecast. Lower headroom only after studying comparable evidence and obtaining the user's decision; one success does not establish calibration. Apply supplied local planning policy without making it a public-package dependency.
9. **Self-review gate.** Before proposal, launch, recovery or final handoff, run the Final Checklist and resolve blockers in this skill's scope.

## Workflow

1. Restore the task's scope and required proof through workflow. Resolve only missing host/configuration facts.
2. Plan the smallest useful work unit, role/model, phase forecast, headroom and saved-result/control path; present the concrete batch for approval.
3. Bind the approved inputs and controls, launch only that batch, and inspect actual progress at the agreed checkpoints.
4. Preserve results and gaps before stopping. Reconcile evidence, actual/unknown subagent cost and any remaining work without automatic relaunch.
5. Return the scoped outcome to workflow for delivery; follow any explicitly supplied local calibration policy.

## Reference Triggers

- `references/planning_and_budget.md`: before proposing subagents, choosing models, estimating cost, changing a batch or proposing headroom reduction.
- `references/execution_and_recovery.md`: before launch, monitoring, interruption, recovery, result assessment or execution handoff.
- `references/run_logging.md`: before an approved launch or attempt-log update when workflow's shared agent logs are enabled; do not load/create templates when off.

## Final Checklist

- Workflow companion active without a routing loop; only necessary domain/context inputs passed to each worker?
- Bounded contribution, model/effort and available controls justified; no delegated cost estimation or main-agent accounting?
- Forecast upper bound, headroom, protected save allowance and real control limits distinguished?
- Exact batch approved; no unapproved nested/retry/replacement/scope expansion?
- Shared logging flag honored; when enabled, original plan and attempt events preserved outside the review tree?
- Useful first artifact and preflighted write path; semantic progress and visible errors checked before reserve?
- Agreed stops honored and available results preserved; recovery justified from evidence and remaining work?
- Acceptance and cost claims match saved proof; headroom change supported and user-decided?
