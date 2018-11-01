from pymarkdownlint.tests.base import BaseTestCase
from pymarkdownlint.config import LintConfig, LintConfigError

from pymarkdownlint import rules


class LintConfigTests(BaseTestCase):
    def test_get_rule_by_name_or_id(self):
        config = LintConfig()

        # get by id
        expected = rules.MaxLineLengthRule()
        rule = config.get_rule_by_name_or_id('MD013')
        self.assertEqual(rule, expected)

        # get by name
        expected = rules.TrailingWhiteSpace()
        rule = config.get_rule_by_name_or_id('trailing-whitespace')
        self.assertEqual(rule, expected)

        # get non-existing
        rule = config.get_rule_by_name_or_id('foo')
        self.assertIsNone(rule)

    def test_load_config_from_file(self):
        # regular config file load, no problems
        LintConfig.load_from_file(self.get_sample_path("markdownlint"))

        # bad config file load
        foo_path = self.get_sample_path("foo")
        with self.assertRaisesRegex(LintConfigError, "Invalid file path: {}".format(foo_path)):
            LintConfig.load_from_file(foo_path)

        # error during file parsing
        bad_markdowlint_path = self.get_sample_path("badmarkdownlint")
        expected_error_msg = "Error during config file parsing: File contains no section headers."
        with self.assertRaisesRegex(LintConfigError, expected_error_msg):
            LintConfig.load_from_file(bad_markdowlint_path)
