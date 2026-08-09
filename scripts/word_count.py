#!/usr/bin/env python3
"""Report Markdown word count, reading time, and optional target-range compliance."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

WORDS_PER_MINUTE = 200


def count_words(markdown: str) -> int:
    """Count word-like tokens after removing common Markdown syntax and URLs."""
    text = re.sub(r"https?://\S+", "", markdown)
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


def main() -> int:
    parser = argparse.ArgumentParser(description="Count words in a Markdown draft.")
    parser.add_argument("draft", type=Path, help="Path to the Markdown draft")
    parser.add_argument("--target", type=parse_target, help="Optional range, e.g. 800-1200")
    args = parser.parse_args()

    if not args.draft.is_file():
        print(f"FAIL: Markdown file not found: {args.draft}", file=sys.stderr)
        return 2

    words = count_words(args.draft.read_text(encoding="utf-8"))
    minutes = max(1, round(words / WORDS_PER_MINUTE)) if words else 0
    print(f"Word count: {words}")
    print(f"Estimated reading time: {minutes} minute(s) at {WORDS_PER_MINUTE} wpm")

    if not args.target:
        return 0
    low, high = args.target
    if low <= words <= high:
        print(f"PASS: Within target range ({low}-{high} words).")
        return 0
    direction = "below" if words < low else "above"
    difference = (low - words) if words < low else (words - high)
    print(f"FLAG: {difference} word(s) {direction} target range ({low}-{high} words).")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
