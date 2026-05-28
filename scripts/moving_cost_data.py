"""City catalog and copy helpers for moving cost calculator pages."""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from generate_col_by_city_pages import STANDALONE, STATES  # noqa: E402

BASE = "/living/housing/moving-cost-calculator"

# Related tools for state/city moving pages
TAKE_HOME_BY_STATE = {
    "california": "/hourly-to-salary-after-tax/state/california/",
    "texas": "/hourly-to-salary-after-tax/state/texas/",
    "florida": "/hourly-to-salary-after-tax/state/florida/",
    "new-york": "/hourly-to-salary-after-tax/state/new-york/",
    "chicago": "/hourly-to-salary-after-tax/state/illinois/",
    "seattle": "/hourly-to-salary-after-tax/state/washington/",
}

HOUSE_AFFORD_BY_STATE = {
    "california": "/living/housing/how-much-house-can-i-afford/california",
    "texas": "/living/housing/how-much-house-can-i-afford/texas",
    "florida": "/living/housing/how-much-house-can-i-afford/florida",
    "new-york": "/living/housing/how-much-house-can-i-afford/new-york",
}

COMFORT_SALARY_BY_STATE = {
    "california": "/living/lifestyle-family/comfortable-salary-california",
    "texas": "/living/lifestyle-family/comfortable-salary-texas",
}

COL_BY_STATE = {
    "california": "/living/housing/cost-of-living-by-city/california",
    "texas": "/living/housing/cost-of-living-by-city/texas",
    "florida": "/living/housing/cost-of-living-by-city/florida",
    "new-york": "/living/housing/cost-of-living-by-city/new-york",
}

# Structured copy for moving-cost state pages (title + body insight cards)
MOVING_STATE_INSIGHTS: dict[str, dict] = {
    "california": {
        "intro": (
            "California typically costs more than the national median. Rent and insurance "
            "drive most of the gap, and wages on the coast are higher—but not always high "
            "enough to offset housing after tax."
        ),
        "insights": [
            {
                "title": "How to use this California moving guide",
                "body": (
                    "Treat this page as a map, not one fixed budget number. Start with the "
                    "calculator above using your current city, then compare Los Angeles, San Diego, "
                    "and San Francisco in the city cards below. Each city page shows rent, food, tax, "
                    "and salary targets so you can separate move-day cash (deposits, movers) from "
                    "month-two recurring bills."
                ),
            },
            {
                "title": "California taxes wages—Texas and Florida do not",
                "body": (
                    "Unlike Texas or Florida, California withholds state income tax on wages "
                    "(up to 13.3% on high earners, plus SDI). A $120,000 gross offer from a "
                    "no–state-tax market will not feel the same after move-in. Run your offer "
                    "through the {take_home_link} before you set a rent cap or sign a lease."
                ),
            },
            {
                "title": "Coast vs inland: where rent spreads widen",
                "body": (
                    "Coastal metros in this guide often run 20% to 40% above inland alternatives. "
                    "Many relocators target Sacramento, Riverside, or Central Valley markets to stay "
                    "in California’s job pool with lower housing pressure. Use the sorted city "
                    "comparison below instead of the state median alone when you negotiate salary "
                    "or choose a neighborhood."
                ),
            },
        ],
    },
    "texas": {
        "intro": (
            "Texas often looks affordable next to California or New York on rent, but "
            "property tax, insurance, and commute costs still shape the real monthly budget—"
            "especially if you plan to buy."
        ),
        "insights": [
            {
                "title": "How to use this Texas moving guide",
                "body": (
                    "Run the calculator with your origin city, then open Dallas, Houston, and "
                    "Austin below. Each page shows mover costs, deposits, and how monthly essentials "
                    "change after the move. State averages hide wide spreads between metros."
                ),
            },
            {
                "title": "No state income tax—but not a free lunch",
                "body": (
                    "Texas does not tax wages at the state level, which can boost take-home pay "
                    "versus California or New York. Sales tax, property tax, HOA fees, and "
                    "insurance still add up. Compare net pay and rent together, not gross salary "
                    "alone."
                ),
            },
            {
                "title": "Houston, Dallas, and Austin are not interchangeable",
                "body": (
                    "Houston often has the lowest rent among major Texas metros; Austin and Dallas "
                    "frequently run higher. A job offer in one city is not the same budget as "
                    "another once commute, utilities, and local rent are included—use the city "
                    "cards below before you commit."
                ),
            },
        ],
    },
    "florida": {
        "intro": (
            "Florida has no state income tax, but coastal rent, storm insurance, and HOA rules "
            "can still make monthly costs feel tight—especially in South Florida."
        ),
        "insights": [
            {
                "title": "How to use this Florida moving guide",
                "body": (
                    "Use the top calculator for your move quote, then compare Miami, Tampa, and "
                    "Orlando below. Miami is not Orlando on monthly housing: open the city that "
                    "matches your job location before you rely on the state average."
                ),
            },
            {
                "title": "Insurance and coast vs inland",
                "body": (
                    "Wind and flood exposure can raise renters and owners insurance on the coast. "
                    "Inland metros are often closer to the US norm on rent. Budget insurance "
                    "changes when you compare offers, not just list rent."
                ),
            },
            {
                "title": "Who Florida fits—and who it strains",
                "body": (
                    "Remote workers and retirees often target Florida for tax and weather, but "
                    "entry-level wages can still feel tight against South Florida rent. Pair "
                    "this page with a take-home estimate and rent cap for your actual offer."
                ),
            },
        ],
    },
    "new-york": {
        "intro": (
            "New York is really two markets: downstate (NYC metro) and upstate. NYC rent and "
            "tax load drive the state average up; other regions can look like a different state "
            "on monthly cost."
        ),
        "insights": [
            {
                "title": "How to use this New York moving guide",
                "body": (
                    "If you are moving to New York City, use the NYC city page and calculator "
                    "destination below—not the state median alone. Upstate moves need different "
                    "rent and tax assumptions; this hub focuses on the downstate metro in our data."
                ),
            },
            {
                "title": "State plus city income tax downstate",
                "body": (
                    "Many downstate workers pay New York State income tax and New York City tax "
                    "on top of federal withholding. Take-home pay drops before you shop for an "
                    "apartment. Run a {take_home_link} on your offer letter first."
                ),
            },
            {
                "title": "Why the state average can mislead",
                "body": (
                    "A single state-wide rent figure blends NYC pressure with lower-cost upstate "
                    "markets. Broker fees, last-month rent, and tight inventory in NYC can also "
                    "raise move-in cash beyond what a typical US move requires."
                ),
            },
        ],
    },
}


