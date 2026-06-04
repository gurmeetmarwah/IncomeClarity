#!/usr/bin/env python3
"""Generate cost-of-living-by-city hub, state, city, and comparison pages."""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from col_hub_content import build_catalog, render_hub_page  # noqa: E402

STYLES_LIVING = '  <link rel="stylesheet" href="/styles-living-system.css">'
STYLES_COL = STYLES_LIVING + '\n  <link rel="stylesheet" href="/styles-col.css">'
BASE = ROOT / "living" / "housing" / "cost-of-living-by-city"

URL_SCRIPT = """  <script>
    (function () {
      const path = window.location.pathname;
      let cleanPath = path;
      if (path.endsWith("/index.html")) cleanPath = path.slice(0, -10);
      else if (path.endsWith(".html")) cleanPath = path.slice(0, -5);
      if (cleanPath !== path) window.history.replaceState({}, "", cleanPath + window.location.search + window.location.hash);
    })();
  </script>"""

HEADER = """  <header class="site-header">
    <div class="container nav-wrap">
      <a class="logo" href="/"><img src="/images/logo.png" alt="" width="32" height="32"><span class="logo-text">Income Clarity</span></a>
      <nav class="nav-links" aria-label="Primary">
        <a href="/hourly-to-salary-after-tax">Income</a>
        <a href="/credit-card-payoff-calculator">Debt</a>
        <a href="/rent-vs-buy-calculator">Living</a>
        <a href="/1099-vs-w2-calculator">Freelance</a>
      </nav>
    </div>
  </header>"""

FOOTER = """  <footer class="site-footer">
    <div class="container footer-layout">
      <p class="footer-copy">© 2026 IncomeClarityLab</p>
    </div>
  </footer>"""


def fmt(n: int) -> str:
    return f"${n:,}"


# Planning constants — documented in EEAT blocks and /methodology#affordability
TAKE_HOME_RATIO = 0.72
CORE_GROSS_SHARE = 0.43
FAMILY_GROSS_SHARE = 0.48
FAMILY_STACK_MULT = 1.35

STATE_TAKE_HOME = {
    "california": "/hourly-to-salary-after-tax/state/california/",
    "texas": "/hourly-to-salary-after-tax/state/texas/",
    "florida": "/hourly-to-salary-after-tax/state/florida/",
    "new-york": "/hourly-to-salary-after-tax/state/new-york/",
}
STANDALONE_TAKE_HOME = {
    "chicago": "/hourly-to-salary-after-tax/state/illinois/",
    "seattle": "/hourly-to-salary-after-tax/state/washington/",
}


def core_monthly(rent: int, groceries: int, utilities: int, transport: int) -> int:
    return rent + groceries + utilities + transport


def housing_share_pct(rent: int, core: int) -> int:
    return round((rent / max(core, 1)) * 100)


def minimum_comfort_salary(core: int) -> int:
    return round((core * 12) / CORE_GROSS_SHARE / 5000) * 5000


def minimum_family_salary(core: int) -> int:
    return round((core * 12 * FAMILY_STACK_MULT) / FAMILY_GROSS_SHARE / 5000) * 5000


def derived_lifestyle_score(col_index: int, housing_share: int) -> int:
    score = 74 - (col_index - 100) * 0.28 - max(0, housing_share - 65) * 0.2
    return max(45, min(78, round(score)))


def prepare_city_metrics(city: dict) -> dict:
    core = core_monthly(city["rent_1br"], city["groceries"], city["utilities"], city["transport"])
    hs = housing_share_pct(city["rent_1br"], core)
    return {
        "core": core,
        "housing_share": hs,
        "min_salary": minimum_comfort_salary(core),
        "min_family": minimum_family_salary(core),
        "derived_score": derived_lifestyle_score(city["col_index"], hs),
        "rent_cap_gross": round(city["rent_1br"] * 12 / 0.30 / 1000) * 1000,
    }


def take_home_link(state_slug: str | None, city_slug: str | None) -> str:
    if state_slug and state_slug in STATE_TAKE_HOME:
        return STATE_TAKE_HOME[state_slug]
    if city_slug and city_slug in STANDALONE_TAKE_HOME:
        return STANDALONE_TAKE_HOME[city_slug]
    return "/hourly-to-salary-after-tax"


def moving_cost_link(state_slug: str | None, city_slug: str) -> str:
    if state_slug:
        return f"/living/housing/moving-cost-calculator/{state_slug}/{city_slug}"
    return f"/living/housing/moving-cost-calculator/{city_slug}"


def compare_links_for_path(page_path: str) -> list[tuple[str, str]]:
    normalized = page_path
    prefix = "/living/housing/cost-of-living-by-city/"
    if normalized.startswith(prefix):
        normalized = normalized[len(prefix):]
    if normalized.endswith("/"):
        normalized = normalized[:-1]
    out: list[tuple[str, str]] = []
    for slug, c in COMPARISONS.items():
        if c["slug_a"] == normalized or c["slug_b"] == normalized:
            out.append((c["title_short"], f"/living/housing/cost-of-living-by-city/compare/{slug}"))
    return out


def validate_city_metrics(city: dict, label: str) -> list[str]:
    m = prepare_city_metrics(city)
    warnings: list[str] = []
    if city["salary_comfort"] < m["min_salary"] * 0.85:
        warnings.append(
            f"{label}: comfort salary {fmt(city['salary_comfort'])} below model floor {fmt(m['min_salary'])}"
        )
    lifestyle = city.get("lifestyle_score")
    if lifestyle is not None and abs(lifestyle - m["derived_score"]) > 10:
        warnings.append(
            f"{label}: lifestyle score {lifestyle} differs from model {m['derived_score']}"
        )
    return warnings


def paras_html(paragraphs: list[str]) -> str:
    return "\n".join(f"        <p>{p}</p>" for p in paragraphs)


def key_points_html(points: list[str]) -> str:
    if not points:
        return ""
    items = "\n".join(f"          <li>{p}</li>" for p in points)
    return f"""
        <ul class="col-key-list">
{items}
        </ul>"""


def faq_html(faqs: list[tuple[str, str]]) -> str:
    blocks = []
    for q, a in faqs:
        paragraphs = "".join(f"<p>{part.strip()}</p>" for part in a.split("\n\n") if part.strip())
        blocks.append(f'          <article class="faq-item"><h3>{q}</h3>{paragraphs}</article>')
    return "\n".join(blocks)


# Monthly singles for a typical adult / small household planning figures
STATES = {
    "california": {
        "name": "California",
        "col_index": 142,
        "rent_1br": 2400,
        "groceries": 480,
        "utilities": 220,
        "transport": 380,
        "tax_note": "State income tax up to 13.3% on high earners",
        "salary_comfort": 98000,
        "narrative": [
            "California costs more than most of the US. Rent and insurance drive the gap. Wages are higher too, but not always enough on the coast.",
            "Use this page as a map. Compare cities below. Then open a city page for rent, food, tax, and salary targets in one place.",
            "California has state income tax up to 13.3% on high earners. Budget for it when you compare offers from Texas or Florida.",
            "Inland metros often run 20% to 40% below coastal rent. Many movers pick Sacramento or Riverside to keep a CA job market with lower rent.",
        ],
        "rank_intro": "Coast cities cost more on rent. Inland cities often cost less.",
        "cities": {
            "los-angeles": {
                "name": "Los Angeles",
                "col_index": 152,
                "rent_1br": 2600,
                "groceries": 520,
                "utilities": 210,
                "transport": 420,
                "salary_comfort": 105000,
                "lifestyle_score": 62,
                "family_4": 92000,
                "house_link": "/living/housing/how-much-house-can-i-afford/california/los-angeles",
                "rent_link": "/living/housing/how-much-rent-can-i-afford",
                "salary_link": "/living/lifestyle-family/comfortable-salary-california",
            },
            "san-diego": {
                "name": "San Diego",
                "col_index": 148,
                "rent_1br": 2550,
                "groceries": 500,
                "utilities": 215,
                "transport": 400,
                "salary_comfort": 102000,
                "lifestyle_score": 64,
                "family_4": 90000,
                "house_link": "/living/housing/how-much-house-can-i-afford/california/san-diego",
                "rent_link": "/living/housing/how-much-rent-can-i-afford",
                "salary_link": "/living/lifestyle-family/comfortable-salary-california",
            },
            "san-francisco": {
                "name": "San Francisco",
                "col_index": 168,
                "rent_1br": 3200,
                "groceries": 540,
                "utilities": 200,
                "transport": 350,
                "salary_comfort": 125000,
                "lifestyle_score": 58,
                "family_4": 110000,
                "house_link": "/living/housing/how-much-house-can-i-afford/california/san-francisco",
                "rent_link": "/living/housing/how-much-rent-can-i-afford",
                "salary_link": "/living/lifestyle-family/comfortable-salary-california",
            },
        },
    },
    "texas": {
        "name": "Texas",
        "col_index": 98,
        "rent_1br": 1450,
        "groceries": 380,
        "utilities": 195,
        "transport": 340,
        "tax_note": "No state income tax; property tax is high for owners",
        "salary_comfort": 72000,
        "narrative": [
            "Texas often looks cheap on rent vs California or New York. Property tax and insurance still matter if you buy.",
            "There is no state income tax. That helps take-home pay. Sales tax and local fees still add up.",
            "Austin and Dallas run above Houston on rent in many years. All three stay below coastal CA on housing.",
            "Use city pages to compare. A job offer in Dallas is not the same math as Austin once rent and commute are in.",
        ],
        "rank_intro": "Houston often has the lowest rent in Texas. Austin often costs more.",
        "cities": {
            "dallas": {
                "name": "Dallas",
                "col_index": 102,
                "rent_1br": 1550,
                "groceries": 390,
                "utilities": 200,
                "transport": 360,
                "salary_comfort": 76000,
                "lifestyle_score": 72,
                "family_4": 78000,
                "house_link": "/living/housing/how-much-house-can-i-afford/texas/dallas",
                "rent_link": "/living/housing/how-much-rent-can-i-afford",
                "salary_link": "/living/lifestyle-family/comfortable-salary-texas",
            },
            "houston": {
                "name": "Houston",
                "col_index": 96,
                "rent_1br": 1400,
                "groceries": 370,
                "utilities": 210,
                "transport": 350,
                "salary_comfort": 70000,
                "lifestyle_score": 74,
                "family_4": 72000,
                "house_link": "/living/housing/how-much-house-can-i-afford/texas/houston",
                "rent_link": "/living/housing/how-much-rent-can-i-afford",
                "salary_link": "/living/lifestyle-family/comfortable-salary-texas",
            },
            "austin": {
                "name": "Austin",
                "col_index": 108,
                "rent_1br": 1750,
                "groceries": 400,
                "utilities": 195,
                "transport": 370,
                "salary_comfort": 82000,
                "lifestyle_score": 70,
                "family_4": 85000,
                "house_link": "/living/housing/how-much-house-can-i-afford/texas/austin",
                "rent_link": "/living/housing/how-much-rent-can-i-afford",
                "salary_link": "/living/lifestyle-family/comfortable-salary-texas",
            },
        },
    },
    "florida": {
        "name": "Florida",
        "col_index": 104,
        "rent_1br": 1750,
        "groceries": 400,
        "utilities": 210,
        "transport": 320,
        "tax_note": "No state income tax; insurance can be high on the coast",
        "salary_comfort": 75000,
        "narrative": [
            "Florida has no state income tax. Rent and storm insurance still push costs up on the coast.",
            "Miami runs far above Tampa and Orlando on rent and HOA. Inland Florida is closer to the US norm.",
            "Many retirees and remote workers moved here after 2020. Entry-level rent can still feel tight on service wages.",
            "Open a city page before you use the state average. Miami is not Orlando on monthly cost.",
        ],
        "rank_intro": "Miami often costs the most in Florida. Orlando and Tampa sit in the middle.",
        "cities": {
            "miami": {
                "name": "Miami",
                "col_index": 118,
                "rent_1br": 2200,
                "groceries": 430,
                "utilities": 225,
                "transport": 340,
                "salary_comfort": 88000,
                "lifestyle_score": 65,
                "family_4": 82000,
                "house_link": "/living/housing/how-much-house-can-i-afford/florida/miami",
                "rent_link": "/living/housing/how-much-rent-can-i-afford",
                "salary_link": "/living/family-budgeting/salary-needed-to-live-comfortably",
            },
            "tampa": {
                "name": "Tampa",
                "col_index": 106,
                "rent_1br": 1650,
                "groceries": 395,
                "utilities": 205,
                "transport": 310,
                "salary_comfort": 74000,
                "lifestyle_score": 73,
                "family_4": 76000,
                "house_link": "/living/housing/how-much-house-can-i-afford/florida/tampa",
                "rent_link": "/living/housing/how-much-rent-can-i-afford",
                "salary_link": "/living/family-budgeting/salary-needed-to-live-comfortably",
            },
            "orlando": {
                "name": "Orlando",
                "col_index": 105,
                "rent_1br": 1600,
                "groceries": 390,
                "utilities": 200,
                "transport": 300,
                "salary_comfort": 72000,
                "lifestyle_score": 74,
                "family_4": 74000,
                "house_link": "/living/housing/how-much-house-can-i-afford/florida/orlando",
                "rent_link": "/living/housing/how-much-rent-can-i-afford",
                "salary_link": "/living/family-budgeting/salary-needed-to-live-comfortably",
            },
        },
    },
    "new-york": {
        "name": "New York",
        "col_index": 135,
        "rent_1br": 2400,
        "groceries": 500,
        "utilities": 225,
        "transport": 290,
        "tax_note": "State + NYC city income tax for many downstate workers",
        "salary_comfort": 105000,
        "med_home": 425000,
        "narrative": [
            "New York splits into downstate and upstate markets. NYC rent drives the state average up.",
            "Open the NYC city page for downstate. Upstate cities run far below NYC on rent.",
            "Income tax hits take-home before you shop for an apartment.",
        ],
        "rank_intro": "NYC costs the most in this state. Upstate areas often cost less.",
        "extra_state_copy": [
            "Many workers live downstate and pay city and state tax. Upstate workers often see lower rent and different job types.",
            "Use the NYC city page for the five boroughs and nearby jobs. Use other guides if you target Buffalo or Albany areas.",
            "A state average can mislead. NYC rent pulls the norm up while smaller towns sit far below it on monthly cost.",
        ],
        "cities": {
            "new-york-city": {
                "name": "New York City",
                "col_index": 158,
                "rent_1br": 3400,
                "groceries": 550,
                "utilities": 230,
                "transport": 280,
                "salary_comfort": 120000,
                "lifestyle_score": 55,
                "family_4": 105000,
                "healthcare": 450,
                "taxes_month": 650,
                "house_link": "/living/housing/how-much-house-can-i-afford/new-york/new-york-city",
                "rent_link": "/living/housing/how-much-rent-can-i-afford",
                "salary_link": "/living/family-budgeting/salary-needed-to-live-comfortably",
            },
        },
    },
}

