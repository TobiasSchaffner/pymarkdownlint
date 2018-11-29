from pymarkdownlint.options import IntOption, StrOption
from pymarkdownlint.rules.base import FileRule, RuleViolation
from pymarkdownlint.mdparser.tag import Tag
from pymarkdownlint.mdparser.parser import Parser


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


class TopLevelListIndent(FileRule):
    """Rule: Bulleted lists should start at beginning of line."""
    name = "ul-start-left"
    id = "MD006"
    error_str = "Consider starting bulleted lists at beginning of line"

    def validate(self, parser):
        last_line = None

        for line in parser.lines:
            if last_line and (last_line != Tag.unlist or last_line != Tag.ordlist):
                # Check if there is space between the start and the list
                if len(line.text) != len(line.text.lstrip()):
                    return RuleViolation(self.id, self.error_str, line.lineno)

            last_line = line.tag
