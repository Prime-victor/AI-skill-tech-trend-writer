"""Exercise link_checker against a throwaway server on localhost; no external network."""

import contextlib
import io
import sys
import tempfile
import threading
import time
import unittest
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))

import link_checker as lc  # noqa: E402


class Handler(BaseHTTPRequestHandler):
    seen_user_agents: list = []

    def log_message(self, *args):
        pass

    def respond(self, status, location=None):
        self.send_response(status)
        if location:
            self.send_header("Location", location)
        self.send_header("Content-Length", "0")
        self.end_headers()

    def route(self):
        Handler.seen_user_agents.append(self.headers.get("User-Agent"))
        path = self.path
        if path == "/ok":
            self.respond(200)
        elif path == "/hop1":
            self.respond(301, "/hop2")
        elif path == "/hop2":
            self.respond(302, "/ok")
        elif path == "/to-missing":
            self.respond(301, "/missing")
        elif path == "/loop":
            self.respond(302, "/loop")
        elif path == "/get-only":
            self.respond(405 if self.command == "HEAD" else 200)
        elif path == "/head-404-get-ok":
            self.respond(404 if self.command == "HEAD" else 200)
        elif path == "/error":
            self.respond(503)
        elif path == "/no-content":
            self.respond(204)
        elif path == "/drop":
            self.close_connection = True
        elif path == "/slow":
            time.sleep(1.5)
            self.respond(200)
        else:
            self.respond(404)

    do_HEAD = route
    do_GET = route


class LinkCheckerTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
        cls.server.daemon_threads = True
        cls.base = f"http://127.0.0.1:{cls.server.server_address[1]}"
        threading.Thread(target=cls.server.serve_forever, daemon=True).start()

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.server.server_close()

    def check(self, path, timeout=5.0):
        return lc.check_url(self.base + path, timeout)

    def run_main(self, text, *options):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "article.md"
            path.write_text(text, encoding="utf-8")
            argv, sys.argv = sys.argv, ["link_checker.py", str(path), *options]
            try:
                with contextlib.redirect_stdout(io.StringIO()) as output:
                    return lc.main(), output.getvalue()
            finally:
                sys.argv = argv

    def test_ok(self):
        result = self.check("/ok")
        self.assertEqual((result.category, result.status, result.method, result.redirects), (lc.OK, 200, "HEAD", 0))
        self.assertTrue(result.ok)

    def test_user_agent_is_sent(self):
        self.check("/ok")
        self.assertIn(lc.USER_AGENT, Handler.seen_user_agents)

    def test_redirect_chain_reports_final_url_and_length(self):
        result = self.check("/hop1")
        self.assertEqual((result.category, result.status, result.redirects), (lc.REDIRECT, 200, 2))
        self.assertEqual(result.final_url, self.base + "/ok")
        self.assertTrue(result.ok)
        self.assertIn("(2 redirects)", lc.format_result(result))

    def test_redirect_to_missing_page_is_broken(self):
        result = self.check("/to-missing")
        self.assertEqual((result.category, result.status, result.redirects), (lc.CLIENT_ERROR, 404, 1))
        self.assertEqual(result.final_url, self.base + "/missing")

    def test_redirect_loop_is_broken(self):
        self.assertFalse(self.check("/loop").ok)

    def test_404(self):
        result = self.check("/missing")
        self.assertEqual((result.category, result.status, result.method), (lc.CLIENT_ERROR, 404, "GET"))

    def test_5xx(self):
        result = self.check("/error")
        self.assertEqual((result.category, result.status), (lc.SERVER_ERROR, 503))

    def test_head_rejected_falls_back_to_get(self):
        for path in ("/get-only", "/head-404-get-ok"):
            with self.subTest(path=path):
                result = self.check(path)
                self.assertEqual((result.category, result.status, result.method), (lc.OK, 200, "GET"))

    def test_non_200_success_is_reported_as_other(self):
        result = self.check("/no-content")
        self.assertEqual((result.category, result.status), (lc.OTHER, 204))
        self.assertFalse(result.ok)

    def test_timeout(self):
        result = self.check("/slow", timeout=0.3)
        self.assertEqual(result.category, lc.TIMEOUT)
        self.assertIsNone(result.status)

    def test_connection_error(self):
        result = self.check("/drop")
        self.assertEqual(result.category, lc.ERROR)
        self.assertTrue(result.detail)

    def test_main_passes_when_all_links_work(self):
        code, output = self.run_main(f"[a]({self.base}/ok) and [b]({self.base}/hop1).")
        self.assertEqual(code, 0)
        self.assertIn("PASS: All 2 link(s)", output)
        self.assertIn("NOTE: 1 link(s) redirect", output)

    def test_main_exits_non_zero_and_separates_kinds(self):
        text = f"{self.base}/ok {self.base}/missing {self.base}/error {self.base}/slow"
        code, output = self.run_main(text, "--timeout", "0.3")
        self.assertEqual(code, 1)
        self.assertIn("3 of 4 link(s) are broken", output)
        for fragment in ("1 4xx client error(s)", "1 5xx server error(s)", "1 timeout(s)"):
            self.assertIn(fragment, output)

    def test_main_flags_urls_missing_from_search_results(self):
        with tempfile.TemporaryDirectory() as folder:
            results = Path(folder) / "results.md"
            results.write_text(f"{self.base}/ok\n", encoding="utf-8")
            code, output = self.run_main(
                f"{self.base}/ok {self.base}/hop1", "--search-results", str(results)
            )
        self.assertEqual(code, 1)
        self.assertIn("1 URL(s) absent from search results", output)

    def test_main_without_links(self):
        self.assertEqual(self.run_main("No links here.")[0], 0)


class ExtractTests(unittest.TestCase):
    def test_extract_urls(self):
        text = "See [docs](https://example.com/a), https://example.com/b. And https://example.com/a again."
        self.assertEqual(lc.extract_urls(text), ["https://example.com/a", "https://example.com/b"])


if __name__ == "__main__":
    unittest.main()
