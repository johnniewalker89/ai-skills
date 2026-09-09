# Context Maintenance

Read only before creating or updating durable context, environment notes or an enabled agent log. Resolve the existing workspace through `context_and_decisions.md` first.

## Navigation

- [Create workspace](#create-a-workspace)
- [Environment and navigation](#update-environment-and-navigation)
- [Maintain context](#maintain-context)
- [Agent logs](#agent-logs)

## Create A Workspace

When creating or initializing a local context workspace, ask for permission to create the baseline structure and to inspect the current project/environment read-only if useful. Do not run `git init` or make the context folder a git repository unless the user explicitly asks for git.

Create only the minimum baseline by default:

- `README.md`
- `context.md`
- `environment.md`
- `tasks/`

Create optional areas only when the user asks for them or the task clearly needs them:

- `agent_logs/`: only when agent logging is enabled by an explicit user flag/request.
- `airflow_logs/`: when there are Airflow analyses without a task id.
- `meta/`: when the user asks to keep long-lived local notes outside normal task snapshots.
- `notes.md`: when the user wants local quick starts or personal notes.

If the user prefers to fill environment details manually, create a template or ask them to provide the needed values.

Use these locations:

- `README.md`: compact root owner map and quick entry to the current context
  surfaces; it must not become a journal, package catalog, or debt duplicate.
- `context.md`: navigation and active/closed task index, not a full journal.
- `environment.md`: local machine-specific environment map for repo paths, shells, Python/dbt runtimes, database contours, and other local runtime facts.
- `tasks/<TASK_ID>.md`: current task snapshot for continuing in a new chat.
- `agent_logs/<TASK_ID>.agent_log.md`: optional audit trail for agent behavior, decisions, evidence, rejected alternatives, and validation.
- `airflow_logs/airflow_logs.md`: shared Airflow failure analysis context when no task id exists.
- `meta/...`: optional long-lived local notes when explicitly requested by the user.

When an existing context workspace has a root `README.md`, read it before the
individual context files and follow its current owner map. Do not infer an old
flat layout from historical links when the owner map routes installation,
development debt, review state, or evidence elsewhere.

Use this compact root-map shape when initializing a context workspace. Include
only rows for surfaces that exist or are created in the current scope, and
localize headings to the user's/workspace language:

When creating this artifact, use the matching example in `references/context_templates.md`; do not load templates during ordinary restore/update.

Keep local markdown context files (`context.md`, task snapshots, agent logs, meta-task files, `notes.md`, and similar `.md` files) in UTF-8. Do not mix UTF-8 with `cp1251` or another encoding in the same file.


## Update Environment And Navigation

After discovering a stable local environment fact, update or propose updating `environment.md` instead of leaving it only in chat, task notes, or logs. Mark agent-discovered values as draft/unconfirmed and ask the user to validate them before treating them as stable future configuration. For Airflow, CI, runner, command, import, or runtime-log investigations, resolve the environment before proposing code changes or commands.

If a configured context workspace lacks `environment.md`, ask whether to create the template, let the user fill it, or inspect local project/config/filesystem read-only and propose a draft. Do not invent paths or runtimes.

Use this minimal `environment.md` template when initializing a new local context workspace:

Localize the headings and explanatory labels in this example to the
user's/workspace language. Keep paths, executable names, identifiers, and
status tokens unchanged.

When creating this artifact, use the matching example in `references/context_templates.md`; do not load templates during ordinary restore/update.

Keep unknown values explicit as `<unknown>` or `unknown`; do not invent paths or env names. If the user allows read-only discovery, propose a draft, label it unconfirmed, and ask the user to validate it. Treat discovered values as unconfirmed until the user accepts them.

Use this minimal `context.md` template when initializing a new local context workspace:

When creating this artifact, use the matching example in `references/context_templates.md`; do not load templates during ordinary restore/update.

Inside `Активные задачи` and `Закрытые задачи`, use stable `-` bullets and
sort DP-style task identifiers by descending numeric id. Do not use sequential
list numbering that must be renumbered when a new task is inserted. Keep
initiatives without a DP-style id in separate active/closed non-DP sections.

Add optional `context.md` sections only when needed:

- `Мета-задачи`: long-lived areas without a normal task id, such as Airflow analyses or project notes.
- `Логи агента`: only when agent logging is explicitly enabled.

Meta-task files use a lighter structure than task snapshots. Keep the current focus near the top, keep history below, and use this shape when creating or reworking a meta-task file:

When creating this artifact, use the matching example in `references/context_templates.md`; do not load templates during ordinary restore/update.

## Maintain Context

For `focused`, `project`, long `investigation`, and `review` tasks with a task id, create or update `tasks/<TASK_ID>.md`. If the task id is known but a task snapshot is not useful, say why.

If a task id appears mid-conversation, switch durable context to that id immediately: create or update `tasks/<TASK_ID>.md`, add a short `context.md` navigation entry when the task is ongoing, and move any prior no-id notes into or link them from the task snapshot when useful. Do not wait until final delivery to create the task context.

For tasks that will continue across chats, keep `tasks/<TASK_ID>.md` as a current snapshot with:

- current objective and chosen mode;
- current status;
- plan and current stage;
- validation plan or criteria;
- facts checked;
- decisions made and why;
- assumptions still in effect;
- changed files or artifacts;
- validation performed and numbers/results;
- risks and stop-points;
- blockers and next step.

Use this default task snapshot shape when creating a new file:

When creating this artifact, use the matching example in `references/context_templates.md`; do not load templates during ordinary restore/update.

Keep `tasks/<TASK_ID>.md` short enough to start a new chat quickly. It is a snapshot, not a full transcript.

Use line count as a guardrail for task snapshots only:

- at 250+ lines, pause and decide whether to compress or archive before adding more detail;
- at 300+ lines, archive before continuing unless the task is being closed immediately.

Update `context.md` as navigation. Keep separate `Активные задачи` and `Закрытые задачи` sections:

- add new ongoing work to `Активные задачи`;
- move completed work to `Закрытые задачи` with a short outcome;
- use stable `-` bullets and sort DP-style task ids by descending numeric id in
  each section; never introduce sequential ordinals;
- keep initiatives without a DP-style task id in separate active/closed non-DP
  sections;
- keep Airflow analyses or other long-lived work without a task id in a separate meta-task section, not in the task list;
- link related agent logs from the log section when useful;
- keep only short status text there.

When the established context workspace defines a task-log review register or a
skill-review/evaluation tree, ordinary task delivery must not write there. This
includes task creation, task closure, agent-log link changes, row backfill, and
review or remediation fields.

- keep `context.md` as active/closed task navigation and do not duplicate review
  or remediation status there;
- keep current task state in `tasks/<TASK_ID>.md` and append only to an enabled
  `agent_logs/<TASK_ID>.agent_log.md`;
- leave the configured review tree byte-for-byte unchanged throughout ordinary
  delivery, including technical closure;
- a separate configured review owner discovers tasks from navigation, snapshots,
  and logs, then creates or reconciles exactly one current-state row during the
  review pass;
- task completion, merge, approval, runtime success, or a closure summary is
  evidence for task state only and never advances review or remediation by
  itself.

If no task-log review register is configured, do not invent one. Keep the short
active/closed navigation entry in `context.md` and preserve any existing review
tree unchanged.

When the task snapshot becomes too long to be a quick-start file, archive it:

1. Rename the current snapshot to `tasks/<TASK_ID>.archive-YYYYMMDD-HHMM.md` using local time.
2. Create a new `tasks/<TASK_ID>.md`.
3. Carry forward only the current snapshot: status, goal, plan, validation, context, decisions, risks, next step, and links to archive files.
4. Keep `context.md` pointing to the current `tasks/<TASK_ID>.md`, not to the archive.

If multiple archives exist, keep the same timestamp naming; it sorts naturally and does not need a version suffix.

## Agent Logs

Use `agent_logs/<TASK_ID>.agent_log.md` only when agent logging is explicitly enabled by the user or when the user asks for a separate agent behavior/reasoning audit trail. Do not create agent logs by default. Do not satisfy an agent-log request by printing an "Agent Log" section only in chat; create or append the file after the local context workspace is established. If no local context workspace is established yet, stop and establish it first.

When agent logging is enabled and a task id becomes known, create or append `agent_logs/<TASK_ID>.agent_log.md` immediately with the current mode, active skills, facts, hypotheses, decisions, rejected alternatives, and validation status. Do not backfill the first agent log only at the end of the task.

If skill routing changes during the task, update the log instead of leaving only the initial skill list. Either update `Active skills` or add `Skill routing updates` with the skill name, reason, and role, for example `greenplum-sql: cross-engine lineage interpretation`.

Meta-tasks do not require separate agent logs by default. Keep meta-task reasoning in the meta-task file itself, such as `meta/<topic>.md` or `airflow_logs/airflow_logs.md`. Create an agent log for a meta-task only when the user explicitly asks for a separate reasoning, regression-analysis, or behavior-review trail.

Do not archive agent logs. Keep `agent_logs/<TASK_ID>.agent_log.md` as an append-only audit trail; use search and the current task snapshot to avoid rereading old detail.

The agent log is an audit trail, not hidden chain-of-thought. Record concise evidence-backed reasoning:

When creating this artifact, use the matching example in `references/context_templates.md`; do not load templates during ordinary restore/update.

Keep detailed evidence and rejected alternatives in `agent_logs/...`; keep `tasks/<TASK_ID>.md` compact.

Keep append order and event time explicit. Use a timestamp for every appended event; if late evidence describes an older event, label the observed/event time separately instead of placing it as if it were current. When a final proof claim depends on raw output, save a durable non-secret path, URL/id, or content hash rather than referring only to an attachment that cannot be found later.

When the established local task context is in Russian, write new task context entries in Russian. Keep SQL identifiers, file paths, command names, and quoted source terms unchanged.
