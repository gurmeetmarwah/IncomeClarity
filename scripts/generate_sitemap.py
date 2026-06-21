#!/usr/bin/env python3
"""Regenerate sitemap.xml from indexable HTML pages and _redirects rules."""
from __future__ import annotations

import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BASE_URL = "https://www.incomeclaritylab.com"

# Root HTML files that 301 to another canonical path (duplicate content)
ROOT_LEGACY = {
    "average-monthly-expenses.html",
    "50-30-20-budget-rule.html",
    "can-i-afford-to-live-alone.html",
    "cost-of-living-california-vs-texas.html",
    "nyc-vs-austin-cost-of-living.html",
    "seattle-vs-denver-cost-of-living.html",
    "how-much-rent-can-i-afford.html",
    "how-much-house-can-i-afford.html",
    "how-much-house-can-i-afford-in-california.html",
    "rent-vs-buy-california.html",
    "when-buying-is-better-than-renting.html",
    "best-way-to-pay-off-credit-card-debt.html",
    "average-credit-card-debt-by-income.html",
    "how-much-credit-card-debt-is-normal.html",
    "how-credit-card-interest-works.html",
    "what-is-credit-card-apr.html",
    "why-paying-minimum-is-bad.html",
    "salary-needed-to-live-comfortably.html",
}

# Redirect-only stubs (real content lives at another URL)
SKIP_FILES = {
    "debt/life-decisions/hourly-to-salary-after-tax.html",
    "debt/life-decisions/rent-vs-buy-calculator.html",
}


def norm(path: str, *, keep_slash: bool = False) -> str:
    """Normalize path; keep_slash preserves trailing slash when set in _redirects."""
    path = path.strip()
    if not path.startswith("/"):
        path = "/" + path
    if not keep_slash and path != "/" and path.endswith("/"):
        path = path.rstrip("/")
    return path


def html_to_canonical(rel: str) -> str:
    if rel == "index.html":
        return "/"
    if rel.endswith("/index.html"):
        return norm("/" + rel[: -len("/index.html")])
    if rel.endswith(".html"):
        return norm("/" + rel[: -len(".html")])
    return norm("/" + rel)


def strip_fragment(path: str) -> str:
    """Sitemap loc values must not include URL fragments."""
    if "#" not in path:
        return path
    base = path.split("#", 1)[0]
    return base if base else "/"


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
        src = strip_fragment(norm(raw_src, keep_slash=raw_src.endswith("/")))
        dst = strip_fragment(norm(raw_dst, keep_slash=raw_dst.endswith("/")))
        if code == "200":
            r200[src] = dst
        elif code.startswith("301"):
            r301[src] = dst
            # Alias without trailing slash → same destination
            if src != "/" and not src.endswith("/"):
                r301[src + "/"] = dst
    return r301, r200


def terminal(path: str, r301: dict[str, str]) -> str:
    """Follow 301 chains; never emit fragment URLs."""
    path = strip_fragment(path)
    seen: set[str] = set()
    while path in r301 and path not in seen:
        seen.add(path)
        path = strip_fragment(r301[path])
    return path


def canonical_sitemap_url(path: str, r301: dict[str, str], r200: dict[str, str]) -> str:
    """One canonical path per page for sitemap.xml."""
    path = terminal(path, r301)

    # Pretty URL (200 source) wins over the static file it rewrites to.
    dest_to_src = {strip_fragment(dst): src for src, dst in r200.items()}
    if path in dest_to_src:
        return dest_to_src[path]

    if path in r200:
        return path

    # Trailing-slash variant of a known 200 source (e.g. state hub pages).
    if path != "/" and path.endswith("/") and path[:-1] in r200:
        return path[:-1]

    return path


def dedupe_urls(urls: set[str]) -> set[str]:
    """Drop .html duplicates when the extensionless URL is already listed."""
    result = set(urls)
    for path in list(result):
        if path.endswith(".html"):
            bare = path[: -len(".html")]
            if bare in result:
                result.discard(path)
    return result


def collect_urls() -> list[str]:
    r301, r200 = load_redirects()
    urls: set[str] = set()

    for p in ROOT.rglob("*.html"):
        if ".git" in p.parts:
            continue
        rel = p.relative_to(ROOT).as_posix()
        if rel in ROOT_LEGACY or rel in SKIP_FILES:
            continue
        urls.add(canonical_sitemap_url(html_to_canonical(rel), r301, r200))

    urls = dedupe_urls(urls)
    return sorted(urls, key=sort_key)


def sort_key(path: str) -> tuple:
    """Home first, then shallow paths, then alphabetical."""
    depth = path.count("/")
    return (0 if path == "/" else 1, depth, path)


def write_sitemap(urls: list[str], out: Path) -> None:
    urlset = ET.Element("urlset", xmlns="http://www.sitemaps.org/schemas/sitemap/0.9")
    for path in urls:
        url_el = ET.SubElement(urlset, "url")
        loc = ET.SubElement(url_el, "loc")
        loc.text = BASE_URL + path if path != "/" else BASE_URL + "/"

    tree = ET.ElementTree(urlset)
    ET.indent(tree, space="  ")
    out.write_text('<?xml version="1.0" encoding="UTF-8"?>\n', encoding="utf-8")
    tree.write(out, encoding="unicode", xml_declaration=False)


def main() -> None:
    urls = collect_urls()
    out = ROOT / "sitemap.xml"
    write_sitemap(urls, out)
    print(f"Wrote {len(urls)} URLs to {out}")


if __name__ == "__main__":
    main()
