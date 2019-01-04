from pymarkdownlint.tests import BaseTestCase
from pymarkdownlint import cli
from pymarkdownlint import __version__

from click.testing import CliRunner


class CLITests(BaseTestCase):
    def setUp(self):
        self.cli = CliRunner()

    def assert_output_line(self, output, index, sample_filename, error_line, expected_error):
        expected_output = "{}:{}: {}".format(self.get_sample_path(sample_filename), error_line, expected_error)
        self.assertEqual(output.split("\n")[index], expected_output)

    def test_no_errors(self):
        result = self.cli.invoke(cli.cli, [self.get_sample_path("good.md")])
        self.assertEqual(result.output, "")
        self.assertEqual(result.exit_code, 0)

    def test_version(self):
        result = self.cli.invoke(cli.cli, ["--version"])
        self.assertEqual(result.output.split("\n")[0], "cli, version {}".format(__version__))

    def test_config_file(self):
        args = ["--config", self.get_sample_path("markdownlint"), self.get_sample_path("sample1.md")]
        result = self.cli.invoke(cli.cli, args)
        expected_string = "Using config from {}".format(self.get_sample_path("markdownlint"))
        self.assertEqual(result.output.split("\n")[0], expected_string)
        self.assert_output_line(result.output, 1, "sample1.md", 4, "MD009 Line has trailing whitespace")
        self.assert_output_line(result.output, 2, "sample1.md", 5, "MD009 Line has trailing whitespace")
        self.assert_output_line(result.output, 3, "sample1.md", 5, "MD010 Line contains hard tab characters (\\t)")
        self.assertEqual(result.exit_code, 3)

    def test_config_file_negative(self):
        args = ["--config", self.get_sample_path("foo"), self.get_sample_path("sample1.md")]
        result = self.cli.invoke(cli.cli, args)
        expected_string = "Error: Invalid value for \"--config\": Path \"{}\" does not exist.".format(
            self.get_sample_path("foo"))
        self.assertEqual(result.output.split("\n")[3], expected_string)

    def test_violations(self):
        result = self.cli.invoke(cli.cli, [self.get_sample_path("sample1.md")])
        self.assert_output_line(result.output, 0, "sample1.md", 3, "MD013 Line exceeds max length (119>80)")
        self.assert_output_line(result.output, 1, "sample1.md", 4, "MD009 Line has trailing whitespace")
        self.assert_output_line(result.output, 2, "sample1.md", 5, "MD009 Line has trailing whitespace")
        self.assert_output_line(result.output, 3, "sample1.md", 5, "MD010 Line contains hard tab characters (\\t)")
        self.assertEqual(result.exit_code, 4)

    def test_violations_with_ignored_rules(self):
        args = ["--ignore", "trailing-whitespace,MD010", self.get_sample_path("sample1.md")]
        result = self.cli.invoke(cli.cli, args)
        self.assert_output_line(result.output, 0, "sample1.md", 3, "MD013 Line exceeds max length (119>80)")
        self.assertEqual(result.exit_code, 1)

    def test_cli_list_files(self):
        result = self.cli.invoke(cli.cli, ["--list-files", self.get_sample_path()])
        expected_list = []
        expected_files = ["good.md", "sample1.md", "sample2.md", "filtering.md"]
        for f in expected_files:
            expected_list.append(self.get_sample_path(f))
        self.assertCountEqual(result.output.split('\n')[:-1], expected_list)
        self.assertEqual(result.exit_code, 0)
