# pymarkdownlint

[![Travis (.org)](https://img.shields.io/travis/cheukyin699/pymarkdownlint.svg?style=for-the-badge)](https://travis-ci.com/cheukyin699/pymarkdownlint)
[![Codecov](https://img.shields.io/codecov/c/github/cheukyin699/pymarkdownlint.svg?style=for-the-badge)](https://codecov.io/gh/cheukyin699/pymarkdownlint/)

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

## Config file ##

```
[general]
# rules can be ignored by name or by id
ignore=max-line-length, R3
```

## Supported Rules ##

ID    | Name                | Description
------|---------------------|----------------------------------------------------
R1    | max-line-length     | Line length must be &lt; 80 chars.
R2    | trailing-whitespace | Line cannot have trailing whitespace (space or tab)
R3    | hard-tabs           | Line contains hard tab characters (\t)

## Development ##

Installation:
```bash
# Use pipenv for development
pip install pipenv
pipenv install --dev
pipenv shell
```

To run tests:
```bash
pipenv shell        # If you have yet to run this
pytest
```

## Wishlist ##
- More rules!
- Better output handling with verbosity levels
- Ignore/exclude files CLI options
- Rule specific configuration in config files
- Auto doc generation based on rules
