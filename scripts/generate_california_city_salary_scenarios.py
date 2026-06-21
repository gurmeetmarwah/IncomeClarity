#!/usr/bin/env python3
"""Generate California city salary scenario pages ($100k / $150k / $200k) from Austin templates."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
AUSTIN_DIR = ROOT / "living" / "lifestyle" / "comfortable-salary" / "texas" / "austin"
OUT_BASE = ROOT / "living" / "lifestyle" / "comfortable-salary" / "california"
CA_STATE_HUB = "/living/lifestyle/comfortable-salary/california"
AUSTIN_HUB = "/living/lifestyle/comfortable-salary/texas/austin"

TIERS = ("100k", "150k", "200k")
TEMPLATE_TIER = {"100k": "100k", "150k": "150k", "200k": "150k"}

CITY_CONFIG: dict[str, dict] = {
    "los-angeles": {
        "name": "Los Angeles",
        "slug": "los-angeles",
        "hub": f"{CA_STATE_HUB}/los-angeles",
        "rent": 2600,
        "core": 3750,
        "single_comfortable": 115_000,
        "couple_comfortable": 155_000,
        "family_comfortable": 200_000,
        "take_home_100k": "~$5,400–$5,800/month",
        "take_home_150k": "~$8,200–$8,700/month",
        "take_home_200k": "~$10,800–$11,400/month",
        "score_100k": "Moderate",
        "score_150k": "Comfortable",
        "score_200k": "Very Comfortable",
        "check_100k_single": "ss-checklist--maybe",
        "check_100k_single_label": "Single Adult: Possible",
        "check_100k_couple": "",
        "check_100k_couple_label": "Couple",
        "rent_low_vs_100k": 2200,
        "rent_100k": 2600,
        "rent_100_vs_150": (2600, 3400),
        "rent_150_vs_200": (3400, 4200),
        "home_100k": "$450k–$550k",
        "home_100k_mortgage": "$2,800–$3,400/mo",
        "home_150k_tiers": ("$550k–$700k", "$750k–$950k", "$950k–$1.15M"),
        "home_150k_feasibility": (("$600k", "Comfortable"), ("$850k", "Realistic"), ("$1.1M", "Possible with planning")),
        "home_200k_feasibility": (("$800k", "Comfortable"), ("$1.1M", "Realistic"), ("$1.4M", "Possible with planning")),
        "home_200k_tiers": ("$700k–$900k", "$950k–$1.2M", "$1.2M–$1.5M"),
        "neighborhoods_premium": "Silver Lake, Santa Monica, or Westside neighborhoods",
        "suburbs_family": "Burbank, Long Beach, or Pasadena",
        "premium_rent_150k": "$3,400–$4,200/month",
        "premium_rent_200k": "$4,200–$5,500/month",
        "family_3br": "$3,200–$4,200/month",
        "100k_city_row": "Moderate",
        "100k_austin_row": "Comfortable",
        "150k_city_row": "Comfortable",
        "150k_austin_row": "Very Comfortable",
        "200k_city_row": "Very Comfortable",
        "200k_austin_row": "High Flexibility",
        "100k_faq_compare_q": "Is Los Angeles expensive compared to Austin?",
        "100k_faq_compare": (
            "Los Angeles rent and state income tax run higher than Austin. At $100k, Austin often feels comfortable "
            "while LA lands at moderate — you may need $115k+ for the same lifestyle buffer."
        ),
        "150k_faq_compare_q": "Is $150k enough in Los Angeles with state tax?",
        "150k_faq_compare": (
            "Yes for many singles and couples — $150k clears comfortable tier math after California taxes. "
            "Families with childcare still need careful budgeting or dual incomes."
        ),
        "budget_100k_takehome": 5600,
        "sample_budget_100k": (
            ("Housing", 2600, 46),
            ("Transportation", 520, 9),
            ("Food", 580, 10),
            ("Healthcare", 380, 7),
            ("Retirement", 450, 8),
            ("Travel", 200, 4),
            ("Investing", 250, 4),
            ("Utilities & misc", 620, 11),
        ),
    },
    "san-diego": {
        "name": "San Diego",
        "slug": "san-diego",
        "hub": f"{CA_STATE_HUB}/san-diego",
        "rent": 2550,
        "core": 3665,
        "single_comfortable": 115_000,
        "couple_comfortable": 150_000,
        "family_comfortable": 195_000,
        "take_home_100k": "~$5,400–$5,800/month",
        "take_home_150k": "~$8,200–$8,700/month",
        "take_home_200k": "~$10,800–$11,400/month",
        "score_100k": "Moderate–Comfortable",
        "score_150k": "Comfortable",
        "score_200k": "Very Comfortable",
        "check_100k_single": "",
        "check_100k_single_label": "Single Adult",
        "check_100k_couple": "",
        "check_100k_couple_label": "Couple",
        "rent_low_vs_100k": 2100,
        "rent_100k": 2550,
        "rent_100_vs_150": (2550, 3300),
        "rent_150_vs_200": (3300, 4000),
        "home_100k": "$425k–$525k",
        "home_100k_mortgage": "$2,700–$3,300/mo",
        "home_150k_tiers": ("$525k–$675k", "$700k–$900k", "$900k–$1.1M"),
        "home_150k_feasibility": (("$575k", "Comfortable"), ("$800k", "Realistic"), ("$1.05M", "Possible with planning")),
        "home_200k_feasibility": (("$750k", "Comfortable"), ("$1.05M", "Realistic"), ("$1.3M", "Possible with planning")),
        "home_200k_tiers": ("$675k–$850k", "$900k–$1.15M", "$1.1M–$1.4M"),
        "neighborhoods_premium": "North Park, La Jolla, or Little Italy",
        "suburbs_family": "Chula Vista, Carlsbad, or Poway",
        "premium_rent_150k": "$3,300–$4,000/month",
        "premium_rent_200k": "$4,000–$5,200/month",
        "family_3br": "$3,100–$4,000/month",
        "100k_city_row": "Moderate–Comfortable",
        "100k_austin_row": "Comfortable",
        "150k_city_row": "Comfortable",
        "150k_austin_row": "Very Comfortable",
        "200k_city_row": "Very Comfortable",
        "200k_austin_row": "High Flexibility",
        "100k_faq_compare_q": "Is San Diego cheaper than Los Angeles?",
        "100k_faq_compare": (
            "San Diego rent runs slightly below Los Angeles, but both have California state income tax. "
            "At $100k, San Diego often feels moderate–comfortable for singles — a bit easier than LA or SF."
        ),
        "150k_faq_compare_q": "Can a family live on $150k in San Diego?",
        "150k_faq_compare": (
            "Yes for many families — $150k supports comfortable tier with savings if housing stays near median. "
            "Childcare and coastal rent above $3,500/month compress margins quickly."
        ),
        "budget_100k_takehome": 5600,
        "sample_budget_100k": (
            ("Housing", 2550, 46),
            ("Transportation", 480, 9),
            ("Food", 550, 10),
            ("Healthcare", 360, 6),
            ("Retirement", 480, 9),
            ("Travel", 220, 4),
            ("Investing", 280, 5),
            ("Utilities & misc", 660, 12),
        ),
    },
    "san-francisco": {
        "name": "San Francisco",
        "slug": "san-francisco",
        "hub": f"{CA_STATE_HUB}/san-francisco",
        "rent": 3200,
        "core": 4290,
        "single_comfortable": 135_000,
        "couple_comfortable": 175_000,
        "family_comfortable": 230_000,
        "take_home_100k": "~$5,400–$5,800/month",
        "take_home_150k": "~$8,200–$8,700/month",
        "take_home_200k": "~$10,800–$11,400/month",
        "score_100k": "Tight",
        "score_150k": "Moderate–Comfortable",
        "score_200k": "Comfortable",
        "check_100k_single": "ss-checklist--maybe",
        "check_100k_single_label": "Single Adult: Tight",
        "check_100k_couple": "ss-checklist--maybe",
        "check_100k_couple_label": "Couple: Possible",
        "rent_low_vs_100k": 2600,
        "rent_100k": 3200,
        "rent_100_vs_150": (3200, 4000),
        "rent_150_vs_200": (4000, 4800),
        "home_100k": "$500k–$650k",
        "home_100k_mortgage": "$3,200–$3,900/mo",
        "home_150k_tiers": ("$650k–$850k", "$900k–$1.1M", "$1.1M–$1.35M"),
        "home_150k_feasibility": (("$700k", "Comfortable"), ("$950k", "Realistic"), ("$1.2M", "Possible with planning")),
        "home_200k_feasibility": (("$900k", "Comfortable"), ("$1.25M", "Realistic"), ("$1.55M", "Possible with planning")),
        "home_200k_tiers": ("$850k–$1.05M", "$1.1M–$1.35M", "$1.35M–$1.65M"),
        "neighborhoods_premium": "Noe Valley, Pacific Heights, or SOMA",
        "suburbs_family": "Oakland, Berkeley, or Daly City",
        "premium_rent_150k": "$4,000–$5,000/month",
        "premium_rent_200k": "$5,000–$6,500/month",
        "family_3br": "$3,800–$5,000/month",
        "100k_city_row": "Challenging",
        "100k_austin_row": "Comfortable",
        "150k_city_row": "Moderate–Comfortable",
        "150k_austin_row": "Very Comfortable",
        "200k_city_row": "Comfortable",
        "200k_austin_row": "High Flexibility",
        "100k_faq_compare_q": "Is $100k enough in San Francisco?",
        "100k_faq_compare": (
            "$100k is tight in San Francisco after state tax and median rent near $3,200. "
            "Many singles need $135k+ for comfortable tier — compare offers to Austin or San Diego for context."
        ),
        "150k_faq_compare_q": "Is $150k middle class in San Francisco?",
        "150k_faq_compare": (
            "Yes — $150k is solidly middle class in SF and clears comfortable tier for singles. "
            "Families and homeownership in the city core still require tradeoffs or higher combined income."
        ),
        "budget_100k_takehome": 5600,
        "sample_budget_100k": (
            ("Housing", 3200, 57),
            ("Transportation", 350, 6),
            ("Food", 520, 9),
            ("Healthcare", 380, 7),
            ("Retirement", 350, 6),
            ("Travel", 150, 3),
            ("Investing", 150, 3),
            ("Utilities & misc", 500, 9),
        ),
    },
}


def _fmt(n: int) -> str:
    return f"${n:,}"


def load_template(tier: str) -> str:
    src_tier = TEMPLATE_TIER[tier]
    path = AUSTIN_DIR / f"is-{src_tier}-enough-to-live-in-austin" / "index.html"
    if not path.is_file():
        raise FileNotFoundError(f"Template missing: {path}")
    return path.read_text(encoding="utf-8")


def apply_path_replacements(html: str, cfg: dict, tier: str) -> str:
    city = cfg["slug"]
    name = cfg["name"]
    hub = cfg["hub"]
    salary_label = tier.replace("k", ",000").replace("100,000", "100,000")
    salary_map = {"100k": "$100,000", "150k": "$150,000", "200k": "$200,000"}
    sal = salary_map[tier]

    for t in ("75k", "100k", "150k", "200k"):
        html = html.replace(f"is-{t}-enough-to-live-in-austin", f"is-{t}-enough-to-live-in-{city}")

    for path in (
        "/living/housing/how-much-house-can-i-afford/texas/austin",
        "/living/housing/cost-of-living-by-city/texas/austin",
        "/living/housing/moving-cost-calculator/texas/austin",
    ):
        html = html.replace(path, path.replace("/texas/austin", f"/california/{city}"))

    html = html.replace("/living/lifestyle/comfortable-salary/texas/austin", hub)

    html = html.replace(
        f'<li><a href="{hub}">Austin</a></li>\n            <li aria-current="page">',
        f'<li><a href="{CA_STATE_HUB}">California</a></li>\n            <li><a href="{hub}">{name}</a></li>\n            <li aria-current="page">',
    )
    html = html.replace(
        f'"position": 3, "name": "Austin", "item": "https://www.incomeclaritylab.com{hub}"',
        f'"position": 3, "name": "California", "item": "https://www.incomeclaritylab.com{CA_STATE_HUB}"',
    )
    html = html.replace(
        f'"position": 4, "name": "$100,000 in Austin"',
        f'"position": 5, "name": "{sal} in {name}"',
    )
    html = html.replace(
        f'"position": 4, "name": "$150,000 in Austin"',
        f'"position": 5, "name": "{sal} in {name}"',
    )

    replacements = [
        ("Austin salary scenario", f"{name} salary scenario"),
        ("Live in Austin?", f"Live in {name}?"),
        ("enough to live in Austin", f"enough to live in {name}"),
        ("Enough to Live in Austin", f"Enough to Live in {name}"),
        ("Live Comfortably in Austin", f"Live Comfortably in {name}"),
        (" to live in Austin ", f" to live in {name} "),
        (" in Austin —", f" in {name} —"),
        (" in Austin after", f" in {name} after"),
        (" in Austin,", f" in {name},"),
        (" in Austin.", f" in {name}."),
        (" in Austin in 2026", f" in {name} in 2026"),
        (" in Austin?", f" in {name}?"),
        ("support in Austin", f"support in {name}"),
        ("create in Austin?", f"create in {name}?"),
        ("$100,000 in Austin", f"$100,000 in {name}"),
        ("$150,000 in Austin", f"$150,000 in {name}"),
        ("$100k in Austin", f"$100k in {name}"),
        ("$150k in Austin", f"$150k in {name}"),
        ("$200k in Austin", f"$200k in {name}"),
        ("Austin salary calculator", f"{name} salary calculator"),
        ("Full Austin calculator", f"Full {name} calculator"),
        ("Know your real number in Austin", f"Know your real number in {name}"),
        ("on our Austin calculator.", f"on our {name} calculator."),
        ("Rent vs Buy Austin", f"Rent vs Buy {name}"),
        ("Cost of Living Austin", f"Cost of Living {name}"),
        ("Moving to Austin Calculator", f"Moving to {name} Calculator"),
        ("How Much House Can I Afford in Austin →", f"How Much House Can I Afford in {name} →"),
        ("Texas's no state income tax boosting take-home", f"California's higher wages partially offset state tax in {name}"),
    ]
    for old, new in replacements:
        html = html.replace(old, new)

    return html


AUSTIN_DALLAS_FAQ = (
    "Austin rent runs higher than Dallas on average, but both cities have no state income tax. "
    "At $100k, Dallas often feels very comfortable while Austin lands at comfortable with slightly less housing flexibility."
)
AUSTIN_DALLAS_FAQ_TAX = (
    "Austin rent runs higher than Dallas on average, but both cities have California state income tax (up to 13.3%). "
    "At $100k, Dallas often feels very comfortable while Austin lands at comfortable with slightly less housing flexibility."
)


def patch_ca_refs(html: str, cfg: dict) -> str:
    name = cfg["name"]
    html = html.replace("Austin Compared With Other Cities", f"{name} Compared With Other Cities")
    html = html.replace(
        "At $100k, Austin is comfortable — but the same salary stretches differently elsewhere.",
        f"At $100k, {name} is {cfg['100k_city_row'].lower()} — but the same salary stretches differently across California.",
    )
    html = html.replace("Can I buy a house in Austin on $100k?", f"Can I buy a house in {name} on $100k?")
    html = html.replace("Austin-specific home price and mortgage ranges.", f"{name}-specific home price and mortgage ranges.")
    html = html.replace("Austin stops feeling like a tradeoff city", f"{name} opens real financial flexibility")
    html = html.replace("Austin's median household income", f"{name}'s median household income")
    html = html.replace("in the Austin metro", f"in the {name} metro")
    html = html.replace("central Austin while still saving", f"desirable {name} neighborhoods while still saving")
    html = html.replace("central Austin on one income", f"central {name} on one income")
    html = html.replace("Can You Buy a Home in Austin on $150k?", f"Can You Buy a Home in {name} on $150k?")
    html = html.replace("Can You Buy a Home in Austin on $200k?", f"Can You Buy a Home in {name} on $200k?")
    html = html.replace("Austin vs Other Cities on $150k", f"{name} vs Other Cities on $150k")
    html = html.replace("Austin vs Other Cities on $200k", f"{name} vs Other Cities on $200k")
    html = html.replace("$150k stretches furthest in Texas", f"$200k stretches furthest in Texas and inland California")
    html = html.replace("Most people earning $150k are not struggling", "Most people earning $200k are not struggling")
    html = html.replace("even at $150k.", "even at $200k.")
    html = html.replace("one $150k earner can support", "one $200k earner can support")
    html = html.replace("It sits well above Austin's median household income", f"It sits well above {name}'s median household income")
    return html


def rebuild_ca_compare_200k(html: str, cfg: dict) -> str:
    slug = cfg["slug"]
    rows = [
        ("los-angeles", "Los Angeles", "Very Comfortable", slug == "los-angeles"),
        ("san-diego", "San Diego", "Very Comfortable", slug == "san-diego"),
        ("san-francisco", "San Francisco", "Comfortable", slug == "san-francisco"),
    ]
    body = []
    for city_slug, city_name, label, here in rows:
        city_hub = f"{CA_STATE_HUB}/{city_slug}"
        cell = f"<strong>{label}</strong> (you are here)" if here else label
        body.append(
            f'              <tr>\n'
            f'                <th scope="row"><a href="{city_hub}">{city_name}</a></th>\n'
            f"                <td>{cell}</td>\n"
            f"              </tr>"
        )
    body.append(
        f'              <tr>\n'
        f'                <th scope="row"><a href="{AUSTIN_HUB}">Austin (TX)</a></th>\n'
        f"                <td>High Flexibility</td>\n"
        f"              </tr>"
    )
    pattern = re.compile(
        r"<caption>Lifestyle at \$200,000 across selected cities</caption>.*?<tbody>\n.*?</tbody>",
        re.DOTALL,
    )
    replacement = (
        f"<caption>Lifestyle at $200,000 across selected cities</caption>\n"
        f"            <thead>\n"
        f"              <tr><th scope=\"col\">City</th><th scope=\"col\">Lifestyle on $200k</th></tr>\n"
        f"            </thead>\n"
        f"            <tbody>\n" + "\n".join(body) + "\n            </tbody>"
    )
    if pattern.search(html):
        return pattern.sub(replacement, html, count=1)
    pattern2 = re.compile(
        r"<caption>Lifestyle at \$150,000 across selected cities</caption>.*?<tbody>\n.*?</tbody>",
        re.DOTALL,
    )
    return pattern2.sub(replacement, html, count=1)


def adapt_cta(html: str, cfg: dict) -> str:
    html = re.sub(
        r'(<a href=")[^"]+(">Compare )(?:Dallas|Houston|Austin \(TX\))(</a>)',
        rf"\1{AUSTIN_HUB}\2Austin (TX)\3",
        html,
        count=1,
    )
    html = html.replace(
        '<a href="/living/housing/cost-of-living-by-city/texas/austin">Cost of living detail</a>',
        f'<a href="/living/housing/cost-of-living-by-city/california/{cfg["slug"]}">Cost of living detail</a>',
    )
    return html


def rebuild_ca_compare_100k(html: str, cfg: dict) -> str:
    name = cfg["name"]
    hub = cfg["hub"]
    slug = cfg["slug"]
    rows = [
        ("los-angeles", "Los Angeles", "Moderate", slug == "los-angeles"),
        ("san-diego", "San Diego", "Moderate–Comfortable", slug == "san-diego"),
        ("san-francisco", "San Francisco", "Challenging", slug == "san-francisco"),
    ]
    body = []
    for city_slug, city_name, label, here in rows:
        city_hub = f"{CA_STATE_HUB}/{city_slug}"
        cell = f"<strong>{label}</strong> (you are here)" if here else label
        body.append(
            f'              <tr>\n'
            f'                <th scope="row"><a href="{city_hub}">{city_name}</a></th>\n'
            f"                <td>{cell}</td>\n"
            f"              </tr>"
        )
    body.append(
        f'              <tr>\n'
        f'                <th scope="row"><a href="{AUSTIN_HUB}">Austin (TX)</a></th>\n'
        f"                <td>{cfg['100k_austin_row']}</td>\n"
        f"              </tr>"
    )
    pattern = re.compile(
        r"<caption>Lifestyle at \$100,000 across selected cities</caption>.*?<tbody>\n.*?</tbody>",
        re.DOTALL,
    )
    replacement = (
        f"<caption>Lifestyle at $100,000 across selected cities</caption>\n"
        f"            <thead>\n"
        f"              <tr><th scope=\"col\">City</th><th scope=\"col\">Lifestyle on $100k</th></tr>\n"
        f"            </thead>\n"
        f"            <tbody>\n" + "\n".join(body) + "\n            </tbody>"
    )
    return pattern.sub(replacement, html, count=1)


def rebuild_ca_compare_150k(html: str, cfg: dict) -> str:
    slug = cfg["slug"]
    rows = [
        ("los-angeles", "Los Angeles", "Comfortable", slug == "los-angeles"),
        ("san-diego", "San Diego", "Comfortable", slug == "san-diego"),
        ("san-francisco", "San Francisco", "Moderate–Comfortable", slug == "san-francisco"),
    ]
    body = []
    for city_slug, city_name, label, here in rows:
        city_hub = f"{CA_STATE_HUB}/{city_slug}"
        cell = f"<strong>{label}</strong> (you are here)" if here else label
        body.append(
            f'              <tr>\n'
            f'                <th scope="row"><a href="{city_hub}">{city_name}</a></th>\n'
            f"                <td>{cell}</td>\n"
            f"              </tr>"
        )
    body.append(
        f'              <tr>\n'
        f'                <th scope="row"><a href="{AUSTIN_HUB}">Austin (TX)</a></th>\n'
        f"                <td>{cfg['150k_austin_row']}</td>\n"
        f"              </tr>"
    )
    pattern = re.compile(
        r"<caption>Lifestyle at \$150,000 across selected cities</caption>.*?<tbody>\n.*?</tbody>",
        re.DOTALL,
    )
    replacement = (
        f"<caption>Lifestyle at $150,000 across selected cities</caption>\n"
        f"            <thead>\n"
        f"              <tr><th scope=\"col\">City</th><th scope=\"col\">Lifestyle on $150k</th></tr>\n"
        f"            </thead>\n"
        f"            <tbody>\n" + "\n".join(body) + "\n            </tbody>"
    )
    return pattern.sub(replacement, html, count=1)


def rebuild_related_scenarios(html: str, cfg: dict, tier: str) -> str:
    hub = cfg["hub"]
    name = cfg["name"]
    slug = cfg["slug"]
    cards = {
        "100k": (
            ("150k", "Very comfortable for singles — homeownership math opens up."),
            ("200k", "High flexibility — family budgets and wealth building."),
        ),
        "150k": (
            ("100k", "Moderate tier — tighter rent and savings margins after CA tax."),
            ("200k", "High flexibility — premium housing and aggressive investing."),
        ),
        "200k": (
            ("100k", "Entry six-figure tier — affordability focus after state tax."),
            ("150k", "Comfortable tier — solid buffer for couples and families."),
        ),
    }
    other = cards[tier]
    grid = []
    for sal, desc in other:
        sal_label = {"100k": "$100k", "150k": "$150k", "200k": "$200k"}[sal]
        grid.append(
            f'          <a class="ss-related-card" href="{hub}/is-{sal}-enough-to-live-in-{slug}">\n'
            f"            <h3>Is {sal_label} Enough to Live in {name}?</h3>\n"
            f"            <p>{desc}</p>\n"
            f"            <span>Read ${sal} scenario →</span>\n"
            f"          </a>"
        )
    grid.append(
        f'          <a class="ss-related-card" href="{hub}">\n'
        f"            <h3>{name} Comfortable Salary Guide</h3>\n"
        f"            <p>Full tiers, calculator, and local cost breakdown.</p>\n"
        f"            <span>Open guide →</span>\n"
        f"          </a>"
    )
    pattern = re.compile(r'<div class="ss-related-grid">\n.*?</div>\n      </div>\n    </section>\n\n    <section class="cs-band" id="cs-faq">', re.DOTALL)
    block = (
        '<div class="ss-related-grid">\n' + "\n".join(grid) + "\n        </div>\n"
        "      </div>\n    </section>\n\n    <section class=\"cs-band\" id=\"cs-faq\">"
    )
    return pattern.sub(block, html, count=1)


def adapt_100k(html: str, cfg: dict) -> str:
    name = cfg["name"]
    hub = cfg["hub"]
    slug = cfg["slug"]
    rent_low = cfg["rent_low_vs_100k"]
    rent_100 = cfg["rent_100k"]
    rent_150, rent_200 = cfg["rent_100_vs_150"]

    html = html.replace("~$6,200/month", cfg["take_home_100k"])
    html = html.replace("Lifestyle Score: Comfortable", f"Lifestyle Score: {cfg['score_100k']}")
    html = html.replace("<li>Single Adult</li>", f'<li class="{cfg["check_100k_single"]}">{cfg["check_100k_single_label"]}</li>')
    html = html.replace("<li>Couple</li>", f'<li class="{cfg["check_100k_couple"]}">{cfg["check_100k_couple_label"]}</li>')

    html = html.replace(
        "What Changes Between $75k and $100k?",
        "What Changes Between Lower Salaries and $100k?",
    )
    html = html.replace(
        f'<a href="{hub}/is-75k-enough-to-live-in-{slug}">$75k Austin scenario</a>',
        f'<a href="{hub}#cs-calc">{name} comfortable salary guide</a>',
    )
    html = html.replace("How $75k and $100k compare in Austin", f"How lower salaries and $100k compare in {name}")
    html = html.replace("<td>$1,700</td><td>$2,300</td>", f"<td>{_fmt(rent_low)}</td><td>{_fmt(rent_100)}</td>")
    html = html.replace("The $100k Lifestyle in Austin", f"The $100k Lifestyle in {name}")
    html = html.replace("$325k–$425k", cfg["home_100k"])
    html = html.replace("$2,100–$2,600/mo", cfg["home_100k_mortgage"])
    html = html.replace(
        "a 3BR in Cedar Park, Round Rock, or Pflugerville ($2,200–$2,800)",
        f"a 3BR in {cfg['suburbs_family']} ($2,800–$3,800)",
    )
    html = html.replace(
        "family comfortable in Austin lands near $145k",
        f"family comfortable in {name} lands near {_fmt(cfg['family_comfortable'])}",
    )
    html = rebuild_ca_compare_100k(html, cfg)
    html = html.replace("Is Austin expensive compared to Dallas?", cfg["100k_faq_compare_q"])
    html = html.replace(AUSTIN_DALLAS_FAQ, cfg["100k_faq_compare"])
    html = html.replace(AUSTIN_DALLAS_FAQ_TAX, cfg["100k_faq_compare"])
    html = html.replace(
        "Yes — $100,000 sits above the metro median household income and clears our comfortable tier for single adults.",
        f"At $100k in {name}, singles often land near or below our {_fmt(cfg['single_comfortable'])} comfortable target after California state tax.",
    )
    html = html.replace("typical affordability lands in the $325k–$425k range", f"typical affordability lands in the {cfg['home_100k']} range")
    html = html.replace(
        f'<a href="{hub}/is-75k-enough-to-live-in-{slug}">\n            <h3>Is $75k Enough to Live in {name}?</h3>',
        f'<a href="{hub}/is-150k-enough-to-live-in-{slug}">\n            <h3>Is $150k Enough to Live in {name}?</h3>',
    )
    html = html.replace("Affordability focus — tighter rent and savings margins.", "Homeownership math and wealth building opens up.")
    html = html.replace("Read $75k scenario →", "Read $150k scenario →")
    html = html.replace(
        f'<a href="{hub}/is-150k-enough-to-live-in-{slug}">\n            <h3>Is $150k Enough to Live in {name}?</h3>\n            <p>High flexibility',
        f'<a href="{hub}/is-200k-enough-to-live-in-{slug}">\n            <h3>Is $200k Enough to Live in {name}?</h3>\n            <p>High flexibility',
    )
    html = html.replace("Read $150k scenario →", "Read $200k scenario →", 1)
    html = html.replace(
        f'<a href="{hub}/is-100k-enough-to-live-in-{slug}">$100k in {name} →</a>',
        f'<a href="{hub}/is-150k-enough-to-live-in-{slug}">$150k in {name} →</a>',
    )
    html = html.replace(
        f'<a href="{hub}/is-150k-enough-to-live-in-{slug}">$150k in {name} →</a>',
        f'<a href="{hub}/is-200k-enough-to-live-in-{slug}">$200k in {name} →</a>',
    )
    html = rebuild_related_scenarios(html, cfg, "100k")
    html = patch_ca_refs(html, cfg)
    html = adapt_cta(html, cfg)
    return html


def adapt_150k(html: str, cfg: dict) -> str:
    name = cfg["name"]
    hub = cfg["hub"]
    slug = cfg["slug"]
    starter, move_up, luxury = cfg["home_150k_tiers"]

    html = html.replace("What Does $150k Actually Feel Like in Austin?", f"What Does $150k Actually Feel Like in {name}?")
    html = html.replace(f"At this income, {name} stops feeling like a tradeoff city.", f"At this income, {name} offers real flexibility — even with California state tax.")
    html = html.replace("Can You Buy a Home in Austin on $150k?", f"Can You Buy a Home in {name} on $150k?")
    html = html.replace("$350k–$450k", starter)
    html = html.replace("$500k–$650k", move_up)
    html = html.replace("$700k–$850k", luxury)
    html = html.replace("Home price feasibility on $150,000 in Austin", f"Home price feasibility on $150,000 in {name}")

    for price, label in cfg["home_150k_feasibility"]:
        html = html.replace(f"<th scope=\"row\">$400k</th><td><strong style=\"color:var(--ss-ok)\">Comfortable</strong></td>", f'<th scope="row">{price}</th><td><strong style="color:var(--ss-ok)">{label}</strong></td>', 1)
    html = html.replace("<th scope=\"row\">$600k</th><td><strong style=\"color:var(--ss-ok)\">Realistic</strong></td>", f'<th scope="row">{cfg["home_150k_feasibility"][1][0]}</th><td><strong style="color:var(--ss-ok)">{cfg["home_150k_feasibility"][1][1]}</strong></td>')
    html = html.replace("<th scope=\"row\">$800k</th><td>Possible with planning</td>", f'<th scope="row">{cfg["home_150k_feasibility"][2][0]}</th><td>{cfg["home_150k_feasibility"][2][1]}</td>')

    html = html.replace(
        "Westlake, Circle C, Mueller, or central 78704 — premium areas that feel out of reach at $75k–$100k.",
        f"{cfg['neighborhoods_premium']} — premium areas that feel out of reach at $100k.",
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
    html = rebuild_ca_compare_150k(html, cfg)
    html = html.replace(
        f"A snapshot of what this income unlocks in {name} — optimization decisions, not survival tradeoffs.",
        f"A snapshot of what this income unlocks in {name} — optimization decisions, not survival tradeoffs.",
    )
    html = html.replace("Can I buy a $600k home in Austin on $150k?", f"Can I buy a {cfg['home_150k_feasibility'][1][0]} home in {name} on $150k?")
    html = html.replace("enough for many $500k–$650k homes depending on rate and down payment.", f"enough for many {move_up} homes depending on rate and down payment.")
    html = html.replace("$150,000", "$150,000")
    html = html.replace("~$9,250/month", cfg["take_home_150k"])
    html = html.replace("Lifestyle Score: Very Comfortable", f"Lifestyle Score: {cfg['score_150k']}")
    html = html.replace(
        f'<a href="{hub}/is-75k-enough-to-live-in-{slug}">',
        f'<a href="{hub}/is-100k-enough-to-live-in-{slug}">',
    )
    html = html.replace("Is $75k Enough to Live in", "Is $100k Enough to Live in")
    html = html.replace("Affordability focus — essentials, rent math, and tight margins.", "Moderate tier — tighter margins after CA state tax.")
    html = html.replace("Read $75k scenario →", "Read $100k scenario →")
    html = rebuild_related_scenarios(html, cfg, "150k")
    html = patch_ca_refs(html, cfg)
    html = adapt_cta(html, cfg)
    return html


def adapt_200k(html: str, cfg: dict) -> str:
    html = adapt_150k(html, cfg)
    name = cfg["name"]
    hub = cfg["hub"]
    slug = cfg["slug"]
    starter, move_up, luxury = cfg["home_200k_tiers"]

    html = html.replace("is-150k-enough-to-live-in-" + slug, "is-200k-enough-to-live-in-" + slug)
    html = html.replace("$150,000", "$200,000")
    html = html.replace(" on $150k?", " on $200k?")
    html = html.replace(" on $150k ", " on $200k ")
    html = html.replace("At $150k ", "At $200k ")
    html = html.replace("At $150k,", "At $200k,")
    html = html.replace("$150k ", "$200k ")
    html = html.replace("$150k?", "$200k?")
    html = html.replace("$150k.", "$200k.")
    html = html.replace("$150k'", "$200k'")
    html = html.replace(">$150k<", ">$200k<")
    html = html.replace(
        "At $100k the focus is affordability. At $200k it is comfort. At $200k the focus is wealth acceleration",
        "At $100k the focus is affordability. At $150k it is comfort. At $200k the focus is wealth acceleration",
    )
    html = html.replace(f"Lifestyle Score: {cfg['score_150k']}", f"Lifestyle Score: {cfg['score_200k']}")
    html = html.replace(cfg["take_home_150k"], cfg["take_home_200k"])
    html = html.replace(cfg["home_150k_tiers"][0], starter)
    html = html.replace(cfg["home_150k_tiers"][1], move_up)
    html = html.replace(cfg["home_150k_tiers"][2], luxury)

    for i, (price, label) in enumerate(cfg["home_200k_feasibility"]):
        old = cfg["home_150k_feasibility"][i]
        html = html.replace(f'<th scope="row">{old[0]}</th>', f'<th scope="row">{price}</th>')
        if i < 2:
            html = html.replace(f">{old[1]}</strong></td>", f">{label}</strong></td>")
        else:
            html = html.replace(f">{old[0]}</th><td>{old[1]}</td>", f">{price}</th><td>{label}</td>")

    html = html.replace(
        f"{cfg['neighborhoods_premium']} — premium areas that feel out of reach at $100k.",
        f"{cfg['neighborhoods_premium']} — premium areas accessible at $200k with planning.",
    )
    html = html.replace(cfg["premium_rent_150k"], cfg["premium_rent_200k"])
    html = html.replace(
        f'<th scope="row"><a href="{hub}">{name}</a></th>\n                <td><strong>{cfg["150k_city_row"]}</strong> (you are here)</td>',
        f'<th scope="row"><a href="{hub}">{name}</a></th>\n                <td><strong>{cfg["200k_city_row"]}</strong> (you are here)</td>',
    )
    html = html.replace(
        f"Can I buy a {cfg['home_150k_feasibility'][1][0]} home in {name} on $150k?",
        f"Can I buy a {cfg['home_200k_feasibility'][1][0]} home in {name} on $200k?",
    )
    html = html.replace(
        f"enough for many {cfg['home_150k_tiers'][1]} homes depending on rate and down payment.",
        f"enough for many {move_up} homes depending on rate and down payment.",
    )
    html = html.replace(
        "At $150k you are choosing <em>how</em> to live well",
        "At $200k you are choosing <em>how</em> to live well",
    )
    html = html.replace(
        "At $75k the focus is survival. At $100k it is savings. At $150k the focus is wealth acceleration",
        "At $100k the focus is affordability. At $150k it is comfort. At $200k the focus is wealth acceleration",
    )
    html = html.replace("At $150k gross (~$9,250/month take-home)", f"At $200k gross ({cfg['take_home_200k']} take-home)")
    html = html.replace(
        "At $150k gross, the 28% housing rule allows roughly $3,500/month toward PITI — enough for many $500k–$650k homes depending on rate and down payment.",
        f"At $200k gross ({cfg['take_home_200k']} take-home), the 28% housing rule allows roughly $4,500/month toward PITI — enough for many {move_up} homes depending on rate and down payment.",
    )
    html = html.replace(
        f"At $200k gross, the 28% housing rule allows roughly $3,500/month toward PITI — enough for many {cfg['home_150k_tiers'][1]} homes depending on rate and down payment.",
        f"At $200k gross ({cfg['take_home_200k']} take-home), the 28% housing rule allows roughly $4,500/month toward PITI — enough for many {move_up} homes depending on rate and down payment.",
    )
    html = html.replace("At $75k the question is", "At $100k the question is")
    html = rebuild_ca_compare_200k(html, cfg)
    html = html.replace("Lifestyle on $150k", "Lifestyle on $200k")
    html = html.replace("Lifestyle at $150,000 across selected cities", "Lifestyle at $200,000 across selected cities")
    html = rebuild_related_scenarios(html, cfg, "200k")
    html = html.replace(
        f"Can I buy a {cfg['home_150k_feasibility'][1][0]} home in {name} on $200k?",
        f"Can I buy a {cfg['home_200k_feasibility'][1][0]} home in {name} on $200k?",
    )
    html = adapt_cta(html, cfg)
    return html


ADAPTERS = {"100k": adapt_100k, "150k": adapt_150k, "200k": adapt_200k}


def generate_page(city_slug: str, tier: str) -> str:
    cfg = CITY_CONFIG[city_slug]
    html = load_template(tier)
    html = apply_path_replacements(html, cfg, tier)
    html = ADAPTERS[tier](html, cfg)
    return html


def main() -> None:
    for city_slug in CITY_CONFIG:
        for tier in TIERS:
            slug = f"is-{tier}-enough-to-live-in-{city_slug}"
            path = OUT_BASE / city_slug / slug / "index.html"
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(generate_page(city_slug, tier), encoding="utf-8")
            print(f"  wrote {path.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
