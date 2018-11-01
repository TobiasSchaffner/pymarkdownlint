"""Markdown Parser."""
from .tag import get_line_type


class Line:
    """Stores information on a single line."""

    def __init__(self, lineno, text):
        """
        Initializes object.

        Note: self.inlines contains data formatted as such:
        Key: type of Tag
        Data: list of positions the tag occurs at
        """
        self.text = text
        self.lineno = lineno
        self.inlines = {}

        # Do analysis on the line as a whole
        self.tag, self.indents, self.meta = get_line_type(text)

        # Do analysis on smaller things
        self.analyze()

    def __str__(self):
        """Debug purposes."""
        return str(self.__dict__)

    def __repr__(self):
        """Debug purposes."""
        return str(self)

    def analyze(self):
        """
        Analyzes the text itself and stores positions of in-text decorators.

        Returns nothing, but the analyzed data can be extracted.
        """
        # TODO
        pass


class Parser:
    """Markdown Parser."""

    def __init__(self, text):
        """Initializes the parser with text, and parses it, line by line."""
        self.text = text
        self.lines = []
        self.parse()

    def parse(self):
        """Parses the text, line by line."""
        for n, line in enumerate(self.text.split('\n'), 1):
            self.lines.append(Line(n, line))

    def __getitem__(self, attr):
        """Finds a list of lines that match the given type."""
        return list(filter(lambda l: l.tag.name == attr, self.lines))
