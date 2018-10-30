"""HTML tag types."""
from enum import Enum
from .utils import count_first_seq

class Tag(Enum):
    """Types of HTML tags."""
    heading = 0
    newline = 1
    paragraph = 2
    blockquote = 3
    unlist = 4
    ordlist = 5
    codeblock = 6
    incode = 10
    bold = 11
    italic = 12
    strikethru = 13


def get_line_type(line):
    """
    Given a line, gives the type of the line, along with extra informations.

    Returns the tuple (Tag, indents, data), where
    - Tag is the type of line
    - indents is the number of space characters before the line starts
    - data is any metadata

    Stored metadata includes the level of heading, the numbering on an
    ordered list, and the symbol used as indicator of an unordered list.
    """
    orig = line
    line = line.lstrip()
    indents = len(orig) - len(line)
    line = line.rstrip()
    if not line:
        return Tag.newline, indents, 0

    if line[0] == '#':
        return Tag.heading, indents, count_first_seq(line, '#')
    if line[0] == '>':
        return Tag.blockquote, indents, 0
    if line[0] in '*-+':
        return Tag.unlist, indents, line[0]

    try:
        num = int(line.split('.')[0])
        return Tag.ordlist, indents, num
    except ValueError:
        pass

    return Tag.paragraph, indents, 0