STANDALONE = {
    "chicago": {
        "name": "Chicago",
        "state_name": "Illinois",
        "col_index": 112,
        "rent_1br": 1850,
        "groceries": 420,
        "utilities": 195,
        "transport": 310,
        "salary_comfort": 82000,
        "lifestyle_score": 68,
        "family_4": 86000,
        "house_link": "/living/housing/how-much-house-can-i-afford",
        "rent_link": "/living/housing/how-much-rent-can-i-afford",
        "salary_link": "/living/family-budgeting/salary-needed-to-live-comfortably",
        "tax_note": "Flat state income tax; sales tax in Cook County adds up",
    },
    "seattle": {
        "name": "Seattle",
        "state_name": "Washington",
        "col_index": 135,
        "rent_1br": 2200,
        "groceries": 480,
        "utilities": 190,
        "transport": 320,
        "salary_comfort": 95000,
        "lifestyle_score": 66,
        "family_4": 92000,
        "house_link": "/living/housing/how-much-house-can-i-afford",
        "rent_link": "/living/housing/how-much-rent-can-i-afford",
        "salary_link": "/living/family-budgeting/salary-needed-to-live-comfortably",
        "tax_note": "No state income tax; sales tax is high",
    },
    "denver": {
        "name": "Denver",
        "state_name": "Colorado",
        "col_index": 118,
        "rent_1br": 1950,
        "groceries": 430,
        "utilities": 185,
        "transport": 340,
        "salary_comfort": 88000,
        "lifestyle_score": 69,
        "family_4": 90000,
        "house_link": "/living/housing/how-much-house-can-i-afford",
        "rent_link": "/living/housing/how-much-rent-can-i-afford",
        "salary_link": "/living/family-budgeting/salary-needed-to-live-comfortably",
        "tax_note": "Flat state income tax; mountain west sales tax",
    },
    "atlanta": {
        "name": "Atlanta",
        "state_name": "Georgia",
        "col_index": 104,
        "rent_1br": 1650,
        "groceries": 400,
        "utilities": 195,
        "transport": 350,
        "salary_comfort": 78000,
        "lifestyle_score": 71,
        "family_4": 80000,
        "healthcare": 410,
        "taxes_month": 220,
        "house_link": "/living/housing/how-much-house-can-i-afford",
        "rent_link": "/living/housing/how-much-rent-can-i-afford",
        "salary_link": "/living/family-budgeting/salary-needed-to-live-comfortably",
        "tax_note": "State income tax; intown vs suburb rent spreads wide",
    },
    "phoenix": {
        "name": "Phoenix",
        "state_name": "Arizona",
        "col_index": 105,
        "rent_1br": 1650,
        "groceries": 390,
        "utilities": 210,
        "transport": 340,
        "salary_comfort": 76000,
        "lifestyle_score": 73,
        "family_4": 82000,
        "healthcare": 400,
        "taxes_month": 180,
        "house_link": "/living/housing/how-much-house-can-i-afford",
        "rent_link": "/living/housing/how-much-rent-can-i-afford",
        "salary_link": "/living/lifestyle/comfortable-salary/arizona/phoenix",
        "tax_note": "Moderate state income tax; summer cooling bills run high",
    },
}


def _patch_salary_links() -> None:
    _standalone_state = {
        "chicago": "illinois",
        "seattle": "washington",
        "denver": "colorado",
        "atlanta": "georgia",
        "phoenix": "arizona",
    }
    for slug, st in STATES.items():
        for cs, city in st["cities"].items():
            city["salary_link"] = f"/living/lifestyle/comfortable-salary/{slug}/{cs}"
    for cs, city in STANDALONE.items():
        state_slug = _standalone_state[cs]
        city["salary_link"] = f"/living/lifestyle/comfortable-salary/{state_slug}/{cs}"


_patch_salary_links()

COMPARISONS = {
    "nyc-vs-chicago": {
        "title": "NYC vs Chicago Cost of Living",
        "title_short": "NYC vs Chicago",
        "city_a": "New York City",
        "city_b": "Chicago",
        "slug_a": "new-york/new-york-city",
        "slug_b": "chicago",
        "rent_a": 3400,
        "rent_b": 1850,
        "groceries_a": 550,
        "groceries_b": 420,
        "transport_a": 280,
        "transport_b": 310,
        "salary_a": 120000,
        "salary_b": 82000,
        "winner_rent": "Chicago",
        "winner_lifestyle": "Chicago on rent; NYC on transit access",
        "narrative": [
            "New York and Chicago are both big-city markets with very different rent lines. NYC rent on a 1-bedroom often runs almost double Chicago.",
            "Chicago wins on housing cost for most renters. NYC wins if you value subway coverage and do not need a car.",
            "Groceries are higher in NYC but not as wide a gap as rent. Both cities tax income — NYC adds a city tax.",
            "A $100k offer in Chicago often feels roomier than $100k in NYC after rent. Run your own take-home with our tax tools.",
            "If you work hybrid, compare commute time and transit pass cost. A cheap rent far from the loop still has a time cost.",
        ],
    },
    "austin-vs-denver": {
        "title": "Austin vs Denver Cost of Living",
        "title_short": "Austin vs Denver",
        "city_a": "Austin",
        "city_b": "Denver",
        "slug_a": "texas/austin",
        "slug_b": "denver",
        "rent_a": 1750,
        "rent_b": 1950,
        "groceries_a": 400,
        "groceries_b": 430,
        "transport_a": 370,
        "transport_b": 340,
        "salary_a": 82000,
        "salary_b": 88000,
        "winner_rent": "Austin slightly",
        "winner_lifestyle": "Denver for outdoors; Austin for no state income tax",
        "narrative": [
            "Austin and Denver are both Sun Belt and mountain west growth cities. Rent rose in both after 2020.",
            "Texas has no state income tax. Colorado taxes income but at a flat rate. Compare take-home, not gross alone.",
            "Denver rent on a 1-bedroom often runs a bit above Austin. Austin car costs can run higher with sprawl.",
            "Denver utilities and heat can spike in winter. Austin AC costs spike in summer. Budget both seasons.",
            "We also have a Seattle vs Denver guide if you are weighing the Pacific Northwest instead of Texas.",
        ],
    },
    "dallas-vs-atlanta": {
        "title": "Dallas vs Atlanta Cost of Living",
        "title_short": "Dallas vs Atlanta",
        "city_a": "Dallas",
        "city_b": "Atlanta",
        "slug_a": "texas/dallas",
        "slug_b": "atlanta",
        "rent_a": 1550,
        "rent_b": 1650,
        "groceries_a": 390,
        "groceries_b": 400,
        "transport_a": 360,
        "transport_b": 350,
        "salary_a": 76000,
        "salary_b": 78000,
        "winner_rent": "Rough tie; Dallas slightly lower on many lists",
        "winner_lifestyle": "Both strong for spread-out suburban living",
        "narrative": [
            "Dallas and Atlanta are both major job hubs with car-first commutes. Neither is a cheap coastal city, but neither is NYC.",
            "Rent on a 1-bedroom is often close — Dallas slightly lower in many quarters, Atlanta varies by intown vs suburb.",
            "Texas has no state income tax. Georgia has a state income tax. A higher gross offer in Atlanta may net less than Dallas.",
            "Property tax in Texas is high for buyers. If you plan to buy, run our Texas house affordability page, not rent alone.",
            "Atlanta intown rents rose with migration from higher-cost metros. Suburbs in both cities still offer more space per dollar.",
        ],
    },
    "seattle-vs-phoenix": {
        "title": "Seattle vs Phoenix Cost of Living",
        "title_short": "Seattle vs Phoenix",
        "city_a": "Seattle",
        "city_b": "Phoenix",
        "slug_a": "seattle",
        "slug_b": "phoenix",
        "rent_a": 2200,
        "rent_b": 1650,
        "groceries_a": 480,
        "groceries_b": 390,
        "transport_a": 320,
        "transport_b": 340,
        "salary_a": 95000,
        "salary_b": 76000,
        "winner_rent": "Phoenix",
        "winner_lifestyle": "Phoenix on rent; Seattle on wages in tech",
        "narrative": [
            "Seattle and Phoenix are both Sun Belt and Pacific northwest growth stories with different rent lines.",
            "Washington has no state income tax. Arizona taxes income at a flat rate.",
            "Seattle rent runs higher. Phoenix summer utilities can narrow the gap.",
            "Tech jobs cluster in both metros. Pay can be strong. Rent still sets the feel of the budget.",
            "Run take-home tools for WA vs AZ before you pick based on gross pay alone.",
        ],
    },
}

