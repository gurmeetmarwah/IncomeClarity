#!/usr/bin/env python3
"""Generate $1,500 and $3,000 interactive payoff scenario pages."""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "debt/payoff-scenarios"

SCENARIOS = [
    {
        "slug": "how-long-to-pay-off-1500-debt",
        "js_file": "payoff-1500-scenario.js",
        "from_tag": "payoff-1500",
        "prefix": "sc15",
        "balance": 1500,
        "balance_label": "$1,500",
        "balance_short": "$1.5k",
        "default_payment": 100,
        "hero_months": "1 year 6 months",
        "hero_interest": "$270",
        "hero_extra": "$25",
        "hero_save_months": "4",
        "hero_save_interest": "$80",
        "payment_min": 25,
        "payment_max": 800,
        "payment_slider_min": 25,
        "balance_min": 100,
        "lump_max": 15000,
        "budget_boost": 25,
        "back_tier": "/debt/credit-cards/payoff-under-5000",
        "back_tier_label": "small balances guide",
        "related_slug": "how-long-to-pay-off-3000-debt",
        "related_title": "$3,000 debt payoff timeline",
        "related_desc": "Step up to a $3k balance—timelines and payment paths.",
        "compare_slug": "how-long-to-pay-off-3000-debt",
        "compare_label": "$3,000 payoff page",
        "title": "How Long Will $1,500 in Credit Card Debt Really Take to Pay Off?",
        "description": "Have $1,500 in credit card debt? See payoff time at your APR and payment—and how $25 more a month changes your finish line.",
        "breadcrumb": "Pay off $1,500 debt",
        "snapshot_rows": [
            ("$50", "3 years 8 months", "$698", "$2,198"),
            ("$75", "2 years 2 months", "$386", "$1,886"),
            ("$100", "1 year 6 months", "$270", "$1,770"),
            ("$125", "1 year 2 months", "$210", "$1,710"),
        ],
        "what_if_lead": "On a $1,500 balance, even +$25/month can shave months off your payoff.",
        "faq_timeline": "At <strong>22% APR</strong> with <strong>$100 a month</strong>, you are debt-free in about <strong>18 months</strong>. And you pay about <strong>$270 in interest</strong>.",
        "faq_realistic": "Most people clear $1,500 in <strong>12 to 24 months</strong> with steady payments above the minimum.",
        "body_class": "",
        "context_section": "",
    },
    {
        "slug": "how-long-to-pay-off-3000-debt",
        "js_file": "payoff-3000-scenario.js",
        "from_tag": "payoff-3000",
        "prefix": "sc3k",
        "balance": 3000,
        "balance_label": "$3,000",
        "balance_short": "$3k",
        "default_payment": 150,
        "hero_months": "2 years 2 months",
        "hero_interest": "$771",
        "hero_extra": "$50",
        "hero_save_months": "6",
        "hero_save_interest": "$200",
        "payment_min": 50,
        "payment_max": 1500,
        "payment_slider_min": 50,
        "balance_min": 200,
        "lump_max": 25000,
        "budget_boost": 50,
        "back_tier": "/debt/credit-cards/payoff-under-5000",
        "back_tier_label": "small balances guide",
        "related_slug": "how-long-to-pay-off-5000-debt",
        "related_title": "$5,000 debt payoff timeline",
        "related_desc": "Next step up—see how a $5k balance changes the math.",
        "compare_slug": "how-long-to-pay-off-1500-debt",
        "compare_label": "$1,500 payoff page",
        "title": "How Long Will $3,000 in Credit Card Debt Really Take to Pay Off?",
        "description": "Have $3,000 in credit card debt? See payoff time at your APR and payment—and how $50 more a month cuts interest and months owed.",
        "breadcrumb": "Pay off $3,000 debt",
        "snapshot_rows": [
            ("$75", "6 years 1 month", "$2,457", "$5,457"),
            ("$100", "3 years 8 months", "$1,395", "$4,395"),
            ("$150", "2 years 2 months", "$771", "$3,771"),
            ("$200", "1 year 6 months", "$541", "$3,541"),
        ],
        "what_if_lead": "On $3,000, +$50/month often saves hundreds in interest versus a slower payment.",
        "faq_timeline": "At <strong>22% APR</strong> with <strong>$150 a month</strong>, you are debt-free in about <strong>2 years 2 months</strong>. And you pay about <strong>$771 in interest</strong>.",
        "faq_realistic": "Most people aim for <strong>18 to 30 months</strong> on a $3,000 balance with payments above the minimum.",
        "body_class": " debt-scenario-page--3k",
        "context_section": """
    <section class="sc5-panel sc5-panel--context" id="sc3k-why" aria-labelledby="sc3k-why-title">
      <header class="sc5-section-head">
        <h2 id="sc3k-why-title">Why $3,000 is a turning point</h2>
        <p>Big enough to hurt. Small enough to beat in under three years.</p>
      </header>
      <div class="sc5-context-grid">
        <article class="sc5-context-card">
          <h3>Interest adds up fast</h3>
          <p>At 22% APR, $3,000 earns about <strong>$55 a month</strong> in interest at first. Pay only $75 and most of your money goes to the bank—not your balance.</p>
        </article>
        <article class="sc5-context-card">
          <h3>Minimums feel affordable</h3>
          <p>A ~$90 minimum keeps you current but can stretch payoff for <strong>years</strong>. See <a href="/debt/debt-reality/why-paying-minimum-is-bad?from=payoff-3000">why paying the minimum hurts</a>.</p>
        </article>
        <article class="sc5-context-card">
          <h3>Compare to $1,500</h3>
          <p>Double the balance does not mean double the time if you raise your payment. See our <a href="/debt/payoff-scenarios/how-long-to-pay-off-1500-debt?from=payoff-3000">$1,500 payoff page</a> if you are prioritizing which card to attack first.</p>
        </article>
      </div>
    </section>""",
    },
]

