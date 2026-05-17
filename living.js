function money(amount) {
  return new Intl.NumberFormat("en-US", {
    style: "currency",
    currency: "USD",
    maximumFractionDigits: 0
  }).format(amount);
}

function monthlyPI(principal, annualRatePct, years) {
  if (principal <= 0) {
    return 0;
  }
  const r = annualRatePct / 100 / 12;
  const n = years * 12;
  if (r <= 0) {
    return principal / n;
  }
  return (principal * r * Math.pow(1 + r, n)) / (Math.pow(1 + r, n) - 1);
}

/**
 * Run rent vs buy simulation for a whole number of years.
 */
function simulateRentVsBuy(inputs, yearsStay) {
  const monthlyRent0 = inputs.monthlyRent;
  const rentIncrease = inputs.rentIncrease / 100;
  const renterInsuranceYear = inputs.renterInsurance;
  const homePrice = inputs.homePrice;
  const downPct = inputs.downPct / 100;
  const rate = inputs.interestRate;
  const loanTermYears = inputs.loanTermYears;
  const propertyTaxPct = inputs.propertyTaxPct / 100;
  const maintenanceType = inputs.maintenanceType;
  const maintenanceValue = inputs.maintenanceValue;
  const appreciation = inputs.appreciation / 100;
  const investmentReturn = inputs.investmentReturn / 100;

  const downPayment = homePrice * downPct;
  const loanAmount = Math.max(homePrice - downPayment, 0);
  const monthlyPayment = monthlyPI(loanAmount, rate, loanTermYears);
  const monthlyRate = rate / 100 / 12;
  const totalMonths = yearsStay * 12;
  const maxMonths = Math.min(totalMonths, loanTermYears * 12);

  let balance = loanAmount;
  let rentRunning = monthlyRent0;
  let totalRentOnly = 0;
  let totalRenterInsurance = 0;
  let totalBuyCash = 0;
  let totalInterest = 0;
  let totalPrincipal = 0;
  let totalPropertyTax = 0;
  let totalMaintenance = 0;

  const cumulativeRentSeries = [];
  const cumulativeBuySeries = [];

  for (let m = 1; m <= totalMonths; m += 1) {
    const yearIndex = Math.floor((m - 1) / 12);
    if (m > 1 && (m - 1) % 12 === 0) {
      rentRunning *= 1 + rentIncrease;
    }

    const insuranceMonth = renterInsuranceYear / 12;
    totalRentOnly += rentRunning;
    totalRenterInsurance += insuranceMonth;
    const rentMonth = rentRunning + insuranceMonth;

    if (m === 1) {
      totalBuyCash += downPayment;
    }

    const assessedAnnual = homePrice * Math.pow(1 + appreciation, yearIndex);
    const annualTax = assessedAnnual * propertyTaxPct;
    const monthlyTax = annualTax / 12;
    totalPropertyTax += monthlyTax;

    let monthlyMaint;
    if (maintenanceType === "pct") {
      monthlyMaint = (assessedAnnual * (maintenanceValue / 100)) / 12;
    } else {
      monthlyMaint = maintenanceValue / 12;
    }
    totalMaintenance += monthlyMaint;

    let pi = 0;
    if (m <= maxMonths && balance > 0) {
      const interest = balance * monthlyRate;
      const principal = Math.min(monthlyPayment - interest, balance);
      totalInterest += interest;
      totalPrincipal += principal;
      pi = interest + principal;
      balance -= principal;
    }

    const buyMonth = pi + monthlyTax + monthlyMaint;
    totalBuyCash += buyMonth;

    if (m % 12 === 0) {
      cumulativeRentSeries.push(totalRentOnly + totalRenterInsurance);
      cumulativeBuySeries.push(totalBuyCash);
    }
  }

  const totalRentAndInsurance = totalRentOnly + totalRenterInsurance;
  const totalMortgagePayments = totalInterest + totalPrincipal;

  const homeValueEnd = homePrice * Math.pow(1 + appreciation, yearsStay);
  const equityEnd = Math.max(0, homeValueEnd - balance);

  const fvDown = downPayment * Math.pow(1 + investmentReturn, yearsStay);
  const investmentGainOnDown = fvDown - downPayment;
  const netRentCost = totalRentAndInsurance - investmentGainOnDown;
  const netBuyCost = totalBuyCash - equityEnd;

  const diff = netRentCost - netBuyCost;
  const buyingBetter = diff > 0;
  const margin = Math.abs(diff);

  return {
    yearsStay,
    totalRentOnly,
    totalRenterInsurance,
    totalRentAndInsurance,
    totalBuyCash,
    totalMortgagePayments,
    totalInterest,
    totalPrincipal,
    totalPropertyTax,
    totalMaintenance,
    equityEnd,
    netBuyCost,
    netRentCost,
    buyingBetter,
    margin,
    homeValueEnd,
    remainingLoan: balance,
    cumulativeRentSeries,
    cumulativeBuySeries,
    rentIncreasePct: inputs.rentIncrease,
    monthlyRentStart: monthlyRent0,
    monthlyRentEnd: rentRunning,
    downPayment
  };
}

