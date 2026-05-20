import sys
import unittest
from pathlib import Path


PACKET_DIR = Path(__file__).resolve().parents[1] / "housing_packet"
sys.path.insert(0, str(PACKET_DIR))

from build_housing_packet_clean import lines_for  # noqa: E402


class TextWrappingTests(unittest.TestCase):
    def test_exact_max_line_fit_does_not_add_ellipsis(self):
        lines = lines_for("first second", "Helvetica", 10, 42, max_lines=2)

        self.assertEqual(lines, ["first", "second"])

    def test_overflow_after_max_lines_adds_ellipsis(self):
        lines = lines_for("first second third", "Helvetica", 10, 42, max_lines=2)

        self.assertEqual(lines, ["first", "second..."])


if __name__ == "__main__":
    unittest.main()
