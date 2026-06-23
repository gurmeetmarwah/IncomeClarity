#!/usr/bin/env python3
"""Inject sitewide page-toc.js into all public HTML pages."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOC_SCRIPT = '  <script src="/page-toc.js" defer></script>\n'
SKIP_NAMES = {
    "index.html",
    "privacy-policy.html",
    "terms.html",
    "contact.html",
}
SKIP_PARTS = {"node_modules", ".git", "scripts"}


def should_skip(path: Path, text: str) -> bool:
    if path.name in SKIP_NAMES:
        return True
    if any(p in SKIP_PARTS for p in path.parts):
        return True
    if "site-footer" not in text and "<footer" not in text:
        return True
    if len(text) < 400:
        return True
    if "Redirecting" in text and len(text) < 900:
        return True
    if 'data-no-toc' in text:
        return True
    return False


def inject(text: str) -> str:
    text = text.replace('<script src="/ha-city-toc.js"></script>\n', "")
    text = text.replace('<script src="/ha-city-toc.js"></script>', "")
    text = text.replace('<script src="/ha-city-toc.js" defer></script>\n', "")
    text = text.replace('<script src="/ha-city-toc.js" defer></script>', "")
    if "page-toc.js" in text:
        return text
    if "</body>" not in text:
        return text
    return text.replace("</body>", TOC_SCRIPT + "</body>", 1)


def main() -> None:
    updated = 0
    skipped = 0
    for path in ROOT.rglob("*.html"):
        if should_skip(path, path.read_text(encoding="utf-8", errors="ignore")):
            skipped += 1
            continue
        text = path.read_text(encoding="utf-8")
        if should_skip(path, text):
            skipped += 1
            continue
        new_text = inject(text)
        if new_text != text:
            path.write_text(new_text, encoding="utf-8")
            updated += 1
    print(f"Injected page-toc.js into {updated} files ({skipped} skipped)")


if __name__ == "__main__":
    main()