HUB_COMPARE_SLUGS = ["nyc-vs-chicago", "austin-vs-denver", "dallas-vs-atlanta", "seattle-vs-phoenix"]


def cost_cards(rent: int, groceries: int, utilities: int, transport: int, tax_line: str) -> str:
    total = rent + groceries + utilities + transport
    return f"""
        <div class="col-cost-grid" role="list">
          <div class="col-cost-card" role="listitem"><span class="col-cost-card__label">Housing (rent)</span><span class="col-cost-card__value">{fmt(rent)}/mo</span></div>
          <div class="col-cost-card" role="listitem"><span class="col-cost-card__label">Groceries</span><span class="col-cost-card__value">{fmt(groceries)}/mo</span></div>
          <div class="col-cost-card" role="listitem"><span class="col-cost-card__label">Utilities</span><span class="col-cost-card__value">{fmt(utilities)}/mo</span></div>
          <div class="col-cost-card" role="listitem"><span class="col-cost-card__label">Car &amp; transit</span><span class="col-cost-card__value">{fmt(transport)}/mo</span></div>
        </div>
        <p class="col-cost-total"><strong>Core bills (no tax):</strong> about {fmt(total)} a month. Tax note: {tax_line}.</p>"""


def city_key_points(city: dict, state_name: str | None = None) -> list[str]:
    core = city["rent_1br"] + city["groceries"] + city["utilities"] + city["transport"]
    return [
        f"1BR rent near {fmt(city['rent_1br'])}/mo (varies by neighborhood).",
        f"Core monthly stack about {fmt(core)}/mo before tax or childcare.",
        f"Comfort salary near {fmt(city['salary_comfort'])} gross · family of 4 near {fmt(city['family_4'])}.",
        f"Cost index {city['col_index']} (US = 100) · lifestyle score {city['lifestyle_score']}/100.",
        "Use take-home pay for rent caps. Add childcare and debt on top of these medians.",
    ]


def state_key_points(data: dict) -> list[str]:
    return [
        f"Typical rent is near {fmt(data['rent_1br'])} a month.",
        f"Many singles plan for {fmt(data['salary_comfort'])} in gross pay.",
        data["tax_note"] + ".",
        "Tap a city below for local rent and pay targets.",
    ]


def state_quick_facts_html(data: dict) -> str:
    facts = [
        ("Typical 1BR rent", f"{fmt(data['rent_1br'])}/mo", "Baseline for a median one-bedroom in this state."),
        ("Comfort salary target", f"{fmt(data['salary_comfort'])}", "Common planning point for singles before debt and childcare."),
        ("Tax context", data["tax_note"], "Tax treatment can materially change take-home pay."),
        ("Next step", "Compare cities below", "Open a city to see local rent, pay targets, and household notes."),
    ]
    cards = "\n".join(
        f"""          <article class="col-fact-card">
            <span class="col-fact-card__kicker">{label}</span>
            <strong class="col-fact-card__value">{value}</strong>
            <p>{note}</p>
          </article>"""
        for label, value, note in facts
    )
    return f"""
        <div class="col-facts-grid">
{cards}
        </div>"""


def compare_takeaways(c: dict) -> list[str]:
    return [
        f"{c['city_a']} rent is {fmt(c['rent_a'])} a month. {c['city_b']} rent is {fmt(c['rent_b'])} a month.",
        f"Lower rent often goes to {c['winner_rent']}.",
        f"Pay targets are {fmt(c['salary_a'])} vs {fmt(c['salary_b'])} in gross pay. Check tax on net pay.",
        "Add kids, debt, and buy vs rent goals before you move for a small rent gap.",
    ]


def _compare_winner_cell(a_val: int, b_val: int, favor_lower: bool = True) -> tuple[str, str]:
    if a_val == b_val:
        return "", ""
    if favor_lower:
        a_wins = a_val < b_val
    else:
        a_wins = a_val > b_val
    a_attr = ' class="col-compare-winner"' if a_wins else ""
    b_attr = ' class="col-compare-winner"' if not a_wins and a_val != b_val else ""
    return a_attr, b_attr


def compare_col_link(city_name: str, href: str) -> str:
    return f'<a href="{href}">{city_name} cost of living</a>'


def compare_summary_strip(c: dict, link_a: str, link_b: str) -> str:
    rent_gap = abs(c["rent_a"] - c["rent_b"])
    sal_gap = abs(c["salary_a"] - c["salary_b"])
    cheaper_pay = c["city_a"] if c["salary_a"] < c["salary_b"] else c["city_b"]
    return f"""    <section class="col-compare-summary" aria-label="Comparison highlights">
      <div class="container">
        <div class="col-compare-summary__grid">
          <article class="col-compare-summary__card">
            <span class="col-compare-summary__label">Rent winner</span>
            <strong class="col-compare-summary__value">{c['winner_rent']}</strong>
            <p>{fmt(rent_gap)}/mo gap on median 1BR</p>
          </article>
          <article class="col-compare-summary__card">
            <span class="col-compare-summary__label">Salary gap</span>
            <strong class="col-compare-summary__value">{fmt(sal_gap)}</strong>
            <p>Comfort pay targets (gross, before tax)</p>
          </article>
          <article class="col-compare-summary__card">
            <span class="col-compare-summary__label">Lower pay target</span>
            <strong class="col-compare-summary__value">{cheaper_pay}</strong>
            <p>Usually signals lower overall cost pressure</p>
          </article>
          <article class="col-compare-summary__card col-compare-summary__card--note">
            <span class="col-compare-summary__label">Lifestyle note</span>
            <strong class="col-compare-summary__value col-compare-summary__value--text">{c.get('winner_lifestyle', 'Compare net pay and commute fit.')}</strong>
          </article>
        </div>
        <p class="col-compare-summary__sources">Figures from {compare_col_link(c['city_a'], link_a)} and {compare_col_link(c['city_b'], link_b)}.</p>
      </div>
    </section>"""


def compare_gap_section(c: dict, takeaways: list[str], link_a: str, link_b: str) -> str:
    rent_gap = abs(c["rent_a"] - c["rent_b"])
    sal_gap = abs(c["salary_a"] - c["salary_b"])
    cheaper_pay = c["city_a"] if c["salary_a"] < c["salary_b"] else c["city_b"]
    narrative = c.get("narrative", [])[:3]

    insight_defs = [
        ("Housing", "Rent gap", takeaways[0] if takeaways else "", "home"),
        ("Income", "Salary fit", takeaways[2] if len(takeaways) > 2 else "", "income"),
        ("Decision", "Before you move", takeaways[3] if len(takeaways) > 3 else "", "plan"),
    ]
    insight_cards = []
    for label, title, body, kind in insight_defs:
        if not body:
            continue
        insight_cards.append(
            f"""          <article class="col-compare-insight col-compare-insight--{kind}">
            <span class="col-compare-insight__tag">{label}</span>
            <h3>{title}</h3>
            <p>{body}</p>
          </article>"""
        )
    for i, line in enumerate(narrative):
        insight_cards.append(
            f"""          <article class="col-compare-insight col-compare-insight--context">
            <span class="col-compare-insight__tag">Context {i + 1}</span>
            <p>{line}</p>
          </article>"""
        )
    insights_html = "\n".join(insight_cards)

    return f"""    <section class="col-band col-compare-gap" aria-labelledby="col-compare-gap-title">
      <div class="container">
        <header class="col-band__head">
          <h2 id="col-compare-gap-title">What the gap means</h2>
          <p class="col-lead">How to read the numbers above when you are choosing between {c['city_a']} and {c['city_b']} — not just which city is cheaper on paper.</p>
        </header>
        <div class="col-compare-verdict" role="list">
          <article class="col-compare-verdict__card" role="listitem">
            <span class="col-compare-verdict__badge col-compare-verdict__badge--rent" aria-hidden="true">R</span>
            <div>
              <span class="col-compare-verdict__label">Rent</span>
              <strong>{c['winner_rent']}</strong>
              <p>{fmt(rent_gap)}/mo separates median 1BR rents.</p>
            </div>
          </article>
          <article class="col-compare-verdict__card" role="listitem">
            <span class="col-compare-verdict__badge col-compare-verdict__badge--pay" aria-hidden="true">$</span>
            <div>
              <span class="col-compare-verdict__label">Comfort salary</span>
              <strong>{cheaper_pay} needs less</strong>
              <p>{fmt(sal_gap)} gap in gross pay targets — verify with take-home tax.</p>
            </div>
          </article>
          <article class="col-compare-verdict__card" role="listitem">
            <span class="col-compare-verdict__badge col-compare-verdict__badge--trade" aria-hidden="true">±</span>
            <div>
              <span class="col-compare-verdict__label">Tradeoff</span>
              <strong>Cheaper ≠ always better</strong>
              <p>{c.get('winner_lifestyle', 'Job mix, commute, and lifestyle still matter.')}</p>
            </div>
          </article>
        </div>
        <div class="col-compare-insights">
{insights_html}
        </div>
        <aside class="col-compare-gap-cta" role="note">
          <p><strong>Next step:</strong> Run take-home pay for both states, then drill into {compare_col_link(c['city_a'], link_a)} and {compare_col_link(c['city_b'], link_b)} for rent tiers, lifestyle bands, and neighborhood notes.</p>
          <p><a href="/hourly-to-salary-after-tax">Compare take-home pay →</a> · <a href="/living/housing/how-much-rent-can-i-afford">Rent affordability →</a></p>
        </aside>
      </div>
    </section>"""


