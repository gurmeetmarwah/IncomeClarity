# SEO Content-Depth Audit

_Audited 52 content pages (+ 23 redirect stubs skipped)._

Sort order: highest **severity score** first (thinner + harder-to-read + fewer visuals/examples = higher score).

**Column legend**
- **Sev**: severity score (higher = more work needed)
- **Words**: body word count (excludes nav/footer/scripts)
- **FRE**: Flesch Reading Ease (target > 60)
- **FK**: Flesch-Kincaid Grade Level (lower = easier; ~8 is ideal)
- **H2/H3**: heading counts
- **Vis**: visual elements (tables + canvas + svg)
- **Int**: interactive elements (numeric/range inputs + selects + buttons)
- **FAQ**: FAQ JSON-LD entries
- **$ / %**: dollar amounts and percentages mentioned in copy
- **Emp**: empathy markers ("what this means", "your", "if you")
- **Gen**: AI-generic boilerplate phrase hits

| Sev | Words |   FRE |   FK | H2/H3 | Vis | Int | FAQ |   $ |   % | Emp | Gen | Page | Flags |
|----:|------:|------:|-----:|:-----:|----:|----:|----:|----:|----:|----:|----:|------|-------|
|  80 |    42 |  11.3 | 15.2 | 0/0 |  0 |   0 |  0 |   0 |   0 |   0 |  0 | `contact.html` | THIN (<600 words), HARD-TO-READ (FRE 11.3), NO-VISUAL (no table/chart/svg), NO-EMPATHY, NO-INTERACTIVE, LOW-EXAMPLES (<5 $ and <3 %), THIN-STRUCTURE (<4 H2/H3) |
|  57 |    81 |  33.6 | 11.1 | 3/0 |  0 |   0 |  0 |   0 |   0 |   0 |  0 | `privacy-policy.html` | THIN (<600 words), HARD-TO-READ (FRE 33.6), NO-VISUAL (no table/chart/svg), NO-EMPATHY, NO-INTERACTIVE, LOW-EXAMPLES (<5 $ and <3 %), THIN-STRUCTURE (<4 H2/H3) |
|  51 |    75 |  39.3 | 11.5 | 3/0 |  0 |   0 |  0 |   0 |   0 |   0 |  0 | `terms.html` | THIN (<600 words), HARD-TO-READ (FRE 39.3), NO-VISUAL (no table/chart/svg), NO-EMPATHY, NO-INTERACTIVE, LOW-EXAMPLES (<5 $ and <3 %), THIN-STRUCTURE (<4 H2/H3) |
|  15 |  1688 |  54.9 |  8.8 | 10/7 |  0 |   0 |  0 |   8 |  33 |   2 |  0 | `methodology.html` | HARD-TO-READ (FRE 54.9), NO-VISUAL (no table/chart/svg), NO-INTERACTIVE |
|  13 |   760 |  76.1 |  4.6 | 7/0 |  0 |   0 |  0 |   1 |   0 |   3 |  0 | `about.html` | NO-VISUAL (no table/chart/svg), NO-INTERACTIVE, LOW-EXAMPLES (<5 $ and <3 %) |
|   5 |  1437 |  72.2 |  5.9 | 8/23 |  0 |  14 |  5 |   8 |  16 |  10 |  0 | `rent-vs-buy-calculator.html` | NO-VISUAL (no table/chart/svg), REPETITIVE (TTR 0.295) |
|   0 |   690 |  76.8 |  4.7 | 7/5 |  1 |   4 |  5 |  20 |  20 |  14 |  0 | `living/family-budgeting/can-i-afford-to-live-alone.html` | — |
|   0 |   725 |  68.0 |  6.3 | 1/16 |  2 |  18 |  5 |  37 |   3 |   4 |  0 | `debt/payoff-scenarios/how-long-to-pay-off-5000-debt/index.html` | — |
|   0 |   842 |  70.2 |  5.7 | 7/9 |  1 |   3 |  6 |  41 |  28 |  10 |  0 | `what-is-take-home-pay.html` | — |
|   0 |   847 |  78.0 |  4.1 | 9/5 |  1 |   3 |  5 |  13 |  16 |  11 |  0 | `living/budgeting/50-30-20-budget-rule.html` | — |
|   0 |   848 |  66.0 |  6.6 | 1/17 |  3 |  19 |  5 |  69 |  23 |   6 |  0 | `living/lifestyle-family/childcare-affordability/index.html` | — |
|   0 |   885 |  66.4 |  6.7 | 1/18 |  1 |  23 |  5 |  32 |   5 |   3 |  0 | `living/lifestyle-family/budgeting-for-roommates/index.html` | — |
|   0 |   896 |  70.4 |  5.9 | 1/17 |  3 |  18 |  5 |  67 |   7 |   5 |  0 | `debt/payoff-scenarios/how-long-to-pay-off-10000-debt/index.html` | REPETITIVE (TTR 0.333) |
|   0 |   905 |  75.2 |  5.3 | 9/4 |  1 |   4 |  4 |  34 |  19 |   5 |  0 | `living/housing/how-much-house-can-i-afford-in-california.html` | — |
|   0 |   919 |  82.2 |  4.0 | 7/9 |  2 |   4 |  5 |  34 |  25 |   5 |  0 | `debt/interest/what-is-credit-card-apr.html` | REPETITIVE (TTR 0.337) |
|   0 |   921 |  66.3 |  6.8 | 2/25 |  1 |   3 |  4 |  31 |   6 |   9 |  0 | `debt/hidden-costs/index.html` | — |
|   0 |   958 |  85.4 |  3.4 | 9/4 |  1 |   5 |  4 |  13 |   5 |   5 |  0 | `living/housing/when-buying-is-better-than-renting.html` | — |
|   0 |   991 |  69.3 |  5.6 | 7/8 |  1 |   4 |  5 |  39 |  15 |  10 |  0 | `best-states-for-take-home-pay.html` | REPETITIVE (TTR 0.32) |
|   0 |  1013 |  61.1 |  6.9 | 1/16 |  3 |  21 |  5 |  78 |   4 |  12 |  0 | `living/lifestyle-family/comfortable-salary-california/index.html` | REPETITIVE (TTR 0.319) |
|   0 |  1016 |  71.3 |  6.3 | 7/5 |  2 |   4 |  4 |  44 |  17 |  11 |  0 | `debt/interest/how-credit-card-interest-works.html` | REPETITIVE (TTR 0.28) |
|   0 |  1031 |  75.0 |  5.2 | 10/7 |  2 |   5 |  4 |  27 |  35 |  10 |  0 | `living/housing/how-much-house-can-i-afford.html` | — |
|   0 |  1050 |  71.9 |  6.2 | 7/9 |  2 |   5 |  5 |  30 |   9 |   9 |  0 | `living/housing/rent-vs-buy-california.html` | — |
|   0 |  1059 |  64.2 |  6.5 | 2/19 |  2 |  16 |  5 |  35 |   5 |   6 |  0 | `living/lifestyle-family/family-of-4-income-guide/index.html` | REPETITIVE (TTR 0.347) |
|   0 |  1078 |  68.9 |  6.4 | 3/23 |  1 |   4 |  4 |  29 |  12 |   8 |  0 | `debt/interest-apr/index.html` | REPETITIVE (TTR 0.311) |
|   0 |  1080 |  75.6 |  5.2 | 9/7 |  2 |   3 |  5 |  29 |   0 |   4 |  0 | `living/cost-of-living/cost-of-living-california-vs-texas.html` | REPETITIVE (TTR 0.346) |
|   0 |  1081 |  73.1 |  5.5 | 2/18 |  1 |   4 |  4 |  38 |   4 |   6 |  0 | `debt/payoff-scenarios/index.html` | REPETITIVE (TTR 0.298) |
|   0 |  1087 |  76.2 |  5.2 | 2/24 |  1 |   4 |  4 |  12 |  16 |   5 |  0 | `debt/life-decisions/index.html` | REPETITIVE (TTR 0.332) |
|   0 |  1088 |  76.0 |  5.2 | 2/20 |  2 |   6 |  4 |  18 |   3 |   7 |  0 | `debt/payoff-strategies/index.html` | REPETITIVE (TTR 0.33) |
|   0 |  1114 |  62.8 |  6.9 | 1/15 |  5 |  22 |  5 | 126 |   6 |  17 |  0 | `living/lifestyle-family/comfortable-salary-texas/index.html` | REPETITIVE (TTR 0.348) |
|   0 |  1117 |  72.3 |  5.5 | 8/7 |  2 |   3 |  5 |  31 |   0 |   5 |  0 | `living/cost-of-living/seattle-vs-denver-cost-of-living.html` | — |
|   0 |  1120 |  73.0 |  5.0 | 9/7 |  2 |   3 |  6 |  26 |  12 |  10 |  0 | `living/budgeting/average-monthly-expenses.html` | — |
|   0 |  1120 |  76.3 |  4.5 | 9/10 |  1 |   4 |  5 |  55 |  28 |  20 |  0 | `living/housing/how-much-rent-can-i-afford.html` | REPETITIVE (TTR 0.326) |
|   0 |  1132 |  73.9 |  5.1 | 3/23 |  2 |   3 |  4 |  24 |  20 |   5 |  0 | `debt/financial-health/index.html` | — |
|   0 |  1151 |  81.6 |  3.8 | 9/7 |  1 |   3 |  3 |  21 |   5 |   5 |  0 | `debt/debt-reality/why-paying-minimum-is-bad.html` | REPETITIVE (TTR 0.32) |
|   0 |  1153 |  61.9 |  6.8 | 8/27 |  1 |   3 |  4 |  62 |  25 |   7 |  0 | `hourly-to-salary-after-tax/state/california/index.html` | REPETITIVE (TTR 0.305) |
|   0 |  1155 |  77.9 |  5.0 | 8/5 |  2 |   3 |  4 |  35 |  24 |  11 |  0 | `debt/financial-health/how-much-credit-card-debt-is-normal.html` | REPETITIVE (TTR 0.322) |
|   0 |  1181 |  61.7 |  7.0 | 8/27 |  1 |   3 |  4 |  59 |  11 |   7 |  0 | `hourly-to-salary-after-tax/state/florida/index.html` | REPETITIVE (TTR 0.3) |
|   0 |  1198 |  78.6 |  4.5 | 8/7 |  2 |   3 |  5 |  32 |   0 |   6 |  0 | `living/cost-of-living/nyc-vs-austin-cost-of-living.html` | REPETITIVE (TTR 0.349) |
|   0 |  1230 |  72.5 |  5.9 | 9/6 |  1 |   3 |  3 |  10 |  18 |   5 |  0 | `debt/strategies/average-credit-card-debt-by-income.html` | REPETITIVE (TTR 0.314) |
|   0 |  1232 |  70.6 |  5.8 | 2/27 |  1 |   4 |  5 |  19 |  20 |   7 |  0 | `living/housing/index.html` | REPETITIVE (TTR 0.342) |
|   0 |  1238 |  61.7 |  7.5 | 8/27 |  1 |   3 |  4 |  53 |  18 |   9 |  0 | `hourly-to-salary-after-tax/state/illinois/index.html` | REPETITIVE (TTR 0.293) |
|   0 |  1242 |  63.1 |  7.4 | 8/27 |  1 |   3 |  4 |  51 |  12 |   4 |  0 | `hourly-to-salary-after-tax/state/washington/index.html` | REPETITIVE (TTR 0.301) |
|   0 |  1252 |  65.4 |  6.8 | 2/26 |  1 |   3 |  4 |  32 |  15 |   6 |  0 | `living/budgeting/index.html` | — |
|   0 |  1266 |  63.4 |  7.3 | 8/27 |  1 |   3 |  4 |  52 |  10 |   8 |  0 | `hourly-to-salary-after-tax/state/texas/index.html` | REPETITIVE (TTR 0.307) |
|   0 |  1293 |  67.7 |  6.9 | 8/27 |  1 |   3 |  4 |  58 |  18 |   8 |  0 | `hourly-to-salary-after-tax/state/new-york/index.html` | REPETITIVE (TTR 0.294) |
|   0 |  1320 |  69.2 |  5.8 | 7/16 |  2 |   8 |  3 |  20 |  14 |   6 |  0 | `1099-vs-w2-calculator.html` | REPETITIVE (TTR 0.315) |
|   0 |  1340 |  70.5 |  5.9 | 10/6 |  2 |   3 |  6 |  30 |  14 |  11 |  0 | `living/family-budgeting/salary-needed-to-live-comfortably.html` | REPETITIVE (TTR 0.337) |
|   0 |  1358 |  70.5 |  5.4 | 2/28 |  1 |   3 |  4 |  63 |  18 |   9 |  0 | `living/lifestyle-family/index.html` | REPETITIVE (TTR 0.275) |
|   0 |  1583 |  72.8 |  5.5 | 6/23 |  1 |   4 |  5 |  67 |  25 |  10 |  0 | `debt.html` | REPETITIVE (TTR 0.272) |
|   0 |  1598 |  74.8 |  4.9 | 8/30 |  1 |   3 |  5 |  34 |  13 |  14 |  0 | `index.html` | REPETITIVE (TTR 0.304) |
|   0 |  1615 |  76.1 |  4.4 | 9/12 |  1 |   4 |  5 |  57 |  19 |   6 |  0 | `debt/payoff/best-way-to-pay-off-credit-card-debt.html` | REPETITIVE (TTR 0.307) |
|   0 |  1656 |  75.9 |  5.0 | 5/24 |  1 |   3 |  8 |  72 |  13 |  19 |  0 | `hourly-to-salary-after-tax.html` | REPETITIVE (TTR 0.252) |

