# Caller Context

Read on entry and when supplied task boundaries change. This is an input contract,
not a dependency on a particular workflow or context repository. The caller may
be an active workflow or the main agent handling a direct user request.

## Required Inputs

Reuse facts already established in the task. Resolve each input before the action
that needs it; an unknown launch detail need not block unrelated direct work.

| Input | Responsibility |
| --- | --- |
| Task and proof | The caller supplies the objective, bounded question, project/direction when relevant, acceptance criteria, review depth and domain owners. Orchestration determines whether delegation adds useful proof. |
| Access and outputs | The caller supplies permitted reads/writes, result destinations and any exact runtime needed to use them. Orchestration verifies the saved-result path before launch; it grants no additional access. |
| Host controls | Reuse the current environment's available models/settings, tools, child-specific counters and stopping mechanisms; resolve only missing capabilities. Apply explicit user/project model restrictions. Verify measurement through `token_accounting.md`; missing counters in a tool response alone do not establish unavailable telemetry. |
| Authorization | Reuse the actual user decisions and existing batch bindings. Orchestration obtains any missing exact batch approval; a caller's approved flag or general implementation permission is insufficient. Operational/test owners retain their additional bindings. |
| Logging | Consume one task-scoped main/subagent flag and, when enabled, its parent identity, log destination and facts-index location. Orchestration owns attempt records and events; the caller owns storage and navigation. |
| Local policy | Apply explicitly supplied planning/calibration policy within its scope. Private history and configuration are optional inputs, never installation prerequisites. |

## Direct Invocation

Use the current request and available task configuration as the caller context.
No workflow or navigator installation is needed. Ask only for a material missing
constraint that cannot be resolved from permitted evidence. Do not create a
context repository, choose a private workspace layout or load another direction's
environment to fill a gap.

Agent logs default to off unless explicitly requested or an established logging
state covers this task. If logging is enabled, resolve permitted log/index
destinations before writing, without asking for a second opt-in. With logging off,
preserve necessary approval and result evidence in the existing task/test surface;
do not create audit logs or an index. Useful saved work remains required.

## Isolation And Return

Preserve the caller's project/direction, context, runtime and access boundaries.
Pass each worker only its assigned task, permitted evidence, required domain
instructions and execution/save constraints. An ordinary worker does not load
orchestration merely because it is a subagent. A separate test orchestrator's
workflow and assessment criteria stay outside a blind subject's active chain.

Return the result links, accepted findings, gaps, observed subagent cost and
continuation point to the caller. For direct invocation, the main agent presents
that same scoped result. Do not invent project acceptance or an independent review.
