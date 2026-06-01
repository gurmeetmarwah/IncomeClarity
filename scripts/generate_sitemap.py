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


def load_redirects() -> tuple[dict[str, str], set[str]]:
    r301: dict[str, str] = {}
    r200: set[str] = set()
    for line in (ROOT / "_redirects").read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        parts = line.split()
        if len(parts) < 3:
            continue
        raw_src, raw_dst, code = parts[0], parts[1], parts[2].rstrip("!")
        src = norm(raw_src, keep_slash=raw_src.endswith("/"))
        dst = norm(raw_dst, keep_slash=raw_dst.endswith("/"))
        if code == "200":
            r200.add(src)
        elif code.startswith("301"):
            r301[src] = dst
            # Alias without trailing slash → same destination
            if src != "/" and not src.endswith("/"):
                r301[src + "/"] = dst
    return r301, r200


def terminal(path: str, r301: dict[str, str], r200: set[str]) -> str:
    seen: set[str] = set()
    while path in r301 and path not in seen:
        seen.add(path)
        path = r301[path]
    # Prefer explicit 200 rule path (e.g. state pages with trailing slash)
    if path in r200:
        return path
    if path != "/" and not path.endswith("/") and path + "/" in r200:
        return path + "/"
    return path


def collect_urls() -> list[str]:
    r301, r200 = load_redirects()
    urls: set[str] = set()

    for p in ROOT.rglob("*.html"):
        if ".git" in p.parts:
            continue
        rel = p.relative_to(ROOT).as_posix()
        if rel in ROOT_LEGACY or rel in SKIP_FILES:
            continue
        urls.add(terminal(html_to_canonical(rel), r301, r200))

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
