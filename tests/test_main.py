"""Smoke tests for the application foundation."""

from contextlib import redirect_stdout
from io import StringIO
import unittest

from resqai.main import main


class MainTests(unittest.TestCase):
    def test_main_reports_foundation_status(self) -> None:
        output = StringIO()
        with redirect_stdout(output):
            main()

        self.assertIn("ResQAI foundation is ready.", output.getvalue())


if __name__ == "__main__":
    unittest.main()
