#!/usr/bin/env python3
"""Apply CTR-focused titles, meta descriptions, and H1s across HTML pages.

Rewrites dry calculator-style headlines into curiosity-driven search snippets.
"""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BRAND = " | Income Clarity"
REDIRECT_MARK = "Redirecting"

# Exact page overrides (path relative to ROOT, posix)
MANUAL: dict[str, dict[str, str]] = {
    "living/lifestyle/comfortable-salary-us/index.html": {
        "title": f"Here's the Salary You Need to Feel Comfortable in Every State (2026){BRAND}",
        "desc": "Curious what comfortable actually means where you live? See salary targets by state and city — rent, taxes, and lifestyle built in.",
        "h1": "Here's the salary you need to feel comfortable in every state",
    },
    "rent-vs-buy-calculator.html": {
        "title": f"Rent or Buy: Which Costs You Less Over 5 Years? Free Calculator (2026){BRAND}",
        "desc": "Stuck on rent vs buy? See the real monthly cost, break-even year, and what stays in your pocket — taxes, maintenance, and equity included.",
    },
    "hourly-to-salary-after-tax.html": {
        "title": f"What Does Your Hourly Wage Really Earn You After Tax in 2026?{BRAND}",
        "desc": "That $25/hr headline rate isn't what hits your bank account. Convert any hourly wage to real 2026 take-home pay — federal tax, FICA, and state tax included.",
    },
    "living/housing/cost-of-living-by-city/index.html": {
        "title": f"Which US City Is Cheapest to Live In? Compare Rent, Taxes & Salary (2026){BRAND}",
        "desc": "Thinking about a move? Compare rent, groceries, taxes, and the salary you'd need in 40+ US cities — before you sign a lease or accept an offer.",
        "h1": "Which US city is cheapest to live in?",
    },
    "living/housing/moving-cost-calculator/index.html": {
        "title": f"How Much Does Moving Really Cost? Free Relocation Calculator (2026){BRAND}",
        "desc": "Surprised by a move's price tag? Estimate movers, deposits, utilities, and how your monthly budget changes before you pack a box.",
        "h1": "How much does moving really cost?",
    },
    "living/housing/how-much-house-can-i-afford.html": {
        "title": f"Can You Afford That Home? See What Your Income Really Buys (2026){BRAND}",
        "desc": "Lenders approve more than you can comfortably carry. Run the 28% rule on your real income and see what home price actually fits your budget.",
    },
    "debt/interest-apr/daily-interest-calculator/index.html": {
        "title": f"How Much Interest Are You Paying Every Single Day? Free Calculator (2026){BRAND}",
        "desc": "Your APR hides a daily leak. See exactly how much interest accrues each day on credit cards, loans, or savings — from principal and rate in seconds.",
        "h1": "How much interest are you paying every single day?",
    },
    "debt/debt-strategies/pay-off-debt-faster/index.html": {
        "title": f"What If You Paid $100 More a Month? See How Fast Debt Disappears (2026){BRAND}",
        "desc": "Small extra payments crush interest faster than you'd guess. Model snowball vs avalanche and see months shaved off your payoff timeline.",
    },
    "debt/financial-health/can-i-afford-my-debt/index.html": {
        "title": f"Is Your Debt Eating Your Paycheck? Free Affordability Check (2026){BRAND}",
        "desc": "Payments feel fine until something breaks. Get a debt health score, monthly breathing room, and a clear plan based on your real income.",
        "og_title": "Is Your Debt Eating Your Paycheck? Free Affordability Check (2026)",
        "twitter_title": "Is Your Debt Eating Your Paycheck?",
    },
    "living/lifestyle-family/comfortable-salary-california/index.html": {
        "title": f"Here's the Salary You Need to Feel Comfortable in California (2026){BRAND}",
        "desc": "California paychecks shrink fast after state tax and rent. See what singles, couples, and families need to earn for a comfortable life — by city.",
        "h1": "Here's the salary you need to feel comfortable in California",
    },
    "living/lifestyle-family/comfortable-salary-texas/index.html": {
        "title": f"Here's the Salary You Need to Feel Comfortable in Texas (2026){BRAND}",
        "desc": "No state income tax helps — but rent and insurance still bite. See comfortable salary targets across Texas metros for your household.",
        "h1": "Here's the salary you need to feel comfortable in Texas",
    },
}


