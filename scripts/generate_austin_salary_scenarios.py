#!/usr/bin/env python3
"""Generate Austin salary scenario pages ($75k / $100k / $150k)."""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "living" / "lifestyle" / "comfortable-salary" / "texas" / "austin"

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
        <a href="/debt">Debt</a>
        <a href="/rent-vs-buy-calculator">Living</a>
        <a href="/1099-vs-w2-calculator">Freelance</a>
      </nav>
    </div>
  </header>"""

FOOTER = """  <footer class="site-footer">
    <div class="container footer-layout">
      <p class="footer-review" role="note"><time datetime="2026-06-01">Last reviewed: June 2026</time> · Reviewed by the <a href="/about">Income Clarity editorial team</a> · <a href="/editorial-policy">Editorial policy</a></p>
      <p class="footer-copy">© 2026 IncomeClarityLab</p>
    </div>
  </footer>"""

AUSTIN_HUB = "/living/lifestyle/comfortable-salary/texas/austin"

# Hand-maintained — do not overwrite when regenerating
HAND_MAINTAINED_SLUGS = {
    "is-75k-enough-to-live-in-austin",
    "is-100k-enough-to-live-in-austin",
    "is-150k-enough-to-live-in-austin",
}

SCENARIOS = [
    {
        "slug": "is-75k-enough-to-live-in-austin",
        "salary": 75000,
        "salary_label": "$75,000",
        "verdict_short": "Basic yes — comfortable is a stretch",
        "verdict_class": "cs-scenario-verdict--mixed",
        "hook": "At $75,000 gross in Austin, you take home about <strong>$4,625/month</strong>. That covers median rent and groceries — but leaves little room for savings, debt payoff, or a car payment on top of essentials.",
        "summary": "For a single renter with no kids and modest spending, $75k can work in Austin. It sits between our <strong>basic ($60k)</strong> and <strong>comfortable ($85k)</strong> tiers for singles. Couples and families need more.",
        "take_home": 4625,
        "essentials": 2715,
        "leftover": 1910,
        "rows": [
            ("Single renter", "Covers essentials; tight on savings and extras", "Basic tier · not quite comfortable"),
            ("Couple", "Two incomes help; one $75k earner is below couple basic ($75k combined need)", "Stretched unless partner also earns"),
            ("Family of 4", "Not enough for rent, food, childcare, and savings", "Well below $110k basic family target"),
        ],
        "example": """        <p>Meet Alex — single, rents a 1BR near $1,750/month, drives to a hybrid office job. On $75k gross:</p>
        <ul class="apr-plain-list">
          <li><strong>Take-home:</strong> ~$4,625/month (no Texas state income tax; federal + FICA still apply).</li>
          <li><strong>Rent ($1,750) + groceries ($400) + utilities ($195) + transport ($370):</strong> ~$2,715 in core costs.</li>
          <li><strong>Left for savings, dining, healthcare, and debt:</strong> ~$1,910/month.</li>
        </ul>
        <p>That leftover sounds okay until you budget $300 for car insurance and gas beyond the transport line, $150 for phone and streaming, and $400 toward an emergency fund. Suddenly there is no margin for a $400/month student loan or a weekend trip. Alex is <em>getting by</em>, not feeling comfortable.</p>""",
        "faq": [
            (
                "Is $75,000 a good salary in Austin?",
                "It is near the metro median for many tech and professional roles — enough for a single renter to cover bills if rent stays near $1,750. It is below our comfortable single target of $85,000 once you add savings and lifestyle spending.",
            ),
            (
                "Can I afford a $1,750 apartment on $75k?",
                "Yes — $1,750 is about 38% of gross monthly pay, slightly above the classic 30% rule but common in Austin. After tax, rent is a larger share. Run your exact take-home in our hourly-to-salary calculator.",
            ),
            (
                "Should I take a $75k offer if I have student loans?",
                "Model debt payments first. $400/month in loans on top of Austin essentials leaves very little buffer at $75k. Compare the offer to Dallas or Houston where rent runs lower.",
            ),
        ],
    },
    {
        "slug": "is-100k-enough-to-live-in-austin",
        "salary": 100000,
        "salary_label": "$100,000",
        "verdict_short": "Comfortable for singles — solid for couples",
        "verdict_class": "cs-scenario-verdict--yes",
        "hook": "$100,000 gross in Austin lands around <strong>$6,167/month</strong> take-home. That clears our <strong>$85,000 comfortable</strong> bar for a single renter — with room for savings and modest lifestyle spending.",
        "summary": "$100k is the salary many Austin job posts cite for mid-level roles. For a single adult renting, it supports a comfortable lifestyle with savings. Couples land near the comfortable tier ($110k). Families of four still need more.",
        "take_home": 6167,
        "essentials": 2715,
        "leftover": 3452,
        "rows": [
            ("Single renter", "Above comfortable tier with savings headroom", "Comfortable · room for hobbies and travel"),
            ("Couple", "One $100k earner or two moderate incomes works", "Near couple comfortable ($110k)"),
            ("Family of 4", "Covers basics; childcare pushes toward $145k comfortable", "Between family basic ($110k) and comfortable"),
        ],
        "example": """        <p>Jordan earns $100k at an Austin software company — partner earns $55k part-time. Combined they gross $155k, but let's focus on Jordan alone:</p>
        <ul class="apr-plain-list">
          <li><strong>Take-home on $100k:</strong> ~$6,167/month.</li>
          <li><strong>Core essentials ($2,715):</strong> rent, food, utilities, transport.</li>
          <li><strong>Comfortable-tier savings (~10–12%):</strong> ~$600–750/month.</li>
          <li><strong>Remaining for lifestyle, insurance, and debt:</strong> ~$2,700+/month.</li>
        </ul>
        <p>Jordan can afford a nicer apartment, pay $500/month toward a car note, and still fund a Roth IRA. That is what \"comfortable\" looks like in our model — not luxury, but no constant tradeoffs. A family of four on one $100k income would not feel the same; childcare alone can add $1,400+/month.</p>""",
        "faq": [
            (
                "Is $100k enough to live comfortably in Austin?",
                "For a single renter without heavy debt, yes — it exceeds our $85,000 comfortable target. Couples aiming for dining out, travel, and savings often want $110,000+ combined.",
            ),
            (
                "How does $100k in Austin compare to California?",
                "No state income tax helps — $100k in Austin often feels like $115k–$120k gross in California after tax on the same lifestyle. Rent is lower than Bay Area or LA, but rose fast since 2020.",
            ),
            (
                "Can a family of 4 live on $100k in Austin?",
                "It is tight. Our family basic tier starts near $110,000; comfortable is $145,000 with childcare. Dual earners or lower rent outside the core helps.",
            ),
        ],
    },
    {
        "slug": "is-150k-enough-to-live-in-austin",
        "salary": 150000,
        "salary_label": "$150,000",
        "verdict_short": "Comfortable for most households",
        "verdict_class": "cs-scenario-verdict--yes",
        "hook": "At <strong>$150,000</strong> gross, Austin take-home is roughly <strong>$9,250/month</strong>. Singles and couples live well above essentials. A family of four can hit the comfortable tier with room for savings and homeownership.",
        "summary": "$150k puts you in the top tier of Austin earners outside executive roles. It supports comfortable-plus lifestyles for singles and couples, and approaches comfortable for a family of four — especially if you buy a home and accept higher housing costs.",
        "take_home": 9250,
        "essentials": 2715,
        "leftover": 6535,
        "rows": [
            ("Single renter", "Well above comfortable; affluent tier within reach", "Comfortable+ ($115k) with large savings margin"),
            ("Couple", "Strong dual-life budget; homeownership feasible", "Above couple comfortable ($110k)"),
            ("Family of 4", "Near comfortable ($145k) with quality childcare", "Room for 529 savings and mortgage"),
        ],
        "example": """        <p>The Patels — two earners, two kids — gross $150k combined ($95k + $55k). Here is what $150k total looks like monthly:</p>
        <ul class="apr-plain-list">
          <li><strong>Take-home (~74%):</strong> ~$9,250/month.</li>
          <li><strong>3BR rent (~$2,400) or mortgage (~$2,800 with taxes):</strong> housing dominates.</li>
          <li><strong>Groceries, utilities, transport for four:</strong> ~$1,800+ combined.</li>
          <li><strong>Childcare (one child in preschool):</strong> ~$1,200/month.</li>
          <li><strong>Still room for:</strong> $800+ savings, $500 lifestyle, and debt payoff.</li>
        </ul>
        <p>At $150k, Austin feels manageable for a family — unlike coastal metros where the same gross buys less house. Compare owning in our <a href="/living/housing/how-much-house-can-i-afford/texas/austin">Austin home affordability guide</a> before you stretch into a $500k+ listing.</p>""",
        "faq": [
            (
                "Is $150k a good household income in Austin?",
                "Yes — it supports a comfortable family budget with savings, or a very strong single/couple lifestyle. It is above Austin's median household income and aligns with our family comfortable tier.",
            ),
            (
                "Can I buy a house in Austin on $150k?",
                "Often yes, with 10–20% down and moderate other debt. At $150k gross, the 28% housing rule allows roughly $3,500/month toward PITI — enough for many $400k–$500k homes at current rates. Run your numbers in our house affordability calculator.",
            ),
            (
                "Is $150k enough for Austin's \"comfortable plus\" lifestyle?",
                "Singles and couples can reach comfortable-plus ($115k–$150k tiers) with travel and dining budget. Families may need $175k+ for affluent-tier childcare and private school extras.",
            ),
        ],
    },
]


