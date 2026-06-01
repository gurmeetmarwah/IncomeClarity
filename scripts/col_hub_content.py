"""Hub page HTML and catalog JSON for cost-of-living-by-city."""
from __future__ import annotations

import json


def fmt(n: int) -> str:
    return f"${n:,}"


def city_tags(city: dict, state_slug: str | None) -> list[str]:
    tags = []
    if city.get("lifestyle_score", 0) >= 72:
        tags.append("family")
    if city.get("col_index", 999) <= 108:
        tags.append("affordable")
    if state_slug in ("texas", "florida") or city.get("name") in ("Austin", "Dallas", "Houston", "Phoenix"):
        tags.append("low-tax")
    if city.get("name") in ("Austin", "Dallas", "Denver", "Phoenix", "Atlanta", "Raleigh"):
        tags.append("remote")
    return tags or ["all"]


def build_catalog(states: dict, standalone: dict) -> list[dict]:
    entries = []
    for state_slug, state in states.items():
        for city_slug, city in state["cities"].items():
            path = f"/living/housing/cost-of-living-by-city/{state_slug}/{city_slug}"
            label = f"{city['name']}, {state['name'][:2].upper() if len(state['name']) > 2 else state['name']}"
            if state["name"] == "California":
                label = f"{city['name']}, CA"
            elif state["name"] == "Texas":
                label = f"{city['name']}, TX"
            elif state["name"] == "Florida":
                label = f"{city['name']}, FL"
            elif state["name"] == "New York":
                label = f"{city['name']}, NY"
            entries.append(_entry(city, city_slug, label, path, state_slug, tags=city_tags(city, state_slug)))
    for slug, city in standalone.items():
        if slug == "new-york":
            continue
        st = city.get("state_name", "")
        abbr = {"Washington": "WA", "Illinois": "IL", "Colorado": "CO", "Georgia": "GA", "Arizona": "AZ"}.get(st, st[:2])
        label = f"{city['name']}, {abbr}"
        path = f"/living/housing/cost-of-living-by-city/{slug}"
        entries.append(_entry(city, slug, label, path, None, tags=city_tags(city, None)))
    return entries


def _entry(city: dict, slug: str, label: str, path: str, state_slug: str | None, tags: list[str]) -> dict:
    return {
        "id": slug,
        "label": label,
        "name": city["name"],
        "path": path,
        "compareKey": slug.replace("-", "").replace("city", "")[:12] or slug,
        "rent": city["rent_1br"],
        "housing": city["rent_1br"],
        "groceries": city["groceries"],
        "utilities": city["utilities"],
        "transport": city["transport"],
        "healthcare": city.get("healthcare", 420),
        "taxes": city.get("taxes_month", 200),
        "salary": city["salary_comfort"],
        "score": city["lifestyle_score"],
        "index": city["col_index"],
        "tags": tags,
    }


def compare_card(c: dict) -> str:
    rent_delta = c["rent_a"] - c["rent_b"]
    sal_delta = c["salary_a"] - c["salary_b"]
    rd_sign = "col-delta--bad" if rent_delta > 0 else "col-delta--good"
    rd_label = f"+{fmt(rent_delta)}/mo" if rent_delta > 0 else f"{fmt(rent_delta)}/mo"
    sd_label = f"+{fmt(abs(sal_delta))}" if sal_delta > 0 else f"-{fmt(abs(sal_delta))}"
    return f"""
          <a class="col-compare-card" href="/living/housing/cost-of-living-by-city/compare/{c['slug']}">
            <h3>{c.get('title_short', c.get('title', 'Compare'))}</h3>
            <div class="col-compare-card__metrics">
              <div class="col-compare-metric"><span>Rent gap</span><strong class="{rd_sign}">{rd_label}</strong></div>
              <div class="col-compare-metric"><span>Pay gap</span><strong>{sd_label}</strong></div>
              <div class="col-compare-metric"><span>Lower rent</span><strong>{c['winner_rent']}</strong></div>
            </div>
            <span class="col-compare-card__cta">See pair →</span>
          </a>"""


def explore_card(e: dict) -> str:
    tags = ",".join(e["tags"])
    return f"""
          <article class="col-explore-card" data-tags="{tags}" data-rent="{e['rent']}" data-score="{e['score']}" data-index="{e['index']}">
            <span class="col-explore-card__loc">{e['label']}</span>
            <h3>{e['name']}</h3>
            <div class="col-explore-card__row"><span>Rent</span><strong>{fmt(e['rent'])}/mo</strong></div>
            <div class="col-explore-card__row"><span>Pay target</span><strong>{fmt(e['salary'])}</strong></div>
            <span class="col-score">Score {e['score']}/100</span>
            <div class="col-explore-card__actions">
              <a class="col-btn col-btn--primary" href="{e['path']}">See costs</a>
            </div>
          </article>"""