function computeRentVsBuy(inputs) {
  return simulateRentVsBuy(inputs, inputs.yearsStay);
}

function findBreakEvenYear(inputs, maxYears) {
  let found = null;
  const cap = Math.min(Math.max(maxYears, 1), 40);
  for (let y = 1; y <= cap; y += 1) {
    const sim = simulateRentVsBuy(inputs, y);
    if (sim.netBuyCost < sim.netRentCost) {
      found = y;
      break;
    }
  }
  return found;
}

function buildWhatItMeansHtml(inputs, r, breakEver) {
  const ys = inputs.yearsStay;
  const lines = [];

  if (breakEver === null) {
    lines.push(
      "👉 With these inputs, buying does not beat renting on a net basis within <strong>40 years</strong>—check home price, mortgage rate, taxes, or rent growth."
    );
  } else if (ys < breakEver) {
    lines.push(
      `👉 <strong>Buying only makes sense if you plan to stay at least about ${breakEver} years</strong>—your <strong>${ys}-year</strong> horizon is shorter than that break-even.`
    );
    lines.push(
      "👉 <strong>Short-term? Renting is usually cheaper</strong> when you may move soon—equity and appreciation need time to offset upfront costs."
    );
  } else {
    lines.push(
      `👉 Your <strong>${ys}-year</strong> plan lines up with owning: net cost favors buying by around <strong>year ${breakEver}</strong> under these assumptions.`
    );
  }

  if (ys <= 4 && breakEver !== null && ys < breakEver) {
    lines.push(
      "👉 Need flexibility or a possible move soon? Renting keeps optionality until your timeline is longer."
    );
  }

  if (breakEver !== null && breakEver >= 5 && breakEver <= 7 && ys < breakEver) {
    lines.push(
      `👉 In many U.S. markets, buying needs roughly <strong>5–7 years</strong> to pencil vs renting—your break-even is around <strong>${breakEver} years</strong>.`
    );
  }

  if (ys >= 10 && r.buyingBetter) {
    lines.push(
      "👉 Longer stays give appreciation and loan paydown more room—aligned with your results favoring buying."
    );
  }

  if (!r.buyingBetter && breakEver !== null && ys >= breakEver) {
    lines.push(
      "👉 Renting still wins on net over your full horizon—try adjusting price, down payment, rate, or expected rent growth."
    );
  }

  if (inputs.interestRate >= 7) {
    lines.push(
      "👉 Your rate assumption is relatively high—comparing lender quotes may materially change rent vs buy."
    );
  }

  const uniq = [...new Set(lines)].slice(0, 6);

  return `
    <h2 class="rvb-prose-h2 rvb-means-h2">What this means for you</h2>
    <div class="rvb-means-box">
      ${uniq.map((line) => `<p class="rvb-means-line">${line}</p>`).join("")}
    </div>
  `;
}

function quickGuideOption(sim) {
  const gap = Math.abs(sim.netRentCost - sim.netBuyCost);
  const scale = Math.max(Math.abs(sim.netRentCost), Math.abs(sim.netBuyCost), 1);
  if (gap / scale < 0.07) {
    return "Depends";
  }
  return sim.buyingBetter ? "Buy" : "Rent";
}

