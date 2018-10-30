"""Markdown Parser."""
from .tag import get_line_type


class Parser:
    """Markdown Parser."""

    def __init__(self, text):
        """Initializes the parser with text, and parses it, line by line."""
        self.text = text

    def parse(self):
        """Parses the text, line by line."""
        for n, line in enumerate(self.text.split('\n'), 1):
            line = get_line_type(line)
