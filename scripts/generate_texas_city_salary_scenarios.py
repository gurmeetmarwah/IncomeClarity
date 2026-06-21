#!/usr/bin/env python3
"""Generate Dallas and Houston salary scenario pages from Austin hand-maintained templates."""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

from salary_scenario_unique_sections import estimate_taxes, inject_unique_sections, patch_take_home_snippets  # noqa: E402
AUSTIN_DIR = ROOT / "living" / "lifestyle" / "comfortable-salary" / "texas" / "austin"
OUT_BASE = ROOT / "living" / "lifestyle" / "comfortable-salary" / "texas"

TIERS = ("75k", "100k", "150k")
TIER_SALARY = {"75k": 75_000, "100k": 100_000, "150k": 150_000}
AUSTIN_HUB = "/living/lifestyle/comfortable-salary/texas/austin"

CITY_CONFIG: dict[str, dict] = {
    "dallas": {
        "name": "Dallas",
        "slug": "dallas",
        "hub": "/living/lifestyle/comfortable-salary/texas/dallas",
        "rent": 1550,
        "core": 2500,
        "col_index": 102,
        "single_comfortable": 80_000,
        "couple_comfortable": 105_000,
        "family_comfortable": 135_000,
        "compare_city_name": "Austin",
        "compare_hub": AUSTIN_HUB,
        "neighborhoods_premium": "Uptown, Deep Ellum, or Plano suburbs",
        "suburbs_family": "Frisco, Plano, or Arlington",
        "rent_75k_vs_100k": (1500, 2100),
        "home_75k": "$225k–$300k",
        "home_100k": "$300k–$400k",
        "home_100k_mortgage": "$1,950–$2,400/mo",
        "home_150k_tiers": ("$350k–$450k", "$500k–$600k", "$650k–$750k"),
        "home_150k_feasibility": (
            ("$350k", "Comfortable"),
            ("$550k", "Realistic"),
            ("$750k", "Possible with planning"),
        ),
        "rent_ranges": {
            "studio": "~$1,100–$1,300",
            "1br": "~$1,450–$1,650",
            "2br": "~$1,800–$2,100",
        },
        "premium_rent_150k": "$2,700–$3,400/month",
        "family_3br": "$2,200–$2,900/month",
        "75k_texas_row": "Comfortable",
        "75k_texas_austin": "Moderate–Comfortable",
        "100k_city_row": "Very Comfortable",
        "100k_austin_row": "Comfortable",
        "150k_city_row": "High Flexibility",
        "150k_austin_row": "Very Comfortable",
        "75k_verdict_single": "🟢 Yes, for many single adults.",
        "75k_verdict_family": "⚠️ Tight for families with children.",
        "75k_lifestyle_single": "Comfortable",
        "75k_lifestyle_downtown": "Comfortable",
        "75k_salary_row": "Very Comfortable",
        "75k_faq_rent_premium": "$1,900",
        "100k_faq_compare": (
            "Dallas rent runs lower than Austin on average, but both cities have no state income tax. "
            "At $100k, Dallas often feels very comfortable while Austin lands at comfortable with slightly less housing flexibility."
        ),
        "100k_faq_compare_q": "Is Dallas expensive compared to Austin?",
    },
    "houston": {
        "name": "Houston",
        "slug": "houston",
        "hub": "/living/lifestyle/comfortable-salary/texas/houston",
        "rent": 1400,
        "core": 2330,
        "col_index": 96,
        "single_comfortable": 75_000,
        "couple_comfortable": 95_000,
        "family_comfortable": 125_000,
        "compare_city_name": "Austin",
        "compare_hub": AUSTIN_HUB,
        "neighborhoods_premium": "Montrose, The Heights, or Katy suburbs",
        "suburbs_family": "Katy, Sugar Land, or The Woodlands",
        "rent_75k_vs_100k": (1350, 1950),
        "home_75k": "$200k–$275k",
        "home_100k": "$275k–$375k",
        "home_100k_mortgage": "$1,800–$2,200/mo",
        "home_150k_tiers": ("$325k–$425k", "$450k–$550k", "$600k–$700k"),
        "home_150k_feasibility": (
            ("$325k", "Comfortable"),
            ("$500k", "Realistic"),
            ("$700k", "Possible with planning"),
        ),
        "rent_ranges": {
            "studio": "~$950–$1,150",
            "1br": "~$1,250–$1,450",
            "2br": "~$1,600–$1,900",
        },
        "premium_rent_150k": "$2,500–$3,200/month",
        "family_3br": "$2,000–$2,700/month",
        "75k_texas_row": "Very Comfortable",
        "75k_texas_austin": "Moderate–Comfortable",
        "100k_city_row": "Very Comfortable",
        "100k_austin_row": "Comfortable",
        "150k_city_row": "High Flexibility",
        "150k_austin_row": "Very Comfortable",
        "75k_verdict_single": "🟢 Yes, for most single adults.",
        "75k_verdict_family": "⚠️ More challenging for families with children.",
        "75k_lifestyle_single": "Very Comfortable",
        "75k_lifestyle_downtown": "Comfortable",
        "75k_salary_row": "Very Comfortable",
        "75k_faq_rent_premium": "$1,750",
        "100k_faq_compare": (
            "Houston is one of the most affordable major Texas metros — rent and home prices run well below Austin. "
            "At $100k, Houston often feels very comfortable with strong savings headroom."
        ),
        "100k_faq_compare_q": "Is Houston expensive compared to Austin?",
    },
}


