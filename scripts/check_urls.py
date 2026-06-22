#!/usr/bin/env python3
"""Verify internal URLs resolve on GitHub Pages-style static hosting."""
from __future__ import annotations

import argparse
import re
import subprocess
import sys
import xml.etree.ElementTree as ET
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parent.parent
SITE = "https://www.incomeclaritylab.com"

REDIRECT_STUB_MARKERS = ("Redirecting…", "location.replace", 'meta http-equiv="refresh"')
ASSET_EXTS = {
    ".css", ".js", ".png", ".jpg", ".jpeg", ".gif", ".webp", ".svg", ".ico",
    ".woff", ".woff2", ".ttf", ".json", ".xml", ".txt", ".pdf",
}


def norm(path: str, *, keep_slash: bool = False) -> str:
    path = path.strip()
    if not path.startswith("/"):
        path = "/" + path
    if not keep_slash and path != "/" and path.endswith("/"):
        path = path.rstrip("/")
    return path


def is_redirect_stub(path: Path) -> bool:
    if not path.is_file():
        return False
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return False
    return all(m in text for m in REDIRECT_STUB_MARKERS)


def file_for_path(path: str) -> Path | None:
    rel = path.lstrip("/")
    if not rel:
        cand = ROOT / "index.html"
        return cand if cand.is_file() else None

    direct = ROOT / rel
    if direct.is_file():
        return direct

    if path.endswith("/"):
        cand = ROOT / rel.rstrip("/") / "index.html"
        return cand if cand.is_file() else None

    html = ROOT / f"{rel}.html"
    index = ROOT / rel / "index.html"
    if html.is_file() and index.is_file() and is_redirect_stub(index):
        return html
    if html.is_file():
        return html
    if index.is_file():
        return index
    return None


def load_redirects() -> tuple[dict[str, str], dict[str, str]]:
    r301: dict[str, str] = {}
    r200: dict[str, str] = {}
    redirects_file = ROOT / "_redirects"
    if not redirects_file.is_file():
        return r301, r200
    for line in redirects_file.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        parts = line.split()
        if len(parts) < 3:
            continue
        raw_src, raw_dst, code = parts[0], parts[1], parts[2].rstrip("!")
        src = norm(raw_src, keep_slash=raw_src.endswith("/"))
        if code == "200":
            r200[src] = raw_dst
        elif code.startswith("301"):
            r301[src] = raw_dst
            if src != "/" and not src.endswith("/"):
                r301[src + "/"] = raw_dst
    return r301, r200


R301, R200 = load_redirects()


def resolve_url(path: str, *, _seen: set[str] | None = None) -> tuple[Path | None, list[str]]:
    if _seen is None:
        _seen = set()
    base, _, _frag = path.partition("#")
    base, _, _query = base.partition("?")
    keep_slash = base.endswith("/")
    clean = norm(base, keep_slash=keep_slash)
    chain: list[str] = []

    for _ in range(16):
        if clean in _seen:
            return None, chain + ["LOOP"]
        _seen.add(clean)

        hit = file_for_path(clean if clean.endswith("/") else clean)
        if hit:
            return hit, chain

        if clean in R200:
            chain.append(f"{clean} -> {R200[clean]} (200)")
            clean = norm(R200[clean], keep_slash=R200[clean].endswith("/"))
            continue

        alt = clean + "/" if not clean.endswith("/") else clean.rstrip("/")
        if alt in R200:
            chain.append(f"{clean} -> {R200[alt]} (200)")
            clean = norm(R200[alt], keep_slash=R200[alt].endswith("/"))
            continue

        if clean in R301:
            chain.append(f"{clean} -> {R301[clean]} (301)")
            clean = norm(R301[clean], keep_slash=R301[clean].endswith("/"))
            continue

        if alt in R301:
            chain.append(f"{clean} -> {R301[alt]} (301)")
            clean = norm(R301[alt], keep_slash=R301[alt].endswith("/"))
            continue

        return None, chain

    return None, chain + ["MAX_REDIRECTS"]


