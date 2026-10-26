import contextlib
import io
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))

import frontmatter_check as fc  # noqa: E402

VALID = """---
title: "How I built a thing"
slug: how-i-built-a-thing
date: 2026-01-15
tags: [python, claude]
summary: "A short summary: with a colon."
status: draft
repo_url: "https://github.com/user/thing"
canonical_url: ""
---

# How I built a thing

Body text.
"""

PLACEHOLDER_BODY = "\nLatency fell to [AUTHOR TO FILL: after value] ms.\n[AUTHOR TO FILL: anecdote]\n"


def post(**overrides):
    """Return VALID with whole frontmatter lines replaced or (value None) removed."""
    lines = []
    for line in VALID.splitlines():
        key = line.split(":", 1)[0]
        if key in overrides:
            if overrides[key] is not None:
                lines.append(f"{key}: {overrides[key]}")
        else:
            lines.append(line)
    return "\n".join(lines) + "\n"


class ParseTests(unittest.TestCase):
    def test_split_returns_frontmatter_and_body(self):
        frontmatter, body = fc.split_frontmatter(VALID)
        self.assertIn("slug: how-i-built-a-thing", frontmatter)
        self.assertNotIn("slug:", body)
        self.assertIn("Body text.", body)

    def test_split_without_frontmatter(self):
        self.assertEqual(fc.split_frontmatter("# Title\n\nText"), (None, "# Title\n\nText"))

    def test_split_unclosed_frontmatter(self):
        self.assertIsNone(fc.split_frontmatter("---\ntitle: x\n\n# Title\n")[0])

    def test_parse_scalars_and_quotes(self):
        fields = fc.parse_frontmatter(fc.split_frontmatter(VALID)[0])
        self.assertEqual(fields["title"], "How I built a thing")
        self.assertEqual(fields["summary"], "A short summary: with a colon.")
        self.assertEqual(fields["canonical_url"], "")

    def test_inline_and_block_lists(self):
        self.assertEqual(fc.as_list("[python, 'claude', ]"), ["python", "claude"])
        fields = fc.parse_frontmatter("tags:\n  - python\n  - claude\n  - skills\nstatus: draft")
        self.assertEqual(fields["tags"], ["python", "claude", "skills"])
        self.assertEqual(fields["status"], "draft")


class ValidateTests(unittest.TestCase):
    def assertError(self, text, fragment, filename=None):
        errors, _ = fc.validate(text, filename)
        self.assertTrue(any(fragment in error for error in errors), f"{fragment!r} not in {errors}")

    def test_valid_post_passes(self):
        self.assertEqual(fc.validate(VALID, "how-i-built-a-thing.md"), ([], []))

    def test_missing_frontmatter(self):
        self.assertError("# Just a heading\n", "frontmatter")

    def test_each_required_field(self):
        for name in fc.REQUIRED_FIELDS:
            with self.subTest(field=name):
                self.assertError(post(**{name: None}), f"{name}: required field is missing")

    def test_canonical_url_is_optional(self):
        self.assertEqual(fc.validate(post(canonical_url=None))[0], [])

    def test_empty_repo_url_is_allowed(self):
        self.assertEqual(fc.validate(post(repo_url='""'))[0], [])

    def test_empty_title(self):
        self.assertError(post(title='""'), "title: must be a non-empty value")

    def test_bad_slugs(self):
        for slug in ("How-I-Built", "has_underscore", "double--hyphen", "-leading", "trailing-", "has space"):
            with self.subTest(slug=slug):
                self.assertError(post(slug=slug), "slug:")

    def test_good_slugs(self):
        for slug in ("post", "post-2", "2026-in-review"):
            with self.subTest(slug=slug):
                self.assertEqual(fc.validate(post(slug=slug))[0], [])

    def test_slug_filename_mismatch_is_a_warning(self):
        errors, warnings = fc.validate(VALID, "other-name.md")
        self.assertEqual(errors, [])
        self.assertTrue(any("does not match the file name" in warning for warning in warnings))

    def test_bad_dates(self):
        for value in ("15-01-2026", "2026/01/15", "2026-1-5", "January 15, 2026", "2026-02-30"):
            with self.subTest(date=value):
                self.assertError(post(date=value), "date:")

    def test_bad_status(self):
        self.assertError(post(status="live"), "status:")

    def test_published_status_is_valid(self):
        self.assertEqual(fc.validate(post(status="published"))[0], [])

    def test_bad_tags(self):
        self.assertError(post(tags="[]"), "tags:")
        self.assertError(post(tags="python"), "tags:")

    def test_block_list_tags_are_valid(self):
        self.assertEqual(fc.validate(post(tags="\n  - python\n  - claude"))[0], [])

    def test_bad_urls(self):
        self.assertError(post(repo_url="github.com/user/thing"), "repo_url:")
        self.assertError(post(canonical_url="not a url"), "canonical_url:")


class PlaceholderTests(unittest.TestCase):
    def test_line_numbers(self):
        self.assertEqual(fc.find_placeholders("a\n[AUTHOR TO FILL: x] and [AUTHOR TO FILL: y]\nb"), [2, 2])

    def test_draft_placeholders_warn_only(self):
        errors, warnings = fc.validate(VALID + PLACEHOLDER_BODY)
        self.assertEqual(errors, [])
        self.assertTrue(any("2 '[AUTHOR TO FILL' marker(s)" in warning for warning in warnings))

    def test_published_placeholders_are_errors(self):
        errors, _ = fc.validate(post(status="published") + PLACEHOLDER_BODY)
        self.assertTrue(any("published post must have none" in error for error in errors))

    def test_placeholder_in_frontmatter_field(self):
        text = post(repo_url='"[AUTHOR TO FILL: repo URL]"')
        self.assertEqual(fc.validate(text)[0], [])
        errors, _ = fc.validate(text.replace("status: draft", "status: published"))
        self.assertEqual(len(errors), 1)


class CliTests(unittest.TestCase):
    def run_main(self, text, name="how-i-built-a-thing.md"):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / name
            path.write_text(text, encoding="utf-8")
            argv, sys.argv = sys.argv, ["frontmatter_check.py", str(path)]
            try:
                with contextlib.redirect_stdout(io.StringIO()) as output:
                    return fc.main(), output.getvalue()
            finally:
                sys.argv = argv

    def test_valid_and_draft_with_placeholders_exit_zero(self):
        self.assertEqual(self.run_main(VALID)[0], 0)
        code, output = self.run_main(VALID + PLACEHOLDER_BODY)
        self.assertEqual(code, 0)
        self.assertIn("WARN", output)

    def test_published_with_placeholders_exits_non_zero(self):
        code, output = self.run_main(post(status="published") + PLACEHOLDER_BODY)
        self.assertEqual(code, 1)
        self.assertIn("ERROR", output)

    def test_missing_file_exits_2(self):
        argv, sys.argv = sys.argv, ["frontmatter_check.py", "no-such-post.md"]
        try:
            with contextlib.redirect_stderr(io.StringIO()):
                self.assertEqual(fc.main(), 2)
        finally:
            sys.argv = argv


if __name__ == "__main__":
    unittest.main()
