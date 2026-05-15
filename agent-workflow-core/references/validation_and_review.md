# Validation And Review

Use this reference before final delivery for `focused`, `project`, `investigation`, and `review` tasks.

## Validation Modes

Choose the lightest validation mode that can prove the result.

For SQL, dbt, analytics, data-pipeline, or production-like changes, make the validation-mode rationale visible to the user before or with the validation plan:

- which validation mode was chosen;
- why it is sufficient or why read-only is insufficient;
- what the checks will prove;
- what they will not prove;
- what evidence or blocker would trigger escalation from read-only to extended sandbox validation.

For new production-like data artifacts, express this as a proof strategy/evidence boundary at the checkpoint before solution artifacts or readiness claims. The boundary must separate evidence already collected from checks still planned.

Do not choose validation mode by convenience. Choose it by proof power:

- `Read-Only Validation` is sufficient only when it can actually prove the requested result without writes, for example by executing a lightweight equivalent query, checking bounded output, comparing aggregates/diffs, or saving reproducible evidence for the success criteria.
- Metadata, DDL review, `EXPLAIN`, and smoke counts can support a design, but they do not by themselves prove that a new production-like mart/model returns the correct result.
- If read-only checks cannot prove the result, explicitly say the artifact is draft/not proven and propose an `Extended Sandbox Validation` plan instead of ending with "done". In user-facing chat, localize that proposal to the user's language and make it an approval question for sandbox work.
- If the user asked for a production-like result and no proof-capable validation mode was completed, the final answer must not claim production/MR readiness.
- Final wording must match the strongest proof actually completed:
  - `designed/draft`: artifacts or design exist, but result correctness or runtime is not proven;
  - `read-only validated`: bounded/executable read-only checks prove the stated success criteria within their named limits;
  - `sandbox proven`: approved sandbox build/diff/runtime checks prove the artifact behavior;
  - `ready`: only when the requested readiness criteria are proven and residual risks are explicitly acceptable.
- For new production-like data artifacts, safe read-only validation discovery is allowed before the checkpoint when it is needed to choose sources, grain, and proof strategy. Keep it bounded and reversible. If a lightweight equivalent query, bounded output check, aggregate comparison, invariant check, or small smoke query can safely reduce uncertainty before the checkpoint, run it and bring evidence.
- After that discovery, the checkpoint must explain whether read-only evidence can prove the result or whether Extended Sandbox Validation is required.
- If the task requires generated SQL/DDL/build artifacts, do not create them before the checkpoint unless the user explicitly asked for an unapproved draft. The checkpoint should be concrete enough that the user is approving a proposed solution, not approving the agent to start thinking.
- Keep approvals staged: ask for repo artifact creation first; after artifacts exist and pass self-review plus available read-only validation, ask separately for extended sandbox validation if it is still required. Do not combine those approvals into one "create artifacts and run sandbox" request.

The proof strategy/evidence boundary should include:

- evidence already collected;
- checks still planned;
- what read-only can prove;
- what read-only cannot prove;
- triggers for Extended Sandbox Validation;
- evidence/artifacts that will be saved;
- success criteria.

Proof claim precision is mandatory. Any statement such as `exact diff`, `equivalent`, `sandbox proven`, `ready`, or `ready_for_mr` must name:

- the comparison surface: full output values, row set, aggregate totals, missing-row check for an added predicate, source-vs-target reconciliation, or another exact surface;
- the scope: exact dates/windows, batch shape, target objects, engine, schema, and relevant parameters;
- the applicability envelope: whether the proof covers daily batches, monthly batches, rolling rebuilds, one partition, multiple partitions, or another execution pattern;
- what did not change and why that makes the comparison sufficient;
- what remains unproven.

Do not write `diff 0/0` or `equivalence proven` without that scope. If only a guard/predicate was validated, say that the added guard did not change the checked row set for the named window; do not imply a full output-value diff unless that was actually executed.

For new production-like data artifacts, use the mandatory checkpoint shape from `references/safety_and_stop_points.md`; do not leave the proof boundary only as scattered prose, and do not ask for approval until every required section is present. If a section is unknown or not applicable, include it anyway and write that explicitly.

Chat-output contract for proposal checkpoints and final proof summaries:

- At most 8 bullets or short lines in chat unless the user asks for detail.
- No raw counts, query text, full rejected-alternative lists, or long evidence-boundary sections in chat.
- Chat must include only: status/proof level, proposed decision, top 1-3 risks/open business questions with recommended defaults when possible, strongest completed proof, what remains unproven, and one next approval/proof step.
- The full mandatory checkpoint shape must still be saved in the task note or agent log; chat may reference that it was saved there instead of printing every section.
- For `read-only validated` production-like artifacts, the final chat line is mandatory when materialization/refresh/runtime/equivalence is still unproven, but it must be written in the user's language and phrased as an approval question for sandbox work.
- Do not leak English boilerplate such as `Next proof step` or `Extended Sandbox Validation` into user-facing Russian chat. English labels may remain in task notes/logs when they are stable internal section names, but the chat-facing approval request must be localized.

When the work involves an optimization, rewrite, attribution/window change, aggregation change, deduplication, join semantic change, or any shortcut that might alter business meaning, make business semantics visible as its own attention line, not only inside generic risks. This is a high-signal user-facing warning, so it must be visually prominent. Use the user's language and emphasize only the stable label with inline code formatting, for example:

- `Бизнес-семантика:` есть риск изменения правила; нужна отдельная проверка эквивалентности или sandbox validation перед внедрением.
- `Бизнес-семантика:` read-only checks подтверждают ту же семантику для проверенных случаев; непроверенные edge cases перечислены ниже.

Use this line in both `Read-Only Validation` and `Extended Sandbox Validation` summaries when business semantics are relevant.

### Read-Only Validation

Use this as the default mode.

This is the normal validation mode for SQL, dbt, analytics, and data-pipeline changes when the result can be proven without changing database state.

Allowed checks:

- targeted diff/readback for low-risk text, config, or documentation;
- local tests, lint, compile, type checks, dry-runs, or command help/version checks;
- repository contracts, model definitions, DDL text, and existing implementation review;
- database validation through `db-access` plus the relevant SQL skills, such as metadata, DDL, `EXPLAIN`, constrained `SELECT`, smoke aggregate, or bounded comparison queries;
- small sanity comparisons that do not change database state.

Expectations:

- state the read-only validation plan before using database access when the task is non-trivial;
- for new production-like artifacts, it is acceptable to state a short reconnaissance intent, perform safe bounded discovery/probes, and then present the full proof strategy after concrete sources and grain are known;
- keep all database work inside `db-access`;
- do not run `dbt run`, `dbt build`, rebuilds, creates, drops, inserts, deletes, or cleanup actions in this mode;
- for code changes, run the narrowest relevant check or explain the blocker;
- for SQL, data, or modeling logic, try to prove correctness with read-only evidence first;
- after a code, SQL, data, or modeling fix, use before/after proof or a patched-query simulation when feasible; show that the affected row, order, metric, rule, or behavior now passes the success criteria;
- compare the result to the user's requested behavior, not only to command success.
- if a proposed rewrite or optimization is not proven equivalent, explicitly say it is a candidate, not a safe replacement, and put the business-semantics warning in a standalone line with the formatted label.
- if a new mart/model is only designed but not result-validated, call it a draft design and name the missing proof step.

### Extended Sandbox Validation

Use this only when read-only validation cannot prove the result and validation requires creating, changing, rebuilding, recalculating, or deleting database state.

Examples include creating or rebuilding intermediate tables/models only to prove whether a row, order, metric, or rule reaches the final artifact.

Triggers that can raise validation from read-only to extended sandbox:

- materialization, schema contract, partition/order key, or runtime behavior must be proven by actually building an artifact;
- `dbt run`, `dbt build`, `--full-refresh`, model rebuild, or dependency selector is needed;
- a sandbox table/view/temp artifact must be created;
- old-vs-new metric comparison requires persisted sandbox outputs;
- read-only checks cannot prove a risky aggregation, attribution window, deduplication, `LEFT ANY JOIN`, `FINAL`, `argMin`, or similar data-shape behavior;
- the user asks to run in a test contour, build a sandbox, or validate on a recreated artifact.

Extended sandbox validation is `project`-gated. Before any action, propose:

- sandbox contour/environment;
- exact commands, actions, target objects, and target set;
- short validation window or interval;
- comparison baseline;
- cleanup/rollback plan;
- `db-access` escalation path when normal read-only validation is not enough.

Then stop and wait for explicit approval.

After approved sandbox actions run, compare the result with the success criteria. A successful run, build, create, or rebuild is not validation by itself.

Do not create database validation artifacts by default. First use read-only validation; if it is insufficient, propose the sandbox validation plan in the user's language and stop. For Russian chat, end with a compact question like: `Следующий шаг проверки: расширенная валидация в песочнице — <sandbox target>, <bounded load>, <comparison checks>, <cleanup>. Запускать?`

Validation should prove the changed behavior, not only that a command completed.
If the sandbox exists to prove a business-semantics-preserving rewrite, report the equivalence result explicitly in the standalone business-semantics line.

## Self-Review Before Delivery

Before final response, run a self-review pass. After implementation, report the material result of that pass compactly: scope, changed files/artifacts, validation evidence, residual risks or blocked checks, and whether the newest user instructions were honored.

Check:

- Did the work answer the newest user request?
- Did I stay inside the requested scope?
- For non-tiny work, did the first user-facing update announce the task mode before skills, plan, or tool commentary?
- Did I avoid reverting unrelated user changes?
- Did I explain the chosen validation mode and the evidence it can and cannot prove?
- Did my final status wording match that evidence, without calling draft/read-only work "done" or "ready"?
- Did I validate the important behavior or state the blocker?
- Did I update durable context when this task will continue?
- Are remaining risks, assumptions, or follow-ups explicit?

For code or SQL review tasks, findings lead. For implementation tasks, summarize changed files, validation, and residual risk.

## Explaining Rationale

When the user asks why something was done:

- answer as an explanation, not a defense;
- name the constraint or evidence that drove the choice;
- describe the tradeoff against reasonable alternatives;
- say what evidence would make you change the decision;
- if the question reveals a bad assumption, acknowledge it and revise.

## Handoff

A good handoff includes:

- what changed or what was found;
- validation performed, with key commands/results when useful;
- what was not validated and why;
- next step only when it naturally follows from the task.
