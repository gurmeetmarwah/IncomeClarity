"""Comfortable salary calculations and catalog — shared by generator and JS export."""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from generate_col_by_city_pages import (  # noqa: E402
    CORE_GROSS_SHARE,
    FAMILY_GROSS_SHARE,
    FAMILY_STACK_MULT,
    STANDALONE,
    STATES,
    core_monthly,
    minimum_comfort_salary,
    minimum_family_salary,
)

HUB_PATH = "/living/lifestyle/comfortable-salary-us"
BASE = "/living/lifestyle/comfortable-salary"

LIFESTYLE_TIERS = {
    "basic": {"label": "Basic Lifestyle", "mult": 0.72, "savings_rate": 0.06},
    "comfortable": {"label": "Comfortable Lifestyle", "mult": 1.0, "savings_rate": 0.12},
    "comfortable_plus": {"label": "Comfortable Plus", "mult": 1.32, "savings_rate": 0.15},
    "high_comfort": {"label": "Affluent Lifestyle", "mult": 1.75, "savings_rate": 0.18},
}

HOUSEHOLD = {
    "single": {"label": "Single", "core_mult": 1.0, "gross_share": CORE_GROSS_SHARE, "childcare": 0},
    "couple": {"label": "Couple", "core_mult": 1.38, "gross_share": 0.45, "childcare": 0},
    "family4": {"label": "Family of 4", "core_mult": FAMILY_STACK_MULT, "gross_share": FAMILY_GROSS_SHARE, "childcare": 1400},
}

HOUSING = {
    "rent": {"label": "Rent", "mult": 1.0},
    "own": {"label": "Own", "mult": 1.16},
}

# Effective take-home share of gross (federal + FICA + state)
STATE_TAKE_HOME = {
    "california": 0.68,
    "texas": 0.74,
    "florida": 0.74,
    "new-york": 0.67,
    "illinois": 0.71,
    "washington": 0.74,
    "colorado": 0.71,
    "georgia": 0.72,
    "arizona": 0.72,
}

STANDALONE_STATE = {
    "chicago": "illinois",
    "seattle": "washington",
    "denver": "colorado",
    "atlanta": "georgia",
    "phoenix": "arizona",
}

FEATURED_STATES = ["california", "texas", "florida", "new-york", "illinois"]
FEATURED_CITIES = [
    ("california", "los-angeles"),
    ("texas", "austin"),
    ("texas", "dallas"),
    ("washington", "seattle"),
    ("illinois", "chicago"),
    ("florida", "miami"),
]

COMPARE_PAIRS = [
    ("California vs Texas", "california", "texas"),
    ("Austin vs Denver", "texas/austin", "colorado/denver"),
    ("NYC vs Chicago", "new-york/new-york-city", "illinois/chicago"),
    ("Seattle vs Dallas", "washington/seattle", "texas/dallas"),
]

PROFILES = [
    ("single", "Single Professional", "solo renter with room to save"),
    ("couple", "Couple", "two earners sharing housing"),
    ("family4", "Family of 4", "two kids and full-time childcare"),
    ("single", "Remote Worker", "single adult with lower commute costs"),
]


def fmt(n: int) -> str:
    return f"${n:,}"


def round_salary(n: float) -> int:
    return int(round(n / 5000) * 5000)


def city_core(city: dict) -> int:
    return core_monthly(city["rent_1br"], city["groceries"], city["utilities"], city["transport"])


def gross_from_monthly(monthly: float, gross_share: float) -> int:
    return round_salary((monthly * 12) / max(gross_share, 0.35))


def compute_salary(
    city: dict,
    household: str = "single",
    housing: str = "rent",
    lifestyle: str = "comfortable",
    state_slug: str | None = None,
) -> dict:
    """Return annual gross targets and monthly breakdown for one scenario."""
    hh = HOUSEHOLD.get(household, HOUSEHOLD["single"])
    ho = HOUSING.get(housing, HOUSING["rent"])
    life = LIFESTYLE_TIERS.get(lifestyle, LIFESTYLE_TIERS["comfortable"])
    core = city_core(city)
    col = city.get("col_index", 100) / 100.0

    monthly_core = core * hh["core_mult"] * ho["mult"] * life["mult"]
    childcare = hh["childcare"] * col * (1.0 if household == "family4" else 0)
    if household == "family4" and lifestyle in ("comfortable_plus", "high_comfort"):
        childcare *= 1.15

    essentials = monthly_core + childcare
    savings = essentials * life["savings_rate"]
    monthly_total = essentials + savings

    annual = gross_from_monthly(monthly_total, hh["gross_share"])

    # Breakdown buckets (monthly)
    housing_amt = city["rent_1br"] * hh["core_mult"] * ho["mult"] * life["mult"] + city["utilities"] * 0.85
    food_amt = city["groceries"] * hh["core_mult"] * life["mult"] * 1.1
    transport_amt = city["transport"] * hh["core_mult"] * life["mult"]
    lifestyle_amt = max(280, 420 * col * life["mult"] * (0.6 + hh["core_mult"] * 0.15))

    buckets = {
        "housing": housing_amt,
        "transportation": transport_amt,
        "food": food_amt,
        "childcare": childcare,
        "savings": savings,
        "lifestyle": lifestyle_amt,
    }
    bucket_total = sum(buckets.values()) or 1
    breakdown = {k: {"amount": round(v), "pct": round(v / bucket_total * 100)} for k, v in buckets.items()}

    return {
        "annual": annual,
        "monthly": round(monthly_total),
        "breakdown": breakdown,
        "lifestyle": lifestyle,
        "household": household,
        "housing": housing,
    }


