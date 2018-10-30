"""Tests pymarkdownlint.mdparser.tag."""
from unittest import TestCase
from pymarkdownlint.mdparser.tag import *


class GetLineTypeTest(TestCase):
    """Tests function get_line_type."""

    def test_newline_no_indents(self):
        """Tests giving a blank line."""
        self.assertEqual(get_line_type(''), (Tag.newline, 0, 0))

    def test_newline_indents(self):
        """Tests giving a blank line with indents."""
        self.assertEqual(get_line_type('  '), (Tag.newline, 2, 0))
        self.assertEqual(get_line_type('\t'), (Tag.newline, 1, 0))
        self.assertEqual(get_line_type('\t\r'), (Tag.newline, 2, 0))

    def test_headings(self):
        """Tests giving a heading."""
        self.assertEqual(get_line_type('#Hello'), (Tag.heading, 0, 1))
        self.assertEqual(get_line_type('##Hello'), (Tag.heading, 0, 2))
        self.assertEqual(get_line_type(' #Hello'), (Tag.heading, 1, 1))
        self.assertEqual(get_line_type('###Hello'), (Tag.heading, 0, 3))

    def test_blockquote(self):
        """Tests giving a blockquote."""
        self.assertEqual(get_line_type('>Hellaie'), (Tag.blockquote, 0, 0))
        self.assertEqual(get_line_type(' >Hellaie'), (Tag.blockquote, 1, 0))

    def test_unlist(self):
        """Tests giving an unordered list."""
        self.assertEqual(get_line_type('- item'), (Tag.unlist, 0, '-'))
        self.assertEqual(get_line_type(' - item'), (Tag.unlist, 1, '-'))
        self.assertEqual(get_line_type('* item'), (Tag.unlist, 0, '*'))
        self.assertEqual(get_line_type('\t+ item'), (Tag.unlist, 1, '+'))

    def test_ordlist(self):
        """Tests giving an ordered list."""
        self.assertEqual(get_line_type('1. item'), (Tag.ordlist, 0, 1))
        self.assertEqual(get_line_type(' 2. item'), (Tag.ordlist, 1, 2))
        self.assertEqual(get_line_type('102. item'), (Tag.ordlist, 0, 102))
        self.assertEqual(get_line_type('\t34. item'), (Tag.ordlist, 1, 34))

    def test_paragraphs(self):
        """Tests giving a paragraph (a line without any of the above)."""
        self.assertEqual(get_line_type('Hello!'), (Tag.paragraph, 0, 0))
        self.assertEqual(get_line_type(' Hello!'), (Tag.paragraph, 1, 0))
