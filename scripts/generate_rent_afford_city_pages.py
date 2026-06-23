#!/usr/bin/env python3
"""Generate city rent affordability pages."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from rent_afford_city_content import EXTENDED
from rent_afford_city_longform import LONGFORM

ROOT = Path(__file__).resolve().parent.parent
BASE = ROOT / "living" / "housing" / "how-much-rent-can-i-afford"
MIN_MAIN_WORDS = 1300

SALARY_TIERS = [50000, 75000, 100000, 150000, 200000]

URL_SCRIPT = """  <script>
    (function () {
      const path = window.location.pathname;
      let cleanPath = path;
      if (path.endsWith("/index.html")) cleanPath = path.slice(0, -10);
      else if (path.endsWith(".html")) cleanPath = path.slice(0, -5);
      if (cleanPath !== path) window.history.replaceState({}, "", cleanPath + window.location.search + window.location.hash);
    })();
  </script>"""


def fmt(n: int | float) -> str:
    return f"${int(round(n)):,}"


def affordable_rent(gross: int) -> int:
    return round(gross * 0.30 / 12)


def city_path(state_slug: str, city_slug: str) -> str:
    return f"/living/housing/how-much-rent-can-i-afford/{state_slug}/{city_slug}"


def budget_breakdown(data: dict, income: int) -> dict:
    net = round(income / 12 * data["tax_takehome"])
    rent = round(min(affordable_rent(income) * 0.96, data["rent_1br"] * 1.03))
    utilities = data["utilities"]
    transport = data["transport"]
    food = round(net * 0.11)
    savings = round(net * data["default_save"] / 100)
    other = max(0, net - rent - utilities - transport - food - savings)
    return {
        "net": net,
        "rent": rent,
        "utilities": utilities,
        "transport": transport,
        "food": food,
        "savings": savings,
        "other": other,
    }


def count_main_words(html: str) -> int:
    m = re.search(r"<main>(.*)</main>", html, re.S)
    main = m.group(1) if m else html
    text = re.sub(r"<[^>]+>", " ", main)
    return len(text.split())


def render_paragraphs(paragraphs: list[str]) -> str:
    return render_prose(paragraphs)


def section_head(title: str, intro: str) -> str:
    return f"""        <header class="ra-section-head">
          <h2>{title}</h2>
          <p class="ra-section-head__intro">{intro}</p>
        </header>"""


def render_prose(paragraphs: list[str], extra_class: str = "") -> str:
    if not paragraphs:
        return ""
    cls = "ra-prose" + (f" {extra_class}" if extra_class else "")
    inner = "\n".join(f"          <p>{p}</p>" for p in paragraphs)
    return f"        <div class=\"{cls}\">\n{inner}\n        </div>"


def render_insights(paragraphs: list[str]) -> str:
    if not paragraphs:
        return ""
    items = "\n".join(f"          <li class=\"ra-insight-item\"><p>{p}</p></li>" for p in paragraphs)
    return f"        <ul class=\"ra-insight-list\">\n{items}\n        </ul>"


def render_reading_block(paragraphs: list[str]) -> str:
    if not paragraphs:
        return ""
    inner = "\n".join(f"          <p>{p}</p>" for p in paragraphs)
    return f"        <div class=\"ra-reading-block\">\n{inner}\n        </div>"


def render_callout(text: str, title: str = "Key takeaway") -> str:
    if not text:
        return ""
    return f"""        <aside class="ra-callout" role="note">
          <p class="ra-callout__title">{title}</p>
          <p>{text}</p>
        </aside>"""


def render_long_tail(sections: list[dict]) -> str:
    blocks = []
    for i, s in enumerate(sections):
        alt = " ra-band--alt" if i % 2 else ""
        paras = render_prose(s["paragraphs"])
        blocks.append(
            f"""    <section class="ra-band ra-article-band{alt}" id="{s['id']}">
      <div class="container container--wide">
        <article class="ra-article-card">
          <h2 class="ra-article-card__title">{s['title']}</h2>
{paras}
        </article>
      </div>
    </section>"""
        )
    return "\n".join(blocks)


def city_page(state_slug: str, city_slug: str, data: dict) -> str:
    name = data.get("name", city_slug.replace("-", " ").title())
    state_name = data.get("state_name", state_slug.replace("-", " ").title())
    ext = EXTENDED[(state_slug, city_slug)]
    lf = LONGFORM[(state_slug, city_slug)]
    path = city_path(state_slug, city_slug)
    canonical = f"https://www.incomeclaritylab.com{path}"

    income = ext["default_income"]
    bb = budget_breakdown(ext, income)
    comfort_low = round(affordable_rent(income) * 0.88)
    comfort_high = round(affordable_rent(income) * 1.03)
    stretch = round(affordable_rent(income) * 1.15)
    median = ext["median_rent"]
    if comfort_high >= median:
        verdict = "Comfortable"
        verdict_class = "ra-verdict--good"
    elif stretch >= median:
        verdict = "Stretch"
        verdict_class = "ra-verdict--mid"
    else:
        verdict = "Tight"
        verdict_class = "ra-verdict--risk"

    tier_rows = "\n".join(
        f'              <tr><td>{fmt(s)}</td><td>{fmt(affordable_rent(s))}</td></tr>'
        for s in SALARY_TIERS
    )

    nh_rows = "\n".join(
        f"""              <tr>
                <th scope="row">{n[0]}</th>
                <td>{fmt(n[1])}</td>
                <td>{fmt(n[2])}+</td>
              </tr>"""
        for n in ext["neighborhoods"]
    )

    expansions_src = list(ext["income_expansions"]) + list(lf.get("extra_expansions", []))
    expansions = "\n".join(
        f"""          <details class="ra-expand">
            <summary class="ra-expand__summary">{e[2]}</summary>
            <div class="ra-expand__body">
              <p>{e[3]}</p>"""
        + (f"\n              <p>{e[4]}</p>" if len(e) > 4 else "")
        + "\n            </div>\n          </details>"
        for e in expansions_src
    )

    tier_cards = "\n".join(
        f"""          <article class="ra-tier-card">
            <h3>{t[0]}</h3>
            <p class="ra-tier-card__income">{fmt(t[1])}+</p>
            <p>{t[2]}</p>
          </article>"""
        for t in ext["tiers"]
    )

    related = "\n".join(
        f'          <a class="ra-related-card" href="{href}"><span>{label}</span><strong>Open guide →</strong></a>'
        for label, href in ext["related"]
    )

    faqs_src = list(ext["faqs"]) + list(lf.get("extra_faqs", []))
    faqs = "\n".join(
        f"""          <article class="faq-item">
            <h3>{q}</h3>
            <p>{a}</p>
          </article>"""
        for q, a in faqs_src
    )

    faq_schema = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}}
            for q, a in faqs_src
        ],
    }

    narrative = render_reading_block(ext["narrative"] + lf.get("snapshot_extra", []))
    rules_html = render_insights(lf.get("rules", []))
    hidden_html = render_insights(lf.get("hidden_costs", []))
    budget_extra_paras = lf.get("budget_extra", [])
    budget_reading_lines = [
        "        <div class=\"ra-reading-block\">",
        "          <p>If rent plus utilities push past one-third of take-home, the other lines get squeezed fast — especially when debt payments are not shown in this simplified example.</p>",
    ]
    budget_reading_lines.extend(f"          <p>{p}</p>" for p in budget_extra_paras)
    budget_reading_lines.append("        </div>")
    budget_reading = "\n".join(budget_reading_lines)

    tiers_intro = f'Planning bands tied to gross income — pair with our <a class="ra-text-link" href="{ext["salary_link"]}">comfortable salary guide</a> for household-specific targets.'
    long_tail_html = render_long_tail(lf.get("long_tail", []))

    glance_row = f"""        <div class="ra-glance-row" aria-label="{name} rent at a glance">
          <div class="ra-glance-pill"><span class="ra-glance-pill__n">{fmt(ext['median_rent'])}</span><span class="ra-glance-pill__l">Median rent</span></div>
          <div class="ra-glance-pill"><span class="ra-glance-pill__n">{ext['col_index']}</span><span class="ra-glance-pill__l">Cost of living index</span></div>
          <div class="ra-glance-pill"><span class="ra-glance-pill__n">{ext['afford_score']}/100</span><span class="ra-glance-pill__l">Affordability score</span></div>
          <div class="ra-glance-pill"><span class="ra-glance-pill__n">30%</span><span class="ra-glance-pill__l">Rent-to-income rule</span></div>
        </div>"""

    budget_total = bb["net"] or 1
    budget_rows = [
        ("Rent", bb["rent"], "rent"),
        ("Utilities", bb["utilities"], "util"),
        ("Transportation", bb["transport"], "trans"),
        ("Food", bb["food"], "food"),
        ("Savings", bb["savings"], "save"),
        ("Other", bb["other"], "other"),
    ]
    budget_list = "\n".join(
        f"""            <li class="ra-budget-row ra-budget-row--{key}" style="--pct:{round(100 * amt / budget_total)}%">
              <div class="ra-budget-row__meta"><span>{label}</span><strong>{fmt(amt)}</strong></div>
              <span class="ra-budget-row__track" aria-hidden="true"><span class="ra-budget-row__fill"></span></span>
            </li>"""
        for label, amt, key in budget_rows
    )

    city_data = {
        "medianRent": ext["median_rent"],
        "defaultIncome": income,
        "defaultDebt": ext["default_debt"],
        "defaultFamily": ext["default_family"],
        "defaultSave": ext["default_save"],
        "taxTakehome": ext["tax_takehome"],
        "transport": ext["transport"],
    }

    toc_items = [
        ("ra-calculator", "Rent calculator"),
        ("ra-rent-snapshot", f"{name} rent snapshot"),
        ("ra-rent-rules", "Gross vs net rent rules"),
        ("ra-rent-by-income", "Rent by income"),
        ("ra-hidden-costs", "Hidden rental costs"),
        ("ra-neighborhoods", "Neighborhood comparison"),
        ("ra-budget-breakdown", "Budget breakdown"),
        ("ra-affordability-tiers", "Affordability tiers"),
    ]
    for s in lf.get("long_tail", []):
        toc_items.append((s["id"], s["title"]))
    toc_items.extend([
        ("ra-related-income", "Related income pages"),
        ("ra-faq", "FAQ"),
    ])
    toc_html = "\n".join(
        f'          <li><a href="#{id_}" class="ha-city-toc__link" data-ha-toc-link>{label}</a></li>'
        for id_, label in toc_items
    )

    compare_parts = ext["compare_slug"].split("/", 1)
    if len(compare_parts) == 2 and (compare_parts[0], compare_parts[1]) in CITIES:
        compare_href = city_path(compare_parts[0], compare_parts[1])
    else:
        compare_href = ext.get("compare_col_link", ext["col_link"])

    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>How Much Rent Can I Afford in {name}, {ext['state_abbr']}? (2026 Guide) | Income Clarity</title>
  <meta name="description" content="How much rent can you afford in {name}? Median rent {fmt(median)}/mo, salary tiers, neighborhood comparison, budget breakdown, and free calculator.">
  <link rel="canonical" href="{canonical}">
  <link rel="stylesheet" href="/styles.css">
  <link rel="stylesheet" href="/styles-living-system.css">
  <link rel="stylesheet" href="/styles-rent.css">
  <link rel="icon" type="image/png" href="/images/logo.png">
  <link rel="apple-touch-icon" href="/images/logo.png">
  <script type="application/json" id="ra-city-data">{json.dumps(city_data)}</script>
  <script type="application/ld+json">{json.dumps(faq_schema, ensure_ascii=False)}</script>
{URL_SCRIPT}
</head>
<body class="ra-page ra-city-page living-tool-page">
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
    <section class="ra-hero ra-city-hero" id="ra-calculator">
      <div class="container container--wide">
        <nav class="take-home-return-nav" aria-label="Breadcrumb">
          <ol class="take-home-return-breadcrumbs">
            <li><a href="/living/housing/how-much-rent-can-i-afford">Rent affordability</a></li>
            <li aria-current="page">{name}</li>
          </ol>
        </nav>
        <span class="label">{name} · {ext['state_abbr']}</span>
        <h1>How Much Rent Can I Afford in {name}?</h1>
        <p class="lead">Find the maximum monthly rent you can comfortably afford based on your income, debts, and {name} housing costs. Median rent is about <strong>{fmt(median)}/month</strong> — use the calculator for your personal comfortable, stretch, and verdict.</p>
        <div class="ha-hero-grid ra-city-hero-grid">
          <div class="ra-city-calc-col">
            <div class="ra-calc-shell ra-city-calc-shell">
              <form id="ra-city-form" class="ra-calc-form ra-city-form" aria-label="{name} rent affordability calculator">
                <label class="ra-field"><span>Annual income ($)</span><input type="number" id="ra-city-income" min="20000" step="1000" value="{income}" required></label>
                <label class="ra-field"><span>Monthly debt payments ($)</span><input type="number" id="ra-city-debt" min="0" step="25" value="{ext['default_debt']}"></label>
                <label class="ra-field"><span>Household size</span><input type="number" id="ra-city-family" min="1" max="8" step="1" value="{ext['default_family']}"></label>
                <label class="ra-field"><span>Savings goal (% of take-home)</span><input type="number" id="ra-city-save" min="0" max="40" step="1" value="{ext['default_save']}"></label>
                <div class="ra-field ra-field--full">
                  <button type="submit" class="ra-btn" id="ra-city-calc-btn">Calculate Rent Affordability</button>
                </div>
              </form>
            </div>
            <div class="ra-city-instant" id="ra-city-instant" aria-live="polite">
              <h2 class="ra-city-instant__title">Your {name} rent estimate</h2>
              <dl class="ra-city-instant__grid">
                <div><dt>Income</dt><dd id="ra-ci-income">{fmt(income)}</dd></div>
                <div><dt>Recommended rent</dt><dd id="ra-ci-comfort">{fmt(comfort_low)} – {fmt(comfort_high)}/month</dd></div>
                <div><dt>Maximum stretch budget</dt><dd id="ra-ci-stretch">{fmt(stretch)}/month</dd></div>
                <div><dt>{name} median rent</dt><dd id="ra-ci-median">{fmt(median)}/month</dd></div>
                <div class="ra-city-instant__verdict"><dt>Verdict</dt><dd id="ra-ci-verdict" class="ra-verdict {verdict_class}">{verdict}</dd></div>
              </dl>
              <p class="ra-city-instant__note" id="ra-ci-summary">Based on {fmt(income)} gross and typical {name} take-home. Adjust debt and savings to see your range update instantly.</p>
            </div>
          </div>
          <aside class="ha-city-toc ha-city-toc--hero" id="ra-toc">
            <div class="ha-city-toc__card">
              <button type="button" class="ha-city-toc__toggle" aria-expanded="true" aria-controls="ra-toc-panel">
                <span class="ha-city-toc__toggle-text">
                  <span class="ha-city-toc__title">On this page</span>
                  <span class="ha-city-toc__kicker">Snapshot, neighborhoods, tiers &amp; more</span>
                </span>
                <svg class="ha-city-toc__toggle-icon" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true"><path fill-rule="evenodd" d="M5.23 7.21a.75.75 0 011.06.02L10 10.94l3.71-3.71a.75.75 0 111.06 1.06l-4.24 4.25a.75.75 0 01-1.06 0L5.21 8.29a.75.75 0 01.02-1.08z" clip-rule="evenodd"/></svg>
              </button>
              <nav class="ha-city-toc__panel" id="ra-toc-panel" aria-label="On this page">
                <ul class="ha-city-toc__list">
{toc_html}
                </ul>
              </nav>
            </div>
          </aside>
        </div>
      </div>
    </section>

    <section class="ra-band ra-band--alt" id="ra-rent-snapshot">
      <div class="container container--wide">
{section_head(f"{name} rent snapshot", f"Local benchmarks for {name}. Compare your calculator result to these medians before you tour apartments.")}
{glance_row}
        <div class="ra-table-card">
          <div class="ra-snapshot-table-wrap">
            <table class="debt-data-table ra-city-table ra-snapshot-table">
              <caption>{name} rent and cost benchmarks</caption>
              <tbody>
                <tr><th scope="row">Median rent</th><td>{fmt(ext['median_rent'])}</td></tr>
                <tr><th scope="row">Studio</th><td>{fmt(ext['rent_studio'])}</td></tr>
                <tr><th scope="row">1 bedroom</th><td>{fmt(ext['rent_1br'])}</td></tr>
                <tr><th scope="row">2 bedroom</th><td>{fmt(ext['rent_2br'])}</td></tr>
                <tr><th scope="row">Rent-to-income benchmark</th><td>30%</td></tr>
                <tr><th scope="row">Cost of living index</th><td>{ext['col_index']} <span class="ra-table-muted">(US avg = 100)</span></td></tr>
                <tr><th scope="row">Affordability score</th><td>{ext['afford_score']}/100</td></tr>
              </tbody>
            </table>
          </div>
        </div>
{narrative}
      </div>
    </section>

    <section class="ra-band" id="ra-rent-rules">
      <div class="container container--wide">
{section_head(f"Gross vs net: how rent rules work in {name}", "Landlords screen on gross income. Your budget runs on take-home pay. Both numbers matter — here is how to use them.")}
{rules_html}
        <p class="ra-cta-line">Run your exact take-home in our <a class="ra-text-link" href="{ext['tax_link']}">{state_name} paycheck calculator</a>, then compare the result to the comfortable band from the calculator above.</p>
      </div>
    </section>

    <section class="ra-band ra-band--alt" id="ra-rent-by-income">
      <div class="container container--wide">
{section_head(f"How much rent can you afford in {name}?", "Affordable monthly rent at the classic 30% of gross income rule. Your real ceiling may be lower once debt, savings, and utilities are in the picture.")}
        <div class="ra-table-card">
          <div class="ra-snapshot-table-wrap">
            <table class="debt-data-table ra-city-table ra-income-table">
              <caption>Affordable rent by salary in {name}</caption>
              <thead><tr><th scope="col">Salary</th><th scope="col">Affordable rent (30% gross)</th></tr></thead>
              <tbody>
{tier_rows}
              </tbody>
            </table>
          </div>
        </div>
        <h3 class="ra-subhead">Common salary scenarios</h3>
        <div class="ra-expand-stack">
{expansions}
        </div>
{render_callout("These figures use the 30% gross rule. Debt, savings, and utilities can lower your real ceiling — that is why we show comfortable and stretch bands in the hero calculator, not just one max.", "How to use this table")}
      </div>
    </section>

    <section class="ra-band" id="ra-hidden-costs">
      <div class="container container--wide">
{section_head(f"Hidden costs of renting in {name}", "The listing price is not your total housing bill. Budget these lines before you compare apartments.")}
{hidden_html}
      </div>
    </section>

    <section class="ra-band ra-band--alt" id="ra-neighborhoods">
      <div class="container container--wide">
{section_head(f"{name} neighborhood comparison", "Typical asking rent and rough income needed for a comfortable 30% gross cap. Your block may differ — use these to narrow your search.")}
        <div class="ra-table-card">
          <div class="ra-snapshot-table-wrap">
            <table class="debt-data-table ra-city-table ra-nh-table">
              <caption>{name} neighborhoods — rent and income benchmarks</caption>
              <thead><tr><th scope="col">Neighborhood</th><th scope="col">Typical rent</th><th scope="col">Comfortable on</th></tr></thead>
              <tbody>
{nh_rows}
              </tbody>
            </table>
          </div>
        </div>
{render_callout(lf.get('neighborhood_prose', ''), 'Neighborhood notes')}
        <p class="ra-cta-line">Compare with <a class="ra-text-link" href="{compare_href}">{ext['compare_note']}</a> or open our <a class="ra-text-link" href="{ext['col_link']}">{name} cost of living guide</a> for groceries, transit, and tax context.</p>
      </div>
    </section>

    <section class="ra-band" id="ra-budget-breakdown">
      <div class="container container--wide">
{section_head(f"Monthly budget breakdown example ({fmt(income)} income)", f"Illustrative split using {name} defaults — not your exact paycheck. Swap in your take-home from our after-tax calculator.")}
        <div class="ra-budget-visual">
          <p class="ra-budget-visual__net">Monthly take-home pay: <strong>{fmt(bb['net'])}</strong></p>
          <ul class="ra-budget-list">
{budget_list}
          </ul>
        </div>
{budget_reading}
      </div>
    </section>

    <section class="ra-band ra-band--alt" id="ra-affordability-tiers">
      <div class="container container--wide">
{section_head(f"Affordability tiers in {name}", tiers_intro)}
        <div class="ra-tier-grid">
{tier_cards}
        </div>
{render_callout(lf.get('tiers_extra', ''), 'How to read these tiers')}
      </div>
    </section>
{long_tail_html}
    <section class="ra-band" id="ra-related-income">
      <div class="container container--wide">
{section_head("Related income &amp; housing pages", f"Connect your rent cap to salary scenarios, cost of living, and buy-vs-rent decisions in {name}.")}
        <div class="ra-related-grid">
{related}
        </div>
      </div>
    </section>

    <section class="ra-band ra-band--alt living-faq-section ra-city-faq" id="ra-faq">
      <div class="container container--wide">
{section_head(f"{name} rent affordability FAQ", "Short answers to common search questions. Run the calculator above for numbers tied to your income and debt.")}
        <div class="faq-stack ra-faq-stack">
{faqs}
        </div>
      </div>
    </section>
  </main>
  <footer class="site-footer">
    <div class="container footer-layout">
      <p class="footer-description">US-only tools to calculate your real income after tax, understand debt, and make smarter financial decisions.</p>
      <div class="footer-grid" role="navigation" aria-label="Footer">
        <section class="footer-column" aria-labelledby="footer-popular-calculators">
          <h2 id="footer-popular-calculators">Popular Calculators</h2>
          <a href="/hourly-to-salary-after-tax">Hourly to Salary After Tax</a>
          <a href="/debt/credit-cards/credit-card-payoff-calculator">Credit Card Payoff Calculator</a>
          <a href="/rent-vs-buy-calculator">Rent vs Buy Calculator</a>
          <a href="/1099-vs-w2-calculator">1099 vs W2 Calculator</a>
        </section>
        <section class="footer-column" aria-labelledby="footer-tools-category">
          <h2 id="footer-tools-category">Tools by Category</h2>
          <a href="/hourly-to-salary-after-tax">Income</a>
          <a href="/debt">Debt</a>
          <a href="/rent-vs-buy-calculator">Living</a>
          <a href="/1099-vs-w2-calculator">Freelance</a>
        </section>
        <section class="footer-column" aria-labelledby="footer-explore-more">
          <h2 id="footer-explore-more">Explore More</h2>
          <a href="/living/housing/how-much-rent-can-i-afford">Rent affordability hub</a>
          <a href="{ext['col_link']}">Cost of living in {name}</a>
          <a href="/rent-vs-buy-calculator">Rent vs buy calculator</a>
        </section>
        <section class="footer-column" aria-labelledby="footer-company">
          <h2 id="footer-company">Company</h2>
          <a href="/about">About</a>
          <a href="/editorial-policy">Editorial policy</a>
          <a href="/contact">Contact</a>
        </section>
      </div>
      <p class="footer-copy">© 2026 IncomeClarityLab</p>
    </div>
  </footer>
  <script src="/rent-afford-city.js"></script>
  <script src="/page-toc.js" defer></script>
</body>
</html>"""


