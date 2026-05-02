/** US approximate combined state income tax factor on taxable-like income (education only — not exact). */
const STATE_EFFECTIVE = {
  AL: 0.052,
  AK: 0,
  AZ: 0.028,
  AR: 0.055,
  CA: 0.078,
  CO: 0.044,
  CT: 0.055,
  DE: 0.055,
  DC: 0.065,
  FL: 0,
  GA: 0.053,
  HI: 0.062,
  ID: 0.058,
  IL: 0.0495,
  IN: 0.0323,
  IA: 0.062,
  KS: 0.052,
  KY: 0.04,
  LA: 0.042,
  ME: 0.063,
  MD: 0.055,
  MA: 0.05,
  MI: 0.0425,
  MN: 0.076,
  MS: 0.052,
  MO: 0.048,
  MT: 0.059,
  NE: 0.055,
  NV: 0,
  NH: 0.05,
  NJ: 0.063,
  NM: 0.048,
  NY: 0.064,
  NC: 0.049,
  ND: 0.022,
  OH: 0.039,
  OK: 0.048,
  OR: 0.076,
  PA: 0.0307,
  RI: 0.056,
  SC: 0.065,
  SD: 0,
  TN: 0,
  TX: 0,
  UT: 0.048,
  VT: 0.062,
  VA: 0.053,
  WA: 0,
  WV: 0.055,
  WI: 0.056,
  WY: 0
};

const STATE_NAMES = [
  ["AL", "Alabama"],
  ["AK", "Alaska"],
  ["AZ", "Arizona"],
  ["AR", "Arkansas"],
  ["CA", "California"],
  ["CO", "Colorado"],
  ["CT", "Connecticut"],
  ["DE", "Delaware"],
  ["DC", "District of Columbia"],
  ["FL", "Florida"],
  ["GA", "Georgia"],
  ["HI", "Hawaii"],
  ["ID", "Idaho"],
  ["IL", "Illinois"],
  ["IN", "Indiana"],
  ["IA", "Iowa"],
  ["KS", "Kansas"],
  ["KY", "Kentucky"],
  ["LA", "Louisiana"],
  ["ME", "Maine"],
  ["MD", "Maryland"],
  ["MA", "Massachusetts"],
  ["MI", "Michigan"],
  ["MN", "Minnesota"],
  ["MS", "Mississippi"],
  ["MO", "Missouri"],
  ["MT", "Montana"],
  ["NE", "Nebraska"],
  ["NV", "Nevada"],
  ["NH", "New Hampshire"],
  ["NJ", "New Jersey"],
  ["NM", "New Mexico"],
  ["NY", "New York"],
  ["NC", "North Carolina"],
  ["ND", "North Dakota"],
  ["OH", "Ohio"],
  ["OK", "Oklahoma"],
  ["OR", "Oregon"],
  ["PA", "Pennsylvania"],
  ["RI", "Rhode Island"],
  ["SC", "South Carolina"],
  ["SD", "South Dakota"],
  ["TN", "Tennessee"],
  ["TX", "Texas"],
  ["UT", "Utah"],
  ["VT", "Vermont"],
  ["VA", "Virginia"],
  ["WA", "Washington"],
  ["WV", "West Virginia"],
  ["WI", "Wisconsin"],
  ["WY", "Wyoming"]
];

/** 2024 federal ordinary brackets — taxable income after standard deduction. */
const BRACKET_TOPS_SINGLE = [11600, 47150, 100525, 191950, 243725, 609350, Infinity];
const BRACKET_TOPS_MFJ = [23200, 94300, 201050, 383900, 487450, 731200, Infinity];
const BRACKET_RATES = [0.1, 0.12, 0.22, 0.24, 0.32, 0.35, 0.37];

const STANDARD_DED_SINGLE = 14600;
const STANDARD_DED_MFJ = 29200;
const SS_WAGE_BASE = 168600;
const ELECTIVE_DEFERRAL_CAP = 23000;

function usd(amount) {
  return new Intl.NumberFormat("en-US", {
    style: "currency",
    currency: "USD",
    maximumFractionDigits: 0
  }).format(amount);
}

function federalIncomeTax(taxableIncome, filingMarried) {
  const ti = Math.max(0, taxableIncome);
  const tops = filingMarried ? BRACKET_TOPS_MFJ : BRACKET_TOPS_SINGLE;
  let tax = 0;
  let prev = 0;
  for (let i = 0; i < BRACKET_RATES.length; i += 1) {
    const top = tops[i];
    const rate = BRACKET_RATES[i];
    const bandWidth = Math.min(ti, top) - prev;
    if (bandWidth > 0) {
      tax += bandWidth * rate;
    }
    prev = top;
    if (ti <= top) {
      break;
    }
  }
  return tax;
}

