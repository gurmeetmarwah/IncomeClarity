#!/usr/bin/env python3
"""Generate state and city house affordability pages."""
import json
import math
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from house_afford_city_content import EXTENDED
from house_afford_state_content import STATE_EXTENDED

ROOT = Path(__file__).resolve().parent.parent
BASE = ROOT / "living" / "housing" / "how-much-house-can-i-afford"

STATES = {
    "california": {
        "name": "California",
        "median_price": 785000,
        "median_income": 96000,
        "tax_pct": 0.75,
        "ins_pct": 0.45,
        "hoa": 200,
        "insight": "California buyers face high list prices, state income tax on take-home pay, and insurance that can rival the mortgage in fire-prone areas.",
        "compare": "Texas",
        "compare_slug": "texas",
        "compare_note": "No state income tax but lower coastal prices are rare.",
        "rent_link": "/living/housing/rent-vs-buy-california.html",
        "col_link": "/living/housing/cost-of-living-by-city/california",
        "salary_link": "/living/lifestyle/comfortable-salary/california",
        "tax_link": "/hourly-to-salary-after-tax/state/california/",
        "salary_blurb": "At the state median home price, many buyers need gross pay near $245k to hit the 28% line with 20% down at 6.5%. Inland metros fit closer to $120k–$160k.",
        "narrative": [
            "California is not one market. The coast costs far more than the state median. Inland cities often fit middle incomes better. Start with your city page, not the state median alone.",
            "State income tax lowers take-home pay. A $120k salary in CA does not feel like $120k in Texas. Use our take-home tool, then run this calculator on gross pay with the 28% rule.",
            "Insurance can add $200 to $500 a month in fire-prone zip codes. We bake a default into the breakdown. Get a real quote before you set your max price.",
            "Prop 13 caps how fast tax can rise after you buy. Your first bill still tracks purchase price. Budget for Mello-Roos in some new tracts.",
            "Many CA buyers put 10% down and pay PMI. That works, but the same income buys less house. If you can wait for 20% down, the monthly payment drops a lot.",
        ],
        "faqs": [
            ("How much house can I afford in California on $150k?", "At $150k gross, the 28% cap is about $3,500 a month. That often fits an inland home near $550k — not a coastal $850k+ listing at today's rates."),
            ("Does Prop 13 change my payment?", "Prop 13 limits how fast your assessed tax can rise. Your first-year bill still depends on purchase price and local rates."),
            ("Should I use the US calculator or this page?", "Use the US page for the rules. Use this page for California tax, insurance, and city medians."),
        ],
        "cities": {
            "los-angeles": {
                "name": "Los Angeles", "median_price": 875000, "median_income": 82000, "tax_pct": 0.72, "ins_pct": 0.5, "hoa": 275,
                "pressure": "Very high — median list prices sit above the 28% line for typical salaries.",
                "local_note": "LA buyers often compete with all-cash offers. Insurance in fire zones can add $300+ a month on top of tax.",
                "narrative": [
                    "Los Angeles spans the Valley, the Westside, and South Bay. Median price near $875k is a blend — many areas sit higher. Do not assume the median fits your target zip.",
                    "Dual income is common. Even then, list prices and HOA can push the stress meter to Stretched at the 28% cap. A smaller home or a longer commute often beats maxing the lender limit.",
                    "Wildfire insurance changed the math. Ask for an insurance quote with the address, not a state average. Tax in LA County is near 0.72% of value on many homes.",
                    "First-time buyers sometimes target condos with lower list prices. Read the HOA docs — special assessments can hit like a second mortgage.",
                ],
                "faqs": [
                    ("What income do I need to buy in Los Angeles?", "For a median home near $875k, plan on $200k+ gross with 20% down at today’s rates — or a smaller home in the Valley."),
                    ("Is LA cheaper than San Francisco?", "List prices are lower than SF, but insurance and HOA can still push the full payment high."),
                ],
            },
            "san-francisco": {
                "name": "San Francisco", "median_price": 1250000, "median_income": 140000, "tax_pct": 0.7, "ins_pct": 0.42, "hoa": 450,
                "pressure": "Extreme — even strong earners often rent or buy with a large down payment.",
                "local_note": "Condos and co-ops add HOA and reserve fees. Many buyers need dual incomes well above $200k for a median unit.",
                "narrative": [
                    "San Francisco has the highest median price in this guide. A $1.25M median condo is not what most $140k earners buy without a large down payment or help from family.",
                    "Co-ops and condos add HOA near $450 a month in our default. Maintenance and reserves can rise after an inspection. Cash buyers still compete in popular buildings.",
                    "Tech wages pulled prices up for years. Remote work eased some blocks, but supply is still tight. Renting while saving a 20% down payment is a common path.",
                    "If you earn $200k gross, run the calculator with your real car and student loans. You may afford a smaller unit — not the citywide median listing.",
                ],
                "faqs": [
                    ("Can I afford a home in San Francisco on $200k?", "You may qualify for a smaller condo, not a median $1.25M listing. Run the calculator with your real debts."),
                    ("Why is SF so expensive?", "Land is scarce, wages are high, and supply is tight. The payment stack still uses the same 28% rule."),
                ],
            },
            "san-diego": {
                "name": "San Diego", "median_price": 920000, "median_income": 95000, "tax_pct": 0.73, "ins_pct": 0.48, "hoa": 320,
                "pressure": "High — military and tech wages help, but insurance and HOA add up fast.",
                "local_note": "Military BAH and tech jobs support demand. Coastal zip codes run above the county median.",
                "narrative": [
                    "San Diego mixes military, biotech, and tourism wages. Median income near $95k does not always match coastal list prices above $900k.",
                    "BAH can help service members qualify. Civilians should still use gross W-2 pay in the calculator. Do not mix BAH and base pay twice.",
                    "Insurance runs higher near the coast. East County and South Bay often have lower list prices with longer commutes.",
                    "Mello-Roos districts add tax on new builds. Ask the seller for the full annual tax bill before you write an offer.",
                ],
                "faqs": [
                    ("How much house can I afford in San Diego on $120k?", "About $2,800 a month at 28% gross. That often maps to a home near $550k–$650k with 20% down — below the median."),
                    ("Does San Diego have Mello-Roos?", "Some new builds add special tax districts. Ask for the full tax bill before you offer."),
                ],
            },
        },
    },
    "texas": {
        "name": "Texas",
        "median_price": 345000,
        "median_income": 72000,
        "tax_pct": 1.6,
        "ins_pct": 0.4,
        "hoa": 75,
        "insight": "Texas has no state income tax, which boosts take-home pay. Property tax is among the highest in the US, so the full PITI still matters.",
        "compare": "California",
        "compare_slug": "california",
        "compare_note": "Higher prices on the coast but income tax shrinks net pay.",
        "rent_link": "/rent-vs-buy-calculator#rent-vs-buy",
        "col_link": "/living/housing/cost-of-living-by-city/texas",
        "salary_link": "/living/lifestyle/comfortable-salary/texas",
        "tax_link": "/hourly-to-salary-after-tax/state/texas/",
        "faqs": [
            ("How much house can I afford in Texas on $90k?", "About $2,100 a month at 28% gross. That often supports a home near $280k–$320k with 20% down at 6.5% — more in cheaper metros."),
            ("Why is Texas property tax so high?", "Texas funds schools and local services largely through property tax instead of state income tax."),
            ("Is buying better than renting in Texas?", "Often after 5–7 years in stable markets. Run your stay and rate in the rent vs buy tool."),
        ],
        "salary_blurb": "Texas has no state income tax, so take-home pay helps. Property tax near 1.6% still pulls $400–$600 a month on a $350k home.",
        "narrative": [
            "Texas has no state income tax. That helps your take-home pay. Property tax is among the highest in the US, so your monthly housing stack is still heavy.",
            "Schools and local services are funded largely through property tax, not income tax. A $345k home can mean $460 a month in tax alone at 1.6%.",
            "Houston, Dallas, and Austin sit at different price points. Austin rose fast with tech jobs. Houston stayed more affordable on median price.",
            "Flood and wind insurance matter on the Gulf Coast. Inland metros see lower insurance but still need a hail and wind quote.",
            "Buying often beats renting after five to seven years if you stay put. Run your timeline in the rent vs buy tool before you size up.",
        ],
        "cities": {
            "houston": {
                "name": "Houston", "median_price": 310000, "median_income": 68000, "tax_pct": 1.65, "ins_pct": 0.45, "hoa": 60,
                "pressure": "Moderate — prices stay below many coastal metros.",
                "local_note": "Flood zones matter. Insurance and tax can rival the mortgage on older homes without updates.",
                "narrative": [
                    "Houston is one of the more affordable big Texas metros. Median price near $310k fits many middle incomes with 20% down at today's rates.",
                    "Flood maps matter. Harvey taught many buyers to check FEMA zones and insurance cost before they fall in love with a kitchen.",
                    "Energy and medical jobs anchor wages. Suburbs in Katy, Pearland, and The Woodlands trade commute time for more house per dollar.",
                    "Property tax near 1.65% is a real line item. On a $300k home that is over $400 a month — not pocket change.",
                ],
                "faqs": [
                    ("How much house can I afford in Houston on $80k?", "About $1,867 a month at 28%. That often fits a home near $250k–$290k with 20% down."),
                    ("Is Houston cheaper than Austin?", "Yes on median price. Austin wages are higher but list prices rose faster."),
                ],
            },
            "dallas": {
                "name": "Dallas", "median_price": 385000, "median_income": 75000, "tax_pct": 1.7, "ins_pct": 0.42, "hoa": 85,
                "pressure": "Moderate to high — growth pushed prices in some suburbs.",
                "local_note": "DFW spans many tax districts. Check the county rate on the listing, not just the state average.",
                "narrative": [
                    "Dallas–Fort Worth is a spread-out market. Median price near $385k is a midpoint — Plano and Frisco run higher, southern suburbs often lower.",
                    "Job growth pulled prices up in some rings. Wages near $75k median mean many buyers target homes below the median to stay Comfortable on the stress meter.",
                    "HOA is common in master-planned suburbs. Add $85 or more in the calculator if the listing has an HOA line.",
                    "Tax districts differ by county and city. Use the seller's tax certificate, not a statewide guess, when you plan your payment.",
                ],
                "faqs": [
                    ("What salary do I need for a median Dallas home?", "Roughly $95k–$110k gross with 20% down at 6.5%, before other debts."),
                    ("Do Dallas homes have HOA?", "Many suburbs do. Enter $85+ in the calculator if you are buying in a planned community."),
                ],
            },
            "austin": {
                "name": "Austin", "median_price": 485000, "median_income": 88000, "tax_pct": 1.55, "ins_pct": 0.4, "hoa": 120,
                "pressure": "Higher than Houston — tech wages help but list prices rose quickly.",
                "local_note": "Tech layoffs and remote work shifted demand. Median price is still above Houston and San Antonio.",
                "narrative": [
                    "Austin prices rose fast with tech and migration. Median near $485k is still below California coasts but above Houston.",
                    "Tech wages near $88k median help, but list prices in popular zip codes outran income for some buyers. Look at suburbs and satellite towns if you are Stretched.",
                    "Property tax near 1.55% plus HOA in many new builds. Run the calculator with both — not mortgage alone.",
                    "Remote workers sometimes keep coastal salaries while buying in Austin. If that is you, still model a pay cut scenario before you max out.",
                ],
                "faqs": [
                    ("How much house can I afford in Austin on $100k?", "About $2,333 a month at 28%. That often supports $320k–$380k with 20% down."),
                    ("Is Austin still a seller’s market?", "It varies by zip. Run your offer against the calculator max, not the list price alone."),
                ],
            },
        },
    },
    "florida": {
        "name": "Florida",
        "median_price": 395000,
        "median_income": 68000,
        "tax_pct": 0.9,
        "ins_pct": 0.55,
        "hoa": 150,
        "insight": "Storm insurance and HOA fees often drive the monthly bill in Florida. No state income tax helps your take-home.",
        "compare": "New York",
        "compare_slug": "new-york",
        "compare_note": "NY has income tax; Florida trades that for higher storm insurance in many zip codes.",
        "rent_link": "/rent-vs-buy-calculator#rent-vs-buy",
        "col_link": "/living/housing/cost-of-living-by-city/florida",
        "salary_link": "/living/family-budgeting/salary-needed-to-live-comfortably",
        "tax_link": "/hourly-to-salary-after-tax/state/florida/",
        "faqs": [
            ("How much house can I afford in Florida?", "Start with 28% of gross for your full housing payment plus HOA. Get an insurance quote early — coast and roof type change the bill a lot."),
            ("Why is Florida insurance so high?", "Storm risk and higher repair costs pushed premiums up in many zip codes. Quotes vary block by block."),
            ("Do I need flood insurance?", "In many zones, yes. It is a separate policy from your home policy and can add $100 to $300 a month."),
        ],
        "salary_blurb": "Florida has no state income tax. Still plan an extra $200 to $400 a month for insurance vs the US norm on many homes.",
        "narrative": [
            "Florida has no state income tax. You keep more of each paycheck. Storm insurance and HOA fees often take that back on the monthly bill.",
            "Coastal condos can cost more to insure than inland homes. Get a quote with the full address before you set a max price.",
            "The state median near $395k is only a midpoint. Miami runs high. Tampa and Orlando sit in the middle for many buyers.",
            "Flood coverage is extra in many zones. Plan $100 to $300 a month if your lender asks for it.",
            "More buyers moved here after 2020. Hot zip codes still see bids over list. Use the stress label — do not shop at your lender max alone.",
        ],
        "cities": {
            "miami": {
                "name": "Miami", "median_price": 580000, "median_income": 62000, "tax_pct": 0.95, "ins_pct": 0.65, "hoa": 280,
                "pressure": "Very high — insurance and condo HOA often exceed the mortgage.",
                "local_note": "Condos need reserves and wind coverage. Lenders may require higher down on older buildings.",
                "narrative": [
                    "Miami is one of the toughest affordability matches in Florida. Median income near $62k and median price near $580k leave a wide gap at the 28% rule.",
                    "Condos dominate many buyer searches. HOA near $280 a month in our default plus high wind insurance can exceed principal and interest.",
                    "Lenders tightened rules on older coastal buildings after insurance market stress. Expect more questions on reserves and roof age.",
                    "If you earn $75k to $90k, target a price well below median or plan a larger down payment. Run the stress label — Stretched is common at median list.",
                ],
                "faqs": [
                    ("Why is Miami insurance so high?", "Hurricane risk and reinsurance costs pushed premiums up statewide."),
                    ("Can I afford Miami on $75k?", "The median home is a stretch at $75k gross. Look at lower price points or rent while saving."),
                ],
            },
            "tampa": {
                "name": "Tampa", "median_price": 385000, "median_income": 65000, "tax_pct": 0.92, "ins_pct": 0.52, "hoa": 140,
                "pressure": "Moderate to high — insurance still matters more than inland states.",
                "local_note": "Tampa Bay growth raised prices after 2020. Flood maps affect insurance in coastal blocks.",
                "narrative": [
                    "Tampa Bay grew fast after 2020. Median price near $385k is more reachable than Miami for many dual-income households.",
                    "Insurance still runs above the US average. Get a quote early — do not size your max price on a national default alone.",
                    "Flood zones along the bay and rivers add cost. A home that looks affordable on list price may fail the full PITI test.",
                    "Suburbs in Hillsborough and Pasco often trade commute for space. Run the calculator with your real drive-to-work budget in mind.",
                ],
                "faqs": [
                    ("How much house can I afford in Tampa on $70k?", "About $1,633 a month at 28%. That often maps to $240k–$280k with 20% down."),
                    ("Do I need flood insurance in Tampa?", "Many zones yes — it is separate from homeowners and can be $100+ a month."),
                ],
            },
            "orlando": {
                "name": "Orlando", "median_price": 410000, "median_income": 64000, "tax_pct": 0.9, "ins_pct": 0.5, "hoa": 125,
                "pressure": "Moderate — tourism wages can lag list prices.",
                "local_note": "Theme-park and service jobs dominate wages. Dual income often makes the median home workable.",
                "narrative": [
                    "Orlando runs on tourism, healthcare, and growth from relocation. Wages near $64k median mean many families need two incomes for a median home near $410k.",
                    "Insurance is lower than Miami but not cheap. New subdivisions often carry HOA near $125 a month — include it in the calculator.",
                    "Compared to Tampa, Orlando can be a wash on price depending on zip. Compare both city pages if you are flexible on job location.",
                    "First-time buyers often target townhomes below the median. That keeps the stress meter in Moderate instead of Stretched.",
                ],
                "faqs": [
                    ("Is Orlando cheaper than Miami?", "Median price and insurance are lower. HOA is still common in new builds."),
                    ("What income for a median Orlando home?", "Plan on $85k–$100k gross with 20% down at 6.5%, plus room for insurance quotes."),
                ],
            },
        },
    },
    "new-york": {
        "name": "New York",
        "median_price": 425000,
        "median_income": 82000,
        "tax_pct": 1.4,
        "ins_pct": 0.4,
        "hoa": 250,
        "insight": "Upstate cities look like the US norm. New York City is a different market — higher price, co-op fees, and local tax.",
        "compare": "Florida",
        "compare_slug": "florida",
        "compare_note": "Lower NYC-area prices exist in FL, but insurance and wages differ.",
        "rent_link": "/living/cost-of-living/nyc-vs-austin-cost-of-living.html",
        "col_link": "/living/housing/cost-of-living-by-city/new-york",
        "salary_link": "/living/family-budgeting/salary-needed-to-live-comfortably",
        "tax_link": "/hourly-to-salary-after-tax/state/new-york/",
        "faqs": [
            ("How much house can I afford in New York state?", "It depends on metro. Buffalo-area homes fit middle incomes. NYC needs a much higher salary for the same 28% rule."),
            ("Does NYC tax change affordability?", "NYC adds city income tax on top of state tax. Check take-home pay, not just gross salary."),
            ("What income do I need to buy in NYC?", "Often $200k or more in gross pay for a median condo payment. Use the NYC city page for your target area."),
        ],
        "narrative": [
            "New York is two markets in one state. Buffalo and Albany fit middle incomes. New York City needs far more gross pay for the same 28% rule.",
            "State and city tax cut take-home pay downstate. $100k in NYC does not spend like $100k in a no-tax state after tax.",
            "Co-ops and condos add fees each month. Our tool includes HOA defaults. Raise them if you shop co-ops with high maintenance.",
            "Tax works different upstate vs the city. Buffalo has a higher rate on a lower price. NYC has a lower rate on a higher home value.",
            "Use a city page before you trust the state median. $425k statewide is not what most Manhattan or Brooklyn buyers face.",
        ],
        "cities": {
            "new-york-city": {
                "name": "New York City", "median_price": 725000, "median_income": 95000, "tax_pct": 0.88, "ins_pct": 0.45, "hoa": 450,
                "pressure": "Very high — co-op maintenance and local tax squeeze cash flow.",
                "local_note": "Co-ops may need 20–50% down and board approval. City income tax hits take-home before you shop.",
                "narrative": [
                    "New York City is the most complex market in this guide. Co-ops, condos, and townhomes each carry different fees and board rules.",
                    "City income tax stacks on state tax. Check take-home pay before you trust gross salary in the calculator.",
                    "Median price near $725k is not one borough. Queens and Bronx listings can sit far below Manhattan medians — still above national norms.",
                    "HOA and maintenance near $450 a month in our default is a floor, not a cap. Luxury buildings run much higher.",
                    "Many buyers need $180k+ gross for a median condo payment with 20% down. If you are below that, size down or widen your search to outer boroughs.",
                ],
                "faqs": [
                    ("What income to buy in NYC?", "Often $180k+ gross for a median condo payment with 20% down — borough and building matter."),
                    ("Are NYC property taxes low?", "Rates look low on paper but assessed values are high. Maintenance fees are the wild card."),
                ],
            },
            "buffalo": {
                "name": "Buffalo", "median_price": 215000, "median_income": 58000, "tax_pct": 2.2, "ins_pct": 0.35, "hoa": 50,
                "pressure": "Lower — prices align better with regional wages.",
                "local_note": "Buffalo offers some of the lowest list prices in NY. Tax rates are higher than NYC as a percent of value.",
                "narrative": [
                    "Buffalo is among the most affordable cities in New York. Median price near $215k pairs better with median income near $58k than downstate metros.",
                    "Tax near 2.2% of value is high as a rate but low in dollars on a $200k home. Budget winter heat and roof work on older stock.",
                    "First-time buyers can often land in the Comfortable stress band with dual income and modest debt. Run your real car and student loan payments in the form.",
                    "Compared to NYC, Buffalo trades higher tax rate for a much lower list price. Your monthly payment can still be half of a downstate condo.",
                ],
                "faqs": [
                    ("How much house can I afford in Buffalo on $60k?", "About $1,400 a month at 28%. That can fit a home near $180k–$220k with 20% down."),
                    ("Is Buffalo a good market for first-time buyers?", "Lower prices help. Still budget for heat, snow removal, and older-home repairs."),
                ],
            },
            "albany": {
                "name": "Albany", "median_price": 285000, "median_income": 72000, "tax_pct": 1.8, "ins_pct": 0.38, "hoa": 80,
                "pressure": "Moderate — state capital jobs support mid-range homes.",
                "local_note": "Government and healthcare jobs stabilize demand. Suburbs in Saratoga and Colonie run above the city median.",
                "narrative": [
                    "Albany anchors state government and healthcare jobs. Median income near $72k supports mid-range homes near $285k for many buyers with 20% down.",
                    "Suburbs like Saratoga Springs run above the city median. If you work downtown but shop suburban, use this page as a floor and check local listings.",
                    "Tax near 1.8% plus insurance near 0.38% of value is typical in our model. Older homes may need cash for heat and cap ex each year.",
                    "Compared to Buffalo, Albany costs more but wages run higher. Compared to NYC, Albany is a different world on monthly payment.",
                ],
                "faqs": [
                    ("What salary for a median Albany home?", "About $75k–$90k gross with 20% down at 6.5%, before car loans or cards."),
                    ("How do Albany taxes compare to Buffalo?", "Effective rates are in the same ballpark; Buffalo’s median price is lower."),
                ],
            },
        },
    },
}

