# Context And Decisions

Use this reference for work that depends on previous state, local repos, task files, database contours, or long-running decisions.

## Navigation

- [Local context workspace and bootstrap](#local-context-workspace)
- [Runtime resolution](#runtime-resolution)
- [Restore context](#restore-context)
- [External research handoff](#external-research-handoff)
- [Workspace guardrails](#workspace-guardrails)
- [Maintain task snapshots](#maintain-context)
- [Agent logs](#agent-logs)
- [Decision hygiene and scope](#decision-hygiene)

## Local Context Workspace

Use the user's configured local context workspace/folder as the task memory area when the user refers to local context, task context, personal context, environment notes, or long-running local notes.

Do not assume a hardcoded folder name, owner, or filesystem path in this shared skill. Discover the local context workspace from:

- an explicit user-provided path or folder name;
- an existing project/workspace instruction that names the context workspace;
- a previously established context workspace in the current task conversation.
- a nearby directory named `my-coding-context`, when it is visible from the current workspace without broad filesystem scanning.

Use `my-coding-context` as the recommended default name for a personal local context workspace. This is a suggestion, not a required name, and it does not imply a git repository.

Automatic durable context is task-id driven. For non-trivial engineering, analytics, SQL, dbt, Python, Airflow, investigation, review, or project work, establish or restore the local context workspace before domain work when the user provides a task id, explicitly asks for durable context, explicitly asks for agent logging, or asks to continue an established context-backed task.

If there is no task id, no explicit context/log request, and no established context-backed task to continue, do not create a new context workspace, task snapshot, `environment.md`, or agent log by default. Work autonomously under the normal task mode, validation, database-access, approval, and safety gates. If durable memory would materially help, ask the user whether to enable it instead of creating it silently.

Do not treat the current working directory, task directory, project root, workspace root, or test/sandbox root as the local context workspace merely because it is writable. The context workspace must be explicitly configured, previously established, user-provided, or an actual nearby `my-coding-context` directory.

Phrases such as "work only inside this folder/workspace/sandbox", "do not use the real context workspace", or "enable agent log" define the allowed boundary for the task. They are not permission to use that root directory as a context workspace or to scatter `context.md`, `environment.md`, `tasks/`, or `agent_logs/` directly in it.

If the user forbids the real/external context workspace and durable context is required for the task, but no task-local `my-coding-context` exists, stop before context-backed domain work and ask whether to create `./my-coding-context` inside the allowed working area or use another path. Do not propose using the allowed working-area root itself as the context workspace unless the user asks for that shape or rejects a separate context directory. Create context files only inside the approved or existing context workspace.

For tasks without a task id or explicit durable-context request, continuing without a context workspace is the default. State that no durable local context was updated only when that matters.

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

```markdown
# <Local context map>

## <Quick entry>

- <Task navigation>: [`context.md`](context.md)
- <Machine environment>: [`environment.md`](environment.md)

## <Information owners>

| Information | Single owner |
| --- | --- |
| Active and closed task navigation | `context.md` |
| Current task snapshot | `tasks/<TASK_ID>.md` |
| Machine-specific runtime and paths | `environment.md` |
| Optional append-only agent log | `agent_logs/<TASK_ID>.agent_log.md` |
```

Keep local markdown context files (`context.md`, task snapshots, agent logs, meta-task files, `notes.md`, and similar `.md` files) in UTF-8. Do not mix UTF-8 with `cp1251` or another encoding in the same file.

## Runtime Resolution

Treat a configured `environment.md` as the first local map for repo roots and runtimes. It may come from an established context workspace, an explicit path, or a workspace instruction. Reading an existing map is read-only and does not by itself authorize creating task snapshots, agent logs, or a new context workspace.

Before the first local runtime-backed command, including incidental helper/validator use:

1. Use the target repo/project runtime when its config or environment map defines one.
2. Otherwise use the exact generic validation runtime mapped for that host and workload.
3. Use a bundled workspace runtime only for the artifact/tooling workflows it explicitly supports, not as a universal fallback.
4. Run bounded discovery only when no applicable mapping exists.

Do not invoke a bare executable or probe an alias recorded as unavailable, forbidden, or a shim. A later successful fallback does not make the initial known-bad attempt acceptable. Verify that the selected runtime matches the intended shell, repo, dependency surface, and task type before changing code or installing packages.

Keep `environment.md` a compact current-state lookup. Store exact
paths/commands, repo roots, local executable paths/versions, selection
constraints, secret-safe configuration-file pointers, and explicit unknowns.
Do not store credential values, account identities, access/approval policy,
task status, branches/commits, install history, dated smoke results, repo
anatomy, package inventories owned by requirements/locks, Git remotes
discoverable from the repo, or policy text owned by another skill/server
document. A `Local executables` section is a machine tool/runtime map, not an
inventory of installed skills or MCP servers.

After discovering a stable local environment fact, update or propose updating `environment.md` instead of leaving it only in chat, task notes, or logs. Mark agent-discovered values as draft/unconfirmed and ask the user to validate them before treating them as stable future configuration. For Airflow, CI, runner, command, import, or runtime-log investigations, resolve the environment before proposing code changes or commands.

If a configured context workspace lacks `environment.md`, ask whether to create the template, let the user fill it, or inspect local project/config/filesystem read-only and propose a draft. Do not invent paths or runtimes.

Use this minimal `environment.md` template when initializing a new local context workspace:

Localize the headings and explanatory labels in this example to the
user's/workspace language. Keep paths, executable names, identifiers, and
status tokens unchanged.

```markdown
# Local Environments

Minimal local environment map for skills. Store only machine-specific facts needed to choose the correct runtime and avoid guessing.

## Runtime Resolution

- preferred shell: `<shell or unknown>`
- forbidden aliases: `<aliases and reason, or none>`
- selection precedence: `project/repo runtime -> exact generic validation runtime -> bounded discovery`

| Workload | Exact runtime/command | Scope/status |
| --- | --- | --- |
| Generic validation | `<exact path/command or unknown>` | `<user-confirmed, draft/unconfirmed, or unknown>` |
| Project runtime | `<exact path/command or unknown>` | `<project/shell constraints>` |

## Repository Roots

- context workspace: `<path or unknown>`
- primary repo: `<path or unknown>`
- dbt root: `<path or unknown>`
- Python project root: `<path or unknown>`
- extra repo roots: `<path(s) or unknown>`

## Local Executables

| Tool | Exact path/version | Scope/status |
| --- | --- | --- |
| `<tool>` | `<exact path/version or unknown>` | `<selection constraint or status>` |

## Local Config Pointers

- `<purpose>`: `<secret-safe file path or unknown>`

## Boundaries

- current configuration only; task/project history lives in its owning context
- local executables are not an inventory of installed skills or MCP servers
- no credential values, account identities, or access/approval policy
- discovered values: `<draft/unconfirmed or user-confirmed>`
```

Keep unknown values explicit as `<unknown>` or `unknown`; do not invent paths or env names. If the user allows read-only discovery, propose a draft, label it unconfirmed, and ask the user to validate it. Treat discovered values as unconfirmed until the user accepts them.

Use this minimal `context.md` template when initializing a new local context workspace:

```markdown
# Локальный контекст задач

В этом файле хранится навигация по локальному контексту задач. Подробности ведутся в отдельных файлах, а не здесь.

## Как вести контекст

- Каждую отдельную задачу с task id вести в `tasks/<TASK_ID>.md`.
- `context.md` использовать как индекс и точку входа, а не как журнал.
- Новые незавершённые задачи добавлять в `Активные задачи`.
- Завершённые задачи переносить в `Закрытые задачи` с кратким итогом.

## Активные задачи

## Закрытые задачи
```

Inside `Активные задачи` and `Закрытые задачи`, use stable `-` bullets and
sort DP-style task identifiers by descending numeric id. Do not use sequential
list numbering that must be renumbered when a new task is inserted. Keep
initiatives without a DP-style id in separate active/closed non-DP sections.

Add optional `context.md` sections only when needed:

- `Мета-задачи`: long-lived areas without a normal task id, such as Airflow analyses or project notes.
- `Логи агента`: only when agent logging is explicitly enabled.

Meta-task files use a lighter structure than task snapshots. Keep the current focus near the top, keep history below, and use this shape when creating or reworking a meta-task file:

```markdown
# <Meta-task name>

## Назначение

## Текущий фокус

## Открытые вопросы

## Архитектура контекста

## Как вести контекст

## Текущее состояние

## Журнал
```

## Restore Context

When durable context is required or already established for the current task, inspect the minimum saved local context needed:

- the existing root `README.md` owner map before choosing individual context
  documents;
- `environment.md` for local repo roots and runtime choices when the task may need project files, SQL/dbt models, Python code, database contours, or repo discovery;
- current repo, branch, and dirty worktree;
- relevant task notes in `tasks/` or another local context file;
- recent decisions, open questions, known blockers, and validation status;
- known project conventions and implementation pointers already present in saved context or the scoped target repo;
- database contour/account through its selected owner: direct MCP via `db-access`, or an approved typed runtime read via a separately installed dedicated access owner + the SQL chain.

Do not ask the user to repeat context that can be recovered safely from local files, git state, or metadata.

If a failure looks like `ModuleNotFoundError`, dependency mismatch, wrong command behavior, or another runtime/import problem, verify the already selected runtime before changing code or installing packages. Do not retry through a different environment until the project/runtime mapping and dependency surface are understood.

## External Research Handoff

Keep this reference responsible for saved local context and its lifecycle. Do not implement broad external context discovery here.

Use the context-research owner selected by the active entry skill when missing requirements, prior decisions, ownership, project documentation, table meaning, lineage, or work discussions can materially change scope, design, implementation, or validation. The research owner handles research questions, bounded source selection, source reconciliation, and the compact task brief. If no such owner is available, preserve the evidence gap instead of expanding this core into an external-search workflow.

Keep OpenMetadata and direct database MCP access in `db-access`. Keep any separately approved typed runtime database-read route in its installed dedicated access owner + SQL chain. After research, this workflow decides what decision-grade facts belong in the task snapshot or agent log.

## Workspace Guardrails

Repo-specific workflow from durable context or user instruction remains authoritative. Do not reinterpret user-reserved branch, commit, push, review, or merge ownership boundaries; pass them unchanged to the operational owner selected by the active entry or domain skill when one is active.

Do not touch unrelated dirty files or revert changes you did not make. If unrelated dirty files exist, work around them and mention only the relevant risk.

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

```markdown
# <TASK_ID> - short title

## Текущий статус

## Цель

## План

## Валидация

## Контекст

## Решения

## Проверки

## Изменения

## Риски и стоп-точки

## Следующий шаг

## Архив
```

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

When the established context workspace defines a task-log review register, keep one current-state row per task there. Follow the root owner map or another explicitly configured workspace location; if neither exists, use a neutral `reviews/STATUS.md` path.

- keep `context.md` as navigation only and do not duplicate review or remediation status there;
- on task creation, add one row with task state `active`, review `pending`, and remediation `unknown`;
- on task closure, change only the task state to `closed` and preserve review and remediation exactly;
- never advance review or remediation from task completion, merge, approval, runtime success, or a closure summary alone;
- only the configured review owner may advance review coverage after saving and indexing the required evidence; remediation validation follows that owner's evidence contract.

If no task-log review register is configured, do not invent a workspace-specific status convention. Keep the short active/closed navigation entry in `context.md` and preserve any existing external review ledger unchanged.

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

```markdown
# <TASK_ID> Agent Log

## YYYY-MM-DD HH:MM MSK

### Mode

### Active skills

### Skill routing updates

### Facts

### Hypotheses

### Checks

### Decisions

### Rejected alternatives

### Validation

### Self-review
```

Keep detailed evidence and rejected alternatives in `agent_logs/...`; keep `tasks/<TASK_ID>.md` compact.

Keep append order and event time explicit. Use a timestamp for every appended event; if late evidence describes an older event, label the observed/event time separately instead of placing it as if it were current. When a final proof claim depends on raw output, save a durable non-secret path, URL/id, or content hash rather than referring only to an attachment that cannot be found later.

When the established local task context is in Russian, write new task context entries in Russian. Keep SQL identifiers, file paths, command names, and quoted source terms unchanged.

## Decision Hygiene

When stakes or ambiguity matter, separate:

- `Facts`: observed from code, metadata, logs, query results, or user statements.
- `Hypotheses`: plausible explanations not yet proven.
- `Decisions`: chosen approach and reason.
- `Open questions`: unresolved business or technical points.
- `Follow-ups`: useful but outside current scope.

Do not turn a hypothesis into implementation logic without either checking it or marking it as an assumption.

## Scope Control

- Do not expand scope silently.
- If a supporting task appears, say whether it is required for the current goal or a follow-up.
- Prefer minimal changes inside the requested ownership boundary.
- Avoid shared framework changes when a local project-level fix solves the task.
- Preserve meaningful existing comments that explain business logic, history, constraints, or non-obvious behavior.