function employeeFica(wages, filingMarried) {
  const w = Math.max(0, wages);
  const ss = Math.min(w, SS_WAGE_BASE) * 0.062;
  const med = w * 0.0145;
  const th = filingMarried ? 250000 : 200000;
  const addMed = Math.max(0, w - th) * 0.009;
  return ss + med + addMed;
}

function selfEmploymentTax(netProfit, filingMarried) {
  const base = Math.max(0, netProfit) * 0.9235;
  const ss = Math.min(base, SS_WAGE_BASE) * 0.124;
  const med = base * 0.029;
  const th = filingMarried ? 250000 : 200000;
  const addMed = Math.max(0, base - th) * 0.009;
  return ss + med + addMed;
}

function standardDed(filingMarried) {
  return filingMarried ? STANDARD_DED_MFJ : STANDARD_DED_SINGLE;
}

function boundedRetirement(amount, gross) {
  const r = Math.max(0, amount);
  return Math.min(r, Math.min(ELECTIVE_DEFERRAL_CAP, gross));
}

function stateFactor(code) {
  return STATE_EFFECTIVE[code] ?? 0.05;
}

/**
 * @returns {{ gross: number, fica: number, federal: number, state: number, taxesPaid: number, net: number }}
 */
function computeW2(inputs) {
  const filingMarried = inputs.filing === "married";
  const gross = Math.max(0, inputs.annualIncome);
  const retirement = boundedRetirement(inputs.retirement, gross);
  const wages = Math.max(0, gross - retirement);
  const fica = employeeFica(wages, filingMarried);
  const fedTaxable = Math.max(0, wages - standardDed(filingMarried));
  const federal = federalIncomeTax(fedTaxable, filingMarried);
  const stFactor = stateFactor(inputs.state);
  const stateBase = Math.max(0, fedTaxable);
  const state = Math.max(0, stateBase * stFactor + inputs.stateAdjustment);
  const taxesPaid = fica + federal + state;
  const net = gross - fica - federal - state - retirement;
  return { gross, fica, federal, state, taxesPaid, net };
}

/**
 * @returns detail lines for 1099 path
 */
function compute1099(inputs) {
  const filingMarried = inputs.filing === "married";
  const gross = Math.max(0, inputs.annualIncome);
  const expenses = Math.max(0, inputs.businessExpenses);
  const netProfit = Math.max(0, gross - expenses);
  const seTax = selfEmploymentTax(netProfit, filingMarried);
  const halfSe = seTax * 0.5;
  const health = Math.max(0, inputs.healthInsurance);
  const retirement = boundedRetirement(inputs.retirement, gross);
  const deductionPct = Math.min(20, Math.max(0, inputs.deductionRatePct));
  const modeledBizDeduction = netProfit * (deductionPct / 100);

  const fedTaxableBeforeQBI = Math.max(
    0,
    netProfit - halfSe - health - retirement - modeledBizDeduction
  );
  const fedTaxable = Math.max(0, fedTaxableBeforeQBI - standardDed(filingMarried));
  const federal = federalIncomeTax(fedTaxable, filingMarried);
  const stFactor = stateFactor(inputs.state);
  const state = Math.max(0, fedTaxable * stFactor + inputs.stateAdjustment);
  const incomeTaxTotal = federal + state;
  const net = gross - expenses - seTax - federal - state - health - retirement;

  return {
    gross,
    netProfit,
    seTax,
    federal,
    state,
    incomeTaxTotal,
    expenses,
    net,
    modeledBizDeduction
  };
}

function populateStates() {
  const sel = document.getElementById("state");
  if (!sel) {
    return;
  }
  sel.innerHTML = STATE_NAMES.map(
    ([code, name]) => `<option value="${code}">${name}</option>`
  ).join("");
  sel.value = "CA";
}

function syncDeductionLabel() {
  const input = document.getElementById("deduction-rate");
  const out = document.getElementById("deduction-rate-value");
  if (input && out) {
    out.textContent = `${input.value}%`;
  }
}