JS_TEMPLATE = """(function () {{
  if (!window.IncomeClarityPayoffScenario) return;
  window.IncomeClarityPayoffScenario.init({{
    idPrefix: "{prefix}",
    defaultBalance: {balance},
    defaultPayment: {default_payment},
    paymentTablePayments: {payment_table},
    budgetBoost: {budget_boost},
    whatIf: {what_if},
    realistic: {realistic},
  }});
}})();
"""

JS_CONFIGS = {
    "sc15": {
        "payment_table": [50, 75, 100, 125, 150, 200],
        "budget_boost": 25,
        "what_if": [
            {"title": "Pay $25 more", "extra": 25},
            {"title": "Pay $50 more", "extra": 50},
            {"title": "Lump sum $300", "lump": 300},
        ],
        "realistic": [
            {"key": "comfortable", "label": "Comfortable", "pct": 0.025, "floor": 50},
            {"key": "moderate", "label": "Moderate", "pct": 0.04, "floor": 75},
            {"key": "aggressive", "label": "Aggressive", "pct": 0.07, "floor": 125},
        ],
    },
    "sc3k": {
        "payment_table": [75, 100, 125, 150, 200, 300],
        "budget_boost": 50,
        "what_if": [
            {"title": "Pay $50 more", "extra": 50},
            {"title": "Pay $75 more", "extra": 75},
            {"title": "Lump sum $500", "lump": 500},
        ],
        "realistic": [
            {"key": "comfortable", "label": "Comfortable", "pct": 0.025, "floor": 75},
            {"key": "moderate", "label": "Moderate", "pct": 0.04, "floor": 125},
            {"key": "aggressive", "label": "Aggressive", "pct": 0.07, "floor": 200},
        ],
    },
}


def fmt_what_if(items):
    parts = []
    for item in items:
        if "extra" in item:
            parts.append(f'{{ title: "Pay ${item["extra"]} more", extra: {item["extra"]} }}')
        else:
            parts.append(f'{{ title: "{item["title"]}", lump: {item["lump"]} }}')
    return "[" + ", ".join(parts) + "]"


def fmt_realistic(items):
    parts = []
    for r in items:
        parts.append(
            f'{{ key: "{r["key"]}", label: "{r["label"]}", pct: {r["pct"]}, floor: {r["floor"]} }}'
        )
    return "[" + ", ".join(parts) + "]"


