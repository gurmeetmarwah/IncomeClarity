"""Extended state-specific content for house affordability state pages."""
from __future__ import annotations

STATE_EXTENDED: dict[str, dict] = {
    "texas": {
        "long_tail": [
            {
                "h2": "How much house can I afford in Texas on $90,000?",
                "paras": [
                    "At $90,000 gross, the 28% rule caps your full housing payment near $2,100 a month. That often supports a home near $280,000–$320,000 with 20% down at 6.5% — more in Houston, less in Austin.",
                    "Texas has no state income tax, so your take-home pay is higher than California or New York at the same gross. Still run property tax in the calculator — it is often $400+ a month on a $300k home.",
                    "If you carry $400 in car and student loan payments, the 36% back-end cap may bind before the 28% housing line. Enter real debts in the form above.",
                ],
            },
            {
                "h2": "Texas property tax and why it changes your max price",
                "paras": [
                    "Texas schools and local services are funded largely through property tax, not income tax. Effective rates near 1.6% mean a $345,000 home can carry $460 a month in tax alone.",
                    "Tax districts differ by county, city, and school district. A home in Collin County may tax differently than the same list price in Harris County. Use the seller's tax certificate, not a statewide average.",
                    "Homestead exemptions help after you buy, but your first-year bill still tracks purchase price. Budget the full assessed amount when you set a max list price.",
                ],
            },
            {
                "h2": "What salary do you need to buy a house in Texas?",
                "paras": [
                    "For a median home near $345,000 with 20% down, plan on $85,000–$100,000 gross at 6.5% with modest debt. Houston and San Antonio often fit below that; Austin runs higher.",
                    "Dual income is common in DFW and Houston suburbs. Two earners at $50k–$60k each can often land in Comfortable stress below the state median.",
                    "Open a city page before you trust the state median alone. Austin median near $485k needs far more gross pay than Houston near $310k.",
                ],
            },
        ],
        "rent_vs_buy": "Texas rent is moderate in many metros, and property tax is high — so buying is not automatic math. If you stay five to seven years and lock a rate, equity often beats renting in Houston and DFW suburbs. Run your timeline in the rent vs buy tool.",
        "buyer_tips": [
            "Pull flood maps on Gulf Coast and Houston-area listings before you offer.",
            "Ask for MUD, PID, and ISD tax lines on new construction — they add to the monthly bill.",
            "Compare Houston, Dallas, and Austin city pages if you are flexible on job location.",
            "Get a wind and hail quote early — roof age changes premiums fast.",
        ],
        "extra_narrative": [
            "Texas is a spread-out state with very different metros. The statewide median near $345k blends affordable Houston stock with pricier Austin and DFW suburbs.",
            "Migration from California and the Midwest pushed prices in some rings after 2020. Competition cooled from peak years but popular school zones still see multiple offers.",
            "Energy, tech, and healthcare jobs anchor wages. Remote workers keeping coastal salaries helped Austin demand — still model a pay-cut case before you max out.",
            "Summer electric on large suburban homes can add $200+ a month. Budget utilities outside PITI when you compare cities.",
        ],
        "extra_faqs": [
            ("Can I afford a $400k home in Texas on $100k?", "Often yes with 20% down and low debt in Houston or DFW suburbs. Austin at $400k may feel Moderate to Stretched depending on HOA and tax district."),
            ("Is Texas cheaper than California for buyers?", "List prices are lower and there is no state income tax. Property tax and insurance still stack up — compare full PITI, not list price alone."),
            ("How much down payment do Texas buyers use?", "20% avoids PMI and strengthens offers. FHA and VA loans allow less — still run the full payment through our calculator."),
            ("Which Texas city is most affordable?", "Houston median is lowest among our featured cities. Austin is highest. Open each city page for local tax and insurance defaults."),
        ],
    },
    "california": {
        "long_tail": [
            {
                "h2": "How much house can I afford in California on $150,000?",
                "paras": [
                    "At $150,000 gross, the 28% cap is about $3,500 a month for housing. That often fits an inland home near $550,000–$650,000 — not a coastal listing above $850,000 at today's rates.",
                    "State income tax lowers take-home pay. Run our California take-home tool before you shop. A $150k salary in CA does not spend like $150k in Texas after tax.",
                    "Insurance in fire-prone zip codes can add $200–$400 a month above our default. Get a quote with the address before you set your max price.",
                ],
            },
            {
                "h2": "California property tax, Prop 13, and Mello-Roos",
                "paras": [
                    "Prop 13 limits how fast your assessed tax can rise after you buy. Your first-year bill still depends on purchase price — typically near 0.75% effective in our state model.",
                    "Mello-Roos and special tax districts on newer tracts can add hundreds a month. Ask the seller for the full annual tax bill, not just the current owner's assessed value.",
                    "Coastal counties often assess higher insurance risk. Tax may look modest next to insurance and HOA on condos.",
                ],
            },
            {
                "h2": "What salary do you need to buy a house in California?",
                "paras": [
                    "For the state median near $785,000 with 20% down, many buyers need $220,000+ gross to hug the 28% line at 6.5%. Coastal metros need more; inland cities may fit $120k–$160k.",
                    "Dual income is standard in LA and the Bay Area. Two earners at $100k each still may not clear a median coastal list price once tax, HOA, and insurance stack up.",
                    "Start with your city page — Los Angeles, San Francisco, and San Diego each have different medians and insurance defaults.",
                ],
            },
        ],
        "rent_vs_buy": "California rent is high, and so is the buy-in. Buying often pays off only on longer timelines in stable zip codes. If you might move in three years, renting while saving a larger down payment may be smarter — especially with high insurance in fire zones.",
        "buyer_tips": [
            "Get an insurance quote with the full address — not a state average.",
            "Read HOA and reserve studies on condos before you waive inspection.",
            "Compare inland vs coastal city pages if commute is flexible.",
            "Run the calculator at 10% and 20% down to see PMI impact.",
        ],
        "extra_narrative": [
            "California is not one housing market. The state median blends $1M+ coastal stock with more reachable inland cities. Your target county may sit far from the number on this page.",
            "Wildfire insurance reforms changed premiums in many zip codes. A home that looked affordable on list price may fail the full PITI test once insurance is real.",
            "Tech, entertainment, and government jobs mix with tourism wages. Lenders use W-2 or two-year averages for variable income — plan on stable pay.",
            "Many buyers use gift funds or co-buyers. Still run the stress meter on income you control long term.",
        ],
        "extra_faqs": [
            ("Is California worth buying vs renting?", "Depends on stay length, rate, and insurance. Use rent vs buy with your real timeline and city tax defaults."),
            ("Can I afford California on $120k?", "You may target $450k–$550k inland with 20% down. Coastal medians need far more gross pay."),
            ("Does Prop 13 help new buyers?", "It limits future increases — your first bill still tracks what you pay for the home."),
            ("Which CA city is cheapest in this guide?", "None are cheap by US standards. San Diego and LA medians differ — open each city calculator."),
        ],
    },
    "florida": {
        "long_tail": [
            {
                "h2": "How much house can I afford in Florida on $80,000?",
                "paras": [
                    "At $80,000 gross, the 28% cap is about $1,867 a month. That often maps to $260,000–$300,000 with 20% down at 6.5% — below the state median near $395,000.",
                    "Florida has no state income tax, which helps take-home pay. Storm insurance and HOA often take that back on the monthly bill, especially on the coast.",
                    "Flood insurance is separate in many zones and can add $100–$300 a month. Budget it before you fall in love with a waterfront listing.",
                ],
            },
            {
                "h2": "Florida homeowners insurance and HOA costs",
                "paras": [
                    "Hurricane risk pushed premiums up statewide. Roof age, construction type, and distance to the coast change quotes block by block.",
                    "Condos carry HOA and reserve requirements that lenders now scrutinize. A low list price with high HOA can fail the 28% rule.",
                    "Our state default insurance near 0.55% of value is a planning figure — coastal Miami runs higher than inland Orlando.",
                ],
            },
            {
                "h2": "What salary do you need to buy a house in Florida?",
                "paras": [
                    "For a median home near $395,000 with 20% down, plan on $100,000–$115,000 gross at 6.5% with modest debt. Miami needs more; Tampa and Orlando vary by zip.",
                    "Tourism and service wages lag list prices in Miami. Dual income is common for median-priced homes in Orlando and Tampa.",
                    "Compare Miami, Tampa, and Orlando city pages — the statewide median hides a wide gap between coastal condos and inland suburbs.",
                ],
            },
        ],
        "rent_vs_buy": "Florida rent rose with migration after 2020. Buying works when insurance, HOA, and your stay timeline align. Coastal condos need stable reserves — run five- and seven-year cases in rent vs buy.",
        "buyer_tips": [
            "Get wind and flood quotes during inspection period, not at closing.",
            "Read condo milestone inspection and reserve study on older buildings.",
            "Ask about CDD fees on new master-planned communities.",
            "Compare Miami vs Tampa city pages if job location is flexible.",
        ],
        "extra_narrative": [
            "Florida's state median near $395k blends Miami condo prices with more reachable Tampa and Orlando suburbs. Insurance drives more of the payment than in many states.",
            "No state income tax attracts relocators from NY and NJ. Hot zip codes still see competition — use the stress label, not your lender max alone.",
            "Flood maps changed after recent storms. A block that looked safe on a map may rate differently today.",
            "Short-term rental rules vary by HOA and county. Verify before you buy an investment unit.",
        ],
        "extra_faqs": [
            ("Do I need flood insurance in Florida?", "Many lenders require it in Zone A or V. Even optional coverage is worth quoting near water."),
            ("Is Florida cheaper than New York to buy?", "List can be lower and there is no state income tax. Insurance and HOA on coastal condos can narrow the gap."),
            ("Can I afford Florida on $70k?", "You may target $220k–$260k with 20% down and low debt. Median $395k needs higher income or a larger down payment."),
            ("Which Florida city is most affordable?", "Orlando and Tampa are more reachable than Miami for many incomes. Open each city page for local defaults."),
        ],
    },
    "new-york": {
        "long_tail": [
            {
                "h2": "How much house can I afford in New York on $100,000?",
                "paras": [
                    "At $100,000 gross, the 28% cap is about $2,333 a month. In Buffalo or Albany that can fit a home near $280,000–$320,000 with 20% down. In NYC, the same income shops far below the median condo price.",
                    "State income tax cuts take-home pay. NYC residents also pay city income tax. Run our New York take-home tool before you trust gross salary in the calculator.",
                    "Co-op maintenance can add $800+ a month in some buildings — raise HOA in the calculator to match the listing.",
                ],
            },
            {
                "h2": "New York property tax: upstate vs NYC",
                "paras": [
                    "Upstate cities like Buffalo carry higher tax rates on lower list prices. NYC rates look lower on paper but assessed values and maintenance fees run high.",
                    "Our state model uses about 1.4% effective tax — your county bill may differ. Always use the seller's tax certificate for planning.",
                    "Winter heat and roof work on older upstate stock add cost beyond PITI. Budget maintenance on pre-1980 homes.",
                ],
            },
            {
                "h2": "What salary do you need to buy a house in New York state?",
                "paras": [
                    "For the statewide median near $425,000 with 20% down, plan on $105,000–$125,000 gross at 6.5% in upstate metros. NYC median condos often need $180,000+ gross.",
                    "New York is two markets in one state. Buffalo fits middle incomes better than Manhattan or Brooklyn. Use a city page before you trust the state median.",
                    "Dual income helps in Albany and NYC suburbs. Run the calculator with all monthly debts — the 36% rule includes car loans and cards.",
                ],
            },
        ],
        "rent_vs_buy": "Downstate rent is high but so are co-op fees and closing costs. Upstate buying can beat renting on shorter timelines. Run rent vs buy with maintenance and tax, not mortgage alone.",
        "buyer_tips": [
            "Open the NYC city page if you shop co-ops — maintenance is often the wild card.",
            "Budget heat and snow removal on older upstate homes.",
            "Compare Buffalo and Albany pages if you are flexible within the state.",
            "Check school and county tax lines — they change the monthly bill.",
        ],
        "extra_narrative": [
            "New York spans affordable upstate cities and among the priciest housing in the US downstate. The statewide median is a midpoint almost no single buyer should use alone.",
            "State government and healthcare jobs stabilize Albany. Finance and tech wages pull NYC prices. Remote work shifted some demand to Hudson Valley towns.",
            "Co-op board approval can take months and require higher down payments than banks alone. Budget time and cash for board packages.",
            "Compared to Florida, NY trades income tax for somewhat lower insurance on many homes — but NYC maintenance fees reverse that advantage.",
        ],
        "extra_faqs": [
            ("Is upstate NY affordable for first-time buyers?", "Buffalo and Albany offer lower list prices than NYC. Still inspect older homes carefully and budget winter costs."),
            ("Can I afford NYC on $120k?", "Outer-borough studios may work — not a median condo with high maintenance. Use the NYC city page."),
            ("How does NY tax affect home buying?", "State and city tax lower take-home pay. Same gross buys less house than in Texas or Florida after tax."),
            ("Which NY city is cheapest to buy?", "Buffalo has the lowest median in our guide. NYC is the highest by a wide margin."),
        ],
    },
}