def _fmt(n: int) -> str:
    return f"${n:,}"


def load_template(tier: str) -> str:
    path = AUSTIN_DIR / f"is-{tier}-enough-to-live-in-austin" / "index.html"
    if not path.is_file():
        raise FileNotFoundError(f"Austin template missing: {path}")
    return path.read_text(encoding="utf-8")


def apply_path_replacements(html: str, cfg: dict) -> str:
    city = cfg["slug"]
    name = cfg["name"]
    hub = cfg["hub"]

    for tier in TIERS:
        html = html.replace(f"is-{tier}-enough-to-live-in-austin", f"is-{tier}-enough-to-live-in-{city}")

    for path in (
        "/living/housing/how-much-house-can-i-afford/texas/austin",
        "/living/housing/cost-of-living-by-city/texas/austin",
        "/living/housing/moving-cost-calculator/texas/austin",
    ):
        html = html.replace(path, path.replace("/austin", f"/{city}"))

    html = html.replace(f"{AUSTIN_HUB}/is-", f"{hub}/is-")
    html = html.replace(
        f"https://www.incomeclaritylab.com{AUSTIN_HUB}/is-",
        f"https://www.incomeclaritylab.com{hub}/is-",
    )
    html = html.replace(
        f'<li><a href="{AUSTIN_HUB}">Austin</a></li>',
        f'<li><a href="{hub}">{name}</a></li>',
    )
    html = html.replace(
        f'"position": 3, "name": "Austin", "item": "https://www.incomeclaritylab.com{AUSTIN_HUB}"',
        f'"position": 3, "name": "{name}", "item": "https://www.incomeclaritylab.com{hub}"',
    )
    html = html.replace(f'href="{AUSTIN_HUB}#cs-calc"', f'href="{hub}#cs-calc"')
    html = html.replace(
        f'href="{AUSTIN_HUB}">\n            <h3>Austin Comfortable Salary Guide</h3>',
        f'href="{hub}">\n            <h3>{name} Comfortable Salary Guide</h3>',
    )

    html = html.replace("Austin salary scenario", f"{name} salary scenario")
    html = html.replace("Live in Austin?", f"Live in {name}?")
    html = html.replace("enough to live in Austin", f"enough to live in {name}")
    html = html.replace("Enough to Live in Austin", f"Enough to Live in {name}")
    html = html.replace("Live Comfortably in Austin", f"Live Comfortably in {name}")
    html = html.replace(" to live in Austin ", f" to live in {name} ")
    html = html.replace(" in Austin —", f" in {name} —")
    html = html.replace(" in Austin after", f" in {name} after")
    html = html.replace(" in Austin,", f" in {name},")
    html = html.replace(" in Austin.", f" in {name}.")
    html = html.replace(" in Austin in 2026", f" in {name} in 2026")
    html = html.replace(" in Austin?", f" in {name}?")
    html = html.replace("support in Austin", f"support in {name}")
    html = html.replace("create in Austin?", f"create in {name}?")
    html = html.replace("$75,000 in Austin", f"$75,000 in {name}")
    html = html.replace("$100,000 in Austin", f"$100,000 in {name}")
    html = html.replace("$150,000 in Austin", f"$150,000 in {name}")
    html = html.replace("Pre-filled for $75,000 in Austin", f"Pre-filled for $75,000 in {name}")
    html = html.replace("$100k in Austin", f"$100k in {name}")
    html = html.replace("$150k in Austin", f"$150k in {name}")
    html = html.replace("Austin salary calculator", f"{name} salary calculator")
    html = html.replace("Full Austin calculator", f"Full {name} calculator")
    html = html.replace("Know your real number in Austin", f"Know your real number in {name}")
    html = html.replace("on our Austin calculator.", f"on our {name} calculator.")
    html = html.replace("Rent vs Buy Austin", f"Rent vs Buy {name}")
    html = html.replace("Cost of Living Austin", f"Cost of Living {name}")
    html = html.replace("Moving to Austin Calculator", f"Moving to {name} Calculator")
    html = html.replace("Austin-specific", f"{name}-specific")
    html = html.replace("How Much House Can I Afford in Austin →", f"How Much House Can I Afford in {name} →")

    return html