def state_moving_insights(state_slug: str, st: dict) -> dict:
    """Return intro + insight cards for a state moving page."""
    if state_slug in MOVING_STATE_INSIGHTS:
        return MOVING_STATE_INSIGHTS[state_slug]
    narrative = st.get("narrative", [])
    intro = narrative[0] if narrative else (
        f"Relocating to {st['name']} changes both move-day cash and monthly bills."
    )
    insights = [
        {"title": f"Planning a move to {st['name']}", "body": p}
        for p in (narrative[1:] if len(narrative) > 1 else [
            "Compare cities below before you use state-wide averages."
        ])
    ]
    return {"intro": intro, "insights": insights}

# Rough state/region tags for distance estimates in JS
STATE_REGION = {
    "california": "west",
    "texas": "south",
    "florida": "south",
    "new-york": "northeast",
    "illinois": "midwest",
    "washington": "west",
    "colorado": "west",
    "georgia": "south",
    "arizona": "west",
}

STANDALONE_REGION = {
    "chicago": "midwest",
    "seattle": "west",
    "denver": "west",
    "atlanta": "south",
    "phoenix": "west",
}


def fmt(n: int) -> str:
    return f"${n:,}"


def monthly_total(c: dict) -> int:
    return (
        c.get("rent_1br", 1500)
        + c.get("groceries", 400)
        + c.get("utilities", 200)
        + c.get("transport", 350)
        + c.get("taxes_month", 180)
    )


