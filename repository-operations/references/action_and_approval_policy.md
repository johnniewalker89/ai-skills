# Action And Approval Policy

Use this reference before any repository mutation or when deciding whether an existing approval covers the next operation.

## Navigation

- [Read: No Approval](#read-no-approval)
- [Technical Setup: No Separate Approval](#technical-setup-no-separate-approval)
- [Technical Grant](#technical-grant)
- [Exact Approval](#exact-approval)
- [Work Commit And Push](#work-commit-and-push)
- [Forbidden](#forbidden)

## Read: No Approval

Keep reads bounded, secret-safe, and non-communicating:

- resolve provider, repository, effective identity, permissions, remotes, upstreams, branches, tags, status, diff, and history;
- fetch refs or run `ls-remote`; clone an explicitly named repository into an already configured workspace without changing provider state;
- read repository files, PR/MR/issue/review/comment threads, settings, collaborators, permissions, rulesets, and protection state;
- inspect pipeline/workflow/check/Jenkins job status, bounded sanitized logs, stage and artifact manifests, releases, tags, and asset digests;
- inspect secret/variable names, scope, and update timestamps when exposed, never their values;
- prepare local drafts, proposed payloads, dry runs, and exact action plans without publishing them.

A read leaves this class when it changes provider state or user-authored repository content, accesses secret values, communicates externally, or exceeds the stated bounded scope. A named clone into a fresh destination and fetch-only ref/cache updates are the explicit benign local-state exceptions.

## Technical Setup: No Separate Approval

The exact server-owned `workspace_feature_branch_start` operation is the only `technical_setup` action. Once the user has named or authorized the work task, repository, and intended new feature branch, it may run without a separate approval. It must start from a clean current local default, bind the exact identity/repository/workspace/default branch, fetch the authoritative SHA, prove local-default ancestry, fast-forward the local default exactly with readback, prove the feature branch absent locally and remotely, create it at that same SHA, and read back branch plus HEAD. Ahead/diverged default state or any binding drift fails closed.

This exception never covers an arbitrary checkout/reset, an established-branch continuation, edits, stage, commit, amend, push, communication, or provider-state mutation. It cannot be generalized to another tool or repository.

While the feature branch has no remote branch, each exact commit/push preflight must fetch again and prove the current authoritative-default SHA remains an ancestor of the branch HEAD. If the default advanced or provenance is unproven, fail closed; this initial contract has no stale-base override. Once the exact branch is published, use the established-branch continuation bindings instead.

## Technical Grant

Resolve the repository policy class from the configured identity-bound instance: `work` or `personal`. Never infer it from the current user, task wording, repository visibility, or local Git author.

Each grant belongs to one immutable repository id, one exact workspace/Git dir, and one branch. Approval for repository A never applies to repository B in the same chat.

For a work repository, a technical grant may cover only established-branch continuation navigation, safe synchronization, and allowlisted validation retry. New-task bootstrap belongs only to the bounded `technical_setup` operation above. A work grant never covers stage, commit, amend, or push. Every work commit and every work push requires its own exact approval under [Work Commit And Push](#work-commit-and-push).

For a personal feature branch, a task-scoped grant may retain the ordinary stage/commit/amend/non-force-push loop. Direct commit/push to an unprotected default branch is allowed only when server-side policy explicitly names that personal repository. For an explicitly server-enabled personal protected default branch, a grant may cover local stage/commit/amend only; each normal non-force push requires its own exact approval bound to expected local/remote SHA plus authoritative readback. No PR/MR is required by this contract. Other protected/default repositories fail closed; work instances must keep both personal exceptions empty.

One short approval may cover an eligible technical loop only when bound to:

- provider/host plus provider-reported immutable account id and repository id;
- workspace realpath plus resolved Git-dir/common-dir identity;
- current task or named project slice;
- exact branch and repository policy class; work grants exclude stage/commit/amend/push, an unprotected personal default allows commit/push only by the explicit personal-repository exception, and an explicitly enabled personal protected default allows only local stage/commit/amend while every push remains excluded from the grant;
- exact allowed action set and repository-relative path allowlist;
- expected local HEAD SHA and remote branch SHA, including the expected absent-remote state for a new branch;
- short TTL, current process nonce, finite use cap, and monotonic use counter.

Treat the grant as ephemeral compare-and-swap state. Before every use, recheck all immutable bindings plus expected SHAs. After a successful use, authoritative readback may advance only the expected local/remote SHA and use counter. Any other drift, process restart, replay/duplicate use, stale SHA, TTL expiry, nonce mismatch, or exhausted use cap invalidates it and requires fresh approval.

There is no trusted cross-chat/session identifier in the current contract. Do not promise provable inter-chat isolation: keep grants in-process only, use a short TTL/process nonce/revocation flag/use cap, and require fresh approval after restart, handoff, compaction uncertainty, or any inability to prove continuity.

Within those bindings, a work-repository grant may cover:

- for continuation, verify and switch the exact established feature branch using its provider/upstream/local/remote SHA bindings without recreating or resetting it to the default branch;
- safe fast-forward synchronization that neither rewrites published history nor targets a protected branch;
- retry an allowlisted validation/test job for the same commit when it has no deploy, publish, release, environment, secret, or other side effect;
- inspect the resulting CI state and continue the technical fix loop.

Within those bindings, a personal-repository grant may additionally cover:

- create or switch the named local feature branch, or remain on an explicitly enabled personal default branch;
- stage exact task files and create normal commits;
- amend an unpushed task commit;
- normal non-force push to the exact granted branch and set its upstream when appropriate only while the target is unprotected;
- later technical commits and, while the target remains unprotected, normal pushes for the same task/branch.

The grant expires immediately when account, repository, task/project, branch, action class, protection state, target environment, or material payload scope changes. A repository-specific rule reserving branch/commit/push ownership to the user overrides the grant.

## Exact Approval

Require per-action exact approval for each named action, target, and payload. One confirmation may cover a presented batch only when every action is independently enumerated with its exact target and payload; it does not authorize later communication or administration.

Task ownership, MR/PR ownership, “continue”, “finish it”, or general implementation approval never substitutes for an `exact_approval` action such as a work commit or push. This does not add approval to the bounded `technical_setup` operation above.

### Work Commit And Push

Before each work-repository commit approval, present a concise chat checkpoint containing only:

- logical change summary;
- exact repository-relative file list;
- completed checks and material limits;
- proposed commit message;
- exact diff digest.

Keep the complete diff available internally and bind the approval to its digest; do not paste the full diff unless the user asks. Bind the approval also to provider/account/repository, workspace/Git-dir identity, task, feature branch, current HEAD/base SHA, exact file set, checks, and commit message. Any drift invalidates it. One approved commit action may stage the exact files and create one commit, then must read the resulting commit SHA back.

Request a separate push approval only after that commit exists. Bind it to the exact non-default feature branch, local commit SHA, expected remote SHA or expected absent branch, and provider protection state (`false`, `true`, or `unknown_until_creation`). The concise checkpoint must state that the history-preserving lease-CAS transport can use a configured credential whose protection-bypass capability is unproven; exact approval makes that risk explicit but does not prove provider-rule compliance. Recheck a known protection state before execution, reject its drift, and read back the authoritative remote SHA plus resulting protection state. Commit approval never pre-authorizes push, and push approval never carries to a later commit or push.

Every communication on the user's behalf requires this exact approval, including edits, reactions, assignments, and notification-causing metadata.

Communications:

- create a PR/MR, issue, discussion, or other published conversation;
- change PR/MR title, body, base, draft/ready state, or close/reopen state;
- post, edit, delete, or react to comments; reply to review; submit approval or request changes;
- assign reviewers/assignees, labels, milestones, mentions, or other notification-causing metadata.

CI, deploy, and publication:

- start a manual workflow/Jenkins job, submit a fresh re-run, stop/cancel work, or alter CI through provider APIs;
- run deploy/staging/production/environment jobs;
- create, move, or delete tags; publish, edit, or delete releases, notes, or assets.

Risky Git and lifecycle:

- create each commit or perform each push in a work repository, following the separate work approvals above;
- push to a protected branch, or to a default branch that lacks the explicit
  server-side personal-repository technical-grant exception;
- merge a PR/MR or perform a published-history squash/rebase;
- force push, delete a remote branch/tag, or discard user changes;
- create a fork or repository, or archive, rename, transfer, change visibility, or delete a repository.

For the explicitly server-enabled personal protected-default contour, one exact approval may authorize one normal non-force push from the named expected local SHA against the named expected remote SHA. Read authoritative branch state back after that push; every later push needs a new exact approval. This path does not require a PR/MR. Do not generalize it to another account, repository, branch, or work contour. Exact approval is necessary but not sufficient for any other protected/default push: when the bound server policy exposes no exact action, fail closed.

Control plane and administration:

- change `.github/workflows/**`, `.github/actions/**`, `.gitlab-ci.yml` or any resolved included CI file, any `CODEOWNERS` location, `.gitmodules`, `.gitattributes`, or repository-recognized deploy/infra/release/security control path; approval must name exact paths and the reviewed diff digest;
- change default branch, collaborators, teams, roles, permissions, or access requests;
- change branch protection, rulesets, required checks, bypass actors, merge policy, or security settings;
- create/update/delete secrets, variables, deploy keys, webhooks, environments, runners, integrations, or repository apps;
- change credential/token scopes, repository-tool configuration, MCP registration, identity binding, allowlists, or action policy.

For destructive, credential, secret, protection-bypass, permission, visibility, transfer, or repository-deletion actions, use two phases: read-only plan and impact/rollback preview, then exact approval, execution, and authoritative readback.

## Forbidden

Do not perform these even under an ordinary approval:

- retrieve, display, copy, log, or persist existing secret/token/private-key values;
- place credentials in repositories, skills, context, logs, prompts, or chat;
- operate as an unverified/wrong account or fall back to global CLI/Git Credential Manager after identity mismatch;
- for a work repository, fall back to raw Git, a provider CLI, global credentials, or another mutation tool when the configured identity-bound contour cannot execute a branch, commit, or push action;
- expose arbitrary provider API endpoints, GraphQL, shell, or raw command execution through repository MCP tools;
- execute wildcard or unresolved destructive targets;
- silently bypass protection, checks, review requirements, or identity allowlists;
- transfer any approval to another account, repository, task, branch, provider, or environment.