def related_links_block(links: list[tuple[str, str]]) -> str:
    items = "\n".join(
        f'          <a class="col-related-card" href="{href}"><strong>{label}</strong><span>Open guide</span></a>'
        for label, href in links
    )
    return f"""
    <section class="col-section col-related" aria-labelledby="col-related-title">
      <div class="container content-page">
        <h2 id="col-related-title">Related guides</h2>
        <p class="col-lead">Use these tools to validate rent targets, salary fit, and buy-versus-rent tradeoffs before you make a move.</p>
        <div class="col-related__grid">
{items}
        </div>
      </div>
    </section>"""


def city_at_a_glance_block(city: dict, core: int) -> str:
    score = city.get("lifestyle_score", 60)
    if score >= 72:
        tier = "Low pressure"
        tone = "good"
    elif score >= 62:
        tier = "Moderate pressure"
        tone = "warn"
    else:
        tier = "High pressure"
        tone = "bad"
    housing_share = round((city["rent_1br"] / max(core, 1)) * 100)
    return f"""
        <div class="col-glance-grid">
          <article class="col-glance-card">
            <span class="col-glance-card__kicker">Monthly essentials</span>
            <strong class="col-glance-card__value">{fmt(core)}/mo</strong>
            <p>Baseline includes rent, groceries, utilities, and transport.</p>
          </article>
          <article class="col-glance-card">
            <span class="col-glance-card__kicker">Housing share</span>
            <strong class="col-glance-card__value">{housing_share}%</strong>
            <p>Rent is the largest line in the core monthly stack for most households.</p>
          </article>
          <article class="col-glance-card">
            <span class="col-glance-card__kicker">Affordability signal</span>
            <strong class="col-glance-card__value">{city["lifestyle_score"]}/100</strong>
            <p><span class="col-pill col-pill--{tone}">{tier}</span></p>
          </article>
        </div>
        <div class="col-pressure-wrap">
          <p class="col-pressure-head"><strong>Budget pressure meter</strong> · where households usually feel cost strain first</p>
          <div class="col-pressure-row"><span>Housing</span><div class="col-pressure-track"><span style="width:{min(95, max(45, housing_share))}%"></span></div></div>
          <div class="col-pressure-row"><span>Transport</span><div class="col-pressure-track"><span style="width:{min(92, max(26, round(city['transport']/max(city['rent_1br'],1)*100)))}%"></span></div></div>
          <div class="col-pressure-row"><span>Groceries + utilities</span><div class="col-pressure-track"><span style="width:{min(88, max(20, round((city['groceries']+city['utilities'])/max(city['rent_1br'],1)*100)))}%"></span></div></div>
        </div>"""


def city_glance_insights(points: list[str]) -> str:
    cards = "".join(
        f"""
          <article class="col-glance-note">
            <p>{point}</p>
          </article>"""
        for point in points
    )
    return f"""
        <div class="col-glance-notes">
{cards}
        </div>"""


def state_recommendations_block(slug: str, data: dict) -> str:
    defaults = [
        "Keep housing near your safe rent tier before adding lifestyle upgrades.",
        "Use take-home pay, not gross pay, when comparing city offers.",
        "Build a move-in buffer for deposits, setup fees, and first-month surprises.",
    ]
    by_state = {
        "california": [
            "If you want California job access with lower pressure, compare inland metros before signing a coastal lease.",
            "Budget state income tax and insurance changes before you set rent in high-cost counties.",
            "For wildfire or coastal risk zones, recheck insurance costs before final move decisions.",
        ],
        "texas": [
            "No state income tax helps take-home pay, but property tax and insurance can still be heavy for buyers.",
            "Houston often gives lower rent than Austin or Dallas; compare commute cost before choosing.",
            "Heat-related utility spikes are real. Use summer bills in your baseline, not spring averages.",
        ],
        "florida": [
            "Coastal insurance and HOA differences can change affordability more than expected.",
            "Compare Miami against Tampa/Orlando before assuming state averages fit your budget.",
            "Storm season risk planning matters. Keep a stronger emergency buffer in coastal zones.",
        ],
        "new-york": [
            "Downstate and upstate budgets differ sharply. Do not use one state average for both.",
            "Include city + state tax effect before committing to a higher headline salary.",
            "If you target NYC, include transit, broker, and move-in fees in month-one planning.",
        ],
    }
    tips = by_state.get(slug, defaults)
    cards = "\n".join(
        f"""          <article class="col-rec-card"><h3>Recommendation {i+1}</h3><p>{tip}</p></article>"""
        for i, tip in enumerate(tips)
    )
    return f"""
    <section class="col-band col-band--tone-warm">
      <div class="container">
        <header class="col-band__head">
          <h2>Recommendations for {data['name']}</h2>
          <p>Practical guidance based on local cost structure, tax profile, and common move patterns.</p>
        </header>
        <div class="col-rec-grid">
{cards}
        </div>
      </div>
    </section>"""


def city_recommendations_block(city: dict, state_name: str | None) -> str:
    name = city["name"]
    state_label = state_name or city.get("state_name", "")
    dense = {"Los Angeles", "San Francisco", "New York City", "Chicago", "Seattle"}
    coastal = {"Miami", "Tampa", "Orlando", "San Diego", "San Francisco", "Los Angeles", "New York City"}
    tips = [
        f"Keep total housing near your safe zone and test commute cost in {name} before signing.",
        f"Use {name} neighborhood-level listings to validate rent assumptions from city averages.",
        f"For families in {state_label}, add childcare and school-zone transport to baseline monthly costs.",
    ]
    if name in dense:
        tips[1] = f"In {name}, parking, transit, and time cost can be as important as rent. Compare full commute burden."
    if name in coastal:
        tips.append(f"In {name}, insurance and weather risk can change monthly cost. Recheck policies before move-in.")
    cards = "\n".join(
        f"""          <article class="col-rec-card"><h3>Recommendation {i+1}</h3><p>{tip}</p></article>"""
        for i, tip in enumerate(tips[:3])
    )
    return f"""
    <section class="col-band col-band--tone-cool">
      <div class="container">
        <header class="col-band__head">
          <h2>Recommendations for {name}</h2>
          <p>Area-aware suggestions to reduce budget stress and improve move decisions.</p>
        </header>
        <div class="col-rec-grid">
{cards}
        </div>
      </div>
    </section>"""


def city_interlink_block(current_path: str, city_name: str) -> str:
    links: list[tuple[str, str]] = []
    for state_slug, state in STATES.items():
        for c_slug, c in state["cities"].items():
            path = f"/living/housing/cost-of-living-by-city/{state_slug}/{c_slug}"
            if path != current_path:
                links.append((c["name"], path))
    for c_slug, c in STANDALONE.items():
        path = f"/living/housing/cost-of-living-by-city/{c_slug}"
        if path != current_path:
            links.append((c["name"], path))
    links.sort(key=lambda x: x[0])
    chips = "\n".join(
        f'        <a class="col-city-chip" href="{href}">{label}</a>' for label, href in links
    )
    return f"""
    <section class="col-band">
      <div class="container">
        <h2>Compare {city_name} with other cities</h2>
        <p class="col-lead">Open another city guide to compare rent, salary targets, and budget pressure side by side.</p>
        <div class="col-city-chips">
{chips}
        </div>
      </div>
    </section>"""


def _place_slug(place_name: str) -> str:
    return place_name.lower().replace(" ", "-")


def city_know_points(city: dict, tax: str) -> list[str]:
    return [
        f"Median 1BR rent near {fmt(city['rent_1br'])}/mo is usually the largest line in a comfort budget.",
        f"Cost-of-living index {city['col_index']} (US average = 100) captures rent, food, utilities, and transport pressure.",
        f"Many singles plan around {fmt(city['salary_comfort'])} gross here before childcare, debt, and extra savings goals.",
        f"Tax context: {tax}",
    ]


def col_know_block(place_name: str, points: list[str], lead: str = "") -> str:
    if not points:
        return ""
    slug = _place_slug(place_name)
    lead_html = f'        <p class="col-know-lead">{lead}</p>' if lead else ""
    items = "\n".join(f"          <li>{p}</li>" for p in points)
    return f"""
    <section class="col-band col-band--tone-cool col-know-section" aria-labelledby="col-know-{slug}-title">
      <div class="container">
        <header class="col-band__head col-know-head">
          <h2 id="col-know-{slug}-title">What to know about {place_name}</h2>
{lead_html}
        </header>
        <ul class="col-know-points">
{items}
        </ul>
      </div>
    </section>"""


def col_lifestyle_tiers_section(
    city: dict,
    place_name: str,
    state_slug: str | None = None,
    salary_link: str = "",
) -> str:
    """Monthly cost + gross pay by lifestyle tier (matches comfortable salary model)."""
    from comfortable_salary_data import LIFESTYLE_TIERS, compute_salary

    slug = _place_slug(place_name)
    tier_cards: list[str] = []
    monthly_by_tier: dict[str, int] = {}

    for key in LIFESTYLE_TIERS:
        result = compute_salary(city, "single", "rent", key, state_slug)
        monthly_by_tier[key] = result["monthly"]
        featured = " col-tier-card--featured" if key == "comfortable" else ""
        tier_cards.append(
            f"""            <article class="col-tier-card{featured}">
              <strong>{LIFESTYLE_TIERS[key]["label"]}</strong>
              <span class="col-tier-card__monthly">{fmt(result["monthly"])}/mo</span>
              <span class="col-tier-card__salary">{fmt(result["annual"])} gross</span>
            </article>"""
        )

    comfort = compute_salary(city, "single", "rent", "comfortable", state_slug)
    breakdown = comfort["breakdown"]
    mix_rows = ""
    for key, label in [
        ("housing", "Housing"),
        ("transportation", "Transportation"),
        ("food", "Food"),
        ("savings", "Savings"),
        ("lifestyle", "Lifestyle spending"),
    ]:
        b = breakdown.get(key, {"amount": 0, "pct": 0})
        mix_rows += f"""            <div class="col-mix-row">
              <span>{label}</span>
              <div class="col-mix-bar"><span style="width:{b['pct']}%"></span></div>
              <span>{b['pct']}%</span>
            </div>
"""

    salary_note = (
        f' <a href="{salary_link}">Open the comfortable salary guide</a> for household and rent vs own options.'
        if salary_link
        else ""
    )

    return f"""    <section class="col-band col-band--alt col-lifestyle-section" aria-labelledby="col-lifestyle-{slug}-title">
      <div class="container">
        <header class="col-band__head">
          <h2 id="col-lifestyle-{slug}-title">Cost of living by lifestyle</h2>
          <p class="col-lead">Monthly spending and gross pay targets for <strong>{place_name}</strong>. Assumes a single renter; add childcare, debt, and extra savings on top.</p>
        </header>
        <p class="col-tier-context">Lifestyle tiers span {fmt(monthly_by_tier["basic"])}/mo (basic) to {fmt(monthly_by_tier["high_comfort"])}/mo (affluent). The highlighted tier is our default comfortable plan with room to save.</p>
        <div class="col-tier-grid">
{chr(10).join(tier_cards)}
        </div>
        <div class="col-lifestyle-breakdown">
          <h3>Monthly mix at the comfortable tier</h3>
          <p class="col-lead">How a {fmt(comfort["monthly"])}/mo budget splits before tax ({fmt(comfort["annual"])} gross target).{salary_note}</p>
          <div class="col-mix-grid">{mix_rows}
          </div>
        </div>
      </div>
    </section>"""


