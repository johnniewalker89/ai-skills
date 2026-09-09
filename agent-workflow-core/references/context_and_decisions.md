# Context And Decisions

Read before restoring an established task or resolving local environment/runtime.
Read `context_maintenance.md` only before durable writes; templates are needed
only when creating the corresponding artifact.

## Navigation

- [Workspace](#local-context-workspace)
- [Runtime](#runtime-resolution)
- [Restore](#restore-context)
- [Research handoff](#external-research-handoff)
- [Workspace guardrails](#workspace-guardrails)
- [Decisions](#decision-hygiene)
- [Scope](#scope-control)

## Local Context Workspace

Use the explicitly configured/user-provided workspace, the one already established
in this task, or a nearby existing `my-coding-context` visible without a broad scan.
That name is a recommendation, not a required directory or an implicit Git repo.
A writable cwd, project, task or sandbox root is not automatically context storage.
"Work only here" or "enable logs" specifies scope, not permission to scatter context
files in that root. If the configured workspace is forbidden and durable context
is needed, resolve a permitted separate workspace with the user before dependent work.

Restore durable context for a task id, explicit context/log request or continuation
of an established context-backed task. Otherwise create no context files by default.
Reading an existing environment map alone enables neither logging nor task storage.
For creation, preserve existing authorization and use the maintenance procedure;
do not run `git init` without explicit user instruction.

`README.md`: compact root owner map. When it exists, read it before the
individual context files and follow its configured paths. Navigation, environment,
task snapshot, optional logs, development debt and review evidence have separate owners.
Ordinary delivery must not write the configured review tree; evaluator owns its rows
and statuses. Do not infer current layout or approval from historical task links.

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
