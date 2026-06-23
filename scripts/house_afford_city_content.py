"""Extended city-specific content for house affordability pages."""
from __future__ import annotations

# Key: (state_slug, city_slug)
EXTENDED: dict[tuple[str, str], dict] = {
    ("california", "los-angeles"): {
        "neighborhoods": [
            {"name": "San Fernando Valley", "range": "$650k–$900k", "note": "More space and yards. Commute to the Westside can run 45–75 minutes at rush hour."},
            {"name": "South Bay", "range": "$750k–$1.1M", "note": "Beach-adjacent blocks cost more. Insurance quotes vary by wildfire zone."},
            {"name": "East LA / Boyle Heights", "range": "$550k–$750k", "note": "Lower list prices than the Westside. Still above many US metros."},
            {"name": "Downtown / Koreatown", "range": "$500k–$700k", "note": "Condos and older stock. Read HOA docs and parking rules before you offer."},
        ],
        "long_tail": [
            {
                "h2": "How much house can I afford in Los Angeles on $150k?",
                "paras": [
                    "At $150,000 gross, the 28% rule caps your full housing payment near $3,500 a month. That often maps to a home near $550,000–$650,000 with 20% down at 6.5% — not the citywide median near $875,000.",
                    "State income tax lowers take-home pay. Run our California take-home tool first. Then enter your real car payment and student loans in the calculator. Other debt shrinks the 36% back-end cap.",
                    "If you earn $150k and want a Westside zip, plan a larger down payment or a condo below $600k. Many buyers pair two incomes and still shop under the median list price.",
                ],
            },
            {
                "h2": "What salary do you need to buy a house in Los Angeles?",
                "paras": [
                    "For a median home near $875,000 with 20% down, many lenders want gross pay near $200,000+ to stay inside the 28% line at today's rates. That is a planning figure — your quote and debts change the number.",
                    "Dual income is common. Two earners at $100k each do not always clear a $900k list price once tax, HOA, and insurance stack up. Use the stress label in the calculator, not the pre-approval letter alone.",
                    "First-time buyers often target $600k–$700k in the Valley or Eastside. That keeps the monthly payment in Moderate instead of Stretched on one or two middle incomes.",
                ],
            },
            {
                "h2": "LA property tax, insurance, and HOA on a typical home",
                "paras": [
                    "LA County property tax often runs near 0.72% of assessed value. On an $875,000 purchase, that is about $525 a month in year one. Prop 13 limits how fast tax can rise after you buy.",
                    "Wildfire insurance changed the math in many zip codes. A quote can add $200–$400 a month above a national average. Get a quote with the full address before you set your max price.",
                    "Condos and townhomes may add HOA near $275 a month or more. Special assessments can hit like a second mortgage. Read the HOA packet before you waive inspection.",
                ],
            },
        ],
        "rent_vs_buy": "Median rent near $2,600 makes buying a long game in LA. If you stay five to seven years and your rate is fixed, equity can beat renting in stable zip codes. If you might move in two years, renting while you save a larger down payment is often smarter.",
        "buyer_tips": [
            "Get an insurance quote with the listing address — not a state average.",
            "Budget Mello-Roos and supplemental tax on newer tracts in the Valley.",
            "Compare condo HOA and reserve funds; low HOA can mean a future special assessment.",
            "Run the calculator at 10% down and 20% down to see PMI impact.",
        ],
        "extra_narrative": [
            "Los Angeles is not one price map. The citywide median blends the Valley, South Bay, and Westside. Your target neighborhood may sit $200,000 above or below the number on this page.",
            "Traffic shapes real affordability. A cheaper home with a 90-minute round trip adds gas, wear, and time cost. Some buyers pay more for housing to cut the commute.",
            "Entertainment and gig income can vary month to month. Lenders use W-2 or two-year averages for self-employment. Plan your down payment on stable income, not your best quarter.",
            "Many LA buyers use gift funds or co-buyers with family. If that applies to you, still run the stress meter on your own income in case the gift is one-time.",
        ],
        "extra_faqs": [
            ("Can I afford a $700k house in Los Angeles?", "On $150k–$175k gross with 20% down and modest debt, $700k is often in range. Above $200k list on one income usually needs a larger down payment or lower rate."),
            ("Is it better to buy a condo or house in LA?", "Condos can lower the list price but HOA and reserves matter. Houses offer space but insurance in fire zones can be steep."),
            ("How much down payment do LA buyers use?", "20% avoids PMI and strengthens offers. Many first-time buyers use 10% with PMI — the same income buys less house."),
            ("Does LA have first-time buyer programs?", "CalHFA and local programs exist. They may help with down payment — still run the full PITI through our calculator."),
        ],
        "col_link": "/living/housing/cost-of-living-by-city/california/los-angeles",
        "salary_link": "/living/lifestyle/comfortable-salary/california/los-angeles",
        "scenario_links": [
            ("$100k in LA", "/living/lifestyle/comfortable-salary/california/los-angeles/is-100k-enough-to-live-in-los-angeles"),
            ("$150k in LA", "/living/lifestyle/comfortable-salary/california/los-angeles/is-150k-enough-to-live-in-los-angeles"),
        ],
    },
    ("california", "san-francisco"): {
        "neighborhoods": [
            {"name": "Mission / Bernal", "range": "$900k–$1.3M", "note": "Dense condo stock. HOA and reserves vary by building age."},
            {"name": "Sunset / Richmond", "range": "$1M–$1.4M", "note": "More single-family homes. Fog belt prices still top US norms."},
            {"name": "SoMa / South Beach", "range": "$1.1M–$1.8M", "note": "High-rise condos with HOA often above $500 a month."},
            {"name": "Oakland (nearby)", "range": "$650k–$950k", "note": "Not SF proper but common for buyers who work in the city."},
        ],
        "long_tail": [
            {
                "h2": "How much house can I afford in San Francisco on $200k?",
                "paras": [
                    "At $200,000 gross, the 28% cap is about $4,667 a month for housing. That can support a smaller condo near $900,000–$1,000,000 with 20% down — not the citywide median near $1.25M.",
                    "Co-op and condo fees eat cash flow. Our default HOA is $450 a month; luxury buildings run higher. Add that before you compare list price to income.",
                    "Tech stock and bonus income may not count fully in underwriting. Use base salary in the calculator, then see if RSU income changes your comfort level.",
                ],
            },
            {
                "h2": "San Francisco co-op vs condo: what changes your payment",
                "paras": [
                    "Co-ops may need 25–50% down and board approval. Monthly maintenance can include property tax and building debt — not just amenities.",
                    "Condos have clearer HOA lines but still carry reserve risk. Older buildings faced insurance and inspection scrutiny after statewide reforms.",
                    "Run two scenarios: one at list price and one $150k below. The stress label shifts fast when HOA is high.",
                ],
            },
            {
                "h2": "What income do you need to buy in San Francisco?",
                "paras": [
                    "For a median unit near $1.25M with 20% down, plan on $250,000+ gross to sit near the 28% line at 6.5%. Many buyers earn less and shop smaller units or outer neighborhoods.",
                    "Dual income above $200k each is common in tech-heavy buildings. Still model student loans and car payments — the 36% rule includes all debt.",
                    "Renting while saving a 20% down payment is a common path. Use rent vs buy with your real stay timeline before you rush an offer.",
                ],
            },
        ],
        "rent_vs_buy": "SF rent is high but so is the entry price for ownership. Buying often pays off only if you stay seven to ten years and your building's finances stay stable. Run your break-even with real HOA and tax.",
        "buyer_tips": [
            "Read co-op financials and board minutes before you pay for an inspection.",
            "Ask for the building's insurance quote history — some associations faced huge hikes.",
            "Model a pay-cut scenario if you work in tech — do not max out on bonus income.",
            "Compare Oakland and Peninsula listings if you need space under $1M.",
        ],
        "extra_narrative": [
            "San Francisco prices reflect scarce land and high wages. The median is not what most $140k earners buy without help from savings, family, or a second income.",
            "Remote work shifted some demand to suburbs. City condos still compete with cash buyers in popular buildings.",
            "Parking, storage, and move-in fees can add $50k+ to your real cost. Ask the listing agent for one-time building charges.",
            "Earthquake insurance is separate from fire and liability. Budget it if your lender or building requires it.",
        ],
        "extra_faqs": [
            ("Can you buy in SF on $150k salary?", "You may qualify for a small condo in outer neighborhoods — not a median $1.25M unit. Run the calculator with your real debts."),
            ("Why is San Francisco HOA so high?", "Labor, reserves, and insurance in dense buildings push fees up. Low HOA can signal deferred maintenance."),
            ("Is SF property tax lower than LA?", "Rates look lower on paper but assessed values are high. Maintenance fees are often the bigger swing factor."),
            ("Should I buy in SF or rent?", "If you might leave in three years, renting is often cheaper after closing costs and HOA. Use our rent vs buy tool with your timeline."),
        ],
        "col_link": "/living/housing/cost-of-living-by-city/california/san-francisco",
        "salary_link": "/living/lifestyle/comfortable-salary/california/san-francisco",
        "scenario_links": [
            ("$150k in SF", "/living/lifestyle/comfortable-salary/california/san-francisco/is-150k-enough-to-live-in-san-francisco"),
            ("$200k in SF", "/living/lifestyle/comfortable-salary/california/san-francisco/is-200k-enough-to-live-in-san-francisco"),
        ],
    },
    ("california", "san-diego"): {
        "neighborhoods": [
            {"name": "North Park / Hillcrest", "range": "$750k–$950k", "note": "Walkable urban pockets. Older homes may need seismic or roof work."},
            {"name": "East County", "range": "$550k–$750k", "note": "More house per dollar. Longer commute to coastal job centers."},
            {"name": "La Jolla / Coastal", "range": "$1.2M+", "note": "Premium zip codes above county median. Insurance runs higher near the coast."},
            {"name": "Chula Vista / South Bay", "range": "$600k–$800k", "note": "Popular with families. Check Mello-Roos on newer master plans."},
        ],
        "long_tail": [
            {
                "h2": "How much house can I afford in San Diego on $120k?",
                "paras": [
                    "At $120,000 gross, the 28% rule allows about $2,800 a month for housing. That often fits a home near $550,000–$650,000 with 20% down — below the county median near $920,000.",
                    "Military BAH can help service members qualify. Civilians should use W-2 gross in the form. Do not count BAH twice if it is already in your pay.",
                    "Insurance near the coast runs higher than East County. A La Jolla quote can change your max price by $200 a month.",
                ],
            },
            {
                "h2": "San Diego Mello-Roos and property tax explained",
                "paras": [
                    "Some new builds carry Mello-Roos special tax on top of Prop 13 tax. Ask the seller for the full annual tax bill before you offer.",
                    "Our model uses about 0.73% effective tax. Your first-year bill tracks purchase price, not the seller's assessed value.",
                    "HOA in planned communities often runs $300+ a month. Enter the real HOA from the listing, not our default alone.",
                ],
            },
            {
                "h2": "What salary do you need for a median San Diego home?",
                "paras": [
                    "For a home near $920,000 with 20% down, many buyers need $210,000+ gross to hug the 28% line at 6.5%. Biotech and military wages help but coastal list prices still outpace median income near $95k.",
                    "Dual income is common in North Park and South Bay. Run the calculator with both incomes combined only if both are on the loan.",
                    "Townhomes below $700k can land in Moderate stress for $120k–$150k households with low debt.",
                ],
            },
        ],
        "rent_vs_buy": "San Diego rent near $2,550 makes buying attractive if you stay put. Coastal premiums mean your break-even may take longer than inland metros. Model five- and ten-year stays.",
        "buyer_tips": [
            "Ask for Mello-Roos disclosure on any home built after 2000.",
            "Get wind and fire quotes early in coastal canyons.",
            "If you use BAH, confirm with your lender how it counts toward housing ratio.",
            "Compare Chula Vista and East County if the median feels out of reach.",
        ],
        "extra_narrative": [
            "San Diego mixes military, biotech, and tourism wages. Median income near $95k does not always match coastal list prices above $900k.",
            "Seasonal tourism can affect short-term rental rules in some zones. Check HOA if you plan to rent a room.",
            "Water and utility tiers rise in summer. Budget $50–$100 more in peak months for older homes without solar.",
            "Competition softened in some zip codes after 2023. Still use the stress label — do not shop at your lender max alone.",
        ],
        "extra_faqs": [
            ("Is San Diego cheaper than Los Angeles?", "Median list is slightly higher than LA in our model but insurance and tax differ by zip. Compare both city calculators."),
            ("Can military BAH cover a San Diego mortgage?", "BAH can help you qualify but the home must fit BAH plus your other income rules. Run the full PITI."),
            ("How much down for a San Diego condo?", "20% is ideal. Some buildings require 25% for investors — check HOA rental caps."),
            ("What about Tijuana commute buyers?", "Some workers live in Mexico and commute — lenders may have different rules. This page models US purchase only."),
        ],
        "col_link": "/living/housing/cost-of-living-by-city/california/san-diego",
        "salary_link": "/living/lifestyle/comfortable-salary/california/san-diego",
        "scenario_links": [
            ("$100k in San Diego", "/living/lifestyle/comfortable-salary/california/san-diego/is-100k-enough-to-live-in-san-diego"),
            ("$200k in San Diego", "/living/lifestyle/comfortable-salary/california/san-diego/is-200k-enough-to-live-in-san-diego"),
        ],
    },
    ("texas", "houston"): {
        "neighborhoods": [
            {"name": "The Woodlands", "range": "$400k–$550k", "note": "Master-planned suburbs with HOA. Strong schools drive demand."},
            {"name": "Katy / Cinco Ranch", "range": "$350k–$480k", "note": "Family-friendly. Commute to Energy Corridor or Galleria."},
            {"name": "Inner Loop", "range": "$380k–$520k", "note": "Older homes, smaller lots. Flood zone checks are critical."},
            {"name": "Pearland / Friendswood", "range": "$320k–$420k", "note": "Often below Houston median. Still verify flood and wind insurance."},
        ],
        "long_tail": [
            {
                "h2": "How much house can I afford in Houston on $80k?",
                "paras": [
                    "At $80,000 gross, the 28% cap is about $1,867 a month. That often supports a home near $250,000–$290,000 with 20% down at 6.5%.",
                    "Texas has no state income tax, so take-home pay helps versus California at the same gross. Property tax near 1.65% still adds $400+ a month on a $300k home.",
                    "If you have $500 a month in car and student debt, the 36% back-end cap may bind before the 28% housing rule. Enter real debts in the calculator.",
                ],
            },
            {
                "h2": "Houston flood zones and insurance costs",
                "paras": [
                    "Harvey showed that flood risk is not only on the coast. Check FEMA maps and get a flood quote even outside mandatory zones.",
                    "Wind and hail coverage can rival property tax on older roofs. Some carriers ask for a roof age inspection at renewal.",
                    "A home that looks cheap on list price may fail the full PITI test once insurance is real.",
                ],
            },
            {
                "h2": "What salary for a median Houston home?",
                "paras": [
                    "For a median home near $310,000 with 20% down, plan on $75,000–$90,000 gross at 6.5% with modest debt. Houston is among the more reachable big Texas metros.",
                    "Energy and medical jobs anchor wages. Dual income at $70k each often lands in Comfortable stress below the median.",
                    "Suburbs trade commute time for space. Gas and tolls are real costs — do not ignore them when you stretch the payment.",
                ],
            },
        ],
        "rent_vs_buy": "Houston rent near $1,400 and lower list prices make buying workable after five to seven years in many suburbs. Flood insurance can tilt the math — include it in rent vs buy.",
        "buyer_tips": [
            "Pull a flood map for every address you like.",
            "Ask for the seller's tax certificate — MUD and ISD lines change the bill.",
            "Budget roof and HVAC reserves on 1980s stock in the Loop.",
            "Compare Katy and Pearland if the Inner Loop median feels tight.",
        ],
        "extra_narrative": [
            "Houston sprawls across counties with different tax rates. The median price is a midpoint — The Woodlands runs higher, some east-side blocks lower.",
            "No zoning means land use varies block to block. Check what's planned next door before you buy.",
            "Humidity and foundation issues show up on inspection. Set aside cash for pier work on older slabs.",
            "Job growth in energy and healthcare supports demand. Still run the stress meter — stretched buyers feel rate hikes fast.",
        ],
        "extra_faqs": [
            ("Is Houston cheaper than Austin?", "Yes on median price. Austin wages are higher but list prices rose faster in the 2020s."),
            ("Do I need flood insurance in Houston?", "Many lenders require it in Zone A or V. Even in X zones, optional coverage is worth quoting."),
            ("How high is Houston property tax?", "Near 1.65% of value in our model — often $425+ a month on a $310k home."),
            ("Can I afford a $350k home on $90k?", "Often yes with 20% down and low debt. Run the calculator with your real car payment."),
        ],
        "col_link": "/living/housing/cost-of-living-by-city/texas/houston",
        "salary_link": "/living/lifestyle/comfortable-salary/texas/houston",
        "scenario_links": [
            ("$75k in Houston", "/living/lifestyle/comfortable-salary/texas/houston/is-75k-enough-to-live-in-houston"),
            ("$100k in Houston", "/living/lifestyle/comfortable-salary/texas/houston/is-100k-enough-to-live-in-houston"),
        ],
    },
    ("texas", "dallas"): {
        "neighborhoods": [
            {"name": "Plano / Frisco", "range": "$450k–$600k", "note": "Corporate jobs and strong schools. HOA common in new builds."},
            {"name": "Oak Cliff / Bishop Arts", "range": "$320k–$450k", "note": "Urban reinvestment zone. Prices rose with migration from coastal states."},
            {"name": "Garland / Richardson", "range": "$300k–$380k", "note": "Often below DFW median. Good rail access in some pockets."},
            {"name": "Fort Worth (DFW)", "range": "$280k–$400k", "note": "Western half of the metro often cheaper than Dallas proper."},
        ],
        "long_tail": [
            {
                "h2": "How much house can I afford in Dallas on $100k?",
                "paras": [
                    "At $100,000 gross, the 28% line is about $2,333 a month. That often maps to $320,000–$380,000 with 20% down at 6.5% — near or below the metro median near $385,000.",
                    "Property tax near 1.7% is a big line item. On a $350k home that is roughly $495 a month before insurance.",
                    "DFW spans many tax districts. Use the listing's tax certificate, not a statewide guess.",
                ],
            },
            {
                "h2": "Dallas property tax and HOA in master-planned suburbs",
                "paras": [
                    "Texas schools are funded largely through property tax. A low list price does not mean a low tax bill.",
                    "HOA near $85 a month is our default — Plano and Frisco plans often run $100–$200.",
                    "MUD taxes on new developments can add $200+ a month until bonds pay down.",
                ],
            },
            {
                "h2": "What income do you need for a median Dallas home?",
                "paras": [
                    "For a $385,000 median home with 20% down, plan on $95,000–$110,000 gross at 6.5% with modest debt.",
                    "Tech and finance transfers from coastal states pushed some suburb prices up. Wages near $75k median mean many buyers shop below the median.",
                    "Dual income at $55k–$65k each can reach Comfortable on a $320k home with low debt.",
                ],
            },
        ],
        "rent_vs_buy": "DFW rent near $1,550 and moderate list prices favor buying after five to seven years in many suburbs. Hail insurance and tax still matter — run both sides in rent vs buy.",
        "buyer_tips": [
            "Compare Plano tax vs Dallas city tax on similar list prices.",
            "Ask about MUD and PID fees on new construction.",
            "Hail claims history can raise premiums — check the CLUE report if you can.",
            "Model a longer commute from Fort Worth to see payment vs gas tradeoffs.",
        ],
        "extra_narrative": [
            "Dallas–Fort Worth is a spread-out market. Median price near $385k blends pricey northern suburbs and more affordable southern blocks.",
            "Job growth pulled migration from California and the Midwest. Competition is softer than 2021 but still real in top school zones.",
            "Summer electric bills on large homes can add $200+ a month. Budget utilities beyond PITI.",
            "Foundation and soil movement show up in inspections. Older pier-and-beam homes need a careful structural review.",
        ],
        "extra_faqs": [
            ("Is Dallas more expensive than Houston?", "Median list is higher in Dallas in our data. Property tax rates are similar."),
            ("Do Dallas homes have HOA?", "Many suburbs do. Enter the real HOA from the listing in the calculator."),
            ("Can I afford Dallas on $75k?", "You can often target $250k–$300k with 20% down. Above $350k may feel Stretched with debt."),
            ("What about Collin County vs Dallas County?", "Tax and school lines change the bill. Always use the address-specific rate."),
        ],
        "col_link": "/living/housing/cost-of-living-by-city/texas/dallas",
        "salary_link": "/living/lifestyle/comfortable-salary/texas/dallas",
        "scenario_links": [
            ("$75k in Dallas", "/living/lifestyle/comfortable-salary/texas/dallas/is-75k-enough-to-live-in-dallas"),
            ("$100k in Dallas", "/living/lifestyle/comfortable-salary/texas/dallas/is-100k-enough-to-live-in-dallas"),
        ],
    },
    ("texas", "austin"): {
        "neighborhoods": [
            {"name": "East Austin", "range": "$500k–$700k", "note": "Rapid price growth. Mix of older homes and new builds."},
            {"name": "Round Rock / Cedar Park", "range": "$400k–$520k", "note": "Suburbs popular with tech families. Toll roads add commute cost."},
            {"name": "South Austin", "range": "$450k–$600k", "note": "Hilly terrain and older stock. Check drainage and foundation."},
            {"name": "Pflugerville / Manor", "range": "$350k–$450k", "note": "More reachable for first-time buyers. Longer commute to downtown."},
        ],
        "long_tail": [
            {
                "h2": "How much house can I afford in Austin on $100k?",
                "paras": [
                    "At $100,000 gross, the 28% cap is about $2,333 a month. That often supports $320,000–$380,000 with 20% down — below the city median near $485,000.",
                    "Tech layoffs and remote work shifted demand but median price is still above Houston. Suburbs help if downtown listings feel out of reach.",
                    "Property tax near 1.55% plus HOA on new builds — enter both in the calculator.",
                ],
            },
            {
                "h2": "Austin property tax after homestead exemption",
                "paras": [
                    "Texas homestead caps some annual tax growth but not your first bill after purchase. Budget on full assessed value at close.",
                    "School district lines in Travis and Williamson counties change rates. A $450k home in Round Rock may tax differently than the same price in Austin city.",
                    "Our model uses planning rates — your protest and exemption status can shift the bill after year one.",
                ],
            },
            {
                "h2": "What salary for a median Austin home?",
                "paras": [
                    "For a $485,000 median home with 20% down, plan on $115,000–$130,000 gross at 6.5% with low debt.",
                    "Remote workers keeping coastal salaries helped demand. Still model a pay-cut case before you max out.",
                    "First-time buyers often target $380k–$420k in suburbs to stay Moderate on the stress meter.",
                ],
            },
        ],
        "rent_vs_buy": "Austin rent near $1,750 rose with home prices. Buying wins on longer timelines if you lock a rate and stay in a growing suburb. Run five- and seven-year cases.",
        "buyer_tips": [
            "Check Williamson vs Travis tax on the same list price.",
            "New builds often carry HOA and MUD — get the full fee schedule.",
            "Model toll costs if you commute on 183 or 130.",
            "Run the calculator if you might return to office full-time — commute may push you closer to town.",
        ],
        "extra_narrative": [
            "Austin prices rose fast with tech and migration. Median near $485k is still below California coasts but above Houston.",
            "Music and service wages lag tech pay — dual income or remote coastal salary often makes the median workable.",
            "Summer heat drives electric bills on large homes. Budget $250+ in July on older HVAC.",
            "Competition cooled from 2022 peaks but popular school zones still see multiple offers.",
        ],
        "extra_faqs": [
            ("Is Austin still worth buying vs renting?", "Depends on stay length and rate. Use rent vs buy with your real timeline and HOA."),
            ("How much down for an Austin townhome?", "20% avoids PMI. Some builders offer incentives — still run full PITI."),
            ("Can I afford Austin on $120k?", "You can often target $400k–$450k with 20% down. Median $485k may feel Stretched with debt."),
            ("Austin vs Dallas affordability?", "Dallas median is lower. Austin wages are higher but list prices rose faster."),
        ],
        "col_link": "/living/housing/cost-of-living-by-city/texas/austin",
        "salary_link": "/living/lifestyle/comfortable-salary/texas/austin",
        "scenario_links": [
            ("$100k in Austin", "/living/lifestyle/comfortable-salary/texas/austin/is-100k-enough-to-live-in-austin"),
            ("$150k in Austin", "/living/lifestyle/comfortable-salary/texas/austin/is-150k-enough-to-live-in-austin"),
        ],
    },
    ("florida", "miami"): {
        "neighborhoods": [
            {"name": "Brickell", "range": "$500k–$900k", "note": "High-rise condos. HOA and wind insurance dominate the payment."},
            {"name": "Coral Gables", "range": "$700k–$1.2M", "note": "Single-family premiums. Flood zones along canals matter."},
            {"name": "Hialeah / Westchester", "range": "$400k–$550k", "note": "More reachable than coastal condos. Still check roof age for insurance."},
            {"name": "Fort Lauderdale (nearby)", "range": "$450k–$650k", "note": "Common alternative for buyers priced out of Miami-Dade condos."},
        ],
        "long_tail": [
            {
                "h2": "How much house can I afford in Miami on $75k?",
                "paras": [
                    "At $75,000 gross, the 28% cap is about $1,750 a month. The citywide median near $580,000 is a stretch at that income once insurance and HOA stack up.",
                    "Target $350,000–$420,000 or plan a larger down payment. Condos with high HOA can fail the payment test even when list price looks OK.",
                    "Florida has no state income tax, which helps take-home. Wind insurance often takes that back on coastal units.",
                ],
            },
            {
                "h2": "Miami condo insurance and HOA costs",
                "paras": [
                    "After statewide insurance reforms, older buildings face reserve and inspection rules. Lenders may require higher down payments.",
                    "HOA near $280 a month is a floor in our model. Luxury towers run $800+ with amenities and reserves.",
                    "Wind and flood are separate lines. Budget both before you set a max price.",
                ],
            },
            {
                "h2": "What salary do you need to buy in Miami?",
                "paras": [
                    "For a median home near $580,000 with 20% down, plan on $140,000–$165,000 gross at 6.5% once insurance and HOA are in the stack.",
                    "Median income near $62k leaves a wide gap at the 28% rule. Dual income and larger down payments are common.",
                    "International buyers and cash offers still compete in Brickell. Payment comfort matters more than winning a bidding war.",
                ],
            },
        ],
        "rent_vs_buy": "Miami rent near $2,200 and high insurance make buying a long bet. Condos need stable reserves and insurable roofs. Rent while you save if your stay is under five years.",
        "buyer_tips": [
            "Read the condo's milestone inspection and reserve study.",
            "Get wind and flood quotes before inspection period ends.",
            "Ask if the building is on an insurer's watch list.",
            "Compare Broward listings if Miami-Dade HOA feels too high.",
        ],
        "extra_narrative": [
            "Miami is one of the toughest matches in Florida. Median income and median price sit far apart at the 28% rule.",
            "Tourism and finance wages vary. Lenders want stable W-2 history — commission-heavy jobs need two-year averages.",
            "Flood maps change with sea-level projects. A block that was dry in 2010 may rate differently today.",
            "Parking and special assessments hit older condos hard. Low list price can hide a $30k assessment.",
        ],
        "extra_faqs": [
            ("Why is Miami insurance so high?", "Hurricane risk and reinsurance costs pushed premiums up statewide."),
            ("Can I buy a Miami condo with 10% down?", "Some buildings allow it; others require 25% for investors or weak reserves."),
            ("Is Miami cheaper than NYC?", "List can be lower but insurance and HOA often exceed northeast norms on coastal condos."),
            ("Do I need flood insurance in Miami?", "Many zones yes — it is separate from homeowners and can be $150+ a month."),
        ],
        "col_link": "/living/housing/cost-of-living-by-city/florida/miami",
        "salary_link": "/living/lifestyle/comfortable-salary/florida/miami",
        "scenario_links": [
            ("$100k in Miami", "/living/lifestyle/comfortable-salary/florida/miami/is-100k-enough-to-live-in-miami"),
            ("$150k in Miami", "/living/lifestyle/comfortable-salary/florida/miami/is-150k-enough-to-live-in-miami"),
        ],
    },
    ("florida", "tampa"): {
        "neighborhoods": [
            {"name": "Hyde Park / South Tampa", "range": "$450k–$650k", "note": "Walkable premium. Flood zones near the bay add cost."},
            {"name": "Brandon / Riverview", "range": "$320k–$420k", "note": "Family suburbs east of the city. Often below metro median."},
            {"name": "St. Petersburg", "range": "$350k–$500k", "note": "Pinellas County option with beach access. Check flood maps."},
            {"name": "Pasco / Wesley Chapel", "range": "$300k–$380k", "note": "Fast growth corridor. New builds with HOA common."},
        ],
        "long_tail": [
            {
                "h2": "How much house can I afford in Tampa on $70k?",
                "paras": [
                    "At $70,000 gross, the 28% cap is about $1,633 a month. That often maps to $240,000–$280,000 with 20% down at 6.5%.",
                    "Insurance still runs above the US average. Get a quote early — do not size your max on a national default.",
                    "Flood zones along the bay can add $100–$250 a month. A home that looks affordable on list price may fail PITI.",
                ],
            },
            {
                "h2": "Tampa Bay flood insurance and wind coverage",
                "paras": [
                    "Ian reminded buyers that inland flooding happens. Check FEMA maps even blocks from the water.",
                    "Roof age drives wind premiums. A 15-year shingle may cost more to insure than a new tile roof.",
                    "HOA in new Pasco builds often runs $140+ a month — include it in the calculator.",
                ],
            },
            {
                "h2": "What salary for a median Tampa home?",
                "paras": [
                    "For a $385,000 median home with 20% down, plan on $90,000–$105,000 gross at 6.5% with modest debt.",
                    "Growth after 2020 raised prices but Tampa remains more reachable than Miami for many dual-income households.",
                    "Suburbs in Hillsborough and Pasco trade commute for space — budget gas and tolls.",
                ],
            },
        ],
        "rent_vs_buy": "Tampa rent near $1,650 and mid-range list prices favor buying after five to seven years in stable suburbs. Flood and wind quotes tilt the break-even — include them.",
        "buyer_tips": [
            "Pull flood maps for South Tampa and waterfront blocks.",
            "Compare Hillsborough vs Pinellas tax on similar prices.",
            "Ask for a wind mitigation inspection to lower premiums.",
            "Brandon and Wesley Chapel help if Hyde Park is out of range.",
        ],
        "extra_narrative": [
            "Tampa Bay grew fast after 2020. Median price near $385k is more reachable than Miami for many families.",
            "Healthcare and finance jobs anchor wages. Remote workers from higher-cost states still compete in Hyde Park.",
            "Summer electric on older Florida block homes can spike. Budget $200+ in peak months.",
            "Insurance markets remain tight — start quotes when you start shopping, not at closing.",
        ],
        "extra_faqs": [
            ("Is Tampa cheaper than Orlando?", "Medians are similar in our data. Insurance and commute differ by zip."),
            ("Do I need flood insurance in Tampa?", "Many bay-adjacent zones yes — separate from homeowners."),
            ("Can I afford Tampa on $80k?", "Often yes for $280k–$320k with 20% down and low debt."),
            ("Tampa vs Miami for first-time buyers?", "Tampa median and insurance are usually lower than Miami condos."),
        ],
        "col_link": "/living/housing/cost-of-living-by-city/florida/tampa",
        "salary_link": "/living/lifestyle/comfortable-salary/florida/tampa",
        "scenario_links": [
            ("$80k in Tampa", "/living/lifestyle/comfortable-salary/florida/tampa/is-80k-enough-to-live-in-tampa"),
            ("$100k in Tampa", "/living/lifestyle/comfortable-salary/florida/tampa/is-100k-enough-to-live-in-tampa"),
        ],
    },
    ("florida", "orlando"): {
        "neighborhoods": [
            {"name": "Winter Park", "range": "$450k–$650k", "note": "Premium suburb near downtown. Older homes need roof and HVAC checks."},
            {"name": "Lake Nona", "range": "$400k–$550k", "note": "Medical city growth. New builds with HOA and CDD fees."},
            {"name": "Kissimmee / Osceola", "range": "$300k–$380k", "note": "More reachable for service-sector wages. Tourist-area traffic is real."},
            {"name": "Dr. Phillips", "range": "$420k–$550k", "note": "Popular with families. Good schools drive list prices up."},
        ],
        "long_tail": [
            {
                "h2": "How much house can I afford in Orlando on $65k?",
                "paras": [
                    "At $65,000 gross, the 28% cap is about $1,517 a month. That often fits $220,000–$260,000 with 20% down — below the median near $410,000.",
                    "Tourism wages can lag list prices. Dual income is common for median-priced homes.",
                    "HOA near $125 a month on new subdivisions — enter the real fee from the listing.",
                ],
            },
            {
                "h2": "Orlando HOA and CDD fees on new construction",
                "paras": [
                    "Community Development Districts add tax-like payments on new master plans. Ask for the full CDD schedule.",
                    "Resort-area condos may restrict owner occupancy. Read HOA rental rules if you plan Airbnb.",
                    "Insurance is lower than Miami but not cheap — roof age still matters for wind credits.",
                ],
            },
            {
                "h2": "What income for a median Orlando home?",
                "paras": [
                    "For a $410,000 median home with 20% down, plan on $95,000–$110,000 gross at 6.5%.",
                    "Theme-park and healthcare jobs mix with remote workers. Median income near $64k means many shop below median.",
                    "Townhomes near $320k can land in Moderate stress for dual $50k incomes with low debt.",
                ],
            },
        ],
        "rent_vs_buy": "Orlando rent near $1,600 and tourism-driven job volatility make a five-year stay test important. Buying works when rate, insurance, and job stability align.",
        "buyer_tips": [
            "Ask for CDD and HOA on any home built after 2005.",
            "Compare Orange vs Osceola tax on the same list price.",
            "Budget pest and lawn care on older Florida block homes.",
            "Winter Park premiums may need $110k+ gross — run the calculator early.",
        ],
        "extra_narrative": [
            "Orlando runs on tourism, healthcare, and relocation growth. Wages near $64k median mean two incomes for many median listings.",
            "Lake Nona and Medical City pulled professional wages up. Service jobs still lag list price growth.",
            "Short-term rental rules vary by HOA and county. Verify before you buy an investment unit.",
            "Compared to Tampa, Orlando can be a wash on price depending on zip — compare both calculators if you are flexible.",
        ],
        "extra_faqs": [
            ("Is Orlando cheaper than Miami?", "Median price and insurance are lower. HOA is still common in new builds."),
            ("Can theme-park workers afford Orlando homes?", "Many target below $350k or rent while saving. Dual income helps for median listings."),
            ("What about Disney area condos?", "Tourist corridors have special insurance and HOA rules — read docs carefully."),
            ("Orlando vs Tampa for families?", "Both are mid-range Florida markets. Compare school zones and commute to your job."),
        ],
        "col_link": "/living/housing/cost-of-living-by-city/florida/orlando",
        "salary_link": "/living/lifestyle/comfortable-salary/florida/orlando",
        "scenario_links": [
            ("$80k in Orlando", "/living/lifestyle/comfortable-salary/florida/orlando/is-80k-enough-to-live-in-orlando"),
            ("$100k in Orlando", "/living/lifestyle/comfortable-salary/florida/orlando/is-100k-enough-to-live-in-orlando"),
        ],
    },
    ("new-york", "new-york-city"): {
        "neighborhoods": [
            {"name": "Queens (Astoria, Jackson Hts)", "range": "$500k–$750k", "note": "Co-ops and condos below Manhattan medians. Still above US norms."},
            {"name": "Brooklyn (Bed-Stuy, Bushwick)", "range": "$650k–$950k", "note": "Row houses and condos. Maintenance varies by building."},
            {"name": "Manhattan", "range": "$900k–$2M+", "note": "Co-op heavy. Board approval and high maintenance common."},
            {"name": "Bronx", "range": "$400k–$600k", "note": "Most reachable borough for many first-time buyers."},
        ],
        "long_tail": [
            {
                "h2": "How much house can I afford in NYC on $150k?",
                "paras": [
                    "At $150,000 gross, city and state tax cut take-home before you shop. The 28% cap is about $3,500 a month on gross — but net pay feels tighter than in no-tax states.",
                    "That payment often fits a smaller condo near $550,000–$650,000 in outer boroughs — not a Manhattan median.",
                    "Co-op maintenance can add $800–$1,500 a month in some buildings. Raise HOA in the calculator to match the listing.",
                ],
            },
            {
                "h2": "NYC co-op maintenance and board approval",
                "paras": [
                    "Co-ops may need 20–50% down and months of board review. Debt-to-income rules can be stricter than banks.",
                    "Maintenance often includes building mortgage and tax — not just amenities.",
                    "Condos have clearer fee lines but still carry reserve risk in older walk-ups.",
                ],
            },
            {
                "h2": "What salary do you need to buy in New York City?",
                "paras": [
                    "For a median unit near $725,000 with 20% down, plan on $180,000+ gross at 6.5% before other debt. Borough and building type move the number a lot.",
                    "Dual income is standard. Two earners at $100k each may still shop below median once maintenance is in the stack.",
                    "Use our NYC take-home tool — city tax stacks on state tax for residents.",
                ],
            },
        ],
        "rent_vs_buy": "NYC rent near $3,400 is high but so is the buy-in. Co-op flip taxes and closing costs favor longer stays. Run rent vs buy with maintenance, not mortgage alone.",
        "buyer_tips": [
            "Model co-op maintenance at the real listing number — not our default.",
            "Get board package requirements before you pay for appraisal.",
            "Compare Queens and Bronx if Brooklyn feels stretched.",
            "Budget mover fees, board fees, and working capital for co-ops.",
        ],
        "extra_narrative": [
            "New York City is the most complex market in this guide. Co-ops, condos, and townhomes each carry different fees and rules.",
            "City income tax stacks on state tax. $100k in NYC does not spend like $100k in Florida after tax.",
            "Median price near $725k blends boroughs — Manhattan medians run much higher.",
            "Many buyers need help from savings or family for down payment. Still run stress on income you control long term.",
        ],
        "extra_faqs": [
            ("What income to buy in NYC?", "Often $180k+ gross for a median condo payment with 20% down — borough matters."),
            ("Are NYC property taxes low?", "Rates look low on paper but values are high. Maintenance is the wild card."),
            ("Can I buy in NYC on $120k?", "Outer-borough studios and small condos may work — not median listings with high maintenance."),
            ("Co-op vs condo in NYC?", "Co-ops often cost less upfront but have stricter boards and higher maintenance risk."),
        ],
        "col_link": "/living/housing/cost-of-living-by-city/new-york/new-york-city",
        "salary_link": "/living/lifestyle/comfortable-salary/new-york/new-york-city",
        "scenario_links": [
            ("$100k in NYC", "/living/lifestyle/comfortable-salary/new-york/new-york-city/is-100k-enough-to-live-in-new-york-city"),
            ("$150k in NYC", "/living/lifestyle/comfortable-salary/new-york/new-york-city/is-150k-enough-to-live-in-new-york-city"),
        ],
    },
    ("new-york", "buffalo"): {
        "neighborhoods": [
            {"name": "North Buffalo", "range": "$200k–$280k", "note": "Walkable pockets near Hertel. Older homes need winter prep."},
            {"name": "South Buffalo", "range": "$160k–$230k", "note": "Often below city median. Check lead and plumbing on pre-war stock."},
            {"name": "Amherst / Williamsville", "range": "$250k–$350k", "note": "Suburban schools. Higher list than city proper."},
            {"name": "Larkinville / Waterfront", "range": "$220k–$320k", "note": "Revitalization zone. Prices rose with remote-worker migration."},
        ],
        "long_tail": [
            {
                "h2": "How much house can I afford in Buffalo on $60k?",
                "paras": [
                    "At $60,000 gross, the 28% cap is about $1,400 a month. That can fit a home near $180,000–$220,000 with 20% down at 6.5%.",
                    "Buffalo is among the most affordable cities in New York. Tax rate is high as a percent but dollars stay low on a $200k home.",
                    "Budget heat, snow removal, and roof work on older stock — PITI is not your only housing cost.",
                ],
            },
            {
                "h2": "Buffalo property tax and winter costs",
                "paras": [
                    "Tax near 2.2% of value sounds steep but on a $215k median it is about $395 a month in our model.",
                    "Heating oil or gas on older homes can add $200+ in winter months.",
                    "Star exemption helps owner-occupants — confirm status at closing.",
                ],
            },
            {
                "h2": "What salary for a median Buffalo home?",
                "paras": [
                    "For a $215,000 median home with 20% down, plan on $55,000–$70,000 gross at 6.5% with low debt.",
                    "First-time buyers often land in Comfortable stress with dual income and modest debt.",
                    "Compared to NYC, Buffalo trades higher tax rate for a much lower list price.",
                ],
            },
        ],
        "rent_vs_buy": "Buffalo rent near $1,100 and low list prices favor buying after a shorter timeline than coastal cities. Still budget maintenance on older homes.",
        "buyer_tips": [
            "Inspect roof, foundation, and plumbing on pre-1970 homes.",
            "Budget $2k–$4k a year for heat and snow-related upkeep.",
            "Compare city vs Amherst tax on similar list prices.",
            "Run the calculator with real student loans — Buffalo is affordable until debt stacks up.",
        ],
        "extra_narrative": [
            "Buffalo offers some of the lowest list prices in New York. Median income near $58k pairs better with homes than downstate metros.",
            "Remote workers from NYC boosted some neighborhoods. Prices rose but remain far below coastal norms.",
            "Healthcare and education jobs anchor wages. Manufacturing legacy means varied housing stock ages.",
            "Snow and freeze-thaw cycles punish deferred maintenance. A cheap list price with a bad roof is not a deal.",
        ],
        "extra_faqs": [
            ("Is Buffalo a good market for first-time buyers?", "Lower prices help. Still budget for heat and older-home repairs."),
            ("How much down for a Buffalo home?", "20% avoids PMI. FHA and state programs may allow less — run full PITI."),
            ("Buffalo vs Albany affordability?", "Buffalo median is lower. Albany wages run higher but homes cost more."),
            ("Can I afford Buffalo on $50k?", "You may target $150k–$180k with 20% down and very low debt."),
        ],
        "col_link": "/living/housing/cost-of-living-by-city/new-york",
        "salary_link": "/living/lifestyle/comfortable-salary/new-york",
        "scenario_links": [],
    },
    ("new-york", "albany"): {
        "neighborhoods": [
            {"name": "Center Square / Hudson Park", "range": "$280k–$380k", "note": "Walkable city pockets near state jobs. Older row stock."},
            {"name": "Colonie / Latham", "range": "$300k–$420k", "note": "Suburban schools. Popular with state employees."},
            {"name": "Saratoga Springs", "range": "$380k–$550k", "note": "Above Albany median. Tourism and tech spillover."},
            {"name": "Troy", "range": "$220k–$320k", "note": "Lower entry than Albany proper. College-town rental mix."},
        ],
        "long_tail": [
            {
                "h2": "How much house can I afford in Albany on $75k?",
                "paras": [
                    "At $75,000 gross, the 28% cap is about $1,750 a month. That often maps to $260,000–$300,000 with 20% down at 6.5%.",
                    "State and healthcare jobs stabilize wages. Median home near $285k is reachable for many dual-income households.",
                    "Tax near 1.8% plus insurance — use the listing's tax bill when you get serious.",
                ],
            },
            {
                "h2": "Albany property tax and older-home costs",
                "paras": [
                    "Effective tax near 1.8% on a $285k home is about $428 a month in our model.",
                    "Older homes may need boiler or window upgrades — budget beyond PITI.",
                    "Suburbs like Colonie may tax differently than city row houses.",
                ],
            },
            {
                "h2": "What salary for a median Albany home?",
                "paras": [
                    "For a $285,000 median home with 20% down, plan on $75,000–$90,000 gross at 6.5% with modest debt.",
                    "Government pensions and stable jobs support demand. Still run the stress meter if you have car loans.",
                    "Saratoga runs above Albany median — use this page as a floor for suburban shopping.",
                ],
            },
        ],
        "rent_vs_buy": "Albany rent near $1,350 and mid-range list prices favor buying after five to seven years for stable state-job households. Budget heat on older row homes.",
        "buyer_tips": [
            "Compare city vs Colonie tax on the same list price.",
            "Inspect heating systems before winter close dates.",
            "Saratoga premiums need a higher income — run the calculator separately.",
            "State job transfers may come — model a move scenario before you max out.",
        ],
        "extra_narrative": [
            "Albany anchors state government and healthcare. Median income near $72k supports mid-range homes for many buyers with 20% down.",
            "College towns nearby add rental demand. Check neighborhood mix if you want quiet blocks.",
            "Winter heat on older row homes can spike bills. Budget utilities outside PITI.",
            "Compared to Buffalo, Albany costs more but wages run higher. Compared to NYC, monthly payment is often half.",
        ],
        "extra_faqs": [
            ("What salary for a median Albany home?", "About $75k–$90k gross with 20% down at 6.5%, before car loans."),
            ("Albany vs Buffalo taxes?", "Effective rates are similar; Buffalo's median price is lower."),
            ("Is Albany good for first-time buyers?", "Mid-range prices and stable jobs help. Still inspect older stock carefully."),
            ("Can I afford Albany on $65k?", "You may target $230k–$260k with 20% down and low debt."),
        ],
        "col_link": "/living/housing/cost-of-living-by-city/new-york",
        "salary_link": "/living/lifestyle/comfortable-salary/new-york",
        "scenario_links": [],
    },
}