class LinkExtractor(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.links: set[str] = set()
        self._skip = 0

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        tag = tag.lower()
        if tag in {"script", "style", "head"}:
            self._skip += 1
            return
        attr = {k.lower(): (v or "") for k, v in attrs}
        if tag in {"a", "link"} and "href" in attr:
            self.links.add(attr["href"])
        elif tag == "form" and "action" in attr:
            self.links.add(attr["action"])

    def handle_endtag(self, tag: str) -> None:
        if tag.lower() in {"script", "style", "head"} and self._skip:
            self._skip -= 1


def normalize_href(href: str) -> str | None:
    if not href or href.startswith(("mailto:", "tel:", "javascript:", "data:", "#")):
        return None
    parsed = urlparse(href)
    if parsed.scheme in {"http", "https"}:
        if parsed.netloc and parsed.netloc not in {"www.incomeclaritylab.com", "incomeclaritylab.com"}:
            return None
        path = parsed.path or "/"
    elif href.startswith("/"):
        path = href
    else:
        return None
    base = path.split("#")[0].split("?")[0]
    return base or "/"


def load_sitemap_paths() -> set[str]:
    """Load all page paths from sitemap.xml (index or flat urlset)."""
    paths: set[str] = set()
    sitemap = ROOT / "sitemap.xml"
    if not sitemap.is_file():
        return paths

    root = ET.fromstring(sitemap.read_text(encoding="utf-8"))
    ns = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}
    tag = root.tag.rsplit("}", 1)[-1]

    if tag == "sitemapindex":
        for loc in root.findall(".//sm:loc", ns):
            if not loc.text:
                continue
            child_name = urlparse(loc.text).path.lstrip("/")
            child_path = ROOT / child_name
            if not child_path.is_file():
                continue
            child_root = ET.fromstring(child_path.read_text(encoding="utf-8"))
            for child_loc in child_root.findall(".//sm:loc", ns):
                if child_loc.text:
                    paths.add(urlparse(child_loc.text).path or "/")
    else:
        for loc in root.findall(".//sm:loc", ns):
            if loc.text:
                paths.add(urlparse(loc.text).path or "/")
    return paths


def collect_paths() -> dict[str, list[str]]:
    refs: dict[str, list[str]] = {}

    def add(path: str, source: str) -> None:
        norm_path = normalize_href(path)
        if not norm_path:
            return
        refs.setdefault(norm_path, []).append(source)

    for html_path in ROOT.rglob("*.html"):
        if "node_modules" in html_path.parts:
            continue
        rel = html_path.relative_to(ROOT).as_posix()
        parser = LinkExtractor()
        try:
            parser.feed(html_path.read_text(encoding="utf-8", errors="ignore"))
        except Exception:
            pass
        for href in parser.links:
            add(href, rel)

    for path in load_sitemap_paths():
        add(path, "sitemap.xml")

    redirects = ROOT / "_redirects"
    if redirects.is_file():
        for line in redirects.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            parts = line.split()
            if len(parts) >= 2:
                add(parts[0], "_redirects")
                add(parts[1], "_redirects")

    return refs


def check_production(paths: set[str]) -> list[tuple[str, str]]:
    broken: list[tuple[str, str]] = []
    for path in sorted(paths):
        url = SITE + path
        result = subprocess.run(
            ["curl", "-sI", "-o", "/dev/null", "-w", "%{http_code}", url],
            capture_output=True,
            text=True,
        )
        code = result.stdout.strip()
        if code not in {"200", "301", "302", "308"}:
            broken.append((code, path))
    return broken


def main() -> int:
    parser = argparse.ArgumentParser(description="Check internal URLs for 404s.")
    parser.add_argument(
        "--production",
        action="store_true",
        help="Also probe live site (requires network).",
    )
    args = parser.parse_args()

    refs = collect_paths()
    broken: list[tuple[str, list[str], list[str]]] = []
    ok = 0

    for path in sorted(refs):
        final, chain = resolve_url(path)
        if final:
            ok += 1
        else:
            broken.append((path, refs[path][:3], chain))

    print(f"Local: checked {len(refs)} URL(s): {ok} OK, {len(broken)} broken")
    if broken:
        print("\nLOCAL BROKEN URLS:")
        for path, sources, chain in broken:
            print(f"  {path}")
            print(f"    sources: {', '.join(sources[:5])}")
            if chain:
                print(f"    chain: {' | '.join(chain)}")
        print("\nRun: python3 scripts/generate_pages_redirect_stubs.py")
        return 1

    print("All internal URLs resolve locally.")

    if args.production:
        prod_broken = check_production(set(refs.keys()))
        print(f"\nProduction: {len(refs) - len(prod_broken)} OK, {len(prod_broken)} broken")
        if prod_broken:
            for code, path in prod_broken:
                print(f"  {code} {path}")
            return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
