"""Some utility functions to make life easier."""


def count_first_seq(string, char):
    """Counts and returns the sequence of chars at the start of the string."""
    for i, c in enumerate(string):
        if c != char: return i

    return len(string)