def build_catalog() -> list[dict]:
    out: list[dict] = []
    for state_slug, st in STATES.items():
        region = STATE_REGION.get(state_slug, "us")
        for city_slug, c in st["cities"].items():
            cid = f"{state_slug}/{city_slug}"
            out.append(
                {
                    "id": cid,
                    "name": c["name"],
                    "state": state_slug,
                    "stateName": st["name"],
                    "region": region,
                    "rent": c["rent_1br"],
                    "groceries": c["groceries"],
                    "utilities": c["utilities"],
                    "transport": c["transport"],
                    "taxes": c.get("taxes_month", st.get("taxes_month", 180)),
                    "colIndex": c.get("col_index", st["col_index"]),
                    "salaryComfort": c.get("salary_comfort", st["salary_comfort"]),
                    "path": f"{BASE}/{state_slug}/{city_slug}",
                    "colPath": f"/living/housing/cost-of-living-by-city/{state_slug}/{city_slug}",
                }
            )
    for slug, c in STANDALONE.items():
        region = STANDALONE_REGION.get(slug, "us")
        out.append(
            {
                "id": slug,
                "name": c["name"],
                "state": slug,
                "stateName": c.get("state_name", c["name"]),
                "region": region,
                "rent": c["rent_1br"],
                "groceries": c["groceries"],
                "utilities": c["utilities"],
                "transport": c["transport"],
                "taxes": c.get("taxes_month", 180),
                "colIndex": c["col_index"],
                "salaryComfort": c["salary_comfort"],
                "path": f"{BASE}/{slug}",
                "colPath": f"/living/housing/cost-of-living-by-city/{slug}",
            }
        )
    return sorted(out, key=lambda x: (x["stateName"], x["name"]))


def catalog_json() -> str:
    return json.dumps(build_catalog(), separators=(",", ":"))


def state_moving_tips(state_name: str, state_slug: str) -> list[tuple[str, list[str]]]:
    """Relocation recommendation cards for state pages."""
    common = [
        (
            "Cash before keys",
            [
                f"Save at least three months of {state_name} rent plus your full move estimate.",
                "Keep $2,000 to $3,000 extra for overlap rent, utility deposits, and first grocery runs.",
                "Do not count credit cards as move funding unless you have a payoff plan.",
            ],
        ),
        (
            "Compare cities, not averages",
            [
                f"State-wide rent hides wide spreads between metros in {state_name}.",
                "Run the calculator for each city you are considering before you sign a lease.",
                "A higher salary offer can still lose if rent and tax rise more than pay.",
            ],
        ),
        (
            "Book movers early",
            [
                "Peak summer and month-end dates cost more and sell out faster.",
                "Get two mover quotes and one truck rental quote in writing.",
                "Confirm elevator, parking permit, and loading rules with both buildings.",
            ],
        ),
    ]
    extra: dict[str, list[tuple[str, list[str]]]] = {
        "california": [
            (
                "California-specific",
                [
                    "Budget state income tax when comparing offers from no-tax states.",
                    "Coastal insurance and rent often beat inland savings on paper — run both.",
                    "Inland metros can cut rent 20% to 40% while keeping some CA job markets.",
                ],
            ),
        ],
        "texas": [
            (
                "Texas-specific",
                [
                    "No state income tax helps take-home pay; property tax matters if you buy.",
                    "Austin and Dallas often run above Houston on rent — compare city pages.",
                    "Summer AC and storm prep can add to first-month utility bills.",
                ],
            ),
        ],
        "florida": [
            (
                "Florida-specific",
                [
                    "Coastal wind insurance can surprise new renters and owners.",
                    "Miami costs far more than Tampa or Orlando on monthly housing.",
                    "HOA and flood-zone rules vary block by block — read leases closely.",
                ],
            ),
        ],
        "new-york": [
            (
                "New York-specific",
                [
                    "Downstate income tax plus NYC city tax can shrink take-home quickly.",
                    "Broker fees and last-month rent are common in tight NYC markets.",
                    "Upstate cities are a different budget than NYC — do not blend them.",
                ],
            ),
        ],
    }
    return common + extra.get(state_slug, [])


def city_moving_tips(city_name: str, state_name: str) -> list[tuple[str, list[str]]]:
    return [
        (
            "Before you sign in " + city_name,
            [
                "Ask for total move-in cash: deposit, first month, fees, and broker charges.",
                "Confirm commute cost and parking before you accept a lower rent farther out.",
                f"Compare {city_name} to other {state_name} cities on this site, not national averages.",
            ],
        ),
        (
            "Move week",
            [
                "Photograph unit condition on day one for your deposit record.",
                "Set up utilities and internet two weeks ahead to avoid rush fees.",
                "Keep essentials in one bag — not on the moving truck.",
            ],
        ),
        (
            "First month budget",
            [
                "Track actual spend against your calculator estimate after 30 days.",
                "Delay furniture and decor until cash flow stabilizes.",
                "Requote renter and auto insurance for your new ZIP code.",
            ],
        ),
    ]


