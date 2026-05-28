#!/usr/bin/env python3
"""Generate cost-of-living-by-city hub, state, city, and comparison pages."""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from col_hub_content import build_catalog, render_hub_page  # noqa: E402

STYLES_COL = '  <link rel="stylesheet" href="/styles-col.css">'
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
      <a class="logo" href="/index.html">Income Clarity</a>
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
    return "\n".join(
        f'          <article class="faq-item"><h3>{q}</h3><p>{a}</p></article>'
        for q, a in faqs
    )


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
            "No state income tax does not apply here. Budget for state tax when you compare offers from Texas or Florida.",
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
        "salary_link": "/living/family-budgeting/salary-needed-to-live-comfortably",
        "tax_note": "Moderate state income tax; summer cooling bills run high",
    },
}

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


def compare_takeaways(c: dict) -> list[str]:
    return [
        f"{c['city_a']} rent is {fmt(c['rent_a'])} a month. {c['city_b']} rent is {fmt(c['rent_b'])} a month.",
        f"Lower rent often goes to {c['winner_rent']}.",
        f"Pay targets are {fmt(c['salary_a'])} vs {fmt(c['salary_b'])} in gross pay. Check tax on net pay.",
        "Add kids, debt, and buy vs rent goals before you move for a small rent gap.",
    ]


