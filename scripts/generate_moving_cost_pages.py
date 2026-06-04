#!/usr/bin/env python3
"""Generate moving-cost-calculator hub, state, and city pages."""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from generate_col_by_city_pages import (  # noqa: E402
    CORE_GROSS_SHARE,
    STANDALONE,
    STATES,
    compare_links_for_path,
    prepare_city_metrics,
    validate_city_metrics,
)
from moving_cost_data import (  # noqa: E402
    BASE,
    COL_BY_STATE,
    COMFORT_SALARY_BY_STATE,
    COMFORT_SALARY_HUB,
    HOUSE_AFFORD_BY_STATE,
    TAKE_HOME_BY_STATE,
    build_catalog,
    catalog_json,
    city_moving_faqs,
    city_moving_tips,
    fmt,
    monthly_total,
    state_moving_faqs,
    state_moving_insights,
    state_moving_tips,
)

OUT = ROOT / "living" / "housing" / "moving-cost-calculator"

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


def head(title: str, desc: str, canonical: str, extra_script: str = "") -> str:
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
  <link rel="stylesheet" href="/styles-moving.css">
  <link rel="icon" type="image/png" href="/images/logo.png">
  <link rel="apple-touch-icon" href="/images/logo.png">
{URL_SCRIPT}
{extra_script}
</head>"""


def faq_html(faqs: list[tuple[str, str]]) -> str:
    blocks = []
    for q, a in faqs:
        paragraphs = "".join(f"<p>{part.strip()}</p>" for part in a.split("\n\n") if part.strip())
        blocks.append(f'          <article class="faq-item"><h3>{q}</h3>{paragraphs}</article>')
    return "\n".join(blocks)


HUB_FAQS = [
    (
        "How much does it cost to move to another state?",
        "Most interstate moves need $4,000 to $8,000 for movers and travel, plus $7,000 to $12,000 in upfront cash for deposits, rent, and setup. Large homes, long distances, and peak moving months can push totals higher.\n\nUse a range, not one fixed number. A move plan that survives a 15% cost surprise is usually much safer than a best-case-only budget.",
    ),
    (
        "How much money should I save before relocating?",
        "A strong baseline is three months of destination rent, full moving cost, and at least a $2,000 safety buffer. If your new job starts after move-in or income is variable, add another month of expenses.\n\nIf you carry debt, include one extra month of debt payments in your cash target so relocation does not trigger new credit card balances.",
    ),
    (
        "Is moving to Texas cheaper than California?",
        "Texas often has lower rent and no state income tax, which can improve take-home cash flow for many households. California can still make sense when salary upside and career growth are higher.\n\nCompare exact city pairs, not state averages. Dallas vs Los Angeles is a different budget than Austin vs San Diego.",
    ),
    (
        "Are professional movers worth it?",
        "Professional movers cost more up front, but they reduce labor stress, time loss, and damage risk on medium-to-long moves. They are often worth it when distance, stairs, or large furniture increase complexity.\n\nDIY or truck rental can be efficient for short moves and smaller homes, especially when you have flexible time and reliable help.",
    ),
    (
        "What hidden moving costs do people forget?",
        "Common misses include lease overlap, utility deposits, parking permits, furnishing basics, and higher renter or auto insurance in the new zip code.\n\nAnother frequent gap is monthly lifestyle drift: longer commute costs, higher grocery prices, and local tax differences can quietly reduce savings after move-in.",
    ),
]


def calc_block(default_from: str = "texas/dallas", default_to: str = "seattle") -> str:
    return f"""
        <div class="mc-calc-shell" id="mc-calculator">
          <div class="mc-calc-layout">
            <form id="mc-calc-form" class="mc-calc-form" aria-label="Moving cost calculator">
              <label class="mc-field"><span>Current city</span><select id="mc-from" required></select></label>
              <label class="mc-field"><span>Destination city</span><select id="mc-to" required></select></label>
              <label class="mc-field"><span>Move distance (miles)</span><input type="number" id="mc-distance" min="25" step="25" placeholder="Auto-estimate"></label>
              <label class="mc-field"><span>Home size</span>
                <select id="mc-size">
                  <option value="studio">Studio</option>
                  <option value="1br" selected>1 bedroom</option>
                  <option value="2br">2 bedroom</option>
                  <option value="3br">3+ bedroom</option>
                </select>
              </label>
              <label class="mc-field"><span>Moving type</span>
                <select id="mc-move-type">
                  <option value="diy">DIY</option>
                  <option value="truck" selected>Rental truck</option>
                  <option value="movers">Professional movers</option>
                </select>
              </label>
              <label class="mc-field"><span>Family size</span><input type="number" id="mc-family" min="1" max="8" value="2"></label>
              <div class="mc-checks">
                <label><input type="checkbox" id="mc-pets"> Pets</label>
                <label><input type="checkbox" id="mc-temp"> Temporary housing (about 1 week)</label>
                <label><input type="checkbox" id="mc-flights"> Flights for household</label>
                <label><input type="checkbox" id="mc-storage"> Storage unit</label>
                <label><input type="checkbox" id="mc-vehicle"> Vehicle transport</label>
              </div>
              <div class="mc-field mc-field--full">
                <button type="submit" class="mc-btn">Estimate Moving Costs</button>
              </div>
            </form>
            <div class="mc-results" aria-live="polite">
              <div class="mc-results-grid">
                <article class="mc-result-card"><p>Estimated moving cost</p><strong id="mc-move-range">$4,200–$6,100</strong></article>
                <article class="mc-result-card"><p>Immediate cash needed</p><strong id="mc-immediate">$8,900</strong></article>
                <article class="mc-result-card"><p>Monthly cost difference</p><strong id="mc-monthly-diff" class="mc-result-delta mc-result-delta--up">+$650/month</strong></article>
              </div>
              <p style="font-size:0.86rem;color:var(--mc-muted);margin:0.75rem 0 0">Immediate cash includes:</p>
              <ul class="mc-immediate-list" id="mc-immediate-list">
                <li>Deposits and first month rent</li>
                <li>Moving services</li>
                <li>Utility setup and essentials</li>
              </ul>
            </div>
          </div>
        </div>
        <script type="application/json" id="mc-catalog">{catalog_json()}</script>"""


def hub_sections() -> str:
    return """
    <section class="mc-band ra-band--alt">
      <div class="container container--wide">
        <header class="mc-band__head"><h2>Moving cost breakdown</h2><p>See the cost mix first, then open each category for details. The visual updates when you change inputs above.</p></header>
        <div class="mc-breakdown-visual" aria-live="polite">
          <div class="mc-mix-row"><div class="mc-mix-meta"><p>Moving services</p><span id="mc-mix-moving-value">$0</span><span id="mc-mix-moving-pct">0%</span></div><div class="mc-mix-track"><span class="mc-mix-fill mc-mix-fill--moving" id="mc-mix-moving-bar" style="width:0%"></span></div></div>
          <div class="mc-mix-row"><div class="mc-mix-meta"><p>Deposits &amp; first month</p><span id="mc-mix-deposits-value">$0</span><span id="mc-mix-deposits-pct">0%</span></div><div class="mc-mix-track"><span class="mc-mix-fill mc-mix-fill--deposits" id="mc-mix-deposits-bar" style="width:0%"></span></div></div>
          <div class="mc-mix-row"><div class="mc-mix-meta"><p>Travel</p><span id="mc-mix-travel-value">$0</span><span id="mc-mix-travel-pct">0%</span></div><div class="mc-mix-track"><span class="mc-mix-fill mc-mix-fill--travel" id="mc-mix-travel-bar" style="width:0%"></span></div></div>
          <div class="mc-mix-row"><div class="mc-mix-meta"><p>Utility setup</p><span id="mc-mix-util-value">$0</span><span id="mc-mix-util-pct">0%</span></div><div class="mc-mix-track"><span class="mc-mix-fill mc-mix-fill--util" id="mc-mix-util-bar" style="width:0%"></span></div></div>
          <div class="mc-mix-row"><div class="mc-mix-meta"><p>Furniture &amp; essentials</p><span id="mc-mix-furnish-value">$0</span><span id="mc-mix-furnish-pct">0%</span></div><div class="mc-mix-track"><span class="mc-mix-fill mc-mix-fill--furnish" id="mc-mix-furnish-bar" style="width:0%"></span></div></div>
          <div class="mc-mix-row"><div class="mc-mix-meta"><p>Temporary housing</p><span id="mc-mix-temp-value">$0</span><span id="mc-mix-temp-pct">0%</span></div><div class="mc-mix-track"><span class="mc-mix-fill mc-mix-fill--temp" id="mc-mix-temp-bar" style="width:0%"></span></div></div>
          <div class="mc-mix-row"><div class="mc-mix-meta"><p>Storage</p><span id="mc-mix-storage-value">$0</span><span id="mc-mix-storage-pct">0%</span></div><div class="mc-mix-track"><span class="mc-mix-fill mc-mix-fill--storage" id="mc-mix-storage-bar" style="width:0%"></span></div></div>
          <div class="mc-mix-row"><div class="mc-mix-meta"><p>Vehicle shipping</p><span id="mc-mix-vehicle-value">$0</span><span id="mc-mix-vehicle-pct">0%</span></div><div class="mc-mix-track"><span class="mc-mix-fill mc-mix-fill--vehicle" id="mc-mix-vehicle-bar" style="width:0%"></span></div></div>
        </div>
      </div>
    </section>

    <section class="mc-band">
      <div class="container container--wide">
        <header class="mc-band__head"><h2>City cost comparison</h2><p>See how monthly costs change when you relocate — not just moving day cash.</p></header>
        <div class="mc-grid-2">
          <article class="mc-card mc-compare-card">
            <div class="mc-compare-route">
              <div class="mc-compare-city"><p>From</p><strong id="mc-compare-from">Dallas</strong></div>
              <span class="mc-compare-arrow" aria-hidden="true">→</span>
              <div class="mc-compare-city"><p>To</p><strong id="mc-compare-to">Seattle</strong></div>
            </div>
            <div class="mc-compare-pill" id="mc-compare-net">Net monthly impact: —</div>
            <div class="mc-compare-row">
              <div class="mc-compare-row__top"><span>Rent difference</span><span id="mc-diff-rent">—</span></div>
              <div class="mc-compare-mini"><span class="mc-compare-mini__fill" id="mc-diff-rent-bar" style="width:0%"></span></div>
            </div>
            <div class="mc-compare-row">
              <div class="mc-compare-row__top"><span>Grocery difference</span><span id="mc-diff-gro">—</span></div>
              <div class="mc-compare-mini"><span class="mc-compare-mini__fill" id="mc-diff-gro-bar" style="width:0%"></span></div>
            </div>
            <div class="mc-compare-row">
              <div class="mc-compare-row__top"><span>Tax difference</span><span id="mc-diff-tax">—</span></div>
              <div class="mc-compare-mini"><span class="mc-compare-mini__fill" id="mc-diff-tax-bar" style="width:0%"></span></div>
            </div>
            <div class="mc-compare-row">
              <div class="mc-compare-row__top"><span>Transportation difference</span><span id="mc-diff-trans">—</span></div>
              <div class="mc-compare-mini"><span class="mc-compare-mini__fill" id="mc-diff-trans-bar" style="width:0%"></span></div>
            </div>
          </article>
          <article class="mc-card">
            <h3>Relocation intelligence</h3>
            <p>Great moves optimize two budgets: one-time cash and monthly lifestyle cost. This comparison highlights recurring pressure fast, so you can decide if salary upside truly beats cost-of-living drag.</p>
            <p>A quick rule: if monthly costs rise more than 8% of take-home pay, plan a larger emergency buffer before signing.</p>
            <p><a href="/living/housing/cost-of-living-by-city">Open cost of living by city →</a></p>
          </article>
        </div>
      </div>
    </section>

    <section class="mc-band mc-band--alt">
      <div class="container container--wide">
        <header class="mc-band__head"><h2>Can you afford this move?</h2><p>Turn your estimate into a yes/no plan with runway, monthly pressure, and next-step actions.</p></header>
        <div class="mc-afford-stepper" aria-label="Move readiness status">
          <div id="mc-step-ready" class="mc-afford-step">Ready</div>
          <div id="mc-step-almost" class="mc-afford-step">Almost ready</div>
          <div id="mc-step-notyet" class="mc-afford-step">Not yet</div>
        </div>
        <div class="mc-afford-layout">
          <form class="mc-calc-form mc-card" onsubmit="return false" aria-label="Move affordability check">
            <label class="mc-field"><span>Current city (affordability view)</span><select id="mc-afford-from"></select></label>
            <label class="mc-field"><span>Destination city (affordability view)</span><select id="mc-afford-to"></select></label>
            <label class="mc-field"><span>Annual salary ($)</span><input type="number" id="mc-salary" value="95000" step="1000"></label>
            <label class="mc-field"><span>Total savings available now ($)</span><input type="number" id="mc-savings" value="12000" step="500"></label>
            <label class="mc-field"><span>Monthly debt payments ($)</span><input type="number" id="mc-debt" value="400" step="25"></label>
            <label class="mc-field"><span>Emergency fund to keep untouched ($)</span><input type="number" id="mc-emergency" value="5000" step="500"></label>
            <label class="mc-field mc-field--full"><span>Minimum monthly savings goal after move ($)</span><input type="number" id="mc-save-goal" value="600" step="50"></label>
          </form>
          <article class="mc-card">
            <p>Move readiness <span class="mc-afford-badge" id="mc-afford-level">Moderate</span></p>
            <p id="mc-afford-note">Run the calculator to see your risk level.</p>
            <div class="mc-afford-kpis">
              <div class="mc-afford-kpi"><p>Cash left after move</p><strong id="mc-afford-cash-left">$0</strong></div>
              <div class="mc-afford-kpi"><p>Monthly leftover after fixed costs</p><strong id="mc-afford-monthly-left">$0</strong></div>
              <div class="mc-afford-kpi"><p>Runway if income is delayed</p><strong id="mc-afford-runway">0 months</strong></div>
              <div class="mc-afford-kpi"><p>Recommended total buffer</p><strong id="mc-afford-buffer">$0</strong></div>
            </div>
            <div class="mc-afford-meter">
              <div class="mc-afford-meter__row"><span>Buffer health</span><div class="mc-afford-meter__track"><span id="mc-afford-cash-meter" class="mc-afford-meter__fill" style="width:0%"></span></div></div>
              <div class="mc-afford-meter__row"><span>Runway strength</span><div class="mc-afford-meter__track"><span id="mc-afford-runway-meter" class="mc-afford-meter__fill" style="width:0%"></span></div></div>
            </div>
            <p id="mc-afford-save-hit">Monthly savings impact appears here after you estimate.</p>
            <ul class="mc-afford-actions">
              <li id="mc-afford-action-1">Set your move estimate to generate actions.</li>
              <li id="mc-afford-action-2">Keep at least one month of essential expenses uncommitted.</li>
              <li id="mc-afford-action-3">Validate rent and deposits before paying movers.</li>
            </ul>
          </article>
        </div>
      </div>
    </section>

    <section class="mc-band">
      <div class="container container--wide">
        <header class="mc-band__head"><h2>Hidden costs of moving</h2><p>These costs often do not appear in basic mover quotes. Planning them early improves cash confidence and lowers post-move stress.</p></header>
        <div class="mc-edu-grid mc-hidden-grid">
          <article class="mc-card mc-hidden-card"><h3>Lease overlap</h3><p>If move-out and move-in dates do not line up, you may pay two rents at once. Even 10 to 14 days can add a four-figure surprise in high-rent cities.</p><p class="mc-hidden-tip"><strong>Plan:</strong> Negotiate prorated days and set an overlap cap before signing.</p></article>
          <article class="mc-card mc-hidden-card"><h3>Utility deposits and connection fees</h3><p>Electric, gas, water, and internet can each require deposits or activation charges. New accounts and poor credit history usually increase upfront utility cash.</p><p class="mc-hidden-tip"><strong>Plan:</strong> Call providers two weeks early and list all setup fees in one checklist.</p></article>
          <article class="mc-card mc-hidden-card"><h3>Furnishing and setup costs</h3><p>Moving to a bigger or different layout often means replacing essentials: beds, curtains, shelving, small kitchen gear, and basic cleaning tools.</p><p class="mc-hidden-tip"><strong>Plan:</strong> Split setup into now/next/later purchases to protect cash flow.</p></article>
          <article class="mc-card mc-hidden-card"><h3>Parking, permits, and building rules</h3><p>Many urban buildings require loading windows, elevator reservations, or city parking permits for trucks. Missed rules can trigger fines or rescheduling costs.</p><p class="mc-hidden-tip"><strong>Plan:</strong> Confirm move-day logistics with both buildings in writing.</p></article>
          <article class="mc-card mc-hidden-card"><h3>Insurance changes</h3><p>Renter, auto, and even health plan costs can shift with ZIP code risk profiles. Coastal weather exposure or dense-city theft risk may raise premiums.</p><p class="mc-hidden-tip"><strong>Plan:</strong> Requote all policies before move day and compare bundles.</p></article>
          <article class="mc-card mc-hidden-card"><h3>Tax and commute drift</h3><p>A higher salary can still feel tighter if local tax, tolls, parking, or transit costs rise. Recurring monthly deltas can erode savings over the first year.</p><p class="mc-hidden-tip"><strong>Plan:</strong> Stress-test monthly budget impact for 12 months, not just move month.</p></article>
        </div>
      </div>
    </section>

    <section class="mc-band">
      <div class="container container--wide">
        <header class="mc-band__head"><h2>Moving planning tips before you sign a lease</h2><p>Use this checklist to reduce surprise costs and protect your monthly budget after move-in.</p></header>
        <div class="mc-tips-grid">
          <article class="mc-card mc-tip-card"><h3>Before you sign</h3><ul class="mc-tip-list">
            <li>Get written move-in and move-out dates, including prorated overlap days.</li>
            <li>Confirm elevator, loading zone, and parking permit rules with both buildings.</li>
            <li>Compare at least two mover quotes and one truck rental quote.</li>
            <li>Requote renter and auto insurance for the new ZIP code.</li>
          </ul></article>
          <article class="mc-card mc-tip-card"><h3>While packing</h3><ul class="mc-tip-list">
            <li>Label boxes by room to avoid duplicate purchases after move-in.</li>
            <li>Keep essentials in a carry-on bag for the first week.</li>
            <li>Photograph valuables before movers load the truck.</li>
            <li>Track utility setup fees in one shared checklist.</li>
          </ul></article>
          <article class="mc-card mc-tip-card"><h3>First 30 days after move</h3><ul class="mc-tip-list">
            <li>Delay non-essential furniture purchases until cash flow stabilizes.</li>
            <li>Review your first full month budget against your pre-move estimate.</li>
            <li>Adjust savings goals if monthly costs shifted more than expected.</li>
            <li>Keep one month of emergency cash untouched for surprises.</li>
          </ul></article>
        </div>
        <p class="mc-tip-note">Tip: Use the calculator above to test city pairs, move type, and home size before committing to a lease.</p>
      </div>
    </section>

    <section class="mc-band">
      <div class="container container--wide">
        <header class="mc-band__head"><h2>Real-life move scenarios</h2><p>Examples of how different households experience the same move math.</p></header>
        <div class="mc-real-grid">
          <article class="mc-card"><h3>Remote worker → Austin</h3><p>Lower rent vs many coastal cities. One-time move cost may pay back in 6–10 months of monthly savings.</p></article>
          <article class="mc-card"><h3>Family → San Diego</h3><p>Higher housing and childcare pressure. Needs a larger immediate cash buffer and longer savings runway.</p></article>
          <article class="mc-card"><h3>NYC → Chicago</h3><p>Often lower rent and different tax load. Still budget mover fees and winter setup costs.</p></article>
        </div>
      </div>
    </section>

    <section class="mc-band mc-band--alt">
      <div class="container container--wide">
        <header class="mc-band__head"><h2>How moving costs work</h2><p>Short guides to help you plan with cash flow, not just a mover quote.</p></header>
        <div class="mc-edu-grid">
          <article class="mc-card"><h3>How much savings before moving?</h3><p>Target three months of destination rent, full move cost, and a $2,000 cushion. Add more if income starts after move-in.</p></article>
          <article class="mc-card"><h3>Cheaper states to relocate to</h3><p>Texas, Florida, and parts of the South often have lower rent. Compare your job offer and tax impact city by city.</p></article>
          <article class="mc-card"><h3>Why housing drives relocation cost</h3><p>Rent and deposits are usually the largest line items. A $300 rent gap becomes $3,600 per year.</p></article>
          <article class="mc-card"><h3>Salary vs lower living costs</h3><p>A higher salary in an expensive city is not always better than a moderate salary where rent is lower.</p></article>
        </div>
      </div>
    </section>

    <section class="mc-band mc-band--alt">
      <div class="container container--wide">
        <header class="mc-band__head"><h2>Moving costs by state and city</h2><p>Open a state or metro page for local deposit norms, tax notes, and city-level estimates.</p></header>
        <div class="mc-city-grid">
          <a class="mc-city-card" href="/living/housing/moving-cost-calculator/california"><h3>California</h3><p>Deposits, taxes, and coastal vs inland rent gaps</p></a>
          <a class="mc-city-card" href="/living/housing/moving-cost-calculator/texas"><h3>Texas</h3><p>No state income tax with wide city spreads</p></a>
          <a class="mc-city-card" href="/living/housing/moving-cost-calculator/florida"><h3>Florida</h3><p>Coastal insurance and metro rent differences</p></a>
          <a class="mc-city-card" href="/living/housing/moving-cost-calculator/new-york"><h3>New York</h3><p>Downstate rent and tax pressure</p></a>
          <a class="mc-city-card" href="/living/housing/moving-cost-calculator/seattle"><h3>Seattle</h3><p>Pacific Northwest relocation costs</p></a>
          <a class="mc-city-card" href="/living/housing/moving-cost-calculator/chicago"><h3>Chicago</h3><p>Midwest mover and parking costs</p></a>
        </div>
      </div>
    </section>

    <section class="mc-band">
      <div class="container container--wide">
        <header class="mc-band__head"><h2>Related living decisions</h2></header>
        <div class="mc-tool-grid">
          <a class="mc-tool-card" href="/living/housing/cost-of-living-by-city"><h3>Cost of living by city</h3><p>Compare rent, groceries, tax, and salary targets.</p></a>
          <a class="mc-tool-card" href="/living/housing/how-much-rent-can-i-afford"><h3>Rent affordability</h3><p>Size rent after the move using take-home pay.</p></a>
          <a class="mc-tool-card" href="/living/lifestyle/comfortable-salary-us/"><h3>Comfortable salary by state</h3><p>Check income needed for your target lifestyle.</p></a>
          <a class="mc-tool-card" href="/rent-vs-buy-calculator"><h3>Rent vs buy calculator</h3><p>Compare staying renter vs buying in the new city.</p></a>
          <a class="mc-tool-card" href="/living/budgeting/average-monthly-expenses.html"><h3>Budgeting for relocation</h3><p>Plan monthly and one-time moving expenses.</p></a>
          <a class="mc-tool-card" href="/living/housing/how-much-house-can-i-afford"><h3>How much house can I afford</h3><p>Test buying if you plan to purchase after moving.</p></a>
        </div>
      </div>
    </section>

    <section class="mc-band mc-band--alt living-faq-section">
      <div class="container container--wide">
        <h2>Frequently asked questions</h2>
        <p class="living-faq-lead">Practical answers for US moves. Pair these with your own quotes and lease terms.</p>
        <div class="faq-stack">
