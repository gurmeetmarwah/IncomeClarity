#!/usr/bin/env python3
"""Generate /debt/credit-cards cluster pages and _redirects entries."""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
HUB = "debt/credit-cards"
HUB_URL = "/debt/credit-cards"
HUB_TITLE = "Credit cards"

PAGE_TEMPLATE = '''<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title} | Income Clarity</title>
  <meta name="description" content="{description}">
  <meta property="og:type" content="website">
  <meta property="og:url" content="https://www.incomeclaritylab.com{url}">
  <meta property="og:title" content="{title}">
  <meta property="og:description" content="{description}">
  <meta property="og:site_name" content="Income Clarity">
  <meta property="og:locale" content="en_US">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{title}">
  <meta name="twitter:description" content="{description}">
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
    "@type": "WebPage",
    "name": "{title}",
    "description": "{description}",
    "url": "https://www.incomeclaritylab.com{url}",
    "isPartOf": {{ "@type": "WebSite", "name": "Income Clarity", "url": "https://www.incomeclaritylab.com/" }}
  }}
  </script>
  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "BreadcrumbList",
    "itemListElement": [
      {{ "@type": "ListItem", "position": 1, "name": "Credit card payoff calculator", "item": "https://www.incomeclaritylab.com/debt" }},
      {{ "@type": "ListItem", "position": 2, "name": "Credit cards", "item": "https://www.incomeclaritylab.com/debt/credit-cards" }},
      {{ "@type": "ListItem", "position": 3, "name": "{breadcrumb}", "item": "https://www.incomeclaritylab.com{url}" }}
    ]
  }}
  </script>
</head>
<body class="debt-credit-cards-child-page housing-hub-page">
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

  <main class="container housing-hub debt-credit-cards-child">
    <nav class="take-home-return-nav housing-hub-crumb" aria-label="Breadcrumb">
      <ol class="take-home-return-breadcrumbs">
        <li><a href="/debt/credit-cards/credit-card-payoff-calculator#payoff">Credit card payoff calculator</a></li>
        <li><a href="/debt/credit-cards">Credit cards</a></li>
        <li aria-current="page">{breadcrumb}</li>
      </ol>
    </nav>

    <p class="debt-minimum-guide-back housing-hub-back">
      <a class="debt-minimum-guide-back-link" id="debt-guide-back-link" href="/debt/credit-cards" data-debt-back-default="/debt/credit-cards">← Back to credit cards</a>
    </p>

    <article class="housing-hub-panel debt-credit-cards-child-article">
      <header class="housing-hub-section-head">
        <p class="housing-hub-kicker">{kicker}</p>
        <h1>{h1}</h1>
        <p class="housing-hub-section-lead">{lead}</p>
      </header>
      {body}
      <p class="debt-credit-cards-child-cta"><a class="debt-topic-explore-btn" href="{cta_href}">{cta_label}</a></p>
    </article>
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
          <a href="/debt/credit-cards">Credit cards</a>
          <a href="/debt/payoff-scenarios">Debt payoff scenarios</a>
          <a href="/debt/credit-cards/credit-card-payoff-calculator#payoff">Payoff calculator</a>
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
</body>
</html>
'''

