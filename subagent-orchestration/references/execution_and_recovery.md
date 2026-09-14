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
Honor explicit stops and access boundaries. At the working upper bound, send
FINISH and use the added25% for completion. Before it, narrow remaining research
to a useful partial result within the work budget. A missed draft or the lower
forecast being reached alone does not shorten that window. Finish earlier for
natural completion or a concrete blocker/failed path; record the reason. Budget overrun during protected
completion is recorded, not a reason to cancel that save. No new research, follow-up
after an explicit user stop or unapproved launch is authorized.

At the saved-result checkpoint, read the artifact and decide whether the remaining
work still fits. If it is absent or unusable, diagnose the cause and prioritize
a useful incremental save; do not automatically FINISH while useful work fits
below the working upper bound. Do not wait for headroom to discover missing proof.
An artifact repeating only scope and intended checks is not a successful useful
result checkpoint. Acknowledging its readback does not establish useful progress.
Keep budget observation active while assessing a checkpoint when the host permits;
otherwise allow for the whole observation-to-decision gap in the reserve and narrow
remaining work before it is consumed. A stopped watch followed by a lengthy parent
review leaves counters unobserved; its previous sample is not a current balance.
During reserve, save existing conclusions and gaps before expanding presentation.
Use explicit execution states:

1. **Working:** investigate within scope and update the useful report.
2. **Finishing:** at the working upper bound, enter the added headroom and send
   one clear instruction:
   stop new research, save existing findings/evidence/gaps and a continuation
   point, then report delivery. This transitions out of research; it is not an
   interrupt. The added allowance covers control latency, writes and bounded repair.
   Do not reserve it again by moving FINISH earlier. Latch protected completion
   when this instruction is sent or final saving is observed, whichever comes first.
   Keep that state across polling invocations and caller-specific deadlines.
3. **Saved:** read the report, verify the allowed path and assess what is useful.
   Preserve partial results and distinguish them from full acceptance.
4. **Delivered or stopped:** confirm the result/terminal state. During protected
   completion never interrupt for tokens, time, a missed useful-result deadline
   or unchanged counters. Saving, required readback and delivery may finish past
   the original cap; retain that cap and the actual overrun in reconciliation.
   Explicit user stops and access violations remain separate controls.

Protection covers saving existing findings/evidence/gaps and a continuation point,
not starting new research or expanding presentation. A partial draft's mere presence
does not establish final saving; use the finish instruction or visible current-phase
evidence for the bound child. Do not require a new ceremonial child message when
its final write is already observable. Before any budget interrupt, recheck the
phase; if unclear or a save call is in flight, request completion once and preserve
it. A stalled write/telemetry error requires diagnosis and retained evidence, not
an automatic budget kill. Do not impose a second timeout on protected saving.

Apply the completion guard after all caller policies, immediately before dispatch.
Never execute an old prepared interrupt after a new saving observation. Recheck
identity and phase at the dispatch boundary; invalidate queued budget stops when
completion starts. If the host enforces an unavoidable external hard cap, explain
that capability limit before launch and reserve earlier; instructions cannot
guarantee survival of a platform termination.

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

