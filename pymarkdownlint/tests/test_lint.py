from pymarkdownlint.tests import BaseTestCase

from pymarkdownlint.lint import MarkdownLinter
from pymarkdownlint.rules import RuleViolation
from pymarkdownlint.config import LintConfig


class RuleOptionTests(BaseTestCase):
    def test_lint(self):
        linter = MarkdownLinter(LintConfig())
        sample = self.get_sample_path("sample1.md")
        with open(sample) as f:
            errors = linter.lint(f.read())
            expected_errors = [RuleViolation("MD013", "Line exceeds max length (119>80)", 3),
                               RuleViolation("MD009", "Line has trailing whitespace", 4),
                               RuleViolation("MD009", "Line has trailing whitespace", 5),
                               RuleViolation("MD010", "Line contains hard tab characters (\\t)", 5)]
            self.assertListEqual(errors, expected_errors)
