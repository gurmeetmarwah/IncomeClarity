"""City-specific unique HTML sections for salary scenario pages (anti-doorway content)."""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

from comfortable_salary_data import STANDALONE_STATE, lifestyle_range  # noqa: E402
from generate_col_by_city_pages import STANDALONE, STATES  # noqa: E402

MARKER_BEGIN = "<!-- SS_UNIQUE_BEGIN -->"
MARKER_END = "<!-- SS_UNIQUE_END -->"

FEDERAL_STD_DED = 14600
FEDERAL_BRACKETS = [
    (0, 0.10),
    (11600, 0.12),
    (47150, 0.22),
    (100525, 0.24),
    (191950, 0.32),
    (243725, 0.35),
    (609350, 0.37),
]
SS_WAGE_BASE = 168600
SS_RATE = 0.062
MEDICARE_RATE = 0.0145

# 1BR rent percentiles (P25 / median / P75) — planning figures, not generic multipliers
RENT_PERCENTILES: dict[str, tuple[int, int, int]] = {
    "austin": (1450, 1750, 2100),
    "dallas": (1300, 1550, 1850),
    "houston": (1150, 1400, 1700),
    "los-angeles": (2200, 2600, 3100),
    "san-diego": (2100, 2550, 3000),
    "san-francisco": (2600, 3200, 3900),
    "miami": (1900, 2200, 2700),
    "tampa": (1450, 1650, 1950),
    "orlando": (1400, 1600, 1900),
    "new-york-city": (2900, 3400, 4100),
    "chicago": (1550, 1850, 2200),
}

STATE_TAX_NOTES: dict[str, str] = {
    "texas": "Texas has no state income tax — federal and FICA still apply.",
    "florida": "Florida has no state income tax — take-home is higher than NY or IL at the same gross.",
    "california": "California state income tax is progressive — effective rates rise quickly above $100k.",
    "new-york": "New York State income tax applies statewide; NYC residents also pay city income tax.",
    "illinois": "Illinois uses a flat 4.95% state income tax on taxable income.",
}

TAX_COMPARE: dict[str, tuple[str, str, str]] = {
    "texas": ("California", "california", "At the same gross, California take-home runs roughly $2,500–$4,500/year lower than Texas because of state income tax."),
    "florida": ("New York", "new-york", "Florida's no state income tax advantage vs NYC is often $4,000–$8,000/year at middle incomes."),
    "california": ("Texas", "texas", "Texas take-home on the same gross is typically $3,000–$6,000/year higher — rent may still be lower in Dallas or Houston."),
    "new-york": ("Florida", "florida", "A $80k gross in Miami often nets $350–$550/month more than NYC after state and city tax."),
    "illinois": ("Texas", "texas", "Illinois flat tax costs roughly $2,800–$4,200/year vs zero state tax in Texas at $75k–$100k."),
}

WORKED_PROFILES: dict[str, dict] = {
    "austin": {"name": "Alex", "job": "hybrid tech role", "neighborhood": "East Austin"},
    "dallas": {"name": "Priya", "job": "corporate finance job", "neighborhood": "Uptown"},
    "houston": {"name": "Marcus", "job": "energy sector analyst", "neighborhood": "Montrose"},
    "los-angeles": {"name": "Daniel", "job": "entertainment-adjacent role", "neighborhood": "Koreatown"},
    "san-diego": {"name": "Elena", "job": "biotech coordinator", "neighborhood": "North Park"},
    "san-francisco": {"name": "Sam", "job": "software engineer", "neighborhood": "Mission District"},
    "miami": {"name": "Isabella", "job": "hospitality manager", "neighborhood": "Little Havana"},
    "tampa": {"name": "Chris", "job": "healthcare admin", "neighborhood": "Hyde Park"},
    "orlando": {"name": "Jordan", "job": "theme-park corporate role", "neighborhood": "Winter Park"},
    "new-york-city": {"name": "Mei", "job": "marketing lead", "neighborhood": "Astoria, Queens"},
    "chicago": {"name": "Dev", "job": "consulting analyst", "neighborhood": "Logan Square"},
}


def fmt(n: int | float) -> str:
    return f"${int(round(n)):,}"


def fmt_k(n: int) -> str:
    if n >= 1000:
        return f"${n // 1000}k"
    return fmt(n)