def patch_remaining_austin_refs(html: str, cfg: dict) -> str:
    name = cfg["name"]
    html = html.replace("in the Austin metro", f"in the {name} metro")
    html = html.replace("Austin Lifestyle", f"{name} Lifestyle")
    html = html.replace("At $100k, Austin is comfortable", f"At $100k, {name} is very comfortable")
    html = html.replace("central Austin on one income", f"central {name} on one income")
    return html


def rebuild_texas_compare_75k(html: str, cfg: dict) -> str:
    name = cfg["name"]
    hub = cfg["hub"]
    slug = cfg["slug"]

    def row(city_slug: str, city_name: str, label: str, here: bool = False) -> str:
        city_hub = f"/living/lifestyle/comfortable-salary/texas/{city_slug}"
        cell = f"<strong>{label}</strong> (you are here)" if here else label
        return (
            f'              <tr>\n'
            f'                <th scope="row"><a href="{city_hub}">{city_name}</a></th>\n'
            f"                <td>{cell}</td>\n"
            f"              </tr>"
        )

    tbody = "\n".join(
        [
            row("austin", "Austin", cfg["75k_texas_austin"]),
            row(
                "dallas",
                "Dallas",
                cfg["75k_texas_row"] if slug == "dallas" else "Comfortable",
                slug == "dallas",
            ),
            row(
                "houston",
                "Houston",
                cfg["75k_texas_row"] if slug == "houston" else "Very Comfortable",
                slug == "houston",
            ),
            '              <tr>\n                <th scope="row"><a href="/living/lifestyle/comfortable-salary/texas">San Antonio</a></th>\n                <td>Very Comfortable</td>\n              </tr>',
        ]
    )
    pattern = r'(<section class="ss-band" id="texas-compare">.*?<tbody>)\s*.*?\s*(</tbody>)'
    replacement = rf"\1\n{tbody}\n            \2"
    html, count = re.subn(pattern, replacement, html, count=1, flags=re.DOTALL)
    if count == 0:
        raise ValueError(f"Could not rebuild Texas compare table for {name}")
    return html


def rebuild_home_feasibility_150k(html: str, cfg: dict) -> str:
    rows = []
    for price, label in cfg["home_150k_feasibility"]:
        if label in ("Comfortable", "Realistic"):
            rows.append(
                f'              <tr><th scope="row">{price}</th>'
                f'<td><strong style="color:var(--ss-ok)">{label}</strong></td></tr>'
            )
        else:
            rows.append(f"              <tr><th scope=\"row\">{price}</th><td>{label}</td></tr>")
    tbody = "\n".join(rows)
    pattern = r'(<section class="ss-band ss-band--alt" id="home-buying">.*?<tbody>)\s*.*?\s*(</tbody>)'
    replacement = rf"\1\n{tbody}\n            \2"
    html, count = re.subn(pattern, replacement, html, count=1, flags=re.DOTALL)
    if count == 0:
        raise ValueError(f"Could not rebuild home feasibility table for {cfg['name']}")
    return html


def adapt_cta(html: str, cfg: dict) -> str:
    compare = cfg["compare_city_name"]
    compare_hub = cfg["compare_hub"]
    html = re.sub(
        r'(<a href=")[^"]+(">Compare )(?:Dallas|Houston|Austin)(</a>)',
        rf'\1{compare_hub}\2{compare}\3',
        html,
        count=1,
    )
    html = html.replace(
        "Layer household size, housing choice, and lifestyle tier on our Austin calculator.",
        f"Layer household size, housing choice, and lifestyle tier on our {cfg['name']} calculator.",
    )
    return html


