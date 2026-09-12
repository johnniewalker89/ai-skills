"""Counter semantics, incomplete final evidence and standalone public package regressions."""

import copy
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from accounting import reconcile, usage, validate_snapshot
from adapters.codex_jsonl import read_child_session
from monitor import Limits, Monitor
from datetime import datetime, timezone


def snapshot():
    return {'child_id': 'child', 'parent_id': 'parent',
            'started_at': '2026-01-01T00:00:00Z', 'ended_at': '2026-01-01T00:02:00Z',
            'totals': [120000, 84000, 5300], 'usage_at': '2026-01-01T00:01:59Z',
            'terminal': 'completed', 'accounting_status': 'complete',
            'coverage_evidence': 'host final usage response for the bound completed attempt',
            'model': 'vendor-current-small', 'effort': 'medium'}


def record():
    return {'child_id': 'child', 'parent_id': 'parent', 'snapshot': snapshot(),
            'plan': {'metric': 'U', 'forecast_low': 25000, 'forecast_high': 40000,
                     'ceiling': 50000, 'elapsed_seconds': {'low': 90, 'high': 180, 'ceiling': 225}}}


class AccountingTests(unittest.TestCase):
    def test_actual_and_deviations_do_not_modify_plan(self):
        source = record()
        original = copy.deepcopy(source)
        result = reconcile(source)
        self.assertEqual(source, original)
        self.assertEqual(result['tokens']['actual'], 41300)
        self.assertEqual(result['tokens']['delta_from_upper'], 1300)
        self.assertEqual(result['tokens']['remaining_to_ceiling'], 8700)
        self.assertTrue(result['tokens']['cap_met'])
        self.assertEqual(result['elapsed_seconds']['actual'], 120)

    def test_baseline_and_metrics_are_separate(self):
        source = record()
        source['baseline'] = [10000, 8000, 1000]
        source['plan']['metric'] = 'T'
        result = reconcile(source)
        self.assertEqual(result['actual_usage']['U'], 38300)
        self.assertEqual(result['tokens']['actual'], 114300)
        self.assertFalse(result['tokens']['cap_met'])

    def test_partial_counter_is_not_final_actual_or_cap_proof(self):
        source = record()
        source['snapshot'].update(accounting_status='unresolved', coverage_evidence=None)
        result = reconcile(source)
        self.assertEqual(result['observed_usage']['U'], 41300)
        self.assertIsNone(result['actual_usage'])
        for name in ('actual', 'delta_from_upper', 'remaining_to_ceiling', 'cap_met'):
            self.assertIsNone(result['tokens'][name])

    def test_missing_counter_is_not_zero(self):
        source = record()
        source['snapshot'].update(totals=None, usage_at=None, accounting_status='unresolved')
        self.assertIsNone(reconcile(source)['observed_usage'])
        source['snapshot']['accounting_status'] = 'complete'
        with self.assertRaises(ValueError):
            reconcile(source)

    def test_real_zero_is_numeric(self):
        source = record()
        source['snapshot']['totals'] = [0, 0, 0]
        self.assertEqual(reconcile(source)['tokens']['actual'], 0)

    def test_invalid_counters_and_resets_fail(self):
        for totals in ([10, 11, 0], [-1, 0, 0], [True, 0, 0], [1.0, 0, 0], [1, None, 0], [1, 0]):
            with self.subTest(totals=totals), self.assertRaises(ValueError):
                usage(totals)
        with self.assertRaises(ValueError):
            usage([10, 5, 1], [20, 5, 1])

    def test_bad_plan_and_metric_fail(self):
        for key, value in [('ceiling', 30000), ('forecast_low', -1),
                           ('forecast_high', float('nan')), ('metric', 'money')]:
            source = record()
            source['plan'][key] = value
            with self.subTest(key=key), self.assertRaises(ValueError):
                reconcile(source)

    def test_identity_checked_before_counters(self):
        state = snapshot()
        state.update(child_id='unrelated', totals='bad')
        with self.assertRaisesRegex(ValueError, 'identity mismatch'):
            validate_snapshot(state, 'child', 'parent')

    def test_malformed_json_shapes_fail_cleanly(self):
        for value in (None, [], 7, 'text'):
            with self.subTest(value=value), self.assertRaises(ValueError):
                validate_snapshot(value, 'child', 'parent')
            with self.subTest(value=value), self.assertRaises(ValueError):
                reconcile(value)

    def test_final_requires_evidence_and_timezone(self):
        for key, value in [('coverage_evidence', None), ('terminal', None),
                           ('usage_at', None), ('started_at', '2026-01-01T00:00:00')]:
            state = snapshot()
            state[key] = value
            with self.subTest(key=key), self.assertRaises(ValueError):
                validate_snapshot(state, 'child', 'parent')

    def test_normalized_host_monitor_has_no_codex_session_requirement(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / 'snapshot.json'
            path.write_text(json.dumps(snapshot()), encoding='utf-8')
            monitor = Monitor('child', 'parent', Limits(45000, 55000, None, None, 180, 225, 60),
                              source_format='normalized')
            result = monitor.sample(path, Path(tmp) / 'result.md', datetime.now(timezone.utc))
            self.assertEqual(result['usage']['U'], 41300)
            self.assertEqual(result['accounting_status'], 'complete')

    def test_copied_skill_runs_without_private_repo_or_dependencies(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            skill = root / 'installed-skill'
            shutil.copytree(Path(__file__).resolve().parents[2], skill,
                            ignore=shutil.ignore_patterns('__pycache__'))
            source, output = root / 'input.json', root / 'output.json'
            source.write_text(json.dumps(record()), encoding='utf-8')
            command = [sys.executable, '-B', str(skill / 'scripts/accounting.py'),
                       '--input', str(source), '--output', str(output)]
            run = subprocess.run(command, cwd=root, text=True, capture_output=True)
            self.assertEqual(run.returncode, 0, run.stderr)
            self.assertEqual(json.loads(output.read_text())['tokens']['actual'], 41300)
            command[-1] = str(source)
            original = source.read_bytes()
            self.assertEqual(subprocess.run(command, capture_output=True).returncode, 2)
            self.assertEqual(source.read_bytes(), original)


class CodexCoverageTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.path = Path(self.tmp.name) / 'session.jsonl'
        self.rows = [{'type': 'session_meta', 'payload': {'id': 'child',
                     'timestamp': '2026-01-01T00:00:00Z',
                     'source': {'subagent': {'thread_spawn': {'parent_thread_id': 'parent'}}}}}]

    def add(self, kind, payload):
        self.rows.append({'type': kind, 'timestamp': '2026-01-01T00:01:00Z', 'payload': payload})

    def count(self, value):
        self.add('event_msg', {'type': 'token_count', 'info': {'total_token_usage': {
            'input_tokens': value, 'cached_input_tokens': 0, 'output_tokens': 10,
            'reasoning_output_tokens': 5}}})

    def read(self, partial=False):
        self.path.write_text(''.join(json.dumps(row) + '\n' for row in self.rows)
                             + ('{"type":' if partial else ''), encoding='utf-8')
        return read_child_session(self.path, 'child', 'parent')

    def test_final_counter_follows_work_and_is_not_sum_of_snapshots(self):
        self.count(100)
        self.add('response_item', {'type': 'message', 'role': 'assistant', 'content': 'private'})
        self.count(200)
        self.add('event_msg', {'type': 'task_complete'})
        state = self.read()
        self.assertEqual(usage(state['totals'])['U'], 210)
        self.assertEqual(state['accounting_status'], 'complete')
        self.assertNotIn('private', json.dumps(state))

    def test_completion_without_new_count_does_not_certify_stale_sample(self):
        self.count(100)
        self.add('response_item', {'type': 'message', 'role': 'assistant'})
        self.add('event_msg', {'type': 'task_complete'})
        self.assertEqual(self.read()['accounting_status'], 'unresolved')

    def test_partial_tail_cannot_certify_final(self):
        self.add('response_item', {'type': 'message', 'role': 'assistant'})
        self.count(100)
        self.add('event_msg', {'type': 'task_complete'})
        self.assertEqual(self.read(partial=True)['accounting_status'], 'unresolved')

    def test_reused_session_needs_explicit_attempt_adapter(self):
        self.add('event_msg', {'type': 'task_started'})
        self.add('event_msg', {'type': 'task_complete'})
        self.add('event_msg', {'type': 'task_started'})
        with self.assertRaisesRegex(ValueError, 'reused child'):
            self.read()

    def test_work_after_old_terminal_does_not_close_current_accounting(self):
        self.add('event_msg', {'type': 'task_complete'})
        self.add('response_item', {'type': 'message', 'role': 'assistant'})
        self.count(100)
        self.assertEqual(self.read()['accounting_status'], 'unresolved')

    def test_late_counter_can_recover_after_terminal(self):
        self.add('response_item', {'type': 'message', 'role': 'assistant'})
        self.add('event_msg', {'type': 'task_complete'})
        self.count(100)
        self.assertEqual(self.read()['accounting_status'], 'complete')


if __name__ == '__main__':
    unittest.main()
