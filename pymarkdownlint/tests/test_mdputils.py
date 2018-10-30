"""Tests pymarkdownlint.mdparser.utils."""
from unittest import TestCase
from pymarkdownlint.mdparser.utils import *


class CountFirstSeqTest(TestCase):
    """Tests function count_first_seq."""

    def test_zero_len_str(self):
        """Test with zero length strings."""
        self.assertEqual(count_first_seq('', 'x'), 0)
        self.assertEqual(count_first_seq('', ''), 0)

    def test_str(self):
        """Test with standard strings."""
        self.assertEqual(count_first_seq('# This is a header', '#'), 1)
        self.assertEqual(count_first_seq('# Had', ' '), 0)
        self.assertEqual(count_first_seq('## Second lvl', '#'), 2)
        self.assertEqual(count_first_seq('### Third with ####', '#'), 3)

