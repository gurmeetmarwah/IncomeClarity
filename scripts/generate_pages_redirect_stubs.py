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

# Trailing-slash URLs for root *.html calculators.
# Must redirect to *.html (not extensionless) or local servers loop: /slug/ → /slug → /slug/.
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


def is_redirect_stub(path: Path) -> bool:
    if not path.is_file():
        return False
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return False
    return "location.replace" in text and 'meta http-equiv="refresh"' in text


def prefer_html_if_flat_file(path: str) -> str:
    """Prefer real content paths; use .html only for flat files (not redirect stubs)."""
    base, _, frag = path.partition("#")
    clean = base.rstrip("/")
    if not clean or clean.endswith(".html"):
        return path
    rel = clean.lstrip("/")
    dir_index = ROOT / rel / "index.html"
    html_file = ROOT / f"{rel}.html"

    if dir_index.is_file() and not is_redirect_stub(dir_index):
        out = f"/{rel}/"
        return f"{out}#{frag}" if frag else out
    if html_file.is_file() and not is_redirect_stub(html_file):
        out = f"/{rel}.html"
        return f"{out}#{frag}" if frag else out
    return path


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
        pass
    elif not base.endswith("/") and path_exists(f"{base}/index.html"):
        base += "/"
    url = base
    if frag:
        url = f"{url}#{frag}"
    url = prefer_html_if_flat_file(url)
    canonical = prefer_html_if_flat_file(url.split("#")[0])
    return url, canonical


def stub_path_for_src(src: str) -> Path:
    rel = src.lstrip("/")
    if rel.endswith(".html"):
        return ROOT / rel
    return ROOT / rel / "index.html"


def write_stub(src: str, dst: str, *, force: bool = False) -> bool:
    out = stub_path_for_src(src)
    if out.is_file() and not force:
        return False
    browser_url, canonical = target_url(dst)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(
        STUB.format(target=browser_url, canonical=canonical),
        encoding="utf-8",
    )
    return True


def refresh_trailing_slash_calculator_stubs() -> int:
    updated = 0
    for slug in TRAILING_SLASH_CALCULATORS:
        src = f"/{slug}/"
        dst = f"/{slug}.html"
        if write_stub(src, dst, force=True):
            updated += 1
            print(f"  ~ {stub_path_for_src(src).relative_to(ROOT)} → {dst}")
    return updated


def regenerate_existing_stubs() -> int:
    updated = 0
    for src, dst in load_redirect_rules():
        out = stub_path_for_src(src)
        if out.is_file() and is_redirect_stub(out):
            write_stub(src, dst, force=True)
            updated += 1
    return updated


def main() -> None:
    created = 0
    created += refresh_trailing_slash_calculator_stubs()
    updated = regenerate_existing_stubs()
    print(f"Refreshed {updated} existing stub(s).")

    for src, dst in load_redirect_rules():
        if path_exists(src):
            continue
        if write_stub(src, dst):
            created += 1
            print(f"  + {stub_path_for_src(src).relative_to(ROOT)}")

    print(f"Created {created} new redirect stub(s).")


if __name__ == "__main__":
    main()
