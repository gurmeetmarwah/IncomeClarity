#!/usr/bin/env python3
"""Generate state and city house affordability pages."""
from pathlib import Path

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


def paragraphs_html(paragraphs: list[str]) -> str:
    return "\n".join(f"        <p>{p}</p>" for p in paragraphs)


def state_page(slug, data):
    cities_html = "\n".join(
        f'          <a class="ha-city-chip" href="/living/housing/how-much-house-can-i-afford/{slug}/{cs}">{c["name"]}</a>'
        for cs, c in data["cities"].items()
    )
    faq_html = "\n".join(
        f'          <article class="faq-item"><h3>{q}</h3><p>{a}</p></article>'
        for q, a in data["faqs"]
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
    salary_blurb = data.get("salary_blurb", f"Median home near {fmt(data['median_price'])} often needs gross pay well above {fmt(data['median_income'])} to stay inside the 28% rule with 20% down.")
    ins_month = int(data["median_price"] * data["ins_pct"] / 100 / 12)
    tax_month = int(data["median_price"] * data["tax_pct"] / 100 / 12)
    state_narrative = paragraphs_html(data.get("narrative", []))
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>How Much House Can I Afford in {data['name']}? Calculator &amp; City Guide | Income Clarity</title>
  <meta name="description" content="How much house can you afford in {data['name']}? Median price {fmt(data['median_price'])}, local tax and insurance, salary needed, and city breakdowns with calculator.">
  <link rel="canonical" href="https://www.incomeclaritylab.com/living/housing/how-much-house-can-i-afford/{slug}">
  <link rel="stylesheet" href="/styles.css">
  <link rel="stylesheet" href="/styles-living-system.css">
  <link rel="icon" type="image/svg+xml" href="/favicon.svg">
{URL_SCRIPT}
</head>
<body class="ha-page living-tool-page">
  <header class="site-header">
    <div class="container nav-wrap">
      <a class="logo" href="/index.html">Income Clarity</a>
      <nav class="nav-links" aria-label="Primary">
        <a href="/hourly-to-salary-after-tax">Income</a>
        <a href="/credit-card-payoff-calculator">Debt</a>
        <a href="/rent-vs-buy-calculator">Living</a>
        <a href="/1099-vs-w2-calculator">Freelance</a>
      </nav>
    </div>
  </header>
  <main>
    <section class="ha-hero" aria-labelledby="ha-title">
      <div class="container">
        <nav class="take-home-return-nav" aria-label="Breadcrumb">
          <ol class="take-home-return-breadcrumbs">
            <li><a href="/living/housing/how-much-house-can-i-afford">House affordability</a></li>
            <li aria-current="page">{data['name']}</li>
          </ol>
        </nav>
        <span class="label">Living · {data['name']}</span>
        <h1 id="ha-title">How Much House Can You Afford in {data['name']}?</h1>
        <p class="lead">{data['insight']} Use the calculator with {data['name']} tax and insurance defaults. Then open a city page for local median prices.</p>
        <div class="ha-calc-shell">
          <form id="ha-calc-form" class="ha-calc-form" aria-label="{data['name']} house affordability">
            <label class="ha-calc__field"><span>Annual income</span><input type="number" id="ha-income" min="20000" step="1000" value="{data['median_income']}" required></label>
            <label class="ha-calc__field"><span>Other monthly debt ($)</span><input type="number" id="ha-debt" min="0" step="25" value="300" required></label>
            <label class="ha-calc__field"><span>Down payment ($)</span><input type="number" id="ha-down" min="0" step="5000" value="{down_default}" required></label>
            <label class="ha-calc__field"><span>Interest rate (%)</span><input type="number" id="ha-rate" min="2" max="15" step="0.05" value="6.5" required></label>
            <input type="hidden" id="ha-location" value="{slug}">
            <div class="ha-calc__actions"><button type="submit" class="ha-calc__btn">Calculate</button></div>
          </form>
          <div id="ha-calc-results" class="ha-results" hidden aria-live="polite"></div>
        </div>
        <div class="ha-city-chips" aria-label="Cities in {data['name']}">
          {cities_html}
        </div>
      </div>
    </section>
    <section class="ha-section">
      <div class="container content-page">
        <h2>{data['name']} at a glance</h2>
        <div class="debt-stats-grid">
          <div class="debt-stat-block"><span class="debt-stat-value">{fmt(data['median_price'])}</span><span class="debt-stat-label">Median home price (approx.)</span></div>
          <div class="debt-stat-block"><span class="debt-stat-value">{fmt(data['median_income'])}</span><span class="debt-stat-label">Median household income</span></div>
          <div class="debt-stat-block"><span class="debt-stat-value">{data['tax_pct']}%</span><span class="debt-stat-label">Typical property tax rate</span></div>
        </div>
        <p>On a {fmt(data['median_price'])} home, tax near {data['tax_pct']}% is about <strong>{fmt(tax_month)}/month</strong>. Insurance near {data['ins_pct']}% of value is about <strong>{fmt(ins_month)}/month</strong>. HOA is about <strong>{fmt(data['hoa'])}/month</strong> where it applies.</p>
        <p>{salary_blurb}</p>
        <aside class="what-this-means" role="note">
          <p class="what-this-means__title">What this means for you</p>
          <p>Use the calculator with your real income and debts. If the stress label is <strong>Stretched</strong>, open a city page — inland or smaller metros may fit where the state median does not.</p>
        </aside>
        <p>Compare with <a href="/living/housing/how-much-house-can-i-afford/{data['compare_slug']}">{data['compare']}</a>: {data['compare_note']}</p>
        <p><a href="{data['tax_link']}">{data['name']} take-home pay</a> · <a href="{data['rent_link']}">Rent vs buy</a> · <a href="/living/housing/how-much-house-can-i-afford">US calculator</a></p>
      </div>
    </section>
    <section class="ha-section" aria-labelledby="ha-col-links-{slug}">
      <div class="container content-page">
        <h2 id="ha-col-links-{slug}">Living costs in {data['name']}</h2>
        <p class="ha-section__lead">Home price is one line. Rent, groceries, tax, and salary needs shape whether a payment feels comfortable.</p>
        <ul class="col-related__list">
          <li><a href="{data.get('col_link', '/living/housing/cost-of-living-by-city')}">Cost of living in {data['name']}</a></li>
          <li><a href="/living/housing/how-much-rent-can-i-afford">Rent affordability in {data['name']}</a></li>
          <li><a href="{data.get('salary_link', '/living/lifestyle/comfortable-salary-us')}">Comfortable salary in {data['name']}</a></li>
        </ul>
      </div>
    </section>
    <section class="ha-section">
      <div class="container content-page">
        <h2>Top cities in {data['name']}</h2>
        <p class="ha-section__lead">Median price and income vary a lot inside one state. Pick your city for local tax, insurance, and a prefilled calculator.</p>
        <div class="ha-compare-table-wrap">
          <table class="debt-data-table">
            <caption>Median price, income, and affordability pressure by city</caption>
            <thead><tr><th scope="col">City</th><th scope="col">Median price</th><th scope="col">Median income</th><th scope="col">Pressure</th></tr></thead>
            <tbody>
{city_rows}
            </tbody>
          </table>
        </div>
      </div>
    </section>
    <section class="ha-faq-section">
      <div class="container content-page">
        <h2>FAQ — {data['name']}</h2>
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
          <p class="eeat-trust__meta"><time datetime="2026-05-27">Last reviewed: May 27, 2026</time> · <a href="/methodology#affordability">Methodology</a></p>
        </header>
        <p>Medians are rounded planning figures from public listing and census sources. Tax and insurance use state defaults — your quote may differ. This is not a loan offer.</p>
      </aside>
    </div>
  </main>
  <footer class="site-footer">
    <div class="container footer-layout">
      <p class="footer-copy">© 2026 IncomeClarityLab</p>
    </div>
  </footer>
  <script src="/house-afford.js"></script>
  <script>
    HouseAfford.bindForm({{ stateSlug: '{slug}', defaultRegion: '{slug}', runOnLoad: true }});
  </script>
</body>
</html>
"""


def city_page(state_slug, state_data, city_slug, city):
    down = int(city["median_price"] * 0.2)
    income_needed = int(city["median_price"] / 3.2)
    local_note = city.get("local_note", city["pressure"])
    city_faqs = city.get("faqs", [])
    faq_html = "\n".join(
        f'          <article class="faq-item"><h3>{q}</h3><p>{a}</p></article>'
        for q, a in city_faqs
    )
    tax_month = int(city["median_price"] * city["tax_pct"] / 100 / 12)
    ins_month = int(city["median_price"] * city["ins_pct"] / 100 / 12)
    other_cities = [
        (cs, c["name"])
        for cs, c in state_data["cities"].items()
        if cs != city_slug
    ]
    sibling_links = " · ".join(
        f'<a href="/living/housing/how-much-house-can-i-afford/{state_slug}/{cs}">{name}</a>'
        for cs, name in other_cities
    )
    city_narrative = paragraphs_html(city.get("narrative", []))
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>How Much House Can I Afford in {city['name']}, {state_data['name']}? | Income Clarity</title>
  <meta name="description" content="Afford a home in {city['name']}? Median price {fmt(city['median_price'])}, income near {fmt(city['median_income'])}, local tax, insurance, and payment calculator.">
  <link rel="canonical" href="https://www.incomeclaritylab.com/living/housing/how-much-house-can-i-afford/{state_slug}/{city_slug}">
  <link rel="stylesheet" href="/styles.css">
  <link rel="stylesheet" href="/styles-living-system.css">
  <link rel="icon" type="image/svg+xml" href="/favicon.svg">
{URL_SCRIPT}
</head>
<body class="ha-page living-tool-page">
  <header class="site-header">
    <div class="container nav-wrap">
      <a class="logo" href="/index.html">Income Clarity</a>
      <nav class="nav-links" aria-label="Primary">
        <a href="/hourly-to-salary-after-tax">Income</a>
        <a href="/credit-card-payoff-calculator">Debt</a>
        <a href="/rent-vs-buy-calculator">Living</a>
      </nav>
    </div>
  </header>
  <main>
    <section class="ha-hero">
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
        <p class="lead">Median home near <strong>{fmt(city['median_price'])}</strong>. Typical household income near <strong>{fmt(city['median_income'])}</strong>. {city['pressure']} Calculator below uses {city['name']} tax and insurance defaults.</p>
        <div class="ha-calc-shell">
          <form id="ha-calc-form" class="ha-calc-form">
            <label class="ha-calc__field"><span>Annual income</span><input type="number" id="ha-income" value="{city['median_income']}" required></label>
            <label class="ha-calc__field"><span>Other monthly debt ($)</span><input type="number" id="ha-debt" value="300" required></label>
            <label class="ha-calc__field"><span>Down payment ($)</span><input type="number" id="ha-down" value="{down}" required></label>
            <label class="ha-calc__field"><span>Interest rate (%)</span><input type="number" id="ha-rate" value="6.5" step="0.05" required></label>
            <input type="hidden" id="ha-location" value="{state_slug}">
            <div class="ha-calc__actions"><button type="submit" class="ha-calc__btn">Calculate</button></div>
          </form>
          <div id="ha-calc-results" class="ha-results" hidden aria-live="polite"></div>
        </div>
      </div>
    </section>
    <section class="ha-section">
      <div class="container content-page">
        <h2>Local numbers for {city['name']}</h2>
        <div class="debt-stats-grid">
          <div class="debt-stat-block"><span class="debt-stat-value">{fmt(city['median_price'])}</span><span class="debt-stat-label">Median home price</span></div>
          <div class="debt-stat-block"><span class="debt-stat-value">{fmt(income_needed)}+</span><span class="debt-stat-label">Rough gross income for median home (3× rule)</span></div>
          <div class="debt-stat-block"><span class="debt-stat-value">{city['tax_pct']}%</span><span class="debt-stat-label">Property tax (effective)</span></div>
          <div class="debt-stat-block"><span class="debt-stat-value">{city['ins_pct']}%</span><span class="debt-stat-label">Insurance (of home value / yr)</span></div>
        </div>
        <p>On a median {fmt(city['median_price'])} home, tax near {city['tax_pct']}% is about <strong>{fmt(tax_month)}/month</strong>. Insurance near {city['ins_pct']}% is about <strong>{fmt(ins_month)}/month</strong>. HOA near <strong>{fmt(city['hoa'])}/month</strong> where it applies.</p>
        <p>{local_note}</p>
        <aside class="what-this-means" role="note">
          <p class="what-this-means__title">What this means for you</p>
          <p>Change income, debt, and down payment in the calculator. Compare with {sibling_links}.</p>
        </aside>
        <p><a href="/living/housing/how-much-house-can-i-afford/{state_slug}">All {state_data['name']} cities</a> · <a href="/living/housing/how-much-house-can-i-afford">US calculator</a></p>
      </div>
    </section>
    <section class="ha-section" aria-labelledby="ha-city-narrative-{city_slug}">
      <div class="container content-page">
        <h2 id="ha-city-narrative-{city_slug}">Affordability in {city['name']}: local context</h2>
{city_narrative}
        <aside class="what-this-means" role="note">
          <p class="what-this-means__title">What this means for you</p>
          <p>Your max price drops when debt is high or insurance is above our default. Run the calculator twice — once at list price and once $50k below — to see the stress change.</p>
        </aside>
      </div>
    </section>
    <section class="ha-faq-section">
      <div class="container content-page">
        <h2>FAQ — {city['name']}</h2>
        <div class="faq-stack">
{faq_html}
        </div>
      </div>
    </section>
  </main>
  <footer class="site-footer"><div class="container"><p class="footer-copy">© 2026 IncomeClarityLab</p></div></footer>
  <script src="/house-afford.js"></script>
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
    for slug, data in STATES.items():
        state_dir = BASE / slug
        state_dir.mkdir(parents=True, exist_ok=True)
        (state_dir / "index.html").write_text(state_page(slug, data), encoding="utf-8")
        for cs, city in data["cities"].items():
            city_dir = state_dir / cs
            city_dir.mkdir(parents=True, exist_ok=True)
            (city_dir / "index.html").write_text(city_page(slug, data, cs, city), encoding="utf-8")
        print(f"Wrote {slug} + {len(data['cities'])} cities")


if __name__ == "__main__":
    main()
