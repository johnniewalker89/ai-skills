# Bundled Counter Tools

Read before using `scripts/monitor.py`, `scripts/accounting.py` or a host adapter.
All ship inside this skill, use Python 3.12 standard library, and require no
private repository, context package or network service. Resolve the host's exact
Python executable and permitted input/output paths before running them.

## Navigation

- [Input contract](#normalized-snapshot)
- [Host adapter](#codex-jsonl-adapter)
- [Control](#monitor)
- [Plan versus actual](#reconciliation)

## Normalized Snapshot

An adapter must verify the selected child/parent binding before reading usage.
It projects the following JSON, without prompts, reasoning text or tool payloads:

```json
{
  "child_id": "child", "parent_id": "parent",
  "started_at": "2026-01-01T00:00:00Z", "ended_at": "2026-01-01T00:02:00Z",
  "model": "resolved-model-id", "effort": "resolved-setting",
  "terminal": "completed", "totals": [120000, 84000, 5300],
  "usage_at": "2026-01-01T00:01:59Z",
  "accounting_status": "complete",
  "coverage_evidence": "bound final-usage response or verified stream cutoff"
}
```

`totals` is cumulative `[input including cache, cached input, output]`; reasoning
already inside output is not added again. Missing counters are `null`, never
invented zeros. An adapter must normalize provider semantics; unavailable cache
data cannot silently become zero for metric U. This bundled counter format requires
all three values; a host without cache accounting needs a verified integration
for a different metric, not fabricated cache values. Do not switch metrics mid-run.
Timestamps require a timezone. `ended_at`, `terminal`, `usage_at`, model and effort
may be null when unavailable; counts require `usage_at`. Accounting status is
`pending` while working, `unresolved` when final coverage is missing, and `complete`
only after verified coverage through the last model work and observed termination.
The core validates the projection; it cannot authenticate an adapter's claim.
Keep the bound source evidence available and verify the adapter before launch.

## Codex JSONL Adapter

`scripts/adapters/codex_jsonl.py --session CHILD.jsonl --child-id CHILD_ID
--parent-id PARENT_ID --output snapshot.json` projects one permitted fresh child.
Pass these arguments on one command line with the resolved Python executable.
It checks `session_meta.payload.source.subagent.thread_spawn.parent_thread_id`
and the child ID, then reads cumulative `event_msg/token_count` counters.
It checks monotonic counters and does not sum snapshots. Final coverage requires
a token sample after the last model/input envelope, an observed terminal event
and no incomplete final JSON record. Completion alone or an early sample cannot
establish final usage. Recheck schema on the current host; replay is not live proof.
Repeated task starts are rejected: reused sessions need an attempt-aware adapter
with a verified baseline and attempt time boundaries. No session discovery scan
or main-agent metering occurs. Unknown/new host schemas need explicit integration.

## Monitor

`scripts/monitor.py` accepts either `--session CHILD.jsonl` for the bundled Codex
adapter or `--snapshot snapshot.json` from another trusted adapter. Supply
`--child-id`, `--parent-id`, `--limits limits.json`, `--result result.md` and
`--output control.json`. A normalized live adapter updates its snapshot atomically.
No flags launch, message or stop agents; the parent handles reported decisions.

Required limits are positive `finish_u`, `stop_u`, `finish_seconds`, `stop_seconds`,
`missing_seconds`; finish precedes stop, with missing allowance inside stop time.
U is uncached input plus output. Optional paired `finish_t`/`stop_t` add explicit
cache-inclusive controls; absent/null pairs leave T diagnostic. Do not silently
add a second stop. Paired `checkpoint_u`/`checkpoint_seconds` precede finish;
`--progress-artifact` chooses the first useful draft when it differs from result.
Presence/hash/size ask for semantic readback; they never prove useful progress.

`--watch-seconds 40 --interval 5` performs bounded local sampling (maximum 45s,
interval at most 20s). JSON output and its JSONL companion retain observations.
`continue`/`waiting` need another watch; `finish` requests saving within the reserve;
`stop` needs the parent's stop tool. After one finish message, `--finishing` keeps
sampling. `review` yields on a saved-result checkpoint or visible execution error.
After inspecting only the named error/checkpoint, use `--reviewed-call-id ID` or
`--checkpoint-reviewed`. These acknowledgements grant no retry or new spending.
The Codex adapter recognizes visible `functions.exec` wrapper failures only;
other tool/domain errors and useful progress require parent checks.

`done` describes lifecycle, while `accounting_status` independently describes
final counter coverage. Neither proves task acceptance. `usage` may remain the
last observation in an unresolved attempt. Control thresholds are observations,
not a hard spending cap; delayed samples/in-flight work require reserved margin.
Malformed/identity-mismatched inputs fail closed; reports cannot overwrite inputs.

## Reconciliation

`scripts/accounting.py --input attempt.json --output reconciliation.json` expects:

```json
{
  "child_id": "child", "parent_id": "parent",
  "plan": {
    "metric": "U", "forecast_low": 25000, "forecast_high": 40000,
    "ceiling": 50000, "elapsed_seconds": {"low": 90, "high": 180, "ceiling": 225}
  },
  "snapshot": {},
  "baseline": [0, 0, 0]
}
```

Replace `snapshot` with the verified projection above. Omit baseline for a fresh
child; a reused attempt needs verified pre-attempt counters and matching time
boundaries. The original plan is retained unchanged; revised limits need a
separate comparison. The result includes numeric actual, actual-minus-upper,
remaining-to-ceiling, cap compliance and elapsed time. Missing final coverage
keeps actual/deviations/compliance null and returns exit 2; observed usage remains
explicitly partial. Exit 0 means complete accounting, not good forecast or accepted
work. Include every failed attempt in batch totals; if any final actual is missing,
the batch total and batch cap compliance remain unresolved. Add the evidence-backed
planning lesson to the result/log; the calculator cannot infer why a task cost more.

Run regressions with the resolved Python: `-B -m unittest discover -s
<skill>/scripts/tests -p test_*.py`. They cover identity, cumulative/baseline math,
final coverage, partial output, controls, CLI safety and standalone package use.
