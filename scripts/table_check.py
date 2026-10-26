#!/usr/bin/env python3
"""Check Markdown tables in a post for structural problems and unpopulated cells."""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

FENCE_PATTERN = re.compile(r" {0,3}(\x60{3,}|~{3,})")
SEPARATOR_CELL_PATTERN = re.compile(r":?-+:?")
CELL_SPLIT_PATTERN = re.compile(r"(?<!\\)\|")
PLACEHOLDER = "[AUTHOR TO FILL"
FILLER_CELLS = {
    "-", "--", "---", "–", "—", "?", "??", "...", "…", "n/a", "na", "tbd", "tbc", "todo",
    "xx", "various", "varies", "unknown",
}
MIN_BODY_ROWS = 2
MAX_COLUMNS = 6


@dataclass
class Table:
    line: int
    header: list[str]
    rows: list[tuple[int, list[str]]] = field(default_factory=list)
    blank_line_before: bool = True


def split_row(line: str) -> list[str]:
    """Split a table row into stripped cells, honouring escaped pipes."""
    text = line.strip()
    if text.startswith("|"):
        text = text[1:]
    if text.endswith("|") and not text.endswith("\\|"):
        text = text[:-1]
    return [cell.strip() for cell in CELL_SPLIT_PATTERN.split(text)]


def is_separator(line: str) -> bool:
    if "-" not in line or "|" not in line:
        return False
    return all(SEPARATOR_CELL_PATTERN.fullmatch(cell) for cell in split_row(line))


def visible_lines(markdown: str) -> list[tuple[int, str]]:
    """Return (line number, text) pairs with frontmatter and fenced code blocks blanked out."""
    lines = markdown.lstrip("﻿").splitlines()
    skip_until = 0
    if lines and lines[0].strip() == "---":
        for index in range(1, len(lines)):
            if lines[index].strip() in ("---", "..."):
                skip_until = index + 1
                break
    result: list[tuple[int, str]] = []
    fence: str | None = None
    for number, line in enumerate(lines, start=1):
        match = FENCE_PATTERN.match(line)
        if number <= skip_until:
            line = ""
        elif fence is None and match:
            fence, line = match.group(1), ""
        elif fence is not None:
            if match and match.group(1)[0] == fence[0] and len(match.group(1)) >= len(fence):
                fence = None
            line = ""
        elif line.startswith(("    ", "\t")):
            line = ""  # indented code block
        result.append((number, line))
    return result


def find_tables(markdown: str) -> tuple[list[Table], list[tuple[int, str]]]:
    """Return the tables found and (line, message) errors for pipe rows that do not form a table."""
    lines = visible_lines(markdown)
    tables: list[Table] = []
    errors: list[tuple[int, str]] = []
    index = 0
    while index < len(lines):
        number, line = lines[index]
        if "|" not in line:
            index += 1
            continue
        following = lines[index + 1][1] if index + 1 < len(lines) else ""
        if is_separator(following) and not is_separator(line):
            header, separator = split_row(line), split_row(following)
            table = Table(number, header, blank_line_before=index == 0 or not lines[index - 1][1].strip())
            if len(header) != len(separator):
                errors.append(
                    (number, f"header has {len(header)} column(s) but the separator row has {len(separator)}; "
                             "the table will not render")
                )
            index += 2
            while index < len(lines) and lines[index][1].strip() and "|" in lines[index][1]:
                table.rows.append((lines[index][0], split_row(lines[index][1])))
                index += 1
            tables.append(table)
            continue
        if line.lstrip().startswith("|"):
            errors.append((number, "row starts with '|' but is not part of a table; add a '| --- |' separator row "
                                   "under the header"))
            while index < len(lines) and lines[index][1].lstrip().startswith("|"):
                index += 1
            continue
        index += 1
    return tables, errors


def is_filler(cell: str) -> bool:
    return re.sub(r"[*_\x60]", "", cell).strip().lower() in FILLER_CELLS


def check(markdown: str, require_table: bool = False) -> tuple[list[str], list[str], int]:
    """Return (errors, warnings, table count) for one post."""
    tables, structural = find_tables(markdown)
    errors = [f"line {line}: {message}" for line, message in structural]
    warnings: list[str] = []

    if require_table and not tables:
        errors.append("no table found, and --require-table was given")

    for table in tables:
        columns = len(table.header)
        name = f"table at line {table.line}"
        if not table.blank_line_before:
            warnings.append(f"{name}: no blank line before the table; some renderers will show it as text")
        if columns > MAX_COLUMNS:
            warnings.append(f"{name}: {columns} columns; more than {MAX_COLUMNS} rarely fits a phone screen")
        for position, cell in enumerate(table.header, start=1):
            if not cell:
                errors.append(f"line {table.line}: header cell {position} is empty")
        if not table.rows:
            errors.append(f"{name}: no body rows")
        elif len(table.rows) < MIN_BODY_ROWS:
            warnings.append(f"{name}: only {len(table.rows)} body row; a one-row table is better as a sentence")

        placeholders = 0
        for line, cells in table.rows:
            if len(cells) != columns:
                errors.append(f"line {line}: row has {len(cells)} cell(s) but the header has {columns}")
            for position, cell in enumerate(cells[:columns], start=1):
                label = table.header[position - 1] or f"column {position}"
                if not cell:
                    errors.append(f"line {line}: empty cell under '{label}'")
                elif is_filler(cell):
                    errors.append(
                        f"line {line}: filler '{cell}' under '{label}'; give the value, or say "
                        "'Not disclosed', 'Not supported', or 'Not measured'"
                    )
                elif PLACEHOLDER in cell:
                    placeholders += 1
        if placeholders:
            warnings.append(f"{name}: {placeholders} cell(s) still hold an '{PLACEHOLDER}' placeholder")

    return errors, warnings, len(tables)


def main() -> int:
    parser = argparse.ArgumentParser(description="Check Markdown tables for structure and unpopulated cells.")
    parser.add_argument("posts", type=Path, nargs="+", help="Path(s) to Markdown post files")
    parser.add_argument("--require-table", action="store_true", help="Fail when a post contains no table")
    args = parser.parse_args()

    missing = [path for path in args.posts if not path.is_file()]
    if missing:
        for path in missing:
            print(f"FAIL: Markdown file not found: {path}", file=sys.stderr)
        return 2

    failed = 0
    for path in args.posts:
        errors, warnings, count = check(path.read_text(encoding="utf-8"), args.require_table)
        for message in errors:
            print(f"ERROR {path}: {message}")
        for message in warnings:
            print(f"WARN  {path}: {message}")
        if errors:
            failed += 1
            print(f"FAIL: {path} has {len(errors)} table error(s) across {count} table(s).")
        else:
            print(f"PASS: {path} has {count} table(s) with no errors.")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
