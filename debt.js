function fmtUSD(amount) {
  return new Intl.NumberFormat("en-US", {
    style: "currency",
    currency: "USD",
    maximumFractionDigits: 0
  }).format(amount);
}

function formatPayoffDuration(months) {
  const years = Math.floor(months / 12);
  const remainingMonths = months % 12;
  if (years === 0) {
    return `${remainingMonths} month${remainingMonths === 1 ? "" : "s"}`;
  }
  if (remainingMonths === 0) {
    return `${years} year${years === 1 ? "" : "s"}`;
  }
  return `${years} year${years === 1 ? "" : "s"} ${remainingMonths} month${remainingMonths === 1 ? "" : "s"}`;
}

function payoffPlanWithTimeline(balance, apr, payment) {
  const monthlyRate = apr / 100 / 12;
  let months = 0;
  let interestPaid = 0;
  let remaining = balance;
  let yearlyInterest = 0;
  let yearlyPrincipal = 0;
  const timeline = [];

  while (remaining > 0 && months < 1200) {
    const interest = remaining * monthlyRate;
    const principalPaid = Math.min(payment - interest, remaining);
    if (principalPaid <= 0) {
      return {
        months: Number.POSITIVE_INFINITY,
        interestPaid: Number.POSITIVE_INFINITY,
        timeline,
        payoffPossible: false
      };
    }
    remaining -= principalPaid;
    interestPaid += interest;
    yearlyInterest += interest;
    yearlyPrincipal += principalPaid;
    months += 1;

    if (months % 12 === 0 || remaining <= 0) {
      timeline.push({
        year: timeline.length + 1,
        interestPaid: yearlyInterest,
        principalPaid: yearlyPrincipal,
        endingBalance: Math.max(0, remaining)
      });
      yearlyInterest = 0;
      yearlyPrincipal = 0;
    }
  }

  return {
    months,
    interestPaid,
    timeline,
    payoffPossible: true
  };
}

function buildWhatIfScenarios(balance, apr, payment) {
  const increments = [50, 100, 200];
  return increments
    .map((increment) => {
      const newPayment = payment + increment;
      const scenarioPlan = payoffPlanWithTimeline(balance, apr, newPayment);
      if (!scenarioPlan) {
        return null;
      }
      return {
        increment,
        newPayment,
        months: scenarioPlan.months,
        interestPaid: scenarioPlan.interestPaid
      };
    })
    .filter(Boolean);
}

const payoffForm = document.getElementById("payoff-form");
const payoffResult = document.getElementById("payoff-result");

payoffForm?.addEventListener("submit", (event) => {
  event.preventDefault();
  const balance = Number(document.getElementById("balance")?.value);
  const apr = Number(document.getElementById("interest-rate")?.value);
  const payment = Number(document.getElementById("minimum-payment")?.value);

  const plan = payoffPlanWithTimeline(balance, apr, payment);
  const payoffPossible = plan.payoffPossible;

  const payoffDuration = payoffPossible ? formatPayoffDuration(plan.months) : "It will not be paid off at this payment";
  const highInterestWarning = payoffPossible && plan.interestPaid > balance
    ? '<p class="debt-result-warning">You’ll pay more in interest than your original balance.</p>'
    : "";
  const notPayingOffWarning = !payoffPossible
    ? '<p class="debt-result-warning">At this payment amount, monthly interest is greater than or equal to your payment, so debt will keep growing or stay stuck.</p>'
    : "";
  const whatIfScenarios = buildWhatIfScenarios(balance, apr, payment);
  const whatIfHtml = whatIfScenarios
    .map((scenario) => {
      const monthsSaved = plan.months - scenario.months;
      const interestSaved = payoffPossible ? (plan.interestPaid - scenario.interestPaid) : null;
      return `
        <article class="what-if-card">
          <h3>Pay ${fmtUSD(scenario.newPayment)}/month (${fmtUSD(scenario.increment)} more)</h3>
          <p>Debt-free in <strong>${formatPayoffDuration(scenario.months)}</strong></p>
          <p>Interest paid: <strong>${fmtUSD(scenario.interestPaid)}</strong></p>
          <p>You save <strong>${monthsSaved} months</strong>${interestSaved !== null ? ` and <strong>${fmtUSD(interestSaved)}</strong> in interest.` : " compared with your current payment level."}</p>
        </article>
      `;
    })
    .join("");
  const maxYearlyPayment = Math.max(
    ...plan.timeline.map((row) => row.principalPaid + row.interestPaid),
    1
  );
  const maxEndingBalance = Math.max(...plan.timeline.map((row) => row.endingBalance), 1);

  const timelineItems = plan.timeline
    .map((row) => {
      const yearlyTotalPaid = row.principalPaid + row.interestPaid;
      const paidWidth = (yearlyTotalPaid / maxYearlyPayment) * 100;
      const interestShare = yearlyTotalPaid > 0 ? (row.interestPaid / yearlyTotalPaid) * 100 : 0;
      const principalShare = 100 - interestShare;
      const balanceWidth = (row.endingBalance / maxEndingBalance) * 100;
      return `
        <article class="debt-timeline-item">
          <div class="debt-timeline-head">
            <strong>Year ${row.year}</strong>
            <span>Ending balance: ${fmtUSD(row.endingBalance)}</span>
          </div>
          <div class="debt-timeline-metrics">
            <span>Principal: ${fmtUSD(row.principalPaid)}</span>
            <span>Interest: ${fmtUSD(row.interestPaid)}</span>
            <span>Total paid: ${fmtUSD(yearlyTotalPaid)}</span>
          </div>
          <div class="debt-timeline-bar" aria-hidden="true">
            <div class="debt-timeline-bar-fill" style="width:${Math.max(paidWidth, 6).toFixed(1)}%">
              <span class="debt-principal-fill" style="width:${Math.max(principalShare, 2).toFixed(1)}%"></span>
              <span class="debt-interest-fill" style="width:${Math.max(interestShare, 2).toFixed(1)}%"></span>
            </div>
          </div>
          <div class="debt-timeline-balance" aria-hidden="true">
            <span style="width:${Math.max(balanceWidth, row.endingBalance > 0 ? 4 : 0).toFixed(1)}%"></span>
          </div>
        </article>
      `;
    })
    .join("");

  payoffResult.innerHTML = `
    <div class="debt-result-hero">
      <h3>Debt payoff result</h3>
      ${notPayingOffWarning}
      ${highInterestWarning}
      <div class="debt-result-kpis">
        <article class="debt-result-kpi">
          <span>Monthly installment in this estimate</span>
          <strong>${fmtUSD(payment)}</strong>
        </article>
        <article class="debt-result-kpi">
          <span>You’ll be in debt for</span>
          <strong>${payoffDuration}</strong>
        </article>
        <article class="debt-result-kpi interest-kpi">
          <span>You’ll pay in interest</span>
          <strong>${payoffPossible ? fmtUSD(plan.interestPaid) : "Keeps increasing"}</strong>
        </article>
      </div>
    </div>
    ${payoffPossible ? `
      <h3>Year-by-year visual timeline</h3>
      <div class="debt-timeline-wrap">
        ${timelineItems}
      </div>
    ` : ""}
    <h2 class="what-if-title">What if you paid more?</h2>
    <div class="what-if-grid">
      ${whatIfHtml}
    </div>
  `;
});