CITIES = {
    ("texas", "austin"): {"name": "Austin", "state_name": "Texas"},
    ("texas", "dallas"): {"name": "Dallas", "state_name": "Texas"},
    ("new-york", "new-york-city"): {"name": "New York City", "state_name": "New York"},
    ("florida", "miami"): {"name": "Miami", "state_name": "Florida"},
    ("illinois", "chicago"): {"name": "Chicago", "state_name": "Illinois"},
}


def main() -> None:
    issues = []
    count = 0
    for (state_slug, city_slug), meta in CITIES.items():
        out_dir = BASE / state_slug / city_slug
        out_dir.mkdir(parents=True, exist_ok=True)
        html = city_page(state_slug, city_slug, meta)
        words = count_main_words(html)
        (out_dir / "index.html").write_text(html, encoding="utf-8")
        count += 1
        label = f"{state_slug}/{city_slug}"
        print(f"  {label}: {words} words")
        if words < MIN_MAIN_WORDS:
            issues.append(f"{label}: {words} words (need {MIN_MAIN_WORDS}+)")
        else:
            print(f"Wrote {out_dir / 'index.html'}")
    print(f"Generated {count} rent affordability city pages")
    if issues:
        print("\nValidation issues:")
        for issue in issues:
            print(f"  - {issue}")
        raise SystemExit(1)


if __name__ == "__main__":
    main()
