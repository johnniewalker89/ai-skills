"""Bound Codex JSONL adapter; schema-specific envelopes, no private repository dependency."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

if __package__ in (None, ''):
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from accounting import counters, validate_snapshot


def read_child_session(session: Path, child_id: str, parent_id: str) -> dict:
    # Validate the first metadata record before examining any session counters.
    with session.open(encoding='utf-8') as stream:
        meta = json.loads(stream.readline())
        p = meta.get('payload', {})
        source = p.get('source')
        spawn = source.get('subagent', {}).get('thread_spawn', {}) if isinstance(source, dict) else {}
        if (not child_id or not parent_id or child_id == parent_id or meta.get('type') != 'session_meta' or p.get('id') != child_id
                or spawn.get('parent_thread_id') != parent_id):
            raise ValueError('child/parent identity mismatch; counters not read')
        state = {'child_id': child_id, 'parent_id': parent_id, 'started_at': p['timestamp'],
                 'model': None, 'effort': None, 'terminal': None, 'totals': None,
                 'usage_at': None, 'ended_at': None, 'exec_wrapper_failures': []}
        exec_calls = set()
        last_work = last_count = last_terminal = 0
        started_count = 0
        truncated = False
        for sequence, line in enumerate(stream, 1):
            if not line.endswith('\n'):
                truncated = True
                break  # Never certify a truncated stream as final.
            event = json.loads(line)
            payload = event.get('payload', {})
            if event.get('type') == 'response_item':
                # Read only envelope types, never project reasoning or tool payloads.
                if payload.get('type') not in ('custom_tool_call_output', 'function_call_output'):
                    last_work = sequence
                kind = payload.get('type')
                call_id = payload.get('call_id')
                if (kind == 'custom_tool_call' and payload.get('name') in ('exec', 'functions.exec')
                        and isinstance(call_id, str)):
                    exec_calls.add(call_id)
                elif kind == 'custom_tool_call_output' and call_id in exec_calls:
                    blocks = payload.get('output')
                    if isinstance(blocks, list):
                        texts = [block.get('text', '') for block in blocks
                                 if isinstance(block, dict) and block.get('type') == 'input_text'
                                 and isinstance(block.get('text', ''), str)]
                        if texts and texts[0].startswith('Script failed\n'):
                            error_type = 'WrapperError'
                            for text in texts:
                                match = re.match(r'Script error:\s*([A-Za-z]+Error):', text)
                                if match:
                                    error_type = match.group(1)
                                    break
                            state['exec_wrapper_failures'].append({
                                'kind': 'exec_wrapper_error', 'call_id': call_id,
                                'at': event.get('timestamp'), 'error_type': error_type})
            if event.get('type') == 'turn_context':
                last_work = sequence
                state.update(model=payload.get('model'), effort=payload.get('effort'))
            if event.get('type') != 'event_msg':
                continue
            kind = payload.get('type')
            if kind == 'task_started':
                started_count += 1
                if started_count > 1:
                    raise ValueError('reused child session needs an attempt-specific adapter and baseline')
                last_work = sequence
                state.update(terminal=None, ended_at=None, started_at=event['timestamp'])
            if kind in ('model_work_started', 'model_work_completed'):
                last_work = sequence
            if kind in ('task_complete', 'turn_aborted', 'task_aborted'):
                last_terminal = sequence
                state['terminal'] = kind
                state['ended_at'] = event.get('timestamp')
            if kind != 'token_count':
                continue
            counts = (payload.get('info') or {}).get('total_token_usage')
            if counts is None:
                continue
            values = counters(tuple(counts.get(k) for k in (
                'input_tokens', 'cached_input_tokens', 'output_tokens')))
            if state['totals'] and any(x < y for x, y in zip(values, state['totals'])):
                raise ValueError('token counter reset in session')
            last_count = sequence
            state.update(totals=values, usage_at=event.get('timestamp'))
    complete = bool(state['terminal'] and last_work and last_count > last_work
                    and last_terminal > last_work and not truncated)
    state['accounting_status'] = 'complete' if complete else ('unresolved' if state['terminal'] else 'pending')
    state['coverage_evidence'] = (f'codex-jsonl: counter record {last_count} follows last model envelope {last_work}; terminal observed' if complete else None)
    return validate_snapshot(state, child_id, parent_id)

def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--session', type=Path, required=True)
    parser.add_argument('--child-id', required=True)
    parser.add_argument('--parent-id', required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    if args.session.resolve() == args.output.resolve():
        parser.error('output must not overwrite session evidence')
    try:
        state = read_child_session(args.session, args.child_id, args.parent_id)
    except (OSError, ValueError, TypeError, KeyError) as error:
        parser.error(str(error))
    args.output.write_text(json.dumps(state, indent=2) + '\n', encoding='utf-8')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
