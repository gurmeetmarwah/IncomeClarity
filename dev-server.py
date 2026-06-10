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

    @staticmethod
    def _normalize_path(path):
        """Compare paths regardless of trailing slash."""
        p = path or "/"
        if p != "/":
            p = p.rstrip("/")
        return p

    def resolve(self, path):
        """Return (serve_relative_path | None, redirect_path | None, fragment)."""
        fragment = ""
        current = path
        for _ in range(32):
            if current in self.redirects:
                dest = self.redirects[current]
                if "#" in dest:
                    dest, fragment = dest.split("#", 1)
                if self._normalize_path(dest) != self._normalize_path(current):
                    return None, dest, fragment
                fragment = ""

            if current in self.rewrites:
                dest = self.rewrites[current]
                if "#" in dest:
                    dest, fragment = dest.split("#", 1)
                rel = dest.lstrip("/")
                return rel, None, fragment

            # Trailing-slash pretty URLs: serve index.html when present (before slash redirects)
            if current.endswith("/") and current != "/":
                index_rel = current.lstrip("/") + "index.html"
                if os.path.isfile(os.path.join(ROOT, index_rel)):
                    return index_rel, None, fragment

            alt = current.rstrip("/") if current.endswith("/") else current + "/"
            if alt != current and alt in self.redirects:
                dest = self.redirects[alt]
                dest_path = dest.split("#", 1)[0]
                if self._normalize_path(dest_path) != self._normalize_path(current):
                    current = alt
                    continue
            if alt != current and alt in self.rewrites:
                current = alt
                continue
            break

        return path.lstrip("/"), None, fragment


class NoCacheHandler(SimpleHTTPRequestHandler):
    _rules = None
    _rules_mtime = None

    @classmethod
    def get_rules(cls):
        """Reload _redirects when the file changes (dev server stays running across edits)."""
        redirects_path = os.path.join(ROOT, "_redirects")
        mtime = os.path.getmtime(redirects_path) if os.path.isfile(redirects_path) else 0
        if cls._rules is None or cls._rules_mtime != mtime:
            cls._rules = RedirectRules(redirects_path)
            cls._rules_mtime = mtime
        return cls._rules

    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=ROOT, **kwargs)

    def _resolve_serve_path(self, path):
        """Map request path to a file under ROOT (redirect rules + .html / index fallbacks)."""
        serve, redirect, fragment = self.get_rules().resolve(path)
        if redirect is not None:
            return serve, redirect, fragment

        rel = (serve or path.lstrip("/")).lstrip("/")
        if not rel:
            return serve, redirect, fragment

        candidates = [rel]
        if not rel.endswith(".html"):
            candidates.append(rel + ".html")
        if not rel.endswith("/index.html"):
            candidates.append(os.path.join(rel.rstrip("/"), "index.html"))

        for candidate in candidates:
            if os.path.isfile(os.path.join(ROOT, candidate)):
                return candidate, None, fragment

        return rel, None, fragment

    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path or "/"
        serve, redirect, fragment = self._resolve_serve_path(path)

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
    print(f"Debt page: http://localhost:{PORT}/debt#debt-hub-title")
    print(f"Interest hub: http://localhost:{PORT}/debt/interest-apr")
    print(f"Strategies hub: http://localhost:{PORT}/debt/payoff-strategies")
    print(f"Financial health hub: http://localhost:{PORT}/debt/financial-health")
    print(f"Credit cards hub: http://localhost:{PORT}/debt/credit-cards")
    print(f"Life decisions hub: http://localhost:{PORT}/debt/life-decisions")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopped.")
