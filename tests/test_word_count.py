import argparse
import contextlib
import io
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))

import word_count as wc  # noqa: E402

FRONTMATTER = """---
title: "Ten words that must never be counted in the total"
slug: a-post
tags: [one, two]
---
"""


class CountTests(unittest.TestCase):
    def test_plain_prose(self):
        self.assertEqual(wc.count_words("One two three four."), 4)

    def test_empty(self):
        self.assertEqual(wc.count_words(""), 0)

    def test_frontmatter_is_excluded(self):
        self.assertEqual(wc.count_words(FRONTMATTER + "\n# Title here\n\nThree more words.\n"), 5)

    def test_unclosed_frontmatter_is_counted_as_text(self):
        self.assertEqual(wc.count_words("---\none two\n"), 2)

    def test_horizontal_rule_later_in_body_is_not_frontmatter(self):
        self.assertEqual(wc.count_words("One two.\n\n---\n\nThree four.\n"), 4)

    def test_backtick_code_block_is_excluded(self):
        text = "Before the block.\n\n```python\nprint('these words are code')\n```\n\nAfter it.\n"
        self.assertEqual(wc.count_words(text), 5)

    def test_tilde_code_block_is_excluded(self):
        self.assertEqual(wc.count_words("One.\n\n~~~\nskip skip skip\n~~~\n\nTwo.\n"), 2)

    def test_fence_of_other_type_does_not_close_block(self):
        self.assertEqual(wc.count_words("One.\n\n```\nskip\n~~~\nskip\n```\n\nTwo.\n"), 2)

    def test_longer_fence_wraps_shorter(self):
        self.assertEqual(wc.count_words("One.\n\n````\n```\nskip\n```\n````\n\nTwo.\n"), 2)

    def test_unclosed_code_block_runs_to_end(self):
        self.assertEqual(wc.count_words("One two.\n\n```\nskip skip\n"), 2)

    def test_inline_code_is_counted(self):
        self.assertEqual(wc.count_words("Run `pytest` now."), 3)

    def test_urls_and_markdown_syntax_are_ignored(self):
        self.assertEqual(wc.count_words("See [the docs](https://example.com/a-b-c) for **more**."), 5)

    def test_html_comments_are_excluded(self):
        self.assertEqual(wc.count_words("One <!-- hidden note\nover lines --> two."), 2)

    def test_frontmatter_and_code_together(self):
        text = FRONTMATTER + "\nIntro words here.\n\n```\ncode code\n```\n\nEnd.\n"
        self.assertEqual(wc.count_words(text), 4)


class TargetTests(unittest.TestCase):
    def test_required_defaults(self):
        self.assertEqual(wc.MODE_TARGETS["news"], (800, 1200))
        self.assertEqual(wc.MODE_TARGETS["build-log"], (1000, 1800))
        self.assertEqual(wc.MODE_TARGETS["portfolio"], (550, 900))

    def test_all_ranges_are_valid(self):
        for name, (low, high) in wc.MODE_TARGETS.items():
            with self.subTest(mode=name):
                self.assertTrue(0 < low < high)

    def test_parse_target(self):
        self.assertEqual(wc.parse_target("800-1200"), (800, 1200))
        self.assertEqual(wc.parse_target(" 500 - 500 "), (500, 500))

    def test_parse_target_rejects_bad_input(self):
        for value in ("800", "1200-800", "0-10", "a-b"):
            with self.subTest(value=value):
                with self.assertRaises(argparse.ArgumentTypeError):
                    wc.parse_target(value)

    def test_target_overrides_mode(self):
        self.assertEqual(wc.resolve_target((10, 20), "news"), (10, 20))
        self.assertEqual(wc.resolve_target(None, "news"), (800, 1200))
        self.assertIsNone(wc.resolve_target(None, None))


class CliTests(unittest.TestCase):
    def run_main(self, text, *options):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "draft.md"
            path.write_text(text, encoding="utf-8")
            argv, sys.argv = sys.argv, ["word_count.py", str(path), *options]
            try:
                with contextlib.redirect_stdout(io.StringIO()) as output:
                    return wc.main(), output.getvalue()
            finally:
                sys.argv = argv

    def test_no_target_exits_zero(self):
        code, output = self.run_main("One two three.")
        self.assertEqual(code, 0)
        self.assertIn("Word count: 3", output)

    def test_mode_pass_and_flag(self):
        self.assertEqual(self.run_main("word " * 1000, "--mode", "news")[0], 0)
        code, output = self.run_main("word " * 10, "--mode", "build-log")
        self.assertEqual(code, 1)
        self.assertIn("990 word(s) below target range (1000-1800", output)

    def test_portfolio_mode_flags_a_long_post(self):
        self.assertEqual(self.run_main("word " * 800, "--mode", "portfolio")[0], 0)
        code, output = self.run_main("word " * 1300, "--mode", "portfolio")
        self.assertEqual(code, 1)
        self.assertIn("above target range", output)

    def test_blog_mode_matches_portfolio_alias(self):
        self.assertEqual(wc.MODE_TARGETS["blog"], wc.MODE_TARGETS["portfolio"])
        self.assertEqual(self.run_main("word " * 800, "--mode", "blog")[0], 0)
        self.assertEqual(self.run_main("word " * 1300, "--mode", "blog")[0], 1)

    def test_target_overrides_mode_on_cli(self):
        code, output = self.run_main("word " * 10, "--mode", "news", "--target", "5-20")
        self.assertEqual(code, 0)
        self.assertIn("from --target", output)

    def test_frontmatter_does_not_push_draft_into_range(self):
        self.assertEqual(self.run_main(FRONTMATTER + "\nOne two.\n", "--target", "3-100")[0], 1)


if __name__ == "__main__":
    unittest.main()
