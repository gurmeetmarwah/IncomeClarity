#!/usr/bin/env python3
"""Generate hand-quality payoff tier landing pages under /debt/credit-cards/."""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
HUB = "debt/credit-cards"

FOOTER = '''  <footer class="site-footer">
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
          <a href="/debt/credit-cards/credit-card-payoff-calculator#payoff">Payoff calculator</a>
          <a href="/debt/payoff-scenarios">Debt payoff scenarios</a>
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
  <script src="/debt-guide-back.js"></script>'''

TIERS = [
    {
        "slug": "payoff-under-5000",
        "title": "Pay Off Credit Card Debt Under $5,000: Fast Wins & Real Timelines",
        "description": "Owe under $5,000 on credit cards? See realistic payoff timelines, interest costs, and step-by-step plans for $1,500 to $4,000 balances in 2026.",
        "breadcrumb": "Pay off under $5,000",
        "label": "Small balances",
        "h1": "How to Pay Off Credit Card Debt Under $5,000",
        "hero_lead": "A few thousand dollars feels heavy—but it is one of the most beatable debt ranges. With a fixed payment above your interest charge, many people clear <strong>under-$5,000 balances in 12 to 36 months</strong>. Pick your path below.",
        "range": "Under $5,000",
        "accent": "small",
        "jump": [
            ("overview", "Overview"),
            ("math", "The math"),
            ("plan", "Your plan"),
            ("scenarios", "Popular amounts"),
            ("faq", "FAQ"),
        ],
        "scenarios": [
            ("$1.5k", "Paying Off $1,500 Debt", "/debt/payoff-scenarios/how-long-to-pay-off-1500-debt", "Interactive planner—often clear in under 2 years."),
            ("$3k", "Paying Off $3,000 Debt", "/debt/payoff-scenarios/how-long-to-pay-off-3000-debt", "Full scenario guide with calculator, timeline, and what-if tools."),
        ],
        "table_caption": "$3,000 balance at 22% APR — how payment size changes your finish line",
        "table_rows": [
            ("$75/mo (near minimum)", "5+ years", "$2,200+", "Mostly interest early on"),
            ("$125/mo", "~2.5 years", "~$900", "Solid starter plan"),
            ("$175/mo", "~1.5 years", "~$550", "Aggressive but realistic"),
            ("$250/mo", "~1 year", "~$350", "Fastest common path"),
        ],
        "prose": """
        <p>If your total credit card debt is <strong>under $5,000</strong>, you are in a range where small, steady payments make a huge difference. This is not a life sentence. It is a math problem with a clear exit—if you stop adding new charges and pay more than your monthly interest.</p>
        <p>Most Americans who carry card debt owe between $2,000 and $6,000 across one or two cards. Under $5,000 often comes from a single emergency, a vacation that lingered, or a few months of overspending. The good news: you do not need a windfall. You need a <strong>fixed monthly payment</strong> you can repeat for 12 to 36 months.</p>
        <h3>Why small balances still hurt</h3>
        <p>Do not let the size fool you. $2,500 at 24% APR still earns about <strong>$50 in interest every month</strong>. Pay only the minimum—often $50 to $75—and your balance barely moves. That is the <a href="/debt/credit-cards/what-happens-if-you-only-pay-minimum">minimum payment trap</a> in miniature: you stay current on the bill, but the real debt sticks around for years.</p>
        <p>The fix is simple to say and harder to do: pick a payment that covers interest <em>and</em> knocks down principal. Even <strong>$40 to $50 above</strong> your minimum can cut a five-year slog to under three years on a $3,000 balance.</p>
        <h3>What a realistic timeline looks like</h3>
        <p>For balances under $5,000, most people target <strong>18 to 36 months</strong>. A $1,500 balance at 22% APR with $100/month can be gone in about 17 months. A $4,000 balance at 24% APR with $200/month often clears in roughly two and a half years. Run your exact numbers in our <a href="/debt/credit-cards/credit-card-payoff-calculator#payoff">payoff calculator</a> before you commit.</p>
        <p>Match your payment to take-home pay—not wishful thinking. Use the <a href="/hourly-to-salary-after-tax#hourly-salary-form">hourly-to-salary after-tax calculator</a> to see what you actually bring home, then decide what you can lock in each month.</p>
        """,
        "plan_steps": [
            ("Stop the bleeding", "Pause new charges on the card you are paying down. Use cash or debit for daily spending so your payment actually shrinks the balance."),
            ("Pick one fixed payment", "Choose an amount above month-one interest and treat it like rent. Same number every month—even when the issuer minimum drops."),
            ("Name your debt-free month", "Enter balance, APR, and payment in the payoff calculator. Write down the month and year you hit zero."),
            ("Automate if you can", "Schedule the payment a day after payday. Automation beats willpower on month six when motivation fades."),
            ("Celebrate milestones", "Every $500 down is real progress. Small balances disappear faster when you track wins, not just the finish line."),
        ],
        "mistakes": [
            "Paying only the minimum because the balance feels 'small enough to ignore.'",
            "Splitting extra cash across too many goals—one focused card payment beats scattered $20 top-ups.",
            "Keeping the card in your wallet while you are paying it off.",
            "Ignoring APR: a store card at 29% needs a higher payment than a 18% card for the same balance.",
        ],
        "faq": [
            ("How long does it take to pay off $3,000 in credit card debt?", "At 22% APR with $125/month, about 2.5 years and roughly $900 in interest. At $175/month, about 18 months. Your APR and payment matter more than the balance label."),
            ("Is $1,500 in credit card debt bad?", "It is common and very manageable with a plan. The risk is paying only the minimum and letting interest stack for years on a balance that could have been cleared quickly."),
            ("Should I use savings to pay off a small balance?", "If your emergency fund still leaves you with at least one month of expenses after the payoff, wiping a high-APR card can save more in interest than your savings earn. Keep a small buffer."),
            ("Snowball or avalanche for under $5,000?", "With one card, both methods are the same—pay that card. With two small cards, snowball (smallest first) builds momentum; avalanche (highest APR first) saves the most interest."),
            ("What payment should I aim for?", "At least enough to cover month-one interest plus $50 to $100 toward principal. On $3,000 at 22% APR, that often means $125 to $175/month."),
        ],
        "related_tier": ("Medium balances ($5,000–$15,000)", "/debt/credit-cards/payoff-5000-to-15000"),
    },
    {
        "slug": "payoff-5000-to-15000",
        "title": "Pay Off $5,000–$15,000 Credit Card Debt: Timelines & Strategies",
        "description": "Carrying $5,000 to $15,000 on credit cards? Compare payoff timelines, total interest, and proven strategies for the most common US debt range.",
        "breadcrumb": "Pay off $5,000–$15,000",
        "label": "Medium balances",
        "h1": "How to Pay Off $5,000 to $15,000 in Credit Card Debt",
        "hero_lead": "This is where most US cardholders live—enough debt to sting, but absolutely payable with a plan. At 22% APR, <strong>$5,000 with $200/month</strong> clears in under three years. <strong>$10,000 with $400/month</strong> can be gone in about two and a half. See what your payment buys.",
        "range": "$5,000–$15,000",
        "accent": "medium",
        "jump": [
            ("overview", "Overview"),
            ("math", "The math"),
            ("plan", "Your plan"),
            ("scenarios", "Popular amounts"),
            ("faq", "FAQ"),
        ],
        "scenarios": [
            ("$5k", "Paying Off $5,000 Debt", "/debt/payoff-scenarios/how-long-to-pay-off-5000-debt", "Interactive planner—timelines, interest, and pay-more comparisons."),
            ("$10k", "Paying Off $10,000 Debt", "/debt/payoff-scenarios/how-long-to-pay-off-10000-debt", "Full scenario guide with calculator, timeline, and what-if tools."),
        ],
        "table_caption": "$10,000 balance at 22% APR — payment paths that actually work",
        "table_rows": [
            ("$200/mo", "7+ years", "$6,500+", "Minimum-style danger zone"),
            ("$300/mo", "~4 years", "~$3,800", "Slow but steady"),
            ("$400/mo", "~2.5 years", "~$2,400", "Strong middle-ground plan"),
            ("$600/mo", "~1.5 years", "~$1,400", "Aggressive payoff"),
        ],
        "prose": """
        <p>Between <strong>$5,000 and $15,000</strong>, credit card debt stops feeling like a slip-up and starts feeling like a weight on every paycheck. You are not alone—this range is the most common serious card balance in US households. The math is still on your side if you pick a <strong>fixed payment</strong> and stop adding new charges.</p>
        <p>At typical APRs of 20% to 25%, interest alone on a $10,000 balance is about <strong>$167 to $208 per month</strong>. Pay only that much and you run in place for years. Pay $400/month and you are buying back years of your life and thousands in interest.</p>
        <h3>Why this range feels stuck</h3>
        <p>Medium balances sit in an awkward middle. They are too big to knock out with one bonus check, but small enough that banks keep extending credit. Minimum payments are designed to feel affordable—$150 to $250 on a $8,000 balance—while most of that money goes to <a href="/debt/credit-cards/how-credit-card-interest-works">interest</a>, not principal.</p>
        <p>Many people pay diligently for years without seeing the balance drop much. That is not a personal failure. It is how revolving interest works. The fix is raising your payment and holding it steady even when the issuer minimum shrinks. Read <a href="/debt/credit-cards/minimum-vs-fixed-payment">minimum vs fixed payment</a> for why that matters.</p>
        <h3>Total interest: the number that should scare you into action</h3>
        <p>On $10,000 at 22% APR, paying $250/month can cost <strong>over $5,000 in total interest</strong> and take six years. The same balance at $450/month might finish in under two and a half years with roughly $2,500 in interest. That $200 monthly difference is worth <strong>$2,500+</strong>—real money you could put toward savings, rent, or a vacation you pay for in cash.</p>
        <p>Use our <a href="/debt/credit-cards/credit-card-interest-calculator">interest calculator</a> to see month-one finance charges and lifetime interest at your payment level. Then model a higher fixed amount in the <a href="/debt/credit-cards/credit-card-payoff-calculator#payoff">payoff calculator</a>.</p>
        """,
        "plan_steps": [
            ("List every card and APR", "Write balance and APR for each card. You cannot prioritize without seeing the full picture."),
            ("Choose snowball or avalanche", "Avalanche attacks highest APR first and saves the most money. Snowball clears the smallest balance first for quick wins. Both work—pick the one you will stick with."),
            ("Set a floor payment", "Decide the minimum total you will pay across cards each month, then add any extra to your target card."),
            ("Consider a balance transfer—carefully", "A 0% promo can pause interest if you will not add new charges and can pay off before the rate jumps. Factor in transfer fees."),
            ("Protect your income plan", "Match payments to after-tax income. A $400/month plan that breaks your budget in month four will not last."),
        ],
        "mistakes": [
            "Paying the minimum on a $8,000 balance because 'at least I'm paying something.'",
            "Balance-transfer hopping without paying down principal during the promo window.",
            "Using cards for emergencies while still paying off old debt—pause new charges first.",
            "Ignoring multiple APRs on one card (purchases vs cash advances).",
        ],
        "faq": [
            ("How long to pay off $10,000 in credit card debt?", "At 22% APR with $400/month, about 2 years 8 months and roughly $2,400 in interest. With $250/month, six years or more. Payment size drives the timeline."),
            ("Is $5,000 in credit card debt normal?", "Yes—it is near the US median for households that carry revolving debt. Normal does not mean comfortable; it means a clear plan can put you ahead of most people who only pay minimums."),
            ("Should I consolidate $12,000 in card debt?", "A personal loan at a lower fixed rate can work if you stop using the cards and the loan payment fits your budget. Compare total interest vs keeping cards and paying aggressively."),
            ("How much interest on $5,000 at 24% APR?", "Month-one interest is about $100. Total interest depends on payment: ~$100/month may never pay off; $200/month might cost ~$2,000 over roughly three years."),
            ("Can I pay off $15,000 in one year?", "You would need about $1,400/month plus interest savings as the balance drops—possible for some incomes, but a 24-to-36-month plan is more realistic for most households."),
        ],
        "related_tier": ("Large balances ($15,000–$50,000)", "/debt/credit-cards/payoff-15000-to-50000"),
    },
    {
        "slug": "payoff-15000-to-50000",
        "title": "Pay Off $15,000–$50,000 Credit Card Debt: Multi-Year Plans That Work",
        "description": "Facing $15,000 to $50,000 in credit card debt? Realistic timelines, interest totals, balance-transfer tips, and income-based strategies for 2026.",
        "breadcrumb": "Pay off $15,000–$50,000",
        "label": "Large balances",
        "h1": "How to Pay Off $15,000 to $50,000 in Credit Card Debt",
        "hero_lead": "Large card balances need a multi-year plan—not panic. At 22% APR, <strong>$25,000 with $750/month</strong> can clear in about three and a half years. The key is a payment you can sustain and a hard stop on new charges.",
        "range": "$15,000–$50,000",
        "accent": "large",
        "jump": [
            ("overview", "Overview"),
            ("math", "The math"),
            ("plan", "Your plan"),
            ("faq", "FAQ"),
        ],
        "scenarios": [],
        "table_caption": "$25,000 balance at 22% APR — sustained payments vs minimum-style traps",
        "table_rows": [
            ("$400/mo", "12+ years", "$30,000+", "Interest can exceed original debt"),
            ("$600/mo", "~6 years", "~$14,000", "Long road, but progress"),
            ("$750/mo", "~3.5 years", "~$8,500", "Serious commitment"),
            ("$1,000/mo", "~2.5 years", "~$5,500", "Aggressive, faster freedom"),
        ],
        "prose": """
        <p>When credit card debt climbs past <strong>$15,000</strong>, the monthly minimum can look like a second rent payment—while barely touching principal. Balances in the <strong>$15,000 to $50,000</strong> range often come from years of minimum payments, income shocks, medical bills, or business expenses on personal cards. This is hard—but it is not hopeless.</p>
        <p>The turning point is treating payoff like a <strong>multi-year project</strong> with a fixed monthly number, not a hope that next month will be easier. Interest on $30,000 at 22% APR is about <strong>$550 per month</strong>. Any plan that pays less than that in the early months is losing ground.</p>
        <h3>Why large balances compound emotionally and financially</h3>
        <p>High balances push up utilization, which can hurt your credit score even when you pay on time. High utilization also makes it harder to qualify for better rates—creating a cycle where you are stuck at 24% to 29% APR on tens of thousands of dollars.</p>
        <p>At the same time, large debts tempt people into partial solutions: minimum payments plus occasional lump sums, or balance transfers without changing spending. What works is boring and repeatable: <strong>the same big payment every month</strong> until the balance hits zero. See <a href="/debt/credit-cards/debt-snowball-vs-avalanche">snowball vs avalanche</a> if you owe multiple cards.</p>
        <h3>Income is the ceiling—plan from take-home pay</h3>
        <p>A $900/month payoff plan sounds great until it collides with rent, childcare, and groceries. Start with your real take-home pay from the <a href="/hourly-to-salary-after-tax#hourly-salary-form">after-tax income calculator</a>. List non-negotiable expenses. What is left is your payoff ceiling—not what you wish you could pay.</p>
        <p>If the math does not close, you have three levers: raise income (overtime, side work, selling items), cut expenses temporarily, or seek structured help (nonprofit credit counseling, debt management plan). Ignoring the gap and paying an unsustainable amount leads to missed payments and penalty APRs—which makes everything worse.</p>
        <h3>Balance transfers and consolidation—when they help</h3>
        <p>A 0% balance transfer on part of a $25,000 debt can save thousands if you pay off the promo balance before the rate resets. Watch transfer fees (often 3% to 5%) and do not use the old cards. A fixed-rate personal loan can lower APR if you qualify—but only if you close the spending loop on the cards.</p>
        <p>Compare total cost with our <a href="/debt/credit-cards/credit-card-interest-calculator">interest calculator</a> before you move debt around. Moving numbers without paying principal faster is just rearranging the same problem.</p>
        """,
        "plan_steps": [
            ("Full debt inventory", "Every card: balance, APR, minimum, due date. Include store cards and forgotten accounts."),
            ("Calculate your sustainable payment", "From take-home pay, set a total monthly amount you can pay for 36+ months without missing rent or essentials."),
            ("Attack highest APR or smallest balance", "Avalanche saves the most interest on large debts. Snowball gives a psychological win if you need momentum—both beat minimum-only."),
            ("Freeze discretionary card use", "Large payoffs fail when new charges offset progress. Use debit or cash for variable spending."),
            ("Review every 90 days", "Check balances, interest paid, and whether you can add $50 to your payment after a raise or expense drop."),
        ],
        "mistakes": [
            "Paying minimums on $20,000+ while hoping interest rates drop.",
            "Taking a 401(k) loan or hardship withdrawal without understanding taxes and lost growth.",
            "Signing up for debt settlement ads that promise quick fixes for high fees.",
            "Transferring balances repeatedly without increasing principal payments.",
        ],
        "faq": [
            ("How long to pay off $20,000 in credit card debt?", "At 22% APR with $600/month, about six years and roughly $18,000 in interest. With $900/month, about three years and roughly $9,000 in interest. Sustainable payment beats optimistic bursts."),
            ("Is $30,000 in credit card debt recoverable?", "Yes, with a multi-year plan and no new charges. Many people have cleared balances this size using avalanche payoff, income increases, and strict budgets."),
            ("Should I use home equity to pay cards?", "Rarely a first move—unsecured card debt becomes secured against your home. Explore aggressive card payoff and counseling before risking your house."),
            ("What is credit counseling?", "Nonprofit agencies can help with a debt management plan—lower rates negotiated with issuers, one monthly payment, typically 3 to 5 years. Good option when DIY plans keep failing."),
            ("How much interest on $25,000 at 24% APR?", "About $500/month at the start. Over a minimum-style payment path, total interest can exceed the original $25,000. Fixed payments of $750+ change the picture dramatically."),
        ],
        "related_tier": ("Severe balances (over $50,000)", "/debt/credit-cards/payoff-over-50000"),
    },
    {
        "slug": "payoff-over-50000",
        "title": "Pay Off Over $50,000 in Credit Card Debt: Options & Recovery Paths",
        "description": "Owe more than $50,000 on credit cards? Understand realistic timelines, professional options, and step-by-step recovery—without shame or quick-fix traps.",
        "breadcrumb": "Pay off over $50,000",
        "label": "Severe balances",
        "h1": "How to Tackle Credit Card Debt Over $50,000",
        "hero_lead": "Severe card debt is a crisis—but people recover from it every day. You need a plan scaled to your income, honest math on interest, and the right help when DIY is not enough. Start with the real numbers—not shame.",
        "range": "Over $50,000",
        "accent": "severe",
        "jump": [
            ("overview", "Overview"),
            ("math", "The math"),
            ("plan", "Your plan"),
            ("options", "Get help"),
            ("faq", "FAQ"),
        ],
        "scenarios": [
            ("$80k", "Paying Off $80,000 Debt", "/debt/credit-cards/payoff-80000-credit-card-debt", "Extreme balance case study—timelines, options, and warnings."),
        ],
        "table_caption": "$60,000 balance at 22% APR — why minimum-style payments fail at this scale",
        "table_rows": [
            ("$800/mo", "15+ years", "$80,000+", "Interest dwarfs principal"),
            ("$1,200/mo", "~8 years", "~$45,000", "Still a long haul"),
            ("$1,800/mo", "~4.5 years", "~$25,000", "Requires major income allocation"),
            ("$2,500/mo", "~3 years", "~$17,000", "Aggressive—needs budget overhaul"),
        ],
        "prose": """
        <p>More than <strong>$50,000</strong> in credit card debt is rare, but it happens—business debt on personal cards, medical crises, divorce, years of minimum payments, or a combination. If this is you, the first step is not a blog tip. It is <strong>honest math</strong> and a decision about whether DIY payoff is realistic on your income.</p>
        <p>Interest alone on $60,000 at 22% APR is about <strong>$1,100 per month</strong>. Pay less than that and your balance grows. Severe debt is not solved by motivation quotes. It is solved by structured payments, income changes, professional plans, or—in some cases—legal options reviewed with a qualified attorney.</p>
        <h3>You are not alone—and shame blocks solutions</h3>
        <p>High balances often carry shame that keeps people hiding statements and paying minimums. Minimums keep collectors quiet while interest compounds. Breaking that cycle starts with listing every account and every APR—no judgment, just data.</p>
        <p>Compare your situation to <a href="/debt/strategies/average-credit-card-debt-by-income">average debt by income</a> to see context, not excuses. Whether you are above or below average, the path forward is the same: stop new charges, maximize sustainable payments, and get expert help when the gap between income and debt is too wide.</p>
        <h3>When DIY is not enough</h3>
        <p>If your sustainable payment cannot cover month-one interest on the total balance, you are in negative amortization territory—the balance grows even while you pay. That is the signal to talk to a <strong>nonprofit credit counselor</strong> (NFCC member agency) about a debt management plan, or to consult a bankruptcy attorney for a factual review—not as a first impulse, but as an informed option.</p>
        <p>Debt settlement companies that promise fast fixes for high fees often leave you worse off. Credit counseling and legitimate debt management plans negotiate with issuers and consolidate payments without the marketing hype.</p>
        <h3>Building a survival budget first</h3>
        <p>Before you send another dollar to cards, secure housing, food, utilities, and minimums on secured debt (car, mortgage). Then allocate everything realistically possible to cards—starting with highest APR (avalanche). Use the <a href="/debt/credit-cards/credit-card-payoff-calculator#payoff">payoff calculator</a> with your actual number, not a fantasy payment.</p>
        <p>Income increases—overtime, second job, selling assets, tax refund, employer bonus—should have a rule: what percentage goes to debt until you hit a defined milestone (e.g., below $40,000).</p>
        """,
        "plan_steps": [
            ("Complete debt and income audit", "Every card, every APR, every minimum. Every income source after tax. Face the full gap."),
            ("Stabilize cash flow", "No missed housing or utility payments. Protect the foundation before heroic card payments."),
            ("Book a nonprofit credit counseling session", "Free or low-cost review. Ask about debt management plans vs DIY."),
            ("Stop all new unsecured charges", "Cut cards from wallets, remove from autofill, freeze accounts if needed."),
            ("Set quarterly review dates", "Every 90 days: balance down? Payment still sustainable? Income changed? Adjust."),
        ],
        "mistakes": [
            "Paying debt settlement firms thousands before understanding alternatives.",
            "Draining retirement accounts without tax and penalty analysis.",
            "Ignoring IRS debt or child support to pay cards—priority debts come first.",
            "Assuming bankruptcy is 'giving up' without a confidential attorney consult.",
        ],
        "faq": [
            ("How long to pay off $80,000 in credit card debt?", "At 22% APR with $2,000/month, roughly four to five years and tens of thousands in interest—if you add no new charges. With $1,000/month, the timeline stretches past a decade. See our $80,000 scenario guide for detail."),
            ("Is $50,000 in credit card debt hopeless?", "No—but it requires a plan matched to income. DIY works for some; others need debt management plans, income increases, or legal options. Hopeless is paying minimums without a strategy."),
            ("Should I file bankruptcy with $60,000 in card debt?", "Only a qualified bankruptcy attorney can answer after reviewing your full situation. It is a legal tool—not a moral failure—for unpayable unsecured debt."),
            ("What is a debt management plan?", "A nonprofit counselor negotiates lower rates with issuers. You make one monthly payment for typically 3 to 5 years. Fees are modest compared to settlement scams."),
            ("Can I negotiate credit card debt myself?", "Sometimes issuers accept hardship plans or lower rates if you call before accounts are charged off. Document every offer in writing."),
        ],
        "related_tier": ("Small balances (under $5,000)", "/debt/credit-cards/payoff-under-5000"),
    },
]


