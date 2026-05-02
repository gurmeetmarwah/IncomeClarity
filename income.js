function formatCurrency(amount) {
  return new Intl.NumberFormat("en-US", {
    style: "currency",
    currency: "USD",
    maximumFractionDigits: 0
  }).format(amount);
}

function clamp(value, min, max) {
  return Math.min(Math.max(value, min), max);
}

function bar(label, width, toneClass) {
  return `
    <div>
      <div class="viz-label">${label}</div>
      <div class="viz-bar-wrap">
        <div class="viz-bar ${toneClass}" style="width:${clamp(width, 2, 100)}%"></div>
      </div>
    </div>
  `;
}

function formatHourlyForTitle(rate) {
  if (!Number.isFinite(rate) || rate <= 0) {
    return "—";
  }
  const rounded = Math.round(rate * 100) / 100;
  return Number.isInteger(rounded) ? String(rounded) : rounded.toFixed(2).replace(/\.?0+$/, "");
}

function getLifestyleInsight(annualGross) {
  if (annualGross < 42000) {
    return {
      title: "Budget-focused",
      text: "Rent and essentials may use most of your take-home—keeping housing toward the lower end of the rent range leaves more room for savings and emergencies."
    };
  }
  if (annualGross < 70000) {
    return {
      title: "Balanced in many markets",
      text: "If rent stays near the 30% target, you can usually cover basics plus steady savings, depending on debt and local prices."
    };
  }
  return {
    title: "More flexibility",
    text: "More room for savings and everyday spending while still following typical rent guidelines—especially if housing stays inside the range above."
  };
}

function calculateProgressiveTax(taxableIncome, brackets) {
  if (taxableIncome <= 0) {
    return 0;
  }
  let tax = 0;
  for (let i = 0; i < brackets.length; i += 1) {
    const bracket = brackets[i];
    const nextMin = i < brackets.length - 1 ? brackets[i + 1].min : Number.POSITIVE_INFINITY;
    const amountInBracket = Math.max(0, Math.min(taxableIncome, nextMin) - bracket.min);
    if (amountInBracket > 0) {
      tax += amountInBracket * bracket.rate;
    }
  }
  return tax;
}

const federalBracketsSingle = [
  { min: 0, rate: 0.1 },
  { min: 11600, rate: 0.12 },
  { min: 47150, rate: 0.22 },
  { min: 100525, rate: 0.24 },
  { min: 191950, rate: 0.32 },
  { min: 243725, rate: 0.35 },
  { min: 609350, rate: 0.37 }
];

const federalStandardDeduction = 14600;
const socialSecurityWageBase = 168600;
const socialSecurityRate = 0.062;
const medicareRate = 0.0145;

function estimateTaxes(annualGross, stateCode) {
  const taxableFederalIncome = Math.max(0, annualGross - federalStandardDeduction);
  const federalTax = calculateProgressiveTax(taxableFederalIncome, federalBracketsSingle);
  const socialSecurityTax = Math.min(annualGross, socialSecurityWageBase) * socialSecurityRate;
  const medicareTax = annualGross * medicareRate;
  const stateRate = getStateEffectiveRate(stateCode, annualGross);
  const stateTax = annualGross * stateRate;
  const totalTax = federalTax + socialSecurityTax + medicareTax + stateTax;
  const annualNet = annualGross - totalTax;
  const averageTaxRate = annualGross > 0 ? (totalTax / annualGross) * 100 : 0;

  let marginalRate = 0;
  for (let i = federalBracketsSingle.length - 1; i >= 0; i -= 1) {
    if (taxableFederalIncome >= federalBracketsSingle[i].min) {
      marginalRate = federalBracketsSingle[i].rate;
      break;
    }
  }
  const ficaMarginal = annualGross < socialSecurityWageBase ? socialSecurityRate + medicareRate : medicareRate;
  const marginalTaxRate = (marginalRate + stateRate + ficaMarginal) * 100;

  return {
    federalTax,
    socialSecurityTax,
    medicareTax,
    stateTax,
    totalTax,
    annualNet,
    averageTaxRate,
    marginalTaxRate
  };
}