function buildOptimizeSectionHtml(optNoDed, optWithExp, f1099, maxOptNet) {
  return `
    <section class="fl-optimize" aria-labelledby="fl-optimize-title">
      <h2 id="fl-optimize-title" class="fl-optimize-h2">What if you optimize your taxes?</h2>
      <p class="fl-optimize-intro">Your <strong>1099 (freelance)</strong> take-home with the same gross, state, filing status, and health insurance as the form—showing how tracking write-offs and saving for retirement can change what you keep.</p>
      <div class="fl-optimize-table-wrap" role="region" aria-label="Take-home by optimization scenario" tabindex="0">
        <table class="fl-optimize-table">
          <thead>
            <tr>
              <th scope="col">Scenario</th>
              <th scope="col" class="fl-optimize-th-num">Take-home</th>
            </tr>
          </thead>
          <tbody>
            <tr class="${optNoDed.net === maxOptNet ? "fl-optimize-row--best" : ""}">
              <td>
                <span class="fl-optimize-scenario">No deductions</span>
                <span class="fl-optimize-hint">No business expenses, no business-deduction %, no retirement in the model</span>
              </td>
              <td class="fl-optimize-cell-num">${usd(optNoDed.net)}</td>
            </tr>
            <tr class="${optWithExp.net === maxOptNet ? "fl-optimize-row--best" : ""}">
              <td>
                <span class="fl-optimize-scenario">With expenses</span>
                <span class="fl-optimize-hint">Your business expenses and QBI-style %; retirement set to $0 for this row</span>
              </td>
              <td class="fl-optimize-cell-num">${usd(optWithExp.net)}</td>
            </tr>
            <tr class="${f1099.net === maxOptNet ? "fl-optimize-row--best" : ""}">
              <td>
                <span class="fl-optimize-scenario">With retirement</span>
                <span class="fl-optimize-hint">Expenses, business deduction %, and your traditional retirement (advanced), if any</span>
              </td>
              <td class="fl-optimize-cell-num">${usd(f1099.net)}</td>
            </tr>
          </tbody>
        </table>
      </div>
      <p class="fl-optimize-foot">Best case in this table is the <strong>highest</strong> take-home. If you have $0 in advanced retirement, the last two rows may match—add a retirement number to see the lift.</p>
    </section>
  `;
}

function buildMeansSectionHtml(w2, f1099, optNoDed, base) {
  const gross = base.annualIncome;
  const lift = f1099.net - optNoDed.net;
  const naiveGap = optNoDed.net - w2.net;
  const finalGap = f1099.net - w2.net;

  let line1;
  if (naiveGap < -500) {
    line1 = `At <strong>${usd(gross)}</strong> gross—the same headline number on both sides—your “no deductions” freelance take-home (<strong>${usd(optNoDed.net)}</strong>) lands <strong>${usd(Math.abs(naiveGap))} lower</strong> than W-2 (<strong>${usd(w2.net)}</strong>). Freelancers often chase the same gross as a salary, but <strong>total tax load</strong> (especially self-employment tax and no employer match) bites harder when you don’t plan around it.`;
  } else if (naiveGap > 500) {
    line1 = `At <strong>${usd(gross)}</strong> gross, even the bare-bones freelance row still shows <strong>${usd(naiveGap)} more</strong> take-home than W-2 in this run—driven by your state, filing status, and other inputs. That won’t be everyone’s story; many 1099 earners see the opposite until they add real costs. Use this as your snapshot, not a rule.`;
  } else {
    line1 = `At <strong>${usd(gross)}</strong> gross, W-2 and a minimal 1099 (no expenses or retirement in the “no deductions” row) are <strong>roughly even</strong> on take-home in this model. The pattern to remember: freelance income still carries <strong>extra tax moving parts</strong> than a paycheck, so it’s worth mapping them on purpose.`;
  }

  let line2;
  if (lift > 300) {
    if (finalGap > 0 && naiveGap < 0) {
      line2 = `After we layer in <strong>your business expenses</strong>, <strong>deduction rate</strong>, and <strong>retirement</strong> (if you entered any), freelance take-home rises <strong>${usd(lift)}</strong> versus the “no deductions” row. You went from <strong>trailing W-2</strong> on the naive row to <strong>ahead by ${usd(finalGap)}</strong> when optimized—an example of how <strong>write-offs and savings can shrink or reverse the gap</strong>.`;
    } else if (finalGap > 0) {
      line2 = `With <strong>expenses, business deduction %, and retirement</strong> in the model, your freelance take-home adds <strong>${usd(lift)}</strong> versus the stripped-down row, finishing at <strong>${usd(f1099.net)}</strong>—still <strong>ahead of W-2</strong> on these numbers. That’s the benefit of building planning into the year, not just at tax time.`;
    } else {
      line2 = `Modeling <strong>deductions and retirement</strong> adds <strong>${usd(lift)}</strong> to your freelance take-home versus the “no deductions” row. W-2 still leads on this run, but the <strong>gap with 1099 narrows</strong> as you keep more of what you earn through ordinary business write-offs and pre-tax savings.`;
    }
  } else {
    line2 = `The “no deductions” and “with retirement” rows are <strong>close</strong> here—often when expenses, deduction %, or retirement are small. In real life, as those grow, <strong>the W-2 vs 1099 gap can shrink a lot</strong>. Revisit this after you have a full year of real business costs.`;
  }

  return `
    <section class="fl-means" aria-labelledby="fl-means-title">
      <h2 id="fl-means-title" class="fl-means-h2">What this means for you</h2>
      <p class="fl-means-intro">Grounded in <strong>your inputs</strong> and the comparison above—not generic advice.</p>
      <div class="fl-means-box">
        <p class="fl-means-line">👉 Freelancers often earn more gross—but pay significantly more tax without planning. ${line1}</p>
        <p class="fl-means-line">👉 With deductions, the gap can shrink or even reverse. ${line2}</p>
      </div>
    </section>
  `;
}