""" + faq_html(HUB_FAQS) + """
        </div>
      </div>
    </section>

    <section class="mc-band">
      <div class="container container--wide">
        <div class="mc-cta-band">
          <h2>A better financial lifestyle might start with the right move</h2>
          <p>Compare another city, stress-test rent, and build a relocation budget you can actually follow.</p>
          <div class="mc-cta-actions">
            <a href="#mc-calculator">Compare another city</a>
            <a href="/living/housing/cost-of-living-by-city">Explore cost of living</a>
            <a href="/living/housing/how-much-rent-can-i-afford">Estimate housing affordability</a>
          </div>
        </div>
      </div>
    </section>"""


def footer_scripts(default_from: str = "texas/dallas", default_to: str = "seattle") -> str:
    return f"""{FOOTER}
  <script src="/moving-cost.js"></script>
  <script>MovingCost.bindForm({{ defaultFrom: '{default_from}', defaultTo: '{default_to}', runOnLoad: true }});</script>"""


def render_hub() -> str:
    faq_ld = json.dumps(
        {
            "@context": "https://schema.org",
            "@type": "FAQPage",
            "mainEntity": [
                {
                    "@type": "Question",
                    "name": q,
                    "acceptedAnswer": {"@type": "Answer", "text": a},
                }
                for q, a in HUB_FAQS
            ],
        },
        separators=(",", ":"),
    )
    schema = f"""  <script type="application/ld+json">
  {{"@context":"https://schema.org","@type":"WebApplication","name":"Moving Cost Calculator","applicationCategory":"FinanceApplication","operatingSystem":"Web","url":"https://www.incomeclaritylab.com/living/housing/moving-cost-calculator"}}
  </script>
  <script type="application/ld+json">
  {faq_ld}
  </script>"""
    body = f"""<body class="mc-page living-tool-page">
{HEADER}
  <main>
    <section class="mc-hero">
      <div class="container container--wide">
        <nav class="take-home-return-nav" aria-label="Breadcrumb">
          <ol class="take-home-return-breadcrumbs">
            <li><a href="/living/housing">Housing</a></li>
            <li aria-current="page">Moving cost calculator</li>
          </ol>
        </nav>
        <span class="label">Living · Relocation</span>
        <h1>Estimate the Real Cost of Moving to a New City</h1>
        <p class="lead">Calculate moving expenses, housing changes, transportation costs, and lifestyle impact before you relocate.</p>
{calc_block()}
      </div>
    </section>
{hub_sections()}
  </main>
{footer_scripts()}
</body>
</html>"""
    return head(
        "Moving Cost Calculator — Estimate Relocation Expenses | Income Clarity",
        "Estimate moving costs, upfront cash, and monthly lifestyle changes before you relocate. Compare cities, stress-test affordability, and plan hidden fees.",
        BASE,
        schema,
    ) + body


def mc_city_nav(state_slug: str, cities: dict, state_name: str) -> str:
    links = [
        f'<a class="mc-city-chip" href="{BASE}/{state_slug}/{cslug}">{c["name"]}</a>'
        for cslug, c in cities.items()
    ]
    chips = "\n          ".join(links)
    return f"""        <div class="mc-city-nav" aria-label="Cities in {state_name}">
          <p class="mc-city-nav__label">Explore by city</p>
          <div class="mc-city-chips">{chips}</div>
        </div>"""


def take_home_href(state_slug: str) -> str:
    return TAKE_HOME_BY_STATE.get(state_slug, "/hourly-to-salary-after-tax")


def col_path_for_interlinks(state_slug: str, city_slug: str, standalone: bool) -> str:
    if standalone:
        return f"/living/housing/cost-of-living-by-city/{city_slug}"
    return f"/living/housing/cost-of-living-by-city/{state_slug}/{city_slug}"


def state_city_compare_section(state_slug: str, st: dict) -> str:
    name = st["name"]
    cities_sorted = sorted(st["cities"].items(), key=lambda item: item[1]["rent_1br"])
    max_rent = max(c["rent_1br"] for _, c in cities_sorted) or 1
    cards = []
    n = len(cities_sorted)
    for i, (cslug, c) in enumerate(cities_sorted):
        monthly = monthly_total(c)
        bar_pct = max(12, int(round(c["rent_1br"] / max_rent * 100)))
        badge = ""
        if n > 1 and i == 0:
            badge = '<span class="mc-city-compare-badge mc-city-compare-badge--low">Lowest rent</span>'
        elif n > 1 and i == n - 1:
            badge = '<span class="mc-city-compare-badge mc-city-compare-badge--high">Highest rent</span>'
        cards.append(
            f"""          <a class="mc-city-compare-card" href="{BASE}/{state_slug}/{cslug}">
            <div class="mc-city-compare-card__head">
              <h3>{c["name"]}</h3>
              {badge}
            </div>
            <div class="mc-city-compare-metrics">
              <div><span class="mc-city-compare-metrics__label">1BR rent</span><strong>{fmt(c["rent_1br"])}</strong></div>
              <div><span class="mc-city-compare-metrics__label">Essentials</span><strong>{fmt(monthly)}</strong></div>
              <div><span class="mc-city-compare-metrics__label">COL index</span><strong>{c.get("col_index", "—")}</strong></div>
              <div><span class="mc-city-compare-metrics__label">Comfort salary</span><strong>{fmt(c.get("salary_comfort", 0))}</strong></div>
            </div>
            <div class="mc-city-compare-bar" aria-hidden="true"><span style="width:{bar_pct}%"></span></div>
            <p class="mc-city-compare-cta">View moving estimate <span aria-hidden="true">→</span></p>
          </a>"""
        )
    cards_html = "\n".join(cards)
    take_home = take_home_href(state_slug)
    return f"""        <div class="mc-city-compare-panel">
          <header class="mc-city-compare-panel__head">
            <h3 class="mc-band__subhead">Compare {name} cities</h3>
            <p>Sorted by typical 1-bedroom rent. Open a city for mover fees, deposits, and monthly cost change vs your current home.</p>
          </header>
          <div class="mc-city-compare-grid">
{cards_html}
          </div>
          <p class="mc-city-compare-foot">Pair city rent with <a href="{take_home}">{name} take-home pay</a> before you sign a lease.</p>
        </div>"""


def mc_methodology_block(
    place_name: str,
    data: dict,
    metrics: dict,
    tax_note: str,
    *,
    include_move_math: bool = True,
) -> str:
    move_math = ""
    if include_move_math:
        move_math = """
          <article class="mc-method-card">
            <h3>Move-day cost model</h3>
            <p>Moving services use base fee + per-mile rate by type (DIY, rental truck, professional movers), scaled by home size. Immediate cash adds deposits (about 1.5× destination rent), first month rent, utility setup, travel, and optional storage or vehicle shipping.</p>
          </article>"""
    lifestyle = data.get("lifestyle_score")
    score_line = (
        f"Model affordability signal: <strong>{metrics['derived_score']}/100</strong> (page score {lifestyle}/100)."
        if lifestyle is not None
        else f"Model affordability signal: <strong>{metrics['derived_score']}/100</strong>."
    )
    return f"""
    <section class="mc-band mc-band--alt">
      <div class="container container--wide content-page">
        <header class="mc-band__head"><h2>How we calculate {place_name} moving numbers</h2><p>Auditable planning math for move-day cash and monthly budget changes.</p></header>
        <div class="mc-method-grid">
{move_math}
          <article class="mc-method-card">
            <h3>Monthly essentials at destination</h3>
            <p>Rent {fmt(data['rent_1br'])} + groceries {fmt(data.get('groceries', 400))} + utilities {fmt(data.get('utilities', 200))} + transport {fmt(data.get('transport', 350))} + local tax estimate {fmt(data.get('taxes_month', 180))} = <strong>{fmt(monthly_total(data))}/mo</strong>.</p>
          </article>
          <article class="mc-method-card">
            <h3>Comfort salary cross-check</h3>
            <p>Annual core ({fmt(metrics['core'] * 12)}) ÷ {int(CORE_GROSS_SHARE * 100)}% gross share ≈ <strong>{fmt(metrics['min_salary'])}</strong>. Published target: {fmt(data.get('salary_comfort', metrics['min_salary']))}.</p>
          </article>
          <article class="mc-method-card">
            <h3>Affordability signal</h3>
            <p>{score_line} Tax note: {tax_note}</p>
          </article>
        </div>
      </div>
    </section>"""


def mc_planning_block(
    place_name: str,
    take_home: str,
    col_path: str,
    rent_link: str,
    house_href: str | None,
    moving_hub: str,
    salary_link: str | None,
    compare_links: list[tuple[str, str]],
) -> str:
    compare_html = ""
    if compare_links:
        items = " · ".join(f'<a href="{href}">{label}</a>' for label, href in compare_links[:3])
        compare_html = f"""
          <p>Compare destination economics head-to-head: {items}.</p>"""
    house_line = (
        f'<p>Before signing, pressure-test buying with <a href="{house_href}">house affordability in {place_name}</a> and the <a href="/rent-vs-buy-calculator">rent vs buy calculator</a>.</p>'
        if house_href
        else '<p>Before signing, compare renting vs buying with the <a href="/rent-vs-buy-calculator">rent vs buy calculator</a>.</p>'
    )
    salary_line = (
        f'<p>Layer income targets using the <a href="{salary_link}">comfortable salary guide</a> and <a href="/living/lifestyle-family/family-of-4-income-guide/">family of 4 income guide</a>.</p>'
        if salary_link
        else f'<p>Layer income targets using the <a href="/living/lifestyle/comfortable-salary-us/">comfortable salary guide</a> and <a href="/living/lifestyle-family/family-of-4-income-guide/">family of 4 income guide</a>.</p>'
    )
    return f"""
    <section class="mc-band">
      <div class="container container--wide content-page">
        <header class="mc-band__head"><h2>Plan your move to {place_name} in order</h2><p>Use this sequence so move-day cash and month-two bills stay aligned.</p></header>
        <div class="mc-context-links">
          <p>Step 1: Run the calculator above with your current city as origin and {place_name} as destination. Save both <strong>estimated moving cost</strong> and <strong>immediate cash needed</strong>.</p>
          <p>Step 2: Convert your offer to net pay in the <a href="{take_home}">take-home calculator</a>, then set a rent cap in the <a href="{rent_link}">rent affordability calculator</a>.</p>
          <p>Step 3: Open the <a href="{col_path}">cost of living guide for {place_name}</a> to validate groceries, utilities, and salary targets against this move estimate.</p>
{compare_html}
{house_line}
{salary_line}
          <p>Return to the <a href="{moving_hub}">US moving cost calculator</a> any time you change origin city, home size, or move type.</p>
        </div>
      </div>
    </section>"""


def mc_eeat_block(place_name: str) -> str:
    slug = place_name.lower().replace(" ", "-")
    return f"""
    <section class="mc-eeat">
      <div class="container container--wide content-page">
        <p class="mc-disclaimer">Educational content for US readers only, not financial or legal advice. Verify quotes with movers, landlords, and your pay stubs.</p>
        <aside class="eeat-trust" aria-labelledby="eeat-mc-{slug}-title">
          <header class="eeat-trust__header">
            <span class="eeat-trust__kicker">How we built this</span>
            <h2 id="eeat-mc-{slug}-title" class="eeat-trust__title">{place_name} Moving Cost Methodology &amp; Data Sources</h2>
            <p class="eeat-trust__meta"><time datetime="2026-05-30">Last reviewed: May 30, 2026</time> · Reviewed by the Income Clarity editorial team · <a href="/methodology#affordability">Read the full methodology</a></p>
          </header>
          <div class="eeat-trust__grid">
            <article class="eeat-trust__card">
              <h3>How we estimate moving costs</h3>
              <ul>
                <li><strong>Move services:</strong> base + per-mile rate by move type, adjusted for home size.</li>
                <li><strong>Immediate cash:</strong> deposits, first month rent, move services, setup, travel, and optional add-ons.</li>
                <li><strong>Monthly change:</strong> destination monthly bundle minus origin monthly bundle.</li>
                <li><strong>Monthly bundle:</strong> rent, groceries, utilities, transport, and a tax estimate line.</li>
              </ul>
            </article>
            <article class="eeat-trust__card">
              <h3>Primary data sources</h3>
              <ul>
                <li><a href="https://www.zillow.com/research/data/" rel="noopener noreferrer">Zillow Research (ZORI)</a> — metro rent medians.</li>
                <li><a href="https://www.huduser.gov/portal/datasets/fmr.html" rel="noopener noreferrer">HUD Fair Market Rents</a> — regional rent benchmarks.</li>
                <li><a href="https://www.bls.gov/cpi/" rel="noopener noreferrer">BLS CPI</a> — food, utilities, and transport inflation context.</li>
                <li><a href="https://www.census.gov/data/developers/data-sets/acs-5year.html" rel="noopener noreferrer">Census ACS</a> — household income and spending patterns.</li>
              </ul>
            </article>
            <article class="eeat-trust__card">
              <h3>What this is not</h3>
              <p>These are planning ranges, not mover contracts or landlord approvals. Final quotes can differ by season, stairs, insurance, and local fees.</p>
            </article>
          </div>
          <p class="eeat-trust__footer">See a mismatch with your move quote? <a href="/contact">Tell us</a> — we fix confirmed errors within 7 days.</p>
        </aside>
      </div>
    </section>"""


def mc_city_interlink_block(current_path: str, place_name: str) -> str:
    links: list[tuple[str, str]] = []
    for state_slug, st in STATES.items():
        for c_slug, c in st["cities"].items():
            path = f"{BASE}/{state_slug}/{c_slug}"
            if path != current_path:
                links.append((c["name"], path))
    for c_slug, c in STANDALONE.items():
        path = f"{BASE}/{c_slug}"
        if path != current_path:
            links.append((c["name"], path))
    links.sort(key=lambda x: x[0])
    chips = "\n          ".join(
        f'<a class="mc-city-chip" href="{href}">{label}</a>' for label, href in links
    )
    return f"""
    <section class="mc-band">
      <div class="container container--wide">
        <header class="mc-band__head"><h2>Compare moving costs in other cities</h2><p>Open another destination guide to compare deposits, mover fees, and monthly budget shifts.</p></header>
        <div class="mc-city-chips mc-city-chips--light">
          {chips}
        </div>
      </div>
    </section>"""


def mc_state_interlink_block(current_slug: str) -> str:
    links: list[tuple[str, str]] = []
    for slug, st in STATES.items():
        if slug != current_slug:
            links.append((st["name"], f"{BASE}/{slug}"))
    for slug, c in STANDALONE.items():
        links.append((c["name"], f"{BASE}/{slug}"))
    chips = "\n          ".join(
        f'<a class="mc-city-chip" href="{href}">{label}</a>' for label, href in links
    )
    return f"""
    <section class="mc-band">
      <div class="container container--wide">
        <header class="mc-band__head"><h2>Explore moving costs in other states and metros</h2><p>Switch destination context without losing your planning workflow.</p></header>
        <div class="mc-city-chips mc-city-chips--light">
          {chips}
        </div>
      </div>
    </section>"""


def page_tool_interlinks(
    state_slug: str,
    state_name: str,
    *,
    city_name: str | None = None,
    city: dict | None = None,
    col_path: str | None = None,
    standalone: bool = False,
    compare_links: list[tuple[str, str]] | None = None,
) -> str:
    take_home = take_home_href(state_slug)
    if state_slug in TAKE_HOME_BY_STATE:
        take_home_label = f"{state_name} take-home pay calculator"
    elif state_slug in STATES:
        take_home_label = f"{state_name} take-home pay calculator"
    else:
        take_home_label = "Take-home pay calculator"

    col_href = col_path or COL_BY_STATE.get(
        state_slug, "/living/housing/cost-of-living-by-city"
    )
    col_label = (
        f"Cost of living in {city_name}"
        if city_name
        else f"Cost of living in {state_name}"
    )

    house_href = None
    house_label = "How much house can I afford"
    if city and city.get("house_link"):
        house_href = city["house_link"]
        house_label = f"House affordability in {city_name}"
    elif state_slug in HOUSE_AFFORD_BY_STATE:
        house_href = HOUSE_AFFORD_BY_STATE[state_slug]
        house_label = f"House affordability in {state_name}"

    tools = [
        (
            take_home,
            take_home_label,
            "Convert gross offers to net pay after state and local tax.",
        ),
        (
            "/living/housing/how-much-rent-can-i-afford",
            "Rent affordability calculator",
            "Cap rent using take-home pay after the move.",
        ),
        (col_href, col_label, "Rent, groceries, utilities, and salary targets."),
        (
            "/rent-vs-buy-calculator",
            "Rent vs buy calculator",
            "Compare staying a renter vs buying in the new city.",
        ),
        (
            BASE,
            "US moving cost calculator",
            "Change origin/destination cities and move type.",
        ),
        (
            "/living/budgeting/average-monthly-expenses.html",
            "Monthly expenses guide",
            "Budget buckets for the first year after moving.",
        ),
    ]
    if house_href:
        tools.insert(
            3,
            (
                house_href,
                house_label,
                "Test buying if you plan to purchase after relocating.",
            ),
        )
    comfort = COMFORT_SALARY_BY_STATE.get(state_slug)
    if comfort:
        tools.append(
            (
                comfort,
                f"Comfortable salary in {state_name}",
                "Income targets with state tax framing.",
            )
        )

    cards = []
    for href, title, desc in tools:
        cards.append(
            f'          <a class="mc-tool-card" href="{href}"><h3>{title}</h3><p>{desc}</p></a>'
        )
    heading = (
        f"Related tools for your {city_name} move"
        if city_name
        else f"Related tools for your {state_name} move"
    )
    compare_html = ""
    if compare_links:
        items = " · ".join(f'<a href="{href}">{label}</a>' for label, href in compare_links[:3])
        compare_html = f"""
        <p class="mc-related-links">City comparison guides: {items}</p>"""
    return f"""    <section class="mc-band">
      <div class="container container--wide">
        <header class="mc-band__head"><h2>{heading}</h2><p>Run take-home pay and housing calculators with the same cities you used above.</p></header>
{compare_html}
        <div class="mc-tool-grid">
{chr(10).join(cards)}
        </div>
      </div>
    </section>"""


def recommendations_html(tips: list[tuple[str, list[str]]]) -> str:
    cards = []
    for title, bullets in tips:
        items = "\n".join(f"            <li>{b}</li>" for b in bullets)
        cards.append(
            f"""          <article class="mc-rec-card">
            <h3>{title}</h3>
            <ul class="mc-rec-list">{items}
            </ul>
          </article>"""
        )
    return "\n".join(cards)


def state_insights_html(state_slug: str, st: dict, take_home: str) -> str:
    data = state_moving_insights(state_slug, st)
    name = st["name"]
    take_home_label = f"{name} take-home calculator"
    take_home_link = f'<a href="{take_home}">{take_home_label}</a>'
    cards = []
    for i, item in enumerate(data["insights"], start=1):
        body = item["body"].format(take_home_link=take_home_link)
        cards.append(
            f"""          <article class="mc-insight-card">
            <span class="mc-insight-card__num" aria-hidden="true">{i}</span>
            <div class="mc-insight-card__body">
              <h3>{item["title"]}</h3>
              <p>{body}</p>
            </div>
          </article>"""
        )
    return f"""        <div class="mc-insights">
          <h3 class="mc-insights__heading">What to know before you move</h3>
          <div class="mc-insights-grid">
{chr(10).join(cards)}
          </div>
        </div>"""


def state_changes_section(state_slug: str, st: dict) -> str:
    name = st["name"]
    insight_data = state_moving_insights(state_slug, st)
    intro = insight_data["intro"]
    rank = st.get("rank_intro", "")
    take_home = take_home_href(state_slug)
    insights_block = state_insights_html(state_slug, st, take_home)
    return f"""    <section class="mc-band mc-band--alt">
      <div class="container container--wide content-page">
        <header class="mc-band__head"><h2>What changes when you move to {name}</h2><p>{rank or f"Rent, tax, and setup costs vary widely across {name} metros."}</p></header>
        <p class="mc-state-intro">{intro}</p>
        <div class="mc-state-stats" role="list">
          <div class="mc-state-stat" role="listitem"><strong>{fmt(st["rent_1br"])}</strong><span>Typical 1BR rent (state median)</span></div>
          <div class="mc-state-stat" role="listitem"><strong>{fmt(monthly_total(st))}</strong><span>Monthly essentials estimate</span></div>
          <div class="mc-state-stat" role="listitem"><strong>{st["col_index"]}</strong><span>Cost-of-living index (US = 100)</span></div>
          <div class="mc-state-stat" role="listitem"><strong>{fmt(st["salary_comfort"])}</strong><span>Comfort salary target (gross)</span></div>
        </div>
{insights_block}
        <aside class="mc-tax-callout" role="note">
          <p class="mc-tax-callout__label">Tax &amp; take-home</p>
          <p><strong>{st.get("tax_note", "State and local taxes affect take-home pay.")}</strong> — <a href="{take_home}">Calculate {name} take-home pay</a> with your offer letter before you compare rent caps.</p>
        </aside>
{state_city_compare_section(state_slug, st)}
      </div>
    </section>"""


def state_recommendations_section(state_name: str, state_slug: str) -> str:
    return f"""    <section class="mc-band mc-rec-band">
      <div class="container container--wide">
        <header class="mc-band__head"><h2>Relocation recommendations for {state_name}</h2><p>Practical steps to lower surprise costs and protect cash flow after move-in.</p></header>
        <div class="mc-rec-grid">
{recommendations_html(state_moving_tips(state_name, state_slug))}
        </div>
      </div>
    </section>"""


def city_snapshot_section(
    state_slug: str, city_slug: str, st: dict, c: dict, *, standalone: bool = False
) -> str:
    name = c["name"]
    state_name = st["name"] if not standalone else c.get("state_name", "US")
    monthly = monthly_total(c)
    col_path = (
        f"/living/housing/cost-of-living-by-city/{state_slug}/{city_slug}"
        if not standalone
        else f"/living/housing/cost-of-living-by-city/{city_slug}"
    )
    parking = (
        "Budget parking permits, garage fees, or transit passes in dense neighborhoods."
        if name in ("Los Angeles", "New York City", "San Francisco", "Chicago")
        else "Include commute fuel, tolls, or transit in your monthly plan — not just rent."
    )
    return f"""    <section class="mc-band mc-band--alt">
      <div class="container container--wide content-page">
        <header class="mc-band__head"><h2>{name} relocation costs at a glance</h2><p>Typical monthly planning figures for singles and couples — adjust for family size and neighborhood.</p></header>
        <div class="mc-state-stats" role="list">
          <div class="mc-state-stat" role="listitem"><strong>{fmt(c["rent_1br"])}</strong><span>Typical 1BR rent</span></div>
          <div class="mc-state-stat" role="listitem"><strong>{fmt(monthly)}</strong><span>Monthly essentials</span></div>
          <div class="mc-state-stat" role="listitem"><strong>{c.get("col_index", st.get("col_index", 100))}</strong><span>COL index (US = 100)</span></div>
          <div class="mc-state-stat" role="listitem"><strong>{fmt(c.get("salary_comfort", st.get("salary_comfort", 80000)))}</strong><span>Comfort salary (gross)</span></div>
        </div>
        <div class="mc-insights">
          <h3 class="mc-insights__heading">{name} budget checkpoints</h3>
          <div class="mc-insights-grid">
            <article class="mc-insight-card">
              <span class="mc-insight-card__num" aria-hidden="true">1</span>
              <div class="mc-insight-card__body">
                <h3>Transportation and parking first</h3>
                <p>{parking} Include this in your monthly budget before locking your rent target.</p>
              </div>
            </article>
            <article class="mc-insight-card">
              <span class="mc-insight-card__num" aria-hidden="true">2</span>
              <div class="mc-insight-card__body">
                <h3>Anchor your core monthly baseline</h3>
                <p>Groceries near {fmt(c.get("groceries", 400))}/mo and utilities near {fmt(c.get("utilities", 200))}/mo in this model. Add debt, childcare, and insurance to personalize your real monthly number.</p>
              </div>
            </article>
            <article class="mc-insight-card">
              <span class="mc-insight-card__num" aria-hidden="true">3</span>
              <div class="mc-insight-card__body">
                <h3>Family-income planning matters</h3>
                <p>Family of four planning often needs near {fmt(c.get("family_4", c.get("salary_comfort", st.get("salary_comfort", 80000))))} gross depending on childcare and debt. Use take-home pay to pressure-test that target before moving.</p>
              </div>
            </article>
          </div>
        </div>
        <aside class="what-this-means" role="note">
          <p class="what-this-means__title">What this means for you</p>
          <p>Use the calculator above with your origin city selected. If immediate cash or monthly difference looks tight, compare a nearby suburb or another {state_name} city before signing.</p>
        </aside>
      </div>
    </section>"""


def city_recommendations_section(city_name: str, state_name: str) -> str:
    return f"""    <section class="mc-band mc-rec-band">
      <div class="container container--wide">
        <header class="mc-band__head"><h2>Tips for moving to {city_name}</h2><p>Checklist-style guidance to pair with your estimate above.</p></header>
        <div class="mc-rec-grid">
{recommendations_html(city_moving_tips(city_name, state_name))}
        </div>
      </div>
    </section>"""


def render_state(state_slug: str, st: dict) -> str:
    name = st["name"]
    canonical = f"{BASE}/{state_slug}"
    avg_rent = st["rent_1br"]
    monthly = monthly_total(st)
    metrics = prepare_city_metrics(st)
    faqs = state_moving_faqs(name)
    city_nav = mc_city_nav(state_slug, st["cities"], name)
    take_home = take_home_href(state_slug)
    col_path = COL_BY_STATE.get(state_slug, "/living/housing/cost-of-living-by-city")
    house_href = HOUSE_AFFORD_BY_STATE.get(state_slug)
    salary_link = COMFORT_SALARY_BY_STATE.get(state_slug, COMFORT_SALARY_HUB)
    compare_links: list[tuple[str, str]] = [
        ("California vs Texas", "/living/cost-of-living/cost-of-living-california-vs-texas.html")
    ]
    for cs, _c in st["cities"].items():
        col_path_city = f"{state_slug}/{cs}"
        for link in compare_links_for_path(f"/living/housing/cost-of-living-by-city/{col_path_city}"):
            if link not in compare_links:
                compare_links.append(link)
    extra = f"""  <script src="/moving-cost.js"></script>
  <script>document.addEventListener('DOMContentLoaded',function(){{MovingCost.bindForm({{defaultTo:'{state_slug}/{next(iter(st["cities"]))}',runOnLoad:true}});}});</script>"""

    body = f"""<body class="mc-page living-tool-page">
{HEADER}
  <main>
    <section class="mc-hero">
      <div class="container container--wide">
        <nav class="take-home-return-nav" aria-label="Breadcrumb">
          <ol class="take-home-return-breadcrumbs">
            <li><a href="{BASE}">Moving cost calculator</a></li>
            <li aria-current="page">{name}</li>
          </ol>
        </nav>
        <span class="label">Living · {name}</span>
        <h1>Average Moving Costs in {name}</h1>
        <p class="lead">Plan deposits, mover fees, and monthly cost changes before you move to {name}. Typical one-bedroom rent runs about {fmt(avg_rent)}. Total monthly essentials often land near {fmt(monthly)}.</p>
{calc_block(default_from="texas/dallas", default_to=f"{state_slug}/{next(iter(st['cities']))}")}
{city_nav}
      </div>
    </section>
{state_changes_section(state_slug, st)}
{state_recommendations_section(name, state_slug)}
{mc_state_interlink_block(state_slug)}
{mc_planning_block(name, take_home, col_path, "/living/housing/how-much-rent-can-i-afford", house_href, BASE, salary_link, compare_links[:4])}
{mc_methodology_block(name, st, metrics, st.get("tax_note", "Tax varies by location."))}
{page_tool_interlinks(state_slug, name, compare_links=compare_links[:4])}
    <section class="mc-band living-faq-section">
      <div class="container container--wide">
        <h2>FAQ — moving to {name}</h2>
        <div class="faq-stack">{faq_html(faqs)}</div>
      </div>
    </section>
{mc_eeat_block(name)}
  </main>
{FOOTER}
{extra}
</body></html>"""
    return head(
        f"Moving Cost Calculator for {name} | Income Clarity",
        f"Estimate moving costs, deposits, and monthly budget changes when relocating to {name}. Compare top cities and plan upfront cash.",
        canonical,
    ) + body


def render_city(state_slug: str, city_slug: str, st: dict, c: dict, *, standalone: bool = False) -> str:
    name = c["name"]
    state_name = st["name"] if not standalone else c.get("state_name", "US")
    cid = f"{state_slug}/{city_slug}" if not standalone else city_slug
    canonical = f"{BASE}/{city_slug}" if standalone else f"{BASE}/{state_slug}/{city_slug}"
    state_bc = (
        f'<li><a href="{BASE}/{state_slug}">{state_name}</a></li>' if not standalone else ""
    )
    faqs = city_moving_faqs(name, state_name)
    col_path = col_path_for_interlinks(state_slug, city_slug, standalone)
    metrics = prepare_city_metrics(c)
    take_home = take_home_href(state_slug if not standalone else city_slug)
    tax_note = st.get("tax_note", c.get("tax_note", "Tax varies by location.")) if not standalone else c.get("tax_note", "Tax varies by location.")
    house_href = c.get("house_link") or HOUSE_AFFORD_BY_STATE.get(state_slug if not standalone else "")
    salary_link = c.get("salary_link") or COMFORT_SALARY_BY_STATE.get(state_slug if not standalone else "", COMFORT_SALARY_HUB)
    col_page_path = f"{state_slug}/{city_slug}" if not standalone else city_slug
    compare_links = compare_links_for_path(f"/living/housing/cost-of-living-by-city/{col_page_path}")
    current_mc_path = canonical

    body = f"""<body class="mc-page living-tool-page">
{HEADER}
  <main>
    <section class="mc-hero">
      <div class="container container--wide">
        <nav class="take-home-return-nav" aria-label="Breadcrumb">
          <ol class="take-home-return-breadcrumbs">
            <li><a href="{BASE}">Moving cost calculator</a></li>
            {state_bc}
            <li aria-current="page">{name}</li>
          </ol>
        </nav>
        <span class="label">Living · {name}</span>
        <h1>Moving Cost Calculator for {name}</h1>
        <p class="lead">Estimate mover fees, deposits, utilities, and rent changes for {name}. Typical one-bedroom rent is about {fmt(c["rent_1br"])}. Use the calculator to compare your current city against {name}.</p>
{calc_block(default_from="texas/dallas", default_to=cid)}
      </div>
    </section>
{city_snapshot_section(state_slug, city_slug, st, c, standalone=standalone)}
{city_recommendations_section(name, state_name)}
{mc_city_interlink_block(current_mc_path, name)}
{mc_planning_block(name, take_home, col_path, c.get("rent_link", "/living/housing/how-much-rent-can-i-afford"), house_href, BASE, salary_link, compare_links)}
{mc_methodology_block(name, c, metrics, tax_note)}
{page_tool_interlinks(state_slug if not standalone else city_slug, state_name, city_name=name, city=c, col_path=col_path, standalone=standalone, compare_links=compare_links)}
    <section class="mc-band living-faq-section">
      <div class="container container--wide">
        <h2>FAQ — moving to {name}</h2>
        <div class="faq-stack">{faq_html(faqs)}</div>
      </div>
    </section>
{mc_eeat_block(name)}
  </main>
{FOOTER}
  <script src="/moving-cost.js"></script>
  <script>document.addEventListener('DOMContentLoaded',function(){{MovingCost.bindForm({{defaultTo:'{cid}',runOnLoad:true}});}});</script>
