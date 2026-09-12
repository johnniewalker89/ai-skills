"""Portable cumulative counters and plan/actual reconciliation; Python 3.12 stdlib."""

from __future__ import annotations

import argparse
import json
import math
from datetime import datetime
from pathlib import Path


def counters(values: object) -> tuple[int, int, int]:
    """Validate input (including cache), cached input, output; reasoning is in output."""
    if not isinstance(values, (list, tuple)) or len(values) != 3:
        raise ValueError('expected three token counters')
    if any(type(v) is not int or v < 0 for v in values) or values[1] > values[0]:
        raise ValueError('invalid token counters')
    return tuple(values)


def usage(values: object, baseline: object = (0, 0, 0)) -> dict[str, int]:
    final, initial = counters(values), counters(baseline)
    delta = counters(tuple(x - y for x, y in zip(final, initial)))
    return {'input': delta[0], 'cached_input': delta[1], 'output': delta[2],
            'U': delta[0] - delta[1] + delta[2], 'T': delta[0] + delta[2]}


def timestamp(value: str) -> datetime:
    result = datetime.fromisoformat(value.replace('Z', '+00:00'))
    if result.tzinfo is None:
        raise ValueError('timestamps must include a timezone')
    return result


def validate_snapshot(state: dict, child_id: str, parent_id: str) -> dict:
    """Validate a projection supplied by a trusted host adapter, not agent estimates."""
    if not isinstance(state, dict):
        raise ValueError('snapshot must be an object')
    if (not child_id or not parent_id or child_id == parent_id
            or state.get('child_id') != child_id or state.get('parent_id') != parent_id):
        raise ValueError('child/parent identity mismatch; counters not read')
    start = timestamp(state['started_at'])
    if state.get('ended_at') and timestamp(state['ended_at']) < start:
        raise ValueError('end precedes start')
    if state.get('totals') is not None:
        counters(state['totals'])
        if not state.get('usage_at') or timestamp(state['usage_at']) < start:
            raise ValueError('missing or invalid counter timestamp')
    if state.get('accounting_status') not in ('pending', 'complete', 'unresolved'):
        raise ValueError('invalid accounting status')
    if state['accounting_status'] == 'complete':
        if (not state.get('terminal') or not state.get('ended_at')
                or state.get('totals') is None or not state.get('coverage_evidence')):
            raise ValueError('complete accounting requires final coverage evidence')
    return state


def comparison(low: int | float, high: int | float, ceiling: int | float,
               actual: int | float | None) -> dict:
    values = (low, high, ceiling)
    if any(type(v) not in (int, float) or not math.isfinite(v) for v in values):
        raise ValueError('forecast and ceiling must be finite numbers')
    if not 0 <= low <= high <= ceiling or ceiling <= 0:
        raise ValueError('expected 0 <= forecast low <= high <= positive ceiling')
    return {'forecast_low': low, 'forecast_high': high, 'ceiling': ceiling,
            'actual': actual, 'delta_from_upper': None if actual is None else actual - high,
            'remaining_to_ceiling': None if actual is None else ceiling - actual,
            'cap_met': None if actual is None else actual <= ceiling}


def reconcile(record: dict) -> dict:
    if not isinstance(record, dict) or not isinstance(record.get('plan'), dict):
        raise ValueError('reconciliation requires a record and plan object')
    plan = record['plan']
    state = validate_snapshot(record['snapshot'], record['child_id'], record['parent_id'])
    metric = plan['metric']
    if metric not in ('U', 'T'):
        raise ValueError('supported metrics: U (uncached input + output), T (input + output)')
    observed = (usage(state['totals'], record.get('baseline', (0, 0, 0)))
                if state.get('totals') is not None else None)
    complete = state['accounting_status'] == 'complete'
    elapsed = ((timestamp(state['ended_at']) - timestamp(state['started_at'])).total_seconds()
               if state.get('ended_at') else None)
    actual = observed[metric] if complete else None
    return {'child_id': record['child_id'], 'parent_id': record['parent_id'],
            'accounting_status': state['accounting_status'], 'metric': metric,
            'tokens': comparison(plan['forecast_low'], plan['forecast_high'], plan['ceiling'], actual),
            'elapsed_seconds': comparison(**plan['elapsed_seconds'], actual=elapsed),
            'observed_usage': observed, 'actual_usage': observed if complete else None,
            'coverage_evidence': state.get('coverage_evidence'),
            'model': state.get('model'), 'effort': state.get('effort')}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    if args.input.resolve() == args.output.resolve():
        parser.error('output must not overwrite input evidence')
    try:
        report = reconcile(json.loads(args.input.read_text(encoding='utf-8')))
    except (OSError, ValueError, TypeError, KeyError) as error:
        parser.error(str(error))
    args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(report, ensure_ascii=False))
    return 0 if report['accounting_status'] == 'complete' else 2


if __name__ == '__main__':
    raise SystemExit(main())