def table_rows_html(rows):
    return "\n".join(
        f"""            <tr>
              <th scope="row">{pay}</th>
              <td>{time}</td>
              <td>{interest}</td>
              <td>{total}</td>
            </tr>"""
        for pay, time, interest, total in rows
    )


def render_html(s: dict) -> str:
    p = s["prefix"]
    url = f"/debt/payoff-scenarios/{s['slug']}"
    rows = table_rows_html(s["snapshot_rows"])

    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{s["title"]} | Income Clarity</title>
  <meta name="description" content="{s["description"]}">
  <meta property="og:type" content="website">
  <meta property="og:url" content="https://www.incomeclaritylab.com{url}">
  <meta property="og:title" content="{s["title"]}">
  <meta property="og:description" content="{s["description"]}">
  <meta property="og:site_name" content="Income Clarity">
  <meta property="og:locale" content="en_US">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{s["title"]}">
  <meta name="twitter:description" content="{s["description"]}">
  <meta name="robots" content="index,follow">
  <link rel="canonical" href="https://www.incomeclaritylab.com{url}">
  <link rel="stylesheet" href="/styles.css">
  <link rel="icon" type="image/png" href="/images/logo.png">
  <link rel="apple-touch-icon" href="/images/logo.png">
  <script>
    (function () {{
      const path = window.location.pathname;
      let cleanPath = path;
      if (path === "/index.html") cleanPath = "/";
      else if (path.endsWith("/index.html")) cleanPath = path.slice(0, -10);
      else if (path.endsWith(".html")) cleanPath = path.slice(0, -5);
      if (cleanPath !== path) window.history.replaceState({{}}, "", cleanPath + window.location.search + window.location.hash);
    }})();
  </script>
  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "WebApplication",
    "name": "{s["title"]}",
    "description": "{s["description"]}",
    "url": "https://www.incomeclaritylab.com{url}",
    "applicationCategory": "FinanceApplication",
    "operatingSystem": "Web",
    "offers": {{ "@type": "Offer", "price": "0", "priceCurrency": "USD" }},
    "isPartOf": {{ "@type": "WebSite", "name": "Income Clarity", "url": "https://www.incomeclaritylab.com/" }}
  }}
  </script>
  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "BreadcrumbList",
    "itemListElement": [
      {{ "@type": "ListItem", "position": 1, "name": "Debt", "item": "https://www.incomeclaritylab.com/debt" }},
      {{ "@type": "ListItem", "position": 2, "name": "Debt payoff scenarios", "item": "https://www.incomeclaritylab.com/debt/payoff-scenarios" }},
      {{ "@type": "ListItem", "position": 3, "name": "{s["breadcrumb"]}", "item": "https://www.incomeclaritylab.com{url}" }}
    ]
  }}
  </script>