def is_content_page(path: Path, text: str) -> bool:
    if REDIRECT_MARK in text:
        return False
    if "noindex" in text[:800] and "refresh" in text[:800]:
        return False
    return "<title>" in text


def set_tag(text: str, tag: str, attr: str | None, new_inner: str) -> str:
    if attr:
        pattern = rf'(<{tag}[^>]*{re.escape(attr)}[^>]*>)(.*?)(</{tag}>)'
    else:
        pattern = rf'(<{tag}[^>]*>)(.*?)(</{tag}>)'
    repl = rf"\1{new_inner}\3"
    return re.sub(pattern, repl, text, count=1, flags=re.DOTALL | re.IGNORECASE)


def strip_brand(title: str) -> str:
    return title.replace(BRAND, "").strip()


def set_title(text: str, title: str) -> str:
    text = re.sub(r"<title>.*?</title>", f"<title>{title}</title>", text, count=1, flags=re.DOTALL)
    short = strip_brand(title)
    if re.search(r'<meta property="og:title"', text, re.I):
        text = re.sub(
            r'(<meta property="og:title" content=")[^"]*(")',
            rf'\1{escape_meta(short)}\2',
            text,
            count=1,
            flags=re.I,
        )
    if re.search(r'<meta name="twitter:title"', text, re.I):
        text = re.sub(
            r'(<meta name="twitter:title" content=")[^"]*(")',
            rf'\1{escape_meta(short)}\2',
            text,
            count=1,
            flags=re.I,
        )
    return text


def escape_meta(desc: str) -> str:
    return desc.replace("&", "&amp;").replace('"', "&quot;")


def set_meta_description(text: str, desc: str) -> str:
    safe = escape_meta(desc)
    if re.search(r'<meta name="description"', text, re.I):
        return re.sub(
            r'(<meta name="description" content=")[^"]*(")',
            rf"\1{safe}\2",
            text,
            count=1,
            flags=re.I,
        )
    return text


def set_og_twitter(text: str, *, og_title: str | None = None, twitter_title: str | None = None) -> str:
    if og_title and re.search(r'<meta property="og:title"', text, re.I):
        text = re.sub(
            r'(<meta property="og:title" content=")[^"]*(")',
            rf"\1{og_title}\2",
            text,
            count=1,
            flags=re.I,
        )
    if twitter_title and re.search(r'<meta name="twitter:title"', text, re.I):
        text = re.sub(
            r'(<meta name="twitter:title" content=")[^"]*(")',
            rf"\1{twitter_title}\2",
            text,
            count=1,
            flags=re.I,
        )
    return text


def set_first_h1(text: str, h1: str) -> str:
    return re.sub(r"(<h1[^>]*>)(.*?)(</h1>)", rf"\1{h1}\3", text, count=1, flags=re.DOTALL | re.IGNORECASE)


def cs_path_depth(rel: str) -> int:
    parts = rel.split("/")
    if "comfortable-salary" not in parts:
        return 0
    idx = parts.index("comfortable-salary")
    return len(parts) - idx - 2  # exclude index.html