URL_SCRIPT = """  <script>
    (function () {
      const path = window.location.pathname;
      let cleanPath = path;
      if (path.endsWith("/index.html")) cleanPath = path.slice(0, -10);
      else if (path.endsWith(".html")) cleanPath = path.slice(0, -5);
      if (cleanPath !== path) window.history.replaceState({}, "", cleanPath + window.location.search + window.location.hash);
    })();
  </script>"""


def fmt(n):
    return f"${n:,}"


def paragraphs_html(paragraphs: list[str], indent: str = "        ") -> str:
    return "\n".join(f"{indent}<p>{p}</p>" for p in paragraphs)


def solve_price(payment_cap, down, annual_rate=6.5, tax_pct=1.1, ins_pct=0.35, hoa=0):
    rate = (annual_rate / 100) / 12
    n = 360
    factor = rate * math.pow(1 + rate, n) / (math.pow(1 + rate, n) - 1)
    tax_ins_monthly_rate = (tax_pct / 100 + ins_pct / 100) / 12
    fixed_hoa = hoa or 0
    mortgage_budget = payment_cap - fixed_hoa
    if mortgage_budget <= 0:
        return {"price": 0, "mortgage": 0, "tax": 0, "ins": 0, "hoa": fixed_hoa, "piti": payment_cap}
    denom = factor + tax_ins_monthly_rate
    loan = max(0, (mortgage_budget - down * tax_ins_monthly_rate) / denom)
    price = loan + down
    mortgage = loan * factor
    tax = (price * tax_pct / 100) / 12
    ins = (price * ins_pct / 100) / 12
    piti = mortgage + tax + ins + fixed_hoa
    return {"price": price, "mortgage": mortgage, "tax": tax, "ins": ins, "hoa": fixed_hoa, "piti": piti}


