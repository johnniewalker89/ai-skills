# Attempt Logging

Read only when the caller's shared agent logs are enabled. The caller supplies
the flag, scope, parent identity, storage and history navigation through
`caller_context.md`; no particular workflow document or directory layout is
required. Do not introduce an independent mandatory log or a second opt-in. With
logging off, this template and the audit index are not created. Required
results/proof remain in their own surfaces.

## Lifecycle And Responsibility

The main orchestrator initializes one log for each approved launch attempt before
calling the launch tool, then binds the returned child identity. A failed launch,
interrupted or unsuccessful execution remains an attempt. An unlaunched proposal
is planning history, not an executed run or measured cost. If a prepared entry is
cancelled before the call, label it unlaunched and exclude it from attempt totals.
Use a unique stable run id under the real parent task/initiative, not a fixture id.

The main agent records coordination events and reconciles observed facts. The
child incrementally saves its domain report in the allowed write set; link it
rather than copying the report into the log. Update on approval/launch, useful
checkpoint, failure, finishing, delivery/stop and final reconciliation, not every
poll. Logs contain concise decisions and evidence, never hidden reasoning.

Keep the original approved plan unchanged. Append forecast/plan revisions with
time, reason, scope and approval evidence. Preserve failures and unknown telemetry.
Record the working forecast, observed phase/usage at FINISH, final total and
ceiling compliance. Final-total-minus-working-upper is diagnostic, not automatically
a forecast failure: final completion is meant to use headroom. Final-minus-last-
pre-FINISH usage is not pure save cost when it includes in-flight work or delayed
observation. Preserve the original definitions of historical approved plans.
Use `token_accounting.md` for required numerical counters and the planning lesson.
Unavailable final counts leave accounting unresolved; a completed child or a
time-only fallback cannot close it. Recover and date backfilled facts without
rewriting the original plan or claiming live monitoring retroactively.

Update the compact facts index at the caller's supplied location, outside any review tree, after the attempt, including
its outcome and evidence limits. Do not assign review/remediation status. A
configured evaluator discovers the log and covers its exact cutoff separately.
For historical backfill label reconstruction date, source evidence and unknowns;
never invent approvals, original forecasts or a contemporaneous event sequence.

## Compact Facts Index

Keep one short row per actual attempt in the caller's direction-specific index:
run/log and result links; task class/output scope; model/effort/host; required input
and delivery method; original forecast and cap in the named token metric and time;
actual tokens/time; delivered/partial/stopped/failed outcome and evidence limits.
Keep lifecycle delivery separate from task acceptance and accounting completeness.
Unknown historical fields stay `unknown`; do not infer startup cost from total cost.
Index rows contain facts, not coordination narratives or current remediation status.
Put append-only detail in the attempt log. Preserve older index versions when
compacting them, with reconstruction date/source cutoff. An empty index is valid:
use the no-history procedure rather than making historical backfill a launch gate.

The planning procedure reads this index once and only a few selected logs. Keep
source evidence linked so a future reader need not rediscover or reread all runs.

## Attempt Template

```markdown
# <run-id> — <bounded task>

## Identity
- Parent: <stable task/initiative key and snapshot link>
- Run id / child id: <id / pending until launch, or unavailable with reason>
- Role / scope / fixture: <question, allowed outputs/access, optional input case>
- Task class / input delivery: <bounded output; mandatory envelope/reads; inline/path/fork; known input size or unknown>
- Source / model / effort / host: <exact revision/configuration or unknown>
- Model choice: <task/proof needs, sufficient model/effort and relevant available alternatives>
- Logging: <shared flag and enabled scope; evidence of user request>

## Original Plan And Approval — immutable
- Forecast: <token range; elapsed-time range>
- Basis: <selected comparable attempt IDs and differences, or uncalibrated bottom-up assumptions>
- Phases: <startup + useful work + save/readback/delivery ranges; save counted once>
- Metric: <definition and cached-input treatment; main excluded>
- Headroom: <percentage and added tokens/time>
- Approved ceiling: <tokens/time per run; applicable additional explicit cap>
- Completion reserve: <tokens/time within ceiling; finish signal and latency>
- Completion protection: <phase observation/latch and final dispatch guard; any save overrun reported against original cap>
- Checkpoint: <first useful report path, when inspected, acceptance criteria>
- Approval: <exact batch/count/model/input/limits and user reply evidence>

## Events — append only
| Observed time / event time if different | Event / state | Evidence and decision |
| --- | --- | --- |
| <time> | <launch/checkpoint/failure/finishing/save/stop/revision> | <facts/link> |

## Result And Plan Versus Actual
- Outcome: <delivered/partial/failed/stopped/unlaunched; scope of usable result>
- Result / evidence / gaps: <durable links and limits>
| Measure | Original forecast | Approved ceiling | Actual | Delta from original upper forecast | Cap compliance |
| --- | --- | --- | --- | --- | --- |
| <primary token metric> | <range> | <cap> | <actual/unknown> | <signed delta/unknown> | <met/exceeded/unknown> |
| Elapsed time | <range> | <cap> | <actual/unknown> | <signed delta/unknown> | <met/exceeded/unknown> |
- Diagnostic telemetry: <separate from spending budget; availability/cutoff>
- Planning lesson: <cause of material deviation, phase to adjust, remaining uncertainty; no automatic headroom reduction>
- Continuation: <saved point, remaining work, cause of failure; no automatic retry>
```
