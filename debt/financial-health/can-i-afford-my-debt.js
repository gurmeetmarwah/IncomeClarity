(function () {
  "use strict";

  const fmt = (n) =>
    new Intl.NumberFormat("en-US", {
      style: "currency",
      currency: "USD",
      maximumFractionDigits: 0,
    }).format(n);

  const pct = (n) => (n * 100).toFixed(1) + "%";

  const NECESSITY_SHARE = { 1: 0.35, 2: 0.3, 3: 0.28, 4: 0.32, 5: 0.34 };
  const COL_MULT = { average: 1, low: 0.92, high: 1.12 };

  const BENCHMARKS = {
    1: { label: "Single adult", avg: 0.14, top: 0.08 },
    2: { label: "Couple", avg: 0.16, top: 0.09 },
    3: { label: "Family of 3", avg: 0.18, top: 0.1 },
    4: { label: "Family of 4", avg: 0.19, top: 0.08 },
    5: { label: "Family of 5+", avg: 0.21, top: 0.09 },
  };

  function num(id) {
    return Math.max(0, parseFloat(document.getElementById(id).value) || 0);
  }

  function scoreDebtRatio(r) {
    if (r < 0.15) return 100;
    if (r < 0.25) return 82;
    if (r < 0.35) return 62;
    if (r < 0.45) return 42;
    return 18;
  }

  function scoreHousingDebt(r) {
    if (r < 0.4) return 100;
    if (r < 0.5) return 76;
    if (r < 0.6) return 52;
    return 24;
  }

  function scoreEmergency(months) {
    if (months >= 6) return 100;
    if (months >= 3) return 78;
    if (months >= 1) return 48;
    return 15;
  }

  function scoreFlex(flexRatio) {
    if (flexRatio >= 0.25) return 100;
    if (flexRatio >= 0.15) return 76;
    if (flexRatio >= 0.05) return 50;
    if (flexRatio >= 0) return 28;
    return 8;
  }

  function scoreDti(dti) {
    if (dti < 0.2) return 100;
    if (dti < 0.36) return 78;
    if (dti < 0.5) return 48;
    return 18;
  }

  function band(score) {
    if (score >= 80)
      return {
        emoji: "🟢",
        label: "Healthy Debt Load",
        cls: "dafd-score--healthy",
      };
    if (score >= 60)
      return {
        emoji: "🟡",
        label: "Manageable but Watch Closely",
        cls: "dafd-score--watch",
      };
    return {
      emoji: "🔴",
      label: "Financial Stress Risk",
      cls: "dafd-score--risk",
    };
  }

  function categoryBand(ratio, healthy, watch) {
    if (ratio < healthy) return { label: "Healthy", cls: "pos" };
    if (ratio < watch) return { label: "Watch", cls: "warn" };
    return { label: "Risk", cls: "neg" };
  }

  function readInputs(extraDebt, incomeMult) {
    const annual = num("dafd-annual-income");
    const takeHome = num("dafd-take-home") * incomeMult;
    const housing = num("dafd-housing");
    const savings = num("dafd-savings");
    const family = parseInt(document.getElementById("dafd-family").value, 10) || 1;
    const col = document.getElementById("dafd-location").value || "average";

    const cards = num("dafd-debt-cards");
    const personal = num("dafd-debt-personal");
    const auto = num("dafd-debt-auto");
    const student = num("dafd-debt-student");
    const bnpl = num("dafd-debt-bnpl");
    const totalDebt = cards + personal + auto + student + bnpl + extraDebt;

    const grossMonthly = annual / 12 || takeHome / 0.72;
    const necessityShare = (NECESSITY_SHARE[family] || 0.32) * (COL_MULT[col] || 1);
    const necessities = takeHome * necessityShare;
    const flexibility = takeHome - housing - totalDebt - necessities;
    const debtRatio = takeHome > 0 ? totalDebt / takeHome : 1;
    const housingDebtRatio = takeHome > 0 ? (housing + totalDebt) / takeHome : 1;
    const dti = grossMonthly > 0 ? totalDebt / grossMonthly : 1;
    const burn = necessities + housing + totalDebt;
    const emergencyMonths = burn > 0 ? savings / burn : 0;

    const scores = {
      debt: scoreDebtRatio(debtRatio),
      housing: scoreHousingDebt(housingDebtRatio),
      emergency: scoreEmergency(emergencyMonths),
      flex: scoreFlex(takeHome > 0 ? flexibility / takeHome : 0),
      dti: scoreDti(dti),
    };
    const overall = Math.round(
      scores.debt * 0.28 +
        scores.housing * 0.22 +
        scores.emergency * 0.18 +
        scores.flex * 0.17 +
        scores.dti * 0.15
    );

    return {
      takeHome,
      housing,
      totalDebt,
      cards,
      personal,
      auto,
      student,
      bnpl,
      necessities,
      flexibility,
      debtRatio,
      housingDebtRatio,
      dti,
      emergencyMonths,
      family,
      overall,
      scores,
      grossMonthly,
    };
  }

  function renderBar(data) {
    const total = Math.max(data.takeHome, 1);
    const segments = [
      { key: "housing", val: data.housing, cls: "dafd-bar__seg--housing", label: "Housing" },
      { key: "debt", val: data.totalDebt, cls: "dafd-bar__seg--debt", label: "Debt" },
      { key: "need", val: data.necessities, cls: "dafd-bar__seg--need", label: "Necessities" },
      {
        key: "flex",
        val: Math.max(0, data.flexibility),
        cls: "dafd-bar__seg--flex",
        label: "Money left",
      },
    ];
    const bar = document.getElementById("dafd-income-bar");
    bar.innerHTML = segments
      .map(
        (s) =>
          `<span class="dafd-bar__seg ${s.cls}" style="width:${Math.min(100, (s.val / total) * 100).toFixed(1)}%" title="${s.label}: ${fmt(s.val)}"></span>`
      )
      .join("");
    document.getElementById("dafd-breath-takehome").textContent = fmt(data.takeHome);
    document.getElementById("dafd-breath-housing").textContent = fmt(data.housing);
    document.getElementById("dafd-breath-debt").textContent = fmt(data.totalDebt);
    document.getElementById("dafd-breath-need").textContent = fmt(data.necessities);
    document.getElementById("dafd-breath-flex").textContent = fmt(data.flexibility);
  }

  function renderSummary(data) {
    const b = band(data.overall);
    const scoreEl = document.getElementById("dafd-score-card");
    scoreEl.className = "dafd-score-card " + b.cls;
    document.getElementById("dafd-score-num").textContent = data.overall;
    document.getElementById("dafd-score-emoji").textContent = b.emoji;
    document.getElementById("dafd-score-label").textContent = b.label;

    const flexLabel =
      data.flexibility >= 800
        ? "strong"
        : data.flexibility >= 400
          ? "moderate"
          : data.flexibility >= 0
            ? "tight"
            : "negative";
    document.getElementById("dafd-summary-list").innerHTML = `
      <li>Debt payments consume <strong>${pct(data.debtRatio)}</strong> of take-home pay</li>
      <li>Emergency fund covers <strong>${data.emergencyMonths.toFixed(1)} months</strong> of core bills</li>
      <li>Housing and debt consume <strong>${pct(data.housingDebtRatio)}</strong> of take-home pay</li>
      <li>You have <strong>${flexLabel}</strong> financial flexibility (${fmt(data.flexibility)}/mo left)</li>`;

    document.getElementById("dafd-health-debt").textContent = data.scores.debt;
    document.getElementById("dafd-health-savings").textContent = data.scores.emergency;
    document.getElementById("dafd-health-cash").textContent = data.scores.flex;
    document.getElementById("dafd-health-emergency").textContent = Math.min(
      100,
      Math.round(data.emergencyMonths * 16.67)
    );
    document.getElementById("dafd-health-housing").textContent = data.scores.housing;
    document.getElementById("dafd-health-overall").textContent = data.overall;

    const bench = BENCHMARKS[data.family] || BENCHMARKS[1];
    document.getElementById("dafd-benchmark-body").innerHTML = `
      <tr><th scope="row">${bench.label}</th><td>${pct(data.debtRatio)}</td><td>${pct(bench.avg)}</td><td>${pct(bench.top)}</td></tr>`;

    const th = data.takeHome * 0.1;
    const outcomes = [
      ["Can comfortably save for retirement", data.overall >= 72 && data.flexibility > th],
      ["Can build emergency fund", data.emergencyMonths >= 2 || data.flexibility > 400],
      ["Can afford modest vacation", data.flexibility > 600 && data.debtRatio < 0.28],
      ["Can handle $1,000 emergency", num("dafd-savings") >= 1000],
      ["Can afford home purchase", data.dti < 0.36 && data.housingDebtRatio < 0.43],
      ["May struggle with job loss", data.emergencyMonths < 2 || data.debtRatio > 0.35],
    ];
    document.getElementById("dafd-outcomes").innerHTML = outcomes
      .map(
        ([text, ok]) =>
          `<li class="${ok ? "dafd-outcome--yes" : "dafd-outcome--no"}"><span aria-hidden="true">${ok ? "✓" : "✗"}</span> ${text}</li>`
      )
      .join("");

    const cardBand = categoryBand(
      data.takeHome > 0 ? data.cards / data.takeHome : 0,
      0.1,
      0.2
    );
    const autoBand = categoryBand(
      data.takeHome > 0 ? data.auto / data.takeHome : 0,
      0.1,
      0.15
    );
    document.getElementById("dafd-acc-cards-status").textContent = cardBand.label;
    document.getElementById("dafd-acc-cards-status").className = "dafd-acc-status " + cardBand.cls;
    document.getElementById("dafd-acc-auto-status").textContent = autoBand.label;
    document.getElementById("dafd-acc-auto-status").className = "dafd-acc-status " + autoBand.cls;
    document.getElementById("dafd-acc-student-note").textContent =
      data.student > 0
        ? `Your student loan payment is ${fmt(data.student)}/mo (${pct(data.takeHome > 0 ? data.student / data.takeHome : 0)} of take-home). US median is about 6–9% for borrowers with payments.`
        : "No student loan payment entered.";
    document.getElementById("dafd-acc-personal-note").textContent =
      data.personal > 0
        ? `Personal loans add ${fmt(data.personal)}/mo — often fixed, but they reduce cash for savings and shocks.`
        : "No personal loan payment entered.";

    renderActionPlan(data.overall);
    renderBar(data);
  }

  function renderActionPlan(score) {
    const el = document.getElementById("dafd-action-plan");
    if (score >= 80) {
      el.innerHTML = `<h3>If debt is healthy</h3><ul><li>Maintain current payment trajectory</li><li>Increase investing once employer match is captured</li><li>Build additional savings beyond 3–6 months</li><li>Avoid new high-APR balances</li></ul>`;
    } else if (score >= 60) {
      el.innerHTML = `<h3>If debt is moderate</h3><ul><li>Focus on highest-interest balances first (<a href="/debt/payoff/best-way-to-pay-off-credit-card-debt">avalanche vs snowball</a>)</li><li>Avoid new debt until ratios improve</li><li>Increase emergency fund toward 3 months</li><li>Review housing share with our <a href="/living/housing/how-much-rent-can-i-afford">rent affordability guide</a></li></ul>`;
    } else {
      el.innerHTML = `<h3>If debt is high risk</h3><ul><li>Run a <a href="/credit-card-payoff-calculator#payoff">payoff timeline</a> with extra payments</li><li>Consider <a href="/debt/payoff/best-way-to-pay-off-credit-card-debt">debt avalanche or snowball</a> strategy</li><li>Look at refinancing only if APR drops materially</li><li>Do a full <a href="/living/budgeting/average-monthly-expenses">budget review</a> — cut subscriptions and pause new BNPL</li></ul>`;
    }
  }

  function renderWhatIf() {
    const extra = parseInt(document.getElementById("dafd-scenario-extra").value, 10) || 0;
    const incomeBoost = parseInt(document.getElementById("dafd-scenario-income").value, 10) || 0;
    const rateDrop = parseInt(document.getElementById("dafd-scenario-rate").value, 10) || 0;
    const incomeMult = 1 + incomeBoost / 100;
    const cardRelief = num("dafd-debt-cards") * (rateDrop / 100) * 0.15;
    const adjExtra = extra - cardRelief;
    const base = readInputs(0, 1);
    const scenario = readInputs(Math.max(0, adjExtra), incomeMult);
    document.getElementById("dafd-scenario-extra-label").textContent = fmt(extra);
    document.getElementById("dafd-scenario-income-label").textContent = incomeBoost + "%";
    document.getElementById("dafd-scenario-rate-label").textContent = rateDrop + "%";
    document.getElementById("dafd-scenario-out").innerHTML = `
      <p><strong>Extra $${extra}/mo toward debt:</strong> Flexibility ${fmt(base.flexibility)} → ${fmt(scenario.flexibility)} · Score ${base.overall} → ${scenario.overall}</p>
      <p><strong>Income +${incomeBoost}%:</strong> Take-home ${fmt(base.takeHome)} → ${fmt(scenario.takeHome)} · Debt ratio ${pct(base.debtRatio)} → ${pct(scenario.debtRatio)}</p>
      <p><strong>Card rates −${rateDrop}%:</strong> Estimated payment relief ~${fmt(cardRelief)}/mo (illustrative).</p>`;
  }

  function analyze() {
    const data = readInputs(0, 1);
    renderSummary(data);
    document.getElementById("dafd-results").hidden = false;
    document.getElementById("dafd-results").scrollIntoView({ behavior: "smooth", block: "start" });
    renderWhatIf();
  }

  document.getElementById("dafd-form").addEventListener("submit", (e) => {
    e.preventDefault();
    analyze();
  });
  document.getElementById("dafd-analyze-btn").addEventListener("click", analyze);
  ["dafd-scenario-extra", "dafd-scenario-income", "dafd-scenario-rate"].forEach((id) => {
    document.getElementById(id).addEventListener("input", () => {
      if (!document.getElementById("dafd-results").hidden) renderWhatIf();
    });
  });
})();
