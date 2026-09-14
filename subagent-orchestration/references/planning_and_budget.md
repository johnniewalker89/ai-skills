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
Before launch readiness, follow `token_accounting.md` to verify measurement;
an estimate or agreed time-only fallback cannot replace numerical actuals.
Keep host-specific commands and chosen model IDs in local configuration or the
approved plan. Mark unsupported controls as unavailable, not as configured limits.
If delegation is unavailable, perform the available domain checks directly and
report any missing independent proof. Self-review is not an independent reviewer;
leave acceptance open when that reviewer is required. Enhanced review may still
use a different independent method if it provides the required evidence.

Use the model/setting options already exposed by the current environment;
discover only a missing capability needed for the decision. For each role choose
a model and supported reasoning setting proportionate to task complexity, error
cost and required evidence. The child may be weaker or stronger than the parent.
Prefer the least expected cost that can meet the quality criteria, including
likely rework and review; neither the parent/maximum nor the cheapest model is
an automatic choice. Briefly explain why the selected configuration is sufficient
compared with relevant available alternatives. Keep uncertainty explicit when
comparable quality/cost evidence is missing. No generation classification or
predecessor lookup is required. Respect explicit user/project model restrictions.

## Forecast And Headroom

The main agent estimates subagent cost itself; do not delegate tariff/budget
estimation. This procedure covers only launched subagents: do not estimate,
meter, budget or report the main agent's own usage, including coordination or
assessment, and never use it as a subagent stop condition.
Use the fixed procedure below; do not invent a new estimation workflow per task.
Include a separately launched reviewer as its own work unit in the same batch.
Retain failed subagent-attempt cost in actual totals; estimate remaining work separately.
Close each attempt's accounting with measured actuals, original forecast/cap
deviations and a supported lesson for the next forecast. Missing final counts
remain an unresolved accounting failure, including after useful delivery.
Keep token metrics distinct from subscription/pricing units across models/hosts.
Do not infer another model's price or subscription savings from token counts.

Separate the working forecast, completion allowance, approved ceiling and
diagnostic checkpoint. The base forecast covers startup and useful work, including
incremental saves. Final save/readback/delivery and control latency use the added
**25% headroom above the working upper bound**, independently for tokens and time:
ceiling = working upper ×1.25. Keep both numbers visible; respect an explicit user
cap by fitting the work unit inside it, never silently increasing it.

Set budget-driven FINISH at the working upper bound. Reaching it ends new research
and starts completion; it never interrupts saving. Earlier checkpoints assess
progress and remaining work. Do not move FINISH towards the lower bound to reserve
completion a second time. A missing draft alone does not exhaust the work window.
Natural completion or a concrete blocker/failed path can justify earlier finishing;
record that reason rather than presenting it as ordinary budget exhaustion.

Check that the added allowance covers final writes/readback and the largest plausible
unobserved request/counter jump. If not, reduce the output scope or explicitly
propose a larger margin before approval. Do not fund a too-small allowance by
silently subtracting it from the working range. Protected completion may still
overrun: retain the original ceiling, preserve the result and report actuals.

Place the first useful checkpoint after plausible startup plus one small proof
cycle and before FINISH. If those cannot fit, narrow the work unit before approval.
During execution a missed checkpoint asks for diagnosis and an incremental save;
continue useful work while it fits below the working upper bound. Headroom does
not authorize new research during finishing or continuation through an access stop.

Study comparable completed work before proposing less headroom. Assess working
phase accuracy, completion cost and total compliance separately; completion in
headroom is expected, not automatically a working-forecast miss. Retain failures,
missed checkpoints and near-ceiling deliveries. Apply supplied local calibration
policy; no reduction without evidence and an explicit user decision. A larger
margin also needs specific agreement and is not inherited from earlier exceptions.

Before proposing delegation, compare sufficient existing/direct checks with the
subagent's expected extra proof and budget. If a useful result is unlikely to fit,
reduce the work unit or change the approach before requesting a launch; a smaller
unit proves only its declared scope and cannot waive required independent proof.

