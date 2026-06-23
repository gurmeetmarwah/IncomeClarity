"""Long-form prose blocks for rent affordability city pages (1300+ words)."""

LONGFORM = {
    ("texas", "austin"): {
        "rules": [
            "Landlords in Austin often ask for gross income at 40 times monthly rent. That is the same math as spending 30% of gross on rent — just written for lease applications. A $1,750 listing implies about $70,000 yearly gross to pass the screen.",
            "Your budget should still run on take-home pay. With no Texas state income tax, Austin workers often keep 75% to 80% of gross after federal and FICA. A $75,000 salary might land near $4,900 a month in take-home — your rent cap should come from that number, not the offer letter alone.",
            "Debt changes the picture fast. A $350 car payment and $200 in student loans can pull your comfortable rent band down by $150 to $250 a month even when gross income looks fine on an application.",
            "Savings goals matter too. If you want 15% of take-home set aside, you may need to rent below the landlord maximum. That is intentional — it leaves room for Austin rent hikes, which averaged 3% to 5% annually in many buildings before cooling.",
        ],
        "hidden_costs": [
            "Listed rent rarely includes electricity, gas, water, trash, or internet. In Austin, plan $150 to $250 a month for utilities on a 1-bedroom, higher in summer when AC runs hard.",
            "Renters insurance is cheap but required in most leases — budget $15 to $25 a month. Parking downtown can add $100 to $250 if it is not included.",
            "Move-in costs hit once: first month, deposit, and sometimes an admin fee. That can mean $4,000 to $5,000 cash due at signing on a $1,800 unit before you buy furniture.",
            "Pet rent and breed restrictions are common in newer Austin complexes. A $50 monthly pet fee is effectively part of your housing cost when you compare listings.",
        ],
        "snapshot_extra": [
            "Austin's cost-of-living index near 108 means everyday bills run a bit above the US average. Rent is the biggest line, but groceries near $400 a month and transport near $370 still compete with your lease payment.",
            "The affordability score of 74/100 on this page reflects median rent against typical wages — not your personal offer. A remote worker paid California wages rents very differently than a local service wage.",
            "Studios near $1,420 and 2-bedrooms near $2,280 bracket the median. Families often need the 2BR row while singles target studios or shared leases in the urban core.",
        ],
        "neighborhood_prose": "Downtown and South Congress command premiums for walkability and nightlife. North Austin and Round Rock trade commute time for square footage. When you tour, ask about average utility bills and parking — two lines that swing the true monthly cost more than a $100 rent difference.",
        "budget_extra": [
            "This example assumes moderate debt entered in the calculator. If you carry $600 a month in loan payments, cut the rent line before you cut groceries or savings.",
            "Austin commuters on toll roads (183A, 290 toll) should add those charges to transportation — they can rival a utility bill over a month of daily driving.",
        ],
        "tiers_extra": "Austin's tier bands map to real listing tiers: survival often means roommates east of I-35 or far north; comfortable fits many 1BRs at $1,600 to $1,900; premium assumes dual income or remote tech wages at $2,400+ for central zip codes.",
        "long_tail": [
            {
                "id": "ra-lt-gross-net-austin",
                "title": "Is rent 30% of gross or net income in Austin?",
                "paragraphs": [
                    "Use gross for landlord approval and net for your real life. Austin property managers commonly require 2.5× to 3× rent in monthly gross income. The 40× annual rule is the same test in different clothes.",
                    "For budgeting, multiply take-home pay by 0.30 — or use our calculator, which also factors debt and savings. On $4,900 take-home, that is $1,470 a month all-in for rent plus utilities if you want a strict cap.",
                    "Texas has no state income tax, so the gross-to-net gap is smaller than in California or New York. Still, benefits and 401(k) deferrals shrink spendable cash. Paste your actual paycheck into the tool after you run state withholding.",
                ],
            },
            {
                "id": "ra-lt-2br-austin",
                "title": "What salary do you need for a 2-bedroom apartment in Austin?",
                "paragraphs": [
                    "Median 2-bedroom rent near $2,280 implies about $91,200 gross at the 30% rule — before utilities, parking, or debt. Dual earners often combine income on the lease; solo renters may need roommates at that price point.",
                    "Suburbs like Pflugerville, Kyle, and Cedar Park sometimes list 2BR units closer to $1,900. Factor commute gas and tolls before you count the savings.",
                    "If you have children, daycare can matter more than an extra bedroom. Run the comfortable salary guide for Austin to layer childcare on top of rent.",
                ],
            },
            {
                "id": "ra-lt-rent-buy-austin",
                "title": "Should you rent or buy in Austin right now?",
                "paragraphs": [
                    "Renting wins on flexibility when job or neighborhood plans are uncertain. Buying pulls ahead after several years if you stay put and rates stabilize — but Austin property tax is heavy for owners.",
                    "Use our rent vs buy calculator with your real stay length. Many Austin renters upgrade to buying only after they know their corridor — not on day one of a new job.",
                    "If your comfortable rent is far below median, buying may be years away. That is normal — build savings while you rent under budget instead of stretching to the landlord max.",
                ],
            },
            {
                "id": "ra-lt-tips-austin",
                "title": "First-time renter tips in Austin",
                "paragraphs": [
                    "Tour in summer if the unit includes AC — you will feel how hard the system works. Ask the current tenant or landlord for last summer's electric bill.",
                    "Read the lease for automatic renewal and rent-increase clauses. Texas notices vary; know how much lead time you have if the landlord raises rent at renewal.",
                    "Get renters insurance before move-in — most leases require it and it is inexpensive. Bundle with auto if you already insure a car in Texas.",
                ],
            },
        ],
        "extra_faqs": [
            (
                "How much is average rent in Austin for a 1-bedroom?",
                "Planning figures center near $1,750, with studios lower and renovated central units higher. Always verify with current listings in your target zip.",
            ),
            (
                "Can I afford Austin rent on $60,000 a year?",
                "Gross cap near $1,500 a month — usually a roommate, studio, or suburb. Comfortable solo 1BR at median rent typically needs closer to $70,000+ with low debt.",
            ),
        ],
        "extra_expansions": [
            (
                60000,
                1500,
                "Can a single person afford Austin on $60k?",
                "Possible with a roommate or a studio outside the core. Solo 1BR at median rent is a stretch without low debt and a tight savings goal.",
                "Budget $1,500 rent plus $200 utilities and $350 transport before you count groceries. That often means living north or east of central Austin.",
            ),
            (
                125000,
                3100,
                "How much rent on $125k in Austin?",
                "Gross rule allows about $3,125 a month — enough for premium 1BR or many 2BR units with savings room if debt stays moderate.",
                "High earners still overspend on square footage. Cap rent so you keep 15% savings for down payment if you plan to buy within five years.",
            ),
        ],
    },
    ("texas", "dallas"): {
        "rules": [
            "DFW landlords typically screen at 3× monthly rent in gross income. Dallas median near $1,550 implies about $62,000 yearly gross minimum — lower than Austin for the same bedroom count.",
            "Take-home pay still drives your lifestyle. Texas has no state income tax, so a $76,000 salary often nets near $4,950 a month. Your comfortable rent should fit inside that cash flow after debt and savings.",
            "The 28% rule used for mortgages is stricter than the 30% rent rule. If you are saving for a down payment, aim closer to 28% of take-home for total housing.",
            "Roommates change approval math — combined income on the lease can qualify for a larger unit while each person pays less than solo median rent.",
        ],
        "hidden_costs": [
            "Summer electric bills in older Dallas apartments can spike above $200. Ask for average usage, not just the landlord's estimate.",
            "Parking in Uptown and Downtown is often paid separately. Budget $75 to $175 monthly if your building does not include a spot.",
            "Renter's insurance and mandatory trash valet fees appear on many newer Frisco and Plano leases — read the fee schedule before you sign.",
            "Application fees and background checks run $50 to $100 per adult. That is not monthly, but it is part of move-in cash due.",
        ],
        "snapshot_extra": [
            "Dallas sits at COL index 102 — slightly above US average but well below coastal metros. Median 1BR near $1,550 is a planning anchor, not a guarantee in Uptown.",
            "Affordability score 75/100 reflects relatively strong wages against rent compared with Austin. Suburban stock keeps options open below median.",
            "2-bedroom median near $1,980 suits small families when combined income clears $80,000 gross with moderate debt.",
        ],
        "neighborhood_prose": "Uptown and Deep Ellum attract young professionals but charge parking and amenity fees. Oak Cliff and southern suburbs offer lower bases with longer commutes. Frisco and Plano fit families who prioritize schools over nightlife — toll roads are part of that trade.",
        "budget_extra": [
            "DFW is car-heavy unless you live on DART rail corridors. If you run two car payments, subtract that from rent headroom before you tour.",
            "Sales tax near 8.25% in Dallas County affects disposable income slightly — not huge, but it adds up on big purchases after rent is paid.",
        ],
        "tiers_extra": "Survival tier in Dallas often means roommate in Irving or Garland. Comfortable tier matches many 1BRs at $1,400 to $1,700. Premium tier is Uptown high-rise or large suburban 2BR with dual income.",
        "long_tail": [
            {
                "id": "ra-lt-gross-net-dallas",
                "title": "Gross vs net rent rules in Dallas",
                "paragraphs": [
                    "Apply with gross; live on net. A $76,000 offer supports about $1,900 monthly rent on paper — but take-home near $4,950 means a safer cap near $1,500 to $1,650 after utilities.",
                    "Employer health premiums and HSA contributions reduce spendable income. Pull a recent pay stub into the calculator's take-home estimate if you have one.",
                    "Dual-income leases are common in DFW. Make sure each earner can still afford the unit if one income disappears — do not combine incomes to max out rent.",
                ],
            },
            {
                "id": "ra-lt-2br-dallas",
                "title": "2-bedroom rent and salary in Dallas",
                "paragraphs": [
                    "At $1,980 median 2BR, plan near $79,200 gross at 30% — higher if you want savings and low debt. Frisco and McKinney listings can run above median; southern Dallas below.",
                    "School district choices push suburban rent. A cheaper apartment with a long commute may cost more in gas and time than a higher rent near work.",
                    "Check our Dallas house affordability guide if you are comparing a $2,000 rent to a $2,200 mortgage — the crossover depends on stay length and tax.",
                ],
            },
            {
                "id": "ra-lt-rent-buy-dallas",
                "title": "Rent vs buy in Dallas-Fort Worth",
                "paragraphs": [
                    "DFW buyers face property tax near 1.7% — renters avoid that line but miss equity. Break-even often lands at five to seven years in stable suburbs.",
                    "If you might transfer within three years, renting below your max preserves cash for the move. Stretch rent makes job changes expensive.",
                    "Run rent vs buy with your actual down payment savings — Dallas median home prices sit below Austin in many corridors.",
                ],
            },
            {
                "id": "ra-lt-tips-dallas",
                "title": "Dallas renter checklist",
                "paragraphs": [
                    "Hail and wind storms matter for parking — covered parking costs more but saves claims. Ask about garage flood history in low-lying complexes.",
                    "Verify commute at rush hour on 75, 635, or your toll road. A cheap rent with a 90-minute drive rarely feels like a win.",
                    "Negotiate lease length — some landlords offer one-month free on 14-month leases. Compare effective rent, not headline rent.",
                ],
            },
        ],
        "extra_faqs": [
            (
                "What is a good rent for $80,000 salary in Dallas?",
                "About $2,000 gross cap — comfortable 1BR in many areas if debt is under $400 a month.",
            ),
            (
                "Is Dallas cheaper than Austin for renters?",
                "Usually yes on median 1BR. Austin's urban core runs hotter; Dallas suburbs offer more sub-$1,600 stock.",
            ),
        ],
        "extra_expansions": [
            (
                55000,
                1375,
                "Rent on $55k in Dallas?",
                "Near $1,375 gross cap — roommate or suburban studio is typical.",
                "Low debt is essential at this income. Add utilities and you may target $1,100 to $1,200 base rent.",
            ),
        ],
    },
    ("new-york", "new-york-city"): {
        "rules": [
            "NYC landlords often require 40× rent in annual gross income and may ask for guarantors if you are under that bar. International and freelance earners should expect extra documentation.",
            "State and city income tax can take 6% to 10% of gross from high earners. A $95,000 salary might net near $5,400 a month — far below the gross-implied rent ceiling.",
            "The 30% rule is a screening tool, not a comfort guarantee. Many NYC renters exceed 35% of take-home and compensate by skipping a car or sharing space.",
            "Roommates are standard, not a failure — combined lease income unlocks neighborhoods no single $75k earner could afford alone.",
        ],
        "hidden_costs": [
            "Broker fees still appear on many market-rate listings — one month or more of rent due at signing. Always ask who pays the broker before you tour.",
            "Electric and gas in older walk-ups can be high in winter. Budget $100 to $200 for utilities even on small units.",
            "MetroCard or OMNY fares add $132+ a month for unlimited subway — cheaper than a car but not free.",
            "Move-in requires first month, security deposit, and sometimes last month — cash due can exceed $10,000 on a $3,400 lease before furniture.",
        ],
        "snapshot_extra": [
            "COL index 158 places NYC among the most expensive US metros. Median 1BR near $3,400 is a citywide blend — Manhattan runs higher, outer boroughs lower.",
            "Affordability score 52/100 reflects rent pressure against wages. High earners survive; middle incomes rely on roommates or long commutes.",
            "Studios near $2,900 and 2BR near $4,500 show why dual income is common for families.",
        ],
        "neighborhood_prose": "Manhattan core and Williamsburg charge premiums for transit and lifestyle. Astoria and parts of the Bronx offer relief with longer commutes. Visit the block at night and check subway access — two factors that matter as much as rent per square foot.",
        "budget_extra": [
            "NYC grocery and dining costs run above national averages — the food line in our example is conservative. Track a month of real receipts if you are new to the city.",
            "If you pay a broker fee, amortize it over your expected stay. A $3,400 fee on a 12-month lease adds $283 to effective monthly housing cost.",
        ],
        "tiers_extra": "Survival tier means roommates in outer boroughs. Comfortable tier is outer-borough 1BR or Manhattan micro-unit. Premium tier is Manhattan 1BR+ with savings — often $150k+ household income.",
        "long_tail": [
            {
                "id": "ra-lt-gross-net-nyc",
                "title": "Gross vs net rent math in New York City",
                "paragraphs": [
                    "A landlord may approve $2,850 rent on $95,000 gross. After NY tax, your take-home might only support $2,200 comfortable all-in housing — know both numbers before you apply.",
                    "NYC local tax hits residents in the five boroughs. Use the New York take-home calculator with your filing status before you set a search filter on StreetEasy or Zillow.",
                    "Guarantor services charge fees if your income is short — that is another move-in cost to budget.",
                ],
            },
            {
                "id": "ra-lt-2br-nyc",
                "title": "2-bedroom apartments and salary in NYC",
                "paragraphs": [
                    "Median 2BR near $4,500 implies $180,000 gross at 30% — dual income or a long commute from lower-rent corridors.",
                    "Families sometimes choose New Jersey or Westchester with higher transit cost but lower base rent — run total monthly housing, not rent alone.",
                    "Rent-stabilized units exist but are scarce — do not build a budget assuming you will find one.",
                ],
            },
            {
                "id": "ra-lt-rent-buy-nyc",
                "title": "Rent vs buy in NYC",
                "paragraphs": [
                    "Buying requires large down payments and co-op boards — many newcomers rent for years first. Transaction costs alone can exceed $50,000 on a million-dollar co-op.",
                    "If you might leave within three years, renting preserves optionality. Use rent vs buy with NYC property tax and maintenance in mind.",
                    "Stretching rent to save for a down payment only works if you actually save the difference — track it monthly.",
                ],
            },
            {
                "id": "ra-lt-tips-nyc",
                "title": "NYC renter tips",
                "paragraphs": [
                    "Apply with documents ready: pay stubs, tax return, bank statements. Competitive listings move in days.",
                    "Check water pressure, windows, and heat — older buildings vary wildly. Ask who controls heat in winter.",
                    "Renter's insurance is inexpensive and required — it also covers liability if you accidentally damage a neighbor's unit.",
                ],
            },
        ],
        "extra_faqs": [
            (
                "What is the 40× rent rule in NYC?",
                "Annual gross must be 40 times monthly rent. $3,000 rent needs $120,000 income unless you have a guarantor.",
            ),
            (
                "Can you live in NYC on $80k?",
                "Yes with roommates or outer-borough discipline. Solo Manhattan 1BR at market rent is a stretch without low debt.",
            ),
        ],
        "extra_expansions": [
            (
                85000,
                2125,
                "Is $2,100 rent OK on $85k in NYC?",
                "On gross paper yes; on take-home it is tight. Outer boroughs work better than Manhattan at that rent.",
                "Add broker fee impact and MetroCard before you call it affordable.",
            ),
        ],
    },
    ("florida", "miami"): {
        "rules": [
            "Miami landlords use standard 3× gross income screens. No Florida state income tax helps take-home, but insurance and parking costs are higher than inland cities.",
            "Flood-zone buildings may pass insurance costs to tenants through fees — ask the leasing office what changed after recent storm seasons.",
            "Seasonal demand spikes in winter — quotes in January can beat summer listings in some buildings.",
            "If you earn commission or tips, bring two years of tax returns — Miami landlords see variable income often.",
        ],
        "hidden_costs": [
            "Hurricane-ready buildings charge amenity and reserve fees. Read the monthly fee sheet, not just base rent.",
            "Car insurance in Miami-Dade is among the highest in the US — transport cost is not just gas and parking.",
            "Condo association rules may restrict short-term guests — irrelevant to rent amount but matters for lifestyle.",
            "Pest control and trash valet fees appear on many newer leases — $30 to $80 monthly combined is common.",
        ],
        "snapshot_extra": [
            "COL index 118 reflects tourism-driven prices. Median 1BR near $2,300 beats Tampa and Orlando by a wide margin.",
            "Affordability score 61/100 — wages in hospitality and services lag rent growth in Brickell and Wynwood.",
            "2BR median near $3,100 pushes families toward $100k+ gross unless they commute from Hialeah or Kendall.",
        ],
        "neighborhood_prose": "Brickell and Wynwood target young professionals with high-rise amenities. Coral Gables trades leafy streets for moderate premiums. Hialeah and west-Dade offer lower bases with car commutes on 836 or 826.",
        "budget_extra": [
            "If you need flood insurance as a renter through contents coverage, add it to renters insurance discussion — not in our base table.",
            "Beach-adjacent units may include wind insurance surcharges in building fees even when you do not own the unit.",
        ],
        "tiers_extra": "Survival tier: roommates in west Miami-Dade. Comfortable: $90k household on $2,000 to $2,400 rent. Premium: Brickell waterfront or large 2BR on $140k+.",
        "long_tail": [
            {
                "id": "ra-lt-gross-net-miami",
                "title": "How Florida tax affects Miami rent budgets",
                "paragraphs": [
                    "No state wage tax means take-home is higher than NYC at the same gross — but rent and insurance eat the advantage.",
                    "A $90,000 salary might net near $5,800 a month. Comfortable rent near $2,250 leaves room if debt stays under $400.",
                    "Self-employed earners pay differently — use the 1099 vs W2 tool if you invoice clients from Miami Beach.",
                ],
            },
            {
                "id": "ra-lt-2br-miami",
                "title": "2-bedroom rent in Miami",
                "paragraphs": [
                    "Families targeting $3,100 median 2BR need roughly $124,000 gross at 30% — or a longer commute from lower-rent zip codes.",
                    "School choice drives Kendall and Coral Gables demand. Compare total cost to Tampa if remote work allows.",
                    "Run our Miami house affordability page if you are weighing rent against buying in a condo tower.",
                ],
            },
            {
                "id": "ra-lt-rent-buy-miami",
                "title": "Rent vs buy in Miami",
                "paragraphs": [
                    "Condos carry HOA and insurance shocks — renters avoid down payment but miss appreciation in hot years.",
                    "If you might relocate seasonally, rent. If you will stay seven plus years, buying can pull ahead — run the calculator.",
                    "Storm risk makes insurance a bigger swing factor for owners than renters — still ask about building reserves.",
                ],
            },
            {
                "id": "ra-lt-tips-miami",
                "title": "Miami leasing tips",
                "paragraphs": [
                    "Tour at different times — parking and traffic near Brickell change rush hour comfort.",
                    "Ask about hurricane prep: generators, shutter storage, garage flood history.",
                    "Get wind coverage quote for your car if you park outside — it affects true transport cost.",
                ],
            },
        ],
        "extra_faqs": [
            (
                "Is Miami more expensive than Tampa for rent?",
                "Yes — median 1BR in Miami often runs $500+ above Tampa. Wages do not always close that gap.",
            ),
            (
                "What salary for $2,500 rent in Miami?",
                "Roughly $100,000 gross at 30% — stretch if debt is high or savings goal is 15%+.",
            ),
        ],
        "extra_expansions": [
            (
                65000,
                1625,
                "Can you rent in Miami on $65k?",
                "Possible in Hialeah or with roommates — not Brickell solo at market rent.",
                "Transport and insurance costs hit harder on lower incomes — budget all-in housing below $1,400 if net is near $4,200.",
            ),
        ],
    },
    ("illinois", "chicago"): {
        "rules": [
            "Chicago landlords typically want 3× gross monthly rent. Flat Illinois state income tax reduces take-home versus Texas but less than NYC.",
            "Cook County sales tax is high — it nibbles disposable income after rent is paid.",
            "Heat included vs tenant-paid gas changes winter utility swings — clarify before you sign.",
            "Student-heavy neighborhoods may offer September lease timing — off-cycle moves can find discounts in winter.",
        ],
        "hidden_costs": [
            "Winter gas heat in older walk-ups can push utilities above $200 in January.",
            "Lakefront buildings may charge for storage lockers and bike rooms separately.",
            "Move-in fees and credit check charges vary — some Chicago landlords charge admin fees over $200.",
            "Street parking permits and garage rentals add $100 to $250 in dense neighborhoods.",
        ],
        "snapshot_extra": [
            "COL index 112 — big-city amenities without NYC rent. Median 1BR near $1,850 is the planning anchor.",
            "Affordability score 70/100 — wages and rent are more balanced than coastal peers.",
            "2BR near $2,400 suits roommates or small families on $95k+ combined gross.",
        ],
        "neighborhood_prose": "Loop and Lincoln Park charge for location and transit. Logan Square and Hyde Park offer different vibes at lower bases. Visit the block at rush hour — Red Line access can save a car payment worth of rent equivalent.",
        "budget_extra": [
            "CTA unlimited pass is cheaper than NYC Metro but still a fixed line — include it in transport.",
            "City sticker and parking tickets are real risks if you street-park — budget conservatively.",
        ],
        "tiers_extra": "Survival: roommates in outer neighborhoods. Comfortable: $82k on $1,700 to $1,950 rent. Premium: Lincoln Park or Loop on $120k+ with savings.",
        "long_tail": [
            {
                "id": "ra-lt-gross-net-chicago",
                "title": "Gross vs net rent in Chicago",
                "paragraphs": [
                    "Illinois flat tax means predictable withholding — still use net for budgeting. $82,000 gross often nets near $5,050 a month.",
                    "Landlord approval at $1,850 rent needs about $66,000 gross — easier than living comfortably on that rent with student loans.",
                    "Union Station or Loop workers may skip a car — reallocate that payment to slightly higher rent near transit.",
                ],
            },
            {
                "id": "ra-lt-2br-chicago",
                "title": "2-bedroom salary needs in Chicago",
                "paragraphs": [
                    "Median 2BR $2,400 needs about $96,000 gross at 30%. Suburban Evanston or Oak Park may differ — check Metra commute cost.",
                    "Three-flat buildings may have owner-occupied units with stricter rules — read lease noise policies.",
                    "Compare our Chicago cost of living page for child care if you need bedroom count for kids, not guests.",
                ],
            },
            {
                "id": "ra-lt-rent-buy-chicago",
                "title": "Rent vs buy in Chicago",
                "paragraphs": [
                    "Property tax and winter maintenance hit owners — renters stay flexible during job changes.",
                    "Buying can work after five to seven years in stable neighborhoods — run break-even with your down payment.",
                    "If you love Lincoln Park rent but cannot buy there, saving the difference in a high-yield account is a valid plan.",
                ],
            },
            {
                "id": "ra-lt-tips-chicago",
                "title": "Chicago renter tips",
                "paragraphs": [
                    "Ask who pays heat and whether radiators are controlled — winter bills surprise newcomers.",
                    "Check el stop distance in February, not July — walk matters in snow.",
                    "Renter's insurance covers theft and liability — inexpensive and often required.",
                ],
            },
        ],
        "extra_faqs": [
            (
                "Is $1,900 rent affordable on $70k in Chicago?",
                "Stretch for many — comfortable closer to $1,600 to $1,750 on that income after tax.",
            ),
            (
                "How does Chicago rent compare to NYC?",
                "Roughly half median 1BR — why many Midwest transplants choose Chicago first.",
            ),
        ],
        "extra_expansions": [
            (
                70000,
                1750,
                "Rent on $70k in Chicago?",
                "Gross cap $1,750 — workable in many neighborhoods with moderate debt.",
                "Take-home near $4,300 means all-in housing should stay under $1,500 if you save 15%.",
            ),
        ],
    },
}
