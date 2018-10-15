from pymarkdownlint.tests.base import BaseTestCase
import pymarkdownlint.rules as rules


class RuleTests(BaseTestCase):
    def test_header_inc(self):
        """For MD001."""
        rule = rules.HeaderIncrement()

        # assert no error
        violation = rule.validate("""# Hello world
## Nice day you got there
# Yoshi
""")
        self.assertIsNone(violation)

        # assert error with bad headers
        violation = rule.validate("""# Hello world
### Nice day you got there
# Yoshi
""")
        expected_violation = rules.RuleViolation(rule.id, rule.error_str)
        self.assertEqual(violation, expected_violation)

    def test_top_level_header(self):
        """For MD002."""
        rule = rules.TopLevelHeader()

        # assert no error
        violation = rule.validate("""# Hello wood

Tamagachis
""")
        self.assertIsNone(violation)

        # assert error
        violation = rule.validate("""## hellowood

Tamagachis
""")
        expected_violation = rules.RuleViolation(rule.id, rule.error_str)
        self.assertEqual(violation, expected_violation)

        # no errors if you configured it right
        rule = rules.TopLevelHeader({'first-header-level': 2})
        violation = rule.validate("""## hello wood

Tamagachis
""")
        self.assertIsNone(violation)

    def test_max_line_length(self):
        """For MD013."""
        rule = rules.MaxLineLengthRule()

        # assert no error
        violation = rule.validate("a" * 80)
        self.assertIsNone(violation)

        # assert error on line length > 81
        expected_violation = rules.RuleViolation("MD013", "Line exceeds max length (81>80)")
        violation = rule.validate("a" * 81)
        self.assertEqual(violation, expected_violation)

        # set line length to 120, and check no violation on length 81
        rule = rules.MaxLineLengthRule({'line-length': 120})
        violation = rule.validate("a" * 81)
        self.assertIsNone(violation)

        # assert raise on 121
        expected_violation = rules.RuleViolation("MD013", "Line exceeds max length (121>120)")
        violation = rule.validate("a" * 121)
        self.assertEqual(violation, expected_violation)

    def test_trailing_whitespace(self):
        """For MD009."""
        rule = rules.TrailingWhiteSpace()

        # assert no error
        violation = rule.validate("a")
        self.assertIsNone(violation)

        # trailing space
        expected_violation = rules.RuleViolation(rule.id, rule.error_str)
        violation = rule.validate("a ")
        self.assertEqual(violation, expected_violation)

        # trailing tab
        violation = rule.validate("a\t")
        self.assertEqual(violation, expected_violation)

    def test_hard_tabs(self):
        """For MD010."""
        rule = rules.HardTab()

        # assert no error
        violation = rule.validate("This is a test")
        self.assertIsNone(violation)

        # contains hard tab
        expected_violation = rules.RuleViolation(rule.id, rule.error_str)
        violation = rule.validate("This is a\ttest")
        self.assertEqual(violation, expected_violation)
