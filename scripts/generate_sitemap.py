#!/usr/bin/env python3
"""Regenerate sitemap index + section sitemaps from indexable HTML and _redirects."""
from __future__ import annotations

import xml.etree.ElementTree as ET
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BASE_URL = "https://www.incomeclaritylab.com"
SITEMAP_NS = "http://www.sitemaps.org/schemas/sitemap/0.9"

SITEMAP_FILES = {
    "core": "sitemap-core.xml",
    "debt": "sitemap-debt.xml",
    "housing": "sitemap-housing.xml",
    "programmatic": "sitemap-programmatic.xml",
}

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

SKIP_FILES = {
    "debt/life-decisions/hourly-to-salary-after-tax.html",
    "debt/life-decisions/rent-vs-buy-calculator.html",
}

EXCLUDE_PATHS = {"/404"}

DEBT_ROOT_PATHS = {
    "/average-credit-card-debt-by-income",
    "/how-credit-card-interest-works",
    "/how-much-credit-card-debt-is-normal",
    "/why-paying-minimum-is-bad",
}

HOUSING_PREFIXES = (
    "/living/housing",
    "/living/budgeting",
    "/living/can-i-afford-to-live-alone",
    "/living/lifestyle-family",
    "/living/cost-of-living",
    "/rent-vs-buy-calculator",
)

# Top-level paths that are legitimate sitemap entries (not legacy aliases).
CORE_ROOT_ALLOW = {
    "/",
    "/about",
    "/contact",
    "/terms",
    "/privacy-policy",
    "/editorial-policy",
    "/methodology",
    "/calculator-methodology",
    "/income",
    "/freelance",
    "/living",
    "/debt",
    "/hourly-to-salary-after-tax",
    "/1099-vs-w2-calculator",
    "/rent-vs-buy-calculator",
    "/what-is-take-home-pay",
    "/best-states-for-take-home-pay",
}


def norm(path: str, *, keep_slash: bool = False) -> str:
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
    if "#" not in path:
        return path
    base = path.split("#", 1)[0]
    return base if base else "/"


def normalize_content_path(path: str) -> str:
    """Identity of the HTML file that gets served."""
    path = strip_fragment(norm(path))
    if path.endswith("/index.html"):
        path = path[: -len("/index.html")]
    elif path.endswith(".html"):
        path = path[: -len(".html")]
    if path != "/" and path.endswith("/"):
        path = path.rstrip("/")
    return path or "/"


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
            if src != "/" and not src.endswith("/"):
                r301[src + "/"] = dst
    return r301, r200


def terminal(path: str, r301: dict[str, str]) -> str:
    path = strip_fragment(path)
    seen: set[str] = set()
    while path in r301 and path not in seen:
        seen.add(path)
        path = strip_fragment(r301[path])
    return path


def resolve_served_content(path: str, r301: dict[str, str], r200: dict[str, str]) -> str:
    """Map any public path to the underlying served HTML identity."""
    path = terminal(path, r301)
    if path in r200:
        return normalize_content_path(r200[path])
    if path != "/" and not path.endswith("/") and path + "/" in r200:
        return normalize_content_path(r200[path + "/"])
    return normalize_content_path(path)


def rewrite_sources_for_content(content: str, r200: dict[str, str]) -> list[str]:
    sources: list[str] = []
    for src, dst in r200.items():
        if normalize_content_path(dst) == content:
            sources.append(norm(src.rstrip("/") if src != "/" else src))
    return sources


def url_rank(path: str) -> tuple:
    """Lower is better. Prefer primary paths over legacy rewrite aliases."""
    score = 0
    if path.endswith("/") and path != "/":
        score += 2
    if path.count("/") <= 1 and path not in CORE_ROOT_ALLOW:
        score += 60
    if path.startswith("/living/family-budgeting/"):
        score += 70
    if path.startswith("/living/lifestyle-family/"):
        score += 20
    if path.startswith("/living/lifestyle-family/comfortable-salary-"):
        score += 80
    if path.endswith(".html"):
        score += 100
    return (score, len(path), path)


def is_indexable_public_url(path: str, r301: dict[str, str]) -> bool:
    """Skip URLs that 301 to a different canonical path."""
    path = norm(path)
    return terminal(path, r301) == path


