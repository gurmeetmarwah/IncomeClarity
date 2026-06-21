#!/usr/bin/env python3
"""Generate FL / NY / IL city salary scenario pages ($80k / $100k / $150k) from Austin templates."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
AUSTIN_DIR = ROOT / "living" / "lifestyle" / "comfortable-salary" / "texas" / "austin"
OUT_BASE = ROOT / "living" / "lifestyle" / "comfortable-salary"

TIERS = ("80k", "100k", "150k")
TEMPLATE_TIER = {"80k": "75k", "100k": "100k", "150k": "150k"}

SALARY_MAP = {"80k": "$80,000", "100k": "$100,000", "150k": "$150,000"}


def _peer_hub(state: str, slug: str) -> str:
    return f"/living/lifestyle/comfortable-salary/{state}/{slug}"


def _cfg(
    *,
    state: str,
    state_name: str,
    slug: str,
    name: str,
    rent: int,
    single: int,
    couple: int,
    family: int,
    compare_name: str,
    compare_state: str,
    compare_slug: str,
    compare_80k: list[tuple[str, str, str, str, str]],
    compare_100k: list[tuple[str, str, str, str, str]],
    compare_150k: list[tuple[str, str, str, str, str]],
    **extra: object,
) -> dict:
    hub = f"/living/lifestyle/comfortable-salary/{state}/{slug}"
    state_hub = f"/living/lifestyle/comfortable-salary/{state}"
    return {
        "state": state,
        "state_name": state_name,
        "state_hub": state_hub,
        "name": name,
        "slug": slug,
        "hub": hub,
        "rent": rent,
        "single_comfortable": single,
        "couple_comfortable": couple,
        "family_comfortable": family,
        "compare_city_name": compare_name,
        "compare_hub": _peer_hub(compare_state, compare_slug),
        "compare_80k": compare_80k,
        "compare_100k": compare_100k,
        "compare_150k": compare_150k,
        **extra,
    }


CITY_CONFIG: dict[tuple[str, str], dict] = {
    ("florida", "miami"): _cfg(
        state="florida",
        state_name="Florida",
        slug="miami",
        name="Miami",
        rent=2200,
        single=100_000,
        couple=130_000,
        family=165_000,
        compare_name="Tampa",
        compare_state="florida",
        compare_slug="tampa",
        compare_80k=[
            ("florida", "miami", "Miami", "Moderate", "miami"),
            ("florida", "tampa", "Tampa", "Comfortable", "tampa"),
            ("florida", "orlando", "Orlando", "Comfortable", "orlando"),
        ],
        compare_100k=[
            ("florida", "miami", "Miami", "Moderate–Comfortable", "miami"),
            ("florida", "tampa", "Tampa", "Very Comfortable", "tampa"),
            ("florida", "orlando", "Orlando", "Very Comfortable", "orlando"),
        ],
        compare_150k=[
            ("florida", "miami", "Miami", "Comfortable", "miami"),
            ("florida", "tampa", "Tampa", "High Flexibility", "tampa"),
            ("florida", "orlando", "Orlando", "High Flexibility", "orlando"),
        ],
        take_home_80k="~$4,900–$5,200/month",
        take_home_100k="~$6,100–$6,500/month",
        take_home_150k="~$9,000–$9,500/month",
        score_80k="Moderate",
        score_100k="Comfortable",
        score_150k="Very Comfortable",
        rent_80_vs_100=(1900, 2400),
        rent_ranges={"studio": "~$1,500–$1,750", "1br": "~$2,000–$2,400", "2br": "~$2,500–$3,100"},
        home_80k="$275k–$375k",
        home_100k="$350k–$450k",
        home_100k_mortgage="$2,200–$2,800/mo",
        home_150k_tiers=("$425k–$550k", "$600k–$750k", "$800k–$950k"),
        home_150k_feasibility=(("$450k", "Comfortable"), ("$650k", "Realistic"), ("$850k", "Possible with planning")),
        neighborhoods_premium="Brickell, Coconut Grove, or Coral Gables",
        suburbs_family="Doral, Kendall, or Fort Lauderdale",
        premium_rent_150k="$3,200–$4,000/month",
        family_3br="$2,800–$3,600/month",
        k80_verdict_single="🟡 Yes for many singles — rent is the main squeeze.",
        k80_verdict_family="⚠️ Tight for families with children.",
        k80_lifestyle_single="Moderate–Comfortable",
        k80_lifestyle_downtown="Moderate",
        k80_salary_row="Moderate",
        k80_faq_rent_premium="$2,600",
        k80_faq_ladder="$50k is difficult for most households. $80k is moderate–comfortable for many singles in Miami. $100k is comfortable with savings room. $150k offers high flexibility including homeownership.",
        k100_faq_compare_q="Is Miami expensive compared to Tampa?",
        k100_faq_compare=(
            "Miami rent runs well above Tampa and Orlando, but all three have no state income tax. "
            "At $100k, Tampa and Orlando often feel very comfortable while Miami lands at moderate–comfortable."
        ),
        k100_city_blurb="At $100k, Miami is moderate–comfortable — but the same salary stretches further inland.",
        tax_blurb="Florida has no state income tax — take-home is higher than NY or IL at the same gross.",
    ),
    ("florida", "tampa"): _cfg(
        state="florida",
        state_name="Florida",
        slug="tampa",
        name="Tampa",
        rent=1650,
        single=80_000,
        couple=105_000,
        family=140_000,
        compare_name="Miami",
        compare_state="florida",
        compare_slug="miami",
        compare_80k=[
            ("florida", "tampa", "Tampa", "Comfortable", "tampa"),
            ("florida", "orlando", "Orlando", "Comfortable", "orlando"),
            ("florida", "miami", "Miami", "Moderate", "miami"),
        ],
        compare_100k=[
            ("florida", "tampa", "Tampa", "Very Comfortable", "tampa"),
            ("florida", "orlando", "Orlando", "Very Comfortable", "orlando"),
            ("florida", "miami", "Miami", "Moderate–Comfortable", "miami"),
        ],
        compare_150k=[
            ("florida", "tampa", "Tampa", "High Flexibility", "tampa"),
            ("florida", "orlando", "Orlando", "High Flexibility", "orlando"),
            ("florida", "miami", "Miami", "Comfortable", "miami"),
        ],
        take_home_80k="~$4,900–$5,200/month",
        take_home_100k="~$6,100–$6,500/month",
        take_home_150k="~$9,000–$9,500/month",
        score_80k="Comfortable",
        score_100k="Very Comfortable",
        score_150k="High Flexibility",
        rent_80_vs_100=(1450, 1850),
        rent_ranges={"studio": "~$1,050–$1,250", "1br": "~$1,450–$1,700", "2br": "~$1,800–$2,200"},
        home_80k="$225k–$300k",
        home_100k="$300k–$400k",
        home_100k_mortgage="$1,950–$2,400/mo",
        home_150k_tiers=("$325k–$425k", "$450k–$550k", "$600k–$700k"),
        home_150k_feasibility=(("$350k", "Comfortable"), ("$500k", "Realistic"), ("$650k", "Possible with planning")),
        neighborhoods_premium="Hyde Park, South Tampa, or Westshore",
        suburbs_family="Brandon, Wesley Chapel, or St. Petersburg",
        premium_rent_150k="$2,500–$3,200/month",
        family_3br="$2,100–$2,800/month",
        k80_verdict_single="🟢 Yes, for many single adults.",
        k80_verdict_family="⚠️ Tight for families with children.",
        k80_lifestyle_single="Comfortable",
        k80_lifestyle_downtown="Comfortable",
        k80_salary_row="Very Comfortable",
        k80_faq_rent_premium="$1,900",
        k80_faq_ladder="$50k is difficult for most households. $80k is comfortable for many singles in Tampa. $100k is very comfortable with strong savings room. $150k offers high flexibility including homeownership.",
        k100_faq_compare_q="Is Tampa cheaper than Miami?",
        k100_faq_compare=(
            "Tampa rent runs well below Miami with the same no state income tax advantage. "
            "At $100k, Tampa often feels very comfortable while Miami needs tighter budgeting on housing."
        ),
        k100_city_blurb="At $100k, Tampa is very comfortable — inland Florida stretches further than Miami.",
        tax_blurb="Florida has no state income tax — take-home is higher than NY or IL at the same gross.",
    ),
    ("florida", "orlando"): _cfg(
        state="florida",
        state_name="Florida",
        slug="orlando",
        name="Orlando",
        rent=1600,
        single=80_000,
        couple=105_000,
        family=135_000,
        compare_name="Tampa",
        compare_state="florida",
        compare_slug="tampa",
        compare_80k=[
            ("florida", "orlando", "Orlando", "Comfortable", "orlando"),
            ("florida", "tampa", "Tampa", "Comfortable", "tampa"),
            ("florida", "miami", "Miami", "Moderate", "miami"),
        ],
        compare_100k=[
            ("florida", "orlando", "Orlando", "Very Comfortable", "orlando"),
            ("florida", "tampa", "Tampa", "Very Comfortable", "tampa"),
            ("florida", "miami", "Miami", "Moderate–Comfortable", "miami"),
        ],
        compare_150k=[
            ("florida", "orlando", "Orlando", "High Flexibility", "orlando"),
            ("florida", "tampa", "Tampa", "High Flexibility", "tampa"),
            ("florida", "miami", "Miami", "Comfortable", "miami"),
        ],
        take_home_80k="~$4,900–$5,200/month",
        take_home_100k="~$6,100–$6,500/month",
        take_home_150k="~$9,000–$9,500/month",
        score_80k="Comfortable",
        score_100k="Very Comfortable",
        score_150k="High Flexibility",
        rent_80_vs_100=(1400, 1800),
        rent_ranges={"studio": "~$1,000–$1,200", "1br": "~$1,400–$1,650", "2br": "~$1,750–$2,100"},
        home_80k="$220k–$290k",
        home_100k="$290k–$380k",
        home_100k_mortgage="$1,900–$2,350/mo",
        home_150k_tiers=("$310k–$410k", "$430k–$530k", "$580k–$680k"),
        home_150k_feasibility=(("$330k", "Comfortable"), ("$480k", "Realistic"), ("$620k", "Possible with planning")),
        neighborhoods_premium="Winter Park, Lake Nona, or Thornton Park",
        suburbs_family="Oviedo, Kissimmee, or Clermont",
        premium_rent_150k="$2,400–$3,000/month",
        family_3br="$2,000–$2,700/month",
        k80_verdict_single="🟢 Yes, for many single adults.",
        k80_verdict_family="⚠️ More challenging for families with children.",
        k80_lifestyle_single="Comfortable",
        k80_lifestyle_downtown="Comfortable",
        k80_salary_row="Very Comfortable",
        k80_faq_rent_premium="$1,850",
        k80_faq_ladder="$50k is difficult for most households. $80k is comfortable for many singles in Orlando. $100k is very comfortable with savings room. $150k offers high flexibility including homeownership.",
        k100_faq_compare_q="Is Orlando cheaper than Miami?",
        k100_faq_compare=(
            "Orlando rent runs below Miami with no state income tax in either city. "
            "At $100k, Orlando and Tampa often feel very comfortable while Miami compresses housing headroom."
        ),
        k100_city_blurb="At $100k, Orlando is very comfortable — theme-park metro costs stay below Miami.",
        tax_blurb="Florida has no state income tax — take-home is higher than NY or IL at the same gross.",
    ),
    ("new-york", "new-york-city"): _cfg(
        state="new-york",
        state_name="New York",
        slug="new-york-city",
        name="New York City",
        rent=3400,
        single=140_000,
        couple=185_000,
        family=230_000,
        compare_name="Chicago",
        compare_state="illinois",
        compare_slug="chicago",
        compare_80k=[
            ("new-york", "new-york-city", "New York City", "Challenging", "new-york-city"),
            ("illinois", "chicago", "Chicago", "Comfortable", "chicago"),
            ("florida", "miami", "Miami", "Moderate", "miami"),
        ],
        compare_100k=[
            ("new-york", "new-york-city", "New York City", "Tight", "new-york-city"),
            ("illinois", "chicago", "Chicago", "Very Comfortable", "chicago"),
            ("florida", "miami", "Miami", "Moderate–Comfortable", "miami"),
        ],
        compare_150k=[
            ("new-york", "new-york-city", "New York City", "Moderate–Comfortable", "new-york-city"),
            ("illinois", "chicago", "Chicago", "High Flexibility", "chicago"),
            ("florida", "miami", "Miami", "Comfortable", "miami"),
        ],
        take_home_80k="~$4,600–$5,000/month",
        take_home_100k="~$5,700–$6,200/month",
        take_home_150k="~$8,400–$9,100/month",
        score_80k="Tight",
        score_100k="Moderate",
        score_150k="Comfortable",
        rent_80_vs_100=(2800, 3600),
        rent_ranges={"studio": "~$2,400–$2,900", "1br": "~$3,200–$3,800", "2br": "~$3,900–$4,800"},
        home_80k="$350k–$475k",
        home_100k="$450k–$600k",
        home_100k_mortgage="$3,000–$3,700/mo",
        home_150k_tiers=("$550k–$700k", "$750k–$950k", "$1M–$1.2M"),
        home_150k_feasibility=(("$575k", "Comfortable"), ("$800k", "Realistic"), ("$1.05M", "Possible with planning")),
        neighborhoods_premium="West Village, Brooklyn Heights, or Tribeca",
        suburbs_family="Jersey City, Hoboken, or outer borough neighborhoods",
        premium_rent_150k="$4,500–$5,800/month",
        family_3br="$3,800–$5,200/month",
        k80_verdict_single="⚠️ Tight for many singles after rent and city tax.",
        k80_verdict_family="❌ Very difficult for families at median rent.",
        k80_lifestyle_single="Tight",
        k80_lifestyle_downtown="Challenging",
        k80_salary_row="Challenging",
        k80_faq_rent_premium="$3,800",
        k80_faq_ladder="$50k is very difficult in NYC. $80k is tight for most singles after state and city tax. $100k is moderate with careful rent choices. $150k opens comfortable tier math for many households.",
        k100_faq_compare_q="Is $100k enough in New York City?",
        k100_faq_compare=(
            "$100k is moderate in NYC after state and city income tax and median rent near $3,400. "
            "The same salary often feels very comfortable in Chicago or Tampa with no Florida tax."
        ),
        k100_city_blurb="At $100k, NYC is tight to moderate — the same salary stretches much further in Chicago.",
        tax_blurb="New York State plus NYC city income tax reduce take-home — budget for both on gross offers.",
    ),
    ("illinois", "chicago"): _cfg(
        state="illinois",
        state_name="Illinois",
        slug="chicago",
        name="Chicago",
        rent=1850,
        single=85_000,
        couple=115_000,
        family=150_000,
        compare_name="New York City",
        compare_state="new-york",
        compare_slug="new-york-city",
        compare_80k=[
            ("illinois", "chicago", "Chicago", "Comfortable", "chicago"),
            ("new-york", "new-york-city", "New York City", "Challenging", "new-york-city"),
            ("florida", "tampa", "Tampa", "Very Comfortable", "tampa"),
        ],
        compare_100k=[
            ("illinois", "chicago", "Chicago", "Very Comfortable", "chicago"),
            ("new-york", "new-york-city", "New York City", "Tight", "new-york-city"),
            ("florida", "tampa", "Tampa", "Very Comfortable", "tampa"),
        ],
        compare_150k=[
            ("illinois", "chicago", "Chicago", "High Flexibility", "chicago"),
            ("new-york", "new-york-city", "New York City", "Moderate–Comfortable", "new-york-city"),
            ("florida", "tampa", "Tampa", "High Flexibility", "tampa"),
        ],
        take_home_80k="~$4,700–$5,000/month",
        take_home_100k="~$5,900–$6,300/month",
        take_home_150k="~$8,700–$9,300/month",
        score_80k="Comfortable",
        score_100k="Very Comfortable",
        score_150k="High Flexibility",
        rent_80_vs_100=(1600, 2100),
        rent_ranges={"studio": "~$1,150–$1,350", "1br": "~$1,600–$1,900", "2br": "~$2,000–$2,500"},
        home_80k="$240k–$320k",
        home_100k="$320k–$420k",
        home_100k_mortgage="$2,050–$2,550/mo",
        home_150k_tiers=("$350k–$450k", "$480k–$580k", "$650k–$780k"),
        home_150k_feasibility=(("$375k", "Comfortable"), ("$525k", "Realistic"), ("$700k", "Possible with planning")),
        neighborhoods_premium="Lincoln Park, Wicker Park, or River North",
        suburbs_family="Evanston, Oak Park, or Naperville",
        premium_rent_150k="$2,800–$3,500/month",
        family_3br="$2,400–$3,200/month",
        k80_verdict_single="🟢 Yes, for many single adults.",
        k80_verdict_family="⚠️ Tight for families with childcare.",
        k80_lifestyle_single="Comfortable",
        k80_lifestyle_downtown="Moderate–Comfortable",
        k80_salary_row="Comfortable",
        k80_faq_rent_premium="$2,200",
        k80_faq_ladder="$50k is difficult for most households. $80k is comfortable for many singles in Chicago. $100k is very comfortable with savings room. $150k offers high flexibility including homeownership.",
        k100_faq_compare_q="Is Chicago cheaper than New York City?",
        k100_faq_compare=(
            "Chicago rent runs well below NYC while both have state income tax — NYC adds city tax. "
            "At $100k, Chicago often feels very comfortable while NYC lands at moderate or tight."
        ),
        k100_city_blurb="At $100k, Chicago is very comfortable — Midwest rent beats NYC by a wide margin.",
        tax_blurb="Illinois flat state income tax reduces take-home — still usually better than NYC city tax stacks.",
    ),
}


def _fmt(n: int) -> str:
    return f"${n:,}"


def load_template(tier: str) -> str:
    src_tier = TEMPLATE_TIER[tier]
    path = AUSTIN_DIR / f"is-{src_tier}-enough-to-live-in-austin" / "index.html"
    if not path.is_file():
        raise FileNotFoundError(f"Template missing: {path}")
    return path.read_text(encoding="utf-8")


def normalize_salary_tier(html: str, tier: str) -> str:
    if tier != "80k":
        return html
    html = html.replace("is-75k-enough-to-live-in-", "is-80k-enough-to-live-in-")
    html = html.replace("$75,000", "$80,000")
    html = html.replace("$75k", "$80k")
    html = html.replace("Pre-filled for $80,000 in", "Pre-filled for $80,000 in")
    html = html.replace(
        "$50k is difficult for most households. $80k is comfortable for many singles. $100k is very comfortable for singles and solid for couples. $150k offers high flexibility including homeownership.",
        "$50k is difficult for most households. $80k is comfortable for many singles. $100k is very comfortable for singles and solid for couples. $150k offers high flexibility including homeownership.",
    )
    return html


def apply_path_replacements(html: str, cfg: dict, tier: str) -> str:
    city = cfg["slug"]
    name = cfg["name"]
    hub = cfg["hub"]
    state = cfg["state"]
    state_name = cfg["state_name"]
    state_hub = cfg["state_hub"]
    sal = SALARY_MAP[tier]

    for t in ("75k", "80k", "100k", "150k"):
        html = html.replace(f"is-{t}-enough-to-live-in-austin", f"is-{tier}-enough-to-live-in-{city}")

    for path in (
        "/living/housing/how-much-house-can-i-afford/texas/austin",
        "/living/housing/cost-of-living-by-city/texas/austin",
        "/living/housing/moving-cost-calculator/texas/austin",
    ):
        html = html.replace(path, path.replace("/texas/austin", f"/{state}/{city}"))

    html = html.replace("/living/lifestyle/comfortable-salary/texas/austin", hub)
    html = html.replace("/living/lifestyle/comfortable-salary/texas", state_hub)

    html = html.replace(
        f'<li><a href="{hub}">Austin</a></li>\n            <li aria-current="page">',
        f'<li><a href="{state_hub}">{state_name}</a></li>\n            <li><a href="{hub}">{name}</a></li>\n            <li aria-current="page">',
    )
    html = html.replace(
        f'"position": 3, "name": "Austin", "item": "https://www.incomeclaritylab.com{hub}"',
        f'"position": 3, "name": "{state_name}", "item": "https://www.incomeclaritylab.com{state_hub}"',
    )
    for old_sal in ("$75,000 in Austin", "$80,000 in Austin", "$100,000 in Austin", "$150,000 in Austin"):
        html = html.replace(
            f'"position": 4, "name": "{old_sal}"',
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
        ("$75,000 in Austin", f"$80,000 in {name}" if tier == "80k" else f"{sal} in {name}"),
        ("$80,000 in Austin", f"$80,000 in {name}"),
        ("$100,000 in Austin", f"$100,000 in {name}"),
        ("$150,000 in Austin", f"$150,000 in {name}"),
        ("$100k in Austin", f"$100k in {name}"),
        ("$150k in Austin", f"$150k in {name}"),
        ("Austin salary calculator", f"{name} salary calculator"),
        ("Full Austin calculator", f"Full {name} calculator"),
        ("Know your real number in Austin", f"Know your real number in {name}"),
        ("on our Austin calculator.", f"on our {name} calculator."),
        ("Rent vs Buy Austin", f"Rent vs Buy {name}"),
        ("Cost of Living Austin", f"Cost of Living {name}"),
        ("Moving to Austin Calculator", f"Moving to {name} Calculator"),
        ("How Much House Can I Afford in Austin →", f"How Much House Can I Afford in {name} →"),
        ("Austin-specific", f"{name}-specific"),
        ("Texas metros", f"{state_name} metros"),
        ("across Texas cities", f"across selected cities"),
        ("Other Texas Cities", "Other Cities"),
        ("Texas cities", "selected cities"),
        ("Compare Dallas", f"Compare {cfg['compare_city_name']}"),
    ]
    for old, new in replacements:
        html = html.replace(old, new)
    return html


def patch_refs(html: str, cfg: dict) -> str:
    name = cfg["name"]
    html = html.replace("Austin Compared With Other Cities", f"{name} Compared With Other Cities")
    html = html.replace(
        "At $100k, Austin is comfortable — but the same salary stretches differently elsewhere.",
        cfg["k100_city_blurb"],
    )
    html = html.replace("Can I buy a house in Austin on $100k?", f"Can I buy a house in {name} on $100k?")
    html = html.replace("in the Austin metro", f"in the {name} metro")
    html = html.replace("central Austin on one income", f"central {name} on one income")
    html = html.replace("Austin stops feeling like a tradeoff city", f"{name} opens real financial flexibility")
    html = html.replace("Austin's median household income", f"{name}'s median household income")
    html = html.replace("Austin Lifestyle", f"{name} Lifestyle")
    html = html.replace("$75k budgets", "$80k budgets")
    html = html.replace("than a $75k budget", "than an $80k budget")
    html = html.replace("from $75k budgets", "from $80k budgets")
    html = html.replace("At $75k the focus is affordability.", "At $80k the focus is affordability.")
    html = html.replace(
        "At $75k the focus is survival. At $100k it is savings. At $150k the focus is wealth acceleration",
        "At $80k the focus is affordability. At $100k it is savings. At $150k the focus is wealth acceleration",
    )
    html = html.replace("At $75k the question is", "At $80k the question is")
    html = html.replace('<th scope="col">$75k</th>', '<th scope="col">$80k</th>')
    return html


def _compare_rows(cfg: dict, peers: list[tuple[str, str, str, str, str]]) -> str:
    body = []
    for state, slug, label, score, here_slug in peers:
        cell = f"<strong>{score}</strong> (you are here)" if slug == cfg["slug"] and state == cfg["state"] else score
        body.append(
            f'              <tr>\n'
            f'                <th scope="row"><a href="{_peer_hub(state, slug)}">{label}</a></th>\n'
            f"                <td>{cell}</td>\n"
            f"              </tr>"
        )
    return "\n".join(body)


def rebuild_compare_80k(html: str, cfg: dict) -> str:
    tbody = _compare_rows(cfg, cfg["compare_80k"])
    pattern = r'(<section class="ss-band" id="texas-compare">.*?<tbody>)\s*.*?\s*(</tbody>)'
    replacement = rf"\1\n{tbody}\n            \2"
    html, count = re.subn(pattern, replacement, html, count=1, flags=re.DOTALL)
    if count == 0:
        raise ValueError(f"Could not rebuild 80k compare table for {cfg['name']}")
    html = html.replace("Comfort level on $75,000 across Texas cities", "Comfort level on $80,000 across selected cities")
    html = html.replace("Comfort level on $80,000 across Texas cities", "Comfort level on $80,000 across selected cities")
    html = html.replace("Comfort Level on $75k", "Comfort Level on $80k")
    html = html.replace("Comfort Level on $80k", "Comfort Level on $80k")
    return html


def rebuild_compare_100k(html: str, cfg: dict) -> str:
    tbody = _compare_rows(cfg, cfg["compare_100k"])
    pattern = re.compile(
        r"<caption>Lifestyle at \$100,000 across selected cities</caption>.*?<tbody>\n.*?</tbody>",
        re.DOTALL,
    )
    replacement = (
        "<caption>Lifestyle at $100,000 across selected cities</caption>\n"
        "            <thead>\n"
        '              <tr><th scope="col">City</th><th scope="col">Lifestyle on $100k</th></tr>\n'
        "            </thead>\n"
        f"            <tbody>\n{tbody}\n            </tbody>"
    )
    return pattern.sub(replacement, html, count=1)


def rebuild_compare_150k(html: str, cfg: dict) -> str:
    tbody = _compare_rows(cfg, cfg["compare_150k"])
    pattern = re.compile(
        r"<caption>Lifestyle at \$150,000 across selected cities</caption>.*?<tbody>\n.*?</tbody>",
        re.DOTALL,
    )
    if not pattern.search(html):
        pattern = re.compile(
            r'(<section class="ss-band ss-band--alt" id="city-compare">.*?<tbody>)\s*.*?\s*(</tbody>)',
            re.DOTALL,
        )
        return pattern.sub(rf"\1\n{tbody}\n            \2", html, count=1)
    replacement = (
        "<caption>Lifestyle at $150,000 across selected cities</caption>\n"
        "            <thead>\n"
        '              <tr><th scope="col">City</th><th scope="col">Lifestyle on $150k</th></tr>\n'
        "            </thead>\n"
        f"            <tbody>\n{tbody}\n            </tbody>"
    )
    return pattern.sub(replacement, html, count=1)


def rebuild_home_feasibility_150k(html: str, cfg: dict) -> str:
    rows = []
    for price, label in cfg["home_150k_feasibility"]:
        if label in ("Comfortable", "Realistic"):
            rows.append(
                f'              <tr><th scope="row">{price}</th>'
                f'<td><strong style="color:var(--ss-ok)">{label}</strong></td></tr>'
            )
        else:
            rows.append(f'              <tr><th scope="row">{price}</th><td>{label}</td></tr>')
    tbody = "\n".join(rows)
    pattern = r'(<section class="ss-band ss-band--alt" id="home-buying">.*?<tbody>)\s*.*?\s*(</tbody>)'
    replacement = rf"\1\n{tbody}\n            \2"
    html, count = re.subn(pattern, replacement, html, count=1, flags=re.DOTALL)
    if count == 0:
        raise ValueError(f"Could not rebuild home feasibility table for {cfg['name']}")
    return html


def rebuild_related_scenarios(html: str, cfg: dict, tier: str) -> str:
    hub = cfg["hub"]
    name = cfg["name"]
    slug = cfg["slug"]
    cards = {
        "80k": (
            ("100k", "Very comfortable for singles — homeownership math opens up."),
            ("150k", "High flexibility — family budgets and wealth building."),
        ),
        "100k": (
            ("80k", "Entry tier — tighter rent and savings margins."),
            ("150k", "High flexibility — premium housing and aggressive investing."),
        ),
        "150k": (
            ("80k", "Affordability focus — essentials and rent math."),
            ("100k", "Comfortable tier — solid buffer for couples and families."),
        ),
    }
    other = cards[tier]
    grid = []
    for sal, desc in other:
        sal_label = {"80k": "$80k", "100k": "$100k", "150k": "$150k"}[sal]
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
    pattern = re.compile(
        r'<div class="ss-related-grid">\n.*?</div>\n      </div>\n    </section>\n\n    <section class="cs-band" id="cs-faq">',
        re.DOTALL,
    )
    block = (
        '<div class="ss-related-grid">\n' + "\n".join(grid) + "\n        </div>\n"
        '      </div>\n    </section>\n\n    <section class="cs-band" id="cs-faq">'
    )
    return pattern.sub(block, html, count=1)


def adapt_cta(html: str, cfg: dict) -> str:
    compare = cfg["compare_city_name"]
    compare_hub = cfg["compare_hub"]
    html = re.sub(
        r'(<a href=")[^"]+(">Compare )(?:Dallas|Houston|Austin|Tampa|Miami|Orlando|Chicago|New York City)(</a>)',
        rf"\1{compare_hub}\2{compare}\3",
        html,
        count=1,
    )
    html = html.replace(
        f'<a href="/living/housing/cost-of-living-by-city/texas/austin">Cost of living detail</a>',
        f'<a href="/living/housing/cost-of-living-by-city/{cfg["state"]}/{cfg["slug"]}">Cost of living detail</a>',
    )
    return html


def adapt_80k(html: str, cfg: dict) -> str:
    name = cfg["name"]
    rent = cfg["rent"]
    hub = cfg["hub"]
    slug = cfg["slug"]
    ranges = cfg["rent_ranges"]
    expenses_low = rent + 1630
    expenses_high = rent + 1930

    html = html.replace("🟡 Yes, for many single adults.", cfg["k80_verdict_single"])
    html = html.replace("⚠️ More challenging for families with children.", cfg["k80_verdict_family"])
    html = html.replace('value="1700" min="500"', f'value="{rent}" min="500"')
    html = html.replace(
        'aria-label="Monthly cost breakdown: housing $1,700, utilities $180, groceries $450, transportation $450, healthcare $300, entertainment $250. Total estimated $3,300 to $4,000 per month."',
        f'aria-label="Monthly cost breakdown: housing ${rent:,}, utilities $180, groceries $450, transportation $450, healthcare $300, entertainment $250. Total estimated {_fmt(expenses_low)} to {_fmt(expenses_high)} per month."',
    )
    html = html.replace("<strong>$1,700</strong>", f"<strong>${rent:,}</strong>", 1)
    html = html.replace("<strong>$3,300 – $4,000</strong>", f"<strong>${expenses_low:,} – ${expenses_high:,}</strong>")
    html = html.replace("What Does Living in Austin Cost?", f"What Does Living in {name} Cost?")
    html = html.replace("Can You Afford Austin on $80k?", f"Can You Afford {name} on $80k?")
    html = html.replace("Can You Afford Austin on $75k?", f"Can You Afford {name} on $80k?")
    html = html.replace("~$1,250–$1,450", ranges["studio"])
    html = html.replace("~$1,650–$1,850", ranges["1br"])
    html = html.replace("~$2,000–$2,400", ranges["2br"])
    html = html.replace("$250k–$325k range", f"{cfg['home_80k']} range")
    html = html.replace("Salary comparison for Austin lifestyle tiers", f"Salary comparison for {name} lifestyle tiers")
    html = html.replace(
        "<td><strong>Comfortable</strong> (you are here)</td>",
        f"<td><strong>{cfg['k80_salary_row']}</strong> (you are here)</td>",
    )
    html = html.replace("Austin vs Other Cities", f"{name} vs Other Cities")
    html = rebuild_compare_80k(html, cfg)
    html = html.replace(
        f"Can I afford a $1,700 apartment on $80k in {name}?",
        f"Can I afford a {_fmt(rent)} apartment on $80k in {name}?",
    )
    html = html.replace(
        f"Can I afford a $1,700 apartment on $75k in {name}?",
        f"Can I afford a {_fmt(rent)} apartment on $80k in {name}?",
    )
    html = html.replace(
        "Yes — $1,700 rent is roughly 33–35% of estimated after-tax income, within common budgeting ranges. Downtown or premium units above $2,000 feel tighter on $75k.",
        f"Yes — {_fmt(rent)} rent is roughly 30–36% of estimated after-tax income, within common budgeting ranges. Premium units above {cfg['k80_faq_rent_premium']} feel tighter on $80k.",
    )
    html = html.replace(
        "$50k is difficult for most households. $80k is comfortable for many singles. $100k is very comfortable for singles and solid for couples. $150k offers high flexibility including homeownership.",
        cfg["k80_faq_ladder"],
    )
    html = html.replace(
        '<tr><th scope="row">Single downtown</th><td><span class="ss-tag ss-tag--moderate">Moderate</span></td></tr>',
        f'<tr><th scope="row">Single downtown</th><td><span class="ss-tag ss-tag--{"comfortable" if cfg["k80_lifestyle_downtown"] == "Comfortable" else "moderate"}">{cfg["k80_lifestyle_downtown"]}</span></td></tr>',
    )
    html = html.replace(
        '<tr><th scope="row">Single renter</th><td><span class="ss-tag ss-tag--comfortable">Comfortable</span></td></tr>',
        f'<tr><th scope="row">Single renter</th><td><span class="ss-tag ss-tag--{"comfortable" if "Comfortable" in cfg["k80_lifestyle_single"] else "moderate"}">{cfg["k80_lifestyle_single"]}</span></td></tr>',
    )
    html = html.replace("Same $80,000 salary stretches differently across Texas metros", f"Same $80,000 salary stretches differently across metros")
    html = rebuild_related_scenarios(html, cfg, "80k")
    html = patch_refs(html, cfg)
    html = adapt_cta(html, cfg)
    return html


def adapt_100k(html: str, cfg: dict) -> str:
    name = cfg["name"]
    hub = cfg["hub"]
    slug = cfg["slug"]
    rent_80, rent_100 = cfg["rent_80_vs_100"]

    html = html.replace("~$6,200/month", cfg["take_home_100k"])
    html = html.replace("Lifestyle Score: Comfortable", f"Lifestyle Score: {cfg['score_100k']}")
    html = html.replace(
        f'<a href="{hub}/is-75k-enough-to-live-in-{slug}">$75k {name} scenario</a>',
        f'<a href="{hub}/is-80k-enough-to-live-in-{slug}">$80k {name} scenario</a>',
    )
    html = html.replace("$75k Austin scenario", f"$80k {name} scenario")
    html = html.replace("What Changes Between $75k and $100k?", "What Changes Between $80k and $100k?")
    html = html.replace("How $75k and $100k compare in Austin", f"How $80k and $100k compare in {name}")
    html = html.replace("<td>$1,700</td><td>$2,300</td>", f"<td>${rent_80:,}</td><td>${rent_100:,}</td>")
    html = html.replace("The $100k Lifestyle in Austin", f"The $100k Lifestyle in {name}")
    html = html.replace("$325k–$425k", cfg["home_100k"])
    html = html.replace("$2,100–$2,600/mo", cfg["home_100k_mortgage"])
    html = html.replace(
        "a 3BR in Cedar Park, Round Rock, or Pflugerville ($2,200–$2,800)",
        f"a 3BR in {cfg['suburbs_family']} ($2,000–$3,200)",
    )
    html = html.replace(
        "family comfortable in Austin lands near $145k",
        f"family comfortable in {name} lands near {_fmt(cfg['family_comfortable'])}",
    )
    html = rebuild_compare_100k(html, cfg)
    html = html.replace("Is Austin expensive compared to Dallas?", cfg["k100_faq_compare_q"])
    html = html.replace(
        "Austin rent runs higher than Dallas on average, but both cities have no state income tax. At $100k, Dallas often feels very comfortable while Austin lands at comfortable with slightly less housing flexibility.",
        cfg["k100_faq_compare"],
    )
    html = html.replace(
        "Yes — $100,000 sits above the metro median household income and clears our comfortable tier for single adults.",
        f"At $100k in {name}, singles often land near our {_fmt(cfg['single_comfortable'])} comfortable target — {cfg['tax_blurb']}",
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
        f'<a href="{hub}/is-75k-enough-to-live-in-{slug}">\n            <h3>Is $75k Enough to Live in {name}?</h3>',
        f'<a href="{hub}/is-80k-enough-to-live-in-{slug}">\n            <h3>Is $80k Enough to Live in {name}?</h3>',
    )
    html = html.replace("Read $75k scenario →", "Read $80k scenario →")
    html = html.replace("Affordability focus — tighter rent and savings margins.", "Moderate tier — tighter margins on housing.")
    html = rebuild_related_scenarios(html, cfg, "100k")
    html = patch_refs(html, cfg)
    html = adapt_cta(html, cfg)
    return html


def adapt_150k(html: str, cfg: dict) -> str:
    name = cfg["name"]
    hub = cfg["hub"]
    slug = cfg["slug"]
    starter, move_up, luxury = cfg["home_150k_tiers"]

    html = html.replace("What Does $150k Actually Feel Like in Austin?", f"What Does $150k Actually Feel Like in {name}?")
    html = html.replace(
        f"At this income, Austin stops feeling like a tradeoff city.",
        f"At this income, {name} offers real flexibility — {cfg['tax_blurb']}",
    )
    html = html.replace("Can You Buy a Home in Austin on $150k?", f"Can You Buy a Home in {name} on $150k?")
    html = html.replace("$350k–$450k", starter)
    html = html.replace("$500k–$650k", move_up)
    html = html.replace("$700k–$850k", luxury)
    html = html.replace("Home price feasibility on $150,000 in Austin", f"Home price feasibility on $150,000 in {name}")
    html = html.replace("~$9,250/month", cfg["take_home_150k"])
    html = html.replace("Lifestyle Score: Very Comfortable", f"Lifestyle Score: {cfg['score_150k']}")
    html = rebuild_home_feasibility_150k(html, cfg)
    html = html.replace(
        "Westlake, Circle C, Mueller, or central 78704 — premium areas that feel out of reach at $75k–$100k.",
        f"{cfg['neighborhoods_premium']} — premium areas that feel out of reach at $80k–$100k.",
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
    html = rebuild_compare_150k(html, cfg)
    html = html.replace(
        f"A snapshot of what this income unlocks in Austin — optimization decisions, not survival tradeoffs.",
        f"A snapshot of what this income unlocks in {name} — optimization decisions, not survival tradeoffs.",
    )
    html = html.replace(
        f"Is $150k a good household income in Austin?",
        f"Is $150k a good household income in {name}?",
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
    html = html.replace(
        f'<a href="{hub}/is-75k-enough-to-live-in-{slug}">',
        f'<a href="{hub}/is-80k-enough-to-live-in-{slug}">',
    )
    html = html.replace("Is $75k Enough to Live in", "Is $80k Enough to Live in")
    html = html.replace("Read $75k scenario →", "Read $80k scenario →")
    html = html.replace("Affordability focus — essentials, rent math, and tight margins.", "Entry tier — tighter margins on housing.")
    html = rebuild_related_scenarios(html, cfg, "150k")
    html = patch_refs(html, cfg)
    html = adapt_cta(html, cfg)
    return html


ADAPTERS = {"80k": adapt_80k, "100k": adapt_100k, "150k": adapt_150k}


def generate_page(state: str, city_slug: str, tier: str) -> str:
    cfg = CITY_CONFIG[(state, city_slug)]
    html = load_template(tier)
    html = normalize_salary_tier(html, tier)
    html = apply_path_replacements(html, cfg, tier)
    html = ADAPTERS[tier](html, cfg)
    return html


def main() -> None:
    for (state, city_slug) in CITY_CONFIG:
        for tier in TIERS:
            slug = f"is-{tier}-enough-to-live-in-{city_slug}"
            path = OUT_BASE / state / city_slug / slug / "index.html"
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(generate_page(state, city_slug, tier), encoding="utf-8")
            print(f"  wrote {path.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
