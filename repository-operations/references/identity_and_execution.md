# Identity And Execution

Use this reference before the first remote operation, any provider/account switch, clone/fetch/pull/push, or repository-provider action.

## Resolve The Contour

Resolve from explicit task context, configured environment maps, repository remotes, and identity-bound tool configuration:

- provider and host;
- repository namespace/name, provider-reported immutable repository id, and canonical remote URL;
- required account plus safe non-secret effective login and immutable account id returned by the provider;
- workspace realpath, resolved Git-dir/common-dir identity, current branch, upstream, dirty state, and default/protected-branch status;
- required permission and action class;
- configured tool instance, credential binding, and repository/namespace allowlist.

Local Git author name/email is commit metadata, not proof of remote identity. A successful fetch or cached credential is not proof that the account is the intended one.

## Tool Selection

Prefer a configured typed repository MCP instance that is bound to one provider/host, one account, and an explicit namespace/repository allowlist. Separate personal and work identities into separate instances even when the implementation package is shared.

At server readiness/startup and again before the first operation in a session, compare the provider-reported effective identity with the configured expected account. Refuse readiness or the operation on mismatch; never defer this check until after a write.

For local Git operations, use the repository's configured Git executable and inspect exact targets. For remote Git operations, use only a configured credential path whose effective identity is verified for this contour. Do not inherit or silently switch to a global provider CLI account or generic Git Credential Manager entry.

Repository MCP tools must expose bounded typed operations rather than arbitrary REST/GraphQL endpoint access or shell commands. The server must independently enforce identity, allowlist, action class, payload bounds, and secret redaction; the skill contract is not a substitute for server enforcement.

If the configured provider tool or required identity is unavailable, preserve local work and report the exact remote blocker. Do not ask the user to paste job logs when an available configured read tool can retrieve them, and do not work around an unavailable write contour with another account.

## Preflight

Before a remote read, verify the effective account when the provider/tool has not already done so for the current session and contour.

Before a write, also verify:

- approval class and exact scope;
- remote URL, immutable account/repository ids, workspace/Git-dir identity, branch, upstream, expected local/remote SHA, and protection state;
- intended file or object set, path allowlist, and a safe preview/diff; for sensitive control-plane paths, bind exact paths and diff digest to exact approval;
- technical-grant TTL, process nonce, revocation/use-cap state, and compare-and-swap precondition when that class is used;
- whether the operation communicates, notifies, deploys, publishes, changes access, or touches control-plane state;
- rollback or recovery path for hard-to-reverse actions.

If a feature branch unexpectedly tracks a default/protected branch, stop before push. If the provider reports an identity, permission, target, protection, or current-state mismatch, stop and reclassify rather than retrying through another path.

Do not persist or replay a technical grant across process restart or uncertain continuity. Because no trusted chat/session id is available, short TTL, process nonce, explicit revocation, finite use cap, and SHA compare-and-swap are the enforceable boundary; report this limitation instead of claiming stronger cross-chat isolation.

## Execution And Readback

Execute the narrowest typed operation with bounded output. Sanitize job logs and artifacts; do not return full environment dumps, credential-bearing URLs, headers, tokens, or secret values.

After execution, read authoritative state back from the local repository and/or provider as appropriate:

- commit SHA, branch and upstream after commit/push;
- exact pipeline/workflow/job state and target SHA after a retry;
- created/updated object id, visible fields, reviewers/labels, or merge state after an approved communication;
- protection, permission, rule, secret-name metadata, environment, release, or repository setting after an approved control-plane action.

Report partial completion when the provider accepted an asynchronous action but its final effect is not yet proven. Record safe identifiers and links, never credential-bearing output.
