# Context And Decisions

Use this reference for work that depends on previous state, local repos, task files, database contours, or long-running decisions.

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

- `context.md`: navigation and active/closed task index, not a full journal.
- `environment.md`: local machine-specific environment map for repo paths, shells, Python/dbt runtimes, database contours, and other local runtime facts.
- `tasks/<TASK_ID>.md`: current task snapshot for continuing in a new chat.
- `agent_logs/<TASK_ID>.agent_log.md`: optional audit trail for agent behavior, decisions, evidence, rejected alternatives, and validation.
- `airflow_logs/airflow_logs.md`: shared Airflow failure analysis context when no task id exists.
- `meta/...`: optional long-lived local notes when explicitly requested by the user.

Keep local markdown context files (`context.md`, task snapshots, agent logs, meta-task files, `notes.md`, and similar `.md` files) in UTF-8. Do not mix UTF-8 with `cp1251` or another encoding in the same file.

When durable context is required or explicitly selected for the task, treat `environment.md` as the first local map for repo roots and runtimes. Read it before searching the filesystem for project repos, dbt projects, Python package roots, SQL model locations, validation runtimes, or shell commands.

When durable context is required or explicitly selected and the task depends on local runtime environment, repo paths, Python/dbt env names, shell choice, or import/runtime failures, consult `environment.md` in the configured local context workspace before probing filesystem, shells, Python/dbt commands, or repo roots. Treat it as machine-specific local configuration, not as portable skill behavior. If a local context workspace exists but `environment.md` does not, use the same context-workspace flow: ask whether to create an environment template, let the user fill it manually, or inspect local project/config/filesystem read-only and propose a draft.

When durable context is required or explicitly selected, after discovering a stable local environment fact, update or propose updating `environment.md` instead of leaving the fact only in chat, task notes, or logs. If the fact was discovered by the agent rather than provided by the user, mark it as draft/unconfirmed in `environment.md` or in a nearby note, and ask the user to validate it in the final response before relying on it as stable context for future tasks. The final response must name the `environment.md` path and ask the user to confirm or correct the draft values.

When durable context is required or explicitly selected for Airflow, CI, runner, command, import, or runtime-log investigations, check `environment.md` before proposing code changes or choosing a validation command. Logs that mention deployed paths, virtualenv/pyenv names, `PYTHONPATH`, missing modules, or wrapper commands are enough to trigger this check.

Use this minimal `environment.md` template when initializing a new local context workspace:

```markdown
# Local Environments

Minimal local environment map for skills. Store only machine-specific facts needed to choose the correct runtime and avoid guessing.

## Paths

- context workspace: `<path or unknown>`
- primary repo: `<path or unknown>`
- dbt root: `<path or unknown>`
- Python project root: `<path or unknown>`
- extra repo roots: `<path(s) or unknown>`

## Runtimes

- Python runtime: `<command/path or unknown>`
- dbt runtime: `<command/path or unknown>`
- preferred shell: `<shell or unknown>`

## Notes

- discovered values: `<draft/unconfirmed or user-confirmed>`
- database access: `through db-access only; <available/unknown/not used>`
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

When durable context is required or already established for the current task, inspect the minimum durable context needed:

- `environment.md` for local repo roots and runtime choices when the task may need project files, SQL/dbt models, Python code, database contours, or repo discovery;
- current repo, branch, and dirty worktree;
- relevant task notes in `tasks/` or another local context file;
- recent decisions, open questions, known blockers, and validation status;
- project conventions, existing implementation patterns, and source-of-truth files;
- database contour/account only through `db-access`.

Do not ask the user to repeat context that can be recovered safely from local files, git state, or metadata.

If a failure looks like `ModuleNotFoundError`, dependency mismatch, wrong command behavior, or another runtime/import problem, check the active runtime before changing code or installing packages. Use `environment.md` when available and verify the path to the relevant `python`, `dbt`, or shell command.

## Workspace Guardrails

Do not create git commits or push changes without explicit user approval. If the user asks for a commit or push, inspect status/diff first and state what will be included before acting.

Before any push, inspect the current branch, upstream, and exact remote target. If the branch is intended as a feature branch but tracks the default branch such as `origin/master` or `origin/main`, stop and ask the user to correct the branch/upstream or approve the exact safe target before pushing.

Repo-specific workflow from durable context or user instruction is authoritative. If the user owns branch creation, commits, pushes, or merge requests for a repo, default to working-tree changes only and do not create those git artifacts unless the user explicitly asks for that exact action.

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
- keep Airflow analyses or other long-lived work without a task id in a separate meta-task section, not in the task list;
- link related agent logs from the log section when useful;
- keep only short status text there.

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