function buildQuickDecisionGuideHtml(inputs) {
  const userYears = inputs.yearsStay;
  const simUnder3 = simulateRentVsBuy(inputs, 2);
  const simMid = simulateRentVsBuy(inputs, 7);
  const simTenPlus = simulateRentVsBuy(inputs, 12);

  const optShort = quickGuideOption(simUnder3);
  const optMid = quickGuideOption(simMid);
  const optLong = quickGuideOption(simTenPlus);

  let activeRow = 1;
  if (userYears < 3) {
    activeRow = 0;
  } else if (userYears >= 10) {
    activeRow = 2;
  }

  const rows = [
    {
      situation: "Stay &lt; 3 years",
      option: optShort,
      note: "(2-year check)"
    },
    {
      situation: "Stay 5–10 years",
      option: optMid,
      note: "(7-year midpoint)"
    },
    {
      situation: "Stay 10+ years",
      option: optLong,
      note: "(12-year check)"
    }
  ];

  const rowHtml = rows
    .map((row, i) => {
      const hilite = i === activeRow ? ' class="rvb-guide-highlight"' : "";
      return `<tr${hilite}><td>${row.situation}</td><td><strong>${row.option}</strong> <span class="rvb-guide-note">${row.note}</span></td></tr>`;
    })
    .join("");

  return `
    <div class="rvb-guide-wrap">
      <p class="rvb-guide-intro">Using your rent, price, rate, and assumptions—here is how each typical stay length compares on net cost.</p>
      <div class="rvb-guide-table-scroll">
        <table class="rvb-guide-table">
          <thead>
            <tr>
              <th scope="col">Situation</th>
              <th scope="col">Better option</th>
            </tr>
          </thead>
          <tbody>
            ${rowHtml}
          </tbody>
        </table>
      </div>
      <p class="rvb-guide-your-row"><strong>Your input:</strong> <strong>${userYears} years</strong> planned → highlighted row is the band that matches.</p>
    </div>
  `;
}

function buildBreakEvenSpotlight(breakEvenYear, yearsStay) {
  if (breakEvenYear === null) {
    return `<div class="rvb-break-even-spotlight rvb-break-even-spotlight--soft" role="status">
      <p class="rvb-break-even-spotlight-lead">On a net-cost basis, <strong>renting stays ahead</strong> through your full <strong>${yearsStay}-year</strong> plan with these numbers.</p>
    </div>`;
  }
  const isMilestone = breakEvenYear <= 2;
  const main =
    breakEvenYear === 1
      ? "Buying becomes cheaper after year 1 (first full year in the home)."
      : `Buying becomes cheaper after year ${breakEvenYear}—that’s when net cost (after equity) starts to beat renting under your assumptions.`;
  return `<div class="rvb-break-even-spotlight ${isMilestone ? "rvb-break-even-spotlight--milestone" : ""}" role="status">
    <div class="rvb-break-even-spotlight-badge">Break-even</div>
    <p class="rvb-break-even-spotlight-lead">${main}</p>
    <p class="rvb-break-even-spotlight-note">Think of this as the point where buying’s long-term equity finally offsets higher upfront cash out.</p>
  </div>`;
}

