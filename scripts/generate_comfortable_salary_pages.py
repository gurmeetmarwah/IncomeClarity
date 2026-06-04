#!/usr/bin/env python3
"""Generate comfortable salary hub, state, and city pages."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

from comfortable_salary_data import (  # noqa: E402
    BASE,
    COMPARE_PAIRS,
    FEATURED_CITIES,
    FEATURED_STATES,
    HUB_PATH,
    HOUSEHOLD,
    HOUSING,
    LIFESTYLE_TIERS,
    PROFILES,
    STANDALONE,
    STANDALONE_STATE,
    STATES,
    affordability_score,
    build_catalog,
    catalog_json,
    compute_salary,
    fmt,
    lifestyle_range,
    salary_link,
    validate_catalog,
)
from generate_col_by_city_pages import (  # noqa: E402
    city_know_points,
    col_know_block,
    col_methodology_block,
    core_monthly,
    prepare_city_metrics,
)

HUB_OUT = ROOT / "living" / "lifestyle" / "comfortable-salary-us"
STATE_OUT = ROOT / "living" / "lifestyle" / "comfortable-salary"

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


def hero_breadcrumbs(crumbs: list[tuple[str, str | None]]) -> str:
    """Build breadcrumb nav; pass (label, href) or (label, None) for current page."""
    items = []
    for label, href in crumbs:
        if href:
            items.append(f'          <li><a href="{href}">{label}</a></li>')
        else:
            items.append(f'          <li aria-current="page">{label}</li>')
    inner = "\n".join(items)
    return f"""        <nav class="take-home-return-nav" aria-label="Breadcrumb">
          <ol class="take-home-return-breadcrumbs">
{inner}
          </ol>
        </nav>"""


def head(title: str, desc: str, canonical: str, body_attrs: str = "") -> str:
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title}</title>
  <meta name="description" content="{desc}">
  <meta name="robots" content="index,follow">
  <link rel="canonical" href="https://www.incomeclaritylab.com{canonical}">
  <link rel="stylesheet" href="/styles.css">
  <link rel="stylesheet" href="/styles-living-system.css">
  <link rel="stylesheet" href="/styles-col.css">
  <link rel="stylesheet" href="/styles-comfortable-salary.css">
  <link rel="icon" type="image/png" href="/images/logo.png">
  <link rel="apple-touch-icon" href="/images/logo.png">
{URL_SCRIPT}
</head>
<body class="cs-page living-tool-page"{body_attrs}>"""


def faq_html(faqs: list[tuple[str, str]]) -> str:
    blocks = []
    for q, a in faqs:
        paragraphs = "".join(f"<p>{part.strip()}</p>" for part in a.split("\n\n") if part.strip())
        blocks.append(f'          <article class="faq-item"><h3>{q}</h3>{paragraphs}</article>')
    return "\n".join(blocks)


def calc_form() -> str:
    return f"""
        <form class="cs-calc-shell" id="cs-calc-form">
          <div class="cs-calc-grid">
            <label class="cs-field"><span>State</span><select id="cs-state" required></select></label>
            <label class="cs-field"><span>City</span><select id="cs-city"></select></label>
            <label class="cs-field"><span>Household</span>
              <select id="cs-household">
                <option value="single">Single</option>
                <option value="couple">Couple</option>
                <option value="family4">Family of 4</option>
              </select>
            </label>
            <label class="cs-field"><span>Housing</span>
              <select id="cs-housing">
                <option value="rent">Rent</option>
                <option value="own">Own</option>
              </select>
            </label>
          </div>
          <button type="submit" class="cs-btn">Calculate My Comfortable Salary</button>
        </form>
        <script type="application/json" id="cs-catalog">{catalog_json()}</script>"""