const freelanceForm = document.getElementById("freelance-form");
const freelanceResult = document.getElementById("freelance-result");
const freelanceOptimizeMount = document.getElementById("freelance-optimize-mount");
const freelanceMeansMount = document.getElementById("freelance-means-mount");

document.getElementById("deduction-rate")?.addEventListener("input", syncDeductionLabel);

populateStates();
syncDeductionLabel();

freelanceForm?.addEventListener("submit", (event) => {
  event.preventDefault();

  const annualIncome = Number(document.getElementById("annual-income")?.value);
  const state = document.getElementById("state")?.value || "CA";
  const filing = document.querySelector('input[name="filing-status"]:checked')?.value || "single";
  const businessExpenses = Number(document.getElementById("business-expenses")?.value) || 0;
  const deductionRatePct = Number(document.getElementById("deduction-rate")?.value) || 0;
  const healthInsurance = Number(document.getElementById("health-insurance")?.value) || 0;
  const retirement = Number(document.getElementById("retirement")?.value) || 0;
  const stateAdjustment = Number(document.getElementById("state-adjustment")?.value) || 0;

  if (!Number.isFinite(annualIncome) || annualIncome < 1) {
    freelanceResult.hidden = false;
    freelanceResult.innerHTML =
      '<p class="fl-result-error">Enter a valid annual income (at least $1).</p>';
    if (freelanceOptimizeMount) {
      freelanceOptimizeMount.hidden = true;
      freelanceOptimizeMount.innerHTML = "";
    }
    if (freelanceMeansMount) {
      freelanceMeansMount.hidden = true;
      freelanceMeansMount.innerHTML = "";
    }
    return;
  }

  const base = {
    annualIncome,
    state,
    filing,
    businessExpenses,
    deductionRatePct,
    healthInsurance,
    retirement,
    stateAdjustment
  };

  const w2 = computeW2(base);
  const f1099 = compute1099(base);
  const optNoDed = compute1099({
    ...base,
    businessExpenses: 0,
    deductionRatePct: 0,
    retirement: 0
  });
  const optWithExp = compute1099({ ...base, retirement: 0 });
  const diff = f1099.net - w2.net;
  const maxOptNet = Math.max(optNoDed.net, optWithExp.net, f1099.net);
  const absDiff = Math.abs(diff);

  let diffClass = "fl-diff-banner--neutral";
  let diffText;
  if (absDiff < 250) {
    diffText = "Your estimated take-home is about the same either way—small differences are normal.";
    diffClass = "fl-diff-banner--neutral";
  } else if (diff < 0) {
    diffText = `You take home <strong>${usd(absDiff)} less</strong> as a freelancer with these inputs.`;
    diffClass = "fl-diff-banner--w2";
  } else {
    diffText = `You take home <strong>${usd(absDiff)} more</strong> as a freelancer with these inputs.`;
    diffClass = "fl-diff-banner--freelance";
  }

  freelanceResult.hidden = false;
  freelanceResult.innerHTML = `
    <div class="fl-diff-banner ${diffClass}">
      <p class="fl-diff-lead">${diffText}</p>
      <p class="fl-diff-sub">Comparison uses the same gross income, your state, filing status, retirement (advanced), and freelancer costs (expenses, insurance, modeled business deduction).</p>
    </div>
    <div class="fl-result-grid">
      <article class="fl-result-card fl-result-w2">
        <header class="fl-result-head">
          <h3 class="fl-result-title">W2 (Employee)</h3>
          <p class="fl-result-tag">Taxes as an employee</p>
        </header>
        <dl class="fl-result-dl">
          <div class="fl-result-row">
            <dt>Gross income</dt>
            <dd>${usd(w2.gross)}</dd>
          </div>
          <div class="fl-result-row">
            <dt>Taxes paid <span class="fl-dt-hint">FICA + federal + state</span></dt>
            <dd>${usd(w2.taxesPaid)}</dd>
          </div>
          <div class="fl-result-row fl-result-row--highlight">
            <dt>Net take-home</dt>
            <dd>${usd(w2.net)}</dd>
          </div>
        </dl>
      </article>
      <article class="fl-result-card fl-result-1099">
        <header class="fl-result-head">
          <h3 class="fl-result-title">1099 (Freelancer)</h3>
          <p class="fl-result-tag">Self-employment + income taxes</p>
        </header>
        <dl class="fl-result-dl">
          <div class="fl-result-row">
            <dt>Gross income</dt>
            <dd>${usd(f1099.gross)}</dd>
          </div>
          <div class="fl-result-row">
            <dt>Self-employment tax</dt>
            <dd>${usd(f1099.seTax)}</dd>
          </div>
          <div class="fl-result-row">
            <dt>Income tax <span class="fl-dt-hint">Federal + state</span></dt>
            <dd>${usd(f1099.incomeTaxTotal)}</dd>
          </div>
          <div class="fl-result-row">
            <dt>Expenses deducted</dt>
            <dd>${usd(f1099.expenses)}</dd>
          </div>
          <div class="fl-result-row fl-result-row--highlight">
            <dt>Net take-home</dt>
            <dd>${usd(f1099.net)}</dd>
          </div>
        </dl>
      </article>
    </div>
    <section class="fl-where-goes" aria-labelledby="fl-where-goes-title">
      <h2 id="fl-where-goes-title" class="fl-where-title">Where your money goes</h2>
      <p class="fl-where-intro">Approximate outflows from your gross, using the same inputs as above.</p>
      <div class="fl-where-grid">
        <div class="fl-where-col fl-where-w2">
          <h3 class="fl-where-h3">W2 (Employee)</h3>
          <dl class="fl-where-dl">
            <div class="fl-where-row">
              <dt>Federal tax</dt>
              <dd>${usd(w2.federal)}</dd>
            </div>
            <div class="fl-where-row">
              <dt>State tax</dt>
              <dd>${usd(w2.state)}</dd>
            </div>
            <div class="fl-where-row">
              <dt>Payroll taxes <span class="fl-where-hint">FICA (Social Security + Medicare)</span></dt>
              <dd>${usd(w2.fica)}</dd>
            </div>
          </dl>
        </div>
        <div class="fl-where-col fl-where-1099">
          <h3 class="fl-where-h3">1099 (Freelancer)</h3>
          <dl class="fl-where-dl">
            <div class="fl-where-row">
              <dt>Self-employment tax</dt>
              <dd>${usd(f1099.seTax)}</dd>
            </div>
            <div class="fl-where-row">
              <dt>Income tax <span class="fl-where-hint">Federal + state</span></dt>
              <dd>${usd(f1099.incomeTaxTotal)}</dd>
            </div>
          </dl>
          <div class="fl-where-deductions">
            <h4 class="fl-where-deductions-title">Deductions</h4>
            <dl class="fl-where-dl fl-where-dl-nested">
              <div class="fl-where-row fl-where-row--sub">
                <dt>Business expenses</dt>
                <dd>${usd(f1099.expenses)}</dd>
              </div>
              <div class="fl-where-row fl-where-row--sub">
                <dt>Self-employed health <span class="fl-where-hint">Deductible</span></dt>
                <dd>${usd(base.healthInsurance)}</dd>
              </div>
              <div class="fl-where-row fl-where-row--sub">
                <dt>Business deduction (QBI-style)</dt>
                <dd>${usd(f1099.modeledBizDeduction)}</dd>
              </div>
              ${
                base.retirement > 0
                  ? `<div class="fl-where-row fl-where-row--sub">
                <dt>Retirement (traditional)</dt>
                <dd>${usd(base.retirement)}</dd>
              </div>`
                  : ""
              }
            </dl>
          </div>
        </div>
      </div>
    </section>
  `;

  if (freelanceOptimizeMount) {
    freelanceOptimizeMount.innerHTML = buildOptimizeSectionHtml(optNoDed, optWithExp, f1099, maxOptNet);
    freelanceOptimizeMount.hidden = false;
  }
  if (freelanceMeansMount) {
    freelanceMeansMount.innerHTML = buildMeansSectionHtml(w2, f1099, optNoDed, base);
    freelanceMeansMount.hidden = false;
  }

  freelanceResult.scrollIntoView({ behavior: "smooth", block: "nearest" });
});