def related_links_block(links: list[tuple[str, str]]) -> str:
    items = "\n".join(f'          <li><a href="{href}">{label}</a></li>' for label, href in links)
    return f"""
    <section class="col-section col-related" aria-labelledby="col-related-title">
      <div class="container content-page">
        <h2 id="col-related-title">Related guides</h2>
        <ul class="col-related__list">
{items}
        </ul>
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
    core = city["rent_1br"] + city["groceries"] + city["utilities"] + city["transport"]
    key_points = city.get("key_points") or city_key_points(city, state_name)
    faqs = city.get(
        "faqs",
        [
            (
                f"How much do I need to earn in {city['name']}?",
                f"Many singles plan around {fmt(city['salary_comfort'])} gross to cover core bills with some saving room. "
                f"Families often plan closer to {fmt(city['family_4'])} gross before childcare, debt, and medical costs."
            ),
            (
                f"Is {city['name']} expensive?",
                f"The city index is {city['col_index']} with US = 100. That means {city['name']} can feel above average or near average based on your rent tier and commute style. "
                "Compare this page with one peer city to judge the real gap."
            ),
            (
                "What counts in cost of living on this page?",
                "Core lines are rent, groceries, utilities, and transport. We show them in monthly dollars for quick planning. "
                "Add debt payments, childcare, healthcare premiums, and savings goals to get your real budget."
            ),
            (
                "Should I use gross or net pay?",
                "Use take-home pay when you set a rent cap. Gross pay is useful for broad planning, but net pay decides monthly comfort. "
                "Run your local take-home calculator after this page."
            ),
            (
                f"What is the lifestyle score in {city['name']}?",
                f"It is {city['lifestyle_score']}/100 in our model. Higher means your income usually stretches further after core bills. "
                "It is a cost-pressure signal, not a quality-of-life score."
            ),
            (
                "Can roommates lower my number?",
                "Yes. Shared rent can drop your housing burden fast. Still include utilities, parking, fees, and move-in costs when you compare listings."
            ),
            (
                "How should I use this page before moving?",
                "Use this sequence: estimate take-home pay, set a rent cap, compare two neighborhoods, then pressure-test your budget with debt and savings. "
                "Do not rely on one listing price alone."
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
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{city['name']} Cost of Living: Rent, Salary &amp; Budget (2026) | Income Clarity</title>
  <meta name="description" content="Cost of living in {city['name']}: rent near {fmt(city['rent_1br'])}/mo, groceries, transport, salary near {fmt(city['salary_comfort'])}, and lifestyle score.">
  <link rel="canonical" href="https://incomeclarity.com/living/housing/cost-of-living-by-city/{page_path}">
  <link rel="stylesheet" href="/styles.css">
{STYLES_COL}
  <link rel="icon" type="image/svg+xml" href="/favicon.svg">
{URL_SCRIPT}
</head>
<body class="col-page col-city-page">
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
    <section class="col-band">
      <div class="container">
        <h2>Monthly cost breakdown</h2>
{cost_cards(city['rent_1br'], city['groceries'], city['utilities'], city['transport'], tax)}
      </div>
    </section>
    <section class="col-band col-band--alt">
      <div class="container">
        <h2>At a glance</h2>
{key_points_html(key_points)}
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
    <section class="col-faq-section">
      <div class="container content-page">
        <h2>FAQ — {city['name']}</h2>
        <div class="faq-stack">
{faq_html(faqs)}
        </div>
      </div>
    </section>
{related_links_block(related)}
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
    salary = {
        "california": "/living/lifestyle-family/comfortable-salary-california",
        "texas": "/living/lifestyle-family/comfortable-salary-texas",
        "florida": "/living/family-budgeting/salary-needed-to-live-comfortably",
    }.get(slug, "/living/family-budgeting/salary-needed-to-live-comfortably")
    related = [
        ("How much house can I afford", house),
        ("Cost of living hub", "/living/housing/cost-of-living-by-city"),
        ("Rent affordability", "/living/housing/how-much-rent-can-i-afford"),
        ("Comfortable salary", salary),
    ]
    city_blurbs = "\n".join(
        f'        <p class="col-city-snap"><a href="/living/housing/cost-of-living-by-city/{slug}/{cs}"><strong>{c["name"]}</strong></a> — index {c["col_index"]}, rent {fmt(c["rent_1br"])}/mo, pay {fmt(c["salary_comfort"])}</p>'
        for cs, c in data["cities"].items()
    )
    faqs = [
        (f"What is rent like in {data['name']}?", f"Typical rent is near {fmt(data['rent_1br'])} a month. Coast and inland areas differ."),
        (f"How much pay do I need in {data['name']}?", f"Many singles plan for {fmt(data['salary_comfort'])} or more in gross pay."),
        (f"How does {data['name']} compare to Texas?", "Texas often has lower rent and no state income tax. Compare your net pay."),
        ("What is the cost index?", "It blends rent, food, power, and car costs. US norm is 100."),
        ("Should I rent or buy?", "Run our rent vs buy tool with local tax and insurance."),
    ]
    if slug != "california":
        faqs[2] = (f"Is {data['name']} cheaper than California?", "Often yes on rent. Compare your job pay and tax on net pay.")
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{data['name']} Cost of Living by City | Income Clarity</title>
  <meta name="description" content="Compare cost of living in {data['name']}: average rent, groceries, taxes, utilities, and top cities ranked.">
  <link rel="canonical" href="https://incomeclarity.com/living/housing/cost-of-living-by-city/{slug}">
  <link rel="stylesheet" href="/styles.css">
{STYLES_COL}
  <link rel="icon" type="image/svg+xml" href="/favicon.svg">
{URL_SCRIPT}
</head>
<body class="col-page">
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
        <p class="col-lead">Cost index is <strong>{data['col_index']}</strong> (US norm is 100). Many singles plan for <strong>{fmt(data['salary_comfort'])}</strong> in gross pay.</p>
{key_points_html(state_key_points(data))}
      </div>
    </section>
    <section class="col-band col-band--alt">
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
{city_blurbs}
        <p class="col-lead">Tools: <a href="{house}">House affordability</a> · <a href="{salary}">Comfortable salary</a> · <a href="/living/housing/how-much-rent-can-i-afford">Rent cap</a></p>
      </div>
    </section>
    <section class="col-faq-section">
      <div class="container content-page">
        <h2>FAQ — {data['name']}</h2>
        <div class="faq-stack">
{faq_html(faqs)}
        </div>
      </div>
    </section>
{related_links_block(related)}
  </main>
{FOOTER}
</body>
</html>
"""