def pick_canonical_url(candidates: set[str], r301: dict[str, str], r200: dict[str, str]) -> str:
    if not candidates:
        raise ValueError("empty candidate set")
    if len(candidates) == 1:
        only = next(iter(candidates))
        return terminal(only, r301) if not is_indexable_public_url(only, r301) else only

    content = resolve_served_content(next(iter(candidates)), r301, r200)
    sources = rewrite_sources_for_content(content, r200)
    pool = set(sources) | candidates

    pool = {u for u in pool if resolve_served_content(u, r301, r200) == content}
    pool = {u for u in pool if is_indexable_public_url(u, r301)}
    if not pool:
        pool = {u for u in candidates if is_indexable_public_url(u, r301)}
    if not pool:
        return min(candidates, key=url_rank)

    return min(pool, key=url_rank)


def collect_urls() -> list[str]:
    r301, r200 = load_redirects()
    by_content: dict[str, set[str]] = defaultdict(set)

    for p in ROOT.rglob("*.html"):
        if ".git" in p.parts:
            continue
        rel = p.relative_to(ROOT).as_posix()
        if rel in ROOT_LEGACY or rel in SKIP_FILES:
            continue
        candidate = html_to_canonical(rel)
        content = resolve_served_content(candidate, r301, r200)
        by_content[content].add(candidate)

    urls: set[str] = set()
    for content, candidates in by_content.items():
        urls.add(pick_canonical_url(candidates, r301, r200))

    urls = dedupe_urls(urls)
    urls -= EXCLUDE_PATHS
    return sorted(urls, key=sort_key)


def dedupe_urls(urls: set[str]) -> set[str]:
    result = set(urls)
    for path in list(result):
        if path.endswith(".html"):
            bare = path[: -len(".html")]
            if bare in result:
                result.discard(path)
    return result


def classify_served_path(served: str) -> str:
    p = served.rstrip("/") or "/"
    if p in EXCLUDE_PATHS:
        return "exclude"
    if "/comfortable-salary" in p or p == "/living/lifestyle/comfortable-salary-us":
        return "programmatic"
    if p.startswith("/debt") or p in DEBT_ROOT_PATHS:
        return "debt"
    if (
        p.startswith(HOUSING_PREFIXES)
        or "cost-of-living-by-city" in p
        or "moving-cost-calculator" in p
        or "how-much-house-can-i-afford" in p
        or "how-much-rent-can-i-afford" in p
    ):
        return "housing"
    return "core"


def classify_url(path: str, r301: dict[str, str], r200: dict[str, str]) -> str:
    served = resolve_served_content(path, r301, r200)
    return classify_served_path(served)


def sort_key(path: str) -> tuple:
    depth = path.count("/")
    return (0 if path == "/" else 1, depth, path)


def write_urlset(urls: list[str], out: Path) -> None:
    urlset = ET.Element("urlset", xmlns=SITEMAP_NS)
    for path in urls:
        url_el = ET.SubElement(urlset, "url")
        loc = ET.SubElement(url_el, "loc")
        loc.text = BASE_URL + path if path != "/" else BASE_URL + "/"

    tree = ET.ElementTree(urlset)
    ET.indent(tree, space="  ")
    out.write_text('<?xml version="1.0" encoding="UTF-8"?>\n', encoding="utf-8")
    tree.write(out, encoding="unicode", xml_declaration=False)


def write_sitemap_index(children: list[str], out: Path) -> None:
    index = ET.Element("sitemapindex", xmlns=SITEMAP_NS)
    for name in children:
        entry = ET.SubElement(index, "sitemap")
        loc = ET.SubElement(entry, "loc")
        loc.text = f"{BASE_URL}/{name}"

    tree = ET.ElementTree(index)
    ET.indent(tree, space="  ")
    out.write_text('<?xml version="1.0" encoding="UTF-8"?>\n', encoding="utf-8")
    tree.write(out, encoding="unicode", xml_declaration=False)


def partition_urls(urls: list[str], r301: dict[str, str], r200: dict[str, str]) -> dict[str, list[str]]:
    buckets: dict[str, list[str]] = {key: [] for key in SITEMAP_FILES}
    for path in urls:
        bucket = classify_url(path, r301, r200)
        if bucket == "exclude":
            continue
        buckets[bucket].append(path)
    for key in buckets:
        buckets[key].sort(key=sort_key)
    return buckets


def main() -> None:
    r301, r200 = load_redirects()
    urls = collect_urls()
    buckets = partition_urls(urls, r301, r200)

    written: list[str] = []
    total = 0
    for key, filename in SITEMAP_FILES.items():
        section_urls = buckets[key]
        if not section_urls:
            continue
        out = ROOT / filename
        write_urlset(section_urls, out)
        written.append(filename)
        total += len(section_urls)
        print(f"  {filename}: {len(section_urls)} URLs")

    write_sitemap_index(written, ROOT / "sitemap.xml")
    print(f"Wrote sitemap index with {len(written)} sections ({total} URLs total)")


if __name__ == "__main__":
    main()