function buildLineChart(rentSeries, buySeries, opts = {}) {
  const breakEvenYear = opts.breakEvenYear;
  const w = 640;
  const h = 340;
  const padL = 52;
  const padR = 24;
  const padT = 36;
  const padB = 44;
  const innerW = w - padL - padR;
  const innerH = h - padT - padB;

  const allVals = [...rentSeries, ...buySeries];
  const maxY = Math.max(...allVals, 1);
  const n = rentSeries.length;
  const stepX = n <= 1 ? innerW / 2 : innerW / Math.max(n - 1, 1);

  function xAt(i) {
    if (n <= 1) {
      return padL + innerW / 2;
    }
    return padL + i * stepX;
  }

  function yAt(v) {
    return padT + innerH - (v / maxY) * innerH;
  }

  const rentPts = rentSeries.map((v, i) => `${xAt(i)},${yAt(v)}`).join(" ");
  const buyPts = buySeries.map((v, i) => `${xAt(i)},${yAt(v)}`).join(" ");

  const ticks = 4;
  let gridLines = "";
  let yLabels = "";
  for (let t = 0; t <= ticks; t += 1) {
    const frac = t / ticks;
    const val = maxY * frac;
    const y = padT + innerH - frac * innerH;
    gridLines += `<line x1="${padL}" y1="${y}" x2="${padL + innerW}" y2="${y}" stroke="#e4edf5" stroke-width="1"/>`;
    yLabels += `<text x="${padL - 8}" y="${y + 4}" text-anchor="end" font-size="11" fill="#627d98">${money(val)}</text>`;
  }

  const yearLabels = rentSeries
    .map((_, i) => {
      const label = i === 0 ? "Start" : `Y${i}`;
      const x = xAt(i);
      return `<text x="${x}" y="${h - 10}" text-anchor="middle" font-size="11" fill="#627d98">${label}</text>`;
    })
    .join("");

  let breakEvenSvg = "";
  if (breakEvenYear != null && breakEvenYear > 0 && breakEvenYear < n) {
    const xbe = xAt(breakEvenYear);
    const yBottom = padT + innerH;
    breakEvenSvg = `
      <line x1="${xbe}" y1="${padT}" x2="${xbe}" y2="${yBottom}" stroke="#c05621" stroke-width="2.5" stroke-dasharray="7 5" class="rvb-chart-be-line" opacity="0.95"/>
      <rect x="${xbe - 56}" y="6" width="112" height="22" rx="6" fill="#fff7ed" stroke="#f6ad55" stroke-width="1.5"/>
      <text x="${xbe}" y="21" text-anchor="middle" font-size="11" font-weight="700" fill="#c05621">Break-even · Year ${breakEvenYear}</text>
    `;
  }

  let dotsSvg = "";
  for (let i = 0; i < n; i += 1) {
    const xr = xAt(i);
    const yr = yAt(rentSeries[i]);
    const yb = yAt(buySeries[i]);
    const yearLabel = i === 0 ? "Start" : `Year ${i}`;
    const rentTip = `${yearLabel} — Rent (cumulative): ${money(rentSeries[i])}`;
    const buyTip = `${yearLabel} — Buy cash out (cumulative): ${money(buySeries[i])}`;
    dotsSvg += `<g class="rvb-chart-point-group">
      <title>${rentTip}</title>
      <circle cx="${xr}" cy="${yr}" r="14" fill="#001a33" fill-opacity="0" class="rvb-chart-point-hit" pointer-events="all"/>
      <circle cx="${xr}" cy="${yr}" r="5" class="rvb-chart-dot rvb-chart-dot-rent" fill="#2d6a9f" stroke="#fff" stroke-width="1.5" pointer-events="none"/>
    </g>`;
    dotsSvg += `<g class="rvb-chart-point-group">
      <title>${buyTip}</title>
      <circle cx="${xr}" cy="${yb}" r="14" fill="#001a33" fill-opacity="0" class="rvb-chart-point-hit" pointer-events="all"/>
      <circle cx="${xr}" cy="${yb}" r="5" class="rvb-chart-dot rvb-chart-dot-buy" fill="#0f7b6c" stroke="#fff" stroke-width="1.5" pointer-events="none"/>
    </g>`;
  }

  return `
    <figure class="rvb-chart" role="group" aria-label="Interactive chart: hover dots for amounts. Orange dashed line shows break-even year when applicable.">
      <p class="rvb-chart-hint"><span class="rvb-chart-hint-dot rent"></span> Hover any dot for totals at that year.</p>
      <svg viewBox="0 0 ${w} ${h}" class="rvb-chart-svg" preserveAspectRatio="xMidYMid meet">
        <rect x="${padL}" y="${padT}" width="${innerW}" height="${innerH}" fill="#fafcfe" rx="6"/>
        ${gridLines}
        ${yLabels}
        ${breakEvenSvg}
        <polyline fill="none" stroke="#2d6a9f" stroke-width="2.5" points="${rentPts}" class="rvb-chart-line-rent"/>
        <polyline fill="none" stroke="#0f7b6c" stroke-width="2.5" points="${buyPts}" class="rvb-chart-line-buy"/>
        ${dotsSvg}
        ${yearLabels}
      </svg>
      <figcaption class="rvb-chart-caption">
        <span class="rvb-legend rvb-legend-rent"><span class="swatch"></span> Rent (cumulative)</span>
        <span class="rvb-legend rvb-legend-buy"><span class="swatch"></span> Buy (cumulative cash out)</span>
        ${breakEvenYear != null && breakEvenYear > 0 ? '<span class="rvb-legend rvb-legend-be"><span class="swatch swatch-be"></span> Break-even</span>' : ""}
      </figcaption>
    </figure>
  `;
}