function makeStateTakeHomeRows(annualGross) {
  const entries = Object.keys(stateTaxData).map((code) => {
    const tax = estimateTaxes(annualGross, code);
    return {
      code,
      name: stateTaxData[code]?.name || code,
      netPay: tax.annualNet,
      averageTax: tax.averageTaxRate
    };
  });
  entries.sort((a, b) => b.netPay - a.netPay);
  return entries;
}

const stateTaxData = {
  AL: { name: "Alabama", rate: 0.04 },
  AK: { name: "Alaska", rate: 0 },
  AZ: { name: "Arizona", rate: 0.025 },
  AR: { name: "Arkansas", rate: 0.04 },
  CA: { name: "California", rate: 0.042 },
  CO: { name: "Colorado", rate: 0.04 },
  CT: { name: "Connecticut", rate: 0.058 },
  DE: { name: "Delaware", rate: 0.05 },
  FL: { name: "Florida", rate: 0 },
  GA: { name: "Georgia", rate: 0.047 },
  HI: { name: "Hawaii", rate: 0.056 },
  ID: { name: "Idaho", rate: 0.05 },
  IL: { name: "Illinois", rate: 0.0495 },
  IN: { name: "Indiana", rate: 0.0315 },
  IA: { name: "Iowa", rate: 0.047 },
  KS: { name: "Kansas", rate: 0.05 },
  KY: { name: "Kentucky", rate: 0.04 },
  LA: { name: "Louisiana", rate: 0.03 },
  ME: { name: "Maine", rate: 0.06 },
  MD: { name: "Maryland", rate: 0.05 },
  MA: { name: "Massachusetts", rate: 0.05 },
  MI: { name: "Michigan", rate: 0.0425 },
  MN: { name: "Minnesota", rate: 0.06 },
  MS: { name: "Mississippi", rate: 0.04 },
  MO: { name: "Missouri", rate: 0.045 },
  MT: { name: "Montana", rate: 0.05 },
  NE: { name: "Nebraska", rate: 0.05 },
  NV: { name: "Nevada", rate: 0 },
  NH: { name: "New Hampshire", rate: 0 },
  NJ: { name: "New Jersey", rate: 0.049 },
  NM: { name: "New Mexico", rate: 0.045 },
  NY: { name: "New York", rate: 0.051 },
  NC: { name: "North Carolina", rate: 0.045 },
  ND: { name: "North Dakota", rate: 0.02 },
  OH: { name: "Ohio", rate: 0.035 },
  OK: { name: "Oklahoma", rate: 0.04 },
  OR: { name: "Oregon", rate: 0.054 },
  PA: { name: "Pennsylvania", rate: 0.0307 },
  RI: { name: "Rhode Island", rate: 0.055 },
  SC: { name: "South Carolina", rate: 0.04 },
  SD: { name: "South Dakota", rate: 0 },
  TN: { name: "Tennessee", rate: 0 },
  TX: { name: "Texas", rate: 0 },
  UT: { name: "Utah", rate: 0.045 },
  VT: { name: "Vermont", rate: 0.06 },
  VA: { name: "Virginia", rate: 0.05 },
  WA: { name: "Washington", rate: 0 },
  WV: { name: "West Virginia", rate: 0.05 },
  WI: { name: "Wisconsin", rate: 0.053 },
  WY: { name: "Wyoming", rate: 0 },
  DC: { name: "District of Columbia", rate: 0.065 }
};

function getIncomeBand(annualGross) {
  if (annualGross < 40000) {
    return "low";
  }
  if (annualGross <= 100000) {
    return "mid";
  }
  return "high";
}