def lifestyle_estimate_section(
    city: dict,
    state_slug: str,
    location_name: str,
    household: str = "single",
    housing: str = "rent",
) -> str:
    """Server-rendered lifestyle tiers (matches hub calculator output)."""
    tiers = lifestyle_range(city, household, housing, state_slug)
    comfort = compute_salary(city, household, housing, "comfortable", state_slug)
    breakdown = comfort["breakdown"]

    tier_cards = []
    for key in LIFESTYLE_TIERS:
        featured = " cs-tier-card--featured" if key == "comfortable" else ""
        tier_cards.append(
            f'            <article class="cs-tier-card{featured}">'
            f'<strong>{LIFESTYLE_TIERS[key]["label"]}</strong>'
            f'<span id="cs-tier-{key}">{fmt(tiers[key])}</span></article>'
        )
    tier_html = "\n".join(tier_cards)

    mix_rows = ""
    for key, label in [
        ("housing", "Housing"),
        ("transportation", "Transportation"),
        ("food", "Food"),
        ("childcare", "Childcare"),
        ("savings", "Savings"),
        ("lifestyle", "Lifestyle Spending"),
    ]:
        b = breakdown.get(key, {"amount": 0, "pct": 0})
        mix_rows += f"""            <div class="cs-mix-row">
              <span>{label}</span>
              <div class="cs-mix-bar"><span id="cs-mix-{key}-bar" style="width:{b['pct']}%"></span></div>
              <span id="cs-mix-{key}-pct">{b['pct']}%</span>
            </div>
"""

    hh = HOUSEHOLD[household]["label"]
    ho = HOUSING[housing]["label"]
    tier_min = fmt(tiers["basic"])
    tier_max = fmt(tiers["high_comfort"])

    return f"""    <section class="cs-band cs-band--alt" id="cs-results" aria-labelledby="cs-results-title">
      <div class="container container--wide">
        <header class="cs-band__head">
          <h2 id="cs-results-title">Comfortable salary estimate</h2>
          <p>Targets for <span id="cs-result-location">{location_name}</span>. Each figure is gross annual pay before tax for a <strong>{hh.lower()}</strong> who <strong>{ho.lower()}s</strong>.</p>
        </header>
        <p class="cs-tier-context">Lifestyle tiers span {tier_min} (basic) to {tier_max} (affluent). The highlighted tier is our default comfortable lifestyle with room to save.</p>
        <div class="cs-tier-grid">
{tier_html}
        </div>
      </div>
    </section>
    <section class="cs-band" id="cs-breakdown" aria-labelledby="cs-breakdown-title">
      <div class="container container--wide">
        <header class="cs-band__head"><h2 id="cs-breakdown-title">Salary breakdown</h2><p>Where your monthly budget goes at the <strong>comfortable</strong> lifestyle tier ({fmt(comfort['annual'])} gross).</p></header>
        <div class="cs-mix-grid">{mix_rows}
        </div>
      </div>
    </section>"""


def results_sections() -> str:
    """Hub default — pre-filled with Texas state median; JS updates on calculator change."""
    return lifestyle_estimate_section(STATES["texas"], "texas", "Texas (example)")


def calc_block() -> str:
    return calc_form() + results_sections()


def profile_cards(city: dict, state_slug: str) -> str:
    cards = []
    for hh_key, title, desc in PROFILES:
        amt = compute_salary(city, hh_key, "rent", "comfortable", state_slug)["annual"]
        cards.append(
            f'          <article class="cs-card"><h3>{title}</h3><p>{desc}</p><span class="cs-card-salary">Recommended: {fmt(amt)}</span></article>'
        )
    return "\n".join(cards)


def state_cards() -> str:
    cards = []
    for slug in FEATURED_STATES:
        if slug == "illinois":
            city = STANDALONE["chicago"]
            st_name = "Illinois"
            rent = city["rent_1br"]
            comfort = compute_salary(city, "single", "rent", "comfortable", slug)["annual"]
            score = affordability_score(city, slug)
        else:
            st = STATES[slug]
            st_name = st["name"]
            rent = st["rent_1br"]
            comfort = compute_salary(st, "single", "rent", "comfortable", slug)["annual"]
            score = affordability_score(st, slug)
        cards.append(
            f'          <a class="cs-card" href="{salary_link(slug)}"><h3>{st_name}</h3>'
            f'<p class="cs-card-meta">Median housing · affordability score {score}/100</p>'
            f'<span class="cs-card-salary">{fmt(comfort)} comfortable</span>'
            f'<span class="cs-card-meta">Typical rent {fmt(rent)}/mo</span></a>'
        )
    return "\n".join(cards)


def city_cards() -> str:
    cards = []
    for state_slug, city_slug in FEATURED_CITIES:
        if state_slug == "illinois":
            city = STANDALONE["chicago"]
            name = city["name"]
        elif state_slug == "washington":
            city = STANDALONE["seattle"]
            name = city["name"]
        else:
            city = STATES[state_slug]["cities"][city_slug]
            name = city["name"]
        comfort = compute_salary(city, "single", "rent", "comfortable", state_slug)["annual"]
        cards.append(
            f'          <a class="cs-card" href="{salary_link(state_slug, city_slug)}"><h3>{name}</h3>'
            f'<p>Comfortable salary for a single renter.</p>'
            f'<span class="cs-card-salary">{fmt(comfort)}</span></a>'
        )
    return "\n".join(cards)