def lookup_city(state: str, city_slug: str) -> tuple[dict, str, str]:
    """Return (city dict, state slug for tax, city display name)."""
    if city_slug in STANDALONE:
        city = STANDALONE[city_slug]
        return city, STANDALONE_STATE[city_slug], city["name"]
    st = STATES[state]
    city = st["cities"][city_slug]
    return city, state, city["name"]


def resolve_paths(state: str, city_slug: str, city: dict) -> dict[str, str]:
    tax_state = STANDALONE_STATE[city_slug] if city_slug in STANDALONE else state
    if city_slug in STANDALONE:
        col = f"/living/housing/cost-of-living-by-city/{city_slug}"
        move = f"/living/housing/moving-cost-calculator/{city_slug}"
    else:
        col = f"/living/housing/cost-of-living-by-city/{state}/{city_slug}"
        move = f"/living/housing/moving-cost-calculator/{state}/{city_slug}"
    hub = f"/living/lifestyle/comfortable-salary/{tax_state}/{city_slug}"
    link = city.get("house_link")
    if link and link != "/living/housing/how-much-house-can-i-afford":
        house = link
    elif city_slug in STANDALONE:
        house = "/living/housing/how-much-house-can-i-afford"
    else:
        house = f"/living/housing/how-much-house-can-i-afford/{state}/{city_slug}"
    return {"col": col, "move": move, "hub": hub, "house": house, "tax_state": tax_state}


def progressive_tax(taxable: float, brackets: list[tuple[int, float]]) -> float:
    tax = 0.0
    for i, (floor, rate) in enumerate(brackets):
        ceiling = brackets[i + 1][0] if i + 1 < len(brackets) else taxable + 1
        amount = min(taxable, ceiling) - floor
        if amount > 0:
            tax += amount * rate
    return tax


def california_tax(taxable: float) -> float:
    ca_brackets = [
        (0, 0.01),
        (10412, 0.02),
        (24684, 0.04),
        (38959, 0.06),
        (54081, 0.08),
        (68350, 0.093),
        (349137, 0.103),
        (418961, 0.113),
        (698271, 0.123),
    ]
    return progressive_tax(taxable, ca_brackets)


def new_york_state_tax(taxable: float) -> float:
    ny_brackets = [
        (0, 0.04),
        (8500, 0.045),
        (11700, 0.0525),
        (13900, 0.055),
        (80650, 0.06),
        (215400, 0.0685),
        (1077550, 0.0965),
    ]
    return progressive_tax(taxable, ny_brackets)


def nyc_city_tax(taxable: float) -> float:
    """NYC resident tax — simplified 2024 brackets on taxable income."""
    nyc_brackets = [
        (0, 0.03078),
        (12000, 0.03762),
        (25000, 0.03819),
        (50000, 0.03876),
    ]
    return progressive_tax(taxable, nyc_brackets)


def state_tax_amount(gross: int, taxable: float, state: str, city_slug: str) -> tuple[float, str]:
    if state in ("texas", "florida"):
        return 0.0, "$0"
    if state == "illinois":
        amt = taxable * 0.0495
        return amt, fmt(amt)
    if state == "california":
        amt = california_tax(taxable)
        return amt, fmt(amt)
    if state == "new-york":
        state_amt = new_york_state_tax(taxable)
        city_amt = nyc_city_tax(taxable) if city_slug == "new-york-city" else 0.0
        total = state_amt + city_amt
        if city_amt:
            return total, f"{fmt(state_amt)} state + {fmt(city_amt)} NYC"
        return total, fmt(total)
    return 0.0, "$0"


def estimate_taxes(gross: int, state: str, city_slug: str) -> dict:
    taxable = max(0, gross - FEDERAL_STD_DED)
    federal = progressive_tax(taxable, FEDERAL_BRACKETS)
    ss = min(gross, SS_WAGE_BASE) * SS_RATE
    medicare = gross * MEDICARE_RATE
    fica = ss + medicare
    state_amt, state_label = state_tax_amount(gross, taxable, state, city_slug)
    total = federal + fica + state_amt
    net = gross - total
    return {
        "federal": federal,
        "fica": fica,
        "ss": ss,
        "medicare": medicare,
        "state": state_amt,
        "state_label": state_label,
        "total": total,
        "net": net,
        "monthly_low": int(net / 12 * 0.99),
        "monthly_high": int(net / 12 * 1.01),
        "monthly_mid": int(net / 12),
    }