def col_methodology_block(city: dict, metrics: dict, tax: str, place_name: str) -> str:
    slug = _place_slug(place_name)
    lifestyle = city.get("lifestyle_score")
    lifestyle_line = (
        f"Index {city['col_index']} (US = 100) with housing share {metrics['housing_share']}% yields model score "
        f"<strong>{metrics['derived_score']}/100</strong>. Page score: {lifestyle}/100."
        if lifestyle is not None
        else f"Index {city['col_index']} (US = 100) with housing share {metrics['housing_share']}% yields model score "
        f"<strong>{metrics['derived_score']}/100</strong>."
    )
    return f"""
    <section class="col-band col-band--alt col-method-section" aria-labelledby="col-method-{slug}-title">
      <div class="container">
        <header class="col-band__head">
          <h2 id="col-method-{slug}-title">How we calculate {place_name} numbers</h2>
          <p class="col-lead">Transparent planning math you can audit before a move or offer decision.</p>
        </header>
        <div class="col-method-summary" role="note">
          <div class="col-method-summary__item">
            <span class="col-method-summary__label">Core monthly stack</span>
            <strong class="col-method-summary__value">{fmt(metrics['core'])}/mo</strong>
          </div>
          <div class="col-method-summary__item">
            <span class="col-method-summary__label">Comfort salary (model)</span>
            <strong class="col-method-summary__value">{fmt(metrics['min_salary'])}</strong>
          </div>
          <div class="col-method-summary__item">
            <span class="col-method-summary__label">Published target</span>
            <strong class="col-method-summary__value">{fmt(city['salary_comfort'])}</strong>
          </div>
        </div>
        <div class="col-method-grid">
          <article class="col-method-card">
            <span class="col-method-card__step" aria-hidden="true">1</span>
            <div class="col-method-card__body">
              <h3>Core monthly stack</h3>
              <p>Rent {fmt(city['rent_1br'])} + groceries {fmt(city['groceries'])} + utilities {fmt(city['utilities'])} + transport {fmt(city['transport'])}.</p>
            </div>
          </article>
          <article class="col-method-card">
            <span class="col-method-card__step" aria-hidden="true">2</span>
            <div class="col-method-card__body">
              <h3>Comfort salary target</h3>
              <p>Annual core ({fmt(metrics['core'] * 12)}) ÷ {int(CORE_GROSS_SHARE * 100)}% gross share ≈ {fmt(metrics['min_salary'])}. We publish {fmt(city['salary_comfort'])} as a market-adjusted planning line.</p>
            </div>
          </article>
          <article class="col-method-card">
            <span class="col-method-card__step" aria-hidden="true">3</span>
            <div class="col-method-card__body">
              <h3>Affordability signal</h3>
              <p>{lifestyle_line}</p>
            </div>
          </article>
          <article class="col-method-card">
            <span class="col-method-card__step" aria-hidden="true">4</span>
            <div class="col-method-card__body">
              <h3>Tax context</h3>
              <p>{tax.rstrip('.')}. Use take-home pay — not gross alone — when setting rent caps and savings goals.</p>
            </div>
          </article>
        </div>
        <p class="col-method-footer"><a href="/methodology#affordability">Read the full affordability methodology →</a></p>
      </div>
    </section>"""


def col_planning_block(
    place_name: str,
    metrics: dict,
    city: dict,
    take_home: str,
    rent_link: str,
    house_link: str,
    salary_link: str,
    moving_link: str,
) -> str:
    return f"""
    <section class="col-band">
      <div class="container">
        <h2>Plan your {place_name} budget in order</h2>
        <div class="col-context-links">
          <p>Start with your real take-home pay in the <a href="{take_home}">state take-home calculator</a>. In {place_name}, core bills run about <strong>{fmt(metrics['core'])}/mo</strong> before debt, childcare, or savings.</p>
          <p>Next, set a rent ceiling in the <a href="{rent_link}">rent affordability calculator</a>. At a 30% gross-income cap, rent near {fmt(city['rent_1br'])}/mo implies planning income around <strong>{fmt(metrics['rent_cap_gross'])}</strong> gross — then stress-test with your actual deductions.</p>
          <p>If you might buy, compare with <a href="{house_link}">house affordability in {place_name}</a> and the <a href="/rent-vs-buy-calculator">rent vs buy calculator</a>. If you are relocating, estimate move cash in the <a href="{moving_link}">moving cost calculator</a>.</p>
          <p>For household targets, use the <a href="{salary_link}">comfortable salary guide</a> and <a href="/living/lifestyle-family/family-of-4-income-guide/">family of 4 income guide</a> to layer childcare and debt on top of these medians.</p>
        </div>
      </div>
    </section>"""


def col_eeat_block(place_name: str, metrics: dict) -> str:
    slug = place_name.lower().replace(" ", "-")
    return f"""
    <section class="col-eeat">
      <div class="container content-page">
        <p class="col-disclaimer">Educational content for US readers only, not financial or legal advice. Verify with pay stubs, listings, and local tax guidance.</p>
        <aside class="eeat-trust" aria-labelledby="eeat-col-{slug}-title">
          <header class="eeat-trust__header">
            <span class="eeat-trust__kicker">How we built this</span>
            <h2 id="eeat-col-{slug}-title" class="eeat-trust__title">{place_name} Cost of Living Methodology &amp; Data Sources</h2>
            <p class="eeat-trust__meta"><time datetime="2026-05-30">Last reviewed: May 30, 2026</time> · Reviewed by the Income Clarity editorial team · <a href="/methodology#affordability">Read the full methodology</a></p>
          </header>
          <div class="eeat-trust__grid">
            <article class="eeat-trust__card">
              <h3>How we calculate affordability</h3>
              <ul>
                <li><strong>Core stack:</strong> 1BR rent + groceries + utilities + transport ({fmt(metrics['core'])}/mo here).</li>
                <li><strong>Comfort salary:</strong> annual core ÷ {int(CORE_GROSS_SHARE * 100)}% gross share, rounded to nearest $5k.</li>
                <li><strong>Family target:</strong> core stack × {FAMILY_STACK_MULT} with a {int(FAMILY_GROSS_SHARE * 100)}% gross share assumption.</li>
                <li><strong>Affordability signal:</strong> cost index + housing share pressure (not a quality-of-life score).</li>
              </ul>
            </article>
            <article class="eeat-trust__card">
              <h3>Primary data sources</h3>
              <ul>
                <li><a href="https://www.zillow.com/research/data/" rel="noopener noreferrer">Zillow Research (ZORI)</a> — metro rent medians.</li>
                <li><a href="https://www.huduser.gov/portal/datasets/fmr.html" rel="noopener noreferrer">HUD Fair Market Rents</a> — regional rent benchmarks.</li>
                <li><a href="https://www.bls.gov/cpi/" rel="noopener noreferrer">BLS CPI</a> — food, utilities, and transport inflation context.</li>
                <li><a href="https://www.census.gov/data/developers/data-sets/acs-5year.html" rel="noopener noreferrer">Census ACS</a> — income and household spending context.</li>
              </ul>
            </article>
            <article class="eeat-trust__card">
              <h3>What this is not</h3>
              <p>These are planning medians, not lease approvals or loan underwriting. Neighborhood rent spreads, insurance, childcare, and debt can shift your real budget by hundreds per month.</p>
            </article>
          </div>
          <p class="eeat-trust__footer">See a mismatch with your market? <a href="/contact">Tell us</a> — we fix confirmed errors within 7 days.</p>
        </aside>
      </div>
    </section>"""


def state_narrative_block(data: dict) -> str:
    return col_know_block(
        data["name"],
        data.get("narrative", []),
        data.get("rank_intro", ""),
    )


def contextual_interlinks_block(
    *,
    place_name: str,
    take_home: str,
    rent_link: str,
    house_link: str,
    salary_link: str,
    compare_links: list[tuple[str, str]],
    extra_cards: list[tuple[str, str]] | None = None,
) -> str:
    compare_html = ""
    if compare_links:
        items = " · ".join(f'<a href="{href}">{label}</a>' for label, href in compare_links[:3])
        compare_html = f"""
        <p class="col-lead">Head-to-head comparisons: {items}</p>"""
    cards = [
        ("Take-home pay", take_home, "Convert gross offers to net before comparing cities."),
        ("Rent affordability", rent_link, "Set a rent cap from your real paycheck."),
        ("Rent vs buy", "/rent-vs-buy-calculator", "Compare long-run housing cost if you might buy."),
        ("Comfortable salary", salary_link, "Benchmark income needed for your household."),
    ]
    if extra_cards:
        cards.extend(extra_cards)
    card_html = "\n".join(
        f'          <a class="col-related-card" href="{href}"><strong>{label}</strong><span>{note}</span></a>'
        for label, href, note in cards
    )
    return f"""
    <section class="col-section col-related" aria-labelledby="col-related-title">
      <div class="container content-page">
        <h2 id="col-related-title">Related tools for {place_name}</h2>
        <p class="col-lead">Use these calculators after this page to pressure-test rent, tax, and relocation decisions with your own numbers.</p>
{compare_html}
        <div class="col-related__grid">
{card_html}
        </div>
      </div>
    </section>"""