def adapt_75k(html: str, cfg: dict) -> str:
    name = cfg["name"]
    rent = cfg["rent"]
    hub = cfg["hub"]
    ranges = cfg["rent_ranges"]
    expenses_low = rent + 1630
    expenses_high = rent + 1930

    html = html.replace("🟡 Yes, for many single adults.", cfg["75k_verdict_single"])
    html = html.replace("⚠️ More challenging for families with children.", cfg["75k_verdict_family"])
    html = html.replace(
        f'value="1700" min="500"',
        f'value="{rent}" min="500"',
    )
    html = html.replace(
        f'aria-label="Monthly cost breakdown: housing $1,700, utilities $180, groceries $450, transportation $450, healthcare $300, entertainment $250. Total estimated $3,300 to $4,000 per month."',
        f'aria-label="Monthly cost breakdown: housing ${rent:,}, utilities $180, groceries $450, transportation $450, healthcare $300, entertainment $250. Total estimated {_fmt(expenses_low)} to {_fmt(expenses_high)} per month."',
    )
    html = html.replace("<strong>$1,700</strong>", f"<strong>${rent:,}</strong>", 1)
    html = html.replace("<strong>$3,300 – $4,000</strong>", f"<strong>${expenses_low:,} – ${expenses_high:,}</strong>")
    html = html.replace("What Does Living in Austin Cost?", f"What Does Living in {name} Cost?")
    html = html.replace("Can You Afford Austin on $75k?", f"Can You Afford {name} on $75k?")
    html = html.replace("~$1,250–$1,450", ranges["studio"])
    html = html.replace("~$1,650–$1,850", ranges["1br"])
    html = html.replace("~$2,000–$2,400", ranges["2br"])
    html = html.replace("$250k–$325k range", f"{cfg['home_75k']} range")
    html = html.replace(
        f'How Much House Can I Afford in {name} →',
        f"How Much House Can I Afford in {name} →",
    )
    html = html.replace("Salary comparison for Austin lifestyle tiers", f"Salary comparison for {name} lifestyle tiers")
    html = html.replace(
        "<td><strong>Comfortable</strong> (you are here)</td>",
        f"<td><strong>{cfg['75k_salary_row']}</strong> (you are here)</td>",
    )
    html = html.replace("Austin vs Other Texas Cities", f"{name} vs Other Texas Cities")
    html = rebuild_texas_compare_75k(html, cfg)
    html = html.replace(
        f"Can I afford a $1,700 apartment on $75k in {name}?",
        f"Can I afford a {_fmt(rent)} apartment on $75k in {name}?",
    )
    html = html.replace(
        f"Yes — $1,700 rent is roughly 33–35% of estimated after-tax income, within common budgeting ranges. Downtown or premium units above $2,000 feel tighter on $75k.",
        f"Yes — {_fmt(rent)} rent is roughly 30–33% of estimated after-tax income, within common budgeting ranges. Premium units above {cfg['75k_faq_rent_premium']} feel tighter on $75k.",
    )
    html = html.replace(
        f"How does $75k compare to other salaries in {name}?",
        f"How does $75k compare to other salaries in {name}?",
    )
    html = html.replace(
        "$50k is difficult for most households. $75k is comfortable for many singles. $100k is very comfortable for singles and solid for couples. $150k offers high flexibility including homeownership.",
        f"$50k is difficult for most households. $75k is {cfg['75k_lifestyle_single'].lower()} for many singles in {name}. $100k is very comfortable for singles and solid for couples. $150k offers high flexibility including homeownership.",
    )
    html = html.replace(
        f'<tr><th scope="row">Single downtown</th><td><span class="ss-tag ss-tag--moderate">Moderate</span></td></tr>',
        f'<tr><th scope="row">Single downtown</th><td><span class="ss-tag ss-tag--{"comfortable" if cfg["75k_lifestyle_downtown"] == "Comfortable" else "moderate"}">{cfg["75k_lifestyle_downtown"]}</span></td></tr>',
    )
    html = html.replace(
        f'<tr><th scope="row">Single renter</th><td><span class="ss-tag ss-tag--comfortable">Comfortable</span></td></tr>',
        f'<tr><th scope="row">Single renter</th><td><span class="ss-tag ss-tag--{"comfortable" if "Comfortable" in cfg["75k_lifestyle_single"] else "moderate"}">{cfg["75k_lifestyle_single"]}</span></td></tr>',
    )
    html = patch_remaining_austin_refs(html, cfg)
    html = adapt_cta(html, cfg)
    return html


