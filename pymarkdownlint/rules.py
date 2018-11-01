from abc import abstractmethod, ABCMeta
import re
from pymarkdownlint.options import IntOption, StrOption
from pymarkdownlint.mdparser.parser import Parser


class Rule(object, metaclass=ABCMeta):
    """ Class representing markdown rules. """
    options_spec = []
    id = []
    name = ""
    error_str = ""

    def __init__(self, opts={}):
        self.options = {}
        for op_spec in self.options_spec:
            self.options[op_spec.name] = op_spec
            actual_option = opts.get(op_spec.name)
            if actual_option:
                self.options[op_spec.name].set(actual_option)

    def __eq__(self, other):
        return self.id == other.id and self.name == other.name

    @abstractmethod
    def validate(self, data):
        pass


class FileRule(Rule):
    """ Class representing rules that act on an entire file """

    @staticmethod
    def md_to_parse(md):
        """
        Converts a string of pure markdown into a Parser object.

        A lot of things are missing in the Parser object, but I hope it
        suffices.
        """
        return Parser(md)

    @abstractmethod
    def validate(self, data):
        pass


class LineRule(Rule):
    """ Class representing rules that act on a data by data basis """

    @abstractmethod
    def validate(self, data):
        pass


class RuleViolation(object):
    def __init__(self, rule_id, message, data_nr=None):
        self.rule_id = rule_id
        self.data_nr = data_nr
        self.message = message

    def __eq__(self, other):
        return self.rule_id == other.rule_id and\
               self.message == other.message and\
               self.data_nr == other.data_nr

    def __str__(self):
        return "{}: {} {}".format(self.data_nr, self.rule_id, self.message)

    def __repr__(self):
        return self.__str__()


class HeaderIncrement(FileRule):
    """Rule: Header levels should only increment 1 level at a time."""
    name = "header-increment"
    id = "MD001"
    error_str = "Headers increment by 1 level at a time"

    def validate(self, parser):
        old_level = None
        for header in parser['heading']:
            level = header.meta
            if old_level and level > old_level + 1:
                return RuleViolation(self.id, self.error_str, header.lineno)
            old_level = level


class TopLevelHeader(FileRule):
    """Rule: First header of the file must be h1."""
    name = "first-header-h1"
    id = "MD002"
    options_spec = [IntOption("first-header-level", 1, "Top level header")]
    error_str = "First header of the file must be top level header"

    def validate(self, parser):
        top_level = self.options['first-header-level'].value
        headers = parser['heading']
        if len(headers) > 0 and headers[0].meta != top_level:
            return RuleViolation(self.id, self.error_str, headers[0].lineno)


class UnorderedListStyle(FileRule):
    """Rule: Unordered list style must match document settings."""
    name = "unordered-list-style"
    id = "MD004"
    options_spec = [StrOption("unordered-list-style", "consistant", "Style")]
    error_str = "List styles must be {}"
    style_dict = {'asterisk': '*', 'plus': '+', 'dash': '-'}

    def validate(self, parser):
        style = self.options['unordered-list-style'].value
        last_style = None
        if style != 'consistent':
            last_style = self.style_dict.get(style, None)

        for unlist in parser['unlist']:
            if last_style and unlist.meta != last_style:
                return RuleViolation(self.id,
                                     self.error_str.format(last_style),
                                     unlist.lineno)
            last_style = unlist.meta


class TrailingWhiteSpace(LineRule):
    """Rule: No line may have trailing whitespace."""
    name = "trailing-whitespace"
    id = "MD009"
    error_str = "Line has trailing whitespace"

    def validate(self, data):
        pattern = re.compile(r"\s$")
        if pattern.search(data):
            return RuleViolation(self.id, self.error_str)


class HardTab(LineRule):
    """Rule: No line may contain tab (\\t) characters."""
    name = "hard-tab"
    id = "MD010"
    error_str = "Line contains hard tab characters (\\t)"

    def validate(self, data):
        if "\t" in data:
            return RuleViolation(self.id, self.error_str)


class MaxLineLengthRule(LineRule):
    """Rule: No line may exceed 80 (default) characters in length."""
    name = "max-line-length"
    id = "MD013"
    options_spec = [IntOption('line-length', 80, "Max line length")]
    error_str = "Line exceeds max length ({}>{})"

    def validate(self, data):
        max_length = self.options['line-length'].value
        if len(data) > max_length:
            return RuleViolation(self.id, self.error_str.format(len(data), max_length))