def rent_percentiles(city_slug: str, median: int) -> tuple[int, int, int]:
    if city_slug in RENT_PERCENTILES:
        return RENT_PERCENTILES[city_slug]
    return (int(median * 0.84), median, int(median * 1.18))


def salary_vs_tiers(salary: int, tiers: dict[str, int]) -> str:
    basic, comfort, plus = tiers["basic"], tiers["comfortable"], tiers["comfortable_plus"]
    if salary >= plus:
        return f"Above comfortable plus ({fmt(plus)}) — affluent tier within reach"
    if salary >= comfort:
        return f"At or above comfortable ({fmt(comfort)}) with savings headroom"
    if salary >= basic:
        return f"Between basic ({fmt(basic)}) and comfortable ({fmt(comfort)}) — essentials covered, savings tight"
    return f"Below basic tier ({fmt(basic)}) for this household"


def worked_example_block(
    *,
    city_name: str,
    city_slug: str,
    salary: int,
    salary_label: str,
    rent: int,
    city: dict,
    tax: dict,
    state_note: str,
    col: str,
) -> str:
    profile = WORKED_PROFILES.get(city_slug, {"name": "Taylor", "job": "local professional", "neighborhood": city_name})
    groceries = city["groceries"]
    utilities = city["utilities"]
    transport = city["transport"]
    core = rent + groceries + utilities + transport
    savings = 400 if salary < 100_000 else 650
    debt_note = "$400/month student loans" if salary < 100_000 else "$250/month car note"
    leftover = tax["monthly_mid"] - core - savings
    rent_pct = round(rent / max(tax["monthly_mid"], 1) * 100)

    return f"""        <p><strong>{profile["name"]}</strong> — single, works as a {profile["job"]} in {profile["neighborhood"]}. On {salary_label} gross in {city_name}:</p>
        <ul class="ss-worked-list">
          <li><strong>Estimated take-home:</strong> {fmt(tax["monthly_mid"])}/month ({state_note.rstrip(".")}).</li>
          <li><strong>Rent ({fmt(rent)}) + groceries ({fmt(groceries)}) + utilities ({fmt(utilities)}) + transport ({fmt(transport)}):</strong> {fmt(core)}/month in core costs.</li>
          <li><strong>Savings target ({fmt(savings)}/mo) and {debt_note}:</strong> leaves about <strong>{fmt(leftover)}/month</strong> for dining, healthcare, and extras.</li>
        </ul>
        <p>At {rent_pct}% of take-home, rent is {"within" if rent_pct <= 35 else "above"} common budgeting ranges in {city_name}. {profile["name"]} {"can save modestly without constant tradeoffs" if leftover > 800 and rent_pct <= 35 else "covers bills but has little margin for rent spikes or emergencies"} — see our <a href="{col}">{city_name} cost of living guide</a> for neighborhood-level detail.</p>"""