## One-Pass Estimation Procedure

1. **Result first.** State the extra proof needed, acceptance criteria and smallest
   independently useful output. Compare with sufficient direct checks. Name the
   task class (classification, document review, evidence review, implementation),
   allowed files/tools and a finite stopping point. Split unrelated questions.
2. **Inventory the actual input.** List the inherited host envelope, mandatory
   skills, raw task evidence and delivery method (inline, paths, snapshot/fork).
   Inspect sizes/metadata already available; avoid reading an archive to price it.
   Bound tool-result volume and likely read/check/write cycles. A short prompt
   with a large inherited context is not a cheap startup.
3. **Choose a sufficient available model/effort.** Use complexity, error cost and
   evidence requirements, including likely rework. The next steps estimate this
   configuration; another model's token count is not its price or proven cost.
4. **Use evidence when comparable.** Read one compact facts index, selecting at
   most three close attempts plus a relevant failure if useful. Match task class,
   output completeness, model/effort/host and input delivery before comparing cost.
   Adjust for the actual differences; document review is not a classification
   baseline. Partial/stopped runs are lower-bound or failure evidence, never a
   completed-task price. Read a selected log only if a missing fact changes the
   decision. No suitable cohort, or one unresolved lookup: use the fallback below.
5. **Estimate work and completion.** Sum startup and useful-work token/time
   ranges for the working forecast. Estimate final save/readback/delivery separately
   to check that it fits the added25% with control latency; do not sum it into the
   working forecast or subtract it again from FINISH. Set finish_u/finish_seconds
   to the corresponding working upper bounds, stop_u/stop_seconds to the padded
   ceilings. Place a diagnostic checkpoint after startup plus one small useful
   cycle and before FINISH. Use the actual read envelope, not prompt length alone.
   If useful work cannot fit, narrow the input/question; if completion cannot fit
   the added allowance, reduce output or propose a larger margin before approval.
6. **Stop estimating.** Present the single batch card below. Unknowns change the
   range or work unit, not the length of a planning investigation. A material gap
   that prevents a useful bounded result is a reason to avoid that delegation.

### When No Comparable Runs Exist

Use a bottom-up, explicitly **uncalibrated** estimate; historical runs are optional.
Reuse a known tokenizer/measurement method if already available. Otherwise label
text-volume estimates approximate; bytes, words and elapsed time are not measured
tokens. Do not install tooling or launch an agent solely to price this attempt.

| Phase | Derive the range from |
| --- | --- |
| Startup | Required host/skill/task input delivered to the child, first bounded reads and their outputs. State cache assumptions; include a cold-input scenario when cache is unknown. |
| Useful work | A finite number of inspect/compare/check cycles, expected context/input per cycle and bounded output. State the cycle-count assumption and one plausible repair; do not silently assume unlimited research or perfect first-pass execution. |
| Save/readback/delivery | Size and count of required artifacts, serialization/write calls, necessary readback and final message, plus a plausible write repair and control latency. |

Estimate elapsed time independently from expected tool/write waits and comparable
host latency where known; do not convert tokens to seconds with an invented rate.
Without latency evidence give a coarse uncertain range and a small useful work
unit. An early saved checkpoint tests the assumptions; it does not retroactively
make the original estimate measured. Explain the numerical assumptions briefly,
without presenting universal per-task or per-model constants as calibrated facts.

Example: working30–50k plus25% gives FINISH at50k and a62.5k ceiling. A30k
checkpoint reviews progress; absent a concrete blocker it leaves work running.
The12.5k gap funds final saving/readback/delivery and control latency. Apply the
same calculation independently to time; early natural completion remains valid.

### Compact Batch Card

For each role retain: question/output and scope; model/effort and reason; input
inventory/delivery; selected attempt IDs or `uncalibrated`; startup/work/save
ranges and assumptions; summed base forecast; primary metric; headroom and cap;
first useful checkpoint; finish threshold/control latency; protected completion
and numerical overrun accounting. Keep the user-facing explanation compact and
put supporting details in the existing plan, not a separate estimation report.

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