def family_table(city: dict, state_slug: str) -> str:
    rows = []
    for hh_key, hh in HOUSEHOLD.items():
        basic = compute_salary(city, hh_key, "rent", "basic", state_slug)["annual"]
        comfort = compute_salary(city, hh_key, "rent", "comfortable", state_slug)["annual"]
        plus = compute_salary(city, hh_key, "rent", "comfortable_plus", state_slug)["annual"]
        rows.append(
            f"            <tr><td>{hh['label']}</td><td>{fmt(basic)}</td><td>{fmt(comfort)}</td><td>{fmt(plus)}</td></tr>"
        )
    return "\n".join(rows)


def whatif_section() -> str:
    return """    <section class="cs-band cs-band--alt" id="cs-whatif" aria-labelledby="cs-whatif-title">
      <div class="container container--wide">
        <header class="cs-band__head"><h2 id="cs-whatif-title">What if scenarios</h2><p>Tap a scenario to update the calculator above.</p></header>
        <div class="cs-whatif-grid">
          <button type="button" class="cs-whatif-btn" data-cs-whatif="texas">What if I move to Texas?</button>
          <button type="button" class="cs-whatif-btn" data-cs-whatif="child">What if I have a child?</button>
          <button type="button" class="cs-whatif-btn" data-cs-whatif="own">What if I buy a home?</button>
          <button type="button" class="cs-whatif-btn" data-cs-whatif="debt">What if I pay off debt?</button>
        </div>
        <p class="cs-whatif-result" id="cs-whatif-result" aria-live="polite"></p>
      </div>
    </section>"""


def drivers_section() -> str:
    drivers = [
        ("Housing costs", "Rent or mortgage usually takes the largest share. A $400 rent gap can mean $8k+ in gross salary."),
        ("Childcare costs", "Full-time care for two kids can add $2,000 to $3,500 per month in many metros."),
        ("Taxes", "State income tax ranges from 0% to 13%+. NYC adds a city tax on top of New York State."),
        ("Healthcare", "Employer plans help. Self-employed households should budget $400 to $800 per month."),
        ("Transportation", "Two-car suburbs cost more than one-car urban life with transit."),
        ("Savings goals", "Comfort usually means saving 10% to 15% of take-home, not just covering bills."),
    ]
    items = "\n".join(
        f'          <article class="cs-driver"><h3>{t}</h3><p>{b}</p></article>' for t, b in drivers
    )
    return f"""    <section class="cs-band" id="cs-drivers" aria-labelledby="cs-drivers-title">
      <div class="container container--wide">
        <header class="cs-band__head"><h2 id="cs-drivers-title">What makes a salary feel comfortable?</h2><p>These cost drivers explain why the same gross pay feels different city to city.</p></header>
        <div class="cs-driver-list">{items}
        </div>
      </div>
    </section>"""


def compare_section() -> str:
    cards = []
    for title, a, b in COMPARE_PAIRS:
        cards.append(f'          <a class="cs-card" href="{HUB_PATH}#cs-compare"><h3>{title}</h3><p>Compare comfortable salary targets side by side in the calculator.</p></a>')
    return f"""    <section class="cs-band cs-band--alt" id="cs-compare" aria-labelledby="cs-compare-title">
      <div class="container container--wide">
        <header class="cs-band__head"><h2 id="cs-compare-title">Compare comfortable salaries</h2><p>Pick two locations in the calculator to see how lifestyle tiers shift.</p></header>
        <div class="cs-compare-grid">
{chr(10).join(cards)}
        </div>
      </div>
    </section>"""


def related_tools_section() -> str:
    cols = [
        ("Housing", [
            ("/living/housing/how-much-rent-can-i-afford", "How much rent can I afford"),
            ("/living/housing/how-much-house-can-i-afford", "How much house can I afford"),
            ("/rent-vs-buy-calculator", "Rent vs buy calculator"),
        ]),
        ("Family", [
            ("/living/lifestyle-family/family-of-4-income-guide/", "Family of 4 budget"),
            ("/living/lifestyle-family/childcare-affordability/", "Childcare affordability"),
        ]),
        ("Cost of living", [
            ("/living/housing/cost-of-living-by-city", "Cost of living by city"),
            ("/living/housing/moving-cost-calculator", "Moving cost calculator"),
        ]),
        ("Debt", [
            ("/credit-card-payoff-calculator", "Credit card payoff scenarios"),
            ("/debt/strategies/average-credit-card-debt-by-income", "Debt by income"),
        ]),
    ]
    html_cols = []
    for title, links in cols:
        items = "\n".join(f"              <li><a href=\"{h}\">{l}</a></li>" for h, l in links)
        html_cols.append(f'          <div class="cs-tool-col"><h3>{title}</h3><ul>{items}\n              </ul></div>')
    return f"""    <section class="cs-band" id="cs-related" aria-labelledby="cs-related-title">
      <div class="container container--wide">
        <header class="cs-band__head"><h2 id="cs-related-title">Related financial decisions</h2><p>Layer housing, family, and debt tools on top of your salary target.</p></header>
        <div class="cs-tool-grid">
{chr(10).join(html_cols)}
        </div>
      </div>
    </section>"""


