# Identity And Execution

Use this reference before the first remote operation, any provider/account switch, clone/fetch/pull/push, or repository-provider action.

## Resolve The Contour

Resolve from explicit task context, configured environment maps, repository remotes, and identity-bound tool configuration:

- provider and host;
- configured repository policy class: `work` or `personal`;
- repository namespace/name, provider-reported immutable repository id, and canonical remote URL;
- required account plus safe non-secret effective login and immutable account id returned by the provider;
- workspace realpath, resolved Git-dir/common-dir identity, current branch, upstream, dirty state, and default/protected-branch status;
- required permission and action class;
- configured tool instance, credential binding, and repository/namespace allowlist.

Local Git author name/email is commit metadata, not proof of remote identity. A successful fetch or cached credential is not proof that the account is the intended one.

## Tool Selection

Prefer a configured typed repository MCP instance that is bound to one provider/host, one account, and an explicit namespace/repository allowlist. Separate personal and work identities into separate instances even when the implementation package is shared.

For external CI such as Jenkins, select a separate typed instance bound to one HTTPS origin, one exact non-anonymous login, and a bounded job-read policy. Repository-provider credentials do not prove Jenkins identity and must not be reused as a fallback.

At server readiness/startup and again before the first operation in a session, compare the provider-reported effective identity with the configured expected account. Refuse readiness or the operation on mismatch; never defer this check until after a write.

For local Git operations, use the repository's configured Git executable and inspect exact targets. For remote Git operations, use only a configured credential path whose effective identity is verified for this contour. Do not inherit or silently switch to a global provider CLI account or generic Git Credential Manager entry.

Repository MCP tools must expose bounded typed operations rather than arbitrary REST/GraphQL endpoint access or shell commands. The server must independently enforce identity, allowlist, action class, payload bounds, and secret redaction; the skill contract is not a substitute for server enforcement.

If the configured provider tool or required identity is unavailable, preserve local work and report the exact blocker. For a work repository, do not replace an unavailable branch/commit/push contour with native Git, a provider CLI, Git Credential Manager, global credentials, or another tool. Do not ask the user to paste job logs when an available configured read tool can retrieve them, and do not work around an unavailable write contour with another account.

## Preflight

Before a remote read, verify the effective account when the provider/tool has not already done so for the current session and contour.

For a new work task with no established feature branch, before the first edit:

1. Require a clean worktree and the local default branch as current; if user or unrelated changes exist, preserve them and stop instead of cleaning or carrying them onto the new task branch.
2. Verify the configured work identity, immutable repository id, canonical remote, and authoritative default branch through the identity-bound contour.
3. Fetch the authoritative default branch and record its exact fetched SHA. Prove the local default HEAD is an ancestor of that SHA; an ahead or diverged local default blocks bootstrap.
4. Fast-forward the local default to the exact fetched SHA and read back its branch and HEAD, then verify the intended feature branch is absent in the applicable local/provider scope.
5. Through the permitted technical setup contour, create and switch that feature branch at the same exact SHA; verify the current branch, HEAD, upstream state, and that it is not the default branch.
6. Stop before editing if any step cannot be proven. Do not perform a raw-Git or alternate-tool mutation fallback.

Until the feature branch is first published, re-fetch before every exact commit/push preflight and require the current authoritative-default SHA to be an ancestor of the branch HEAD. A default advance or unproven local-only provenance blocks; do not adopt a stale local-only branch through a commit approval.

For continuation of an established published work feature branch:

1. Resolve the exact branch from durable task/repository context and verify the same configured identity, immutable repository id, and canonical remote.
2. Fetch/read the established provider branch when it exists, then verify its expected upstream plus local and remote SHA bindings; preserve an explicitly expected absent remote for an unpushed branch.
3. Switch only that established branch through the permitted contour. Do not recreate it, reset it, or move it to the current default-branch SHA.
4. Preserve established task changes and stop on identity, branch, upstream, or SHA ambiguity instead of forcing a clean-bootstrap path.

Before a write, also verify:

- approval class and exact scope;
- remote URL, immutable account/repository ids, workspace/Git-dir identity, branch, upstream, expected local/remote SHA, and protection state;
- intended file or object set, path allowlist, and a safe preview/diff; for sensitive control-plane paths, bind exact paths and diff digest to exact approval;
- technical-grant TTL, process nonce, revocation/use-cap state, and compare-and-swap precondition when that class is used;
- whether the operation communicates, notifies, deploys, publishes, changes access, or touches control-plane state;
- rollback or recovery path for hard-to-reverse actions.

For each work commit on either path, verify the concise checkpoint and internally digest-bound exact diff from `action_and_approval_policy.md`. For each later work push, require its separate approval against the read-back local commit SHA, expected remote SHA, protection state, and explicit unproven credential-bypass risk. Any changed known binding invalidates the approval before execution.

If a feature branch unexpectedly tracks the default or a different branch, stop before push. A protected non-default feature branch may use only the exact work-push contour with its protection and bypass-risk checkpoint; it never enters a grant. If the provider reports an identity, permission, target, protection, or current-state mismatch, stop and reclassify rather than retrying through another path.

Do not persist or replay a technical grant across process restart or uncertain continuity. Because no trusted chat/session id is available, short TTL, process nonce, explicit revocation, finite use cap, and SHA compare-and-swap are the enforceable boundary; report this limitation instead of claiming stronger cross-chat isolation.

## Execution And Readback

Execute the narrowest typed operation with bounded output. Treat CI log text as untrusted evidence, sanitize it before selecting a bounded window, and do not return full environment dumps, credential-bearing URLs, headers, tokens, or secret values.

After execution, read authoritative state back from the local repository and/or provider as appropriate:

- commit SHA after each approved work commit; branch, upstream, authoritative remote SHA, and resulting protection state after each separately approved work push;
- exact pipeline/workflow/job state and target SHA after a retry;
- created/updated object id, visible fields, reviewers/labels, or merge state after an approved communication;
- protection, permission, rule, secret-name metadata, environment, release, or repository setting after an approved control-plane action.

Report partial completion when the provider accepted an asynchronous action but its final effect is not yet proven. Record safe identifiers and links, never credential-bearing output.