def stress_label(piti, gross, debts=300):
    monthly_gross = gross / 12
    housing_cap = monthly_gross * 0.28
    total_cap = monthly_gross * 0.36 - debts
    payment_cap = min(housing_cap, total_cap)
    pct = (piti / monthly_gross) * 100 if monthly_gross else 0
    if payment_cap < housing_cap - 1:
        return "Over limit", "ha-stress--over"
    if pct > 32:
        return "Stretched", "ha-stress--high"
    if pct > 26:
        return "Moderate", "ha-stress--moderate"
    return "Comfortable", "ha-stress--comfortable"


def income_tier_rows(city, salaries=(75000, 100000, 125000, 150000, 200000), debts=300, rate=6.5):
    down_pct = 0.2
    rows = []
    for gross in salaries:
        monthly_gross = gross / 12
        housing_cap = monthly_gross * 0.28
        total_cap = monthly_gross * 0.36 - debts
        payment_cap = min(housing_cap, total_cap)
        down = 0
        out = solve_price(payment_cap, down, rate, city["tax_pct"], city["ins_pct"], city["hoa"])
        label, cls = stress_label(out["piti"], gross, debts)
        rows.append((gross, int(out["price"]), label, cls))
    return rows


def median_piti(city, rate=6.5):
    down = int(city["median_price"] * 0.2)
    loan = city["median_price"] - down
    r = (rate / 100) / 12
    n = 360
    factor = r * math.pow(1 + r, n) / (math.pow(1 + r, n) - 1)
    mortgage = loan * factor
    tax = (city["median_price"] * city["tax_pct"] / 100) / 12
    ins = (city["median_price"] * city["ins_pct"] / 100) / 12
    hoa = city["hoa"]
    piti = mortgage + tax + ins + hoa
    total = piti or 1
    return {
        "mortgage": mortgage,
        "tax": tax,
        "ins": ins,
        "hoa": hoa,
        "piti": piti,
        "pct": {
            "mortgage": round(mortgage / total * 100),
            "tax": round(tax / total * 100),
            "ins": round(ins / total * 100),
            "hoa": round(hoa / total * 100),
        },
    }


