"""Read one bound child snapshot or supported host session; emit decisions, never launch or stop agents."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import time
from accounting import usage, validate_snapshot
from adapters.codex_jsonl import read_child_session
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path


@dataclass(frozen=True)
class Limits:
    finish_u: int
    stop_u: int
    finish_t: int | None
    stop_t: int | None
    finish_seconds: int
    stop_seconds: int
    missing_seconds: int
    checkpoint_u: int | None = None
    checkpoint_seconds: int | None = None

    def __post_init__(self) -> None:
        if any(type(value) is not int for value in self.__dict__.values() if value is not None):
            raise ValueError('limits must be integer counters and seconds')
        for low, high in ((self.finish_u, self.stop_u),
                          (self.finish_seconds, self.stop_seconds)):
            if not 0 < low < high:
                raise ValueError("finish thresholds must be positive and below stops")
        if (self.finish_t is None) != (self.stop_t is None):
            raise ValueError("both total-token thresholds are required when enabled")
        if self.finish_t is not None and not 0 < self.finish_t < self.stop_t:
            raise ValueError("total-token thresholds must be positive and below stops")
        if not 0 < self.missing_seconds < self.stop_seconds:
            raise ValueError("invalid missing-telemetry allowance")
        if (self.checkpoint_u is None) != (self.checkpoint_seconds is None):
            raise ValueError("both saved-result checkpoint thresholds are required")
        if self.checkpoint_u is not None:
            if not 0 < self.checkpoint_u < self.finish_u:
                raise ValueError("checkpoint tokens must precede the finish reserve")
            if not 0 < self.checkpoint_seconds < self.finish_seconds:
                raise ValueError("checkpoint time must precede the finish reserve")


class Monitor:
    def __init__(self, child_id: str, parent_id: str, limits: Limits, *,
                 reviewed_call_ids: tuple[str, ...] = (),
                 checkpoint_reviewed: bool = False, source_format: str = 'codex-jsonl') -> None:
        if child_id == parent_id:
            raise ValueError("a parent session is not a subject")
        if source_format not in ('codex-jsonl', 'normalized'):
            raise ValueError('unsupported adapter format')
        self.source_format = source_format
        self.child_id = child_id
        self.parent_id = parent_id
        self.limits = limits
        self.previous: tuple[int, int, int] | None = None
        self.missing_since: float | None = None
        self.reviewed_call_ids = set(reviewed_call_ids)
        self.checkpoint_reviewed = checkpoint_reviewed

    def sample(self, session: Path, result: Path, now: datetime, *,
               progress_artifact: Path | None = None) -> dict:
        state = (read_child_session(session, self.child_id, self.parent_id)
                 if self.source_format == 'codex-jsonl' else validate_snapshot(
                     json.loads(session.read_text(encoding='utf-8')), self.child_id, self.parent_id))
        end = datetime.fromisoformat(state.pop('ended_at').replace('Z', '+00:00')) if state.get('ended_at') else now
        state.pop('ended_at', None)
        elapsed = max(0.0, (end - datetime.fromisoformat(
            state['started_at'].replace('Z', '+00:00'))).total_seconds())
        totals = state.pop('totals')
        reason = None
        if totals is not None:
            if self.previous and any(x < y for x, y in zip(totals, self.previous)):
                reason = 'counter_reset'
            self.previous = totals
            self.missing_since = None
        else:
            if self.missing_since is None:
                self.missing_since = elapsed if self.previous else 0.0
        measured = usage(totals) if totals is not None else None
        u, t = (measured['U'], measured['T']) if measured else (None, None)
        evidence = self._artifact(result)
        progress = evidence if progress_artifact is None else self._artifact(progress_artifact)
        failures = state.pop('exec_wrapper_failures', [])
        attention = [failure for failure in failures
                     if failure['call_id'] not in self.reviewed_call_ids]
        checkpoint_due = (self.limits.checkpoint_u is not None and (
            elapsed >= self.limits.checkpoint_seconds
            or u is not None and u >= self.limits.checkpoint_u))
        if checkpoint_due and not self.checkpoint_reviewed:
            attention.append({'kind': 'saved_result_checkpoint',
                              'artifact_path': str(progress_artifact or result),
                              'artifact_present': progress is not None,
                              'requires': 'orchestrator semantic readback and remaining-work decision'})
        action = 'continue'
        if reason:
            action = 'stop'
        elif state['terminal']:
            action, reason = 'done', state['terminal']
        elif elapsed >= self.limits.stop_seconds:
            action, reason = 'stop', 'elapsed_limit'
        elif u is not None and (u >= self.limits.stop_u or (
                self.limits.stop_t is not None and t >= self.limits.stop_t)):
            action, reason = 'stop', 'token_limit'
        elif totals is None:
            if elapsed - self.missing_since >= self.limits.missing_seconds:
                action, reason = 'stop', 'telemetry_unavailable'
            else:
                action, reason = 'waiting', 'telemetry_pending'
        elif (u >= self.limits.finish_u or (
                self.limits.finish_t is not None and t >= self.limits.finish_t)
              or elapsed >= self.limits.finish_seconds):
            action, reason = 'finish', 'completion_reserve'
        budget_action = action
        if action in ('continue', 'waiting') and attention:
            action, reason = 'review', attention[0]['kind']
        return {**state, 'sampled_at': now.isoformat(), 'elapsed_seconds': elapsed,
                'usage': measured,
                'action': action, 'reason': reason, 'budget_action': budget_action,
                'total_token_limit_enabled': self.limits.stop_t is not None,
                'result': evidence, 'progress_artifact': progress,
                'attention': attention,
                'error_coverage': ('visible functions.exec wrapper failures only; not all tool/domain errors'
                                   if self.source_format == 'codex-jsonl' else
                                   'host adapter observations only; parent checks tool/domain errors')}

    @staticmethod
    def _artifact(path: Path) -> dict | None:
        if not path.is_file():
            return None
        raw = path.read_bytes()
        return {'path': str(path), 'bytes': len(raw),
                'sha256': hashlib.sha256(raw).hexdigest()}




def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    inputs = parser.add_mutually_exclusive_group(required=True)
    inputs.add_argument('--session', type=Path, help='bound Codex JSONL session')
    inputs.add_argument('--snapshot', type=Path, help='normalized snapshot from a trusted host adapter')
    parser.add_argument('--child-id', required=True)
    parser.add_argument('--parent-id', required=True)
    parser.add_argument('--limits', type=Path, required=True)
    parser.add_argument('--result', type=Path, required=True)
    parser.add_argument('--progress-artifact', type=Path,
                        help='approved first useful saved artifact; defaults to result')
    parser.add_argument('--reviewed-call-id', action='append', default=[],
                        help='a visible wrapper failure already examined by the orchestrator')
    parser.add_argument('--checkpoint-reviewed', action='store_true',
                        help='orchestrator has inspected checkpoint evidence and recorded its decision')
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--watch-seconds', type=float, default=0)
    parser.add_argument('--interval', type=float, default=5)
    parser.add_argument('--finishing', action='store_true', help='reserve message already sent; keep sampling')
    args = parser.parse_args()
    if (not math.isfinite(args.watch_seconds) or not math.isfinite(args.interval)
            or not 0 <= args.watch_seconds <= 45 or not 0 < args.interval <= 20):
        parser.error('watch must be 0..45 seconds; interval must be 0..20')
    source_path = args.session or args.snapshot
    protected = {source_path.resolve(), args.result.resolve(), args.limits.resolve()}
    if args.progress_artifact is not None:
        protected.add(args.progress_artifact.resolve())
    if args.output.suffix != '.json' or any(p.resolve() in protected for p in (
            args.output, args.output.with_suffix('.jsonl'))):
        parser.error('report must not overwrite session, limits or subject result')
    configured_limits = {'finish_t': None, 'stop_t': None,
                         **json.loads(args.limits.read_text(encoding='utf-8'))}
    monitor = Monitor(args.child_id, args.parent_id,
                      Limits(**configured_limits),
                      reviewed_call_ids=tuple(args.reviewed_call_id),
                      checkpoint_reviewed=args.checkpoint_reviewed,
                      source_format='codex-jsonl' if args.session else 'normalized')
    deadline = time.monotonic() + args.watch_seconds
    args.output.parent.mkdir(parents=True, exist_ok=True)
    while True:
        try:
            report = monitor.sample(source_path, args.result, datetime.now(timezone.utc),
                                    progress_artifact=args.progress_artifact)
        except (OSError, ValueError, KeyError, TypeError) as error:
            report = {'child_id': args.child_id, 'action': 'stop',
                      'reason': 'invalid_session_or_telemetry', 'error': str(error)}
        args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
        with args.output.with_suffix('.jsonl').open('a', encoding='utf-8') as stream:
            stream.write(json.dumps(report, ensure_ascii=False) + '\n')
        remaining = deadline - time.monotonic()
        if (report['action'] in ('stop', 'done', 'review')
                or report['action'] == 'finish' and not args.finishing or remaining <= 0):
            print(json.dumps(report, ensure_ascii=False), flush=True)
            return 2 if report['action'] == 'stop' else 0
        time.sleep(min(args.interval, remaining))


if __name__ == '__main__':
    raise SystemExit(main())
