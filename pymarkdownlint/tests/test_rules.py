from pymarkdownlint.tests.base import BaseTestCase
from pymarkdownlint.mdparser.parser import Parser
from pymarkdownlint.rules.base import *
from pymarkdownlint.rules.filerule import *
from pymarkdownlint.rules.linerule import *


class BaseRuleTest(BaseTestCase):
    """A basic (automated) rule test"""

    def setup_test(self, config):
        """
        A shorthand for setting up tests, succinctly.

        ``config`` is a dictionary of things, including:
        - ``rule``: the actual rule to test
        - ``okay``: a list of text (list of strings) that comply with the rule
        - ``bad``: a list of tuples, first the text, then the violation (filled
          out, if you please)

        Note that the first element in the tuple is always the configuration
        that goes with the rule.

        An example::

            conf = {'rule': HeaderIncrement,
                    'okay': [({},
                              ['# Hello world',
                               '## Nice day you got there',
                               '# Yoshi']],
                    'bad':  [({},
                              ['# Hello world',
                               '### Nice day you got there',
                               '# Yoshi'],
                              HeaderIncrement.error_str,
                              2)]}

        Note that only :class:`FileRule` have lists as arguments.
        :class:`LineRule` have strings as arguments.

        :param config: configuration to run tests on
        """
        for cfg, text in config['okay']:
            # Assert no errors
            rule = config['rule'](cfg)
            if isinstance(text, list):
                # Only FileRules have lists as arguments
                text = Parser('\n'.join(text))
            violation = rule.validate(text)
            self.assertIsNone(violation)

        for cfg, text, err, lineno in config['bad']:
            # Assert errors
            rule = config['rule'](cfg)
            if isinstance(text, list):
                # Only FileRules have lists as arguments
                text = Parser('\n'.join(text))
            observed = rule.validate(text)
            expected = RuleViolation(rule.id, err, lineno)
            self.assertEqual(observed, expected)


class FileRuleTests(BaseRuleTest):
    """Tests all file rules"""

    def test_header_inc(self):
        """For MD001."""
        conf = {'rule': HeaderIncrement,
                'okay': [({},
                          ['# Hello world',
                           '## Nice day you got there',
                           '# Yoshi'])],
                'bad':  [({},
                          ['# Hello world',
                           '### Nice day you got there',
                           '# Yoshi'],
                          HeaderIncrement.error_str,
                          2)]}
        self.setup_test(conf)

    def test_top_level_header(self):
        """For MD002."""
        conf = {'rule': TopLevelHeader,
                'okay': [({},
                          ['# Hello wood',
                           '',
                           'Tamagachis']),
                         ({'first-header-level': 2},
                          ['## hello wood',
                           '',
                           'Tamagachis'])],
                'bad':  [({},
                          ['## hellowood',
                           '',
                           'Tamagachis'],
                          TopLevelHeader.error_str,
                          1)]}
        self.setup_test(conf)

    def test_unlist_styles(self):
        """For MD004."""
        conf = {'rule': UnorderedListStyle,
                'okay': [({},
                          ['- happy',
                           '- day'])],
                'bad':  [({},
                          ['- happy',
                           '+ day'],
                          UnorderedListStyle.error_str.format('-'),
                          2),
                         ({'unordered-list-style': 'dash'},
                          ['+ happy',
                           '+ day'],
                          UnorderedListStyle.error_str.format('-'),
                          1)]}
        self.setup_test(conf)

    def test_beg_list_at_startofline(self):
        """For MD006."""
        conf = {'rule': TopLevelListIndent,
                'okay': [({},
                          ['some things',
                           '',
                           '- Happy',
                           '- Days']),
                         ({},
                          ['some things',
                           '',
                           '- Happy',
                           '  - Days'])],
                'bad':  [({},
                          ['some things',
                           '',
                           ' - Happy',
                           ' - Days'],
                          TopLevelListIndent.error_str,
                          3)]}
        self.setup_test(conf)


class LineRuleTests(BaseRuleTest):
    """Tests all line rules"""

    def test_trailing_whitespace(self):
        """For MD009."""
        conf = {'rule': TrailingWhiteSpace,
                'okay': [({},
                          'a')],
                'bad':  [({},
                          'a ',
                          TrailingWhiteSpace.error_str,
                          None),
                         ({},
                          'a\t',
                          TrailingWhiteSpace.error_str,
                          None)]}
        self.setup_test(conf)

    def test_hard_tabs(self):
        """For MD010."""
        conf = {'rule': HardTab,
                'okay': [({},
                          'This is a test')],
                'bad':  [({},
                          'This is a\ttest',
                          HardTab.error_str,
                          None)]}
        self.setup_test(conf)

    def test_max_line_length(self):
        """For MD013."""
        conf = {'rule': MaxLineLengthRule,
                'okay': [({},
                          'a' * 80),
                         ({'line-length': 120},
                          'a' * 81)],
                'bad':  [({},
                          'a' * 81,
                          MaxLineLengthRule.error_str.format(81, 80),
                          None),
                         ({'line-length': 120},
                          'a' * 121,
                          MaxLineLengthRule.error_str.format(121, 120),
                          None)]}
        self.setup_test(conf)