def other_scenarios(current_slug: str) -> str:
    cards = []
    for s in SCENARIOS:
        if s["slug"] == current_slug:
            continue
        title = f"Is {s['salary_label']} Enough to Live in Austin?"
        cards.append(
            f'          <a class="cs-card" href="{AUSTIN_HUB}/{s["slug"]}">'
            f"<h3>{title}</h3>"
            f'<p>{s["verdict_short"]}</p>'
            f'<span class="cs-card-cta">Read scenario →</span></a>'
        )
    return "\n".join(cards)


def faq_html(faqs: list[tuple[str, str]]) -> str:
    return "\n".join(
        f'          <article class="faq-item"><h3>{q}</h3><p>{a}</p></article>' for q, a in faqs
    )


def faq_schema(faqs: list[tuple[str, str]]) -> str:
    import json

    entities = [
        {
            "@type": "Question",
            "name": q,
            "acceptedAnswer": {"@type": "Answer", "text": a},
        }
        for q, a in faqs
    ]
    return json.dumps(
        {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": entities},
        indent=2,
    )


def render(s: dict) -> str:
    title = f"Is {s['salary_label']} Enough to Live in Austin? (2026) | Income Clarity"
    desc = (
        f"Wondering if {s['salary_label']} stretches in Austin? See take-home pay, rent math, "
        f"and household verdicts — {s['verdict_short'].lower()}."
    )
    canonical = f"{AUSTIN_HUB}/{s['slug']}"
    table_rows = "\n".join(
        f"              <tr><th scope=\"row\">{hh}</th><td>{detail}</td><td>{tier}</td></tr>"
        for hh, detail, tier in s["rows"]
    )
    other = other_scenarios(s["slug"])

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
  <script type="application/ld+json">
{faq_schema(s["faq"])}
  </script>
  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "BreadcrumbList",
    "itemListElement": [
      {{ "@type": "ListItem", "position": 1, "name": "Living", "item": "https://www.incomeclaritylab.com/rent-vs-buy-calculator" }},
      {{ "@type": "ListItem", "position": 2, "name": "Comfortable salary", "item": "https://www.incomeclaritylab.com/living/lifestyle/comfortable-salary-us" }},
      {{ "@type": "ListItem", "position": 3, "name": "Austin", "item": "https://www.incomeclaritylab.com{AUSTIN_HUB}" }},
      {{ "@type": "ListItem", "position": 4, "name": "{s['salary_label']} in Austin", "item": "https://www.incomeclaritylab.com{canonical}" }}
    ]
  }}
  </script>
