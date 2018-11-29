from abc import abstractmethod, ABCMeta
import re
from pymarkdownlint.options import IntOption, StrOption
from pymarkdownlint.mdparser.parser import Parser


class Rule(object, metaclass=ABCMeta):
    """ Class representing markdown rules. """
    options_spec = []
    id = ""
    name = ""
    error_str = ""

    def __init__(self, opts={}):
        self.options = {}
        for spec in self.options_spec:
            self.options[spec.name] = spec.clone()
            actual_option = opts.get(spec.name)
            if actual_option:
                self.options[spec.name].set(actual_option)

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