def count_syllables(word: str) -> int:
    word = word.lower().strip(".,!?;:'\"()[]")
    if not word:
        return 0
    if len(word) <= 3:
        return 1
    word = re.sub(r"e$", "", word)
    vowels = "aeiouy"
    count = 0
    prev_vowel = False
    for ch in word:
        is_vowel = ch in vowels
        if is_vowel and not prev_vowel:
            count += 1
        prev_vowel = is_vowel
    return max(1, count)


def flesch_reading_ease(text: str) -> float:
    words = re.findall(r"[A-Za-z']+", text)
    if not words:
        return 0.0
    sentences = max(1, len(re.findall(r"[.!?]+", text)))
    syllables = sum(count_syllables(w) for w in words)
    return 206.835 - 1.015 * (len(words) / sentences) - 84.6 * (syllables / len(words))


def visible_text_words(html: str) -> int:
    text = re.sub(r"<script[\s\S]*?</script>", " ", html, flags=re.I)
    text = re.sub(r"<style[\s\S]*?</style>", " ", text, flags=re.I)
    text = re.sub(r"<[^>]+>", " ", text)
    return len(text.split())


def build_state_toc_html(slug: str, ext: dict) -> str:
    entries: list[tuple[str, str, str | None]] = [
        ("ha-calculator", "Affordability calculator", None),
        ("ha-local-stats", "At a glance", None),
        ("ha-piti-breakdown", "Payment breakdown", None),
        ("ha-income-tiers", "Salary tiers", None),
        ("ha-cities", "City comparison", None),
        ("ha-rules", "28/36 rule", "State guides"),
        (f"ha-narrative-{slug}", "Buying context", None),
    ]
    for i, block in enumerate(ext.get("long_tail", [])):
        entries.append((f"ha-lt-{slug}-{i}", toc_label(block["h2"]), None))
    entries.extend([
        ("ha-rent-buy", "Rent vs buy", None),
        ("ha-tips", "First-time buyer tips", None),
        ("ha-related", "Related tools", "More"),
        ("ha-faq", "FAQ", None),
    ])
    rows: list[str] = []
    current_group = None
    for anchor_id, label, group in entries:
        if group and group != current_group:
            rows.append(f'          <li class="ha-city-toc__group" aria-hidden="true">{group}</li>')
            current_group = group
        rows.append(
            f'          <li><a href="#{anchor_id}" class="ha-city-toc__link" data-ha-toc-link>{label}</a></li>'
        )
    return "\n".join(rows)


