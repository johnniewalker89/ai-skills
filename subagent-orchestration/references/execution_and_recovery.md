# Execution And Recovery

Read before launch, control, interruption or result reconciliation.

## Navigation

- [Saved result and reserve](#plan-the-saved-result)
- [Execution, measurement and reconciliation](#run-and-reconcile)

## Plan The Saved Result

Before launch, name the smallest independently useful artifact, its allowed path,
and a checkpoint comfortably before the completion reserve to inspect it. For
long artifact tasks, plan incremental saves inside the approved write set; the
first useful draft must not depend on writing every report or final summary.
File existence, size, tool activity and elapsed time are not semantic progress.

The first artifact is a growing domain report: what was checked, supported
findings, evidence links, gaps and the next useful step. A standalone checker or
output file is supporting evidence, not a substitute for an assessable report.
Expand that same report as work proceeds; the child need not duplicate the
parent's coordination log. For short tasks the saved result can be compact.

Check that the subject has a simple permitted way to save that artifact. Resolve
required shell/runtime/serialization boundaries before launch; verify an uncertain
write path with inert disposable content, without running a new agent or revealing
the answer. Do not spend the subject's task budget constructing a generic writer.
Size the reserve for the actual output volume, write-call latency and readback,
including a bounded repair; reserve time shorter than one expected write cannot
protect the result. Keep short tasks lightweight rather than requiring checkpoints
for every step.

If required startup consumes most of the forecast, narrow the work unit or remove
unnecessary inputs before proposing it. During execution compare actual startup
and progress with the remaining work, not just the hard ceiling. An early mismatch
requires a new feasibility decision inside the existing limits; it does not
authorize a larger budget, fresh retry, or a weaker acceptance criterion.

## Run And Reconcile

Give each approved agent a bounded question, the minimum sufficient raw evidence
and the owners needed for that question. Do not prescribe the conclusion.
Preserve the active direction's context, access limits and authorized write boundary.
Pass the agreed saved-result checkpoint and completion reserve to the subject;
these are execution instructions, never expected answers or scoring hints.

Before launch, verify monitor capability using existing evidence as described in
`token_accounting.md`. After the approved spawn, bind the actual child and check
its baseline/first sample by the agreed deadline. Missing future child records
before spawn is expected; an unverified reader capability is the launch blocker.
Use proportionate control: cheap counters or batched local sampling where available,
without a new main-agent inference per sample when the tool can handle it. Missing
telemetry during a run is an unresolved accounting failure, not zero. Recover
within the agreed allowance or finish/save/stop; time-only fallback does not
waive required numerical final accounting or authorize an unmetered launch.
Avoid using a recoverable sampling delay as a stop trigger by default.
Monitor visible execution failures and the named artifact as well as counters.
If the adapter only meters usage, arrange the missing progress/error checks
explicitly. At the first failed artifact-write invocation, inspect its actual
failure and preserve available work before funding another large attempt. A
known-broken serialization path is not progress because tokens are increasing.

At a diagnostic checkpoint, check progress, remaining cost and all applicable
ceilings. A late but valid sample alone does not require discarding a useful run;
continue only when the agreed controls and remaining budget support completion.
Honor explicit stops and access boundaries. If remaining work no longer fits,
stop starting new work and use the reserved allowance to save available evidence
and its gaps before the ceiling. Reserve is not extra authorization: no follow-up
after an agreed immediate stop, no unapproved launch and no spending past a cap.

At the saved-result checkpoint, read the artifact and decide whether the remaining
work still fits. If it is absent or unusable, prioritize a bounded partial save or
stop; do not wait for the final reserve to discover that nothing was preserved.
During reserve, save existing conclusions and gaps before expanding presentation.
Use explicit execution states:

1. **Working:** investigate within scope and update the useful report.
2. **Finishing:** send one clear instruction before the reserved save window:
   stop new research, save existing findings/evidence/gaps and a continuation
   point, then report delivery. An upper-forecast crossing prompts a feasibility
   check; it is not a hard stop. Leave enough token/time allowance for control
   latency, writes and bounded repair inside every approved ceiling.
3. **Saved:** read the report, verify the allowed path and assess what is useful.
   Preserve partial results and distinguish them from full acceptance.
4. **Delivered or stopped:** confirm the result/terminal state. Interrupt at an
   actual agreed hard boundary, explicit stop, access violation, or an
   unresponsive worker under the agreed fallback. Finishing is not permission
   to exceed a ceiling; do not send new work after an immediate stop.

Do not repeatedly issue the finishing instruction or keep sampling unchanged
status when the host can wait for relevant progress. An adapter may report both
budget action and attention: inspect the failure without forgetting the save
window. Control observations are not a guarantee against telemetry latency.
After interruption,
assess saved artifacts first. Before proposing another attempt, identify the cause,
what can be reused and a credible remaining-cost path to the required result.
Already spent tokens neither justify continuation nor make a restart economical.

Apply the agreed criteria to actual artifacts and relevant execution evidence,
not only an agent's final claim or confidence. Check findings against source/repro
artifacts; reject unsupported suggestions and reconcile disagreements by evidence.
The main agent owns the final decision. Record accepted/rejected findings, proof
gained, gaps and measured subagent cost separately. Complete the final counter
read and original forecast/cap comparison in `token_accounting.md`; missing
actuals keep accounting open even when useful task output is delivered.
Include resolved executor/reviewer
models/settings, host and input revision where known; mark unknowns explicitly.
Limit conclusions to that configuration and evidence; one successful run does not
prove reliability on every model, host or task. Low cost never upgrades weak proof.