def adapt_100k(html: str, cfg: dict) -> str:
    name = cfg["name"]
    hub = cfg["hub"]
    rent_75, rent_100 = cfg["rent_75k_vs_100k"]

    html = html.replace(
        f'<a href="{hub}/is-75k-enough-to-live-in-{cfg["slug"]}">$75k {name} scenario</a>',
        f'<a href="{hub}/is-75k-enough-to-live-in-{cfg["slug"]}">$75k {name} scenario</a>',
    )
    html = html.replace("$75k Austin scenario", f"$75k {name} scenario")
    html = html.replace("How $75k and $100k compare in Austin", f"How $75k and $100k compare in {name}")
    html = html.replace("<td>$1,700</td><td>$2,300</td>", f"<td>${rent_75:,}</td><td>${rent_100:,}</td>")
    html = html.replace("The $100k Lifestyle in Austin", f"The $100k Lifestyle in {name}")
    html = html.replace("$325k–$425k", cfg["home_100k"])
    html = html.replace("$2,100–$2,600/mo", cfg["home_100k_mortgage"])
    html = html.replace(
        "a 3BR in Cedar Park, Round Rock, or Pflugerville ($2,200–$2,800)",
        f"a 3BR in {cfg['suburbs_family']} ($2,000–$2,700)",
    )
    html = html.replace(
        "family comfortable in Austin lands near $145k",
        f"family comfortable in {name} lands near {_fmt(cfg['family_comfortable'])}",
    )
    html = html.replace("Austin Compared With Other Cities", f"{name} Compared With Other Cities")
    html = html.replace(
        f'<th scope="row"><a href="{AUSTIN_HUB}">Austin</a></th>\n                <td>Comfortable</td>',
        f'<th scope="row"><a href="{AUSTIN_HUB}">Austin</a></th>\n                <td>{cfg["100k_austin_row"]}</td>',
    )
    html = html.replace(
        f'<th scope="row"><a href="{hub}">{name}</a></th>\n                <td>Very Comfortable</td>',
        f'<th scope="row"><a href="{hub}">{name}</a></th>\n                <td><strong>{cfg["100k_city_row"]}</strong> (you are here)</td>',
    )
    html = html.replace(
        "Is Austin expensive compared to Dallas?",
        cfg["100k_faq_compare_q"],
    )
    html = html.replace(
        "Austin rent runs higher than Dallas on average, but both cities have no state income tax. At $100k, Dallas often feels very comfortable while Austin lands at comfortable with slightly less housing flexibility.",
        cfg["100k_faq_compare"],
    )
    html = html.replace(
        f"Yes — $100,000 sits above the metro median household income and clears our comfortable tier for single adults.",
        f"Yes — $100,000 sits above the {name} metro median household income and clears our comfortable tier for single adults ({_fmt(cfg['single_comfortable'])}).",
    )
    html = html.replace(
        "typical affordability lands in the $325k–$425k range",
        f"typical affordability lands in the {cfg['home_100k']} range",
    )
    html = html.replace(
        "Mortgage payments often run $2,100–$2,600/month",
        f"Mortgage payments often run {cfg['home_100k_mortgage'].replace('/mo', '/month')}",
    )
    html = html.replace(
        f'<a href="{hub}/is-75k-enough-to-live-in-{cfg["slug"]}">\n            <h3>Is $75k Enough to Live in {name}?</h3>',
        f'<a href="{hub}/is-75k-enough-to-live-in-{cfg["slug"]}">\n            <h3>Is $75k Enough to Live in {name}?</h3>',
    )
    html = patch_remaining_austin_refs(html, cfg)
    html = adapt_cta(html, cfg)
    return html


