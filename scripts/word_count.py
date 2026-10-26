#!/usr/bin/env python3
"""Report Markdown word count, reading time, and optional target-range compliance."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

WORDS_PER_MINUTE = 200

# Default length targets per mode or structure; --target overrides them.
MODE_TARGETS: dict[str, tuple[int, int]] = {
    "news": (800, 1200),
    "brief": (300, 600),
    "roundup": (800, 1200),
    "deep-dive": (1500, 2500),
    "firsthand": (1000, 1800),
    "build-log": (1000, 1800),
    "lessons-learned": (900, 1500),
    "opinion": (700, 1200),
    "explainer": (1200, 2000),
    "experiment": (1000, 1800),
    # A 3-5 minute read on a typical blog, which also counts code blocks and tables.
    "blog": (550, 900),
    # Older name for "blog", kept so existing commands keep working.
    "portfolio": (550, 900),
}

FENCE_PATTERN = re.compile(r" {0,3}(\x60{3,}|~{3,})")


def strip_frontmatter(markdown: str) -> str:
    """Remove a leading '---' delimited YAML block; leave the text alone if it is unclosed."""
    lines = markdown.lstrip("﻿").splitlines()
    if not lines or lines[0].strip() != "---":
        return markdown
    for index in range(1, len(lines)):
        if lines[index].strip() in ("---", "..."):
            return "\n".join(lines[index + 1 :])
    return markdown


def strip_code_blocks(markdown: str) -> str:
    """Remove fenced code blocks, including an unclosed one that runs to the end."""
    kept: list[str] = []
    fence: str | None = None
    for line in markdown.splitlines():
        match = FENCE_PATTERN.match(line)
        if fence is None:
            if match:
                fence = match.group(1)
            else:
                kept.append(line)
        elif match and match.group(1)[0] == fence[0] and len(match.group(1)) >= len(fence):
            fence = None
    return "\n".join(kept)


def count_words(markdown: str) -> int:
    """Count prose words, ignoring frontmatter, code blocks, comments, Markdown syntax, and URLs."""
    text = strip_code_blocks(strip_frontmatter(markdown))
    text = re.sub(r"<!--.*?-->", " ", text, flags=re.DOTALL)
    text = re.sub(r"https?://\S+", "", text)
    text = re.sub(r"[\x60*_#>\[\](){}|]", " ", text)
    return len(re.findall(r"\b[\w'-]+\b", text, flags=re.UNICODE))


def parse_target(value: str) -> tuple[int, int]:
    match = re.fullmatch(r"\s*(\d+)\s*-\s*(\d+)\s*", value)
    if not match:
        raise argparse.ArgumentTypeError("target must use MIN-MAX, for example 800-1200")
    low, high = map(int, match.groups())
    if low <= 0 or high < low:
        raise argparse.ArgumentTypeError("target values must be positive and MIN must not exceed MAX")
    return low, high


def resolve_target(target: tuple[int, int] | None, mode: str | None) -> tuple[int, int] | None:
    """An explicit --target wins over the default range for --mode."""
    if target:
        return target
    return MODE_TARGETS[mode] if mode else None


def main() -> int:
    modes = ", ".join(f"{name} {low}-{high}" for name, (low, high) in MODE_TARGETS.items())
    parser = argparse.ArgumentParser(description="Count words in a Markdown draft.")
    parser.add_argument("draft", type=Path, help="Path to the Markdown draft")
    parser.add_argument("--mode", choices=sorted(MODE_TARGETS), help=f"Use a default target range: {modes}")
    parser.add_argument("--target", type=parse_target, help="Range that overrides --mode, e.g. 800-1200")
    args = parser.parse_args()

    if not args.draft.is_file():
        print(f"FAIL: Markdown file not found: {args.draft}", file=sys.stderr)
        return 2

    words = count_words(args.draft.read_text(encoding="utf-8"))
    minutes = max(1, round(words / WORDS_PER_MINUTE)) if words else 0
    print(f"Word count: {words} (frontmatter and code blocks excluded)")
    print(f"Estimated reading time: {minutes} minute(s) at {WORDS_PER_MINUTE} wpm")

    target = resolve_target(args.target, args.mode)
    if not target:
        return 0
    low, high = target
    source = "--target" if args.target else f"--mode {args.mode}"
    if low <= words <= high:
        print(f"PASS: Within target range ({low}-{high} words, from {source}).")
        return 0
    direction = "below" if words < low else "above"
    difference = (low - words) if words < low else (words - high)
    print(f"FLAG: {difference} word(s) {direction} target range ({low}-{high} words, from {source}).")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