function getStateEffectiveRate(stateCode, annualGross) {
  const baseRate = stateTaxData[stateCode]?.rate ?? 0.04;
  const incomeBand = getIncomeBand(annualGross);

  const bandAdjustments = {
    CA: { low: -0.004, mid: 0, high: 0.01 },
    NY: { low: -0.003, mid: 0, high: 0.009 },
    OR: { low: -0.004, mid: 0, high: 0.01 },
    HI: { low: -0.003, mid: 0, high: 0.009 },
    CT: { low: -0.002, mid: 0, high: 0.007 },
    NJ: { low: -0.002, mid: 0, high: 0.006 },
    MN: { low: -0.002, mid: 0, high: 0.006 },
    VT: { low: -0.002, mid: 0, high: 0.006 },
    MA: { low: -0.001, mid: 0, high: 0.004 }
  };

  const adjustment = bandAdjustments[stateCode]?.[incomeBand] ?? 0;
  return clamp(baseRate + adjustment, 0, 0.15);
}

function getAverageSavingsRate(annualGross) {
  if (annualGross < 40000) {
    return 0.05;
  }
  if (annualGross < 70000) {
    return 0.08;
  }
  if (annualGross < 100000) {
    return 0.11;
  }
  return 0.14;
}

const hourlySalaryForm = document.getElementById("hourly-salary-form");
const hourlySalaryResult = document.getElementById("hourly-salary-result");
const stateTaxTablePanel = document.getElementById("state-tax-table-panel");
const stateInput = document.getElementById("state");
const stateList = document.getElementById("state-list");
const sortedStateCodes = Object.keys(stateTaxData).sort((a, b) => {
  return stateTaxData[a].name.localeCompare(stateTaxData[b].name);
});

function resolveStateCode(rawValue) {
  const normalized = String(rawValue || "").trim().toLowerCase();
  if (!normalized) {
    return "";
  }

  const exactCode = sortedStateCodes.find((code) => code.toLowerCase() === normalized);
  if (exactCode) {
    return exactCode;
  }

  const exactName = sortedStateCodes.find((code) => stateTaxData[code].name.toLowerCase() === normalized);
  if (exactName) {
    return exactName;
  }

  const prefixMatch = sortedStateCodes.find((code) => stateTaxData[code].name.toLowerCase().startsWith(normalized));
  if (prefixMatch) {
    return prefixMatch;
  }

  const containsMatch = sortedStateCodes.find((code) => stateTaxData[code].name.toLowerCase().includes(normalized));
  return containsMatch || "";
}

if (stateList) {
  for (const code of sortedStateCodes) {
    const option = document.createElement("option");
    option.value = stateTaxData[code].name;
    stateList.appendChild(option);
  }
}

if (stateInput) {
  stateInput.addEventListener("blur", () => {
    const matchedCode = resolveStateCode(stateInput.value);
    if (matchedCode) {
      stateInput.value = stateTaxData[matchedCode].name;
    }
  });

  stateInput.addEventListener("keydown", (event) => {
    if (event.key === "Enter") {
      const matchedCode = resolveStateCode(stateInput.value);
      if (matchedCode) {
        stateInput.value = stateTaxData[matchedCode].name;
      }
    }
  });
}

function renderStateTaxTable(annualGross, stateCode) {
  if (!stateTaxTablePanel) {
    return;
  }

  const stateRows = makeStateTakeHomeRows(annualGross);
  const collapsedRows = stateRows.slice(0, 10);
  const expandedRows = stateRows.slice(10);
  const collapsedRowsHtml = collapsedRows
    .map((row, index) => {
      return `
        <tr ${row.code === stateCode ? 'class="is-selected-state"' : ""}>
          <td>${index + 1}</td>
          <td>${row.name}</td>
          <td>${formatCurrency(row.netPay)}</td>
          <td>${row.averageTax.toFixed(1)}%</td>
        </tr>
      `;
    })
    .join("");
  const expandedRowsHtml = expandedRows
    .map((row, index) => {
      return `
        <tr class="extra-state-row${row.code === stateCode ? " is-selected-state" : ""}">
          <td>${index + 11}</td>
          <td>${row.name}</td>
          <td>${formatCurrency(row.netPay)}</td>
          <td>${row.averageTax.toFixed(1)}%</td>
        </tr>
      `;
    })
    .join("");

  stateTaxTablePanel.innerHTML = `
    <h3>Tax by state in United States of America (estimated)</h3>
    <p>Take-home comparison for the same gross income across all US states and DC.</p>
    <table class="state-tax-table">
      <thead>
        <tr>
          <th>Rank</th>
          <th>State</th>
          <th>Net pay</th>
          <th>Average tax</th>
        </tr>
      </thead>
      <tbody>
        ${collapsedRowsHtml}
        ${expandedRowsHtml}
      </tbody>
    </table>
    <button type="button" class="btn secondary show-more-btn" id="toggle-states">Show more states</button>
  `;

  const toggleButton = stateTaxTablePanel.querySelector("#toggle-states");
  const extraRows = stateTaxTablePanel.querySelectorAll(".extra-state-row");
  let expanded = false;
  extraRows.forEach((row) => {
    row.style.display = "none";
  });

  if (toggleButton) {
    if (extraRows.length === 0) {
      toggleButton.style.display = "none";
    }
    toggleButton.addEventListener("click", () => {
      expanded = !expanded;
      extraRows.forEach((row) => {
        row.style.display = expanded ? "table-row" : "none";
      });
      toggleButton.textContent = expanded ? "Show fewer states" : "Show more states";
    });
  }
}