def cta_section(state_link: str | None = None) -> str:
    state_href = state_link or f"{BASE}/california"
    return f"""    <section class="cs-cta-band" aria-labelledby="cs-cta-title">
      <div class="container container--wide">
        <h2 id="cs-cta-title">Financial comfort starts with knowing your number</h2>
        <p>Pick a state or city to see local salary targets.</p>
        <div class="cs-cta-actions">
          <a href="{state_href}">Explore your state</a>
          <a href="{HUB_PATH}#cs-cities">Compare cities</a>
          <a href="/living/housing/how-much-rent-can-i-afford">Calculate housing affordability</a>
        </div>
      </div>
    </section>"""


HUB_FAQS = [
    (
        "What is considered a comfortable salary in the US?",
        "Comfort means covering housing, food, transport, healthcare, and still saving each month. There is no one national number. A single renter in Houston may feel fine near $70k gross. The same lifestyle in NYC often needs $120k+.",
    ),
    (
        "Is $100k enough to live comfortably?",
        "$100k goes far in Texas or Florida for a couple without heavy debt. In San Francisco or NYC it may only cover basics for a family of four. Run your city and household in the calculator above.",
    ),
    (
        "What salary does a family of 4 need?",
        "Families need more room for housing, food, and childcare. Many US metros land between $85k and $175k gross for a comfortable family budget. Coastal cities sit at the high end.",
    ),
    (
        "Which states require the highest income?",
        "California, New York, and Hawaii often top the list because of rent and taxes. Texas and Florida have no state income tax but insurance and property tax still matter.",
    ),
    (
        "How does housing affect comfortable salary?",
        "Housing is usually 30% to 40% of a comfort budget. Every $500/month in rent adds roughly $10k to $14k in gross salary need after tax.",
    ),
]


def render_hub() -> str:
    breadcrumbs = hero_breadcrumbs(
        [
            ("Living", "/rent-vs-buy-calculator"),
            ("Comfortable salary (US)", None),
        ]
    )
    return f"""{head(
        "What Salary Do You Need to Live Comfortably in the US? | Income Clarity",
        "Estimate a comfortable income by location, family size, housing, and lifestyle. Browse salary targets by state and city.",
        HUB_PATH,
    )}
{HEADER}
  <main>
    <section class="cs-hero">
      <div class="container container--wide">
        <p class="label">Comfortable salary calculator</p>
{breadcrumbs}
        <h1>What salary do you need to live comfortably in the US?</h1>
        <p class="lead">Estimate a comfortable income based on your location, family size, housing costs, and lifestyle goals.</p>
{calc_form()}
      </div>
    </section>

{results_sections()}

    <section class="cs-band" id="cs-profiles" aria-labelledby="cs-profiles-title">
      <div class="container container--wide">
        <header class="cs-band__head"><h2 id="cs-profiles-title">Lifestyle profiles</h2><p>Typical comfortable targets for common household types (US median city mix).</p></header>
        <div class="cs-profile-grid">
{profile_cards({"rent_1br": 1650, "groceries": 400, "utilities": 200, "transport": 330, "col_index": 100}, None)}
        </div>
      </div>
    </section>

    <section class="cs-band cs-band--alt" id="cs-states" aria-labelledby="cs-states-title">
      <div class="container container--wide">
        <header class="cs-band__head"><h2 id="cs-states-title">Salary by state</h2><p>Browse comfortable salary, median housing, and affordability scores.</p></header>
        <div class="cs-state-grid">
{state_cards()}
        </div>
      </div>
    </section>

    <section class="cs-band" id="cs-cities" aria-labelledby="cs-cities-title">
      <div class="container container--wide">
        <header class="cs-band__head"><h2 id="cs-cities-title">Salary by city</h2><p>Featured metros with local rent and lifestyle context.</p></header>
        <div class="cs-city-grid">
{city_cards()}
        </div>
      </div>
    </section>

    <section class="cs-band cs-band--alt" id="cs-family" aria-labelledby="cs-family-title">
      <div class="container container--wide">
        <header class="cs-band__head"><h2 id="cs-family-title">Family size comparison</h2><p>How household size shifts salary need at the US median cost mix.</p></header>
        <table class="cs-family-table">
          <thead><tr><th>Household</th><th>Basic</th><th>Comfortable</th><th>Comfortable Plus</th></tr></thead>
          <tbody>
{family_table({"rent_1br": 1650, "groceries": 400, "utilities": 200, "transport": 330, "col_index": 100}, None)}
          </tbody>
        </table>
      </div>
    </section>

{whatif_section()}
{drivers_section()}
{compare_section()}
{related_tools_section()}

    <section class="cs-band cs-band--alt" id="cs-faq" aria-labelledby="cs-faq-title">
      <div class="container container--wide content-page">
        <header class="cs-band__head"><h2 id="cs-faq-title">FAQ</h2></header>
        <div class="faq-list">
{faq_html(HUB_FAQS)}
        </div>
      </div>
    </section>

{cta_section()}

  </main>
{FOOTER}
  <script src="/comfortable-salary.js"></script>
</body>
</html>"""