def build_unique_sections(
    *,
    state: str,
    city_slug: str,
    salary: int,
    hub: str | None = None,
) -> str:
    city, tax_state, city_name = lookup_city(state, city_slug)
    paths = resolve_paths(state, city_slug, city)
    salary_label = fmt(salary)
    tax = estimate_taxes(salary, paths["tax_state"], city_slug)
    p25, p50, p75 = rent_percentiles(city_slug, city["rent_1br"])
    rent_cap_30 = int(tax["monthly_mid"] * 0.30)
    tiers_single = lifestyle_range(city, "single", "rent", paths["tax_state"])
    tiers_couple = lifestyle_range(city, "couple", "rent", paths["tax_state"])
    tiers_family = lifestyle_range(city, "family4", "rent", paths["tax_state"])

    col = paths["col"]
    house = paths["house"]
    move = paths["move"]
    hub_path = hub or paths["hub"]

    state_note = STATE_TAX_NOTES.get(paths["tax_state"], STATE_TAX_NOTES.get(state, ""))
    compare_name, compare_state, compare_blurb = TAX_COMPARE.get(
        paths["tax_state"], TAX_COMPARE.get(state, ("another state", "texas", ""))
    )
    compare_tax = estimate_taxes(salary, compare_state, "austin")
    tax_delta = int(tax["net"] - compare_tax["net"])

    worked = worked_example_block(
        city_name=city_name,
        city_slug=city_slug,
        salary=salary,
        salary_label=salary_label,
        rent=city["rent_1br"],
        city=city,
        tax=tax,
        state_note=state_note,
        col=col,
    )

    def tier_row(household: str, tiers: dict[str, int], highlight: bool = False) -> str:
        placement = salary_vs_tiers(salary, tiers)
        row_class = ' class="ss-tier-row--here"' if highlight else ""
        here = " <strong>(your salary)</strong>" if highlight else ""
        return (
            f"              <tr{row_class}><th scope=\"row\">{household}</th>"
            f"<td>{fmt(tiers['basic'])}</td><td>{fmt(tiers['comfortable'])}</td>"
            f"<td>{fmt(tiers['comfortable_plus'])}</td>"
            f"<td>{placement}{here}</td></tr>"
        )

    return f"""    <section class="ss-band ss-band--alt" id="tax-breakdown">
      <div class="container container--wide">
        <header class="ss-band__head">
          <h2>What {salary_label} Becomes in {city_name} After Taxes</h2>
          <p>{state_note} Figures assume single filer, standard deduction, W-2 wages — not self-employment or itemized deductions.</p>
        </header>
        <div class="scenario-table-wrap">
          <table class="scenario-table ss-tax-table">
            <caption>Estimated annual tax breakdown on {salary_label} in {city_name}</caption>
            <thead>
              <tr><th scope="col">Tax line</th><th scope="col">Annual</th><th scope="col">Monthly</th></tr>
            </thead>
            <tbody>
              <tr><th scope="row">Federal income tax</th><td>{fmt(tax["federal"])}</td><td>{fmt(tax["federal"] / 12)}</td></tr>
              <tr><th scope="row">FICA (Social Security + Medicare)</th><td>{fmt(tax["fica"])}</td><td>{fmt(tax["fica"] / 12)}</td></tr>
              <tr><th scope="row">State / local income tax</th><td>{tax["state_label"]}</td><td>{fmt(tax["state"] / 12) if tax["state"] else "$0"}</td></tr>
              <tr><th scope="row">Total tax</th><td><strong>{fmt(tax["total"])}</strong></td><td><strong>{fmt(tax["total"] / 12)}</strong></td></tr>
              <tr><th scope="row">Estimated take-home</th><td><strong>{fmt(tax["net"])}</strong></td><td><strong>{fmt(tax["monthly_low"])}–{fmt(tax["monthly_high"])}/mo</strong></td></tr>
            </tbody>
          </table>
        </div>
        <aside class="ss-callout" role="note">
          <p><strong>vs {compare_name}:</strong> {compare_blurb} On {salary_label}, our model shows roughly <strong>{fmt(abs(tax_delta))}/year {"more" if tax_delta > 0 else "less"}</strong> take-home in {city_name} than {compare_name}. Run your exact number in the <a href="/hourly-to-salary-after-tax#hourly-salary-form">after-tax salary calculator</a>.</p>
        </aside>
      </div>
    </section>

    <section class="ss-band" id="rent-percentiles">
      <div class="container container--wide">
        <header class="ss-band__head">
          <h2>{city_name} Rent Percentiles vs Your {salary_label} Budget</h2>
          <p>Median 1BR rent in {city_name} is {fmt(p50)}/month (COL index {city["col_index"]}). Here is where the market sits — and what a 30% take-home rent cap allows.</p>
        </header>
        <div class="scenario-table-wrap">
          <table class="scenario-table ss-rent-table">
            <caption>1-bedroom rent distribution in {city_name}</caption>
            <thead>
              <tr><th scope="col">Percentile</th><th scope="col">Monthly rent</th><th scope="col">Who it fits</th></tr>
            </thead>
            <tbody>
              <tr><th scope="row">25th (budget)</th><td>{fmt(p25)}</td><td>Older stock, roommates, or outer neighborhoods</td></tr>
              <tr><th scope="row">50th (median)</th><td><strong>{fmt(p50)}</strong></td><td>Typical 1BR — our planning default</td></tr>
              <tr><th scope="row">75th (premium)</th><td>{fmt(p75)}</td><td>New builds, downtown, or walkable cores</td></tr>
              <tr><th scope="row">30% rent cap on {salary_label}</th><td><strong>{fmt(rent_cap_30)}</strong></td><td>Max housing on estimated take-home — before other bills</td></tr>
            </tbody>
          </table>
        </div>
        <p class="ss-band__foot">Full category breakdown — groceries, utilities, transport — lives in our <a href="{col}">{city_name} cost of living guide</a> and <a href="/living/housing/how-much-rent-can-i-afford">rent affordability calculator</a>.</p>
      </div>
    </section>

    <section class="ss-band ss-band--alt" id="lifestyle-tiers">
      <div class="container container--wide">
        <header class="ss-band__head">
          <h2>Basic, Comfortable, and Comfortable Plus in {city_name}</h2>
          <p>Our lifestyle tiers include median local costs <em>plus</em> savings — not just covering rent. See where {salary_label} lands for each household type.</p>
        </header>
        <div class="scenario-table-wrap">
          <table class="scenario-table ss-tier-table">
            <caption>Gross salary targets by household and tier in {city_name}</caption>
            <thead>
              <tr><th scope="col">Household</th><th scope="col">Basic</th><th scope="col">Comfortable</th><th scope="col">Comfortable plus</th><th scope="col">{salary_label} verdict</th></tr>
            </thead>
            <tbody>
{tier_row("Single renter", tiers_single, highlight=True)}
{tier_row("Couple", tiers_couple)}
{tier_row("Family of 4", tiers_family)}
            </tbody>
          </table>
        </div>
        <p class="ss-band__foot">Tier definitions and calculator defaults: <a href="{hub_path}#cs-calc">{city_name} comfortable salary guide</a>.</p>
      </div>
    </section>

    <section class="ss-band" id="worked-example">
      <div class="container container--wide content-page">
        <header class="ss-band__head">
          <h2>Real Numbers: One Month on {salary_label} in {city_name}</h2>
          <p>Not a template — this uses {city_name} median rent ({fmt(city["rent_1br"])}), local grocery/utility/transport lines, and {city_name}-specific tax math.</p>
        </header>
{worked}
      </div>
    </section>

    <section class="ss-band ss-band--alt" id="local-resources">
      <div class="container container--wide">
        <div class="ss-links-band">
          <h3>{city_name} cost &amp; salary resources</h3>
          <p>Go deeper on local numbers before you sign a lease or accept an offer.</p>
          <div class="ss-context-links">
            <a href="{col}">{city_name} cost of living →</a>
            <a href="{house}">How much house can I afford in {city_name} →</a>
            <a href="{hub_path}">{city_name} salary calculator →</a>
            <a href="{move}">Moving to {city_name} →</a>
          </div>
        </div>
      </div>
    </section>"""