## Skipped (redirect stubs)

- `50-30-20-budget-rule.html`
- `average-credit-card-debt-by-income.html`
- `average-monthly-expenses.html`
- `best-way-to-pay-off-credit-card-debt.html`
- `can-i-afford-to-live-alone.html`
- `cost-of-living-california-vs-texas.html`
- `debt/financial-health/why-paying-minimum-is-bad.html`
- `debt/life-decisions/hourly-to-salary-after-tax.html`
- `debt/life-decisions/rent-vs-buy-calculator.html`
- `how-credit-card-interest-works.html`
- `how-much-credit-card-debt-is-normal.html`
- `how-much-house-can-i-afford-in-california.html`
- `how-much-house-can-i-afford.html`
- `how-much-rent-can-i-afford.html`
- `living/family-budgeting/50-30-20-budget-rule.html`
- `living/family-budgeting/average-monthly-expenses.html`
- `nyc-vs-austin-cost-of-living.html`
- `rent-vs-buy-california.html`
- `salary-needed-to-live-comfortably.html`
- `seattle-vs-denver-cost-of-living.html`
- `what-is-credit-card-apr.html`
- `when-buying-is-better-than-renting.html`
- `why-paying-minimum-is-bad.html`

## Summary

- Avg body words: **1072**
- Avg Flesch Reading Ease: **68.6** (target > 60)
- Pages flagged THIN (<600 words): **3**
- Pages flagged HARD-TO-READ (FRE < 60): **4**
- Pages without a table/chart/svg visual: **6**
- Pages without any interactive element: **5**
- Pages with LOW-EXAMPLES (<5 $ and <3 %): **4**
- Pages with 3+ AI-generic phrases: **0**