def state_page(slug, data):
    ext = STATE_EXTENDED.get(slug, {})
    all_faqs = list(data.get("faqs", [])) + ext.get("extra_faqs", [])
    faq_html = "\n".join(
        f'          <article class="faq-item"><h3>{q}</h3><p>{a}</p></article>'
        for q, a in all_faqs
    )
    faq_schema = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in all_faqs],
    }
    cities_html = "\n".join(
        f'          <a class="ha-city-chip" href="/living/housing/how-much-house-can-i-afford/{slug}/{cs}">{c["name"]}</a>'
        for cs, c in data["cities"].items()
    )
    city_cards = "\n".join(
        f"""          <a class="ha-state-card" href="/living/housing/how-much-house-can-i-afford/{slug}/{cs}">
            <h3>{c['name']}</h3>
            <p class="ha-state-card__meta">Median {fmt(c['median_price'])} · Income {fmt(c['median_income'])}</p>
            <p class="ha-state-card__meta">{c['pressure']}</p>
            <span class="ha-state-card__cta">Open {c['name']} calculator →</span>
          </a>"""
        for cs, c in data["cities"].items()
    )
    city_rows = "\n".join(
        f"""              <tr>
                <th scope="row"><a href="/living/housing/how-much-house-can-i-afford/{slug}/{cs}">{c['name']}</a></th>
                <td>{fmt(c['median_price'])}</td>
                <td>{fmt(c['median_income'])}</td>
                <td>{c['pressure']}</td>
              </tr>"""
        for cs, c in data["cities"].items()
    )
    down_default = int(data["median_price"] * 0.2)
    income_needed = int(data["median_price"] / 3.2)
    salary_blurb = data.get("salary_blurb", f"Median home near {fmt(data['median_price'])} often needs gross pay well above {fmt(data['median_income'])} to stay inside the 28% rule with 20% down.")
    ins_month = int(data["median_price"] * data["ins_pct"] / 100 / 12)
    tax_month = int(data["median_price"] * data["tax_pct"] / 100 / 12)
    state_narrative = paragraphs_html(data.get("narrative", []))
    extra_narrative = paragraphs_html(ext.get("extra_narrative", []))
    piti = median_piti(data)
    tier_rows = income_tier_rows(data)
    tier_table = "\n".join(
        f"""              <tr>
                <td>{fmt(gross)}</td>
                <td>{fmt(price)}</td>
                <td><span class="ha-results__stress {cls}">{label}</span></td>
              </tr>"""
        for gross, price, label, cls in tier_rows
    )
    long_tail_html = ""
    for i, block in enumerate(ext.get("long_tail", [])):
        sid = f"ha-lt-{slug}-{i}"
        long_tail_html += f"""
    <section class="ha-section ha-section--alt" id="{sid}" aria-labelledby="{sid}-title">
      <div class="container content-page">
        <h2 id="{sid}-title">{block['h2']}</h2>
{paragraphs_html(block['paras'], indent="        ")}
      </div>
    </section>"""
    tips_html = "\n".join(f"          <li>{t}</li>" for t in ext.get("buyer_tips", []))
    rent_vs_buy = ext.get(
        "rent_vs_buy",
        f"Compare rent and buy with your stay timeline in {data['name']}. Run both sides in our rent vs buy tool before you size up.",
    )
    toc_list_html = build_state_toc_html(slug, ext)
    col_link = data.get("col_link", "/living/housing/cost-of-living-by-city")
    salary_link = data.get("salary_link", "/living/lifestyle/comfortable-salary-us")
    rent_link = data.get("rent_link", "/rent-vs-buy-calculator")
    tax_link = data.get("tax_link", f"/hourly-to-salary-after-tax/state/{slug}/")

    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>How Much House Can You Afford in {data['name']}? Income, Tax &amp; City Guide (2026) | Income Clarity</title>
  <meta name="description" content="How much house can you afford in {data['name']}? Median price {fmt(data['median_price'])}, salary tiers, property tax, insurance, city breakdowns, and free PITI calculator.">
  <link rel="canonical" href="https://www.incomeclaritylab.com/living/housing/how-much-house-can-i-afford/{slug}">
  <link rel="stylesheet" href="/styles.css">
  <link rel="stylesheet" href="/styles-living-system.css">
  <link rel="icon" type="image/png" href="/images/logo.png">
  <link rel="apple-touch-icon" href="/images/logo.png">
  <script type="application/ld+json">{json.dumps(faq_schema, ensure_ascii=False)}</script>
{URL_SCRIPT}
</head>
<body class="ha-page living-tool-page ha-city-page">
  <header class="site-header">
    <div class="container nav-wrap">
      <a class="logo" href="/"><img src="/images/logo.png" alt="" width="32" height="32"><span class="logo-text">Income Clarity</span></a>
      <nav class="nav-links" aria-label="Primary">
        <a href="/hourly-to-salary-after-tax">Income</a>
        <a href="/debt">Debt</a>
        <a href="/rent-vs-buy-calculator">Living</a>
        <a href="/1099-vs-w2-calculator">Freelance</a>
      </nav>
    </div>
  </header>
  <main>
    <section class="ha-hero" id="ha-calculator" aria-labelledby="ha-title">
      <div class="container">
        <nav class="take-home-return-nav" aria-label="Breadcrumb">
          <ol class="take-home-return-breadcrumbs">
            <li><a href="/living/housing/how-much-house-can-i-afford">House affordability</a></li>
            <li aria-current="page">{data['name']}</li>
          </ol>
        </nav>
        <span class="label">Living · {data['name']}</span>
        <h1 id="ha-title">How Much House Can You Afford in {data['name']}?</h1>
        <p class="lead">{data['insight']} Run the calculator — this page also has salary tiers, city comparisons, and {data['name']} buyer guides.</p>
        <div class="ha-hero-grid">
        <div class="ha-calc-shell">
          <form id="ha-calc-form" class="ha-calc-form" aria-label="{data['name']} house affordability calculator">
            <label class="ha-calc__field"><span>Annual income ($)</span><input type="number" id="ha-income" min="20000" step="1000" value="{data['median_income']}" required></label>
            <label class="ha-calc__field"><span>Other monthly debt ($)</span><input type="number" id="ha-debt" min="0" step="25" value="300" required></label>
            <label class="ha-calc__field"><span>Down payment ($)</span><input type="number" id="ha-down" min="0" step="5000" value="{down_default}" required></label>
            <label class="ha-calc__field"><span>Interest rate (%)</span><input type="number" id="ha-rate" min="2" max="15" step="0.05" value="6.5" required></label>
            <input type="hidden" id="ha-location" value="{slug}">
            <div class="ha-calc__actions"><button type="submit" class="ha-calc__btn">Calculate max home price</button></div>
          </form>
          <div id="ha-calc-results" class="ha-results" hidden aria-live="polite"></div>
        </div>
      <aside class="ha-city-toc ha-city-toc--hero" id="ha-toc">
        <div class="ha-city-toc__card">
          <button type="button" class="ha-city-toc__toggle" aria-expanded="true" aria-controls="ha-toc-panel">
            <span class="ha-city-toc__toggle-text">
              <span class="ha-city-toc__title">On this page</span>
              <span class="ha-city-toc__kicker">City guides, salary tiers, tax breakdown &amp; more</span>
            </span>
            <svg class="ha-city-toc__toggle-icon" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true"><path fill-rule="evenodd" d="M5.23 7.21a.75.75 0 011.06.02L10 10.94l3.71-3.71a.75.75 0 111.06 1.06l-4.24 4.25a.75.75 0 01-1.06 0L5.21 8.29a.75.75 0 01.02-1.08z" clip-rule="evenodd"/></svg>
          </button>
          <nav class="ha-city-toc__panel" id="ha-toc-panel" aria-label="On this page">
            <ul class="ha-city-toc__list">
{toc_list_html}
            </ul>
          </nav>
        </div>
      </aside>
        </div>
        <div class="ha-city-chips" aria-label="Cities in {data['name']}">
          {cities_html}
        </div>
      </div>
    </section>

    <section class="ha-section" id="ha-local-stats" aria-labelledby="ha-glance-title">
      <div class="container content-page">
        <h2 id="ha-glance-title">{data['name']} home affordability at a glance</h2>
        <p class="ha-section__lead">Planning figures for {data['name']}. Your lender quote and tax bill may differ — use these as a starting point, then open a city page for local medians.</p>
        <div class="ha-glance-grid">
          <div class="ha-glance-card"><span class="ha-glance-card__n">{fmt(data['median_price'])}</span><span class="ha-glance-card__l">Median home price</span></div>
          <div class="ha-glance-card"><span class="ha-glance-card__n">{fmt(data['median_income'])}</span><span class="ha-glance-card__l">Median household income</span></div>
          <div class="ha-glance-card"><span class="ha-glance-card__n">{fmt(income_needed)}+</span><span class="ha-glance-card__l">Rough gross for median (3× rule)</span></div>
          <div class="ha-glance-card"><span class="ha-glance-card__n">{fmt(int(piti['piti']))}/mo</span><span class="ha-glance-card__l">Est. PITI on median (20% down)</span></div>
        </div>
        <p>On a median {fmt(data['median_price'])} home, property tax near {data['tax_pct']}% is about <strong>{fmt(tax_month)}/month</strong>. Insurance near {data['ins_pct']}% of value is about <strong>{fmt(ins_month)}/month</strong>. HOA is about <strong>{fmt(data['hoa'])}/month</strong> where it applies.</p>
        <p>{salary_blurb}</p>
        <aside class="what-this-means" role="note">
          <p class="what-this-means__title">What this means for you</p>
          <p>Use the calculator with your real income and debts. If the stress label is <strong>Stretched</strong>, open a city page — smaller metros may fit where the state median does not.</p>
        </aside>
        <p>Compare with <a href="/living/housing/how-much-house-can-i-afford/{data['compare_slug']}">{data['compare']}</a>: {data['compare_note']}</p>
      </div>
    </section>

    <section class="ha-section ha-section--tone" id="ha-piti-breakdown" aria-labelledby="ha-piti-title">
      <div class="container content-page">
        <h2 id="ha-piti-title">Monthly payment breakdown on a median {data['name']} home</h2>
        <p class="ha-section__lead">Estimated PITI at {fmt(data['median_price'])} list, 20% down, 6.5% rate, and {data['name']} tax and insurance defaults.</p>
        <div class="ha-piti-visual">
          <div class="ha-piti-visual__total">
            <span class="ha-results__label">Estimated monthly PITI</span>
            <p class="ha-results__price">{fmt(int(piti['piti']))}<span>/mo</span></p>
          </div>
          <div class="ha-piti-bars">
            <div class="ha-piti-bar-row"><span>Principal &amp; interest</span><div class="ha-piti-bar"><span style="width:{piti['pct']['mortgage']}%"></span></div><span>{fmt(int(piti['mortgage']))}</span></div>
            <div class="ha-piti-bar-row"><span>Property tax</span><div class="ha-piti-bar"><span style="width:{piti['pct']['tax']}%"></span></div><span>{fmt(int(piti['tax']))}</span></div>
            <div class="ha-piti-bar-row"><span>Insurance</span><div class="ha-piti-bar"><span style="width:{piti['pct']['ins']}%"></span></div><span>{fmt(int(piti['ins']))}</span></div>
            <div class="ha-piti-bar-row"><span>HOA</span><div class="ha-piti-bar"><span style="width:{max(piti['pct']['hoa'], 4)}%"></span></div><span>{fmt(int(piti['hoa']))}</span></div>
          </div>
        </div>
        <p>In {data['name']}, buyers who only compare list price to income miss tax and insurance. Run the calculator with your real debts — the 36% back-end rule includes car loans and cards.</p>
      </div>
    </section>

    <section class="ha-section" id="ha-income-tiers" aria-labelledby="ha-tiers-title">
      <div class="container content-page">
        <h2 id="ha-tiers-title">How much house can you afford in {data['name']} by salary?</h2>
        <p class="ha-section__lead">Max home price at common gross salaries, 6.5% rate, $300/month other debt, and {data['name']} tax and insurance defaults.</p>
        <div class="ha-compare-table-wrap">
          <table class="debt-data-table ha-tier-table">
            <caption>Affordable home price by gross annual income in {data['name']}</caption>
            <thead><tr><th scope="col">Gross salary</th><th scope="col">Max home (est.)</th><th scope="col">Stress</th></tr></thead>
            <tbody>
{tier_table}
            </tbody>
          </table>
        </div>
        <p>These rows assume no down payment in the solver — your down payment raises what you can buy. City medians vary — open Houston, Dallas, or your target city for local numbers.</p>
        <p><a href="{tax_link}">{data['name']} take-home pay calculator</a> · <a href="{salary_link}">Comfortable salary in {data['name']}</a></p>
      </div>
    </section>

    <section class="ha-section ha-section--alt" id="ha-cities" aria-labelledby="ha-cities-title">
      <div class="container content-page">
        <h2 id="ha-cities-title">Top cities in {data['name']} for home buyers</h2>
        <p class="ha-section__lead">Median price and income vary a lot inside one state. Pick your city for local tax, insurance, and a prefilled calculator.</p>
        <div class="ha-state-grid">
{city_cards}
        </div>
        <div class="ha-compare-table-wrap">
          <table class="debt-data-table">
            <caption>Median price, income, and affordability pressure by city in {data['name']}</caption>
            <thead><tr><th scope="col">City</th><th scope="col">Median price</th><th scope="col">Median income</th><th scope="col">Pressure</th></tr></thead>
            <tbody>
{city_rows}
            </tbody>
          </table>
        </div>
      </div>
    </section>

    <section class="ha-section" id="ha-rules" aria-labelledby="ha-rules-title">
      <div class="container content-page">
        <h2 id="ha-rules-title">The 28/36 rule in {data['name']}</h2>
        <p class="ha-section__lead">Lenders often use two caps. Our calculator applies both so you see a realistic max — not just what a bank might pre-approve.</p>
        <div class="ha-rules-grid">
          <article class="ha-rules-card">
            <h3>28% front-end</h3>
            <p>Your full housing payment — mortgage, tax, insurance, and HOA — should stay near or below 28% of gross monthly income. In {data['name']}, tax and insurance often move the stress meter before list price does.</p>
          </article>
          <article class="ha-rules-card">
            <h3>36% back-end</h3>
            <p>All monthly debt plus housing should stay near or below 36% of gross income. Car loans and student debt shrink your max home price even when income is strong.</p>
          </article>
          <article class="ha-rules-card">
            <h3>Stress meter</h3>
            <p>We label results Comfortable, Moderate, Stretched, or Over limit. Shop below your max if you want room for repairs, childcare, or savings.</p>
          </article>
        </div>
      </div>
    </section>

    <section class="ha-section ha-section--alt" id="ha-narrative-{slug}" aria-labelledby="ha-narrative-title-{slug}">
      <div class="container content-page">
        <h2 id="ha-narrative-title-{slug}">Buying a home in {data['name']}: what to know</h2>
{state_narrative}
{extra_narrative}
        <aside class="what-this-means" role="note">
          <p class="what-this-means__title">What this means for you</p>
          <p>The state median is a blend — your target city may sit far above or below. Open a city page before you set a max offer price.</p>
        </aside>
      </div>
    </section>
{long_tail_html}
    <section class="ha-section" id="ha-rent-buy" aria-labelledby="ha-rent-buy-title">
      <div class="container content-page">
        <h2 id="ha-rent-buy-title">Rent vs buy in {data['name']}</h2>
        <p>{rent_vs_buy}</p>
        <p><a href="{rent_link}">Rent vs buy calculator</a> · <a href="/living/housing/how-much-rent-can-i-afford">How much rent can I afford?</a></p>
      </div>
    </section>

    <section class="ha-section ha-section--alt" id="ha-tips" aria-labelledby="ha-tips-title">
      <div class="container content-page">
        <h2 id="ha-tips-title">First-time buyer tips in {data['name']}</h2>
        <ul class="ha-tips-list">
{tips_html}
        </ul>
      </div>
    </section>

    <section class="ha-section" id="ha-related" aria-labelledby="ha-related-title">
      <div class="container content-page">
        <h2 id="ha-related-title">Related tools for {data['name']} buyers</h2>
        <div class="ha-related-grid">
          <a class="ha-related-card" href="{col_link}"><span>Cost of living</span><strong>{data['name']} COL guide →</strong></a>
          <a class="ha-related-card" href="{salary_link}"><span>Comfortable salary</span><strong>{data['name']} salary target →</strong></a>
          <a class="ha-related-card" href="/living/housing/how-much-house-can-i-afford"><span>US calculator</span><strong>National affordability →</strong></a>
          <a class="ha-related-card" href="/living/housing/how-much-house-can-i-afford/{data['compare_slug']}"><span>Compare states</span><strong>{data['compare']} affordability →</strong></a>
        </div>
        <ul class="col-related__list">
          <li><a href="{col_link}">Cost of living in {data['name']}</a></li>
          <li><a href="/living/housing/how-much-rent-can-i-afford">Rent affordability in {data['name']}</a></li>
          <li><a href="{tax_link}">{data['name']} take-home pay</a></li>
        </ul>
      </div>
    </section>

    <section class="ha-faq-section" id="ha-faq">
      <div class="container content-page">
        <h2>FAQ — how much house can I afford in {data['name']}?</h2>
        <div class="faq-stack">
{faq_html}
        </div>
      </div>
    </section>

    <div class="container content-page">
      <aside class="eeat-trust" aria-labelledby="eeat-{slug}-title">
        <header class="eeat-trust__header">
          <span class="eeat-trust__kicker">How we built this</span>
          <h2 id="eeat-{slug}-title" class="eeat-trust__title">{data['name']} affordability data</h2>
          <p class="eeat-trust__meta"><time datetime="2026-06-01">Last reviewed: June 1, 2026</time> · <a href="/methodology#affordability">Methodology</a></p>
        </header>
        <p>Median prices, tax, and insurance are rounded planning figures from public listing and census sources. Your quote and lender rules may differ. This is not a loan offer or tax advice.</p>
      </aside>
    </div>
  </main>
  <footer class="site-footer">
    <div class="container footer-layout">
      <p class="footer-copy">© 2026 IncomeClarityLab</p>
    </div>
  </footer>
  <script src="/house-afford.js"></script>
  <script src="/page-toc.js" defer></script>
  <script>
    HouseAfford.bindForm({{ stateSlug: '{slug}', defaultRegion: '{slug}', runOnLoad: true }});
  </script>
