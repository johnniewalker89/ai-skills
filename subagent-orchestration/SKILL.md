---
name: subagent-orchestration
description: Plan, budget, coordinate and recover subagent work with approved scope, useful saved results and progress control. Use directly or from a task workflow before proposing or managing agents, including delegation discovered mid-task; ordinary single-agent work does not need it.
---

# Subagent Orchestration

## Role

- Purpose: improve result quality through bounded, explicitly approved work that adds useful evidence or an independent check of a risky result.
- Owns: delegation feasibility, role/task decomposition, model/effort selection, subagent cost forecasts and headroom, exact batch approval/retention, saved-result checkpoints, monitoring, interruption/recovery and result reconciliation.
- Delegates to: the calling task owner for context, runtime, review depth, general approval lifecycle, log settings and final delivery; domain owners for task correctness and acceptance; available tools for execution and observations. No particular workflow, navigator or private context package is required.

## Hard Gates

1. **Entry and context gate.** Activate before proposing, budgeting, launching or managing subagents, including mid-task delegation. Read `references/caller_context.md` to consume the calling task's scope, tools, destinations, log state and authorization evidence. Direct invocation uses the same contract without requiring another skill; resolve only missing inputs needed for the next action. Do not route back to a navigator or import another direction's workflow/context. A worker doing only its assigned domain task does not inherit this orchestration chain.
2. **Feasibility gate.** Read `references/planning_and_budget.md` before a proposal or material replanning. Identify a bounded question and extra proof worth the cost; verify available host controls. Choose an available model and supported reasoning setting proportionate to the task, error cost and required evidence; do not default to the parent or maximum model. Use sufficient direct checks when delegation adds no necessary value or is unavailable. Do not launch agents to estimate agent cost.
3. **Budget and measurement gate.** Estimate and control only subagents, excluding the main agent. Present their forecast, 25% headroom above its upper bound, final ceiling and time using one consistent token metric. Read `references/token_accounting.md`: before launch verify the reader's capability on existing evidence; after the approved spawn bind the new child's identity and obtain its first sample. Never require a not-yet-created child's records before spawn. Time-only control or `unknown` cannot replace required accounting. Explain a larger margin without inheriting an earlier exception; keep cache-inclusive telemetry separate as defined in `references/planning_and_budget.md`.
4. **Approval gate.** Every batch requires explicit prior user approval of tasks, count, model/effort and token/time budgets. General implementation permission is insufficient. Reuse unchanged approved scope; no automatic nested, replacement, retry or expanded launch. Test-specific bindings and access approvals remain with their respective owners.
5. **Saved-result and logging gate.** Read `references/execution_and_recovery.md` before launch or control. Plan a growing domain report, an early useful-result checkpoint and a verified write path. Apply the caller's shared agent-logs flag: only when enabled, read `references/run_logging.md`, initialize the approved attempt log before launch and maintain its facts index in the supplied storage. With logging off, no audit log/index is required; useful work results are still required. Counters, file presence and activity are not proof of useful progress.
6. **Control gate.** Verify child identity and monitor usage plus semantic progress. Inspect the first write failure or missed report checkpoint promptly. Use work → finishing → save/readback → delivery; signal finishing before the hard boundary so the child stops new research and saves findings, gaps and a continuation point. Forecast crossing alone is not interruption. Honor agreed stop/access boundaries and control latency; no automatic extension or follow-up after an immediate stop.
7. **Reconciliation gate.** Assess saved artifacts against the agreed criteria, not agent confidence. Record measured tokens and elapsed time for every attempt, compare them with the immutable forecast and effective ceilings, and save the planning lesson. Missing final counters are an unresolved accounting failure, not completed reconciliation; preserve useful work and recover the facts before closing it. Include failed-attempt cost; missing output never authorizes a restart. Return results and limits to the caller or deliver directly. Self-review is not independent review.
8. **Calibration gate.** Distinguish useful completion in headroom from an accurate base forecast. Lower headroom only after studying comparable evidence and obtaining the user's decision; one success does not establish calibration. Apply supplied local planning policy without making it a public-package dependency.
9. **Self-review gate.** Before proposal, launch, recovery or final handoff, run the Final Checklist and resolve blockers in this skill's scope.

## Workflow

1. Resolve the caller context and required proof, reusing the active task's supplied facts and resolving only material gaps.
2. Plan the smallest useful work unit, role/model, phase forecast, headroom and saved-result/control path; present the concrete batch for approval.
3. Bind the approved inputs and controls, launch only that batch, and inspect actual progress at the agreed checkpoints.
4. Preserve results before stopping. Reconcile evidence, measured subagent cost, forecast deviations and remaining work; keep missing final counters unresolved without automatic relaunch.
5. Return the scoped outcome to the calling task owner, or deliver it directly when invoked alone; follow any explicitly supplied local calibration policy.

## Reference Triggers

- `references/caller_context.md`: on entry, before planning or control, and when task scope, direction, destinations, logging or authorization evidence changes.
- `references/planning_and_budget.md`: before proposing subagents, choosing models, estimating cost, changing a batch or proposing headroom reduction.
- `references/token_accounting.md`: before launch readiness, telemetry recovery, final cost reconciliation or calibration.
- `references/counter_tools.md`: before running the bundled portable counter tools or connecting a host adapter; includes the normalized input contract and Codex adapter.
- `references/execution_and_recovery.md`: before launch, monitoring, interruption, recovery, result assessment or execution handoff.
- `references/run_logging.md`: before an approved launch or attempt-log update when the caller's shared agent logs are enabled; do not load/create templates when off.

## Final Checklist

- Caller context sufficient for the next action, with no mandatory workflow/navigator or cross-direction context import; only necessary domain/context inputs passed to each worker?
- Bounded contribution and task-proportionate model/effort chosen from available candidates; no automatic parent/maximum choice, delegated cost estimation or main-agent accounting?
- Forecast upper bound, headroom, protected save allowance and real control limits distinguished?
- Child-specific measurement verified before launch; final numeric actuals, forecast/cap deltas and planning lesson saved, or accounting failure explicitly left open?
- Exact batch approved; no unapproved nested/retry/replacement/scope expansion?
- Shared logging flag honored; when enabled, original plan and attempt events preserved outside the review tree?
- Useful first artifact and preflighted write path; semantic progress and visible errors checked before reserve?
- Agreed stops honored and available results preserved; recovery justified from evidence and remaining work?
- Acceptance and cost claims match saved proof; headroom change supported and user-decided?
