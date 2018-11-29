# pymarkdownlint

[![Travis (.org)](https://img.shields.io/travis/com/cheukyin699/pymarkdownlint.svg?style=for-the-badge)](https://travis-ci.com/cheukyin699/pymarkdownlint)
[![Codecov](https://img.shields.io/codecov/c/github/cheukyin699/pymarkdownlint.svg?style=for-the-badge)](https://codecov.io/gh/cheukyin699/pymarkdownlint/)
![Python Versions](https://img.shields.io/badge/python-3.7-blue.svg?style=for-the-badge)

Markdown linter written in python. Inspired by [mivok/markdownlint](https://github.com/mivok/markdownlint).

Get started by running:

```bash
markdownlint examples/             # lint all files in a directory
markdownlint examples/example1.md  # lint a single file
markdownlint examples/example1.md  # lint a single file
```

NOTE: The returned exit code equals the number of errors found.

Other commands and variations:

```bash
Usage: markdownlint [OPTIONS] PATH

Markdown lint tool, checks your markdown for styling issues

Options:
  --config PATH  Config file location (default: .markdownlint).
  --list-files   List markdown files in given path and exit.
  --ignore TEXT  Ignore rules (comma-separated by id or name).
  --version      Show the version and exit.
  --help         Show this message and exit.
```

You can modify pymarkdownlint's behavior by specifying a config file like so:

```bash
markdownlint --config myconfigfile
```

By default, markdownlint will look for an **optional** `.markdownlint` file for configuration.

## Config file

```
[general]
# rules can be ignored by name or by id
ignore=max-line-length,MD013
```

## Supported Rules

Please see the ruleset [here][ruleset].

## Development

Installation:

```bash
# Use pipenv for development
pip install pipenv
pipenv install --dev
pipenv shell
```

To run tests:

```bash
pipenv shell        # If you have not run this yet
pytest
```

## Wishlist

- More rules!
- Better output handling with verbosity levels
- Ignore/exclude files CLI options
- Rule specific configuration in config files
- Auto doc generation based on rules

[ruleset]: https://github.com/markdownlint/markdownlint/blob/master/docs/RULES.md