def get_state_data(state_slug: str) -> tuple[dict, str]:
    if state_slug in STATES:
        return STATES[state_slug], STATES[state_slug]["name"]
    # Standalone-only states (one metro in catalog)
    for city_slug, mapped in STANDALONE_STATE.items():
        if mapped == state_slug:
            city = STANDALONE[city_slug]
            return {
                "name": city["state_name"],
                "col_index": city["col_index"],
                "rent_1br": city["rent_1br"],
                "groceries": city["groceries"],
                "utilities": city["utilities"],
                "transport": city["transport"],
                "salary_comfort": city["salary_comfort"],
                "tax_note": city.get("tax_note", ""),
                "narrative": [
                    f"{city['name']} anchors this state estimate.",
                    "Suburbs and rural areas may run lower on rent with higher transport costs.",
                ],
                "cities": {city_slug: city},
            }, city["state_name"]
    raise KeyError(state_slug)


def state_drivers_section(
    state_slug: str,
    st: dict,
    st_name: str,
    comfort: int,
    core: int,
    score: int,
) -> str:
    narratives = st.get("narrative", [])
    rank = st.get("rank_intro", "")
    tax = st.get("tax_note", "Varies by state and locality")
    lead = rank or (narratives[0] if narratives else f"Rent, tax, and daily costs shape how much you need to earn in {st_name}.")

    points = "\n".join(f"          <li>{p}</li>" for p in narratives) if narratives else ""
    points_block = (
        f"""
        <ul class="cs-driver-points">
{points}
        </ul>"""
        if points
        else ""
    )

    col_link = (
        f"/living/housing/cost-of-living-by-city/{state_slug}"
        if state_slug in STATES
        else None
    )
    col_footer = (
        f'        <p class="cs-drivers-footer"><a href="{col_link}">See full cost of living in {st_name} →</a></p>'
        if col_link
        else ""
    )

    return f"""    <section class="cs-band" id="cs-state-drivers" aria-labelledby="cs-state-drivers-title">
      <div class="container container--wide">
        <header class="cs-band__head cs-drivers-head">
          <h2 id="cs-state-drivers-title">What drives salary need in {st_name}</h2>
          <p class="cs-drivers-lead">{lead}</p>
        </header>
        <div class="cs-drivers-layout">
          <div class="cs-drivers-copy">
{points_block}
            <aside class="cs-tax-callout" aria-label="Tax note for {st_name}">
              <p class="cs-tax-callout__label">Tax &amp; take-home pay</p>
              <p>{tax}</p>
            </aside>
{col_footer}
          </div>
          <div class="cs-drivers-metrics" role="list">
            <article class="cs-driver-metric" role="listitem">
              <span class="cs-driver-metric__label">Median 1BR rent</span>
              <strong class="cs-driver-metric__value">{fmt(st["rent_1br"])}</strong>
              <span class="cs-driver-metric__hint">/month · housing anchor</span>
            </article>
            <article class="cs-driver-metric" role="listitem">
              <span class="cs-driver-metric__label">Cost-of-living index</span>
              <strong class="cs-driver-metric__value">{st.get("col_index", 100)}</strong>
              <span class="cs-driver-metric__hint">US average = 100</span>
            </article>
            <article class="cs-driver-metric" role="listitem">
              <span class="cs-driver-metric__label">Monthly essentials</span>
              <strong class="cs-driver-metric__value">{fmt(core)}</strong>
              <span class="cs-driver-metric__hint">rent + food + utilities + transport</span>
            </article>
            <article class="cs-driver-metric" role="listitem">
              <span class="cs-driver-metric__label">Comfortable lifestyle</span>
              <strong class="cs-driver-metric__value">{fmt(comfort)}</strong>
              <span class="cs-driver-metric__hint">single renter · gross · see tiers below</span>
            </article>
            <article class="cs-driver-metric cs-driver-metric--score" role="listitem">
              <span class="cs-driver-metric__label">Affordability score</span>
              <strong class="cs-driver-metric__value">{score}<span class="cs-driver-metric__of">/100</span></strong>
              <span class="cs-driver-metric__hint">higher = easier to stretch pay</span>
            </article>
          </div>
        </div>
      </div>
    </section>"""