const rentBuyForm = document.getElementById("rent-buy-form");
const rentBuyResult = document.getElementById("rent-buy-result");
const rvbRateLowerRate = document.getElementById("rvb-rate-lower-rate");
const rvbRateLowerMonthly = document.getElementById("rvb-rate-lower-monthly");
const rvbRateLowerOutcome = document.getElementById("rvb-rate-lower-outcome");
const rvbRateLowerInsight = document.getElementById("rvb-rate-lower-insight");
const rvbRateHigherRate = document.getElementById("rvb-rate-higher-rate");
const rvbRateHigherMonthly = document.getElementById("rvb-rate-higher-monthly");
const rvbRateHigherOutcome = document.getElementById("rvb-rate-higher-outcome");
const rvbRateHigherInsight = document.getElementById("rvb-rate-higher-insight");
const rvbDownLowerValue = document.getElementById("rvb-down-lower-value");
const rvbDownLowerMonthly = document.getElementById("rvb-down-lower-monthly");
const rvbDownLowerPmi = document.getElementById("rvb-down-lower-pmi");
const rvbDownLowerInsight = document.getElementById("rvb-down-lower-insight");
const rvbDownHigherValue = document.getElementById("rvb-down-higher-value");
const rvbDownHigherMonthly = document.getElementById("rvb-down-higher-monthly");
const rvbDownHigherPmi = document.getElementById("rvb-down-higher-pmi");
const rvbDownHigherInsight = document.getElementById("rvb-down-higher-insight");

function updateStaticDecisionCards(inputs) {
  const baseDownPct = Math.min(100, Math.max(0, inputs.downPct));
  const baseLoan = Math.max(inputs.homePrice * (1 - baseDownPct / 100), 0);

  const lowerRate = Math.max(0, inputs.interestRate - 1);
  const higherRate = Math.max(0, inputs.interestRate + 1);
  const lowerRatePi = monthlyPI(baseLoan, lowerRate, inputs.loanTermYears);
  const higherRatePi = monthlyPI(baseLoan, higherRate, inputs.loanTermYears);
  const lowerRateSim = simulateRentVsBuy({ ...inputs, interestRate: lowerRate }, inputs.yearsStay);
  const higherRateSim = simulateRentVsBuy({ ...inputs, interestRate: higherRate }, inputs.yearsStay);

  if (rvbRateLowerRate) rvbRateLowerRate.textContent = `${lowerRate.toFixed(2).replace(/\.00$/, "")}%`;
  if (rvbRateLowerMonthly) rvbRateLowerMonthly.textContent = `${money(lowerRatePi)}/month`;
  if (rvbRateLowerOutcome) rvbRateLowerOutcome.textContent = lowerRateSim.buyingBetter ? "Buying tends to look stronger" : "Renting can still be competitive";
  if (rvbRateLowerInsight) rvbRateLowerInsight.textContent = "Insight: Lower rates usually reduce monthly pressure and can move break-even earlier.";

  if (rvbRateHigherRate) rvbRateHigherRate.textContent = `${higherRate.toFixed(2).replace(/\.00$/, "")}%`;
  if (rvbRateHigherMonthly) rvbRateHigherMonthly.textContent = `${money(higherRatePi)}/month`;
  if (rvbRateHigherOutcome) rvbRateHigherOutcome.textContent = higherRateSim.buyingBetter ? "Buying can still work, but margin narrows" : "Renting tends to look stronger";
  if (rvbRateHigherInsight) rvbRateHigherInsight.textContent = "Insight: Higher rates often delay break-even, making renting more attractive in the short term.";

  const lowerDownPct = Math.min(100, Math.max(0, baseDownPct - 5));
  const higherDownPct = Math.min(100, Math.max(0, baseDownPct + 5));
  const lowerDownLoan = Math.max(inputs.homePrice * (1 - lowerDownPct / 100), 0);
  const higherDownLoan = Math.max(inputs.homePrice * (1 - higherDownPct / 100), 0);
  const lowerDownPi = monthlyPI(lowerDownLoan, inputs.interestRate, inputs.loanTermYears);
  const higherDownPi = monthlyPI(higherDownLoan, inputs.interestRate, inputs.loanTermYears);

  if (rvbDownLowerValue) rvbDownLowerValue.textContent = `${lowerDownPct.toFixed(1).replace(/\.0$/, "")}%`;
  if (rvbDownLowerMonthly) rvbDownLowerMonthly.textContent = `${money(lowerDownPi)}/month`;
  if (rvbDownLowerPmi) rvbDownLowerPmi.textContent = lowerDownPct < 20 ? "PMI likely added (until ~20% equity)" : "PMI usually not required";
  if (rvbDownLowerInsight) rvbDownLowerInsight.textContent = lowerDownPct < 20
    ? "Insight: Lower down payments increase monthly costs and can reduce buying advantage."
    : "Insight: Even with this lower down payment, PMI may be avoided at or above 20%.";

  if (rvbDownHigherValue) rvbDownHigherValue.textContent = `${higherDownPct.toFixed(1).replace(/\.0$/, "")}%`;
  if (rvbDownHigherMonthly) rvbDownHigherMonthly.textContent = `${money(higherDownPi)}/month`;
  if (rvbDownHigherPmi) rvbDownHigherPmi.textContent = higherDownPct < 20 ? "PMI may still apply" : "PMI usually not required";
  if (rvbDownHigherInsight) rvbDownHigherInsight.textContent = "Insight: Higher down payments usually lower monthly costs and improve buying economics over time.";
}

