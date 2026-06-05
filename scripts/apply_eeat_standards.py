#!/usr/bin/env python3
"""Apply sitewide E-E-A-T standards: review dates, footer links, meta updates."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

REVIEW_HTML = (
    '<p class="footer-review" role="note">'
    '<time datetime="2026-06-01">Last reviewed: June 2026</time>'
    ' · Reviewed by the <a href="/about">Income Clarity editorial team</a>'
    ' · <a href="/editorial-policy">Editorial policy</a>'
    "</p>\n      "
)

FOOTER_COMPANY_OLD = re.compile(
    r"<section class=\"footer-column\" aria-labelledby=\"footer-company\">.*?</section>",
    re.DOTALL,
)

FOOTER_COMPANY_NEW = """<section class="footer-column" aria-labelledby="footer-company">
          <h2 id="footer-company">Company</h2>
          <a href="/about">About</a>
          <a href="/editorial-policy">Editorial policy</a>
          <a href="/calculator-methodology">Calculator methodology</a>
          <a href="/methodology">Full methodology</a>
          <a href="/contact">Contact</a>
          <a href="/privacy-policy">Privacy Policy</a>
          <a href="/terms">Terms</a>
        </section>"""

LAST_REVIEWED_PATTERNS = [
    (re.compile(r"<time datetime=\"20\d{2}-\d{2}-\d{2}\">Last reviewed:[^<]*</time>"), '<time datetime="2026-06-01">Last reviewed: June 2026</time>'),
    (re.compile(r"Last reviewed:\s*(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2},?\s*20\d{2}", re.I), "Last reviewed: June 2026"),
    (re.compile(r"Last reviewed:\s*(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\.?\s+\d{1,2},?\s*20\d{2}", re.I), "Last reviewed: June 2026"),
]

EEAT_META_SUFFIX = ' · <a href="/editorial-policy">Editorial policy</a> · <a href="/calculator-methodology">Calculator methodology</a>'


def should_skip(path: Path) -> bool:
    if "node_modules" in path.parts:
        return True
    text = path.read_text(encoding="utf-8", errors="ignore")
    if "Redirecting" in text and len(text) < 800:
        return True
    if "site-footer" not in text:
        return True
    return False


def update_file(path: Path) -> bool:
    text = path.read_text(encoding="utf-8")
    original = text

    for pattern, repl in LAST_REVIEWED_PATTERNS:
        text = pattern.sub(repl, text)

    if FOOTER_COMPANY_OLD.search(text):
        text = FOOTER_COMPANY_OLD.sub(FOOTER_COMPANY_NEW, text, count=1)

    if "footer-review" not in text and "footer-copy" in text:
        text = text.replace(
            '<p class="footer-copy">© 2026 IncomeClarityLab</p>',
            REVIEW_HTML + '<p class="footer-copy">© 2026 IncomeClarityLab</p>',
            1,
        )

    if "eeat-trust__meta" in text and EEAT_META_SUFFIX not in text:
        text = re.sub(
            r'(<p class="eeat-trust__meta">.*?)(</p>)',
            lambda m: m.group(1) + EEAT_META_SUFFIX + m.group(2) if EEAT_META_SUFFIX not in m.group(1) else m.group(0),
            text,
            count=1,
        )

    if "methodology-meta" in text:
        text = re.sub(
            r'<p class="methodology-meta"><time datetime="20\d{2}-\d{2}-\d{2}">[^<]*</time>',
            '<p class="methodology-meta"><time datetime="2026-06-01">Last reviewed: June 2026</time>',
            text,
            count=1,
        )

    if text != original:
        path.write_text(text, encoding="utf-8")
        return True
    return False


def main() -> int:
    changed = 0
    for path in sorted(ROOT.rglob("*.html")):
        if should_skip(path):
            continue
        if update_file(path):
            changed += 1
            print(f"updated {path.relative_to(ROOT)}")
    print(f"Done. Updated {changed} files.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
