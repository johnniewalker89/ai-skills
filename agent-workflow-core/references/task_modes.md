# Task Modes

Choose the lightest mode that protects quality. For non-tiny work, make the chosen mode the first user-facing sentence so the user can correct it before the work proceeds.

The mode set is closed: `quick`, `focused`, `project`, `investigation`, and `review`.
Use the mode as an exact literal token. Do not append or prepend qualifiers, checklist names, phases, or task labels.
Do not invent synonyms or phase names such as `quick-check`, `edit`, `implementation`, `development`, `analysis`, `audit`, `research`, or `review/scoring`. If a task is implementation work, its mode is still `quick`, `focused`, or `project` depending on risk. If a task is a check, proof, or scoring pass, its mode is still one of the five allowed values.

When announcing a non-tiny task, the first user-facing sentence must be shaped like `Режим: ` followed by exactly one allowed mode value in backticks. Put the task subtype in the next sentence, not in the mode token.

If you accidentally announce an invalid mode, correct the mode explicitly in the next user-facing update before tool work or file edits continue.

## quick

Use for tiny, clear, low-risk tasks:

- factual answers;
- simple command output;
- single obvious file read;
- formatting or wording with no hidden business rule.

If a task id appears but the user only asks a tiny factual question, `quick` is still allowed.
If the user asks to do, analyze, check, fix, implement, validate, or continue that task, escalate to `focused` or higher.

Behavior:

- answer or act directly;
- no separate plan unless the user asks;
- no task context update unless it changes a durable decision.

## focused

Use for normal engineering, SQL, data, config, or documentation work with limited scope.

Do not use `focused` only because the code diff looks small. If the task changes production semantics, changes external system state, requires object creation/rebuild/recalculation, requires extended sandbox validation, or contains destructive/hard-to-reverse work, choose `project`.

A known task id is usually at least `focused` when the user asks for work, not just a factual answer.

Behavior:

- state mode and immediate approach in one or two sentences;
- inspect relevant repo/context before editing;
- keep a short visible plan when useful;
- use read-only validation by default;
- update task context when a task id or established task/context files exist; if no context update is needed, say why;
- execute, validate, self-review, and report concise results.

`focused` does not mean "plan only in memory". It means the plan is smaller than `project` mode but still visible in updates, context, or both when the work has durable state.

## project

Use when the task is multi-step, expensive, destructive, high-stakes, cross-system, business-ambiguous, production-like, or likely to span chats.

Also use `project` when the change is small but the risk is high:

- production or production-like model, SQL, config, or data-contract logic;
- new production-like mart/model design, even in an eval or sandbox, when business grain, refresh window, attribution window, target materialization, or validation assumptions are not already fixed by the user;
- attribution, allocation, revenue, billing, audit, compliance, or permission-policy semantics;
- grain, join keys, mappings, fallback/default behavior, lifecycle windows, or validation assumptions;
- external system state changes, database writes, object creation, rebuilds, recalculations, or actions requiring cleanup/rollback;
- production-like validation assumptions, extended sandbox validation, generated validation artifacts, expensive runs, cleanup, or rollback decisions;
- destructive or hard-to-reverse goals;
- unclear business rules where several plausible interpretations would produce different data.

Behavior:

- state why `project` mode was chosen;
- restore context and current repo/database state;
- perform safe autonomous read-only reconnaissance when it is needed to avoid a generic plan: local source search, existing contracts, metadata through `db-access`, bounded counts, and bounded `EXPLAIN`/query-log checks when safe;
- run safe proof-oriented read-only probes before the checkpoint when they can reduce uncertainty without writes, expensive scans, or semantic commitment: lightweight equivalent queries, bounded output checks, aggregate comparisons, invariant checks, or small smoke queries;
- after reconnaissance, propose stages, dependencies, proof strategy/evidence boundary, expected artifacts, stop-points, and cleanup/rollback considerations when relevant;
- for cross-system or multi-artifact work, include source/contour map, ownership boundaries, unresolved business rules, and validation responsibilities;
- stop and wait for explicit approval before implementation, generated artifacts that embody the solution, sandbox validation artifacts, DDL/DML, large recalculation, migration, or long run;
- if the task is a new production-like data artifact with unfixed sources, grain, refresh, attribution/window, materialization, or validation assumptions, the checkpoint must be concrete: selected sources, rejected alternatives, proposed grain, refresh/reprocessing scheme, attribution/window semantics, proof strategy/evidence boundary, artifacts to create, and stop-points;
- the proof strategy/evidence boundary must distinguish evidence already collected, checks still planned, what read-only can prove, what read-only cannot prove, triggers for Extended Sandbox Validation, and what evidence/artifacts will be saved;
- use the mandatory checkpoint shape from `references/safety_and_stop_points.md` for new production-like data artifacts; do not scatter proof details only in prose, and do not ask for approval until every required section is present;
- do not ask approval merely to start safe read-only discovery; ask when discovery would become expensive, writable, broad/unbounded, or semantically committing;
- if the user explicitly asked for a draft without approval gates, label it as draft and still name unproven assumptions and the missing proof step;
- maintain task context with status, decisions, checks, changed files, blockers, and next step;
- archive old chronology when task context becomes too large.

For detailed project gates and destructive-action rules, read `safety_and_stop_points.md`.

## investigation

Use for failures, data mismatches, runtime/tool issues, production symptoms, unclear causes, or "why is this happening" tasks.

Behavior:

- separate symptom, facts, hypotheses, checks, and conclusion;
- prefer logs, metadata, actual runtime path, and direct evidence over guesses;
- test one hypothesis at a time when possible;
- when localizing a suspected bug, provide an evidence chain: the object exists before the suspected step, fails at a specific condition/join/mapping/window, is absent after that step, and the relevant field values explain why;
- mark a suspected cause as unproven if the evidence chain is incomplete, and state the next read-only check needed;
- classify the result: fixed, explained, reproduced, not reproduced, blocked, or follow-up.

## review

Use when the user asks for review, findings, or evaluation.

Behavior:

- lead with findings ordered by severity;
- cite file/line or exact artifact locations when available;
- focus on bugs, semantic risks, regressions, missing tests, and validation gaps;
- keep summary secondary;
- if no issues are found, say so and name residual risk.
