# Validation And Review

Use this reference for proof selection and final delivery for `focused`, `project`, `investigation`, and `review` tasks.

## Navigation

- [Validation modes](#validation-modes)
- [Self-review before delivery](#self-review-before-delivery)
- [Explaining rationale](#explaining-rationale)
- [Handoff](#handoff)

## Review Depth

Task mode, review depth and access mode are separate. Normal review retains all required owner proof; enhanced review adds a distinct check of a named risk. Use the workflow's conditional economy/depth procedure for enhanced review or any subagent, and never infer independence from a second agent's name. Reuse sufficient current evidence; changed inputs/state, freshness or a new risk justify repeat checks.

## Validation Modes

Choose the lightest safe check set that can prove the requested result. Domain
owners decide sufficiency; metadata, lint and smoke cannot establish behavior
they did not exercise. Describe the checked surface, exact inputs/revision,
environment, applicability and unproven levels. Reuse unchanged valid evidence.

Keep task mode and review depth separate from read-only versus approved sandbox
access. Writes, privileged access and cleanup retain their operational owner.
For SQL/dbt/data-pipeline or production-like artifacts, read
`references/data_artifact_proof.md` before selecting proof or a checkpoint.

Report the strongest completed level: draft/designed, bounded read-only validated,
approved sandbox proven, or ready only when the requested criteria are actually
proven. A successful command or a passed local self-review is not full acceptance.
Fix/disclose blockers; never use a budget limit to upgrade an incomplete result.

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
