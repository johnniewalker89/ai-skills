# Planning And Budget

Read before proposing, budgeting or materially replanning subagents.

Delegation must add evidence or a useful independent check of a risky result.
Two agents reaching the same conclusion without checking different evidence do
not establish quality. Ordinary review stays with its domain owners; skill-test
and evaluation machinery is not a prerequisite for a domain reviewer.

## Navigation

- [Host and roles](#host-and-roles)
- [Forecast and headroom](#forecast-and-headroom)
- [Explain the budget](#explain-the-budget)
- [Approve the batch](#approve-the-batch)
- [Compare cost](#compare-cost-without-reducing-proof)

## Host And Roles

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

## Forecast And Headroom

The main agent estimates subagent cost itself; do not delegate tariff/budget
estimation. This procedure covers only launched subagents: do not estimate,
meter, budget or report the main agent's own usage, including coordination or
assessment, and never use it as a subagent stop condition.
For each subagent estimate startup/context, task execution, and saving/checking
an assessable result separately, including likely recovery. Count the actual
host envelope and required skill/input reads; a short user request is not a short
subject context. Include a separately launched reviewer in the approved batch.
Use comparable model/settings, host, role/task and input/cache observations;
give a justified range and assumptions, with uncertainty where data is missing.
Make one short planning pass over the available compact summary and a few close
successes and failures. If evidence is sparse, mark uncertainty and size the
work accordingly; do not turn estimation into an archive investigation. Account
for startup, useful work and saving, then stop estimating. Additional history
research is justified only by a material unresolved decision.
Retain failed subagent-attempt cost in actual totals; estimate remaining work separately.
Keep token metrics distinct from subscription/pricing units across models/hosts.
Do not infer another model's price or subscription savings from token counts.

Separate the subagent forecast from the user-approved expenditure/time ceiling and from
a diagnostic checkpoint. State whether each control is enforced or estimated;
never relabel an agreed stop as a warning during a run. Include a completion
reserve inside each applicable subagent ceiling for its output and required checks.
Start every new subagent budget with **25% uncertainty headroom above the upper
forecast**, for both tokens and elapsed time; add it before launch, not only after
a failure: ceiling = upper forecast × (1 + headroom), rounded upward when needed.
Crossing the base upper forecast is a diagnostic event, not an interrupt trigger.
Use the enlarged gap to finish and preserve the result; plan the finish signal,
save window and stop against the padded ceiling, with enough allowance for writes
and observed control latency. Propose more upfront when calibration, scope, host or write path is
uncertain, and state the reason. A higher margin is a specific proposal requiring
the user's agreement, not a new default or an exception inherited by later batches.
Show the base forecast, percentage, added amount
and final ceiling separately; headroom is not expected consumption. Respect an
explicit user cap by fitting the work unit inside it, never silently increasing it.

Study comparable completed work before proposing less headroom. Separate
delivery success from forecast accuracy: a useful result completed in headroom
is valuable, but does not validate the original upper forecast. Consider failures,
missing observations, saved-result checkpoints and near-stop completions too.
Keep the current allowance until an evidence-backed reduction is explicitly
accepted by the user; one success or a new task/model/host cohort is insufficient.
Apply any supplied local calibration policy within its scope.

Keep completion work in the phase forecast and its protected reserve inside the
ceiling; do not count it twice. Headroom never delays the first useful-artifact
checkpoint or authorizes spending through an unresolved failure. A larger ceiling
still needs exact user approval; the active run's limits do not grow automatically.
Before proposing delegation, compare sufficient existing/direct checks with the
subagent's expected extra proof and budget. If a useful result is unlikely to fit,
reduce the work unit or change the approach before requesting a launch; a smaller
unit proves only its declared scope and cannot waive required independent proof.

## Explain The Budget

Use one consistent primary metric in proposals and result summaries. Show the
subagent count/tasks, expected range in thousands of tokens, added headroom,
final ceiling and time; say explicitly that the main agent is excluded. For
example, an upper forecast of 60 thousand plus 25% (15 thousand) gives a ceiling
of 75 thousand. Do not lead with unexplained telemetry symbols or switch from
this metric to a cache-inclusive total when comparing runs.

Define the primary metric and cached-input treatment in the technical plan. Where
available, uncached input plus output preserves the existing planning convention;
it is not a billing price or proof that cached input is free. Cumulative input
including cached/repeated context remains diagnostic telemetry by default, not a
second spending budget or hidden stop. Use an additional stop only for a concrete
need, explaining its meaning and basis in the same user approval. Preserve old
explicitly approved controls; changing presentation does not change active limits.

The orchestration owner selects the budget and calibration evidence. Test owners
add profile, input/evidence bindings and subject/replay constraints to this one
proposal; they do not choose a competing time allowance or a second approval.
Do not split a batch merely to fit a profile's arbitrary time default.

## Approve The Batch

Every subagent requires prior explicit user approval, including read-only review,
focused smoke, exploration and nested delegation. General permission to complete
the task is not approval for a batch. No launching while waiting for an answer.

Present one concrete batch:

- Questions/tasks and roles; scope, input revision and permitted outputs/access;
  assessment owner/method, required evidence, first saved-result checkpoint and
  any additional reviewer launch.
- Number of launches, supported models and reasoning settings, including any
  child agents or planned retries; disclose inherited or unavailable settings.
- Token budget per subagent and total for the batch with the metric defined
  (including cached-input treatment), elapsed-time cap and replay allowance. Distinguish
  forecast, uncertainty headroom, approved ceilings, completion reserve and diagnostic/stop triggers;
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

Keep the original forecast, reserve, metric and approved ceiling immutable.
Record later revisions as dated events, with their reason and any required new
approval; compare actuals against the original plan as well as the effective cap.
When shared agent logs are enabled, keep this record in the attempt log using
`run_logging.md`; otherwise retain the necessary approval/result evidence in the
existing task or test surface without creating an audit log or index.

## Compare Cost Without Reducing Proof

Compare the same subagent scenario and required checks before/after. Within
subagent sessions count discovery, loaded instructions, tool schemas/results,
repeated calls and output. Save full necessary evidence once and link
its compact result; don't reread it without an input/state/freshness/risk reason.

Report text/bytes/calls as proxies and tokens only when measured. Neither a
shorter SKILL.md nor fewer calls proves subscription savings or reliability.
Never hide missed pages, failed checks or unproven claims to fit a budget.