def render_hub_page(
    catalog: list[dict],
    comparisons: list[dict],
    states_meta: list[dict],
    header: str,
    footer: str,
    url_script: str,
    faq_html: str,
    explained_html: str,
    lifestyle_section: str = "",
) -> str:
    catalog_json = json.dumps(catalog)
    compare_cards = "\n".join(compare_card(c) for c in comparisons)
    explore_cards = "\n".join(explore_card(e) for e in catalog)
    state_tiles = "\n".join(
        f"""
          <a class="col-state-tile" href="{s['path']}">
            <h3>{s['name']}</h3>
            <p class="col-state-tile__meta">{s['city_count']} cities · {s['tagline']}</p>
            <div class="col-state-tile__stats">
              <div><span>Avg rent</span><strong>{fmt(s['rent_1br'])}/mo</strong></div>
              <div><span>Comfort salary</span><strong>{fmt(s['salary_comfort'])}</strong></div>
              <div><span>Cost index</span><strong>{s['col_index']}</strong></div>
            </div>
          </a>"""
        for s in states_meta
    )
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Cost of Living by City — Compare U.S. Cities (2026) | Income Clarity</title>
  <meta name="description" content="Compare the real cost of living across U.S. cities. Housing, groceries, transportation, taxes, and salary needs before you move.">
  <link rel="canonical" href="https://www.incomeclaritylab.com/living/housing/cost-of-living-by-city">
  <link rel="stylesheet" href="/styles.css">
  <link rel="stylesheet" href="/styles-living-system.css">
  <link rel="stylesheet" href="/styles-col.css">
  <link rel="icon" type="image/svg+xml" href="/favicon.svg">
{url_script}
</head>
<body class="col-page living-tool-page">
{header}
  <main>
    <section class="col-hero-hub">
      <div class="container">
        <nav class="take-home-return-nav" aria-label="Breadcrumb">
          <ol class="take-home-return-breadcrumbs">
            <li><a href="/rent-vs-buy-calculator">Living</a></li>
            <li aria-current="page">Cost of living by city</li>
          </ol>
        </nav>
        <span class="label">Cost of living · U.S. cities</span>
        <h1>Cost of Living by U.S. City</h1>
        <p class="subhead">See rent, food, bills, and pay targets before you move.</p>
        <div class="col-hero-search">
          <label for="col-search-input">Search city or state</label>
          <div class="col-hero-search__row col-hero-search__row--lookup">
            <input type="search" id="col-search-input" list="col-search-list" placeholder="Try Austin, Texas, Miami…" autocomplete="off">
            <button type="button" class="col-btn col-btn--primary" id="col-search-go">Go</button>
          </div>
          <datalist id="col-search-list"></datalist>
          <p class="col-input-help" id="col-search-help">Type a city or state, then press Enter.</p>
          <div class="col-search-hints">
            <span>Try:</span>
            <button type="button" data-hint="Austin, TX">Austin, TX</button>
            <button type="button" data-hint="Seattle, WA">Seattle, WA</button>
            <button type="button" data-hint="Miami, FL">Miami, FL</button>
          </div>
        </div>
        <div class="col-hub-plain">
          <p>Moving? Start with rent. It is often the biggest bill each month.</p>
          <p>We also list food, power, and car costs. Tax is not in the core stack.</p>
          <p>Comfort pay is gross pay before tax. Add debt and kids on top.</p>
          <p>Index 100 is the US norm. A higher index means you need more pay or tighter spending.</p>
          <p>Pick a state if you know the state but not the city. Pick a pair if you debate two places.</p>
          <p>Your lease quote beats our defaults. Use tools after you pick a city.</p>
        </div>
      </div>
    </section>

    <section class="col-insight-bar" aria-label="Quick insights">
      <div class="container col-insight-bar__grid">
        <div class="col-insight-pill"><span class="col-insight-pill__kicker">Lowest rent hub</span><span class="col-insight-pill__val">Houston, TX</span></div>
        <div class="col-insight-pill"><span class="col-insight-pill__kicker">Fast rent growth</span><span class="col-insight-pill__val">Miami &amp; NYC</span></div>
        <div class="col-insight-pill"><span class="col-insight-pill__kicker">Low tax states</span><span class="col-insight-pill__val">TX &amp; FL</span></div>
        <div class="col-insight-pill"><span class="col-insight-pill__kicker">Family picks</span><span class="col-insight-pill__val">Houston · Orlando</span></div>
      </div>
    </section>

    <section class="col-band" id="col-featured-compare">
      <div class="container">
        <header class="col-band__head">
          <h2>City pairs</h2>
          <p>Rent gap and pay gap in one click.</p>
        </header>
        <div class="col-compare-scroll">
{compare_cards}
        </div>
      </div>
    </section>

    <section class="col-band col-band--alt" id="col-states">
      <div class="container">
        <header class="col-band__head">
          <h2>Browse by state</h2>
          <p>State medians and links to each metro.</p>
        </header>
        <div class="col-state-grid">
{state_tiles}
        </div>
      </div>
    </section>

    <section class="col-band" id="col-explore">
      <div class="container">
        <header class="col-band__head">
          <h2>Popular cities</h2>
          <p>Rent, pay target, and score. Use filters to narrow the list.</p>
        </header>
        <div class="col-toolbar">
          <div class="col-chips" role="group" aria-label="Filter cities">
            <button type="button" class="col-chip is-active" data-col-filter="all">All</button>
            <button type="button" class="col-chip" data-col-filter="affordable">Lower rent</button>
            <button type="button" class="col-chip" data-col-filter="family">Family</button>
            <button type="button" class="col-chip" data-col-filter="remote">Remote</button>
            <button type="button" class="col-chip" data-col-filter="low-tax">Low tax</button>
          </div>
          <div class="col-sort">
            <label for="col-sort" class="sr-only">Sort cities</label>
            <select id="col-sort">
              <option value="score">Sort: best score</option>
              <option value="rent">Sort: rent low to high</option>
              <option value="index">Sort: cost index</option>
            </select>
          </div>
        </div>
        <div class="col-explore-grid" id="col-city-grid">
{explore_cards}
        </div>
        <div class="col-explore-more">
          <button type="button" class="col-btn col-btn--ghost" id="col-show-more" aria-expanded="false">Show more cities</button>
        </div>
      </div>
    </section>

    <section class="col-band col-band--alt" id="col-breakdown">
      <div class="container">
        <header class="col-band__head">
          <h2>Monthly breakdown</h2>
          <p>See how one city stacks up to the US norm.</p>
        </header>
        <div class="col-breakdown-panel">
          <div>
            <label for="col-breakdown-city">Selected city</label>
            <select id="col-breakdown-city"></select>
            <div class="col-breakdown-legend">
              <span class="leg-us">U.S. average</span>
              <span class="leg-city">Selected city</span>
            </div>
          </div>
          <div id="col-breakdown-bars"></div>
        </div>
      </div>
    </section>

