#!/usr/bin/env python3
"""Check every HTTP(S) URL in a Markdown article for a successful response."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

URL_PATTERN = re.compile(r"https?://[^\s<>\]\[\)]+")
USER_AGENT = "tech-trend-writer-link-checker/1.0"


def extract_urls(text: str) -> list[str]:
    """Return unique URLs in first-seen order, without trailing punctuation."""
    urls: list[str] = []
    for match in URL_PATTERN.findall(text):
        url = match.rstrip(".,;:!?")
        if url not in urls:
            urls.append(url)
    return urls


def request_status(url: str, timeout: float) -> tuple[bool, int | None, str]:
    """Try HEAD, then GET when a server rejects or mishandles HEAD."""
    for method in ("HEAD", "GET"):
        request = Request(url, method=method, headers={"User-Agent": USER_AGENT})
        try:
            with urlopen(request, timeout=timeout) as response:
                status = response.getcode()
                if status == 200:
                    return True, status, method
                if method == "HEAD":
                    continue
                return False, status, method
        except HTTPError as error:
            if method == "HEAD" and error.code in {403, 405, 501}:
                continue
            return False, error.code, method
        except (URLError, TimeoutError, OSError) as error:
            detail = error.reason if isinstance(error, URLError) else str(error)
            return False, None, f"{method}: {detail}"
    return False, None, "No response"


def main() -> int:
    parser = argparse.ArgumentParser(description="Check HTTP(S) links in a Markdown file.")
    parser.add_argument("article", type=Path, help="Path to the Markdown article")
    parser.add_argument("--timeout", type=float, default=10.0, help="Per-request timeout in seconds")
    parser.add_argument(
        "--search-results",
        type=Path,
        help="Optional text or Markdown export of search results; fail URLs absent from it",
    )
    args = parser.parse_args()

    if not args.article.is_file():
        print(f"FAIL: Markdown file not found: {args.article}", file=sys.stderr)
        return 2
    if args.timeout <= 0:
        print("FAIL: --timeout must be positive", file=sys.stderr)
        return 2

    urls = extract_urls(args.article.read_text(encoding="utf-8"))
    if not urls:
        print("PASS: No HTTP(S) URLs found; nothing to check.")
        return 0

    search_urls: set[str] | None = None
    if args.search_results:
        if not args.search_results.is_file():
            print(f"FAIL: Search-results file not found: {args.search_results}", file=sys.stderr)
            return 2
        search_urls = set(extract_urls(args.search_results.read_text(encoding="utf-8")))

    failures = 0
    for url in urls:
        if search_urls is not None and url not in search_urls:
            failures += 1
            print(f"FAIL not-in-search-results {url}")
            continue
        ok, status, detail = request_status(url, args.timeout)
        if ok:
            print(f"OK   {status} ({detail}) {url}")
        else:
            failures += 1
            label = str(status) if status is not None else "unreachable"
            print(f"FAIL {label} ({detail}) {url}")

    if failures:
        print(f"FAIL: {failures} of {len(urls)} link(s) are broken or unreachable.")
        return 1
    print(f"PASS: All {len(urls)} link(s) returned HTTP 200.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
