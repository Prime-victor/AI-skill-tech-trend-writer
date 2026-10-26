import contextlib
import io
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))

import table_check as tc  # noqa: E402

GOOD = """# Post

Intro sentence.

| Model | Context (tokens) | Source |
| --- | ---: | --- |
| A | 200,000 | [Docs](https://example.com/a) |
| B | 128,000 | [Docs](https://example.com/b) |

After the table.
"""


def table(*rows, header="| Metric | Before | After |", separator="| --- | --- | --- |"):
    return "Intro.\n\n" + "\n".join([header, separator, *rows]) + "\n\nOutro.\n"


class ParsingTests(unittest.TestCase):
    def test_split_row(self):
        self.assertEqual(tc.split_row("| a | b |  |"), ["a", "b", ""])
        self.assertEqual(tc.split_row("a | b"), ["a", "b"])
        self.assertEqual(tc.split_row(r"| a \| b | c |"), [r"a \| b", "c"])

    def test_is_separator(self):
        for line in ("| --- | --- |", "|:--|--:|", "--- | :---:"):
            with self.subTest(line=line):
                self.assertTrue(tc.is_separator(line))
        for line in ("| a | b |", "---", "| --- | x |", ""):
            with self.subTest(line=line):
                self.assertFalse(tc.is_separator(line))

    def test_finds_table_with_line_numbers(self):
        tables, errors = tc.find_tables(GOOD)
        self.assertEqual(errors, [])
        self.assertEqual(len(tables), 1)
        self.assertEqual(tables[0].line, 5)
        self.assertEqual(tables[0].header, ["Model", "Context (tokens)", "Source"])
        self.assertEqual([line for line, _ in tables[0].rows], [7, 8])

    def test_tables_in_code_blocks_and_frontmatter_are_ignored(self):
        text = "---\ntitle: a | b\n---\n\n```\n| a | b |\n| --- | --- |\n|  |  |\n```\n\n    | x |\n"
        self.assertEqual(tc.find_tables(text), ([], []))

    def test_pipe_in_prose_is_not_a_table(self):
        self.assertEqual(tc.find_tables("Run `a | b` to pipe output.\n"), ([], []))

    def test_two_tables(self):
        self.assertEqual(len(tc.find_tables(GOOD + "\n" + table("| x | 1 | 2 |", "| y | 3 | 4 |"))[0]), 2)


class CheckTests(unittest.TestCase):
    def assertError(self, text, fragment, **options):
        errors, _, _ = tc.check(text, **options)
        self.assertTrue(any(fragment in error for error in errors), f"{fragment!r} not in {errors}")

    def assertWarning(self, text, fragment):
        errors, warnings, _ = tc.check(text)
        self.assertEqual(errors, [])
        self.assertTrue(any(fragment in warning for warning in warnings), f"{fragment!r} not in {warnings}")

    def test_good_table_passes(self):
        self.assertEqual(tc.check(GOOD), ([], [], 1))

    def test_no_table_is_fine_unless_required(self):
        self.assertEqual(tc.check("Just prose.\n"), ([], [], 0))
        self.assertError("Just prose.\n", "no table found", require_table=True)

    def test_empty_cell(self):
        self.assertError(table("| Latency | 2.1 s |  |", "| Cost | $4 | $2 |"), "line 5: empty cell under 'After'")

    def test_filler_cells(self):
        for filler in ("-", "N/A", "TBD", "?", "...", "**TBD**", "Various", "—"):
            with self.subTest(filler=filler):
                self.assertError(table(f"| Latency | 2.1 s | {filler} |", "| Cost | $4 | $2 |"), "filler")

    def test_explicit_absence_is_allowed(self):
        text = table("| Latency | Not measured | 0.8 s |", "| Cost | Not disclosed | None |")
        self.assertEqual(tc.check(text)[0], [])

    def test_short_and_long_rows(self):
        self.assertError(table("| Latency | 2.1 s |", "| Cost | $4 | $2 |"), "row has 2 cell(s) but the header has 3")
        self.assertError(table("| Latency | 2.1 s | 0.8 s | x |", "| Cost | $4 | $2 |"), "row has 4 cell(s)")

    def test_escaped_pipe_does_not_add_a_cell(self):
        self.assertEqual(tc.check(table(r"| a \| b | 1 | 2 |", "| c | 3 | 4 |"))[0], [])

    def test_header_separator_mismatch(self):
        self.assertError(table("| a | 1 | 2 |", "| b | 3 | 4 |", separator="| --- | --- |"), "will not render")

    def test_missing_separator_row(self):
        self.assertError("Intro.\n\n| Metric | Before |\n| Latency | 2.1 s |\n", "not part of a table")

    def test_empty_header_cell(self):
        self.assertError(table("| a | 1 | 2 |", "| b | 3 | 4 |", header="| Metric |  | After |"), "header cell 2 is empty")

    def test_no_body_rows(self):
        self.assertError(table(), "no body rows")

    def test_single_row_warns(self):
        self.assertWarning(table("| Latency | 2.1 s | 0.8 s |"), "only 1 body row")

    def test_missing_blank_line_before_warns(self):
        text = "Intro.\n| Metric | Before |\n| --- | --- |\n| a | 1 |\n| b | 2 |\n"
        self.assertWarning(text, "no blank line before")

    def test_wide_table_warns(self):
        header = "| " + " | ".join(f"c{n}" for n in range(7)) + " |"
        separator = "|" + " --- |" * 7
        row = "| " + " | ".join("v" for _ in range(7)) + " |"
        self.assertWarning(table(row, row, header=header, separator=separator), "7 columns")

    def test_author_placeholders_warn_but_pass(self):
        text = table("| Latency | [AUTHOR TO FILL: before] | [AUTHOR TO FILL: after] |", "| Cost | $4 | $2 |")
        self.assertWarning(text, "2 cell(s) still hold")


class CliTests(unittest.TestCase):
    def run_main(self, text, *options):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "post.md"
            path.write_text(text, encoding="utf-8")
            argv, sys.argv = sys.argv, ["table_check.py", str(path), *options]
            try:
                with contextlib.redirect_stdout(io.StringIO()) as output:
                    return tc.main(), output.getvalue()
            finally:
                sys.argv = argv

    def test_exit_codes(self):
        self.assertEqual(self.run_main(GOOD)[0], 0)
        code, output = self.run_main(table("| Latency | 2.1 s | TBD |", "| Cost | $4 | $2 |"))
        self.assertEqual(code, 1)
        self.assertIn("ERROR", output)

    def test_require_table(self):
        self.assertEqual(self.run_main("Prose only.\n")[0], 0)
        self.assertEqual(self.run_main("Prose only.\n", "--require-table")[0], 1)

    def test_missing_file_exits_2(self):
        argv, sys.argv = sys.argv, ["table_check.py", "no-such-post.md"]
        try:
            with contextlib.redirect_stderr(io.StringIO()):
                self.assertEqual(tc.main(), 2)
        finally:
            sys.argv = argv


if __name__ == "__main__":
    unittest.main()