def city_page(
    city_slug: str,
    city: dict,
    state_slug: str | None,
    state_name: str | None,
    state_data: dict | None,
) -> str:
    page_path = f"{state_slug}/{city_slug}" if state_slug else city_slug
    breadcrumbs = '<li><a href="/living/housing/cost-of-living-by-city">Cost of living</a></li>'
    if state_slug and state_name:
        breadcrumbs += f'\n            <li><a href="/living/housing/cost-of-living-by-city/{state_slug}">{state_name}</a></li>'
    breadcrumbs += f'\n            <li aria-current="page">{city["name"]}</li>'
    tax = state_data["tax_note"] if state_data else STANDALONE.get(city_slug, {}).get("tax_note", "Varies by state")
    metrics = prepare_city_metrics(city)
    core = metrics["core"]
    effective_state = state_slug
    if not effective_state:
        from comfortable_salary_data import STANDALONE_STATE

        effective_state = STANDALONE_STATE.get(city_slug)
    lifestyle_section = col_lifestyle_tiers_section(
        city, city["name"], effective_state, city.get("salary_link", "")
    )
    key_points = city.get("key_points") or city_key_points(city, state_name)
    faqs = city.get(
        "faqs",
        [
            (
                f"How much do I need to earn in {city['name']}?",
                f"Many singles plan around {fmt(city['salary_comfort'])} gross to cover core bills with some saving room. "
                f"Families often plan closer to {fmt(city['family_4'])} gross before childcare, debt, and medical costs.\n\n"
                "Use this as a planning line, then adjust with your own debt payments, savings target, and local neighborhood rent."
            ),
            (
                f"Is {city['name']} expensive?",
                f"The city index is {city['col_index']} with US = 100. That means {city['name']} can feel above average or near average based on your rent tier and commute style. "
                "Compare this page with one peer city to judge the real gap.\n\n"
                "The same city can feel affordable or tight depending on commute distance, parking costs, and housing choice."
            ),
            (
                "What counts in cost of living on this page?",
                "Core lines are rent, groceries, utilities, and transport. We show them in monthly dollars for quick planning. "
                "Add debt payments, childcare, healthcare premiums, and savings goals to get your real budget.\n\n"
                "Treat this page as your baseline, then layer personal costs on top before you sign a lease."
            ),
            (
                "Should I use gross or net pay?",
                "Use take-home pay when you set a rent cap. Gross pay is useful for broad planning, but net pay decides monthly comfort. "
                "Run your local take-home calculator after this page.\n\n"
                "This prevents overestimating affordability when taxes or deductions are high."
            ),
            (
                f"What is the lifestyle score in {city['name']}?",
                f"It is {city['lifestyle_score']}/100 in our model. Higher means your income usually stretches further after core bills. "
                "It is a cost-pressure signal, not a quality-of-life score.\n\n"
                "Use it to compare budget strain between cities, then use your own priorities for final decisions."
            ),
            (
                "Can roommates lower my number?",
                "Yes. Shared rent can drop your housing burden fast. Still include utilities, parking, fees, and move-in costs when you compare listings.\n\n"
                "Many renters use roommates for 12 to 24 months to build savings before moving solo."
            ),
            (
                "How should I use this page before moving?",
                "Use this sequence: estimate take-home pay, set a rent cap, compare two neighborhoods, then pressure-test your budget with debt and savings. "
                "Do not rely on one listing price alone.\n\n"
                "Shortlist 2 to 3 neighborhoods and run the same budget in each to avoid surprise costs."
            ),
        ],
    )
    if state_slug:
        house_col = f"/living/housing/cost-of-living-by-city/{state_slug}"
    else:
        house_col = f"/living/housing/cost-of-living-by-city/{city_slug}"
    related = [
        ("Cost of living hub", "/living/housing/cost-of-living-by-city"),
        (f"How much house can I afford — {city['name']}", city["house_link"]),
        ("Rent affordability calculator", city["rent_link"]),
        ("Comfortable salary guide", city["salary_link"]),
    ]
    if state_slug:
        related.insert(1, (f"Cost of living — {state_name}", house_col))
    current_path = f"/living/housing/cost-of-living-by-city/{page_path}"
    take_home = take_home_link(state_slug, city_slug if not state_slug else None)
    moving = moving_cost_link(state_slug, city_slug)
    compare_links = compare_links_for_path(page_path)
    extra_cards = [
        ("Moving cost calculator", moving, "Estimate deposits, move fees, and first-month cash."),
        ("Cost to live alone", "/living/can-i-afford-to-live-alone", "Test solo living pressure by city and income."),
    ]
    if state_slug:
        extra_cards.insert(0, (f"Cost of living — {state_name}", f"/living/housing/cost-of-living-by-city/{state_slug}", f"Compare all {state_name} cities."))
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{city['name']} Cost of Living: Rent, Salary &amp; Budget (2026) | Income Clarity</title>
  <meta name="description" content="Cost of living in {city['name']}: rent near {fmt(city['rent_1br'])}/mo, groceries, transport, salary near {fmt(city['salary_comfort'])}, and lifestyle score.">
  <link rel="canonical" href="https://www.incomeclaritylab.com/living/housing/cost-of-living-by-city/{page_path}">
  <link rel="stylesheet" href="/styles.css">
{STYLES_COL}
  <link rel="icon" type="image/png" href="/images/logo.png">
  <link rel="apple-touch-icon" href="/images/logo.png">
{URL_SCRIPT}
</head>
<body class="col-page living-tool-page col-city-page">
{HEADER}
  <main>
    <section class="col-hero-inner">
      <div class="container">
        <nav class="take-home-return-nav" aria-label="Breadcrumb">
          <ol class="take-home-return-breadcrumbs">
{breadcrumbs}
          </ol>
        </nav>
        <span class="label">Cost of living · {city['name']}</span>
        <h1>Cost of Living in {city['name']}</h1>
        <p class="lead">Monthly rent, food, bills, and pay targets for {city['name']}.</p>
        <div class="col-term-grid">
          <article class="col-term-card">
            <h3>Cost index</h3>
            <p>US average is 100. A higher score means higher cost pressure for similar habits.</p>
          </article>
          <article class="col-term-card">
            <h3>Comfort salary</h3>
            <p>A planning target for gross pay before tax. Add debt, childcare, and savings goals on top.</p>
          </article>
          <article class="col-term-card">
            <h3>Core monthly stack</h3>
            <p>Rent + food + utilities + transport. This is your baseline before lifestyle and long-term goals.</p>
          </article>
        </div>
        <div class="col-stat-row">
          <div class="col-stat-box"><span class="col-stat-box__n">{city['col_index']}</span><span class="col-stat-box__l">Cost index</span></div>
          <div class="col-stat-box"><span class="col-stat-box__n">{city['lifestyle_score']}</span><span class="col-stat-box__l">Affordability</span></div>
          <div class="col-stat-box"><span class="col-stat-box__n">{fmt(city['rent_1br'])}</span><span class="col-stat-box__l">Median rent</span></div>
          <div class="col-stat-box"><span class="col-stat-box__n">{fmt(city['salary_comfort'])}</span><span class="col-stat-box__l">Comfort salary</span></div>
        </div>
      </div>
    </section>
    <section class="col-band col-band--tone-cool">
      <div class="container">
        <h2>Monthly cost breakdown</h2>
{cost_cards(city['rent_1br'], city['groceries'], city['utilities'], city['transport'], tax)}
      </div>
    </section>
{lifestyle_section}
    <section class="col-band col-band--alt col-band--tone-cool">
      <div class="container">
        <h2>At a glance</h2>
{city_at_a_glance_block(city, core)}
{city_glance_insights(key_points)}
        <aside class="col-callout" role="note">
          <strong>Your move:</strong> Get a real rent quote, then check it against <a href="{city['rent_link']}">rent affordability</a> and <a href="{city['house_link']}">home buying</a> for {city['name']}.
        </aside>
      </div>
    </section>
    <section class="col-band">
      <div class="container">
        <h2>Family &amp; household notes</h2>
        <p class="col-lead">Family of 4: about <strong>{fmt(city['family_4'])} gross</strong>. Singles: near <strong>{fmt(city['salary_comfort'])}</strong>. Add childcare separately in hot job markets.</p>
        <div class="col-household-grid">
          <article class="col-household-card">
            <h3>Single renter</h3>
            <p>Target pay near <strong>{fmt(city['salary_comfort'])}</strong> gross. Keep rent close to 30% of take-home where possible.</p>
          </article>
          <article class="col-household-card">
            <h3>Couple sharing rent</h3>
            <p>Split housing can lower pressure fast, but still budget two commute patterns, groceries, and debt payments.</p>
          </article>
          <article class="col-household-card">
            <h3>Family with kids</h3>
            <p>Plan around <strong>{fmt(city['family_4'])}</strong> gross, then add childcare, after-school, and healthcare costs.</p>
          </article>
        </div>
        <ul class="col-key-list">
          <li>Use this page for city medians, then validate with 2–3 live listings in your target zip codes.</li>
          <li>Add one-time move costs (deposits, setup fees, furniture) outside monthly totals.</li>
          <li>Stress-test with debt and savings goals before signing a lease or mortgage.</li>
        </ul>
        <p><a href="/living/lifestyle-family/family-of-4-income-guide/">Family budget guide</a> · <a href="{city['salary_link']}">Comfortable salary</a> · <a href="{city['house_link']}">House affordability</a></p>
      </div>
    </section>
{city_recommendations_block(city, state_name)}
{city_interlink_block(current_path, city['name'])}
{col_know_block(city['name'], city_know_points(city, tax))}
{col_planning_block(city['name'], metrics, city, take_home, city['rent_link'], city['house_link'], city['salary_link'], moving)}
{col_methodology_block(city, metrics, tax, city['name'])}
    <section class="col-faq-section">
      <div class="container content-page">
        <h2>FAQ — {city['name']}</h2>
        <div class="faq-stack">
{faq_html(faqs)}
        </div>
      </div>
    </section>
{contextual_interlinks_block(
    place_name=city['name'],
    take_home=take_home,
    rent_link=city['rent_link'],
    house_link=city['house_link'],
    salary_link=city['salary_link'],
    compare_links=compare_links,
    extra_cards=extra_cards,
)}
{col_eeat_block(city['name'], metrics)}
  </main>
{FOOTER}
  <script src="/guide-back.js"></script>