def state_city_chips(state_slug: str, st: dict) -> str:
    chips = []
    for city_slug, city in st.get("cities", {}).items():
        chips.append(f'          <a href="{salary_link(state_slug, city_slug)}">{city["name"]}</a>')
    for city_slug, mapped in STANDALONE_STATE.items():
        if mapped == state_slug and city_slug not in st.get("cities", {}):
            city = STANDALONE[city_slug]
            chips.append(f'          <a href="{salary_link(state_slug, city_slug)}">{city["name"]}</a>')
    return "\n".join(chips)


def render_state(state_slug: str) -> str:
    st, st_name = get_state_data(state_slug)
    canonical = salary_link(state_slug)
    comfort = compute_salary(st, "single", "rent", "comfortable", state_slug)["annual"]
    tiers = lifestyle_range(st, "single", "rent", state_slug)
    core = core_monthly(st["rent_1br"], st["groceries"], st["utilities"], st["transport"])
    score = affordability_score(st, state_slug)
    tax = st.get("tax_note", "Varies by state")
    body_attrs = f' data-cs-page="state" data-cs-state="{state_slug}"'

    city_rows = ""
    for city_slug, city in st.get("cities", {}).items():
        c_comfort = compute_salary(city, "single", "rent", "comfortable", state_slug)["annual"]
        city_rows += (
            f'          <a class="cs-card" href="{salary_link(state_slug, city_slug)}"><h3>{city["name"]}</h3>'
            f'<p>Rent near {fmt(city["rent_1br"])}/mo</p><span class="cs-card-salary">{fmt(c_comfort)}</span></a>'
        )

    faqs = [
        (
            f"What is a comfortable salary in {st_name}?",
            f"A single renter often needs about {fmt(comfort)} gross for a comfortable lifestyle. Couples and families need more. Use the calculator for your household.",
        ),
        (
            f"How do taxes affect take-home pay in {st_name}?",
            f"{tax}. Convert gross targets to net pay with our take-home calculator before you sign a lease.",
        ),
    ]

    drivers_block = state_drivers_section(state_slug, st, st_name, comfort, core, score)

    return f"""{head(
        f"Comfortable Salary in {st_name} (2026) | Income Clarity",
        f"Comfortable salary estimates for {st_name}. Housing costs, taxes, city breakdowns, and family income targets.",
        canonical,
        body_attrs,
    )}
{HEADER}
  <main>
    <section class="cs-hero">
      <div class="container container--wide">
        <p class="label">Comfortable salary · {st_name}</p>
{hero_breadcrumbs([
            ("Living", "/rent-vs-buy-calculator"),
            ("Comfortable salary (US)", HUB_PATH),
            (st_name, None),
        ])}
        <h1>Comfortable salary in {st_name}</h1>
        <p class="lead">State income targets based on local rent, taxes, and typical monthly costs.</p>
        <div class="cs-stat-row">
          <div class="cs-stat"><strong>{fmt(comfort)}</strong><span>Comfortable lifestyle · single renter</span></div>
          <div class="cs-stat"><strong>{fmt(tiers['basic'])}–{fmt(tiers['high_comfort'])}</strong><span>Basic to affluent range</span></div>
          <div class="cs-stat"><strong>{fmt(st["rent_1br"])}</strong><span>Median 1BR rent</span></div>
          <div class="cs-stat"><strong>{score}/100</strong><span>Affordability score</span></div>
        </div>
        <div class="cs-city-nav">
          <p class="cs-city-nav__label">Browse cities in {st_name}</p>
          <div class="cs-city-chips">{state_city_chips(state_slug, st)}
          </div>
        </div>
{calc_form()}
      </div>
    </section>

{lifestyle_estimate_section(st, state_slug, st_name)}

{drivers_block}

    <section class="cs-band cs-band--alt" aria-labelledby="cs-state-cities-title">
      <div class="container container--wide">
        <header class="cs-band__head"><h2 id="cs-state-cities-title">Top city breakdowns</h2></header>
        <div class="cs-city-grid">
{city_rows}
        </div>
      </div>
    </section>

    <section class="cs-band" aria-labelledby="cs-state-family-title">
      <div class="container container--wide">
        <header class="cs-band__head"><h2 id="cs-state-family-title">Family income recommendations</h2></header>
        <table class="cs-family-table">
          <thead><tr><th>Household</th><th>Basic</th><th>Comfortable</th><th>Comfortable Plus</th></tr></thead>
          <tbody>
{family_table(st, state_slug)}
          </tbody>
        </table>
      </div>
    </section>

{related_tools_section()}

    <section class="cs-band cs-band--alt" id="cs-faq">
      <div class="container container--wide content-page">
        <header class="cs-band__head"><h2>FAQ</h2></header>
        <div class="faq-list">
{faq_html(faqs)}
        </div>
      </div>
    </section>

{cta_section(canonical)}

  </main>
{FOOTER}
  <script src="/comfortable-salary.js"></script>
</body>
</html>"""