def lifestyle_range(city: dict, household: str = "single", housing: str = "rent", state_slug: str | None = None) -> dict:
    out = {}
    for key in LIFESTYLE_TIERS:
        out[key] = compute_salary(city, household, housing, key, state_slug)["annual"]
    return out


def affordability_score(city: dict, state_slug: str | None = None) -> int:
    """Higher = easier to feel comfortable on median wages."""
    core = city_core(city)
    target = minimum_comfort_salary(core)
    comfort = city.get("salary_comfort", target)
    col = city.get("col_index", 100)
    score = 78 - (col - 100) * 0.22 - max(0, comfort - target) / 2000
    return max(35, min(85, round(score)))


def salary_link(state_slug: str, city_slug: str | None = None) -> str:
    if city_slug:
        return f"{BASE}/{state_slug}/{city_slug}"
    return f"{BASE}/{state_slug}"


def build_catalog_entry(
    city_id: str,
    name: str,
    state_slug: str,
    state_name: str,
    city: dict,
) -> dict:
    core = city_core(city)
    comfort_computed = compute_salary(city, "single", "rent", "comfortable", state_slug)["annual"]
    family_computed = compute_salary(city, "family4", "rent", "comfortable", state_slug)["annual"]
    return {
        "id": city_id,
        "name": name,
        "state": state_slug,
        "stateName": state_name,
        "colIndex": city.get("col_index", 100),
        "rent": city["rent_1br"],
        "groceries": city["groceries"],
        "utilities": city["utilities"],
        "transport": city["transport"],
        "salaryComfort": comfort_computed,
        "familySalary": family_computed,
        "affordScore": affordability_score(city, state_slug),
        "takeHome": STATE_TAKE_HOME.get(state_slug, 0.72),
        "path": salary_link(state_slug, city_id.split("/")[-1] if "/" in city_id else None),
    }


def build_catalog() -> list[dict]:
    catalog: list[dict] = []
    seen: set[str] = set()

    for state_slug, st in STATES.items():
        for city_slug, city in st["cities"].items():
            cid = f"{state_slug}/{city_slug}"
            if cid in seen:
                continue
            seen.add(cid)
            catalog.append(
                build_catalog_entry(cid, city["name"], state_slug, st["name"], city)
            )
        # State-level pseudo entry for calculator default
        catalog.append(
            build_catalog_entry(
                state_slug,
                st["name"],
                state_slug,
                st["name"],
                {
                    "col_index": st["col_index"],
                    "rent_1br": st["rent_1br"],
                    "groceries": st["groceries"],
                    "utilities": st["utilities"],
                    "transport": st["transport"],
                    "salary_comfort": st["salary_comfort"],
                },
            )
        )

    for city_slug, city in STANDALONE.items():
        state_slug = STANDALONE_STATE[city_slug]
        cid = f"{state_slug}/{city_slug}"
        if cid in seen:
            continue
        seen.add(cid)
        catalog.append(
            build_catalog_entry(cid, city["name"], state_slug, city["state_name"], city)
        )

    # State-level entries for metros not in STATES (e.g. Illinois → Chicago only)
    state_ids = {c["id"] for c in catalog if "/" not in c["id"]}
    for state_slug in sorted(set(STANDALONE_STATE.values())):
        if state_slug in state_ids or state_slug in STATES:
            continue
        for city_slug, mapped in STANDALONE_STATE.items():
            if mapped != state_slug:
                continue
            city = STANDALONE[city_slug]
            catalog.append(
                build_catalog_entry(
                    state_slug,
                    city["state_name"],
                    state_slug,
                    city["state_name"],
                    {
                        "col_index": city["col_index"],
                        "rent_1br": city["rent_1br"],
                        "groceries": city["groceries"],
                        "utilities": city["utilities"],
                        "transport": city["transport"],
                        "salary_comfort": city["salary_comfort"],
                    },
                )
            )
            state_ids.add(state_slug)
            break

    return sorted(catalog, key=lambda c: (c["stateName"], c["name"]))


def catalog_json() -> str:
    return json.dumps(build_catalog(), separators=(",", ":"))


def validate_catalog() -> list[str]:
    warnings: list[str] = []
    for entry in build_catalog():
        if "/" not in entry["id"]:
            continue
        parts = entry["id"].split("/")
        state_slug, city_slug = parts[0], parts[1]
        st = STATES.get(state_slug)
        city = None
        if st:
            city = st["cities"].get(city_slug)
        if not city:
            city = STANDALONE.get(city_slug)
        if not city:
            continue
        computed = compute_salary(city, "single", "rent", "comfortable", state_slug)["annual"]
        stored = city.get("salary_comfort", computed)
        if abs(computed - stored) > stored * 0.25:
            warnings.append(
                f"{entry['name']}: model {fmt(computed)} vs stored comfort {fmt(stored)}"
            )
    return warnings