</body></html>"""
    body = body.replace(
        f"/living/housing/cost-of-living-by-city/{state_slug}/{city_slug if state_slug in STATES else city_slug}",
        col_path,
    )
    return head(
        f"Moving Cost Calculator for {name} | Income Clarity",
        f"Plan moving costs for {name}: deposits, movers, utilities, transportation, and monthly rent changes before you relocate.",
        canonical,
    ) + body


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "index.html").write_text(render_hub(), encoding="utf-8")
    print("Wrote hub", OUT / "index.html")

    for state_slug, st in STATES.items():
        state_dir = OUT / state_slug
        state_dir.mkdir(parents=True, exist_ok=True)
        (state_dir / "index.html").write_text(render_state(state_slug, st), encoding="utf-8")
        print("Wrote state", state_dir / "index.html")
        for city_slug, c in st["cities"].items():
            city_dir = state_dir / city_slug
            city_dir.mkdir(parents=True, exist_ok=True)
            (city_dir / "index.html").write_text(
                render_city(state_slug, city_slug, st, c), encoding="utf-8"
            )
            print("Wrote city", city_dir / "index.html")

    for slug, c in STANDALONE.items():
        city_dir = OUT / slug
        city_dir.mkdir(parents=True, exist_ok=True)
        pseudo = {"name": c.get("state_name", ""), "col_index": c["col_index"], "rent_1br": c["rent_1br"]}
        (city_dir / "index.html").write_text(
            render_city(slug, slug, pseudo, c, standalone=True), encoding="utf-8"
        )
        print("Wrote metro", city_dir / "index.html")

    metric_warnings: list[str] = []
    catalog = build_catalog()
    for state_slug, st in STATES.items():
        metric_warnings.extend(validate_city_metrics(st, f"mc/state/{state_slug}"))
        for cs, c in st["cities"].items():
            metric_warnings.extend(validate_city_metrics(c, f"mc/{state_slug}/{cs}"))
            entry = next((x for x in catalog if x["id"] == f"{state_slug}/{cs}"), None)
            if entry and entry["rent"] != c["rent_1br"]:
                metric_warnings.append(
                    f"mc/{state_slug}/{cs}: catalog rent {entry['rent']} != data rent {c['rent_1br']}"
                )
    for slug, c in STANDALONE.items():
        city = {k: v for k, v in c.items() if k not in ("state_name", "tax_note")}
        metric_warnings.extend(validate_city_metrics(city, f"mc/{slug}"))
        entry = next((x for x in catalog if x["id"] == slug), None)
        if entry and entry["rent"] != c["rent_1br"]:
            metric_warnings.append(
                f"mc/{slug}: catalog rent {entry['rent']} != data rent {c['rent_1br']}"
            )
    if metric_warnings:
        print("METRIC WARNINGS:")
        for w in metric_warnings:
            print(" ", w)
    else:
        print("All moving pages pass metric validation checks")


if __name__ == "__main__":
    main()