def render_city(state_slug: str, city_slug: str) -> str:
    if state_slug == "illinois" and city_slug == "chicago":
        city = STANDALONE["chicago"]
        st_name = "Illinois"
    elif state_slug in STANDALONE_STATE.values() and city_slug in STANDALONE:
        city = STANDALONE[city_slug]
        st_name = city["state_name"]
    else:
        city = STATES[state_slug]["cities"][city_slug]
        st_name = STATES[state_slug]["name"]

    canonical = salary_link(state_slug, city_slug)
    body_attrs = f' data-cs-page="city" data-cs-state="{state_slug}" data-cs-city="{state_slug}/{city_slug}"'

    tiers_single = lifestyle_range(city, "single", "rent", state_slug)
    single = tiers_single["comfortable"]
    couple = compute_salary(city, "couple", "rent", "comfortable", state_slug)["annual"]
    family = compute_salary(city, "family4", "rent", "comfortable", state_slug)["annual"]
    own = compute_salary(city, "single", "own", "comfortable", state_slug)["annual"]
    core = core_monthly(city["rent_1br"], city["groceries"], city["utilities"], city["transport"])

    faqs = [
        (
            f"What salary do singles need in {city['name']}?",
            f"Singles renting a 1-bedroom often need about {fmt(single)} gross for a comfortable budget with savings.",
        ),
        (
            f"What salary does a family need in {city['name']}?",
            f"A family of four with rent and childcare often lands near {fmt(family)} gross for a comfortable tier.",
        ),
    ]

    col_path = (
        f"/living/housing/cost-of-living-by-city/{state_slug}/{city_slug}"
        if state_slug in STATES
        else f"/living/housing/cost-of-living-by-city/{city_slug}"
    )
    move_path = (
        f"/living/housing/moving-cost-calculator/{state_slug}/{city_slug}"
        if state_slug in STATES
        else f"/living/housing/moving-cost-calculator/{city_slug}"
    )

    st_data, _ = get_state_data(state_slug)
    tax = st_data.get("tax_note", city.get("tax_note", "Varies by state and locality"))
    metrics = prepare_city_metrics(city)
    know_block = col_know_block(
        city["name"],
        city_know_points(city, tax),
        lead=f"Local rent, tax, and daily costs drive how much you need to earn in {city['name']}.",
    )
    method_block = col_methodology_block(city, metrics, tax, city["name"])

    return f"""{head(
        f"Comfortable Salary in {city['name']} (2026) | Income Clarity",
        f"Comfortable salary for singles, couples, and families in {city['name']}. Housing, rent vs buy, and cost breakdown.",
        canonical,
        body_attrs,
    )}
{HEADER}
  <main>
    <section class="cs-hero">
      <div class="container container--wide">
        <p class="label">Comfortable salary · {city['name']}</p>
{hero_breadcrumbs([
            ("Living", "/rent-vs-buy-calculator"),
            ("Comfortable salary (US)", HUB_PATH),
            (st_name, salary_link(state_slug)),
            (city["name"], None),
        ])}
        <h1>Comfortable salary in {city['name']}</h1>
        <p class="lead">Local income targets by household type, housing choice, and lifestyle tier.</p>
        <div class="cs-stat-row">
          <div class="cs-stat"><strong>{fmt(single)}</strong><span>Single · comfortable lifestyle</span></div>
          <div class="cs-stat"><strong>{fmt(tiers_single['basic'])}–{fmt(tiers_single['high_comfort'])}</strong><span>Single · basic to affluent</span></div>
          <div class="cs-stat"><strong>{fmt(couple)}</strong><span>Couple · comfortable</span></div>
          <div class="cs-stat"><strong>{fmt(family)}</strong><span>Family of 4 · comfortable</span></div>
        </div>
{calc_form()}
      </div>
    </section>

{lifestyle_estimate_section(city, state_slug, city["name"])}

    <section class="cs-band">
      <div class="container container--wide">
        <header class="cs-band__head"><h2>Cost of living breakdown</h2><p>Monthly essentials before savings at median local prices.</p></header>
        <div class="cs-stat-row">
          <div class="cs-stat"><strong>{fmt(city['rent_1br'])}</strong><span>Rent</span></div>
          <div class="cs-stat"><strong>{fmt(city['groceries'])}</strong><span>Groceries</span></div>
          <div class="cs-stat"><strong>{fmt(city['utilities'])}</strong><span>Utilities</span></div>
          <div class="cs-stat"><strong>{fmt(city['transport'])}</strong><span>Transport</span></div>
          <div class="cs-stat"><strong>{fmt(core)}</strong><span>Core total</span></div>
        </div>
      </div>
    </section>

    <section class="cs-band cs-band--alt">
      <div class="container container--wide">
        <header class="cs-band__head"><h2>Rent vs buy impact</h2><p>Owning often raises housing cost even after equity build.</p></header>
        <p>Comfortable salary when renting: <strong>{fmt(single)}</strong>. When owning a similar home: <strong>{fmt(own)}</strong> (+{fmt(own - single)} gross).</p>
        <p>Compare long-term math in our <a href="/rent-vs-buy-calculator">rent vs buy calculator</a> and <a href="/living/housing/how-much-house-can-i-afford">house affordability guide</a>.</p>
      </div>
    </section>

    <section class="cs-band">
      <div class="container container--wide">
        <header class="cs-band__head"><h2>Local comparisons</h2></header>
        <div class="cs-compare-grid">
          <a class="cs-card" href="{salary_link(state_slug)}"><h3>{st_name} state average</h3><p>See all cities in {st_name}.</p></a>
          <a class="cs-card" href="{col_path}"><h3>Cost of living in {city['name']}</h3><p>Rent, food, and tax detail.</p></a>
          <a class="cs-card" href="{move_path}"><h3>Moving to {city['name']}</h3><p>One-time and monthly move costs.</p></a>
        </div>
      </div>
    </section>

    <section class="cs-band cs-band--alt">
      <div class="container container--wide">
        <header class="cs-band__head"><h2>Family size comparison</h2></header>
        <table class="cs-family-table">
          <thead><tr><th>Household</th><th>Basic</th><th>Comfortable</th><th>Comfortable Plus</th></tr></thead>
          <tbody>
{family_table(city, state_slug)}
          </tbody>
        </table>
      </div>
    </section>

{know_block}
{method_block}

{related_tools_section()}

    <section class="cs-band" id="cs-faq">
      <div class="container container--wide content-page">
        <header class="cs-band__head"><h2>FAQ</h2></header>
        <div class="faq-list">
{faq_html(faqs)}
        </div>
      </div>
    </section>

{cta_section(salary_link(state_slug))}

  </main>
{FOOTER}
  <script src="/comfortable-salary.js"></script>
</body>
</html>"""