</body>
</html>
"""


def toc_label(text: str, max_len: int = 52) -> str:
    if len(text) <= max_len:
        return text
    return text[: max_len - 1].rstrip() + "…"


def build_city_toc_html(city_slug: str, ext: dict) -> str:
    entries: list[tuple[str, str, str | None]] = [
        ("ha-calculator", "Affordability calculator", None),
        ("ha-local-stats", "At a glance", None),
        ("ha-piti-breakdown", "Payment breakdown", None),
        ("ha-income-tiers", "Salary tiers", None),
        ("ha-neighborhoods", "Neighborhoods", None),
        ("ha-rules", "28/36 rule", "Local guides"),
        (f"ha-narrative-{city_slug}", "Local context", None),
    ]
    for i, block in enumerate(ext.get("long_tail", [])):
        entries.append((f"ha-lt-{city_slug}-{i}", toc_label(block["h2"]), None))
    entries.extend([
        ("ha-rent-buy", "Rent vs buy", None),
        ("ha-tips", "First-time buyer tips", None),
        ("ha-related", "Related tools", "More"),
        ("ha-faq", "FAQ", None),
    ])
    rows: list[str] = []
    current_group = None
    for anchor_id, label, group in entries:
        if group and group != current_group:
            rows.append(f'          <li class="ha-city-toc__group" aria-hidden="true">{group}</li>')
            current_group = group
        rows.append(
            f'          <li><a href="#{anchor_id}" class="ha-city-toc__link" data-ha-toc-link>{label}</a></li>'
        )
    return "\n".join(rows)


def city_page(state_slug, state_data, city_slug, city):
    down = int(city["median_price"] * 0.2)
    income_needed = int(city["median_price"] / 3.2)
    local_note = city.get("local_note", city["pressure"])
    ext = EXTENDED.get((state_slug, city_slug), {})
    all_faqs = list(city.get("faqs", [])) + ext.get("extra_faqs", [])
    faq_html = "\n".join(
        f'          <article class="faq-item"><h3>{q}</h3><p>{a}</p></article>'
        for q, a in all_faqs
    )
    faq_schema = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in all_faqs],
    }
    tax_month = int(city["median_price"] * city["tax_pct"] / 100 / 12)
    ins_month = int(city["median_price"] * city["ins_pct"] / 100 / 12)
    piti = median_piti(city)
    tier_rows = income_tier_rows(city)
    other_cities = [(cs, c["name"]) for cs, c in state_data["cities"].items() if cs != city_slug]
    sibling_links = " · ".join(
        f'<a href="/living/housing/how-much-house-can-i-afford/{state_slug}/{cs}">{name}</a>'
        for cs, name in other_cities
    )
    city_narrative = paragraphs_html(city.get("narrative", []))
    extra_narrative = paragraphs_html(ext.get("extra_narrative", []))
    rent_vs_buy = ext.get("rent_vs_buy", f"Compare rent and buy with your stay timeline. {state_data['name']} has no one-size answer — run the numbers for your zip and rate.")
    col_link = ext.get("col_link", f"/living/housing/cost-of-living-by-city/{state_slug}/{city_slug}")
    salary_link = ext.get("salary_link", state_data.get("salary_link", "/living/lifestyle/comfortable-salary-us"))
    rent_link = state_data.get("rent_link", "/rent-vs-buy-calculator")
    tax_link = state_data.get("tax_link", f"/hourly-to-salary-after-tax/state/{state_slug}/")
    scenario_links = ext.get("scenario_links", [])

    neighborhoods = ext.get("neighborhoods", [])
    nh_cards = "\n".join(
        f"""          <article class="ha-nh-card">
            <h3>{n['name']}</h3>
            <p class="ha-nh-card__range">{n['range']}</p>
            <p>{n['note']}</p>
          </article>"""
        for n in neighborhoods
    )

    tier_table = "\n".join(
        f"""              <tr>
                <td>{fmt(gross)}</td>
                <td>{fmt(price)}</td>
                <td><span class="ha-results__stress {cls}">{label}</span></td>
              </tr>"""
        for gross, price, label, cls in tier_rows
    )

    long_tail_html = ""
    for i, block in enumerate(ext.get("long_tail", [])):
        sid = f"ha-lt-{city_slug}-{i}"
        long_tail_html += f"""
      <section class="ha-section ha-section--alt" id="{sid}" aria-labelledby="{sid}-title">
        <div class="container content-page">
          <h2 id="{sid}-title">{block['h2']}</h2>
{paragraphs_html(block['paras'], indent="          ")}
        </div>
      </section>"""

    tips_html = "\n".join(f"          <li>{t}</li>" for t in ext.get("buyer_tips", []))
    scenario_html = "\n".join(
        f'          <a class="ha-related-card" href="{href}"><span>{label}</span><strong>Salary scenario →</strong></a>'
        for label, href in scenario_links
    )
    toc_list_html = build_city_toc_html(city_slug, ext)

    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>How Much House Can You Afford in {city['name']}? Income, Payment &amp; Local Costs (2026) | Income Clarity</title>
  <meta name="description" content="How much house can you afford in {city['name']}, {state_data['name']}? Median price {fmt(city['median_price'])}, salary tiers, property tax, insurance, HOA, and a free PITI calculator.">
  <link rel="canonical" href="https://www.incomeclaritylab.com/living/housing/how-much-house-can-i-afford/{state_slug}/{city_slug}">
  <link rel="stylesheet" href="/styles.css">
  <link rel="stylesheet" href="/styles-living-system.css">
  <link rel="icon" type="image/png" href="/images/logo.png">
  <link rel="apple-touch-icon" href="/images/logo.png">
  <script type="application/ld+json">{json.dumps(faq_schema, ensure_ascii=False)}</script>
{URL_SCRIPT}
</head>
<body class="ha-page living-tool-page ha-city-page">
  <header class="site-header">
    <div class="container nav-wrap">
      <a class="logo" href="/"><img src="/images/logo.png" alt="" width="32" height="32"><span class="logo-text">Income Clarity</span></a>
      <nav class="nav-links" aria-label="Primary">
        <a href="/hourly-to-salary-after-tax">Income</a>
        <a href="/debt">Debt</a>
        <a href="/rent-vs-buy-calculator">Living</a>
        <a href="/1099-vs-w2-calculator">Freelance</a>
      </nav>
    </div>
  </header>
  <main>
    <section class="ha-hero" id="ha-calculator">
      <div class="container">
        <nav class="take-home-return-nav" aria-label="Breadcrumb">
          <ol class="take-home-return-breadcrumbs">
            <li><a href="/living/housing/how-much-house-can-i-afford">US</a></li>
            <li><a href="/living/housing/how-much-house-can-i-afford/{state_slug}">{state_data['name']}</a></li>
            <li aria-current="page">{city['name']}</li>
          </ol>
        </nav>
        <span class="label">{city['name']} · {state_data['name']}</span>
        <h1>How Much House Can You Afford in {city['name']}?</h1>
        <p class="lead">Median home near <strong>{fmt(city['median_price'])}</strong>. Typical income near <strong>{fmt(city['median_income'])}</strong>. {city['pressure']} Run the calculator — this page also has salary tiers, neighborhood prices, and local buyer guides.</p>
        <div class="ha-hero-grid">
        <div class="ha-calc-shell">
          <form id="ha-calc-form" class="ha-calc-form" aria-label="{city['name']} house affordability calculator">
            <label class="ha-calc__field"><span>Annual income ($)</span><input type="number" id="ha-income" min="20000" step="1000" value="{city['median_income']}" required></label>
            <label class="ha-calc__field"><span>Other monthly debt ($)</span><input type="number" id="ha-debt" min="0" step="25" value="300" required></label>
            <label class="ha-calc__field"><span>Down payment ($)</span><input type="number" id="ha-down" min="0" step="5000" value="{down}" required></label>
            <label class="ha-calc__field"><span>Interest rate (%)</span><input type="number" id="ha-rate" min="2" max="15" step="0.05" value="6.5" required></label>
            <input type="hidden" id="ha-location" value="{state_slug}">
            <div class="ha-calc__actions"><button type="submit" class="ha-calc__btn">Calculate max home price</button></div>
          </form>
          <div id="ha-calc-results" class="ha-results" hidden aria-live="polite"></div>
        </div>
      <aside class="ha-city-toc ha-city-toc--hero" id="ha-toc">
        <div class="ha-city-toc__card">
          <button type="button" class="ha-city-toc__toggle" aria-expanded="true" aria-controls="ha-toc-panel">
            <span class="ha-city-toc__toggle-text">
              <span class="ha-city-toc__title">On this page</span>
              <span class="ha-city-toc__kicker">Guides, salary tiers, neighborhoods &amp; more</span>
            </span>
            <svg class="ha-city-toc__toggle-icon" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true"><path fill-rule="evenodd" d="M5.23 7.21a.75.75 0 011.06.02L10 10.94l3.71-3.71a.75.75 0 111.06 1.06l-4.24 4.25a.75.75 0 01-1.06 0L5.21 8.29a.75.75 0 01.02-1.08z" clip-rule="evenodd"/></svg>
          </button>
          <nav class="ha-city-toc__panel" id="ha-toc-panel" aria-label="On this page">
            <ul class="ha-city-toc__list">
{toc_list_html}
            </ul>
          </nav>
        </div>
      </aside>
        </div>
      </div>
    </section>

    <section class="ha-section" id="ha-local-stats" aria-labelledby="ha-glance-title">
      <div class="container content-page">
        <h2 id="ha-glance-title">{city['name']} home affordability at a glance</h2>
        <p class="ha-section__lead">Planning figures for {city['name']}, {state_data['name']}. Your lender quote and tax bill may differ — use these as a starting point.</p>
        <div class="ha-glance-grid">
          <div class="ha-glance-card"><span class="ha-glance-card__n">{fmt(city['median_price'])}</span><span class="ha-glance-card__l">Median home price</span></div>
          <div class="ha-glance-card"><span class="ha-glance-card__n">{fmt(city['median_income'])}</span><span class="ha-glance-card__l">Median household income</span></div>
          <div class="ha-glance-card"><span class="ha-glance-card__n">{fmt(income_needed)}+</span><span class="ha-glance-card__l">Rough gross for median (3× rule)</span></div>
          <div class="ha-glance-card"><span class="ha-glance-card__n">{fmt(int(piti['piti']))}/mo</span><span class="ha-glance-card__l">Est. PITI on median (20% down)</span></div>
        </div>
        <p>On a median {fmt(city['median_price'])} home, property tax near {city['tax_pct']}% is about <strong>{fmt(tax_month)}/month</strong>. Insurance near {city['ins_pct']}% of value is about <strong>{fmt(ins_month)}/month</strong>. HOA is about <strong>{fmt(city['hoa'])}/month</strong> where it applies.</p>
        <p>{local_note}</p>
        <aside class="what-this-means" role="note">
          <p class="what-this-means__title">What this means for you</p>
          <p>Change income, debt, and down payment in the calculator above. Compare with {sibling_links}.</p>
        </aside>
      </div>
    </section>

    <section class="ha-section ha-section--tone" id="ha-piti-breakdown" aria-labelledby="ha-piti-title">
      <div class="container content-page">
        <h2 id="ha-piti-title">Monthly payment breakdown on a median {city['name']} home</h2>
        <p class="ha-section__lead">Estimated PITI at {fmt(city['median_price'])} list, 20% down, 6.5% rate, and {city['name']} tax and insurance defaults. Principal and interest are the largest line — but tax, insurance, and HOA still move the stress meter.</p>
        <div class="ha-piti-visual">
          <div class="ha-piti-visual__total">
            <span class="ha-results__label">Estimated monthly PITI</span>
            <p class="ha-results__price">{fmt(int(piti['piti']))}<span>/mo</span></p>
          </div>
          <div class="ha-piti-bars">
            <div class="ha-piti-bar-row"><span>Principal &amp; interest</span><div class="ha-piti-bar"><span style="width:{piti['pct']['mortgage']}%"></span></div><span>{fmt(int(piti['mortgage']))}</span></div>
            <div class="ha-piti-bar-row"><span>Property tax</span><div class="ha-piti-bar"><span style="width:{piti['pct']['tax']}%"></span></div><span>{fmt(int(piti['tax']))}</span></div>
            <div class="ha-piti-bar-row"><span>Insurance</span><div class="ha-piti-bar"><span style="width:{piti['pct']['ins']}%"></span></div><span>{fmt(int(piti['ins']))}</span></div>
            <div class="ha-piti-bar-row"><span>HOA</span><div class="ha-piti-bar"><span style="width:{max(piti['pct']['hoa'], 4)}%"></span></div><span>{fmt(int(piti['hoa']))}</span></div>
          </div>
        </div>
        <p>In {city['name']}, buyers who only compare list price to income miss tax and insurance. Run the calculator with your real debts — the 36% back-end rule includes car loans and cards.</p>
      </div>
    </section>

    <section class="ha-section" id="ha-income-tiers" aria-labelledby="ha-tiers-title">
      <div class="container content-page">
        <h2 id="ha-tiers-title">How much house can you afford in {city['name']} by salary?</h2>
        <p class="ha-section__lead">Max home price at common gross salaries, 6.5% rate, $300/month other debt, and {city['name']} tax and insurance. Stress label uses the 28% housing cap.</p>
        <div class="ha-compare-table-wrap">
          <table class="debt-data-table ha-tier-table">
            <caption>Affordable home price by gross annual income in {city['name']}</caption>
            <thead><tr><th scope="col">Gross salary</th><th scope="col">Max home (est.)</th><th scope="col">Stress</th></tr></thead>
            <tbody>
{tier_table}
            </tbody>
          </table>
        </div>
        <p>These rows assume no down payment in the solver — your down payment raises what you can buy. Enter your real numbers in the calculator for a personal max.</p>
        <p><a href="{tax_link}">{state_data['name']} take-home pay calculator</a> · <a href="{salary_link}">Comfortable salary in {city['name']}</a></p>
      </div>
    </section>

    <section class="ha-section ha-section--alt" id="ha-neighborhoods" aria-labelledby="ha-nh-title">
      <div class="container content-page">
        <h2 id="ha-nh-title">{city['name']} home prices by area</h2>
        <p class="ha-section__lead">The citywide median blends expensive and affordable pockets. Use these ranges as a map — not a guarantee for any one listing.</p>
        <div class="ha-nh-grid">
{nh_cards}
        </div>
      </div>
    </section>

    <section class="ha-section" id="ha-rules" aria-labelledby="ha-rules-title">
      <div class="container content-page">
        <h2 id="ha-rules-title">The 28/36 rule in {city['name']}</h2>
        <p class="ha-section__lead">Lenders often use two caps. Our calculator applies both so you see a realistic max — not just what a bank might pre-approve.</p>
        <div class="ha-rules-grid">
          <article class="ha-rules-card">
            <h3>28% front-end</h3>
            <p>Your full housing payment — mortgage, tax, insurance, and HOA — should stay near or below 28% of gross monthly income. In {city['name']}, insurance and HOA often push buyers over this line before list price does.</p>
          </article>
          <article class="ha-rules-card">
            <h3>36% back-end</h3>
            <p>All monthly debt plus housing should stay near or below 36% of gross income. A $400 car payment and $250 in student loans shrink your max home price even when income is strong.</p>
          </article>
          <article class="ha-rules-card">
            <h3>Stress meter</h3>
            <p>We label results Comfortable, Moderate, Stretched, or Over limit. Shop below your max if you want room for repairs, childcare, or savings — especially in {state_data['name']} where tax and insurance vary by block.</p>
          </article>
        </div>
      </div>
    </section>

    <section class="ha-section ha-section--alt" id="ha-narrative-{city_slug}" aria-labelledby="ha-narrative-title-{city_slug}">
      <div class="container content-page">
        <h2 id="ha-narrative-title-{city_slug}">Buying a home in {city['name']}: local context</h2>
{city_narrative}
{extra_narrative}
        <aside class="what-this-means" role="note">
          <p class="what-this-means__title">What this means for you</p>
          <p>Run the calculator twice — once at list price and once $50k below — to see how fast the stress label changes in {city['name']}.</p>
        </aside>
      </div>
    </section>
{long_tail_html}
    <section class="ha-section" id="ha-rent-buy" aria-labelledby="ha-rent-buy-title">
      <div class="container content-page">
        <h2 id="ha-rent-buy-title">Rent vs buy in {city['name']}</h2>
        <p>{rent_vs_buy}</p>
        <p><a href="{rent_link}">Rent vs buy calculator</a> · <a href="/living/housing/how-much-rent-can-i-afford">How much rent can I afford?</a></p>
      </div>
    </section>

    <section class="ha-section ha-section--alt" id="ha-tips" aria-labelledby="ha-tips-title">
      <div class="container content-page">
        <h2 id="ha-tips-title">First-time buyer tips in {city['name']}</h2>
        <ul class="ha-tips-list">
{tips_html}
        </ul>
      </div>
    </section>

    <section class="ha-section" id="ha-related" aria-labelledby="ha-related-title">
      <div class="container content-page">
        <h2 id="ha-related-title">Related tools for {city['name']}</h2>
        <div class="ha-related-grid">
          <a class="ha-related-card" href="{col_link}"><span>Cost of living</span><strong>{city['name']} COL guide →</strong></a>
          <a class="ha-related-card" href="{salary_link}"><span>Comfortable salary</span><strong>{city['name']} salary target →</strong></a>
          <a class="ha-related-card" href="/living/housing/how-much-house-can-i-afford/{state_slug}"><span>{state_data['name']} overview</span><strong>All {state_data['name']} cities →</strong></a>
          <a class="ha-related-card" href="/living/housing/how-much-house-can-i-afford"><span>US calculator</span><strong>National affordability →</strong></a>
{scenario_html}
        </div>
        <p><a href="/living/housing/how-much-house-can-i-afford/{state_slug}">All {state_data['name']} cities</a> · <a href="/living/housing/how-much-house-can-i-afford">US calculator</a></p>
      </div>
    </section>

    <section class="ha-faq-section" id="ha-faq">
      <div class="container content-page">
        <h2>FAQ — how much house can I afford in {city['name']}?</h2>
        <div class="faq-stack">
{faq_html}
        </div>
      </div>
    </section>

    <div class="container content-page">
      <aside class="eeat-trust" aria-labelledby="eeat-{city_slug}-title">
        <header class="eeat-trust__header">
          <span class="eeat-trust__kicker">How we built this</span>
          <h2 id="eeat-{city_slug}-title" class="eeat-trust__title">{city['name']} affordability data</h2>
          <p class="eeat-trust__meta"><time datetime="2026-06-01">Last reviewed: June 1, 2026</time> · <a href="/methodology#affordability">Methodology</a></p>
        </header>
        <p>Median prices, tax, and insurance are rounded planning figures from public listing and census sources. Your quote and lender rules may differ. This is not a loan offer or tax advice.</p>
      </aside>
    </div>
  </main>
  <footer class="site-footer">
    <div class="container footer-layout">
      <p class="footer-copy">© 2026 IncomeClarityLab</p>
    </div>
  </footer>
  <script src="/house-afford.js"></script>
  <script src="/page-toc.js" defer></script>
  <script>
    HouseAfford.bindForm({{
      stateSlug: '{state_slug}',
      city: {{ taxPct: {city['tax_pct']}, insPct: {city['ins_pct']}, hoa: {city['hoa']} }},
      runOnLoad: true
    }});
  </script>
</body>
</html>
"""