def inject_unique_sections(html: str, *, state: str, city_slug: str, salary: int, hub: str | None = None) -> str:
    block = build_unique_sections(state=state, city_slug=city_slug, salary=salary, hub=hub)
    wrapped = f"    {MARKER_BEGIN}\n{block}\n    {MARKER_END}"

    pattern = re.compile(re.escape(MARKER_BEGIN) + r".*?" + re.escape(MARKER_END), re.DOTALL)
    if pattern.search(html):
        return pattern.sub(wrapped, html, count=1)

    anchor = re.compile(r"(    </section>\n)\n(    <section class=\"ss-band\")")
    match = anchor.search(html)
    if not match:
        raise ValueError(f"Could not find injection point for {state}/{city_slug}")
    return anchor.sub(rf"\1\n{wrapped}\n\n\2", html, count=1)


def patch_take_home_snippets(html: str, tax: dict, salary: int | None = None) -> str:
    low, high = tax["monthly_low"], tax["monthly_high"]
    mid = tax["monthly_mid"]
    html = re.sub(
        r"Estimated After-Tax Income: <strong>\$[\d,]+–\$[\d,]+/month</strong>",
        f"Estimated After-Tax Income: <strong>{fmt(low)}–{fmt(high)}/month</strong>",
        html,
        count=1,
    )
    html = re.sub(
        r'<strong id="ss-out-takehome">\$[\d,]+ – \$[\d,]+</strong>',
        f'<strong id="ss-out-takehome">{fmt(low)} – {fmt(high)}</strong>',
        html,
        count=1,
    )
    html = re.sub(
        r"<strong>~\$[\d,]+/month</strong>",
        f"<strong>~{fmt(mid)}/month</strong>",
        html,
        count=1,
    )
    html = re.sub(
        r"estimated take-home is about \$[\d,]+–\$[\d,]+ per month",
        f"estimated take-home is about {fmt(low)}–{fmt(high)} per month",
        html,
    )
    if salary is not None:
        html = re.sub(
            r'id="ss-salary" name="salary" value="\d+"',
            f'id="ss-salary" name="salary" value="{salary}"',
            html,
            count=1,
        )
    return html
