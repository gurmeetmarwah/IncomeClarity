#!/usr/bin/env python3
"""Local dev server: no-cache headers + Netlify-style _redirects support."""
from http.server import HTTPServer, SimpleHTTPRequestHandler
from urllib.parse import urlparse
import os

PORT = int(os.environ.get("PORT", "8080"))
ROOT = os.path.dirname(os.path.abspath(__file__))


class RedirectRules:
    def __init__(self, redirects_path):
        self.redirects = {}
        self.rewrites = {}
        if os.path.isfile(redirects_path):
            self._load(redirects_path)

    def _load(self, path):
        with open(path, encoding="utf-8") as f:
            for raw in f:
                line = raw.strip()
                if not line or line.startswith("#"):
                    continue
                parts = line.split()
                if len(parts) < 3:
                    continue
                from_path, to_path, status = parts[0], parts[1], parts[2].rstrip("!")
                if status == "301":
                    self.redirects[from_path] = to_path
                elif status == "200":
                    self.rewrites[from_path] = to_path

    def resolve(self, path):
        """Return (serve_relative_path | None, redirect_path | None, fragment)."""
        fragment = ""
        current = path
        for _ in range(32):
            if current in self.redirects:
                dest = self.redirects[current]
                if "#" in dest:
                    dest, fragment = dest.split("#", 1)
                return None, dest, fragment

            if current in self.rewrites:
                dest = self.rewrites[current]
                if "#" in dest:
                    dest, fragment = dest.split("#", 1)
                rel = dest.lstrip("/")
                return rel, None, fragment

            alt = current.rstrip("/") if current.endswith("/") else current + "/"
            if alt != current and alt in self.redirects:
                current = alt
                continue
            if alt != current and alt in self.rewrites:
                current = alt
                continue
            break

        return path.lstrip("/"), None, fragment


class NoCacheHandler(SimpleHTTPRequestHandler):
    rules = RedirectRules(os.path.join(ROOT, "_redirects"))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=ROOT, **kwargs)

    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path or "/"
        serve, redirect, fragment = self.rules.resolve(path)

        if redirect is not None:
            loc = redirect
            if parsed.query:
                loc += "?" + parsed.query
            if fragment:
                loc += "#" + fragment
            self.send_response(301)
            self.send_header("Location", loc)
            self.end_headers()
            return

        if serve is not None and serve != path.lstrip("/"):
            self.path = "/" + serve
            if parsed.query:
                self.path += "?" + parsed.query

        return super().do_GET()

    def end_headers(self):
        self.send_header("Cache-Control", "no-store, no-cache, must-revalidate, max-age=0")
        self.send_header("Pragma", "no-cache")
        self.send_header("Expires", "0")
        super().end_headers()


if __name__ == "__main__":
    os.chdir(ROOT)
    server = HTTPServer(("", PORT), NoCacheHandler)
    print(f"Serving {ROOT} at http://localhost:{PORT}/ (no-cache + _redirects)")
    print(f"Debt page: http://localhost:{PORT}/credit-card-payoff-calculator#debt-hub-title")
    print(f"Interest hub: http://localhost:{PORT}/debt/interest-apr")
    print(f"Strategies hub: http://localhost:{PORT}/debt/payoff-strategies")
    print(f"Financial health hub: http://localhost:{PORT}/debt/financial-health")
    print(f"Hidden costs hub: http://localhost:{PORT}/debt/hidden-costs")
    print(f"Life decisions hub: http://localhost:{PORT}/debt/life-decisions")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopped.")