def apply_pattern_rules(rel: str, text: str) -> tuple[str, bool]:
    changed = False
    original = text
    title_brand = re.escape(BRAND)

    # Comfortable salary — city (state/city segment)
    m = re.search(r"<title>Comfortable Salary in ([^<(]+) \(2026\)" + title_brand + r"</title>", text)
    if m and cs_path_depth(rel) >= 2:
        place = m.group(1).strip()
        title = f"What Salary Do You Need to Feel Comfortable in {place}? (2026){BRAND}"
        desc = (
            f"Wondering if your paycheck stretches in {place}? See comfortable income targets "
            f"for singles, couples, and families — with real rent, tax, and lifestyle math."
        )
        text = set_title(text, title)
        text = set_meta_description(text, desc)
        text = set_first_h1(text, f"What salary do you need to feel comfortable in {place}?")
        changed = True
        return text, changed

    # Comfortable salary — state hub
    m = re.search(r"<title>Comfortable Salary in ([^<(]+) \(2026\)" + title_brand + r"</title>", text)
    if m and cs_path_depth(rel) == 1:
        state = m.group(1).strip()
        title = f"Here's What a Comfortable Salary Looks Like in {state} (2026){BRAND}"
        desc = (
            f"Curious what you'd need to earn in {state}? Browse city-by-city salary targets, "
            f"median rent, taxes, and family income ranges."
        )
        text = set_title(text, title)
        text = set_meta_description(text, desc)
        text = set_first_h1(text, f"What salary do you need to feel comfortable in {state}?")
        changed = True
        return text, changed

    # Moving cost — city/state
    m = re.search(r"<title>Moving Cost Calculator for ([^|]+)\s*\|\s*Income Clarity</title>", text)
    if m:
        place = m.group(1).strip()
        title = f"How Much Does It Cost to Move to {place}? Real Numbers (2026){BRAND}"
        desc = (
            f"Planning a move to {place}? Estimate movers, deposits, utilities, and how your "
            f"monthly budget changes — before you commit."
        )
        text = set_title(text, title)
        text = set_meta_description(text, desc)
        if re.search(rf"<h1>Moving Cost Calculator for {re.escape(place)}</h1>", text):
            text = set_first_h1(text, f"How much does it really cost to move to {place}?")
        changed = True
        return text, changed

    # House afford — state guide
    m = re.search(
        r"<title>How Much House Can I Afford in ([^?]+)\? Calculator &amp; City Guide" + title_brand + r"</title>",
        text,
    )
    if m:
        state = m.group(1).strip()
        title = f"Can You Afford a Home in {state}? Here's What Your Income Buys (2026){BRAND}"
        desc = (
            f"Before you tour listings in {state}, see what home price fits the 28% rule on your "
            f"real income — with local tax, insurance, and city breakdowns."
        )
        text = set_title(text, title)
        text = set_meta_description(text, desc)
        changed = True
        return text, changed

    # House afford — city
    m = re.search(
        r"<title>How Much House Can I Afford in ([^,]+), ([^?]+)\?" + title_brand + r"</title>",
        text,
    )
    if m:
        city, state = m.group(1).strip(), m.group(2).strip()
        title = f"Can You Afford a Home in {city}? What {state} Buyers Actually Need (2026){BRAND}"
        desc = (
            f"Median prices in {city} don't tell your story. Run your income through the 28% rule "
            f"and see what monthly payment — and home price — you can actually carry."
        )
        text = set_title(text, title)
        text = set_meta_description(text, desc)
        changed = True
        return text, changed

    # COL — state hub
    m = re.search(r"<title>([^<]+) Cost of Living by City" + title_brand + r"</title>", text)
    if m and "cost-of-living-by-city" in rel:
        state = m.group(1).strip()
        title = f"{state} Cost of Living: Which Cities Stretch Your Pay the Furthest? (2026){BRAND}"
        desc = (
            f"Not every {state} city costs the same. Compare rent, groceries, taxes, and salary "
            f"needs across metros before you move or negotiate an offer."
        )
        text = set_title(text, title)
        text = set_meta_description(text, desc)
        changed = True
        return text, changed

    # COL — city
    m = re.search(
        r"<title>([^<]+) Cost of Living: Rent, Salary &amp; Budget \(2026\)" + title_brand + r"</title>",
        text,
    )
    if m:
        city = m.group(1).strip()
        title = f"{city} Cost of Living: Can You Afford to Live There? (2026){BRAND}"
        desc = (
            f"Thinking about {city}? See typical rent, groceries, transport, taxes, and the salary "
            f"you'd need to live comfortably — with a side-by-side city comparison."
        )
        text = set_title(text, title)
        text = set_meta_description(text, desc)
        changed = True
        return text, changed

    # COL — compare
    m = re.search(
        r"<title>([^<]+) vs ([^<]+) Cost of Living \(2026\)" + title_brand + r"</title>",
        text,
    )
    if m:
        a, b = m.group(1).strip(), m.group(2).strip()
        title = f"{a} vs {b}: Which City Costs Less to Live In? (2026){BRAND}"
        desc = (
            f"Choosing between {a} and {b}? Compare rent, daily expenses, taxes, and take-home "
            f"pay so you know which city leaves more in your pocket."
        )
        text = set_title(text, title)
        text = set_meta_description(text, desc)
        changed = True
        return text, changed

    # Hourly — state
    m = re.search(
        r"<title>([^<]+) Salary After Tax Calculator: Your Real Take-Home Pay in 2026" + title_brand + r"</title>",
        text,
    )
    if m:
        state = m.group(1).strip()
        title = f"How Much of Your {state} Salary Do You Actually Keep in 2026?{BRAND}"
        desc = (
            f"Gross pay in {state} isn't what you spend. Convert $15–$50/hr to real take-home "
            f"after federal tax, FICA, and {state} state tax."
        )
        text = set_title(text, title)
        text = set_meta_description(text, desc)
        changed = True
        return text, changed

    # Long-form comfortable salary (family pages)
    m = re.search(
        r"<title>How Much Salary Do You Need to Live Comfortably in ([^<]+) in 2026\?" + title_brand + r"</title>",
        text,
    )
    if m:
        state = m.group(1).strip()
        title = f"Here's the Salary You Need to Feel Comfortable in {state} (2026){BRAND}"
        desc = (
            f"Wondering what comfortable really means in {state}? See income targets by city, "
            f"household type, and lifestyle — with rent and tax math built in."
        )
        text = set_title(text, title)
        text = set_meta_description(text, desc)
        changed = True
        return text, changed

    return text, text != original