PAGES: list[dict] = [
    # Section 1 — calculators
    {
        "slug": "credit-card-payoff-calculator",
        "title": "Credit Card Payoff Calculator",
        "breadcrumb": "Credit card payoff calculator",
        "kicker": "💳 Calculator",
        "h1": "Credit Card Payoff Calculator",
        "lead": "Calculate how long it will take to eliminate your balance at your APR and monthly payment.",
        "body": "<p>Enter your balance, APR, and payment on our main payoff tool to see months to zero and total interest paid. Compare minimum vs fixed payments side by side.</p>",
        "cta_href": "/debt/credit-cards/credit-card-payoff-calculator#payoff",
        "cta_label": "Open payoff calculator",
    },
    {
        "slug": "minimum-payment-calculator",
        "title": "Minimum Payment Calculator",
        "breadcrumb": "Minimum payment calculator",
        "kicker": "📉 Calculator",
        "h1": "Minimum Payment Calculator",
        "lead": "See how long minimum payments keep you in debt—and how much extra interest they cost.",
        "body": "<p>Minimum payments are designed to keep accounts current, not to clear balances quickly. Run your numbers to see years to payoff and total interest when you pay only the minimum vs a fixed amount.</p>",
        "cta_href": "/debt/credit-cards/credit-card-payoff-calculator#payoff",
        "cta_label": "Compare minimum vs fixed",
    },
    {
        "slug": "credit-card-payment-calculator",
        "title": "Credit Card Payment Calculator",
        "breadcrumb": "Credit card payment calculator",
        "kicker": "💵 Calculator",
        "h1": "Credit Card Payment Calculator",
        "lead": "Estimate monthly payments and payoff timelines for your credit card balance.",
        "body": "<p>Plug in your balance and target payoff date—or your payment size and APR—to see what it takes to reach zero. Adjust one variable at a time to find a payment you can sustain.</p>",
        "cta_href": "/debt/credit-cards/credit-card-payoff-calculator#payoff",
        "cta_label": "Estimate your payment",
    },
    {
        "slug": "credit-card-interest-calculator",
        "title": "Credit Card Interest Calculator",
        "breadcrumb": "Credit card interest calculator",
        "kicker": "📈 Calculator",
        "h1": "Credit Card Interest Calculator",
        "lead": "Estimate total interest costs over the full life of your credit card debt.",
        "body": "<p>Total interest depends on your balance, APR, payment size, and whether you add new charges. Our payoff calculator projects lifetime interest for your exact inputs.</p>",
        "cta_href": "/debt/credit-cards/credit-card-payoff-calculator#payoff",
        "cta_label": "Calculate total interest",
    },
    # Section 2 — payoff scenarios
    {
        "slug": "payoff-1500-credit-card-debt",
        "title": "How to Pay Off $1,500 in Credit Card Debt",
        "breadcrumb": "Pay off $1,500",
        "kicker": "💸 Payoff scenario",
        "h1": "How to Pay Off $1,500 in Credit Card Debt",
        "lead": "A $1,500 balance is manageable with a clear payment plan—here is how long it takes at common APRs.",
        "body": "<p>At 22% APR with $75/month, $1,500 clears in about 2 years with roughly $300 in interest. Bump to $125/month and you finish in under 14 months. Run your exact numbers in the payoff calculator.</p>",
        "cta_href": "/debt/credit-cards/credit-card-payoff-calculator#payoff",
        "cta_label": "Plan your $1,500 payoff",
    },
    {
        "slug": "payoff-3000-credit-card-debt",
        "title": "How to Pay Off $3,000 in Credit Card Debt",
        "breadcrumb": "Pay off $3,000",
        "kicker": "💸 Payoff scenario",
        "h1": "How to Pay Off $3,000 in Credit Card Debt",
        "lead": "Three thousand dollars in card debt is a common starting point—see realistic timelines by payment size.",
        "body": "<p>At 24% APR, $3,000 with $150/month takes about 2 years and $600 in interest. Minimum payments can stretch this to 8+ years. A fixed payment above the interest line is the fastest lever.</p>",
        "cta_href": "/debt/credit-cards/credit-card-payoff-calculator#payoff",
        "cta_label": "Plan your $3,000 payoff",
    },
    {
        "slug": "payoff-5000-credit-card-debt",
        "title": "How to Pay Off $5,000 in Credit Card Debt",
        "breadcrumb": "Pay off $5,000",
        "kicker": "💸 Payoff scenario",
        "h1": "How to Pay Off $5,000 in Credit Card Debt",
        "lead": "Five thousand dollars at typical APRs can take a few years or over a decade—it depends on your payment.",
        "body": "<p>At 24% APR, $5,000 with $200/month clears in about 2.7 years. Pay only the minimum (~$100) and you may need 17+ years and pay more in interest than the original balance.</p>",
        "cta_href": "/debt/credit-cards/credit-card-payoff-calculator#payoff",
        "cta_label": "Plan your $5,000 payoff",
    },
    {
        "slug": "payoff-12000-credit-card-debt",
        "title": "How to Pay Off $12,000 in Credit Card Debt",
        "breadcrumb": "Pay off $12,000",
        "kicker": "💸 Payoff scenario",
        "h1": "How to Pay Off $12,000 in Credit Card Debt",
        "lead": "Twelve thousand in revolving debt needs a sustained plan—here is what different monthly payments achieve.",
        "body": "<p>At 22% APR, $12,000 with $400/month takes about 3.5 years and $4,800 in interest. Doubling the payment cuts both time and interest materially. Stop new charges on the target card while you pay down.</p>",
        "cta_href": "/debt/credit-cards/credit-card-payoff-calculator#payoff",
        "cta_label": "Plan your $12,000 payoff",
    },
    {
        "slug": "payoff-80000-credit-card-debt",
        "title": "How to Pay Off $80,000 in Credit Card Debt",
        "breadcrumb": "Pay off $80,000",
        "kicker": "💸 Payoff scenario",
        "h1": "How to Pay Off $80,000 in Credit Card Debt",
        "lead": "Large balances require aggressive payments and often professional guidance—start with an honest timeline.",
        "body": "<p>At 20% APR, $80,000 with $2,000/month still takes 5+ years and tens of thousands in interest. Consider avalanche ordering, balance transfers only after fee math, and whether consolidation or credit counseling fits your situation.</p>",
        "cta_href": "/debt/credit-cards/credit-card-payoff-calculator#payoff",
        "cta_label": "Model your payoff path",
    },
    # Section 3 — interest & APR
    {
        "slug": "apr-explained",
        "title": "What Is APR?",
        "breadcrumb": "What is APR?",
        "kicker": "📚 Interest & APR",
        "h1": "What Is APR?",
        "lead": "APR is the yearly cost of borrowing on your card—including interest and certain fees.",
        "body": "<p>Purchase APR applies to everyday spending. Cash advance and penalty APRs are often higher. Your statement shows each rate. Daily periodic rate = APR ÷ 365; interest accrues on your average daily balance.</p>",
        "cta_href": "/debt/credit-cards/what-is-credit-card-apr",
        "cta_label": "Read full APR guide",
    },
    {
        "slug": "cash-advance-apr",
        "title": "Cash Advance APR Explained",
        "breadcrumb": "Cash advance APR",
        "kicker": "📚 Interest & APR",
        "h1": "Cash Advance APR Explained",
        "lead": "Cash advances usually carry a higher APR, no grace period, and upfront fees.",
        "body": "<p>Unlike purchases, cash advances often start accruing interest immediately. Issuers may charge 3–5% per advance plus a higher APR than your purchase rate. Avoid unless absolutely necessary.</p>",
        "cta_href": "/debt/credit-cards/how-credit-card-interest-works",
        "cta_label": "How interest is calculated",
    },
    {
        "slug": "how-credit-card-interest-works",
        "title": "How Credit Card Interest Is Calculated",
        "breadcrumb": "How interest is calculated",
        "kicker": "📚 Interest & APR",
        "h1": "How Credit Card Interest Is Calculated",
        "lead": "Most US cards use average daily balance and daily compounding—small balances still add up fast.",
        "body": "<p>Each day, the issuer multiplies your balance by the daily periodic rate. Monthly finance charges sum those daily amounts. Paying mid-cycle or above the minimum reduces the balance interest is charged on.</p>",
        "cta_href": "/debt/interest/how-credit-card-interest-works",
        "cta_label": "Read detailed interest guide",
    },
    # Section 4 — minimum payment trap
    {
        "slug": "what-happens-if-you-only-pay-minimum",
        "title": "What Happens If You Only Pay the Minimum?",
        "breadcrumb": "Only paying the minimum",
        "kicker": "🚨 Minimum payments",
        "h1": "What Happens If You Only Pay the Minimum?",
        "lead": "Minimums keep your account current but can leave you in debt for years while interest compounds.",
        "body": "<p>Most of each minimum payment covers interest, not principal—especially at high APR. New charges reset the clock. The result: years of payments with little progress toward zero.</p>",
        "cta_href": "/debt/debt-reality/why-paying-minimum-is-bad",
        "cta_label": "See the minimum payment trap",
    },
    {
        "slug": "how-minimum-payments-are-calculated",
        "title": "How Minimum Payments Are Calculated",
        "breadcrumb": "How minimums are calculated",
        "kicker": "🚨 Minimum payments",
        "h1": "How Minimum Payments Are Calculated",
        "lead": "Issuers typically use a percentage of balance plus interest—often around 1–3% of balance with a floor near $25–$40.",
        "body": "<p>As your balance drops, the minimum drops too—slowing payoff. Some cards add current-month interest and fees to the formula. Check your card agreement for the exact method.</p>",
        "cta_href": "/debt/credit-cards/minimum-payment-calculator",
        "cta_label": "Run minimum payment math",
    },
    # Section 5 — strategies
    {
        "slug": "debt-snowball-vs-avalanche",
        "title": "Debt Snowball vs Debt Avalanche",
        "breadcrumb": "Snowball vs avalanche",
        "kicker": "⚖️ Payoff methods",
        "h1": "Debt Snowball vs Debt Avalanche",
        "lead": "Avalanche saves the most interest; snowball builds momentum by clearing small balances first.",
        "body": "<p><strong>Avalanche:</strong> pay extra toward the highest APR balance. <strong>Snowball:</strong> pay extra toward the smallest balance. Both work if you stop adding new debt and pay more than the minimum.</p>",
        "cta_href": "/debt/payoff/best-way-to-pay-off-credit-card-debt",
        "cta_label": "Compare payoff strategies",
    },
    {
        "slug": "minimum-vs-fixed-payment",
        "title": "Minimum Payment vs Fixed Payment",
        "breadcrumb": "Minimum vs fixed payment",
        "kicker": "⚖️ Payoff methods",
        "h1": "Minimum Payment vs Fixed Payment",
        "lead": "A fixed payment locks in progress; minimums shrink as the balance falls and extend your timeline.",
        "body": "<p>Choose a payment you can sustain—even $50 above the minimum changes years-to-zero. Automate it so you are not tempted to drop back to the minimum when the bill shrinks.</p>",
        "cta_href": "/debt/credit-cards/credit-card-payoff-calculator#payoff",
        "cta_label": "Compare payment paths",
    },
    {
        "slug": "balance-transfer-vs-paying-interest",
        "title": "Balance Transfer vs Paying Interest",
        "breadcrumb": "Balance transfer vs paying interest",
        "kicker": "⚖️ Payoff methods",
        "h1": "Balance Transfer vs Paying Interest",
        "lead": "A 0% promo can save interest if you pay off before the rate resets and fees do not erase the benefit.",
        "body": "<p>Balance transfer fees (often 3–5%) and post-promo APR matter. You need a plan to clear the balance during the promo window. If you will keep spending, paying down in place may be simpler.</p>",
        "cta_href": "/debt/credit-cards/credit-card-payoff-calculator",
        "cta_label": "Model your payoff first",
    },
]