def write(path: Path, html: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(html, encoding="utf-8")
    print(f"  wrote {path.relative_to(ROOT)}")


def main() -> None:
    print("Generating comfortable salary pages...")
    write(HUB_OUT / "index.html", render_hub())

    state_slugs = set(FEATURED_STATES)
    state_slugs.update(STATES.keys())
    state_slugs.update(STANDALONE_STATE.values())

    for state_slug in sorted(state_slugs):
        write(STATE_OUT / state_slug / "index.html", render_state(state_slug))

    for state_slug, st in STATES.items():
        for city_slug in st["cities"]:
            write(STATE_OUT / state_slug / city_slug / "index.html", render_city(state_slug, city_slug))

    for city_slug, state_slug in STANDALONE_STATE.items():
        write(STATE_OUT / state_slug / city_slug / "index.html", render_city(state_slug, city_slug))

    warnings = validate_catalog()
    if warnings:
        print("Validation warnings:")
        for w in warnings:
            print(f"  - {w}")
    else:
        print("All salary pages pass validation checks.")

    # Copy JS to scripts folder
    js_src = ROOT / "comfortable-salary.js"
    js_dst = ROOT / "scripts" / "comfortable-salary.js"
    js_dst.write_text(js_src.read_text(encoding="utf-8"), encoding="utf-8")
    print("Done.")


if __name__ == "__main__":
    main()