</head>
<body class="debt-scenario-page{s["body_class"]}">
  <header class="site-header">
    <div class="container nav-wrap">
      <a class="logo" href="/"><img src="/images/logo.png" alt="" width="32" height="32"><span class="logo-text">Income Clarity</span></a>
      <nav class="nav-links" aria-label="Primary">
        <a href="/hourly-to-salary-after-tax">Income</a>
        <a href="/debt" aria-current="page">Debt</a>
        <a href="/rent-vs-buy-calculator">Living</a>
        <a href="/1099-vs-w2-calculator">Freelance</a>
      </nav>
    </div>
  </header>

  <main class="container sc5-page">
    <nav class="take-home-return-nav sc5-crumb" aria-label="Breadcrumb">
      <ol class="take-home-return-breadcrumbs">
        <li><a href="/debt/credit-cards">Credit cards</a></li>
        <li><a href="/debt/credit-cards/payoff-under-5000">Small balances</a></li>
        <li><a href="/debt/payoff-scenarios">Payoff scenarios</a></li>
        <li aria-current="page">{s["breadcrumb"]}</li>
      </ol>
    </nav>

    <p class="sc5-back">
      <a class="debt-minimum-guide-back-link" id="debt-guide-back-link" href="{s["back_tier"]}" data-debt-back-default="{s["back_tier"]}">← Back to {s["back_tier_label"]}</a>
    </p>

    <nav class="sc5-jump" aria-label="On this page">
      <a href="#{p}-quick-calc">Quick calc</a>
      <a href="#{p}-planner">Planner</a>
      <a href="#{p}-timeline">Timeline</a>
      <a href="#{p}-what-if">What if</a>
      <a href="#{p}-payment-table">Payments</a>
      <a href="#{p}-faq">FAQ</a>
    </nav>

    <section class="sc5-hero" id="{p}-hero" aria-labelledby="{p}-hero-title">
      <div class="sc5-hero-copy">
        <span class="label">Debt payoff scenario · {s["balance_label"]}</span>
        <h1 id="{p}-hero-title">{s["title"]}</h1>
        <p class="sc5-hero-lead">At 22% APR with ${s["default_payment"]} a month, you are debt-free in <strong>{s["hero_months"]}</strong>. And you pay {s["hero_interest"]} in interest. Pay {s["hero_extra"]} more a month and you save {s["hero_save_months"]} months and {s["hero_save_interest"]}. See your real numbers below.</p>
        <button type="button" class="sc5-btn sc5-btn--primary" data-scroll-to="{p}-quick-calc">Calculate payoff timeline</button>
      </div>
      <aside class="sc5-hero-preview" id="{p}-hero-preview" aria-label="Example payoff preview">
        <p class="sc5-preview-kicker">Live preview</p>
        <dl class="sc5-preview-stats">
          <div><dt>Debt balance</dt><dd data-preview-balance>{s["balance_label"]}</dd></div>
          <div><dt>Monthly payment</dt><dd data-preview-payment>${s["default_payment"]}</dd></div>
          <div><dt>Estimated payoff time</dt><dd data-preview-time>{s["hero_months"]}</dd></div>
        </dl>
      </aside>
    </section>
{s["context_section"]}
    <section class="sc5-panel" id="{p}-snapshot" aria-labelledby="{p}-snapshot-title">
      <header class="sc5-section-head">
        <h2 id="{p}-snapshot-title">{s["balance_label"]} debt at 22% APR: four payment paths</h2>
        <p>Same balance. Same APR. The only thing that changes is your monthly payment.</p>
      </header>
      <div class="scenario-table-wrap">
        <table class="scenario-table">
          <caption class="scenario-table__caption">Payoff time and total interest on a {s["balance_label"]} balance at 22% APR</caption>
          <thead>
            <tr>
              <th scope="col">Monthly payment</th>
              <th scope="col">Time to debt-free</th>
              <th scope="col">Total interest</th>
              <th scope="col">Total paid</th>
            </tr>
          </thead>
          <tbody>
{rows}
          </tbody>
        </table>
        <p class="scenario-table__footnote">Rough numbers. Your card uses daily interest. Issuer rules can shift the months by a few.</p>
      </div>
    </section>

    <aside class="what-this-means" role="note">
      <p class="what-this-means__title">What this means for you</p>
      <p>Small balances reward steady payments. Pick a fixed monthly amount above your interest charge—and hold it even when the issuer minimum drops.</p>
      <p>Match your payment to take-home pay, not wishful thinking. Use the planner below, then lock a number you can repeat every month.</p>
    </aside>

    <section class="sc5-panel sc5-panel--quick" id="{p}-quick-calc" aria-labelledby="{p}-quick-title">
      <header class="sc5-section-head">
        <h2 id="{p}-quick-title">Quick payoff calculator</h2>
        <p>Enter your numbers for an instant estimate—defaults match a typical {s["balance_short"]} credit card scenario.</p>
      </header>
      <form class="sc5-quick-form" id="{p}-quick-form">
        <label class="sc5-field">
          <span>Debt amount</span>
          <input type="number" id="{p}-quick-balance" value="{s["balance"]}" min="{s["balance_min"]}" step="50" required>
        </label>
        <label class="sc5-field">
          <span>Interest rate (APR %)</span>
          <input type="number" id="{p}-quick-apr" value="22" min="0" max="35" step="0.1" required>
        </label>
        <label class="sc5-field">
          <span>Monthly payment</span>
          <input type="number" id="{p}-quick-payment" value="{s["default_payment"]}" min="{s["payment_min"]}" step="25" required>
        </label>
        <button type="submit" class="sc5-btn sc5-btn--primary">Calculate</button>
      </form>
      <div class="sc5-quick-results" id="{p}-quick-results" hidden></div>
    </section>

    <section class="sc5-panel sc5-panel--planner" id="{p}-planner" aria-labelledby="{p}-planner-title">
      <header class="sc5-section-head">
        <h2 id="{p}-planner-title">Advanced payoff planner</h2>
        <p>Adjust debt type, rate, payments, and strategy—results update live on the right.</p>
      </header>
      <div class="sc5-planner-grid">
        <div class="sc5-planner-inputs">
          <fieldset class="sc5-fieldset">
            <legend>A. Debt type</legend>
            <div class="sc5-debt-type-grid" role="group" aria-label="Debt type">
              <button type="button" class="sc5-debt-type-card is-selected" data-debt-type="credit-card" aria-pressed="true">💳 Credit card</button>
              <button type="button" class="sc5-debt-type-card" data-debt-type="personal-loan" aria-pressed="false">📄 Personal loan</button>
              <button type="button" class="sc5-debt-type-card" data-debt-type="medical" aria-pressed="false">🏥 Medical debt</button>
              <button type="button" class="sc5-debt-type-card" data-debt-type="auto" aria-pressed="false">🚗 Auto loan</button>
              <button type="button" class="sc5-debt-type-card" data-debt-type="student" aria-pressed="false">🎓 Student loan</button>
            </div>
            <p class="sc5-hint" id="{p}-debt-type-hint">Revolving APR—paying more than the minimum usually saves years of interest.</p>
          </fieldset>

          <label class="sc5-field sc5-field--slider">
            <span>B. Interest rate (APR %)</span>
            <div class="sc5-slider-row">
              <input type="range" id="{p}-apr-range" min="0" max="35" step="0.5" value="22" aria-label="APR slider">
              <input type="number" id="{p}-apr" min="0" max="35" step="0.1" value="22" aria-label="APR percent">
            </div>
          </label>

          <label class="sc5-field sc5-field--slider">
            <span>C. Monthly payment</span>
            <div class="sc5-slider-row">
              <input type="range" id="{p}-payment-range" min="{s["payment_slider_min"]}" max="{s["payment_max"]}" step="25" value="{s["default_payment"]}" aria-label="Monthly payment slider">
              <input type="number" id="{p}-payment" min="{s["payment_slider_min"]}" max="{s["payment_max"]}" step="25" value="{s["default_payment"]}" aria-label="Monthly payment dollars">
            </div>
          </label>

          <label class="sc5-field">
            <span>D. Extra monthly payment</span>
            <input type="number" id="{p}-extra" value="0" min="0" max="{s["payment_max"]}" step="25" aria-describedby="{p}-extra-hint">
            <span class="sc5-hint" id="{p}-extra-hint">Added on top of your base monthly payment.</span>
          </label>

          <label class="sc5-field">
            <span>E. One-time lump sum</span>
            <input type="number" id="{p}-lump" value="0" min="0" max="{s["lump_max"]}" step="50">
          </label>

          <label class="sc5-field">
            <span>F. Debt strategy (guidance)</span>
            <select id="{p}-strategy" aria-label="Payoff strategy">
              <option value="minimum">Minimum payments</option>
              <option value="aggressive">Aggressive payoff</option>
              <option value="avalanche">Debt avalanche</option>
              <option value="snowball">Debt snowball</option>
            </select>
          </label>

          <label class="sc5-field">
            <span>Balance (adjust if not {s["balance_label"]})</span>
            <input type="number" id="{p}-balance" value="{s["balance"]}" min="{s["balance_min"]}" step="50">
          </label>
        </div>

        <aside class="sc5-results-sticky" aria-live="polite" aria-atomic="true">
          <h3 class="sc5-results-title">Your payoff snapshot</h3>
          <dl class="sc5-results-dl">
            <div class="sc5-result-row sc5-result-row--primary">
              <dt>Debt-free in</dt>
              <dd id="{p}-result-duration">—</dd>
            </div>
            <div class="sc5-result-row">
              <dt>Total interest paid</dt>
              <dd id="{p}-result-interest">—</dd>
            </div>
            <div class="sc5-result-row sc5-result-row--highlight">
              <dt>Interest saved vs base payment</dt>
              <dd id="{p}-result-saved">—</dd>
            </div>
            <div class="sc5-result-row">
              <dt>Estimated debt-free date</dt>
              <dd id="{p}-result-date">—</dd>
            </div>
          </dl>
          <p class="sc5-result-warning" id="{p}-result-warning" hidden></p>
          <a class="sc5-btn sc5-btn--secondary" href="/debt/credit-cards/credit-card-payoff-calculator#payoff">Open full payoff calculator</a>
        </aside>
      </div>
    </section>

    <section class="sc5-panel" id="{p}-timeline" aria-labelledby="{p}-timeline-title">
      <header class="sc5-section-head">
        <h2 id="{p}-timeline-title">Payoff timeline visualization</h2>
        <p>See how your balance shrinks month by month at your current inputs.</p>
      </header>
      <div id="{p}-timeline-bar"></div>
      <div class="sc5-viz-panel" id="{p}-viz-panel">
        <div class="sc5-chart-summary" id="{p}-chart-summary" aria-live="polite"></div>
        <div class="sc5-chart-grid">
          <div class="sc5-chart-card">
            <h3 class="sc5-chart-heading">Where your payments go</h3>
            <p class="sc5-chart-sub">Stacked by year—<strong class="sc5-chart-sub-interest">interest</strong> vs <strong class="sc5-chart-sub-principal">principal</strong>.</p>
            <div class="sc5-stacked-chart" id="{p}-stacked-chart" role="img" aria-label="Yearly principal and interest breakdown"></div>
            <div class="sc5-chart-legend">
              <span class="sc5-legend-item sc5-legend-item--principal"><i aria-hidden="true"></i> Principal</span>
              <span class="sc5-legend-item sc5-legend-item--interest"><i aria-hidden="true"></i> Interest</span>
            </div>
          </div>
          <div class="sc5-chart-card sc5-chart-card--balance">
            <h3 class="sc5-chart-heading">Balance shrinking</h3>
            <p class="sc5-chart-sub">Remaining debt after each year of payments.</p>
            <div class="sc5-balance-chart" id="{p}-balance-chart"></div>
            <p class="sc5-chart-insight" id="{p}-chart-insight"></p>
          </div>
        </div>
      </div>
    </section>

    <section class="sc5-panel sc5-panel--what-if" id="{p}-what-if" aria-labelledby="{p}-what-if-title">
      <header class="sc5-section-head">
        <h2 id="{p}-what-if-title">What if I pay more?</h2>
        <p>{s["what_if_lead"]}</p>
      </header>
      <div class="sc5-what-if-grid" id="{p}-what-if-grid"></div>
    </section>

    <section class="sc5-panel" id="{p}-payment-table" aria-labelledby="{p}-table-title">
      <header class="sc5-section-head">
        <h2 id="{p}-table-title">Monthly payment comparison</h2>
        <p>How payoff time and interest change when you raise your fixed monthly payment.</p>
      </header>
      <div class="sc5-table-wrap">
        <table class="state-page-compare-table sc5-compare-table">
          <thead>
            <tr>
              <th scope="col">Monthly payment</th>
              <th scope="col">Payoff time</th>
              <th scope="col">Total interest</th>
            </tr>
          </thead>
          <tbody id="{p}-payment-table-body"></tbody>
        </table>
      </div>
    </section>

    <section class="sc5-panel sc5-panel--strategies" id="{p}-strategies" aria-labelledby="{p}-strategies-title">
      <header class="sc5-section-head">
        <h2 id="{p}-strategies-title">Debt payoff strategies</h2>
        <p>One {s["balance_short"]} balance is straightforward—strategy matters more when you have several accounts.</p>
      </header>
      <div class="sc5-strategy-grid">
        <a class="sc5-strategy-card" href="/debt/payoff-strategies?from={s["from_tag"]}">
          <h3>Debt snowball</h3>
          <p>Focus on the smallest balance first for quick wins and momentum.</p>
          <span class="sc5-card-cta">Payoff strategies →</span>
        </a>
        <a class="sc5-strategy-card" href="/debt/credit-cards/minimum-payment-calculator">
          <h3>Minimum payment calculator</h3>
          <p>See how issuer minimums compare to a fixed payment plan.</p>
          <span class="sc5-card-cta">Estimate minimum →</span>
        </a>
        <a class="sc5-strategy-card" href="/debt/credit-cards/payoff-under-5000">
          <h3>Small balances guide</h3>
          <p>Under $5,000—timelines, plans, and popular payoff amounts.</p>
          <span class="sc5-card-cta">Read guide →</span>
        </a>
      </div>
    </section>

    <section class="sc5-panel sc5-panel--budget" id="{p}-budget" aria-labelledby="{p}-budget-title">
      <header class="sc5-section-head">
        <h2 id="{p}-budget-title">Budget impact</h2>
      </header>
      <p class="sc5-budget-impact" id="{p}-budget-impact">Adjust the planner to see how extra dollars affect your debt-free date.</p>
      <p class="sc5-budget-links">Check take-home pay in the <a href="/hourly-to-salary-after-tax#hourly-salary-form">salary after tax calculator</a>.</p>
    </section>

    <section class="sc5-panel sc5-panel--interest" id="{p}-interest" aria-labelledby="{p}-interest-title">
      <header class="sc5-section-head">
        <h2 id="{p}-interest-title">How interest grows on {s["balance_label"]}</h2>
      </header>
      <div class="sc5-interest-grid">
        <article class="sc5-interest-card">
          <h3>Interest adds up every day</h3>
          <p>Cards charge interest daily until you pay the balance down. Small debts still bleed money at high APR.</p>
          <a href="/debt/credit-cards/how-credit-card-interest-works?from={s["from_tag"]}">How credit card interest works →</a>
        </article>
        <article class="sc5-interest-card">
          <h3>The minimum payment trap</h3>
          <p>Minimums keep your account current. But most of each payment goes to interest—not principal.</p>
          <a href="/debt/debt-reality/why-paying-minimum-is-bad?from={s["from_tag"]}">Why minimums hurt →</a>
        </article>
        <article class="sc5-interest-card">
          <h3>Compare amounts</h3>
          <p>See how {s["balance_label"]} compares to other common balances in our payoff scenario library.</p>
          <a href="/debt/payoff-scenarios/{s["compare_slug"]}?from={s["from_tag"]}">{s["compare_label"]} →</a>
        </article>
      </div>
    </section>

    <section class="sc5-panel" id="{p}-realistic" aria-labelledby="{p}-realistic-title">
      <header class="sc5-section-head">
        <h2 id="{p}-realistic-title">Is this payment realistic?</h2>
        <p>Suggested payment levels for a {s["balance_label"]} balance—calibrate to your take-home pay.</p>
      </header>
      <div class="sc5-realistic-grid" id="{p}-realistic-grid"></div>
    </section>

    <section class="sc5-panel sc5-panel--related" id="{p}-related" aria-labelledby="{p}-related-title">
      <header class="sc5-section-head">
        <h2 id="{p}-related-title">Related calculators</h2>
      </header>
      <div class="sc5-related-grid">
        <a class="sc5-related-card" href="/debt/credit-cards/credit-card-payoff-calculator#payoff">
          <h3>Credit card payoff calculator</h3>
          <p>Year-by-year breakdown for any balance.</p>
        </a>
        <a class="sc5-related-card" href="/debt/payoff-scenarios/{s["related_slug"]}?from={s["from_tag"]}">
          <h3>{s["related_title"]}</h3>
          <p>{s["related_desc"]}</p>
        </a>
        <a class="sc5-related-card" href="/debt/credit-cards/payoff-under-5000">
          <h3>Small balances hub</h3>
          <p>Guides for debt under $5,000.</p>
        </a>
        <a class="sc5-related-card" href="/debt/payoff-scenarios">
          <h3>All payoff scenarios</h3>
          <p>Balances, traps, and strategies in one place.</p>
        </a>
      </div>
    </section>

    <section class="sc5-panel sc5-panel--faq" id="{p}-faq" aria-labelledby="{p}-faq-title">
      <header class="sc5-section-head">
        <h2 id="{p}-faq-title">Frequently asked questions</h2>
      </header>
      <div class="housing-hub-accordion faq-stack">
        <details class="housing-hub-accordion-item faq-item" open>
          <summary>How long does it take to pay off {s["balance_label"].lower()} debt?</summary>
          <p>{s["faq_timeline"]} Run your numbers in the planner above.</p>
        </details>
        <details class="housing-hub-accordion-item faq-item">
          <summary>How much interest will I pay?</summary>
          <p>Total interest is the sum of every finance charge until your balance hits zero. Bigger payments and a lower APR both cut it. See the comparison table above.</p>
        </details>
        <details class="housing-hub-accordion-item faq-item">
          <summary>What is a realistic payoff timeline?</summary>
          <p>{s["faq_realistic"]} Match your payment to your take-home pay after rent, food, and bills.</p>
        </details>
        <details class="housing-hub-accordion-item faq-item">
          <summary>Should I make extra payments?</summary>
          <p>Yes. Even a small bump cuts months off your payoff and saves real interest. Test scenarios in the "What if" section above.</p>
        </details>
      </div>
    </section>

    <section class="sc5-cta-panel" id="{p}-cta" aria-labelledby="{p}-cta-title">
      <h2 id="{p}-cta-title">Calculate your debt payoff timeline</h2>
      <p>Run any balance, APR, and payment in the full calculator—with year-by-year interest and principal.</p>
      <a class="sc5-btn sc5-btn--primary sc5-btn--lg" href="/debt/credit-cards/credit-card-payoff-calculator#payoff">Open payoff calculator</a>
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
          <a href="/debt/credit-cards/payoff-under-5000">Small balances guide</a>
          <a href="/debt/payoff-scenarios">Debt payoff scenarios</a>
          <a href="/debt/credit-cards/minimum-payment-calculator">Minimum payment calculator</a>
        </section>
        <section class="footer-column" aria-labelledby="footer-company">
          <h2 id="footer-company">Company</h2>
          <a href="/about">About</a>
          <a href="/editorial-policy">Editorial policy</a>
          <a href="/calculator-methodology">Calculator methodology</a>
          <a href="/methodology">Full methodology</a>
          <a href="/contact">Contact</a>
          <a href="/privacy-policy">Privacy Policy</a>
          <a href="/terms">Terms</a>
        </section>
      </div>
      <p class="footer-review" role="note"><time datetime="2026-06-01">Last reviewed: June 2026</time> · Reviewed by the <a href="/about">Income Clarity editorial team</a> · <a href="/editorial-policy">Editorial policy</a></p>
      <p class="footer-copy">© 2026 IncomeClarityLab</p>
    </div>
  </footer>

  <script src="/guide-back.js"></script>
  <script src="/debt-guide-back.js"></script>
  <script src="/debt/payoff-scenarios/payoff-scenario-engine.js"></script>
  <script src="/debt/payoff-scenarios/{s["js_file"]}"></script>
</body>
</html>
"""


def render_js(s: dict) -> str:
    cfg = JS_CONFIGS[s["prefix"]]
    return JS_TEMPLATE.format(
        prefix=s["prefix"],
        balance=s["balance"],
        default_payment=s["default_payment"],
        payment_table=str(cfg["payment_table"]),
        budget_boost=cfg["budget_boost"],
        what_if=fmt_what_if(cfg["what_if"]),
        realistic=fmt_realistic(cfg["realistic"]),
    )


def main() -> None:
    for s in SCENARIOS:
        html_path = OUT / s["slug"] / "index.html"
        js_path = OUT / s["js_file"]
        html_path.parent.mkdir(parents=True, exist_ok=True)
        html_path.write_text(render_html(s), encoding="utf-8")
        js_path.write_text(render_js(s), encoding="utf-8")
        print(f"Wrote {html_path.relative_to(ROOT)}")
        print(f"Wrote {js_path.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
