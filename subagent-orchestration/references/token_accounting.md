# Required Token Accounting

Plan, measured actuals and their comparison are required for every subagent
attempt. A useful report alone does not complete the accounting. This contract
applies to every caller, including Engineering, Game and direct invocation;
optional audit logging changes storage, not the requirement to retain these facts.

## Establish Measurement Before Launch

This skill ships its calculator, monitor and supported host adapters under
`scripts/`; read `counter_tools.md` before using them. No separate private tool
installation is required. A missing bundled file is a broken/incomplete skill
installation; a missing adapter is an integration gap. Neither proves the host
has no counters. Actual telemetry can be unavailable when the host exposes no
per-child usage endpoint or accessible records, or permitted access excludes them.

Check the host's permitted child-specific sources: tool usage responses,
configured adapters and local session records when available. Absence of counters
in a delegation tool is not evidence that the host has no telemetry. Reuse a
known working adapter or perform bounded discovery in allowed configuration;
do not import another direction's context, inspect unrelated sessions, collect
main/account usage or launch a test child merely to discover a counter source.

Preflight verifies the reader's capability against an existing permitted child
record or an authoritative host capability. It does not measure a future child:
that child's ID, session file and first counter cannot exist before spawn and
must never be prerequisites for calling spawn. Bind the metric, identity
matching, baseline, sampling/final-read procedure, permitted paths, update delay
and first-sample deadline to the proposed batch. Recorded replay proves parsing,
not timely live delivery. After the approved spawn returns, bind the actual child/parent IDs and
check the first real sample by that deadline. Separate exact usage measurement
from a hard spending cap: in-flight work and reporting latency still need reserves.

If no verified measurement source exists, block the dependent launch and state
the missing capability. Time/artifact fallback does not satisfy token accounting
or make that batch launch-ready. General permission to proceed does not waive
this requirement. Continue useful direct work that does not depend on delegation.

## Identity And Counts

Read only the selected child's counters after verifying its immutable identity
and parent/task binding. For cumulative records retain input, cached input,
output, timestamps, model/effort and source evidence. Use the last valid final
total once; do not sum cumulative snapshots or add reasoning already included
in output. With the usual metric, actual = input - cached input + output;
cache-inclusive totals remain separate diagnostics. A reused session needs the
verified pre-attempt baseline; a reset, malformed record or identity mismatch
is an error, not zero usage. A failed launch counts as zero only when evidence
proves no child execution or charge occurred.

On Codex hosts with permitted JSONL session records, the bundled adapter binds
`session_meta` child/parent identity and read `event_msg` / `token_count` /
`info.total_token_usage`. Verify the current schema and matching record before
using it. These fields do not require a particular private repository, path or
workflow. Other hosts supply the normalized contract to the same calculator
and monitor; the Codex adapter is optional. Do not expose hidden reasoning or
unrelated session content.

## Loss, Final Read And Planning Lesson

During telemetry loss, preserve the last valid measurement, diagnose within the
agreed allowance, and finish/save/stop before the protected boundary if recovery
does not fit. `Unknown` is an honest temporary failure state; it is never a
successful substitute for actuals. Do not fund an automatic continuation or
replacement with the same unresolved measurement gap.

After delivery, failure or interruption, read the final counters and establish
coverage through the last executed model work; lifecycle completion alone does
not prove a final counter. Recover missing data from the bound source. If it
remains unavailable, return useful work with accounting explicitly unresolved
and leave the affected accounting/debt open. Never invent exact usage from time.

Save original forecast range, headroom and ceiling beside numeric actuals,
elapsed time, actual-minus-upper-forecast and remaining-to-ceiling (or overrun).
Compare revised limits separately without rewriting the original approval.
State what caused a material miss, which phase estimate should change and what
remains uncalibrated; do not lower headroom from one good result. Keep failed
attempts in totals and distinguish useful delivery from forecast accuracy.

With logs enabled, append the reconciliation and evidence link to each attempt
and update its facts index. With logs off, save the same required facts in the
existing result/test surface. A retrospective recovery is dated as a backfill;
it does not prove live monitoring happened during the original run.
