"""Tests pymarkdownlint.mdparser.parser."""
from os.path import join
from pymarkdownlint.tests import BaseTestCase
from pymarkdownlint.mdparser.tag import Tag
from pymarkdownlint.mdparser.parser import *


class LineTest(BaseTestCase):
    """Tests class Line."""

    def test_init(self):
        """Test initialization."""
        line = Line(1, "# Header")

        self.assertEqual(line.tag, Tag.heading)
        self.assertEqual(line.lineno, 1)


class ParserTest(BaseTestCase):
    """Tests class Parser."""

    def test_filtering(self):
        """Test analyzing and filtering."""
        sample_dir = self.get_sample_path()
        sample_md = join(sample_dir, 'filtering.md')
        sample_text = open(sample_md, 'r').read()
        parser = Parser(sample_text)

        self.assertEqual(len(parser['heading']), 2)
        self.assertEqual(len(parser['unlist']), 2)
        self.assertEqual(len(parser['ordlist']), 2)