def render_scenarios(scenarios: list) -> str:
    if not scenarios:
        return ""
    cards = ""
    for tag, title, href, desc in scenarios:
        cards += f'''
        <a class="cc-payoff-tier-scenario-card" href="{href}">
          <span class="cc-payoff-tier-scenario-tag">{tag}</span>
          <h3>{title}</h3>
          <p>{desc}</p>
          <span class="cc-payoff-tier-scenario-cta">Read guide →</span>
        </a>'''
    return f'''
    <section class="housing-hub-panel cc-payoff-tier-scenarios-panel" id="scenarios" aria-labelledby="scenarios-title">
      <header class="housing-hub-section-head">
        <p class="housing-hub-kicker">📌 Popular amounts</p>
        <h2 id="scenarios-title">Jump to a specific balance guide</h2>
      </header>
      <div class="cc-payoff-tier-scenario-grid">{cards}
      </div>
    </section>'''


def render_table(caption: str, rows: list) -> str:
    body = ""
    for payment, time_col, interest, note in rows:
        body += f"<tr><td class=\"num\">{payment}</td><td class=\"num\">{time_col}</td><td class=\"num\">{interest}</td><td>{note}</td></tr>"
    return f'''
      <div class="scenario-table-wrap">
        <table class="scenario-table">
          <caption>{caption}</caption>
          <thead>
            <tr>
              <th class="num">Monthly payment</th>
              <th class="num">Payoff time</th>
              <th class="num">Total interest (approx.)</th>
              <th>Notes</th>
            </tr>
          </thead>
          <tbody>{body}
          </tbody>
        </table>
      </div>'''


