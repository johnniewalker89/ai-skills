"""Synthetic-only control regressions; no model sessions or external services."""

import json
import subprocess
import sys
import tempfile
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from monitor import Limits, Monitor


class MonitorTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.session = self.root / 'child.jsonl'
        self.result = self.root / 'result.md'
        self.start = datetime(2026, 1, 1, tzinfo=timezone.utc)
        self.limits = Limits(45000, 55000, 400000, 550000, 360, 540, 90)
        self.monitor = Monitor('child', 'parent', self.limits)

    def write_session(self, counts=None, terminal=None, parent='parent', partial=False):
        rows = [{'type': 'session_meta', 'payload': {'id': 'child',
                 'timestamp': self.start.isoformat(), 'source': {'subagent':
                 {'thread_spawn': {'parent_thread_id': parent}}}}}]
        if counts is not None:
            rows.append({'type': 'event_msg', 'timestamp': self.start.isoformat(),
                         'payload': {'type': 'token_count', 'info': {'total_token_usage':
                         dict(zip(('input_tokens', 'cached_input_tokens', 'output_tokens'), counts))}}})
        if terminal:
            rows.append({'type': 'event_msg', 'timestamp': (self.start + timedelta(seconds=5)).isoformat(),
                         'payload': {'type': terminal}})
        self.session.write_text(''.join(json.dumps(r) + '\n' for r in rows), encoding='utf-8')
        if partial:
            with self.session.open('a', encoding='utf-8') as f:
                f.write('{"type":')

    def sample(self, seconds=64):
        return self.monitor.sample(self.session, self.result, self.start + timedelta(seconds=seconds))

    def append_exec_output(self, call_id='failed-write', error='SyntaxError', *, failed=True,
                           tool='exec', private_text='private payload must not be reported',
                           output_blocks=None):
        output = ([{'type': 'input_text', 'text': 'Script failed\nWall time 0.0 seconds\nOutput:\n'},
                   {'type': 'input_text', 'text': f'Script error:\n{error}: {private_text}'}]
                  if failed else [{'type': 'input_text', 'text': json.dumps(
                      {'exit_code': 1, 'output': f'Expected negative test: {error}: {private_text}'})}])
        if output_blocks is not None:
            output = output_blocks
        rows = [
            {'type': 'response_item', 'timestamp': self.start.isoformat(),
             'payload': {'type': 'custom_tool_call', 'call_id': call_id,
                         'name': tool, 'input': private_text}},
            {'type': 'response_item', 'timestamp': self.start.isoformat(),
             'payload': {'type': 'custom_tool_call_output', 'call_id': call_id, 'output': output}},
        ]
        with self.session.open('a', encoding='utf-8') as stream:
            stream.write(''.join(json.dumps(row) + '\n' for row in rows))

    def test_visible_wrapper_failure_yields_before_budget_and_does_not_echo_payload(self):
        self.write_session((320524, 273920, 5895))
        self.limits = Limits(60000, 70000, 580000, 700000, 360, 450, 90)
        self.monitor = Monitor('child', 'parent', self.limits)
        self.append_exec_output()
        result = self.sample(206)
        self.assertEqual((result['action'], result['budget_action']), ('review', 'continue'))
        self.assertEqual(result['attention'][0]['error_type'], 'SyntaxError')
        self.assertEqual(result['attention'][0]['call_id'], 'failed-write')
        self.assertIsNone(result['result'])
        self.assertNotIn('private payload', json.dumps(result))
        self.assertFalse(self.result.exists())

    def test_review_acknowledges_only_named_failure_across_monitor_invocations(self):
        self.write_session((1000, 900, 100))
        self.append_exec_output()
        self.monitor = Monitor('child', 'parent', self.limits, reviewed_call_ids=('failed-write',))
        self.assertEqual(self.sample()['action'], 'continue')
        self.append_exec_output('second-write', 'ReferenceError')
        self.monitor = Monitor('child', 'parent', self.limits, reviewed_call_ids=('failed-write',))
        result = self.sample()
        self.assertEqual(result['action'], 'review')
        self.assertEqual([item['call_id'] for item in result['attention']], ['second-write'])

    def test_apply_patch_wrapper_failure_without_exception_class_requires_review(self):
        self.write_session((1000, 900, 100))
        # Captured wrapper shape; the private absolute artifact path is replaced.
        self.append_exec_output(tool='functions.exec', output_blocks=[
            {'type': 'input_text', 'text': 'Script failed\nWall time 0.0 seconds\nOutput:\n'},
            {'type': 'input_text', 'text': 'Script error:\napply_patch verification failed: '
             'invalid patch: multiple operations target <private-artifact>/notes.md'},
        ])
        result = self.sample()
        self.assertEqual((result['action'], result['budget_action']), ('review', 'continue'))
        self.assertEqual(result['attention'], [{
            'kind': 'exec_wrapper_error', 'call_id': 'failed-write',
            'at': self.start.isoformat(), 'error_type': 'WrapperError',
        }])
        self.assertNotIn('private-artifact', json.dumps(result))
        self.monitor = Monitor('child', 'parent', self.limits, reviewed_call_ids=('another-call',))
        self.assertEqual(self.sample()['action'], 'review')
        self.monitor = Monitor('child', 'parent', self.limits, reviewed_call_ids=('failed-write',))
        self.assertEqual(self.sample()['attention'], [])
        self.assertEqual(self.sample()['action'], 'continue')

    def test_confirmed_wrapper_failure_requires_review_without_details(self):
        self.write_session((1000, 900, 100))
        self.append_exec_output(output_blocks=[
            {'type': 'input_text', 'text': 'Script failed\nWall time 0.0 seconds\nOutput:\n'},
        ])
        result = self.sample()
        self.assertEqual(result['action'], 'review')
        self.assertEqual(result['attention'][0]['error_type'], 'WrapperError')

    def test_error_text_without_outer_wrapper_failure_does_not_require_review(self):
        for blocks in (
            [{'type': 'input_text', 'text': 'Script completed\nWall time 0.0 seconds\nOutput:\n'},
             {'type': 'input_text', 'text': json.dumps({'exit_code': 0, 'output':
              'Script failed\nScript error:\napply_patch verification failed: expected test'})}],
            [{'type': 'input_text', 'text': 'Script error:\nSyntaxError: expected test'}],
            [{'type': 'input_text', 'text': 'Script error:\napply_patch verification failed'}],
        ):
            with self.subTest(blocks=blocks):
                self.write_session((1000, 900, 100))
                self.append_exec_output(output_blocks=blocks)
                result = self.sample()
                self.assertEqual(result['action'], 'continue')
                self.assertEqual(result['attention'], [])

    def test_successful_wrapper_printing_literal_failure_marker_does_not_require_review(self):
        for detail in ('This is printed data', 'Script error:\nTypeError: printed data'):
            with self.subTest(detail=detail):
                self.write_session((1000, 900, 100))
                self.append_exec_output(output_blocks=[
                    {'type': 'input_text', 'text': 'Script completed\nWall time 0.0 seconds\nOutput:\n'},
                    {'type': 'input_text', 'text': 'Script failed\n' + detail},
                ])
                result = self.sample()
                self.assertEqual(result['action'], 'continue')
                self.assertEqual(result['attention'], [])

    def test_domain_failure_or_unbound_tool_output_is_not_wrapper_failure(self):
        self.write_session((1000, 900, 100))
        self.append_exec_output(failed=False)
        self.append_exec_output('different-tool', tool='domain_check')
        self.assertEqual(self.sample()['action'], 'continue')
        self.assertEqual(self.sample()['attention'], [])

    def test_saved_result_checkpoint_requires_semantic_review_even_with_existing_file(self):
        self.limits = Limits(45000, 55000, 400000, 550000, 360, 540, 90,
                             checkpoint_u=20000, checkpoint_seconds=120)
        self.monitor = Monitor('child', 'parent', self.limits)
        self.write_session((1000, 900, 100))
        self.assertEqual(self.sample(119)['action'], 'continue')
        self.assertEqual(self.sample(120)['action'], 'review')
        self.assertFalse(self.sample(120)['attention'][0]['artifact_present'])
        self.result.write_text('Only a heading; not proof', encoding='utf-8')
        result = self.sample(120)
        self.assertEqual(result['action'], 'review')
        self.assertTrue(result['attention'][0]['artifact_present'])
        self.monitor = Monitor('child', 'parent', self.limits, checkpoint_reviewed=True)
        self.assertEqual(self.sample(120)['action'], 'continue')
        self.write_session((20000, 0, 0))
        self.monitor = Monitor('child', 'parent', self.limits)
        self.assertEqual(self.sample(10)['action'], 'review')

    def test_checkpoint_limits_cannot_spend_the_completion_reserve(self):
        for kwargs in ({'checkpoint_u': 20000}, {'checkpoint_seconds': 120},
                       {'checkpoint_u': 45000, 'checkpoint_seconds': 120},
                       {'checkpoint_u': 20000, 'checkpoint_seconds': 360},
                       {'checkpoint_u': 0, 'checkpoint_seconds': 120}):
            with self.subTest(kwargs=kwargs), self.assertRaises(ValueError):
                Limits(45000, 55000, 400000, 550000, 360, 540, 90, **kwargs)

    def test_budget_stop_and_reserve_keep_priority_over_error_attention(self):
        for counts, action in (((46000, 0, 0), 'finish'), ((56000, 0, 0), 'stop')):
            with self.subTest(action=action):
                self.write_session(counts)
                self.append_exec_output()
                result = self.sample()
                self.assertEqual(result['action'], action)
                self.assertEqual(result['budget_action'], action)
                self.assertEqual(result['attention'][0]['kind'], 'exec_wrapper_error')
        self.write_session(terminal='turn_aborted')
        self.append_exec_output()
        self.assertEqual(self.sample()['action'], 'done')

    def test_progress_artifact_is_observed_and_cannot_be_clobbered_by_report(self):
        self.start = datetime.now(timezone.utc)
        self.write_session((1000, 900, 100))
        progress = self.root / 'partial.json'
        progress.write_text('saved partial work', encoding='utf-8')
        self.limits = Limits(45000, 55000, 400000, 550000, 360, 540, 90,
                             checkpoint_u=100, checkpoint_seconds=120)
        self.monitor = Monitor('child', 'parent', self.limits)
        result = self.monitor.sample(self.session, self.result, self.start,
                                     progress_artifact=progress)
        self.assertEqual(result['action'], 'review')
        self.assertIsNone(result['result'])
        self.assertEqual(result['progress_artifact']['bytes'], 18)
        config = self.root / 'limits.json'
        config.write_text(json.dumps(self.limits.__dict__), encoding='utf-8')
        command = [sys.executable, '-B', str(Path(__file__).resolve().parents[1] / 'monitor.py'),
                   '--session', str(self.session), '--child-id', 'child', '--parent-id', 'parent',
                   '--limits', str(config), '--result', str(self.result),
                   '--progress-artifact', str(progress), '--output', str(progress)]
        cli = subprocess.run(command, capture_output=True, text=True)
        self.assertEqual(cli.returncode, 2)
        self.assertEqual(progress.read_text(), 'saved partial work')

    def test_cli_yields_for_review_and_explicit_ack_does_not_change_result(self):
        self.start = datetime.now(timezone.utc)
        self.write_session((1000, 900, 100))
        self.append_exec_output()
        config = self.root / 'limits.json'
        config.write_text(json.dumps(self.limits.__dict__), encoding='utf-8')
        output = self.root / 'monitor.json'
        command = [sys.executable, '-B', str(Path(__file__).resolve().parents[1] / 'monitor.py'),
                   '--session', str(self.session), '--child-id', 'child', '--parent-id', 'parent',
                   '--limits', str(config), '--result', str(self.result), '--output', str(output)]
        completed = subprocess.run(command, capture_output=True, text=True)
        self.assertEqual(completed.returncode, 0, completed.stderr)
        self.assertEqual(json.loads(output.read_text())['action'], 'review')
        command += ['--reviewed-call-id', 'failed-write']
        completed = subprocess.run(command, capture_output=True, text=True)
        self.assertEqual(completed.returncode, 0, completed.stderr)
        self.assertEqual(json.loads(output.read_text())['action'], 'continue')
        self.assertFalse(self.result.exists())

    def test_late_valid_sample_does_not_abort_and_counts_cache_once(self):
        self.write_session((251000, 226000, 3000), partial=True)
        result = self.sample()
        self.assertEqual(result['action'], 'continue')
        self.assertEqual((result['usage']['U'], result['usage']['T']), (28000, 254000))

    def test_cache_total_is_diagnostic_without_explicit_limits(self):
        self.monitor = Monitor('child', 'parent', Limits(45000, 55000, None, None, 360, 540, 90))
        self.write_session((5000000, 4990000, 1000))
        result = self.sample()
        self.assertEqual(result['action'], 'continue')
        self.assertFalse(result['total_token_limit_enabled'])
        self.assertEqual(result['usage']['U'], 11000)
        self.assertEqual(result['usage']['T'], 5001000)
        self.write_session((5100000, 5040000, 1000))
        self.assertEqual(self.sample()['action'], 'stop')

    def test_explicit_legacy_total_limits_still_apply(self):
        for counts, action in (((450000, 449000, 100), 'finish'),
                               ((600000, 599000, 100), 'stop')):
            with self.subTest(action=action):
                self.write_session(counts)
                result = self.sample()
                self.assertEqual(result['action'], action)
                self.assertTrue(result['total_token_limit_enabled'])

    def test_total_limit_requires_complete_valid_pair(self):
        for finish, stop in ((None, 500), (100, None), (0, 100), (100, 100), (200, 100)):
            with self.subTest(finish=finish, stop=stop), self.assertRaises(ValueError):
                Limits(45000, 55000, finish, stop, 360, 540, 90)

    def test_cli_without_total_limits_keeps_time_and_identity_controls(self):
        self.start = datetime.now(timezone.utc)
        self.write_session((5000000, 4990000, 1000))
        config = self.root / 'limits.json'
        configured = {k: v for k, v in self.limits.__dict__.items()
                      if k not in ('finish_t', 'stop_t')}
        config.write_text(json.dumps(configured), encoding='utf-8')
        output = self.root / 'monitor.json'
        command = [sys.executable, '-B', str(Path(__file__).resolve().parents[1] / 'monitor.py'),
                   '--session', str(self.session), '--child-id', 'child', '--parent-id', 'parent',
                   '--limits', str(config), '--result', str(self.result), '--output', str(output)]
        completed = subprocess.run(command, capture_output=True, text=True)
        self.assertEqual(completed.returncode, 0, completed.stderr)
        report = json.loads(output.read_text())
        self.assertEqual(report['action'], 'continue')
        self.assertFalse(report['total_token_limit_enabled'])
        self.monitor = Monitor('child', 'parent', Limits(45000, 55000, None, None, 360, 540, 90))
        self.assertEqual(self.sample(540)['action'], 'stop')
        self.write_session((5000000, 4990000, 1000), parent='wrong')
        with self.assertRaisesRegex(ValueError, 'identity mismatch'):
            self.sample()

    def test_reserve_then_stop_preserves_result(self):
        self.result.write_bytes(b'partial proof\n')
        self.write_session((50000, 7000, 2000))
        self.assertEqual(self.sample()['action'], 'finish')
        self.write_session((60000, 7000, 2000))
        result = self.sample()
        self.assertEqual(result['action'], 'stop')
        self.assertEqual(self.result.read_bytes(), b'partial proof\n')
        self.assertEqual(result['result']['bytes'], 14)

    def test_missing_counters_wait_then_stop(self):
        self.write_session()
        self.assertEqual(self.sample(64)['action'], 'waiting')
        self.assertEqual(self.sample(90)['reason'], 'telemetry_unavailable')

    def test_unchanged_counter_is_valid_during_inflight_call(self):
        self.write_session((1000, 900, 100))
        self.sample(1)
        self.assertEqual(self.sample(120)['action'], 'continue')

    def test_parent_is_rejected_before_counters(self):
        self.write_session((9999999, 0, 0), parent='wrong')
        with self.assertRaisesRegex(ValueError, 'identity mismatch'):
            self.sample()
        with self.assertRaises(ValueError):
            Monitor('parent', 'parent', self.limits)

    def test_invalid_and_decreasing_counters_are_not_zero_usage(self):
        self.write_session((1000, 800, 100))
        self.sample()
        self.write_session((1000, 700, 100))
        self.assertEqual(self.sample()['reason'], 'counter_reset')
        self.write_session((100, 200, 0))
        with self.assertRaisesRegex(ValueError, 'invalid token counters'):
            self.sample()

    def test_full_tokens_and_elapsed_independently_trigger_stops(self):
        self.write_session((550000, 549000, 1))
        self.assertEqual(self.sample()['reason'], 'token_limit')
        self.write_session((550000, 549000, 1))
        self.assertEqual(self.sample(540)['reason'], 'elapsed_limit')

    def test_reset_is_detected_across_separate_watch_invocations(self):
        self.write_session((1000, 800, 100))
        with self.session.open('a', encoding='utf-8') as f:
            f.write(json.dumps({'type': 'event_msg', 'payload': {'type': 'token_count',
                    'info': {'total_token_usage': {'input_tokens': 10,
                    'cached_input_tokens': 0, 'output_tokens': 1}}}}) + '\n')
        with self.assertRaisesRegex(ValueError, 'counter reset'):
            self.sample()

    def test_terminal_states_and_absent_result_remain_distinct(self):
        for terminal in ('task_complete', 'turn_aborted', 'task_aborted'):
            with self.subTest(terminal=terminal):
                self.write_session(terminal=terminal)
                result = self.sample()
                self.assertEqual((result['action'], result['reason']), ('done', terminal))
                self.assertEqual(result['elapsed_seconds'], 5)
                self.assertIsNone(result['result'])

    def test_cli_reports_stop_without_modifying_evidence(self):
        self.write_session((60000, 0, 0))
        self.result.write_bytes(b'preserved')
        config = self.root / 'limits.json'
        config.write_text(json.dumps(self.limits.__dict__), encoding='utf-8')
        output = self.root / 'report.json'
        command = [sys.executable, '-B', str(Path(__file__).resolve().parents[1] / 'monitor.py'),
                   '--session', str(self.session), '--child-id', 'child', '--parent-id', 'parent',
                   '--limits', str(config), '--result', str(self.result), '--output', str(output)]
        run = subprocess.run(command, capture_output=True, text=True)
        self.assertEqual(run.returncode, 2, run.stderr)
        self.assertEqual(json.loads(output.read_text())['action'], 'stop')
        self.assertEqual(self.result.read_bytes(), b'preserved')
        self.assertTrue(output.with_suffix('.jsonl').is_file())
        command[-1] = str(self.result)
        self.assertEqual(subprocess.run(command, capture_output=True).returncode, 2)
        self.assertEqual(self.result.read_bytes(), b'preserved')

    def test_finishing_mode_keeps_sampling_and_sidecar_cannot_clobber_result(self):
        self.start = datetime.now(timezone.utc)
        self.write_session((46000, 0, 0))
        config = self.root / 'limits.json'
        config.write_text(json.dumps(self.limits.__dict__), encoding='utf-8')
        output = self.root / 'report.json'
        command = [sys.executable, '-B', str(Path(__file__).resolve().parents[1] / 'monitor.py'),
                   '--session', str(self.session), '--child-id', 'child', '--parent-id', 'parent',
                   '--limits', str(config), '--result', str(self.result), '--output', str(output),
                   '--watch-seconds', '0.03', '--interval', '0.01', '--finishing']
        run = subprocess.run(command, capture_output=True, text=True)
        self.assertEqual(run.returncode, 0, run.stderr)
        self.assertGreaterEqual(len(output.with_suffix('.jsonl').read_text().splitlines()), 2)
        command[command.index('--result') + 1] = str(output.with_suffix('.jsonl'))
        before = output.with_suffix('.jsonl').read_bytes()
        self.assertEqual(subprocess.run(command, capture_output=True).returncode, 2)
        self.assertEqual(output.with_suffix('.jsonl').read_bytes(), before)


if __name__ == '__main__':
    unittest.main()
