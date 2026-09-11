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
Record actuals, original forecast delta and compliance with each effective cap;
successful delivery in headroom does not make the base forecast accurate.

Update the compact facts index at the caller's supplied location, outside any review tree, after the attempt, including
its outcome and evidence limits. Do not assign review/remediation status. A
configured evaluator discovers the log and covers its exact cutoff separately.
For historical backfill label reconstruction date, source evidence and unknowns;
never invent approvals, original forecasts or a contemporaneous event sequence.

## Template

```markdown
# <run-id> — <bounded task>

## Identity
- Parent: <stable task/initiative key and snapshot link>
- Run id / child id: <id / pending until launch, or unavailable with reason>
- Role / scope / fixture: <question, allowed outputs/access, optional input case>
- Source / model / effort / host: <exact revision/configuration or unknown>
- Logging: <shared flag and enabled scope; evidence of user request>

## Original Plan And Approval — immutable
- Forecast: <token range; elapsed-time range>
- Metric: <definition and cached-input treatment; main excluded>
- Headroom: <percentage and added tokens/time>
- Approved ceiling: <tokens/time per run; applicable additional explicit cap>
- Completion reserve: <tokens/time within ceiling; finish signal and latency>
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
- Continuation: <saved point, remaining work, cause of failure; no automatic retry>
```
