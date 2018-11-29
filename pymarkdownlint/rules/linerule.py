import re
from pymarkdownlint.options import IntOption, StrOption
from pymarkdownlint.rules.base import LineRule, RuleViolation


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
