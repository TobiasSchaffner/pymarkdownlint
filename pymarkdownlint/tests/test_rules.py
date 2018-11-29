from pymarkdownlint.tests.base import BaseTestCase
from pymarkdownlint.mdparser.parser import Parser
from pymarkdownlint.rules.base import *
from pymarkdownlint.rules.filerule import *
from pymarkdownlint.rules.linerule import *


class FileRuleTests(BaseTestCase):
    """Tests all file rules"""

    def test_header_inc(self):
        """For MD001."""
        rule = HeaderIncrement()

        # assert no error
        violation = rule.validate(Parser("""# Hello world
## Nice day you got there
# Yoshi
"""))
        self.assertIsNone(violation)

        # assert error with bad headers
        violation = rule.validate(Parser("""# Hello world
### Nice day you got there
# Yoshi
"""))
        expected_violation = RuleViolation(rule.id, rule.error_str, 2)
        self.assertEqual(violation, expected_violation)

    def test_top_level_header(self):
        """For MD002."""
        rule = TopLevelHeader()

        # assert no error
        violation = rule.validate(Parser("""# Hello wood

Tamagachis
"""))
        self.assertIsNone(violation)

        # assert error
        violation = rule.validate(Parser("""## hellowood

Tamagachis
"""))
        expected_violation = RuleViolation(rule.id, rule.error_str, 1)
        self.assertEqual(violation, expected_violation)

        # no errors if you configured it right
        rule = TopLevelHeader({'first-header-level': 2})
        violation = rule.validate(Parser("""## hello wood

Tamagachis
"""))
        self.assertIsNone(violation)

    def test_unlist_styles(self):
        """For MD004."""
        rule = UnorderedListStyle()

        # assert no error
        self.assertIsNone(rule.validate(Parser("""- happy
- day
""")))

        # assert error
        violation = rule.validate(Parser("""- happy
+ day
"""))
        expected_violation = RuleViolation(rule.id,
                                           rule.error_str.format('-'),
                                           2)
        self.assertEqual(violation, expected_violation)
        rule = UnorderedListStyle({'unordered-list-style': 'dash'})
        violation = rule.validate(Parser("""+ happy
+ day
"""))
        expected_violation = RuleViolation(rule.id,
                                           rule.error_str.format('-'),
                                           1)
        self.assertEqual(violation, expected_violation)


class LineRuleTests(BaseTestCase):
    """Tests all line rules"""

    def test_trailing_whitespace(self):
        """For MD009."""
        rule = TrailingWhiteSpace()

        # assert no error
        violation = rule.validate("a")
        self.assertIsNone(violation)

        # trailing space
        expected_violation = RuleViolation(rule.id, rule.error_str)
        violation = rule.validate("a ")
        self.assertEqual(violation, expected_violation)

        # trailing tab
        violation = rule.validate("a\t")
        self.assertEqual(violation, expected_violation)

    def test_hard_tabs(self):
        """For MD010."""
        rule = HardTab()

        # assert no error
        violation = rule.validate("This is a test")
        self.assertIsNone(violation)

        # contains hard tab
        expected_violation = RuleViolation(rule.id, rule.error_str)
        violation = rule.validate("This is a\ttest")
        self.assertEqual(violation, expected_violation)

    def test_max_line_length(self):
        """For MD013."""
        rule = MaxLineLengthRule()

        # assert no error
        violation = rule.validate("a" * 80)
        self.assertIsNone(violation)

        # assert error on line length > 81
        expected_violation = RuleViolation("MD013", "Line exceeds max length (81>80)")
        violation = rule.validate("a" * 81)
        self.assertEqual(violation, expected_violation)

        # set line length to 120, and check no violation on length 81
        rule = MaxLineLengthRule({'line-length': 120})
        violation = rule.validate("a" * 81)
        self.assertIsNone(violation)

        # assert raise on 121
        expected_violation = RuleViolation("MD013", "Line exceeds max length (121>120)")
        violation = rule.validate("a" * 121)
        self.assertEqual(violation, expected_violation)