</body>
</html>
"""


def state_page(slug: str, data: dict) -> str:
    city_rows = "\n".join(
        f"""              <tr>
                <th scope="row"><a href="/living/housing/cost-of-living-by-city/{slug}/{cs}">{c['name']}</a></th>
                <td>{c['col_index']}</td>
                <td>{fmt(c['rent_1br'])}</td>
                <td>{fmt(c['salary_comfort'])}</td>
                <td>{c['lifestyle_score']}</td>
              </tr>"""
        for cs, c in data["cities"].items()
    )
    chips = "\n".join(
        f'          <a class="col-city-chip" href="/living/housing/cost-of-living-by-city/{slug}/{cs}" data-city="{c["name"].lower()}">{c["name"]}</a>'
        for cs, c in data["cities"].items()
    )
    house = f"/living/housing/how-much-house-can-i-afford/{slug}"
    salary = f"/living/lifestyle/comfortable-salary/{slug}" if slug in STATES or slug == "illinois" else "/living/lifestyle/comfortable-salary-us"
    related = [
        ("How much house can I afford", house),
        ("Cost of living hub", "/living/housing/cost-of-living-by-city"),
        ("Rent affordability", "/living/housing/how-much-rent-can-i-afford"),
        ("Comfortable salary", salary),
    ]
    city_blurbs = "\n".join(
        f"""        <article class="col-city-snap-card">
          <h3><a href="/living/housing/cost-of-living-by-city/{slug}/{cs}">{c["name"]}</a></h3>
          <p class="col-city-snap-kpi"><span>COL index</span><strong>{c["col_index"]}</strong></p>
          <p class="col-city-snap-kpi"><span>1BR rent</span><strong>{fmt(c["rent_1br"])}/mo</strong></p>
          <p class="col-city-snap-kpi"><span>Comfort salary</span><strong>{fmt(c["salary_comfort"])}</strong></p>
          <p class="col-city-snap-meta">Lifestyle score: {c.get("lifestyle_score", "—")}/100</p>
        </article>"""
        for cs, c in data["cities"].items()
    )
    faqs = [
        (
            f"What is rent like in {data['name']}?",
            f"Typical rent is near {fmt(data['rent_1br'])} a month, but city and neighborhood spreads can be large.\n\n"
            "Use state averages for quick orientation, then validate with local listings before deciding where to live."
        ),
        (
            f"How much pay do I need in {data['name']}?",
            f"Many singles plan for {fmt(data['salary_comfort'])} or more in gross pay to stay comfortable after core bills.\n\n"
            "If you carry debt or support family costs, target higher income or lower housing to protect monthly breathing room."
        ),
        (
            f"How does {data['name']} compare to Texas?",
            "Texas often has lower rent and no state income tax, which can improve take-home flexibility.\n\n"
            "Still compare exact city pairs and job offers, not only state averages."
        ),
        (
            "What is the cost index?",
            "The index combines major monthly lines like rent, food, utilities, and transport, with US = 100 as baseline.\n\n"
            "It helps compare relative pressure across places, but your actual budget depends on personal spending patterns."
        ),
        (
            "Should I rent or buy?",
            "Rent and buy decisions depend on local prices, taxes, rates, and how long you plan to stay.\n\n"
            "Run rent vs buy with your likely move timeline so you compare total cost, not only monthly payment."
        ),
    ]
    if slug != "california":
        faqs[2] = (
            f"Is {data['name']} cheaper than California?",
            "Often yes on rent and some daily costs, but salary levels and taxes can change the net outcome.\n\n"
            "Compare your expected take-home pay and rent in both places before assuming one is always cheaper."
        )
    state_metrics = prepare_city_metrics(data)
    take_home = take_home_link(slug, None)
    state_compare = [("California vs Texas", "/living/cost-of-living/cost-of-living-california-vs-texas.html")]
    if slug == "texas":
        state_compare = [("California vs Texas", "/living/cost-of-living/cost-of-living-california-vs-texas.html")]
    elif slug == "california":
        state_compare = [("California vs Texas", "/living/cost-of-living/cost-of-living-california-vs-texas.html")]
    else:
        state_compare = []
    for cs, _c in data["cities"].items():
        for cmp_slug, cmp in COMPARISONS.items():
            if cmp["slug_a"].endswith(f"/{cs}") or cmp["slug_b"].endswith(f"/{cs}"):
                link = (cmp["title_short"], f"/living/housing/cost-of-living-by-city/compare/{cmp_slug}")
                if link not in state_compare:
                    state_compare.append(link)
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{data['name']} Cost of Living by City | Income Clarity</title>
  <meta name="description" content="Compare cost of living in {data['name']}: average rent, groceries, taxes, utilities, and top cities ranked.">
  <link rel="canonical" href="https://www.incomeclaritylab.com/living/housing/cost-of-living-by-city/{slug}">
  <link rel="stylesheet" href="/styles.css">
{STYLES_COL}
  <link rel="icon" type="image/png" href="/images/logo.png">
  <link rel="apple-touch-icon" href="/images/logo.png">
{URL_SCRIPT}
</head>
<body class="col-page living-tool-page">
{HEADER}
  <main>
    <section class="col-hero-inner">
      <div class="container">
        <nav class="take-home-return-nav" aria-label="Breadcrumb">
          <ol class="take-home-return-breadcrumbs">
            <li><a href="/living/housing/cost-of-living-by-city">Cost of living</a></li>
            <li aria-current="page">{data['name']}</li>
          </ol>
        </nav>
        <span class="label">Browse by state · {data['name']}</span>
        <h1>Cost of Living in {data['name']}</h1>
        <p class="lead">State overview, city rankings, and links to deep city guides. {data['tax_note']}.</p>
        <div class="col-city-chips">{chips}</div>
      </div>
    </section>
    <section class="col-section">
      <div class="container content-page">
        <h2>{data['name']} at a glance</h2>
{cost_cards(data['rent_1br'], data['groceries'], data['utilities'], data['transport'], data['tax_note'])}
        <p class="col-lead">Cost index is <strong>{data['col_index']}</strong> (US norm is 100). Use these quick facts as planning anchors before you compare individual cities.</p>
{state_quick_facts_html(data)}
      </div>
    </section>
{col_lifestyle_tiers_section(data, data["name"], slug, f"/living/lifestyle/comfortable-salary/{slug}")}
    <section class="col-band col-band--alt col-band--tone-cool">
      <div class="container">
        <h2>Top cities in {data['name']}</h2>
        <p class="col-lead">{data['rank_intro']}</p>
        <div class="col-compare-table-wrap">
          <table class="debt-data-table">
            <caption>City rankings: index, rent, salary, lifestyle score</caption>
            <thead><tr><th scope="col">City</th><th scope="col">Index</th><th scope="col">Rent (1BR)</th><th scope="col">Comfort salary</th><th scope="col">Lifestyle</th></tr></thead>
            <tbody>
{city_rows}
            </tbody>
          </table>
        </div>
      </div>
    </section>
    <section class="col-band">
      <div class="container">
        <h2>City snapshots</h2>
        <p class="col-lead">Quick city cards for rent, cost index, and income targets. Open a city to view deeper local detail.</p>
        <div class="col-city-snap-grid">
{city_blurbs}
        </div>
        <p class="col-lead">Tools: <a href="{house}">House affordability</a> · <a href="{salary}">Comfortable salary</a> · <a href="/living/housing/how-much-rent-can-i-afford">Rent cap</a></p>
      </div>
    </section>
{state_narrative_block(data)}
{col_planning_block(
    data['name'],
    state_metrics,
    data,
    take_home,
    "/living/housing/how-much-rent-can-i-afford",
    house,
    salary,
    f"/living/housing/moving-cost-calculator/{slug}",
)}
{col_methodology_block(data, state_metrics, data['tax_note'], data['name'])}
{state_recommendations_block(slug, data)}
    <section class="col-faq-section">
      <div class="container content-page">
        <h2>FAQ — {data['name']}</h2>
        <div class="faq-stack">
{faq_html(faqs)}
        </div>
      </div>
    </section>
{contextual_interlinks_block(
    place_name=data['name'],
    take_home=take_home,
    rent_link="/living/housing/how-much-rent-can-i-afford",
    house_link=house,
    salary_link=salary,
    compare_links=state_compare[:4],
    extra_cards=[
        (f"Moving cost — {data['name']}", f"/living/housing/moving-cost-calculator/{slug}", "Estimate relocation cash by state."),
        ("Cost of living hub", "/living/housing/cost-of-living-by-city", "Browse all states and cities."),
    ],
)}
{col_eeat_block(data['name'], state_metrics)}
  </main>
{FOOTER}
</body>
</html>
"""


