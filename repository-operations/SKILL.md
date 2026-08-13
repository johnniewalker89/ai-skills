---
name: repository-operations
description: "Use for local or remote repository and CI operations across Git, GitHub, GitLab, or Jenkins: identity/provider resolution, clone/fetch/status/diff/history, branches/commits/pushes, pipelines/jobs/checks/logs/artifacts, PR/MR/issues/reviews/comments, releases, repository settings, permissions, rulesets, secrets metadata, and administrative actions. Use with the active Engineering or Game workflow owner so approvals remain direction-local."
---

# Repository Operations

Use this skill as the neutral repository control layer shared by Engineering and Game work. It classifies and executes repository operations; it does not own task workflow or code quality.

## Role

- Purpose: operate repositories through the correct provider, account, target, and approval scope without approval spam or unintended actions on the user's behalf.
- Owns: repository/provider/account resolution, effective-identity verification, repository action classification, technical-grant boundaries, communication/admin/risky-action enforcement, Git remote/branch/upstream safety, CI evidence retrieval, narrow execution, secret-safe output, and final-state readback.
- Delegates to: the active direction workflow for obtaining and retaining approval, the active code/content domain owner for artifact quality, language/runtime owners for failure interpretation, and configured identity-bound repository tools for provider operations.

## Hard Gates

1. **Workflow companion gate.** Use the behavioral workflow companion selected by the active direction's navigator and role map. That workflow obtains and holds approval; this skill classifies actions, enforces the approved scope, executes, and reads state back. Never substitute another direction's workflow.
2. **Identity gate.** Before any remote operation, resolve provider/host, effective account, repository, remote URL, required permission, and configured identity-bound tool or credential path. Never infer identity from a local Git author or a matching repository name. Read `references/identity_and_execution.md` before the first remote operation or any account/provider switch.
3. **Classification gate.** Before acting, classify every operation as `read`, `technical_grant`, `exact_approval`, or `forbidden`. Read `references/action_and_approval_policy.md` before any write, communication, CI control, publish/release, risky Git, credential, permission, or administrative action.
4. **Read gate.** Bounded repository inspection and diagnostics are allowed without approval when they do not change provider state or user-authored repository content, expose secrets, or communicate externally. A named clone into a fresh destination and fetch-only ref/cache updates remain read-class operations.
5. **Technical-grant gate.** Ordinary technical work may use one short task-scoped approval only when bound to provider/host, immutable account/repository ids, workspace realpath + Git-dir identity, task/project, exact branch, allowed actions + paths, expected local/remote SHA, short TTL, process nonce, and finite use cap. Enforce compare-and-swap before every use; drift, restart, replay, nonce/TTL/use exhaustion, or CAS mismatch invalidates the grant. It never covers communication, any protected-branch push, force/destructive Git, deploy/publish/release, credentials, secrets, repository control-plane configuration, or administration. On an explicitly server-enabled personal default branch, the grant may cover local stage/commit/amend even when the branch is protected; every normal non-force push then requires separate exact approval and authoritative readback, with no PR/MR required by this contract. A grant may include direct default-branch push only while that branch is unprotected and the exact personal repository is explicitly enabled. Other protected/default/work repositories keep their stricter policy and fail closed; no repository in the chat inherits another repository's exception.
6. **Exact-approval gate.** Every communication on the user's behalf and every merge, deploy, publish/release, risky/destructive Git, credential/secret, permission, protection/ruleset, repository setting, or administrative action requires per-action exact approval for the named operation, target, and payload. Do not carry that approval to a later action. One confirmation may cover a presented batch only when every action is independently enumerated with its exact payload and target.
7. **Control-plane gate.** Repository-tool source/configuration, MCP registration, credentials, account bindings, allowlists, policy files, `.github/workflows/**`, `.github/actions/**`, `.gitlab-ci.yml` and its includes, `CODEOWNERS`, `.gitmodules`, `.gitattributes`, repository deploy/infra/release/security control paths, branch protection, rulesets, bypasses, secrets/variables, deploy keys, webhooks, environments, and security settings are control-plane surfaces. They are never part of an ordinary technical grant; changing a file surface requires exact sensitive-path approval naming exact paths and the reviewed diff digest.
8. **Forbidden gate.** Never read or reveal stored secret/token values, use a mismatched identity, fall back to global credentials after identity failure, expose an arbitrary provider API or shell through MCP, execute wildcard destructive actions, silently bypass protection, or reuse approval across accounts, repositories, branches, or tasks.
9. **Readback gate.** Before a write, capture the safe relevant baseline or preview. After it, read authoritative resulting state. A command exit code or accepted API response alone is not proof.
10. **Self-review gate.** Before reporting repository success, readiness, blocker, or completed action, run this skill's Final Checklist.
11. **External-CI gate.** When a repository status/check targets Jenkins, use the configured identity-bound Jenkins tool for job/build/stage/log evidence. Read `references/jenkins_execution.md` before the first Jenkins operation or any Jenkins control action.

## Workflow

1. Resolve the active direction workflow and the exact repository contour.
2. Inspect local worktree/branch/upstream/remote and provider identity as needed without approval.
3. Split mixed requests into independently classified operations; unknown or mixed-impact operations use the stricter class.
4. Reuse a valid technical grant only while every binding remains unchanged; otherwise ask the workflow owner to obtain the required approval.
5. Preview the narrow target, execute through the configured identity-bound path, and stop on identity, permission, protection, scope, or payload drift.
6. Read back the resulting local/provider state and report evidence, remaining actions, and unproven effects.

## Reference Triggers

- Read `references/action_and_approval_policy.md` before any repository write, communication, CI control, publish/release, risky Git, control-plane, or administrative action, or when deciding whether an existing approval applies.
- Read `references/identity_and_execution.md` before the first remote operation, account/provider selection or switch, clone/fetch/pull/push, provider-tool use, or final-state proof.
- Read `references/jenkins_execution.md` before following a Jenkins status link, reading Jenkins evidence, or preparing any Jenkins build control.

## Final Checklist

- Did I use only the active direction's workflow companion?
- Did I verify provider/host, effective account, repository, remote, branch/upstream, and permission relevant to the operation?
- Did I classify every operation and use no approval for bounded reads, one correctly bound grant for ordinary technical work, and exact approval for communication/control-plane/risky/admin work?
- Did I keep communication, every protected-branch push, deploy/release, secrets, credentials, and repository administration outside the technical grant; limit protected-default local commit/amend plus direct default pushes to their exact personal-repository policies; and require separate exact approval/readback for each eligible protected-default push without inventing a PR/MR requirement?
- Did I stop on scope or identity drift without falling back to global credentials, arbitrary APIs, raw MCP shell, or protection bypass?
- Did staging/commit/push include only intended files and the exact approved branch?
- Did I bound and sanitize CI logs, artifacts, repository metadata, and tool output?
- Did I use head-bound repository-provider checks for PR/MR readiness and explicitly report any conflict with external-CI aggregate or stage results?
- Did I read authoritative state back and distinguish completed, accepted-but-unproven, blocked, and remaining actions?