def render_plan(steps: list) -> str:
    items = "".join(f"<li><strong>{title}.</strong> {body}</li>" for title, body in steps)
    return f'<ol class="apr-plain-list cc-payoff-tier-steps">{items}</ol>'


def render_mistakes(mistakes: list) -> str:
    items = "".join(f"<li>{m}</li>" for m in mistakes)
    return f'<ul class="apr-plain-list">{items}</ul>'


def render_faq(faq: list) -> str:
    items = ""
    for q, a in faq:
        items += f"<article class=\"faq-item\"><h3>{q}</h3><p>{a}</p></article>"
    return f'''
    <section class="housing-hub-panel housing-hub-panel--faq" id="faq" aria-labelledby="faq-title">
      <header class="housing-hub-section-head">
        <p class="housing-hub-kicker">❓ FAQ</p>
        <h2 id="faq-title">Common questions</h2>
      </header>
      <div class="faq-stack">{items}
      </div>
    </section>'''


def render_jump(jump: list) -> str:
    pills = "".join(f'<a class="housing-hub-jump-pill" href="#{anchor}">{label}</a>' for anchor, label in jump)
    return f'<nav class="housing-hub-jump cc-payoff-tier-jump" aria-label="On this page">{pills}</nav>'


def render_page(tier: dict) -> str:
    url = f"/{HUB}/{tier['slug']}"
    faq_schema = ",\n      ".join(
        f'{{ "@type": "Question", "name": "{q}", "acceptedAnswer": {{ "@type": "Answer", "text": "{a}" }} }}'
        for q, a in tier["faq"]
    )
    related_label, related_href = tier["related_tier"]
    scenarios_html = render_scenarios(tier["scenarios"])

    return f'''<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{tier["title"]} | Income Clarity</title>
  <meta name="description" content="{tier["description"]}">
  <meta property="og:type" content="website">
  <meta property="og:url" content="https://www.incomeclaritylab.com{url}">
  <meta property="og:title" content="{tier["title"]}">
  <meta property="og:description" content="{tier["description"]}">
  <meta property="og:site_name" content="Income Clarity">
  <meta property="og:locale" content="en_US">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{tier["title"]}">
  <meta name="twitter:description" content="{tier["description"]}">
  <meta name="robots" content="index,follow">
  <link rel="canonical" href="https://www.incomeclaritylab.com{url}">
  <link rel="stylesheet" href="/styles.css?v=cc-payoff-tier">
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
    "name": "{tier["title"]}",
    "description": "{tier["description"]}",
    "url": "https://www.incomeclaritylab.com{url}",
    "isPartOf": {{ "@type": "WebSite", "name": "Income Clarity", "url": "https://www.incomeclaritylab.com/" }}
  }}
  </script>
  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "BreadcrumbList",
    "itemListElement": [
      {{ "@type": "ListItem", "position": 1, "name": "Debt", "item": "https://www.incomeclaritylab.com/debt" }},
      {{ "@type": "ListItem", "position": 2, "name": "Credit cards", "item": "https://www.incomeclaritylab.com/debt/credit-cards" }},
      {{ "@type": "ListItem", "position": 3, "name": "{tier["breadcrumb"]}", "item": "https://www.incomeclaritylab.com{url}" }}
    ]
  }}
  </script>
  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "FAQPage",
    "mainEntity": [
      {faq_schema}
    ]
  }}
  </script>
</head>
<body>
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

  <main class="container debt-page cc-payoff-tier-page cc-payoff-tier-page--{tier["accent"]}">
    <nav class="take-home-return-nav housing-hub-crumb" aria-label="Breadcrumb">
      <ol class="take-home-return-breadcrumbs">
        <li><a href="/debt">Debt</a></li>
        <li><a href="/debt/credit-cards">Credit cards</a></li>
        <li aria-current="page">{tier["breadcrumb"]}</li>
      </ol>
    </nav>

    <p class="debt-minimum-guide-back housing-hub-back">
      <a class="debt-minimum-guide-back-link" id="debt-guide-back-link" href="/debt/credit-cards#cc-payoff-scenarios" data-debt-back-default="/debt/credit-cards#cc-payoff-scenarios">← Back to credit cards</a>
    </p>

    <section class="debt-hero cc-payoff-tier-hero">
      <span class="label">{tier["label"]} · {tier["range"]}</span>
      <h1>{tier["h1"]}</h1>
      <p class="lead">{tier["hero_lead"]}</p>
      {render_jump(tier["jump"])}
    </section>

    <section class="housing-hub-panel cc-payoff-tier-intro" id="overview" aria-labelledby="overview-title">
      <header class="housing-hub-section-head">
        <p class="housing-hub-kicker debt-credit-cards-hub-kicker--violet">💸 Start here</p>
        <h2 id="overview-title">Who this guide is for</h2>
      </header>
      <div class="debt-page-prose">{tier["prose"]}
      </div>
      <aside class="what-this-means cc-payoff-tier-glance" role="note">
        <p class="what-this-means__title">At a glance</p>
        <p>Balance range: <strong>{tier["range"]}</strong>. Pick a fixed monthly payment above your interest charge. Use our calculators to see your real debt-free date—not a guess.</p>
      </aside>
    </section>

    <section class="housing-hub-panel cc-payoff-tier-math" id="math" aria-labelledby="math-title">
      <header class="housing-hub-section-head">
        <p class="housing-hub-kicker">📊 The math</p>
        <h2 id="math-title">How payment size changes interest and timeline</h2>
      </header>
      <p class="debt-page-prose">Same balance. Same APR. The only variable is how much you pay each month. Small bumps above the minimum save thousands in total interest.</p>
      {render_table(tier["table_caption"], tier["table_rows"])}
      <p class="debt-credit-cards-child-cta cc-payoff-tier-cta">
        <a class="debt-topic-explore-btn" href="/debt/credit-cards/credit-card-payoff-calculator#payoff">Run your numbers in the payoff calculator</a>
        <a class="debt-topic-explore-btn debt-topic-explore-btn--secondary" href="/debt/credit-cards/credit-card-interest-calculator">Estimate total interest</a>
      </p>
    </section>

    <section class="housing-hub-panel cc-payoff-tier-plan" id="plan" aria-labelledby="plan-title">
      <header class="housing-hub-section-head">
        <p class="housing-hub-kicker debt-credit-cards-hub-kicker--teal">✅ Your plan</p>
        <h2 id="plan-title">Step-by-step payoff checklist</h2>
      </header>
      {render_plan(tier["plan_steps"])}
      <h3 class="cc-payoff-tier-subhead">Mistakes to avoid</h3>
      {render_mistakes(tier["mistakes"])}
    </section>

    {scenarios_html}

    <section class="housing-hub-panel cc-payoff-tier-tools" aria-labelledby="tools-title">
      <header class="housing-hub-section-head">
        <p class="housing-hub-kicker">🧮 Tools</p>
        <h2 id="tools-title">Calculators that match this balance range</h2>
      </header>
      <div class="interlink-grid">
        <a class="interlink-card" href="/debt/credit-cards/credit-card-payoff-calculator#payoff">
          <h3>Payoff calculator</h3>
          <p>Enter balance, APR, and payment—get your debt-free date and year-by-year timeline.</p>
          <span class="interlink-cta">Open calculator</span>
        </a>
        <a class="interlink-card" href="/debt/credit-cards/minimum-payment-calculator">
          <h3>Minimum payment calculator</h3>
          <p>See how issuer minimums compare to a fixed payment—and why minimums stretch payoff for years.</p>
          <span class="interlink-cta">Estimate minimum</span>
        </a>
        <a class="interlink-card" href="/debt/credit-cards/credit-card-interest-calculator">
          <h3>Interest calculator</h3>
          <p>Daily interest, month-one finance charges, and total interest over the life of your debt.</p>
          <span class="interlink-cta">Calculate interest</span>
        </a>
      </div>
    </section>

    {render_faq(tier["faq"])}

    <section aria-label="Other balance ranges" class="interlink-section cc-payoff-tier-related">
      <h2>Other balance ranges</h2>
      <div class="interlink-grid">
        <a class="interlink-card" href="{related_href}">
          <h3>{related_label}</h3>
          <p>Continue to the next guide in our payoff series.</p>
          <span class="interlink-cta">Read guide</span>
        </a>
        <a class="interlink-card" href="/debt/credit-cards">
          <h3>Credit cards hub</h3>
          <p>All calculators, APR guides, and payoff strategies in one place.</p>
          <span class="interlink-cta">Back to hub</span>
        </a>
      </div>
    </section>

    <aside class="eeat-trust cc-payoff-tier-trust" aria-labelledby="trust-title">
      <header class="eeat-trust__header">
        <span class="eeat-trust__kicker">🔒 Methodology</span>
        <h2 id="trust-title" class="eeat-trust__title">How we build payoff guides</h2>
        <p class="eeat-trust__meta"><time datetime="2026-06-01">Last reviewed: June 2026</time> · <a href="/calculator-methodology">Calculator methodology</a> · <a href="/editorial-policy">Editorial policy</a></p>
      </header>
      <p class="debt-page-prose">Timeline and interest examples use monthly amortization at fixed payments—educational models, not quotes from your bank. Real issuers may use average daily balance methods and changing minimums. Always verify with your statement. Sources: <a href="https://www.consumerfinance.gov/" rel="noopener">CFPB</a>, <a href="https://www.federalreserve.gov/releases/g19/current/" rel="noopener">Federal Reserve G.19</a> average APR data.</p>
    </aside>
  </main>

{FOOTER}
</body>
</html>
'''


def main() -> None:
    for tier in TIERS:
        out = ROOT / HUB / tier["slug"] / "index.html"
        out.parent.mkdir(parents=True, exist_ok=True)
        html = render_page(tier)
        out.write_text(html, encoding="utf-8")
        words = len(" ".join(html.split()).split())
        print(f"Wrote {out.relative_to(ROOT)} (~{words} words in file)")


if __name__ == "__main__":
    main()
