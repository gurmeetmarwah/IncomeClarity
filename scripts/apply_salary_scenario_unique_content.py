#!/usr/bin/env python3
"""Inject city-specific unique sections into all salary scenario pages."""
from __future__ import annotations

import re
from pathlib import Path

from salary_scenario_unique_sections import (
    estimate_taxes,
    inject_unique_sections,
    lookup_city,
    patch_take_home_snippets,
    resolve_paths,
)

ROOT = Path(__file__).resolve().parent.parent
SCENARIO_ROOT = ROOT / "living" / "lifestyle" / "comfortable-salary"

TIER_SALARY = {
    "75k": 75_000,
    "80k": 80_000,
    "100k": 100_000,
    "150k": 150_000,
    "200k": 200_000,
}


def parse_scenario_path(path: Path) -> tuple[str, str, int, str] | None:
    rel = path.relative_to(SCENARIO_ROOT)
    parts = rel.parts
    if len(parts) < 3 or parts[-1] != "index.html":
        return None
    slug = parts[-2]
    m = re.match(r"is-(\d+k)-enough-to-live-in-(.+)", slug)
    if not m:
        return None
    tier = m.group(1)
    city_slug = m.group(2)
    if tier not in TIER_SALARY:
        return None
    state = parts[0]
    if state == "illinois" and city_slug == "chicago":
        pass
    elif len(parts) == 4:
        state = parts[0]
    else:
        return None
    return state, city_slug, TIER_SALARY[tier], slug


def apply_page(path: Path) -> bool:
    parsed = parse_scenario_path(path)
    if not parsed:
        return False
    state, city_slug, salary, _ = parsed
    city, _, _ = lookup_city(state, city_slug)
    html = path.read_text(encoding="utf-8")
    paths = resolve_paths(state, city_slug, city)
    tax = estimate_taxes(salary, paths["tax_state"], city_slug)
    html = inject_unique_sections(html, state=state, city_slug=city_slug, salary=salary)
    html = patch_take_home_snippets(html, tax, salary)
    path.write_text(html, encoding="utf-8")
    return True


def main() -> None:
    count = 0
    for path in sorted(SCENARIO_ROOT.glob("**/is-*-enough-to-live-in-*/index.html")):
        if apply_page(path):
            print(f"  updated {path.relative_to(ROOT)}")
            count += 1
    print(f"Done — {count} scenario pages updated.")


if __name__ == "__main__":
    main()
