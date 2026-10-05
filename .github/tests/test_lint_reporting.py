import contextlib
import importlib.util
import io
from pathlib import Path
import unittest

spec = importlib.util.spec_from_file_location('report', Path(__file__).resolve().parents[1] / 'scripts/report_hadolint.py')
reporter = importlib.util.module_from_spec(spec)
spec.loader.exec_module(reporter)


class ReportingTests(unittest.TestCase):
    def finding(self, level):
        return {'level': level, 'file': 'apps/test/Dockerfile', 'line': 3,
                'code': 'DL4006', 'message': 'test\n::error::not a separate annotation'}

    def test_warnings_and_information_do_not_fail(self):
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            self.assertEqual(reporter.report([self.finding('warning'), self.finding('info')]), 0)
        self.assertEqual(output.getvalue().count('::warning file='), 2)
        self.assertIn('%0A', output.getvalue())

    def test_errors_still_fail(self):
        with contextlib.redirect_stdout(io.StringIO()) as output:
            self.assertEqual(reporter.report([self.finding('error')]), 1)
        self.assertTrue(output.getvalue().startswith('::error file='))

    def test_invalid_results_fail_closed(self):
        for data in ({}, [self.finding('unknown')]):
            with self.assertRaises(ValueError):
                reporter.report(data)


if __name__ == '__main__':
    unittest.main()