def adapt_150k(html: str, cfg: dict) -> str:
    name = cfg["name"]
    hub = cfg["hub"]
    starter, move_up, luxury = cfg["home_150k_tiers"]

    html = html.replace(f"What Does $150k Actually Feel Like in Austin?", f"What Does $150k Actually Feel Like in {name}?")
    html = html.replace(
        f"At this income, Austin stops feeling like a tradeoff city.",
        f"At this income, {name} stops feeling like a tradeoff city.",
    )
    html = html.replace(f"Can You Buy a Home in Austin on $150k?", f"Can You Buy a Home in {name} on $150k?")
    html = html.replace("$350k–$450k", starter)
    html = html.replace("$500k–$650k", move_up)
    html = html.replace("$700k–$850k", luxury)
    html = html.replace("Home price feasibility on $150,000 in Austin", f"Home price feasibility on $150,000 in {name}")
    html = rebuild_home_feasibility_150k(html, cfg)

    html = html.replace(
        "Westlake, Circle C, Mueller, or central 78704 — premium areas that feel out of reach at $75k–$100k.",
        f"{cfg['neighborhoods_premium']} — premium areas that feel out of reach at $75k–$100k.",
    )
    html = html.replace(
        "$3,000–$3,800/month for a 2–3BR in central Austin while still saving 15%+.",
        f"{cfg['premium_rent_150k']} for a 2–3BR in desirable {name} neighborhoods while still saving 15%+.",
    )
    html = html.replace(
        "$2,400–$3,200/month rent or mortgage in good school districts fits the budget.",
        f"{cfg['family_3br']} rent or mortgage in good school districts fits the budget.",
    )
    html = html.replace("Austin vs Other Cities on $150k", f"{name} vs Other Cities on $150k")
    html = html.replace(
        f'<th scope="row"><a href="{AUSTIN_HUB}">Austin</a></th>\n                <td>Very Comfortable</td>',
        f'<th scope="row"><a href="{AUSTIN_HUB}">Austin</a></th>\n                <td>{cfg["150k_austin_row"]}</td>',
    )
    html = html.replace(
        f'<th scope="row"><a href="{hub}">{name}</a></th>\n                <td>High Flexibility</td>',
        f'<th scope="row"><a href="{hub}">{name}</a></th>\n                <td><strong>{cfg["150k_city_row"]}</strong> (you are here)</td>',
    )
    html = html.replace(
        f"A snapshot of what this income unlocks in Austin — optimization decisions, not survival tradeoffs.",
        f"A snapshot of what this income unlocks in {name} — optimization decisions, not survival tradeoffs.",
    )
    html = html.replace(
        f"Is $150k a good household income in Austin?",
        f"Is $150k a good household income in {name}?",
    )
    html = html.replace(
        f"It sits well above Austin's median household income",
        f"It sits well above {name}'s median household income",
    )
    html = html.replace(
        "Can I buy a $600k home in Austin on $150k?",
        f"Can I buy a {cfg['home_150k_feasibility'][1][0]} home in {name} on $150k?",
    )
    html = html.replace(
        "enough for many $500k–$650k homes depending on rate and down payment.",
        f"enough for many {move_up} homes depending on rate and down payment.",
    )
    html = html.replace(
        f"Can a family of 4 save while living on $150k in Austin?",
        f"Can a family of 4 save while living on $150k in {name}?",
    )
    html = html.replace(
        f"Why do some $150k earners still feel financially stressed in Austin?",
        f"Why do some $150k earners still feel financially stressed in {name}?",
    )
    html = patch_remaining_austin_refs(html, cfg)
    html = adapt_cta(html, cfg)
    return html


ADAPTERS = {
    "75k": adapt_75k,
    "100k": adapt_100k,
    "150k": adapt_150k,
}


def generate_page(city_slug: str, tier: str) -> str:
    cfg = CITY_CONFIG[city_slug]
    html = load_template(tier)
    html = apply_path_replacements(html, cfg)
    html = ADAPTERS[tier](html, cfg)
    salary = TIER_SALARY[tier]
    html = inject_unique_sections(html, state="texas", city_slug=city_slug, salary=salary, hub=cfg["hub"])
    tax = estimate_taxes(salary, "texas", city_slug)
    html = patch_take_home_snippets(html, tax, salary)
    return html


def main() -> None:
    for city_slug in CITY_CONFIG:
        cfg = CITY_CONFIG[city_slug]
        out_dir = OUT_BASE / city_slug
        for tier in TIERS:
            slug = f"is-{tier}-enough-to-live-in-{city_slug}"
            path = out_dir / slug / "index.html"
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(generate_page(city_slug, tier), encoding="utf-8")
            print(f"  wrote {path.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