{lifestyle_section}
    <section class="col-band" id="col-salary">
      <div class="container">
        <header class="col-band__head">
          <h2>Pay you may need</h2>
          <p>Start here, then open a city page for local numbers.</p>
        </header>
        <div class="col-salary-grid">
          <article class="col-salary-card">
            <h3>Single person</h3>
            <p>Often $65k to $120k in gross pay. High-rent coasts sit at the top.</p>
            <a href="/living/lifestyle/comfortable-salary-us">Salary guide →</a>
          </article>
          <article class="col-salary-card">
            <h3>Couple</h3>
            <p>Two incomes help. Shared rent cuts cost per person.</p>
            <a href="/living/family-budgeting/can-i-afford-to-live-alone.html">Cost to live as a couple →</a>
          </article>
          <article class="col-salary-card">
            <h3>Family of 4</h3>
            <p>Add child care after rent. $90k to $220k gross is common on city pages.</p>
            <a href="/living/lifestyle-family/family-of-4-income-guide/">Family of 4 budget →</a>
          </article>
          <article class="col-salary-card">
            <h3>Remote work</h3>
            <p>Compare net pay by state. No income tax can beat a higher gross in some moves.</p>
            <a href="/hourly-to-salary-after-tax">Net pay by state →</a>
          </article>
        </div>
      </div>
    </section>

    <section class="col-band col-band--alt" id="col-scenarios">
      <div class="container">
        <header class="col-band__head">
          <h2>Sample budgets</h2>
          <p>How costs feel for real homes.</p>
        </header>
        <div class="col-scenario-grid">
          <article class="col-scenario-card">
            <h3>Young professional in Austin</h3>
            <p><strong>Salary:</strong> $95k gross</p>
            <p><strong>Rent burden:</strong> Moderate — 1BR near $1,750/mo</p>
            <p><strong>Edge:</strong> No state income tax</p>
          </article>
          <article class="col-scenario-card">
            <h3>Family in San Diego</h3>
            <p><strong>Salary needed:</strong> ~$220k gross (family line)</p>
            <p><strong>Rent burden:</strong> High on coastal zips</p>
            <p><a href="/living/housing/cost-of-living-by-city/california/san-diego">San Diego COL →</a></p>
          </article>
          <article class="col-scenario-card">
            <h3>Remote worker in Dallas</h3>
            <p><strong>Salary:</strong> $85k from coastal employer</p>
            <p><strong>Affordability advantage:</strong> Strong vs NYC/SF</p>
            <p><a href="/living/housing/cost-of-living-by-city/texas/dallas">Dallas COL →</a></p>
          </article>
        </div>
      </div>
    </section>

    <section class="col-band" id="col-explained">
      <div class="container">
        <header class="col-band__head">
          <h2>Key ideas</h2>
          <p>What to weigh when you compare cities or job offers.</p>
        </header>
        <div class="col-explained-grid">
{explained_html}
        </div>
      </div>
    </section>

    <section class="col-band col-band--alt" id="col-tools">
      <div class="container">
        <header class="col-band__head">
          <h2>Related tools</h2>
          <p>Go from comparison to a concrete housing or salary plan.</p>
        </header>
        <div class="col-tools-grid">
          <a class="col-tool-link" href="/rent-vs-buy-calculator"><strong>Rent vs buy calculator</strong><span>Break-even year and net cost</span></a>
          <a class="col-tool-link" href="/living/housing/how-much-house-can-i-afford"><strong>How much house can I afford</strong><span>28/36 rule by location</span></a>
          <a class="col-tool-link" href="/living/housing/how-much-rent-can-i-afford"><strong>Rent affordability</strong><span>Cap rent on take-home pay</span></a>
          <a class="col-tool-link" href="/living/budgeting/average-monthly-expenses.html"><strong>Monthly expenses guide</strong><span>Budget buckets and benchmarks</span></a>
          <a class="col-tool-link" href="/living/lifestyle/comfortable-salary/california"><strong>Comfortable salary (California)</strong><span>State take-home and targets</span></a>
          <a class="col-tool-link" href="/living/lifestyle/comfortable-salary/texas"><strong>Comfortable salary (Texas)</strong><span>No state income tax framing</span></a>
        </div>
      </div>
    </section>

    <section class="col-band col-band--alt">
      <div class="container">
        <h2>How we score cities</h2>
        <ul class="col-key-list">
          <li>Rent, food, power, and commute in plain monthly dollars — index 100 = U.S. norm.</li>
          <li>Comfort salary is gross pay before tax; add childcare and debt on top.</li>
          <li>Compare net pay by state when you weigh job offers — tax can beat a small rent gap.</li>
          <li>Your lease quote beats our defaults; use tools after you pick a city.</li>
        </ul>
      </div>
    </section>

    <section class="col-faq-section">
      <div class="container content-page">
        <h2>Frequently asked questions</h2>
        <div class="faq-stack">
{faq_html}
        </div>
      </div>
    </section>

    <section class="col-band">
      <div class="container">
        <div class="col-final-cta">
          <h2>Next steps</h2>
          <p>Pick a city, test housing, or map the pay you need.</p>
          <div class="col-final-cta__actions">
            <a class="col-btn col-btn--primary" href="#col-explore">Compare another city</a>
            <a class="col-btn col-btn--ghost" href="/living/housing/how-much-house-can-i-afford">Housing affordability</a>
            <a class="col-btn col-btn--ghost" href="/living/lifestyle/comfortable-salary-us">Salary calculators</a>
          </div>
        </div>
      </div>
    </section>
  </main>
{footer}
  <script type="application/json" id="col-catalog">{catalog_json}</script>
  <script src="/col-by-city.js"></script>
  <script>
    document.querySelectorAll('[data-hint]').forEach(function(btn) {{
      btn.addEventListener('click', function() {{
        var input = document.getElementById('col-search-input');
        if (input) {{ input.value = btn.getAttribute('data-hint'); input.focus(); }}
      }});
    }});
  </script>
  <script src="/guide-back.js"></script>
</body>
</html>
"""