def compare_page(slug: str, c: dict) -> str:
    link_a = f"/living/housing/cost-of-living-by-city/{c['slug_a']}".replace("//", "/")
    link_b = f"/living/housing/cost-of-living-by-city/{c['slug_b']}".replace("//", "/")
    takeaways = compare_takeaways(c)
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
        return f"""
          <article class="col-compare-visual-card">
            <header class="col-compare-visual-head">
              <h3>{label}</h3>
              <p><span>{delta_label}</span><strong>{winner_label}</strong></p>
            </header>
            <div class="col-compare-visual-row">
              <span class="col-compare-visual-city">{c['city_a']}</span>
              <div class="col-compare-visual-track"><span class="col-compare-visual-fill col-compare-visual-fill--a" style="width:{a_w}%"></span></div>
              <strong>{fmt(a_val)}{suffix}</strong>
            </div>
            <div class="col-compare-visual-row">
              <span class="col-compare-visual-city">{c['city_b']}</span>
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
            <h3>{c['city_a']} profile</h3>
            <p>{c['city_a']} shows rent near {fmt(c['rent_a'])}/mo and a comfort pay target near {fmt(c['salary_a'])} gross.</p>
            <p>{city_context[0] if len(city_context) > 0 else f'{c["city_a"]} is a strong fit for people who value its job mix and daily lifestyle.'}</p>
            <p><a href="{link_a}">Open {c['city_a']} city guide →</a></p>
          </article>
          <article class="col-compare-context-card">
            <h3>{c['city_b']} profile</h3>
            <p>{c['city_b']} shows rent near {fmt(c['rent_b'])}/mo and a comfort pay target near {fmt(c['salary_b'])} gross.</p>
            <p>{city_context[1] if len(city_context) > 1 else f'{c["city_b"]} can be a better fit if you want a different rent-to-pay balance.'}</p>
            <p><a href="{link_b}">Open {c['city_b']} city guide →</a></p>
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
  <link rel="canonical" href="https://incomeclarity.com/living/housing/cost-of-living-by-city/compare/{slug}">
  <link rel="stylesheet" href="/styles.css">
{STYLES_COL}
  <link rel="icon" type="image/svg+xml" href="/favicon.svg">
{URL_SCRIPT}
</head>
<body class="col-page col-compare-page">
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
        <p class="col-lead">This page helps you compare {c['city_a']} and {c['city_b']} for a real move decision. Use it to check monthly cost gaps, salary fit, and lifestyle tradeoffs before you choose a city.</p>
      </div>
    </section>
    <section class="col-section">
      <div class="container content-page">
        <h2>Quick comparison</h2>
        <div class="col-compare-table-wrap">
          <table class="debt-data-table">
            <caption>{c['city_a']} vs {c['city_b']} monthly planning figures</caption>
            <thead><tr><th scope="col">Category</th><th scope="col">{c['city_a']}</th><th scope="col">{c['city_b']}</th></tr></thead>
            <tbody>
              <tr><th scope="row">Rent (1BR)</th><td>{fmt(c['rent_a'])}</td><td>{fmt(c['rent_b'])}</td></tr>
              <tr><th scope="row">Groceries</th><td>{fmt(c['groceries_a'])}</td><td>{fmt(c['groceries_b'])}</td></tr>
              <tr><th scope="row">Transport</th><td>{fmt(c['transport_a'])}</td><td>{fmt(c['transport_b'])}</td></tr>
              <tr><th scope="row">Comfort salary</th><td>{fmt(c['salary_a'])}</td><td>{fmt(c['salary_b'])}</td></tr>
            </tbody>
          </table>
        </div>
        <p><a href="{link_a}">{c['city_a']} cost of living</a> · <a href="{link_b}">{c['city_b']} cost of living</a></p>
      </div>
    </section>
    <section class="col-section">
      <div class="container content-page">
        <h2>Category breakdown</h2>
{category_notes}
      </div>
    </section>
    <section class="col-band col-band--alt">
      <div class="container content-page">
        <h2>City context: when each one fits</h2>
{context_cards}
      </div>
    </section>
    <section class="col-band col-band--alt">
      <div class="container">
        <h2>What the gap means</h2>
{key_points_html(takeaways + c.get("narrative", [])[:2])}
      </div>
    </section>
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
    return render_hub_page(catalog, comparisons, states_meta, HEADER, FOOTER, URL_SCRIPT, faqs, explained)


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


if __name__ == "__main__":
    main()
