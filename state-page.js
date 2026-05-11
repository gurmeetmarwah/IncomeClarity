function spFormatCurrency(amount) {
  return new Intl.NumberFormat("en-US", {
    style: "currency",
    currency: "USD",
    maximumFractionDigits: 0
  }).format(amount);
}

function spClamp(value, min, max) {
  return Math.min(Math.max(value, min), max);
}

const SP_FEDERAL_BRACKETS_SINGLE = [
  { min: 0, rate: 0.1 },
  { min: 11600, rate: 0.12 },
  { min: 47150, rate: 0.22 },
  { min: 100525, rate: 0.24 },
  { min: 191950, rate: 0.32 },
  { min: 243725, rate: 0.35 },
  { min: 609350, rate: 0.37 }
];

const SP_FEDERAL_STD_DEDUCTION = 14600;
const SP_SS_WAGE_BASE = 168600;
const SP_SS_RATE = 0.062;
const SP_MEDICARE_RATE = 0.0145;

const SP_STATE_TAX_DATA = {
  CA: { name: "California", rate: 0.042 },
  TX: { name: "Texas", rate: 0 },
  FL: { name: "Florida", rate: 0 },
  NY: { name: "New York", rate: 0.051 },
  WA: { name: "Washington", rate: 0 },
  IL: { name: "Illinois", rate: 0.0495 }
};

const SP_BAND_ADJUSTMENTS = {
  CA: { low: -0.004, mid: 0, high: 0.01 },
  NY: { low: -0.003, mid: 0, high: 0.009 }
};

function spIncomeBand(annualGross) {
  if (annualGross < 40000) return "low";
  if (annualGross <= 100000) return "mid";
  return "high";
}

function spStateEffectiveRate(stateCode, annualGross) {
  const baseRate = SP_STATE_TAX_DATA[stateCode]?.rate ?? 0;
  const band = spIncomeBand(annualGross);
  const adjustment = SP_BAND_ADJUSTMENTS[stateCode]?.[band] ?? 0;
  return spClamp(baseRate + adjustment, 0, 0.15);
}

function spProgressiveTax(taxableIncome, brackets) {
  if (taxableIncome <= 0) return 0;
  let tax = 0;
  for (let i = 0; i < brackets.length; i += 1) {
    const bracket = brackets[i];
    const nextMin = i < brackets.length - 1 ? brackets[i + 1].min : Number.POSITIVE_INFINITY;
    const amountInBracket = Math.max(0, Math.min(taxableIncome, nextMin) - bracket.min);
    if (amountInBracket > 0) tax += amountInBracket * bracket.rate;
  }
  return tax;
}

function spEstimateTaxes(annualGross, stateCode) {
  const taxableFederal = Math.max(0, annualGross - SP_FEDERAL_STD_DEDUCTION);
  const federalTax = spProgressiveTax(taxableFederal, SP_FEDERAL_BRACKETS_SINGLE);
  const ssTax = Math.min(annualGross, SP_SS_WAGE_BASE) * SP_SS_RATE;
  const medicareTax = annualGross * SP_MEDICARE_RATE;
  const stateRate = spStateEffectiveRate(stateCode, annualGross);
  const stateTax = annualGross * stateRate;
  const totalTax = federalTax + ssTax + medicareTax + stateTax;
  const annualNet = Math.max(0, annualGross - totalTax);
  return { federalTax, ssTax, medicareTax, stateTax, totalTax, annualNet };
}

function spStateInsightCopy(stateCode) {
  switch (stateCode) {
    case "CA":
      return "California has some of the highest state income taxes in the US, which can significantly reduce take-home pay.";
    case "NY":
      return "New York applies relatively high state and (in some cities) local taxes, which lowers take-home pay versus no-tax states.";
    case "IL":
      return "Illinois uses a flat state income tax, so the rate stays the same across income levels but still reduces take-home pay.";
    case "TX":
    case "FL":
    case "WA":
      return `${SP_STATE_TAX_DATA[stateCode].name} has no state income tax, so take-home pay is generally higher than in higher-tax states at the same gross income.`;
    default:
      return "Your state's tax rules affect take-home pay alongside federal withholding.";
  }
}

const spTakeHomeLearnLinkHtml = `<p class="take-home-edu"><a href="/what-is-take-home-pay.html">What is take home pay?</a></p>`;

const spStatePageRoot = document.querySelector("[data-state-page]");
const spStateCode = spStatePageRoot?.dataset.stateCode || "CA";
const spStateName = SP_STATE_TAX_DATA[spStateCode]?.name || "your state";
const spForm = document.getElementById("state-salary-form");
const spResult = document.getElementById("state-salary-result");

function spRenderResult(annualGross) {
  if (!spResult) return;
  const tax = spEstimateTaxes(annualGross, spStateCode);
  const monthlyNet = tax.annualNet / 12;
  const biweeklyNet = tax.annualNet / 26;
  const weeklyNet = tax.annualNet / 52;
  const monthlyTakeHome = spFormatCurrency(monthlyNet);
  const biweeklyTakeHome = spFormatCurrency(biweeklyNet);
  const weeklyTakeHome = spFormatCurrency(weeklyNet);
  const yearlyGross = spFormatCurrency(annualGross);
  const yearlyNet = spFormatCurrency(tax.annualNet);
  const stateTaxStr = spFormatCurrency(tax.stateTax);
  const federalTaxStr = spFormatCurrency(tax.federalTax);

  spResult.innerHTML = `
    <div class="state-salary-kpis">
      <article class="state-salary-kpi">
        <span>Yearly salary (gross)</span>
        <strong>${yearlyGross}</strong>
      </article>
      <article class="state-salary-kpi state-salary-kpi--primary">
        <span>Take home (yearly)</span>
        <strong>${yearlyNet}</strong>
      </article>
      <article class="state-salary-kpi">
        <span>Take home (monthly)</span>
        <strong>${monthlyTakeHome}</strong>
      </article>
      <article class="state-salary-kpi">
        <span>Take home (biweekly)</span>
        <strong>${biweeklyTakeHome}</strong>
      </article>
      <article class="state-salary-kpi">
        <span>Take home (weekly)</span>
        <strong>${weeklyTakeHome}</strong>
      </article>
      <article class="state-salary-kpi">
        <span>Estimated ${spStateName} tax</span>
        <strong>${stateTaxStr}</strong>
      </article>
      <article class="state-salary-kpi">
        <span>Federal tax</span>
        <strong>${federalTaxStr}</strong>
      </article>
    </div>
    ${spTakeHomeLearnLinkHtml}
    <p class="state-salary-insight" role="note">${spStateInsightCopy(spStateCode)}</p>
    <p class="note">Estimate only—actual withholding can vary by filing status, deductions, and local taxes.</p>
  `;
}

spForm?.addEventListener("submit", (event) => {
  event.preventDefault();
  const hourly = Number(document.getElementById("state-hourly-rate")?.value);
  const hours = Number(document.getElementById("state-hours-per-week")?.value);
  if (!hourly || !hours) {
    if (spResult) {
      spResult.innerHTML = '<p class="note">Please enter a valid hourly wage and hours per week.</p>';
    }
    return;
  }
  const annualGross = hourly * hours * 52;
  spRenderResult(annualGross);
});

document.addEventListener("DOMContentLoaded", () => {
  const previewGross = 25 * 40 * 52;
  spRenderResult(previewGross);
});