DEBT_TOOL_PAGES: list[dict] = [
    {
        "slug": "debt-to-income",
        "prefix": "debt",
        "title": "Debt-to-Income Calculator",
        "breadcrumb": "Debt-to-income",
        "kicker": "📊 Debt tools",
        "h1": "Debt-to-Income Calculator",
        "lead": "See how monthly debt payments compare to your gross income—a key metric lenders use.",
        "body": "<p>Debt-to-income (DTI) = total monthly debt payments ÷ gross monthly income. Under 36% is often considered manageable; above 43% may limit mortgage approval. Include cards, auto, student loans, and housing.</p>",
        "cta_href": "/debt/financial-health/can-i-afford-my-debt",
        "cta_label": "Check if you can afford your debt",
    },
    {
        "slug": "monthly-debt-planner",
        "prefix": "debt",
        "title": "Monthly Debt Payment Planner",
        "breadcrumb": "Monthly debt planner",
        "kicker": "📊 Debt tools",
        "h1": "Monthly Debt Payment Planner",
        "lead": "Map out how much to send each creditor every month while staying within your budget.",
        "body": "<p>List minimums first, then allocate extra to either the highest APR (avalanche) or smallest balance (snowball). Our payoff calculator shows how each extra dollar changes your finish line.</p>",
        "cta_href": "/debt/credit-cards/credit-card-payoff-calculator#payoff",
        "cta_label": "Plan monthly payments",
    },
]


