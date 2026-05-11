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

/**
 * Replaces the two illustrative scenario cards with the user's inputs (card 1)
 * and the first successful pay-more scenario (card 2), matching existing card markup.
 */
function buildMinimumScenarioCardsHTML(balance, apr, payment, plan, payoffPossible) {
  const payoffDuration = payoffPossible
    ? formatPayoffDuration(plan.months)
    : "Will not pay off at this payment";
  const interestLine = payoffPossible ? fmtUSD(plan.interestPaid) : "Keeps increasing";

  let quote1 =
    "Interest and timeline below reflect your numbers—small payment bumps often shorten payoff sharply.";
  if (!payoffPossible) {
    quote1 =
      "At this payment, finance charges eat the whole payment (or more)—raise the monthly amount or lower APR to make principal move.";
  } else if (plan.interestPaid > balance) {
    quote1 = "You’ll pay more in interest than your original balance at this payment level.";
  }

  const whatIfs = buildWhatIfScenarios(balance, apr, payment).filter((s) => Number.isFinite(s.months));
  const firstLift = whatIfs[0];

  let card2Html;
  if (firstLift) {
    const monthsSaved = payoffPossible && Number.isFinite(plan.months)
      ? plan.months - firstLift.months
      : null;
    const interestSaved =
      payoffPossible && Number.isFinite(plan.interestPaid) && Number.isFinite(firstLift.interestPaid)
        ? plan.interestPaid - firstLift.interestPaid
        : null;
    let quote2 =
      "Same balance and APR—only the monthly payment changes in this comparison.";
    if (monthsSaved !== null && monthsSaved > 0 && interestSaved !== null && interestSaved > 0) {
      quote2 = `You’d finish <strong>${monthsSaved} month${monthsSaved === 1 ? "" : "s"} sooner</strong> and pay <strong>${fmtUSD(interestSaved)}</strong> less in interest.`;
    } else if (!payoffPossible) {
      quote2 = `With <strong>${fmtUSD(firstLift.newPayment)}/month</strong>, payoff becomes possible in <strong>${formatPayoffDuration(firstLift.months)}</strong> under this model.`;
    }

    card2Html = `
      <article class="debt-minimum-card">
        <h3 class="debt-minimum-card-heading">
          <span class="debt-minimum-label">Scenario 2</span>
          <span class="debt-minimum-context">Pay ${fmtUSD(firstLift.increment)} more per month</span>
          <span class="debt-minimum-sum">${fmtUSD(balance)} balance · ${apr}% APR</span>
        </h3>
        <dl class="debt-minimum-stats">
          <div><dt>Monthly payment</dt><dd><strong>${fmtUSD(firstLift.newPayment)}/month</strong></dd></div>
          <div><dt>Time to pay off</dt><dd><strong>${formatPayoffDuration(firstLift.months)}</strong></dd></div>
          <div><dt>Total interest</dt><dd><strong>${fmtUSD(firstLift.interestPaid)}</strong></dd></div>
        </dl>
        <p class="debt-minimum-eq"><span class="debt-minimum-eq-quote">${quote2}</span></p>
      </article>
    `;
  } else {
    card2Html = `
      <article class="debt-minimum-card">
        <h3 class="debt-minimum-card-heading">
          <span class="debt-minimum-label">Scenario 2</span>
          <span class="debt-minimum-context">Pay-more comparison</span>
          <span class="debt-minimum-sum">${fmtUSD(balance)} balance · ${apr}% APR</span>
        </h3>
        <dl class="debt-minimum-stats">
          <div><dt>Note</dt><dd><strong>No +$50 / +$100 / +$200 bump</strong> <span class="debt-minimum-stat-detail">(in this model) produced a payoff path from your inputs.</span></dd></div>
          <div><dt>Try next</dt><dd><strong>Larger payment</strong> or check APR—then recalculate.</dd></div>
        </dl>
        <p class="debt-minimum-eq"><span class="debt-minimum-eq-quote">Use the “What if you paid more?” section below for other payment levels.</span></p>
      </article>
    `;
  }

  const card1Html = `
    <article class="debt-minimum-card">
      <h3 class="debt-minimum-card-heading">
        <span class="debt-minimum-label">Scenario 1</span>
        <span class="debt-minimum-context">Your calculator inputs</span>
        <span class="debt-minimum-sum">${fmtUSD(balance)} balance · ${apr}% APR</span>
      </h3>
      <dl class="debt-minimum-stats">
        <div><dt>Monthly payment</dt><dd><strong>${fmtUSD(payment)}/month</strong> <span class="debt-minimum-stat-detail">(steady payment in this estimate)</span></dd></div>
        <div><dt>Time to pay off</dt><dd><strong>${payoffDuration}</strong></dd></div>
        <div><dt>Total interest</dt><dd><strong>${interestLine}</strong></dd></div>
      </dl>
      <p class="debt-minimum-eq"><span class="debt-minimum-eq-quote">${quote1}</span></p>
    </article>
  `;

  return card1Html + card2Html;
}

const payoffForm = document.getElementById("payoff-form");
const payoffResult = document.getElementById("payoff-result");
const debtMinimumCardsRoot = document.getElementById("debt-minimum-cards-root");

payoffForm?.addEventListener("submit", (event) => {
  event.preventDefault();
  const balance = Number(document.getElementById("balance")?.value);
  const apr = Number(document.getElementById("interest-rate")?.value);
  const payment = Number(document.getElementById("minimum-payment")?.value);

  const plan = payoffPlanWithTimeline(balance, apr, payment);
  const payoffPossible = plan.payoffPossible;

  if (debtMinimumCardsRoot) {
    debtMinimumCardsRoot.innerHTML = buildMinimumScenarioCardsHTML(balance, apr, payment, plan, payoffPossible);
  }

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
      const monthsSaved =
        Number.isFinite(plan.months) && Number.isFinite(scenario.months)
          ? plan.months - scenario.months
          : null;
      const interestSaved =
        payoffPossible && Number.isFinite(plan.interestPaid) && Number.isFinite(scenario.interestPaid)
          ? plan.interestPaid - scenario.interestPaid
          : null;
      const saveLine =
        monthsSaved !== null && monthsSaved > 0
          ? `You save <strong>${monthsSaved} month${monthsSaved === 1 ? "" : "s"}</strong>${
              interestSaved !== null && interestSaved > 0
                ? ` and <strong>${fmtUSD(interestSaved)}</strong> in interest.`
                : "."
            }`
          : "Compared with your baseline payment in this estimate.";
      return `
        <article class="what-if-card">
          <h3>Pay ${fmtUSD(scenario.newPayment)}/month (${fmtUSD(scenario.increment)} more)</h3>
          <p>Debt-free in <strong>${formatPayoffDuration(scenario.months)}</strong></p>
          <p>Interest paid: <strong>${fmtUSD(scenario.interestPaid)}</strong></p>
          <p>${saveLine}</p>
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
    ${notPayingOffWarning}
    ${highInterestWarning}
    ${payoffPossible ? `
      <h3 id="payoff-result-heading" class="debt-timeline-heading">Year-by-year visual timeline</h3>
      <div class="debt-timeline-wrap">
        ${timelineItems}
      </div>
    ` : ""}
    <h2 class="what-if-title">What if you paid more?</h2>
    <div class="what-if-grid">
      ${whatIfHtml}
    </div>
  `;

  payoffResult.focus({ preventScroll: true });
  (debtMinimumCardsRoot ?? payoffResult).scrollIntoView({ behavior: "smooth", block: "start" });
});