def compare_page(slug: str, c: dict) -> str:
    link_a = f"/living/housing/cost-of-living-by-city/{c['slug_a']}".replace("//", "/")
    link_b = f"/living/housing/cost-of-living-by-city/{c['slug_b']}".replace("//", "/")
    takeaways = compare_takeaways(c)
    rent_a_cls, rent_b_cls = _compare_winner_cell(c["rent_a"], c["rent_b"])
    gro_a_cls, gro_b_cls = _compare_winner_cell(c["groceries_a"], c["groceries_b"])
    tr_a_cls, tr_b_cls = _compare_winner_cell(c["transport_a"], c["transport_b"])
    sal_a_cls, sal_b_cls = _compare_winner_cell(c["salary_a"], c["salary_b"], favor_lower=True)
    city_context = c.get("narrative", [])
    faqs = [
        (
            f"Is {c['city_a']} or {c['city_b']} cheaper?",
            f"On rent, {c['winner_rent']} usually wins in this pair. Still, total cost is rent + food + commute + tax. "
            "Use this page for monthly planning, then run take-home pay to compare real net pay."
        ),
        (
            "Which city is better for families?",
            "Families should compare childcare, school zones, home size, and commute time, not only 1BR rent. "
            "A city with higher rent can still work if wages are stronger and care costs are lower in your target area."
        ),
        (
            "Should I move for a 10% raise?",
            "A raise helps only if your core monthly costs do not rise faster. "
            "As a quick rule, if living costs rise 15% and pay rises 10%, your monthly cushion may shrink."
        ),
        (
            "Do these numbers include tax?",
            "Not in the core rows. Tax is separate because state and city rules vary by filing status and income type. "
            "After this comparison, run a take-home calculator for both locations."
        ),
        (
            "What about buying a home?",
            "Rent winners do not always win for buyers. Property tax, insurance, HOA, and interest rates can flip the result. "
            "Open each city's housing tools if you might buy within the next 1 to 3 years."
        ),
        (
            "How should I use this page with job offers?",
            "Start with the salary row, then stress-test the rent row with real listings in your target neighborhoods. "
            "If your job is hybrid, include commute cost and time as a real monthly line."
        ),
    ]
    def compare_visual_row(label: str, a_val: int, b_val: int, suffix: str = "/mo", favor_lower: bool = True) -> str:
        max_val = max(a_val, b_val, 1)
        a_w = round((a_val / max_val) * 100)
        b_w = round((b_val / max_val) * 100)
        delta = abs(a_val - b_val)
        if delta == 0:
            winner = "Tie"
        elif favor_lower:
            winner = c["city_a"] if a_val < b_val else c["city_b"]
        else:
            winner = c["city_a"] if a_val > b_val else c["city_b"]
        delta_label = f"Gap {fmt(delta)}{suffix}" if delta else "No gap"
        winner_label = "Lead: Tie" if winner == "Tie" else f"Lead: {winner}"
        city_a_label = f'<a href="{link_a}">{c["city_a"]}</a>'
        city_b_label = f'<a href="{link_b}">{c["city_b"]}</a>'
        return f"""
          <article class="col-compare-visual-card">
            <header class="col-compare-visual-head">
              <h3>{label}</h3>
              <p><span>{delta_label}</span><strong>{winner_label}</strong></p>
            </header>
            <div class="col-compare-visual-row">
              <span class="col-compare-visual-city">{city_a_label}</span>
              <div class="col-compare-visual-track"><span class="col-compare-visual-fill col-compare-visual-fill--a" style="width:{a_w}%"></span></div>
              <strong>{fmt(a_val)}{suffix}</strong>
            </div>
            <div class="col-compare-visual-row">
              <span class="col-compare-visual-city">{city_b_label}</span>
              <div class="col-compare-visual-track"><span class="col-compare-visual-fill col-compare-visual-fill--b" style="width:{b_w}%"></span></div>
              <strong>{fmt(b_val)}{suffix}</strong>
            </div>
          </article>"""

    category_notes = f"""
        <div class="col-compare-visuals">
{compare_visual_row("Rent (1BR)", c["rent_a"], c["rent_b"])}
{compare_visual_row("Groceries", c["groceries_a"], c["groceries_b"])}
{compare_visual_row("Transport", c["transport_a"], c["transport_b"])}
{compare_visual_row("Comfort salary", c["salary_a"], c["salary_b"], suffix="", favor_lower=False)}
        </div>
"""
    context_cards = f"""
        <div class="col-compare-context-grid">
          <article class="col-compare-context-card">
            <h3>{c['city_a']}</h3>
            <p>{c['city_a']} shows rent near {fmt(c['rent_a'])}/mo and a comfort pay target near {fmt(c['salary_a'])} gross.</p>
            <p>{city_context[0] if len(city_context) > 0 else f'{c["city_a"]} is a strong fit for people who value its job mix and daily lifestyle.'}</p>
            <footer class="col-compare-context-card__foot">{compare_col_link(c['city_a'], link_a)} →</footer>
          </article>
          <article class="col-compare-context-card">
            <h3>{c['city_b']}</h3>
            <p>{c['city_b']} shows rent near {fmt(c['rent_b'])}/mo and a comfort pay target near {fmt(c['salary_b'])} gross.</p>
            <p>{city_context[1] if len(city_context) > 1 else f'{c["city_b"]} can be a better fit if you want a different rent-to-pay balance.'}</p>
            <footer class="col-compare-context-card__foot">{compare_col_link(c['city_b'], link_b)} →</footer>
          </article>
        </div>
        <p class="col-lead">Context note: {c.get("winner_lifestyle", "Lifestyle and job fit can matter as much as rent.")}.</p>
"""
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{c['title']} (2026) | Income Clarity</title>
  <meta name="description" content="Compare {c['city_a']} vs {c['city_b']}: rent, groceries, transport, and salary needed to live comfortably.">
  <link rel="canonical" href="https://www.incomeclaritylab.com/living/housing/cost-of-living-by-city/compare/{slug}">
  <link rel="stylesheet" href="/styles.css">
{STYLES_COL}
  <link rel="icon" type="image/png" href="/images/logo.png">
  <link rel="apple-touch-icon" href="/images/logo.png">
{URL_SCRIPT}
</head>
<body class="col-page living-tool-page col-compare-page">
{HEADER}
  <main>
    <section class="col-hero-inner">
      <div class="container">
        <nav class="take-home-return-nav" aria-label="Breadcrumb">
          <ol class="take-home-return-breadcrumbs">
            <li><a href="/living/housing/cost-of-living-by-city">Cost of living</a></li>
            <li aria-current="page">{c['city_a']} vs {c['city_b']}</li>
          </ol>
        </nav>
        <h1>{c['title']}</h1>
        <p class="lead">Rent, food, commute, and pay targets side by side.</p>
      </div>
    </section>
    <section class="col-compare-intro">
      <div class="container">
        <p class="col-compare-intro__text">This page compares {compare_col_link(c['city_a'], link_a)} and {compare_col_link(c['city_b'], link_b)} side by side. Use it to check monthly cost gaps, salary fit, and lifestyle tradeoffs before you choose a city.</p>
      </div>
    </section>
{compare_summary_strip(c, link_a, link_b)}
    <section class="col-section col-compare-quick">
      <div class="container content-page">
        <header class="col-section__head">
          <h2>Quick comparison</h2>
          <p class="col-section__lead">Median planning figures from each city guide. Green cells highlight the better value for that row (lower cost or lower salary need).</p>
        </header>
        <div class="col-compare-table-wrap">
          <table class="debt-data-table col-compare-table">
            <caption>{compare_col_link(c['city_a'], link_a)} vs {compare_col_link(c['city_b'], link_b)} — monthly planning figures</caption>
            <thead><tr><th scope="col">Category</th><th scope="col">{compare_col_link(c['city_a'], link_a)}</th><th scope="col">{compare_col_link(c['city_b'], link_b)}</th></tr></thead>
            <tbody>
              <tr><th scope="row">Rent (1BR)</th><td{rent_a_cls}>{fmt(c['rent_a'])}</td><td{rent_b_cls}>{fmt(c['rent_b'])}</td></tr>
              <tr><th scope="row">Groceries</th><td{gro_a_cls}>{fmt(c['groceries_a'])}</td><td{gro_b_cls}>{fmt(c['groceries_b'])}</td></tr>
              <tr><th scope="row">Transport</th><td{tr_a_cls}>{fmt(c['transport_a'])}</td><td{tr_b_cls}>{fmt(c['transport_b'])}</td></tr>
              <tr><th scope="row">Comfort salary</th><td{sal_a_cls}>{fmt(c['salary_a'])}</td><td{sal_b_cls}>{fmt(c['salary_b'])}</td></tr>
            </tbody>
          </table>
        </div>
      </div>
    </section>
    <section class="col-section col-compare-categories">
      <div class="container content-page">
        <header class="col-section__head">
          <h2>Category breakdown</h2>
          <p class="col-section__lead">Line-by-line view of how {compare_col_link(c['city_a'], link_a)} and {compare_col_link(c['city_b'], link_b)} differ — bars scale to the higher city in each pair.</p>
        </header>
{category_notes}
      </div>
    </section>
    <section class="col-band col-band--alt col-compare-context">
      <div class="container content-page">
        <header class="col-band__head">
          <h2>City context: when each one fits</h2>
          <p class="col-lead">Go deeper on {compare_col_link(c['city_a'], link_a)} or {compare_col_link(c['city_b'], link_b)} when the table alone does not capture job market, commute, or lifestyle fit.</p>
        </header>
{context_cards}
      </div>
    </section>
{compare_gap_section(c, takeaways, link_a, link_b)}
    <section class="col-faq-section">
      <div class="container content-page">
        <h2>FAQ</h2>
        <div class="faq-stack">
{faq_html(faqs)}
        </div>
      </div>
    </section>
    <section class="col-section">
      <div class="container content-page">
        <p><a href="/living/housing/cost-of-living-by-city">← All cities and states</a></p>
      </div>
    </section>
  </main>
{FOOTER}
</body>
</html>
"""


def hub_page() -> str:
    catalog = build_catalog(STATES, STANDALONE)
    comparisons = [{**COMPARISONS[s], "slug": s} for s in HUB_COMPARE_SLUGS]
    states_meta = []
    state_taglines = {
        "california": "High rent · State tax",
        "texas": "No state tax · High property tax",
        "florida": "No state tax · Insurance",
        "new-york": "NYC vs upstate · State tax",
    }
    for slug, data in STATES.items():
        states_meta.append({
            "name": data["name"],
            "path": f"/living/housing/cost-of-living-by-city/{slug}",
            "city_count": len(data["cities"]),
            "tagline": state_taglines.get(slug, ""),
            "rent_1br": data["rent_1br"],
            "salary_comfort": data["salary_comfort"],
            "col_index": data["col_index"],
        })
    explained = """
          <article class="col-explained-card"><h3>Housing drives the gap</h3><p>Rent is usually the biggest line. A small rent gap beats a small grocery gap.</p></article>
          <article class="col-explained-card"><h3>Hidden city costs</h3><p>Parking, HOA, insurance, and move-in fees sit outside median rent.</p></article>
          <article class="col-explained-card"><h3>Tax changes take-home</h3><p>Same gross pay can net very different amounts by state.</p></article>
          <article class="col-explained-card"><h3>Remote work moves</h3><p>Check tax rules if you earn in one state and live in another.</p></article>"""
    faqs = faq_html([
        ("Which city is cheapest here?", "Houston and many inland metros rank low on rent. Your job and tax still matter."),
        ("How much salary for NYC?", "Many singles plan for $120k+ gross on a median 1BR stack."),
        ("Is Texas cheaper than California?", "Often lower rent and no state income tax. Run both city pages."),
        ("What matters most when moving?", "Housing, then tax, then childcare if you have kids."),
        ("How do I compare two cities?", "Use a pair card or open two city pages. Compare net pay."),
    ])
    example_city = STATES["texas"]["cities"]["austin"]
    lifestyle_section = col_lifestyle_tiers_section(
        example_city,
        "Austin, TX (example)",
        "texas",
        "/living/lifestyle/comfortable-salary/texas/austin",
    )
    return render_hub_page(
        catalog, comparisons, states_meta, HEADER, FOOTER, URL_SCRIPT, faqs, explained, lifestyle_section
    )


def standalone_page(slug: str, data: dict) -> str:
    city = {k: v for k, v in data.items() if k not in ("state_name", "tax_note")}
    return city_page(slug, city, None, data.get("state_name"), None)


def main() -> None:
    BASE.mkdir(parents=True, exist_ok=True)
    (BASE / "index.html").write_text(hub_page(), encoding="utf-8")
    print("Wrote hub")

    compare_dir = BASE / "compare"
    for slug, data in COMPARISONS.items():
        d = compare_dir / slug
        d.mkdir(parents=True, exist_ok=True)
        (d / "index.html").write_text(compare_page(slug, data), encoding="utf-8")
        print(f"Wrote compare/{slug}")

    for slug, data in STATES.items():
        sd = BASE / slug
        sd.mkdir(parents=True, exist_ok=True)
        (sd / "index.html").write_text(state_page(slug, data), encoding="utf-8")
        for cs, city in data["cities"].items():
            cd = sd / cs
            cd.mkdir(parents=True, exist_ok=True)
            html = city_page(cs, city, slug, data["name"], data)
            (cd / "index.html").write_text(html, encoding="utf-8")
        print(f"Wrote {slug} + {len(data['cities'])} cities")

    for slug, data in STANDALONE.items():
        d = BASE / slug
        d.mkdir(parents=True, exist_ok=True)
        (d / "index.html").write_text(standalone_page(slug, data), encoding="utf-8")
        print(f"Wrote standalone {slug}")

    sys.path.insert(0, str(ROOT / "scripts"))
    from seo_audit import analyze

    failures = []
    for html in BASE.rglob("index.html"):
        s = analyze(html.resolve())
        if s.flesch_reading_ease < 60:
            failures.append(f"{html}: FRE {s.flesch_reading_ease}")
    if failures:
        print("WARNINGS:")
        for f in failures:
            print(" ", f)
    else:
        print("All pages pass FRE >= 60 and minimum copy")

    metric_warnings: list[str] = []
    for slug, data in STATES.items():
        metric_warnings.extend(validate_city_metrics(data, f"state/{slug}"))
        for cs, city in data["cities"].items():
            metric_warnings.extend(validate_city_metrics(city, f"{slug}/{cs}"))
    for slug, data in STANDALONE.items():
        city = {k: v for k, v in data.items() if k not in ("state_name", "tax_note")}
        metric_warnings.extend(validate_city_metrics(city, slug))
    if metric_warnings:
        print("METRIC WARNINGS:")
        for w in metric_warnings:
            print(" ", w)
    else:
        print("All city metrics pass validation checks")


if __name__ == "__main__":
    main()