rentBuyForm?.addEventListener("submit", (event) => {
  event.preventDefault();

  const maintenanceType = document.getElementById("maintenance-type")?.value || "pct";
  const maintenanceVal = Number(document.getElementById("maintenance-value")?.value);

  const inputs = {
    monthlyRent: Number(document.getElementById("monthly-rent")?.value),
    rentIncrease: Number(document.getElementById("rent-increase")?.value),
    renterInsurance: Number(document.getElementById("renter-insurance")?.value),
    homePrice: Number(document.getElementById("home-price")?.value),
    downPct: Number(document.getElementById("down-payment-pct")?.value),
    interestRate: Number(document.getElementById("interest-rate")?.value),
    loanTermYears: Number(document.getElementById("loan-term")?.value),
    propertyTaxPct: Number(document.getElementById("property-tax-pct")?.value),
    maintenanceType,
    maintenanceValue: maintenanceVal,
    yearsStay: Number(document.getElementById("years-stay")?.value),
    appreciation: Number(document.getElementById("appreciation")?.value),
    investmentReturn: Number(document.getElementById("investment-return")?.value)
  };

  const r = computeRentVsBuy(inputs);
  const breakEvenYear = findBreakEvenYear(inputs, inputs.yearsStay);
  const breakEvenEver = findBreakEvenYear(inputs, 40);
  const whatItMeansHtml = buildWhatItMeansHtml(inputs, r, breakEvenEver);
  updateStaticDecisionCards(inputs);

  const verdictMain = r.buyingBetter
    ? `Buying saves you ${money(r.margin)} over ${r.yearsStay} years`
    : `Renting is cheaper by ${money(r.margin)} over ${r.yearsStay} years`;

  const verdictDetail =
    "Net comparison uses rent plus insurance (adjusted for investing your down payment at your assumed return), minus ending home equity from buying.";

  rentBuyResult.innerHTML = `
    <div class="rvb-verdict">
      <p class="rvb-verdict-lead">${verdictMain}</p>
      <p class="rvb-verdict-sub">${verdictDetail}</p>
    </div>
    <h2 class="rvb-prose-h2">Full cost breakdown</h2>
    <div class="rvb-breakdown-grid">
      <div class="rvb-breakdown-col">
        <h3 class="rvb-breakdown-h3">Renting</h3>
        <dl class="rvb-breakdown-dl">
          <dt>Total rent paid</dt>
          <dd>${money(r.totalRentOnly)}</dd>
          <dt>Renter’s insurance (total)</dt>
          <dd>${money(r.totalRenterInsurance)}</dd>
          <dt>Rent increases</dt>
          <dd>${r.rentIncreasePct.toFixed(1)}% per year · from ${money(r.monthlyRentStart)}/mo → ${money(r.monthlyRentEnd)}/mo by year ${r.yearsStay}</dd>
        </dl>
      </div>
      <div class="rvb-breakdown-col">
        <h3 class="rvb-breakdown-h3">Buying</h3>
        <dl class="rvb-breakdown-dl">
          <dt>Mortgage payments (P+I)</dt>
          <dd>${money(r.totalMortgagePayments)}</dd>
          <dt>Interest paid</dt>
          <dd>${money(r.totalInterest)}</dd>
          <dt>Principal paid</dt>
          <dd>${money(r.totalPrincipal)}</dd>
          <dt>Property tax</dt>
          <dd>${money(r.totalPropertyTax)}</dd>
          <dt>Maintenance</dt>
          <dd>${money(r.totalMaintenance)}</dd>
          <dt>Equity built (est.)</dt>
          <dd>${money(r.equityEnd)} <span class="rvb-breakdown-note">(home value minus loan balance after ${r.yearsStay} yrs)</span></dd>
        </dl>
      </div>
    </div>
    ${whatItMeansHtml}
    <p class="note rvb-note">Estimates only. Actual taxes, insurance, maintenance, rent increases, and appreciation vary by market. Not tax or legal advice.</p>
  `;
});