</head>
<body class="cs-page living-tool-page cs-scenario-page">
{HEADER}
  <main>
    <section class="cs-hero">
      <div class="container container--wide">
        <p class="label">Austin salary scenario · {s["salary_label"]}</p>
        <nav class="take-home-return-nav" aria-label="Breadcrumb">
          <ol class="take-home-return-breadcrumbs">
            <li><a href="/rent-vs-buy-calculator">Living</a></li>
            <li><a href="/living/lifestyle/comfortable-salary-us">Comfortable salary</a></li>
            <li><a href="{AUSTIN_HUB}">Austin</a></li>
            <li aria-current="page">{s["salary_label"]}</li>
          </ol>
        </nav>
        <h1>Is {s["salary_label"]} enough to live in Austin?</h1>
        <p class="lead">{s["hook"]}</p>
        <p class="cs-scenario-verdict {s["verdict_class"]}"><strong>Short answer:</strong> {s["summary"]}</p>
        <div class="cs-stat-row">
          <div class="cs-stat"><strong>{s["salary_label"]}</strong><span>Gross salary</span></div>
          <div class="cs-stat"><strong>${s["take_home"]:,}</strong><span>Est. take-home / month</span></div>
          <div class="cs-stat"><strong>${s["essentials"]:,}</strong><span>Core essentials / month</span></div>
          <div class="cs-stat"><strong>${s["leftover"]:,}</strong><span>Left after essentials</span></div>
        </div>
        <p class="cs-hero-jump-wrap"><a class="cs-hero-jump" href="#cs-scenario-math">See the math ↓</a></p>
      </div>
    </section>

    <section class="cs-band" id="cs-scenario-math">
      <div class="container container--wide content-page">
        <header class="cs-band__head"><h2>Monthly budget at {s["salary_label"]} in Austin</h2><p>Median local costs for a single renter; your rent and habits may differ.</p></header>
{s["example"]}
        <div class="scenario-table-wrap">
          <table class="scenario-table">
            <caption>How {s["salary_label"]} stacks up by household type in Austin</caption>
            <thead><tr><th scope="col">Household</th><th scope="col">Reality check</th><th scope="col">Our tier</th></tr></thead>
            <tbody>
{table_rows}
            </tbody>
          </table>
        </div>
        <aside class="what-this-means" role="note">
          <p class="what-this-means__title">What this means for you</p>
          <p>These are planning numbers — not a guarantee. Debt, healthcare, and rent above $1,750 change the picture fast. Run your exact take-home in the <a href="/hourly-to-salary-after-tax#hourly-salary-form">hourly-to-salary after-tax calculator</a> and compare rent caps in our <a href="/living/housing/how-much-rent-can-i-afford">rent affordability guide</a>.</p>
        </aside>
      </div>
    </section>

    <section class="cs-band cs-band--alt">
      <div class="container container--wide content-page">
        <header class="cs-band__head"><h2>When {s["salary_label"]} feels tight in Austin</h2></header>
        <p>These costs eat margin faster than the median model assumes:</p>
        <ul class="apr-plain-list">
          <li><strong>Rent above $1,750</strong> — central neighborhoods and new builds often run $2,000–$2,400 for a 1BR.</li>
          <li><strong>Car + insurance</strong> — Austin is car-heavy; $400/month transport can become $600+ with a note and full coverage.</li>
          <li><strong>Student loans or card debt</strong> — $300–500/month in payments turns a \"fine on paper\" salary into paycheck-to-paycheck.</li>
          <li><strong>Healthcare</strong> — high-deductible plans can add $200–400/month in effective cost for families.</li>
        </ul>
        <p>If two or more apply, bump your target toward the next tier in our <a href="{AUSTIN_HUB}#cs-calc">Austin calculator</a> — or compare a lower-rent market like <a href="/living/lifestyle/comfortable-salary/texas/houston">Houston</a>.</p>
      </div>
    </section>

    <section class="cs-band">
      <div class="container container--wide">
        <header class="cs-band__head"><h2>Compare other Austin salary scenarios</h2></header>
        <div class="cs-compare-grid">
{other}
          <a class="cs-card" href="{AUSTIN_HUB}"><h3>Austin comfortable salary guide</h3><p>Full tiers, calculator, and local cost breakdown.</p><span class="cs-card-cta">Open guide →</span></a>
        </div>
      </div>
    </section>

    <section class="cs-band" id="cs-faq">
      <div class="container container--wide content-page">
        <header class="cs-band__head"><h2>FAQ</h2></header>
        <div class="faq-list">
{faq_html(s["faq"])}
        </div>
      </div>
    </section>

    <section class="cs-cta-band">
      <div class="container container--wide">
        <h2>Know your real number in Austin</h2>
        <p>Layer household size, housing choice, and lifestyle tier on our Austin calculator.</p>
        <div class="cs-cta-actions">
          <a href="{AUSTIN_HUB}#cs-calc">Austin salary calculator</a>
          <a href="/living/lifestyle/comfortable-salary/texas/dallas">Compare Dallas</a>
          <a href="/living/housing/cost-of-living-by-city/texas/austin">Cost of living detail</a>
        </div>
      </div>
    </section>
  </main>
{FOOTER}
</body>
</html>"""


def main() -> None:
    for s in SCENARIOS:
        if s["slug"] in HAND_MAINTAINED_SLUGS:
            print(f"  skip (hand-maintained) {s['slug']}")
            continue
        path = OUT / s["slug"] / "index.html"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(render(s), encoding="utf-8")
        print(f"  wrote {path.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