def write_page(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def render_page(page: dict, url_prefix: str) -> str:
    url = f"{url_prefix}/{page['slug']}"
    return PAGE_TEMPLATE.format(
        title=page["title"],
        description=page["lead"],
        url=url,
        breadcrumb=page["breadcrumb"],
        kicker=page["kicker"],
        h1=page["h1"],
        lead=page["lead"],
        body=page["body"],
        cta_href=page["cta_href"],
        cta_label=page["cta_label"],
    )


def redirect_rules(slug: str, prefix: str) -> list[str]:
    base = f"/{prefix}/{slug}"
    return [
        f"{base}.html     {base}    301!",
        f"{base}     {base}/    301!",
        f"{base}/     {base}/index.html    200",
    ]


def main() -> None:
    created = 0
    rules: list[str] = [
        "/debt/credit-cards/                /debt/credit-cards                      301!",
        "/debt/credit-cards                 /debt/credit-cards/index.html           200",
        "/debt/hidden-costs/                /debt/credit-cards                      301!",
        "/debt/hidden-costs                 /debt/credit-cards                      301!",
    ]

    HAND_MAINTAINED = {
        "credit-card-payoff-calculator",
        "minimum-payment-calculator",
        "credit-card-interest-calculator",
        "cash-advance-apr",
        "debt-snowball-vs-avalanche",
        "minimum-vs-fixed-payment",
        "balance-transfer-vs-paying-interest",
        "payoff-under-5000",
        "payoff-5000-to-15000",
        "payoff-15000-to-50000",
        "payoff-over-50000",
        "payoff-10000-credit-card-debt",
    }

    for page in PAGES:
        rel = f"{HUB}/{page['slug']}/index.html"
        if page["slug"] not in HAND_MAINTAINED:
            write_page(ROOT / rel, render_page(page, HUB_URL))
        rules.extend(redirect_rules(page["slug"], HUB))
        created += 1

    for page in DEBT_TOOL_PAGES:
        prefix = page["prefix"]
        rel = f"{prefix}/{page['slug']}/index.html"
        url_prefix = f"/{prefix}"
        content = PAGE_TEMPLATE.format(
            title=page["title"],
            description=page["lead"],
            url=f"{url_prefix}/{page['slug']}",
            breadcrumb=page["breadcrumb"],
            kicker=page["kicker"],
            h1=page["h1"],
            lead=page["lead"],
            body=page["body"],
            cta_href=page["cta_href"],
            cta_label=page["cta_label"],
        )
        # Debt tool pages breadcrumb: skip credit-cards middle link
        content = content.replace(
            '<li><a href="/debt/credit-cards">Credit cards</a></li>\n        <li aria-current="page">',
            '<li aria-current="page">',
        )
        content = content.replace(
            '← Back to credit cards',
            "← Back to debt calculator",
        )
        content = content.replace(
            'href="/debt/credit-cards" data-debt-back-default="/debt/credit-cards"',
            'href="/debt/credit-cards/credit-card-payoff-calculator#payoff" data-debt-back-default="/debt/credit-cards/credit-card-payoff-calculator#payoff"',
        )
        write_page(ROOT / rel, content)
        rules.extend(redirect_rules(page["slug"], prefix))
        created += 1

    redirects_path = ROOT / "_redirects"
    text = redirects_path.read_text(encoding="utf-8")
    # Remove old hidden-costs rules
    lines = [
        ln
        for ln in text.splitlines()
        if "/debt/hidden-costs" not in ln
    ]
    # Insert credit-cards rules after financial-health block
    insert_at = next(
        (i for i, ln in enumerate(lines) if ln.startswith("/debt/life-decisions")),
        len(lines),
    )
    new_block = rules + [""]
    lines = lines[:insert_at] + new_block + lines[insert_at:]
    redirects_path.write_text("\n".join(lines) + "\n", encoding="utf-8")

    print(f"Created/updated {created} cluster pages")
    print(f"Added {len(rules)} redirect rules")


if __name__ == "__main__":
    main()