const defaultAnnualGross = 25 * 40 * 52;
renderStateTaxTable(defaultAnnualGross, "TX");

hourlySalaryForm?.addEventListener("submit", (event) => {
  event.preventDefault();

  const hourlyRate = Number(document.getElementById("hourly-rate")?.value);
  const hoursPerWeek = Number(document.getElementById("hours-per-week")?.value);
  const rawStateInput = String(stateInput?.value || "").trim();
  const stateCode = resolveStateCode(rawStateInput);

  if (!hourlyRate || !hoursPerWeek || !stateCode) {
    hourlySalaryResult.innerHTML = "<p>Please enter hourly wage, hours/week, and a valid state.</p>";
    return;
  }

  const annualGross = hourlyRate * hoursPerWeek * 52;
  const tax = estimateTaxes(annualGross, stateCode);
  const federalTax = tax.federalTax;
  const socialSecurityTax = tax.socialSecurityTax;
  const medicareTax = tax.medicareTax;
  const stateTax = tax.stateTax;
  const totalTax = tax.totalTax;
  const annualNet = tax.annualNet;
  const monthlyNet = annualNet / 12;
  const biweeklyNet = annualNet / 26;
  const weeklyNet = annualNet / 52;
  const suggestedRentMonthly = monthlyNet * 0.3;
  const suggestedRentYearly = suggestedRentMonthly * 12;
  const averageSavingsRate = getAverageSavingsRate(annualGross);
  const averageSavingsMonthly = monthlyNet * averageSavingsRate;
  const averageSavingsYearly = averageSavingsMonthly * 12;
  const goodLifestyleSavingsRate = 0.2;
  const goodLifestyleSavingsMonthly = monthlyNet * goodLifestyleSavingsRate;
  const goodLifestyleSavingsYearly = goodLifestyleSavingsMonthly * 12;
  const savingsGapMonthly = goodLifestyleSavingsMonthly - averageSavingsMonthly;
  const savingsGapYearly = goodLifestyleSavingsYearly - averageSavingsYearly;
  const rentRangeLow = monthlyNet * 0.25;
  const rentRangeHigh = monthlyNet * 0.35;
  const lifestyle = getLifestyleInsight(annualGross);
  const hourlyTitle = formatHourlyForTitle(hourlyRate);

  const annualGrossPct = 100;
  const federalPct = (federalTax / annualGross) * 100;
  const socialSecurityPct = (socialSecurityTax / annualGross) * 100;
  const medicarePct = (medicareTax / annualGross) * 100;
  const statePct = (stateTax / annualGross) * 100;
  const netPct = (annualNet / annualGross) * 100;
  hourlySalaryResult.innerHTML = `
    <div class="income-kpi-grid">
      <article class="kpi-card">
        <span class="kpi-label">Yearly salary (gross)</span>
        <strong>${formatCurrency(annualGross)}</strong>
      </article>
      <article class="kpi-card">
        <span class="kpi-label">After-tax income (yearly)</span>
        <strong>${formatCurrency(annualNet)}</strong>
      </article>
      <article class="kpi-card">
        <span class="kpi-label">Monthly income (after tax)</span>
        <strong>${formatCurrency(monthlyNet)}</strong>
      </article>
      <article class="kpi-card">
        <span class="kpi-label">Biweekly income (after tax)</span>
        <strong>${formatCurrency(biweeklyNet)}</strong>
      </article>
      <article class="kpi-card">
        <span class="kpi-label">Weekly income (after tax)</span>
        <strong>${formatCurrency(weeklyNet)}</strong>
      </article>
    </div>
    <section class="affordability-section" aria-labelledby="affordability-heading">
      <h2 id="affordability-heading" class="affordability-h2">What can you afford on $${hourlyTitle}/hour?</h2>
      <p class="affordability-lead">Planning snapshot from your estimated take-home—not a lease or loan qualification.</p>
      <div class="affordability-pillars">
        <article class="affordability-pillar">
          <h3 class="affordability-pillar-title">Rent range</h3>
          <p class="affordability-pillar-value">${formatCurrency(rentRangeLow)} – ${formatCurrency(rentRangeHigh)}<span class="affordability-unit">/month</span></p>
          <p class="affordability-pillar-note">Typical band is about <strong>25–35%</strong> of take-home. Many budgets target near <strong>30%</strong> (~${formatCurrency(suggestedRentMonthly)}/mo · ~${formatCurrency(suggestedRentYearly)}/yr).</p>
        </article>
        <article class="affordability-pillar">
          <h3 class="affordability-pillar-title">Savings potential</h3>
          <p class="affordability-pillar-value">${formatCurrency(averageSavingsMonthly)} – ${formatCurrency(goodLifestyleSavingsMonthly)}<span class="affordability-unit">/month</span></p>
          <p class="affordability-pillar-note">From <strong>typical U.S. savings</strong> at this income (${(averageSavingsRate * 100).toFixed(0)}%) up to a <strong>20%</strong> savings goal. Closing that gap adds about <strong>${formatCurrency(savingsGapMonthly)}/mo</strong> (~${formatCurrency(savingsGapYearly)}/yr).</p>
        </article>
        <article class="affordability-pillar">
          <h3 class="affordability-pillar-title">Lifestyle level</h3>
          <p class="affordability-pillar-lifestyle">${lifestyle.title}</p>
          <p class="affordability-pillar-note">${lifestyle.text}</p>
        </article>
      </div>
    </section>
    <div class="tax-breakdown">
      <h3>Estimated tax and withholding breakdown (${stateTaxData[stateCode]?.name || "Selected state"})</h3>
      <p>Gross income: <strong>${formatCurrency(annualGross)}</strong> · Total withholding: <strong>${formatCurrency(totalTax)}</strong></p>
      <div class="viz-row">
        ${bar(`Gross income: ${formatCurrency(annualGross)} (100%)`, annualGrossPct, "viz-gross")}
        ${bar(`Federal tax: ${formatCurrency(federalTax)} (${federalPct.toFixed(1)}%)`, federalPct, "viz-tax")}
        ${bar(`Social Security: ${formatCurrency(socialSecurityTax)} (${socialSecurityPct.toFixed(1)}%)`, socialSecurityPct, "viz-tax")}
        ${bar(`Medicare: ${formatCurrency(medicareTax)} (${medicarePct.toFixed(1)}%)`, medicarePct, "viz-tax")}
        ${bar(`State tax: ${formatCurrency(stateTax)} (${statePct.toFixed(1)}%)`, statePct, "viz-tax")}
        ${bar(`Net pay: ${formatCurrency(annualNet)} (${netPct.toFixed(1)}%)`, netPct, "viz-takehome")}
      </div>
    </div>
    <p class="note">This is an estimate for planning and may differ from actual payroll withholding.</p>
    <p class="note">State rates are modeled as effective withholding estimates with low/mid/high income-band calibration for closer cross-state comparisons.</p>
    <p class="note">Biweekly and weekly figures shown above are after-tax estimates.</p>
  `;
  renderStateTaxTable(annualGross, stateCode);
});
