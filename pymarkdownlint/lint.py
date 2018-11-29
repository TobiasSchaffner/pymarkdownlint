from pymarkdownlint.rules.base import LineRule, FileRule
from pymarkdownlint.mdparser.parser import Parser


class MarkdownLinter(object):
    def __init__(self, config):
        self.config = config

    @property
    def line_rules(self):
        return [rule for rule in self.config.rules if isinstance(rule, LineRule)]

    @property
    def file_rules(self):
        return [rule for rule in self.config.rules if isinstance(rule, FileRule)]

    def _apply_line_rules(self, markdown_string):
        """ Iterates over the lines in a given markdown string and applies all the enabled line rules to each line """
        all_violations = []
        lines = markdown_string.split("\n")
        line_rules = self.line_rules
        ignoring = False
        for line_nr, line in enumerate(lines, 1):
            if ignoring:
                if line.strip() == '<!-- markdownlint:enable -->':
                    ignoring = False
            else:
                if line.strip() == '<!-- markdownlint:disable -->':
                    ignoring = True
                    continue

                for rule in line_rules:
                    violation = rule.validate(line)
                    if violation:
                        violation.data_nr = line_nr
                        all_violations.append(violation)
        return all_violations

    def _apply_file_rules(self, markdown_string):
        """Iterates through all filerules."""
        all_violations = []
        parser = Parser(markdown_string)
        for rule in self.file_rules:
            violation = rule.validate(parser)
            if violation:
                all_violations.append(violation)
        return all_violations

    def lint(self, markdown_string):
        all_violations = []
        all_violations.extend(self._apply_line_rules(markdown_string))
        all_violations.extend(self._apply_file_rules(markdown_string))
        return all_violations

    def lint_files(self, files):
        """ Lints a list of files.
        :param files: list of files to lint
        :return: a list of violations found in the files
        """
        all_violations = []
        for filename in files:
            with open(filename, 'r') as f:
                content = f.read()
                violations = self.lint(content)
                all_violations.extend(violations)
                for e in violations:
                    print("{}:{}: {} {}".format(filename, e.data_nr, e.rule_id, e.message))
        return len(all_violations)
