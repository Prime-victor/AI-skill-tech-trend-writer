#!/usr/bin/env python3
"""Check every HTTP(S) URL in a Markdown article and report broken links by kind."""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from http.client import HTTPException
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import HTTPRedirectHandler, Request, build_opener

URL_PATTERN = re.compile(r"https?://[^\s<>\]\[\)]+")
USER_AGENT = "Mozilla/5.0 (compatible; tech-trend-writer-link-checker/2.0)"

OK = "OK"
REDIRECT = "REDIRECT"
CLIENT_ERROR = "4XX"
SERVER_ERROR = "5XX"
TIMEOUT = "TIMEOUT"
ERROR = "ERROR"
OTHER = "OTHER"
NOT_IN_SEARCH = "NOT-IN-SEARCH-RESULTS"

SUMMARY_LABELS = {
    CLIENT_ERROR: "4xx client error(s)",
    SERVER_ERROR: "5xx server error(s)",
    TIMEOUT: "timeout(s)",
    ERROR: "connection error(s)",
    OTHER: "other non-200 response(s)",
    NOT_IN_SEARCH: "URL(s) absent from search results",
}


@dataclass
class LinkResult:
    url: str
    category: str
    status: int | None = None
    method: str = ""
    final_url: str = ""
    redirects: int = 0
    detail: str = ""

    @property
    def ok(self) -> bool:
        return self.category in (OK, REDIRECT)


class RedirectRecorder(HTTPRedirectHandler):
    """Follow redirects as usual while recording each hop."""

    def __init__(self) -> None:
        self.hops: list[str] = []

    def redirect_request(self, req, fp, code, msg, headers, newurl):
        new_request = super().redirect_request(req, fp, code, msg, headers, newurl)
        if new_request is not None:
            self.hops.append(newurl)
            if req.get_method() == "HEAD":
                new_request.method = "HEAD"
        return new_request


def extract_urls(text: str) -> list[str]:
    """Return unique URLs in first-seen order, without trailing punctuation."""
    urls: list[str] = []
    for match in URL_PATTERN.findall(text):
        url = match.rstrip(".,;:!?")
        if url not in urls:
            urls.append(url)
    return urls


def classify_status(status: int) -> str:
    if 400 <= status < 500:
        return CLIENT_ERROR
    if 500 <= status < 600:
        return SERVER_ERROR
    return OTHER


def is_timeout(error: BaseException) -> bool:
    if isinstance(error, TimeoutError):
        return True
    return isinstance(error, URLError) and isinstance(error.reason, TimeoutError)


def check_url(url: str, timeout: float) -> LinkResult:
    """Try HEAD first, then GET when HEAD does not return 200."""
    result = LinkResult(url, ERROR, detail="No response")
    for method in ("HEAD", "GET"):
        recorder = RedirectRecorder()
        opener = build_opener(recorder)
        request = Request(url, method=method, headers={"User-Agent": USER_AGENT, "Accept": "*/*"})
        try:
            with opener.open(request, timeout=timeout) as response:
                status = response.status
                hops = len(recorder.hops)
                if status == 200:
                    category = REDIRECT if hops else OK
                    return LinkResult(url, category, status, method, response.geturl(), hops)
                result = LinkResult(url, classify_status(status), status, method, response.geturl(), hops)
        except HTTPError as error:
            result = LinkResult(
                url, classify_status(error.code), error.code, method, error.geturl() or url,
                len(recorder.hops), str(error.reason),
            )
            error.close()
        except (URLError, OSError, HTTPException, ValueError) as error:
            if is_timeout(error):
                # A server that hangs on HEAD will usually hang on GET too.
                return LinkResult(url, TIMEOUT, method=method, detail=f"no response within {timeout:g}s")
            reason = error.reason if isinstance(error, URLError) else error
            result = LinkResult(url, ERROR, method=method, detail=str(reason) or type(error).__name__)
    return result


def format_result(result: LinkResult) -> str:
    status = str(result.status) if result.status is not None else "-"
    line = f"{result.category:<8} {status:<3} {result.method:<4} {result.url}"
    if result.redirects:
        plural = "redirect" if result.redirects == 1 else "redirects"
        line += f" -> {result.final_url} ({result.redirects} {plural})"
    if result.detail:
        line += f" [{result.detail}]"
    return line


def main() -> int:
    parser = argparse.ArgumentParser(description="Check HTTP(S) links in a Markdown file.")
    parser.add_argument("article", type=Path, help="Path to the Markdown article")
    parser.add_argument("--timeout", type=float, default=10.0, help="Per-request timeout in seconds (default: 10)")
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

    results: list[LinkResult] = []
    for url in urls:
        if search_urls is not None and url not in search_urls:
            result = LinkResult(url, NOT_IN_SEARCH)
            print(f"{NOT_IN_SEARCH} {url}")
        else:
            result = check_url(url, args.timeout)
            print(format_result(result))
        results.append(result)

    redirected = sum(1 for result in results if result.category == REDIRECT)
    if redirected:
        print(f"NOTE: {redirected} link(s) redirect; consider citing the final URL.")

    broken = [result for result in results if not result.ok]
    if broken:
        counts = [
            f"{count} {label}"
            for category, label in SUMMARY_LABELS.items()
            if (count := sum(1 for result in broken if result.category == category))
        ]
        print(f"FAIL: {len(broken)} of {len(urls)} link(s) are broken: {', '.join(counts)}.")
        return 1
    print(f"PASS: All {len(urls)} link(s) returned HTTP 200.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