def state_moving_faqs(state_name: str) -> list[tuple[str, str]]:
    return [
        (
            f"How much does it cost to move to {state_name}?",
            f"Most households spend $3,500 to $8,500 on movers and travel, plus $6,000 to $12,000 in upfront cash for deposits and setup. {state_name} rent and tax rules change your monthly budget after move-in day.\n\nDistance, home size, and peak season matter. Long interstate moves with professional movers land at the high end. Local DIY moves can sit lower if you already own boxes and have help.",
        ),
        (
            f"How much should I save before moving to {state_name}?",
            f"A practical target is three months of {state_name} rent at your destination, your full moving estimate, and a $2,000 to $3,000 safety buffer. If you carry debt, add one extra month of minimum payments so relocation does not push balances onto cards.\n\nIf your job starts after move-in or income is variable, add another month of essentials. That buffer protects you from lease overlap and delayed first paychecks.",
        ),
        (
            f"Are movers worth it for a {state_name} move?",
            "Movers cost more up front but save time and reduce injury risk on long trips. They are often worth it when you have heavy furniture, stairs, or limited help.\n\nDIY or truck rental can work for shorter moves and smaller homes, especially if you can pack over several weekends. Compare at least two quotes before you decide.",
        ),
        (
            f"What hidden costs surprise people moving to {state_name}?",
            "Lease overlap, utility deposits, parking permits, storage, and furnishing basics are the usual misses. Insurance premiums can also change by ZIP code.\n\nMonthly lifestyle drift matters too: groceries, commute, childcare, and local tax differences can reduce savings even when rent looks similar on paper.",
        ),
        (
            f"How long does it take to financially recover after moving to {state_name}?",
            "If your monthly costs drop after the move, divide one-time moving cash by monthly savings to estimate breakeven months. If costs rise, focus on whether salary growth or career upside justifies the tighter budget.\n\nMany households need 6 to 18 months to feel stable again after a large relocation, depending on how much cash they kept in reserve.",
        ),
        (
            f"Should I move to {state_name} without a job lined up?",
            "Only if you have enough cash to cover rent, food, insurance, and debt payments for several months without income. Moving without work increases pressure to accept the first lease or job offer.\n\nIf you are exploring, run this calculator for multiple cities and build a written budget before you give notice at your current home.",
        ),
    ]


def city_moving_faqs(city_name: str, state_name: str) -> list[tuple[str, str]]:
    return [
        (
            f"What does it cost to move to {city_name}?",
            f"Moving to {city_name} usually needs both a move budget and a higher monthly plan. Use this page to compare rent, tax, and setup costs against your current city.\n\nEnter your origin city in the calculator above to see mover fees, immediate cash needs, and monthly cost difference side by side.",
        ),
        (
            f"How much rent deposit is typical in {city_name}?",
            "Many renters budget first month rent plus a security deposit equal to one month. In competitive markets, landlords may also ask for the last month or a broker fee.\n\nPlan immediate cash as deposit plus first month plus moving costs, not rent alone.",
        ),
        (
            f"Is {city_name} cheaper than other {state_name} cities?",
            f"Compare city pages inside {state_name}. Job-center and coastal metros often cost more than inland options even within the same state.\n\nSalary offers should be compared after tax and rent, not on gross pay alone.",
        ),
        (
            f"How much emergency cash should I keep after moving to {city_name}?",
            "A strong baseline is one month of local rent in cash after you pay move-in costs. If your income is commission-based or you are between jobs, target two to three months.\n\nKeep this separate from your moving budget so small surprises do not go on high-interest debt.",
        ),
        (
            f"What is the biggest budget mistake when relocating to {city_name}?",
            "Using national averages instead of neighborhood-level rent and commute costs. The second mistake is skipping tax and insurance changes when comparing job offers.\n\nRun your numbers twice: once for move month cash, once for month-two recurring bills.",
        ),
        (
            f"Can I afford {city_name} on my current salary?",
            f"Use the affordability section in the US moving calculator hub with your salary, savings, and debt entered. Then set {city_name} as the destination to see whether move costs fit your cash on hand.\n\nIf monthly leftover is negative, either raise income, lower rent target, or delay the move until savings catch up.",
        ),
    ]
