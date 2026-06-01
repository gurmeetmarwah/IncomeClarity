#!/usr/bin/env python3
"""Local dev server with GitHub Pages-style URLs and _redirects support."""
from __future__ import annotations

import http.server
import os
import socketserver
from pathlib import Path
from urllib.parse import unquote, urlparse

ROOT = Path(__file__).resolve().parent.parent
PORT = int(os.environ.get("PORT", "8080"))

REDIRECT_STUB_MARKERS = ("Redirecting…", "location.replace", 'meta http-equiv="refresh"')


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


def is_redirect_stub(path: Path) -> bool:
    if not path.is_file():
        return False
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return False
    return all(m in text for m in REDIRECT_STUB_MARKERS)


def flat_html_path(rel: str) -> Path | None:
    """Path to {rel}.html at repo root or nested path."""
    cand = ROOT / f"{rel}.html"
    return cand if cand.is_file() else None


def resolve_static_file(path: str) -> str | None:
    """GitHub Pages-style path → file to serve (avoids directory redirect loops)."""
    rel = path.lstrip("/")
    if not rel:
        return "/index.html"

    if path.endswith("/"):
        dir_name = rel.rstrip("/")
        index = ROOT / dir_name / "index.html"
        html = flat_html_path(dir_name)
        if index.is_file() and is_redirect_stub(index) and html:
            return f"/{dir_name}.html"
        if index.is_file():
            return f"/{dir_name}/index.html"
        return None

    html = flat_html_path(rel)
    index_in_dir = ROOT / rel / "index.html"

    if html and index_in_dir.is_file() and is_redirect_stub(index_in_dir):
        return f"/{rel}.html"
    if html and not index_in_dir.is_file():
        return f"/{rel}.html"
    if html:
        return f"/{rel}.html"
    if index_in_dir.is_file():
        return f"/{rel}/index.html"
    return None


def apply_redirect_target(dst: str) -> str:
    """Prefer .html targets when a flat file exists (prevents /page ↔ /page/ loops)."""
    base, sep, frag = dst.partition("#")
    keep_slash = base.endswith("/")
    clean = norm(base, keep_slash=keep_slash)
    if not clean.endswith("/") and not clean.endswith(".html"):
        rel = clean.lstrip("/")
        if flat_html_path(rel):
            clean = f"/{rel}.html"
    return clean + (sep + frag if sep else "")


class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(ROOT), **kwargs)

    def do_GET(self) -> None:
        parsed = urlparse(self.path)
        raw_path = parsed.path or "/"
        path = norm(raw_path, keep_slash=raw_path.endswith("/"))
        query = parsed.query
        frag = parsed.fragment

        static = resolve_static_file(raw_path if raw_path.endswith("/") else path)
        if static:
            self.path = static
            if query:
                self.path += "?" + query
            return super().do_GET()

        if path in R200:
            self.path = "/" + R200[path].lstrip("/")
            if query:
                self.path += "?" + query
            return super().do_GET()

        if path != "/" and not path.endswith("/") and path + "/" in R200:
            self.path = "/" + R200[path + "/"].lstrip("/")
            if query:
                self.path += "?" + query
            return super().do_GET()

        if path in R301:
            dest = apply_redirect_target(R301[path])
            if query:
                dest += ("&" if "?" in dest else "?") + query
            if frag and "#" not in dest:
                dest += "#" + frag
            self.send_response(301)
            self.send_header("Location", dest)
            self.end_headers()
            return

        return super().do_GET()


class ReuseTCPServer(socketserver.TCPServer):
    allow_reuse_address = True


def main() -> None:
    with ReuseTCPServer(("", PORT), Handler) as httpd:
        print(f"Serving {ROOT} at http://127.0.0.1:{PORT}/")
        print("GitHub Pages-style URLs + _redirects (use this instead of python -m http.server)")
        httpd.serve_forever()


if __name__ == "__main__":
    main()
