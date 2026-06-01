#!/usr/bin/env python3
"""Local dev server that applies _redirects (GitHub Pages does not)."""
from __future__ import annotations

import http.server
import socketserver
from pathlib import Path
from urllib.parse import unquote, urlparse

ROOT = Path(__file__).resolve().parent.parent
PORT = 8080


def norm(path: str, *, keep_slash: bool = False) -> str:
    path = unquote(path).strip()
    if not path.startswith("/"):
        path = "/" + path
    if not keep_slash and path != "/" and path.endswith("/"):
        path = path.rstrip("/")
    return path


def load_redirects() -> tuple[dict[str, str], dict[str, str]]:
    r301: dict[str, str] = {}
    r200: dict[str, str] = {}
    for line in (ROOT / "_redirects").read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        parts = line.split()
        if len(parts) < 3:
            continue
        raw_src, raw_dst, code = parts[0], parts[1], parts[2].rstrip("!")
        src = norm(raw_src, keep_slash=raw_src.endswith("/"))
        dst = raw_dst
        if code == "200":
            r200[src] = dst
        elif code.startswith("301"):
            r301[src] = dst
            if src != "/" and not src.endswith("/"):
                r301[src + "/"] = dst
    return r301, r200


R301, R200 = load_redirects()


class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(ROOT), **kwargs)

    def do_GET(self) -> None:
        parsed = urlparse(self.path)
        path = norm(parsed.path, keep_slash=parsed.path.endswith("/"))
        query = parsed.query
        frag = parsed.fragment

        if path in R301:
            dest = R301[path]
            if query:
                dest += ("&" if "?" in dest else "?") + query
            if frag:
                dest += "#" + frag
            self.send_response(301)
            self.send_header("Location", dest)
            self.end_headers()
            return

        if path in R200:
            self.path = R200[path]
            if query:
                self.path += "?" + query
            return super().do_GET()

        if path != "/" and not path.endswith("/") and path + "/" in R200:
            self.path = R200[path + "/"]
            if query:
                self.path += "?" + query
            return super().do_GET()

        return super().do_GET()


def main() -> None:
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print(f"Serving {ROOT} at http://127.0.0.1:{PORT}/ (_redirects enabled)")
        httpd.serve_forever()


if __name__ == "__main__":
    main()
