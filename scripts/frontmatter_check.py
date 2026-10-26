#!/usr/bin/env python3
"""Validate the YAML frontmatter of a blog post and flag unfilled placeholders."""

from __future__ import annotations

import argparse
import re
import sys
from datetime import date
from pathlib import Path

REQUIRED_FIELDS = ("title", "slug", "date", "tags", "summary", "status", "repo_url")
NON_EMPTY_FIELDS = ("title", "slug", "date", "summary", "status")
URL_FIELDS = ("repo_url", "canonical_url")
STATUS_VALUES = ("draft", "published")
PLACEHOLDER = "[AUTHOR TO FILL"

SLUG_PATTERN = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*")
DATE_PATTERN = re.compile(r"\d{4}-\d{2}-\d{2}")
URL_PATTERN = re.compile(r"https?://\S+")
KEY_PATTERN = re.compile(r"([A-Za-z_][\w-]*)\s*:\s*(.*)")
LIST_ITEM_PATTERN = re.compile(r"\s*-\s+(.*)")


def unquote(value: str) -> str:
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
        return value[1:-1]
    return value


def split_frontmatter(text: str) -> tuple[str | None, str]:
    """Return (frontmatter, body); frontmatter is None when the block is missing or unclosed."""
    lines = text.lstrip("﻿").splitlines()
    if not lines or lines[0].strip() != "---":
        return None, text
    for index in range(1, len(lines)):
        if lines[index].strip() in ("---", "..."):
            return "\n".join(lines[1:index]), "\n".join(lines[index + 1 :])
    return None, text


def parse_frontmatter(frontmatter: str) -> dict[str, str | list[str]]:
    """Parse the simple YAML subset used by posts: scalars, inline lists, and block lists."""
    fields: dict[str, str | list[str]] = {}
    current: str | None = None
    for line in frontmatter.splitlines():
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        item = LIST_ITEM_PATTERN.fullmatch(line)
        if item and current is not None and (fields[current] == "" or isinstance(fields[current], list)):
            if fields[current] == "":
                fields[current] = []
            fields[current].append(unquote(item.group(1)))
            continue
        match = KEY_PATTERN.fullmatch(line.rstrip())
        if match and not line[0].isspace():
            current = match.group(1)
            fields[current] = unquote(match.group(2))
        else:
            current = None
    return fields


def as_list(value: str | list[str]) -> list[str]:
    """Normalise a block list or an inline ``[a, b]`` list to non-empty strings."""
    if isinstance(value, str):
        stripped = value.strip()
        if not (stripped.startswith("[") and stripped.endswith("]")):
            return []
        value = [unquote(part) for part in stripped[1:-1].split(",")]
    return [item.strip() for item in value if item.strip()]


def find_placeholders(text: str) -> list[int]:
    """Return the 1-based line number of every placeholder occurrence."""
    return [
        number
        for number, line in enumerate(text.splitlines(), start=1)
        for _ in range(line.count(PLACEHOLDER))
    ]


def validate(text: str, filename: str | None = None) -> tuple[list[str], list[str]]:
    """Return (errors, warnings) for one post."""
    errors: list[str] = []
    warnings: list[str] = []

    frontmatter, _ = split_frontmatter(text)
    if frontmatter is None:
        return ["frontmatter: no '---' delimited block at the top of the file"], warnings
    fields = parse_frontmatter(frontmatter)

    for name in REQUIRED_FIELDS:
        if name not in fields:
            errors.append(f"{name}: required field is missing")
    for name in NON_EMPTY_FIELDS:
        if name in fields and not (isinstance(fields[name], str) and fields[name].strip()):
            errors.append(f"{name}: must be a non-empty value")

    def scalar(name: str) -> str | None:
        """Return a field worth format-checking: present, non-empty, and not a placeholder."""
        value = fields.get(name)
        if not isinstance(value, str) or not value.strip() or PLACEHOLDER in value:
            return None
        return value.strip()

    slug = scalar("slug")
    if slug and not SLUG_PATTERN.fullmatch(slug):
        errors.append(f"slug: '{slug}' must be lowercase letters and digits separated by single hyphens")
    if slug and filename and SLUG_PATTERN.fullmatch(slug) and Path(filename).stem != slug:
        warnings.append(f"slug: '{slug}' does not match the file name '{Path(filename).name}'")

    post_date = scalar("date")
    if post_date:
        if not DATE_PATTERN.fullmatch(post_date):
            errors.append(f"date: '{post_date}' must use YYYY-MM-DD")
        else:
            try:
                date.fromisoformat(post_date)
            except ValueError:
                errors.append(f"date: '{post_date}' is not a real calendar date")

    status = scalar("status")
    if status and status not in STATUS_VALUES:
        errors.append(f"status: '{status}' must be one of: {', '.join(STATUS_VALUES)}")

    if "tags" in fields and not as_list(fields["tags"]):
        errors.append("tags: must be a list with at least one tag, e.g. [python, claude]")

    for name in URL_FIELDS:
        url = scalar(name)
        if url and not URL_PATTERN.fullmatch(url):
            errors.append(f"{name}: '{url}' must be an http(s) URL or empty")

    placeholder_lines = find_placeholders(text)
    if placeholder_lines:
        where = ", ".join(str(number) for number in placeholder_lines)
        message = f"placeholders: {len(placeholder_lines)} '{PLACEHOLDER}' marker(s) left on line(s) {where}"
        if status == "published":
            errors.append(message + "; a published post must have none")
        else:
            warnings.append(message)

    return errors, warnings


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate post frontmatter and flag unfilled placeholders.")
    parser.add_argument("posts", type=Path, nargs="+", help="Path(s) to Markdown post files")
    args = parser.parse_args()

    missing = [path for path in args.posts if not path.is_file()]
    if missing:
        for path in missing:
            print(f"FAIL: Markdown file not found: {path}", file=sys.stderr)
        return 2

    failed = 0
    for path in args.posts:
        errors, warnings = validate(path.read_text(encoding="utf-8"), path.name)
        for message in errors:
            print(f"ERROR {path}: {message}")
        for message in warnings:
            print(f"WARN  {path}: {message}")
        if errors:
            failed += 1
            print(f"FAIL: {path} has {len(errors)} error(s).")
        else:
            print(f"PASS: {path} frontmatter is valid.")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
