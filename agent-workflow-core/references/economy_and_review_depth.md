# Economy And Review Depth

Read for enhanced review, subagents or a cost comparison. Ordinary delivery uses
the short economy gate in SKILL.md without loading this reference.

## Navigation

- [Proof and assessor](#choose-the-proof)
- [Models, budgets and approval](#propose-before-any-subagent-launch)
- [Execution and assessment](#run-and-reconcile)
- [Cost comparison](#compare-cost-without-reducing-proof)

## Choose The Proof

Keep the task mode unchanged. Normal review covers the outcome and all mandatory
owner checks. Enhanced review adds a distinct way to challenge an important claim.
Use it for high error cost, shared contracts, interacting components, substantial
uncertainty, a need for independent checking or an explicit user request.

Name the specific risk and the extra evidence expected. A different oracle, an
independent calculation or a reviewer can help; merely rereading the same result
or counting agent agreement does not establish independence. If the proposed
check is unavailable, report the missing proof instead of claiming enhancement.

Before execution, name the domain acceptance criteria, required artifacts, who
will assess them and how. The domain owner defines sufficient proof; workflow
arranges assessment and reconciles the result. The main agent may assess in a
separate pass, disclosing when it also authored the work. An independent reviewer
is an optional additional role unless required by the task, not an automatic
extra launch. A different model or a fresh agent alone does not prove independence.

## Propose Before Any Subagent Launch

Use the current host's available delegation tools, models/settings, isolation,
usage reporting and stop controls. Reuse known capabilities; discover only gaps.
Keep host-specific commands and chosen model IDs in local configuration or the
approved plan. Mark unsupported controls as unavailable, not as configured limits.
If delegation is unavailable, perform the available domain checks directly and
report any missing independent proof. Self-review is not an independent reviewer;
leave acceptance open when that reviewer is required. Enhanced review may still
use a different independent method if it provides the required evidence.

Select a model and supported reasoning setting for each role from task difficulty,
error cost, evidence/context needs and available capabilities. Parent, executor
and reviewer may use different models. Prefer the least expected subagent cost
that can meet the same quality criteria, including likely subagent rework and review;
do not impose a fixed model across roles or hosts.
Explain the choice from available evidence; mark an uncalibrated choice uncertain.

The main agent estimates subagent cost itself; do not delegate tariff/budget
estimation. This procedure covers only launched subagents: do not estimate,
meter, budget or report the main agent's own usage, including coordination or
assessment, and never use it as a subagent stop condition.
For each subagent include startup/context, execution, likely recovery and saving
an assessable result; include a separately launched reviewer in the approved batch.
Use comparable model/settings, host, role/task and input/cache observations;
give a justified range and assumptions, with uncertainty where data is missing.
Retain failed subagent-attempt cost in actual totals; estimate remaining work separately.
Keep token metrics distinct from subscription/pricing units across models/hosts.
Do not infer another model's price or subscription savings from token counts.

Separate the subagent forecast from the user-approved expenditure/time ceiling and from
a diagnostic checkpoint. State whether each control is enforced or estimated;
never relabel an agreed stop as a warning during a run. Include a completion
reserve inside each applicable subagent ceiling for its output and required checks.
Before proposing delegation, compare sufficient existing/direct checks with the
subagent's expected extra proof and budget. If a useful result is unlikely to fit,
reduce the work unit or change the approach before requesting a launch; a smaller
unit proves only its declared scope and cannot waive required independent proof.

Every subagent requires prior explicit user approval, including read-only review,
focused smoke, exploration and nested delegation. General permission to complete
the task is not approval for a batch. No launching while waiting for an answer.

Present one concrete batch:

- Questions/tasks and roles; scope, input revision and permitted outputs/access;
  assessment owner/method, required evidence and any additional reviewer launch.
- Number of launches, supported models and reasoning settings, including any
  child agents or planned retries; disclose inherited or unavailable settings.
- Token budget per subagent and total for the batch with the metric defined
  (including cached-input treatment), elapsed-time cap and replay allowance. Distinguish
  forecast, approved ceilings, completion reserve and diagnostic/stop triggers;
  disclose enforcement and telemetry latency. Do not convert tokens into
  subscription percentages without comparable telemetry.
- Expected contribution to quality and a stopping criterion.

Record the user's reply and its exact batch. Reuse it for the unchanged approved
steps without asking again. New/nested/replacement/retry launches outside the
batch, changed questions/models/inputs or increased count/budget require another
approval. No automatic expansion after a failure or because budget remains.
Ordinary domain review uses only its domain owners, without skill-development
test or evaluation dependencies. When testing skills themselves, the validation
owner adds profile, exact input/plan hashes and isolation to this same approval;
it does not introduce a second generic approval procedure.

## Run And Reconcile

Give each approved agent a bounded question, the minimum sufficient raw evidence
and the owners needed for that question. Do not prescribe the conclusion.
Preserve the active direction's context, access limits and authorized write boundary.

Prepare and verify the subagent monitor/baseline before launching the subject.
Use proportionate control: cheap counters or batched local sampling where available,
without a new main-agent inference per sample when the tool can handle it. Missing
telemetry is unknown, not zero; agree a bounded fallback or stop before launch.
Avoid using a recoverable sampling delay as a stop trigger by default.

At a diagnostic checkpoint, check progress, remaining cost and all applicable
ceilings. A late but valid sample alone does not require discarding a useful run;
continue only when the agreed controls and remaining budget support completion.
Honor explicit stops and access boundaries. If remaining work no longer fits,
stop starting new work and use the reserved allowance to save available evidence
and its gaps before the ceiling. Reserve is not extra authorization: no follow-up
after an agreed immediate stop, no unapproved launch and no spending past a cap.

For long interruptible work, save reusable evidence at natural boundaries within
the allowed outputs; keep short tasks and closeout lightweight. After interruption,
assess saved artifacts first. Before proposing another attempt, identify the cause,
what can be reused and a credible remaining-cost path to the required result.
Already spent tokens neither justify continuation nor make a restart economical.

Apply the agreed criteria to actual artifacts and relevant execution evidence,
not only an agent's final claim or confidence. Check findings against source/repro
artifacts; reject unsupported suggestions and reconcile disagreements by evidence.
The main agent owns the final decision. Record accepted/rejected findings, proof
gained, gaps and actual/unknown subagent cost separately. Include resolved executor/reviewer
models/settings, host and input revision where known; mark unknowns explicitly.
Limit conclusions to that configuration and evidence; one successful run does not
prove reliability on every model, host or task. Low cost never upgrades weak proof.

## Compare Cost Without Reducing Proof

Compare the same subagent scenario and required checks before/after. Within
subagent sessions count discovery, loaded instructions, tool schemas/results,
repeated calls and output. Save full necessary evidence once and link
its compact result; don't reread it without an input/state/freshness/risk reason.

Report text/bytes/calls as proxies and tokens only when measured. Neither a
shorter SKILL.md nor fewer calls proves subscription savings or reliability.
Never hide missed pages, failed checks or unproven claims to fit a budget.
