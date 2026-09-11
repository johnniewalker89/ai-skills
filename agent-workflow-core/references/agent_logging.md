# Agent Logging

## Shared Opt-In

All agent logs are optional by default. One user request such as “enable agent
logs” enables both main and subagent logs for the requested task or initiative.
Retain the flag and its scope in established context; no second child-log opt-in
is needed. A task id, a subagent launch, or a test profile does not enable audit
logging. Apply an explicit disable request prospectively, preserving history.
Do not infer a permanent global preference from a task-scoped request.

With logging off, create no agent audit logs, run-log templates or audit index.
Their absence is neither a failure nor review backlog. Required domain results,
test evidence and proportionate execution controls remain necessary; do not turn
them into an audit log under a different name.

## Storage And Navigation

Use the established context workspace and its owner map. Keep a compact current
snapshot separate from append-only audit history. The main log records decisions,
routing, evidence and validation; `context_templates.md` supplies its template.
Do not record hidden reasoning or secrets.

When enabled, use a stable parent key: the task id for an ordinary task, or the
initiative's stable key for meta work. A business case used as a test fixture is
an input, not the parent of the test initiative. Reuse existing keys and paths.
Portable defaults, adapted to the workspace's existing layout:

- main log: `agent_logs/<parent-key>.agent_log.md`;
- attempt logs: `agent_logs/subagents/<parent-key>/<run-id>.md`;
- compact facts index: `agent_logs/subagents/INDEX.md`.

Link the main log and relevant attempt-index anchor from the parent snapshot or
meta file. Task navigation may carry a short inline link with the parent entry;
do not create a separate global agent-log section in `context.md`. Keep facts
indexes outside the evaluation tree. Workflow owns this layout and shared history
navigation; orchestration owns the attempt schema, event updates and planning
summary. A configured evaluator exclusively owns review coverage and verdicts.

## Historical Continuity

Preserve old links and measured facts when moving history; a small forwarding
file can retain the former entry point. Keep original forecasts, failed-attempt
costs and evidence limits. Distinguish attempted work from unlaunched proposals.
Reconstruct only what available evidence supports, label retrospective entries
and unknown values, and never make reconstructed logs look contemporaneous.

Keep the index small enough for a single planning pass: parent/run ids, task and
model/setting, forecast/ceiling, actual tokens/time, outcome and evidence links.
Do not copy full reports or review verdicts into it. Moving history does not
authorize fresh agents or a full re-review of old attempts. Private cohort policy
and accumulated history remain local, not dependencies of the public package.