def main():
    issues = []
    for slug, data in STATES.items():
        state_dir = BASE / slug
        state_dir.mkdir(parents=True, exist_ok=True)
        state_html = state_page(slug, data)
        (state_dir / "index.html").write_text(state_html, encoding="utf-8")
        state_words = visible_text_words(state_html)
        state_text = re.sub(r"<script[\s\S]*?</script>", " ", state_html, flags=re.I)
        state_text = re.sub(r"<[^>]+>", " ", state_text)
        state_fre = flesch_reading_ease(state_text)
        if state_words < 1200:
            issues.append(f"{slug} (state): {state_words} words (need 1200+)")
        if state_fre < 60:
            issues.append(f"{slug} (state): FRE {state_fre:.1f} (need 60+)")
        print(f"  {slug} (state): {state_words} words, FRE {state_fre:.1f}")
        for cs, city in data["cities"].items():
            city_dir = state_dir / cs
            city_dir.mkdir(parents=True, exist_ok=True)
            html = city_page(slug, data, cs, city)
            (city_dir / "index.html").write_text(html, encoding="utf-8")
            words = visible_text_words(html)
            text = re.sub(r"<script[\s\S]*?</script>", " ", html, flags=re.I)
            text = re.sub(r"<[^>]+>", " ", text)
            fre = flesch_reading_ease(text)
            if words < 1200:
                issues.append(f"{slug}/{cs}: {words} words (need 1200+)")
            if fre < 60:
                issues.append(f"{slug}/{cs}: FRE {fre:.1f} (need 60+)")
            print(f"  {slug}/{cs}: {words} words, FRE {fre:.1f}")
        print(f"Wrote {slug} + {len(data['cities'])} cities")
    if issues:
        print("\nValidation issues:")
        for i in issues:
            print(f"  - {i}")
        raise SystemExit(1)


if __name__ == "__main__":
    main()