def apply_manual(rel: str, text: str) -> tuple[str, bool]:
    cfg = MANUAL.get(rel)
    if not cfg:
        return text, False
    if "title" in cfg:
        text = set_title(text, cfg["title"])
    if "desc" in cfg:
        text = set_meta_description(text, cfg["desc"])
    if "h1" in cfg:
        text = set_first_h1(text, cfg["h1"])
    text = set_og_twitter(
        text,
        og_title=cfg.get("og_title"),
        twitter_title=cfg.get("twitter_title"),
    )
    return text, True


def sync_social_from_title(text: str) -> str:
    m = re.search(r"<title>(.*?)</title>", text, re.DOTALL)
    if not m:
        return text
    short = strip_brand(m.group(1))
    return set_og_twitter(text, og_title=short, twitter_title=short)


def process_file(path: Path) -> bool:
    rel = path.relative_to(ROOT).as_posix()
    text = path.read_text(encoding="utf-8")
    if not is_content_page(path, text):
        return False

    updated, _ = apply_manual(rel, text)
    updated, _ = apply_pattern_rules(rel, updated)
    updated = sync_social_from_title(updated)
    if updated == text:
        return False

    path.write_text(updated, encoding="utf-8")
    return True


def main() -> None:
    count = 0
    for path in sorted(ROOT.rglob("*.html")):
        if process_file(path):
            count += 1
            print(f"updated {path.relative_to(ROOT)}")
    print(f"Done. Updated {count} files.")


if __name__ == "__main__":
    main()
