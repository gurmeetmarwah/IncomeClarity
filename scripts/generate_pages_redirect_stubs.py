#!/usr/bin/env python3
"""Create redirect stub HTML for GitHub Pages (_redirects is not applied there).

Generates index.html / .html stubs for 301 sources in _redirects when no file exists yet.
"""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REDIRECTS = ROOT / "_redirects"

STUB = '''<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="robots" content="noindex,follow">
  <link rel="canonical" href="{canonical}">
  <meta http-equiv="refresh" content="0;url={target}">
  <script>location.replace("{target}" + location.search + location.hash);</script>
  <title>Redirecting…</title>
</head>
<body>
  <p>Redirecting to <a href="{target}">{target}</a>.</p>
</body>
</html>
'''

# Trailing-slash URLs for root *.html calculators (GitHub Pages serves /page from page.html, not /page/).
TRAILING_SLASH_CALCULATORS = (
    "rent-vs-buy-calculator",
    "credit-card-payoff-calculator",
    "1099-vs-w2-calculator",
    "hourly-to-salary-after-tax",
)


def norm(path: str, *, keep_slash: bool = False) -> str:
    path = path.strip()
    if not path.startswith("/"):
        path = "/" + path
    if not keep_slash and path != "/" and path.endswith("/"):
        path = path.rstrip("/")
    return path


def path_exists(web_path: str) -> bool:
    p = web_path.lstrip("/")
    if not p:
        return (ROOT / "index.html").is_file()
    if (ROOT / p).is_file():
        return True
    if (ROOT / p / "index.html").is_file():
        return True
    if not p.endswith(".html") and (ROOT / f"{p}.html").is_file():
        return True
    return False


def load_redirect_rules() -> list[tuple[str, str]]:
    """301 and 200 rules from _redirects (Netlify-style; stubs backfill GitHub Pages)."""
    rules: list[tuple[str, str]] = []
    for line in REDIRECTS.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        parts = line.split()
        if len(parts) < 3:
            continue
        raw_src, raw_dst, code = parts[0], parts[1], parts[2].rstrip("!")
        if not (code.startswith("301") or code == "200"):
            continue
        src = norm(raw_src, keep_slash=raw_src.endswith("/"))
        rules.append((src, raw_dst))
    return rules


def target_url(dst: str) -> tuple[str, str]:
    """Return (browser_url, canonical_url) without hash; hash appended by stub JS."""
    base, _, frag = dst.partition("#")
    keep_slash = base.endswith("/")
    base = norm(base, keep_slash=keep_slash)
    if base.endswith("/index.html"):
        base = base[: -len("index.html")]
        if not base.endswith("/"):
            base += "/"
    elif base.endswith(".html"):
        base = base[: -len(".html")]
    elif not base.endswith("/") and path_exists(f"{base}/index.html"):
        base += "/"
    url = base
    if frag:
        url = f"{url}#{frag}"
    canonical = url.split("#")[0]
    return url, canonical


def stub_path_for_src(src: str) -> Path:
    rel = src.lstrip("/")
    if rel.endswith(".html"):
        return ROOT / rel
    return ROOT / rel / "index.html"


def write_stub(src: str, dst: str) -> bool:
    out = stub_path_for_src(src)
    if out.is_file():
        return False
    browser_url, canonical = target_url(dst)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(
        STUB.format(target=browser_url, canonical=canonical),
        encoding="utf-8",
    )
    return True


def main() -> None:
    created = 0
    for slug in TRAILING_SLASH_CALCULATORS:
        src = f"/{slug}/"
        dst = f"/{slug}"
        if not path_exists(src) and write_stub(src, dst):
            created += 1
            print(f"  + {stub_path_for_src(src).relative_to(ROOT)}")

    for src, dst in load_redirect_rules():
        if path_exists(src):
            continue
        if write_stub(src, dst):
            created += 1
            print(f"  + {stub_path_for_src(src).relative_to(ROOT)}")

    print(f"Created {created} redirect stub(s).")


if __name__ == "__main__":
    main()
