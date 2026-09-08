# Economy And Review Depth

Read for enhanced review, subagents or a cost comparison. Ordinary delivery uses
the short economy gate in SKILL.md without loading this reference.

## Choose The Proof

Keep the task mode unchanged. Normal review covers the outcome and all mandatory
owner checks. Enhanced review adds a distinct way to challenge an important claim.
Use it for high error cost, shared contracts, interacting components, substantial
uncertainty, a need for independent checking or an explicit user request.

Name the specific risk and the extra evidence expected. A different oracle, an
independent calculation or a reviewer can help; merely rereading the same result
or counting agent agreement does not establish independence. If the proposed
check is unavailable, report the missing proof instead of claiming enhancement.

## Propose Before Any Subagent Launch

Every subagent requires prior explicit user approval, including read-only review,
focused smoke, exploration and nested delegation. General permission to complete
the task is not approval for a batch. No launching while waiting for an answer.

Present one concrete batch:

- Questions/tasks and roles; scope, input revision and permitted outputs/access.
- Number of launches, proposed models and reasoning effort, including any child
  agents or planned retries. Resolve what the host actually supports.
- Token budget per task and total, elapsed-time cap, replay allowance and whether
  each limit is tool-enforced or an estimate. Include coordination/review cost;
  do not convert tokens into subscription percentages without comparable telemetry.
- Expected contribution to quality and a stopping criterion.

Record the user's reply and its exact batch. Reuse it for the unchanged approved
steps without asking again. New/nested/replacement/retry launches outside the
batch, changed questions/models/inputs or increased count/budget require another
approval. No automatic expansion after a failure or because budget remains.
For skill subjects, the validation owner adds exact input/plan hashes and its
isolation contract; this reference is not an alternate test harness.

## Run And Reconcile

Give each approved agent a bounded question, the minimum sufficient raw evidence
and the owners needed for that question. Do not prescribe the conclusion. Keep
evaluation expectations and known answers out of blind subject inputs. Preserve
the active direction's context, access limits and authorized write boundary.

Do not delegate more launches implicitly. Track usage/time with available tools;
when a cap cannot be enforced, disclose that in the proposal and conservatively
stop before further work exceeds it. Missing telemetry is unknown, not zero.
At the limit, stop the batch and save partial evidence; extra work needs approval.

Check findings against source/repro artifacts; reject unsupported suggestions
and reconcile disagreements by evidence. The main agent owns the final decision.
Record accepted/rejected findings, proof gained, gaps and actual/unknown cost.

## Compare Cost Without Reducing Proof

Compare the same scenario and required checks before/after. Count discovery,
loaded skill bodies and conditional references, tool schemas/results, repeated
calls, all agents and reconciliation. Save full necessary evidence once and link
its compact result; don't reread it without an input/state/freshness/risk reason.

Report text/bytes/calls as proxies and tokens only when measured. Neither a
shorter SKILL.md nor fewer calls proves subscription savings or reliability.
Never hide missed pages, failed checks or unproven claims to fit a budget.
