(function () {
  const DEBT_TYPES = {
    "credit-card": { label: "Credit Card", apr: 22, hint: "Revolving APR—paying more than the minimum usually saves years of interest." },
    "personal-loan": { label: "Personal Loan", apr: 14, hint: "Fixed installment loans often have lower APR than cards but still reward extra payments." },
    medical: { label: "Medical Debt", apr: 8, hint: "Some medical balances are low- or no-interest—confirm your actual rate." },
    auto: { label: "Auto Loan", apr: 7, hint: "Auto loans amortize on a schedule; extra payments cut total interest." },
    student: { label: "Student Loan", apr: 6, hint: "Federal and private rates vary widely—use your servicer’s rate." },
  };

  const STRATEGIES = {
    minimum: { label: "Minimum payments", multiplier: 0.02, floor: 25 },
    aggressive: { label: "Aggressive payoff", extraSuggest: 100 },
    avalanche: { label: "Debt avalanche", note: "On multiple debts, attack the highest APR first while paying minimums elsewhere." },
    snowball: { label: "Debt snowball", note: "On multiple debts, clear the smallest balance first for momentum." },
  };

  function fmtUSD(n) {
    return new Intl.NumberFormat("en-US", { style: "currency", currency: "USD", maximumFractionDigits: 0 }).format(n);
  }

  function formatDuration(months) {
    if (!Number.isFinite(months) || months === Infinity) return "Will not pay off";
    const y = Math.floor(months / 12);
    const m = months % 12;
    if (y === 0) return `${m} month${m === 1 ? "" : "s"}`;
    if (m === 0) return `${y} year${y === 1 ? "" : "s"}`;
    return `${y} year${y === 1 ? "" : "s"} ${m} month${m === 1 ? "" : "s"}`;
  }

  function debtFreeDate(months) {
    if (!Number.isFinite(months) || months === Infinity) return "—";
    const d = new Date();
    d.setMonth(d.getMonth() + months);
    return d.toLocaleDateString("en-US", { month: "long", year: "numeric" });
  }

  function payoffPlan(balance, apr, payment, opts) {
    const lump = (opts && opts.lumpSum) || 0;
    const monthlyRate = apr / 100 / 12;
    let remaining = Math.max(0, balance - lump);
    let months = 0;
    let interestPaid = 0;
    const monthlyBalances = [remaining];

    if (remaining <= 0) {
      return { months: 0, interestPaid: 0, payoffPossible: true, monthlyBalances: [0] };
    }

    while (remaining > 0.01 && months < 1200) {
      const interest = remaining * monthlyRate;
      const principal = Math.min(payment - interest, remaining);
      if (principal <= 0) {
        return {
          months: Infinity,
          interestPaid: Infinity,
          payoffPossible: false,
          monthlyBalances,
        };
      }
      remaining -= principal;
      interestPaid += interest;
      months += 1;
      monthlyBalances.push(Math.max(0, remaining));
    }

    return { months, interestPaid, payoffPossible: true, monthlyBalances };
  }

  function minimumPayment(balance, apr) {
    const pct = Math.max(balance * 0.02, 25);
    const interest = (balance * (apr / 100)) / 12;
    return Math.max(pct, interest + 10);
  }

  const els = {
    balance: document.getElementById("sc5-balance"),
    apr: document.getElementById("sc5-apr"),
    aprRange: document.getElementById("sc5-apr-range"),
    payment: document.getElementById("sc5-payment"),
    paymentRange: document.getElementById("sc5-payment-range"),
    extra: document.getElementById("sc5-extra"),
    lump: document.getElementById("sc5-lump"),
    strategy: document.getElementById("sc5-strategy"),
    debtTypeCards: document.querySelectorAll("[data-debt-type]"),
    quickBalance: document.getElementById("sc5-quick-balance"),
    quickApr: document.getElementById("sc5-quick-apr"),
    quickPayment: document.getElementById("sc5-quick-payment"),
    quickForm: document.getElementById("sc5-quick-form"),
    heroPreview: document.getElementById("sc5-hero-preview"),
    results: {
      duration: document.getElementById("sc5-result-duration"),
      interest: document.getElementById("sc5-result-interest"),
      saved: document.getElementById("sc5-result-saved"),
      date: document.getElementById("sc5-result-date"),
      warning: document.getElementById("sc5-result-warning"),
    },
    quickResults: document.getElementById("sc5-quick-results"),
    timelineBar: document.getElementById("sc5-timeline-bar"),
    timelineChart: document.getElementById("sc5-balance-chart"),
    whatIfGrid: document.getElementById("sc5-what-if-grid"),
    paymentTable: document.getElementById("sc5-payment-table-body"),
    budgetImpact: document.getElementById("sc5-budget-impact"),
    realisticGrid: document.getElementById("sc5-realistic-grid"),
  };

  let baselinePlan = null;
  let selectedDebtType = "credit-card";

  function readInputs() {
    const balance = Number(els.balance?.value) || 5000;
    const apr = Number(els.apr?.value) || 22;
    const payment =
      (Number(els.payment?.value) || 200) + (Number(els.extra?.value) || 0);
    const lump = Number(els.lump?.value) || 0;
    return { balance, apr, payment, lump };
  }

  function syncSliders() {
    if (els.aprRange && els.apr) {
      els.aprRange.value = els.apr.value;
    }
    if (els.paymentRange && els.payment) {
      els.paymentRange.value = els.payment.value;
    }
  }

  function updatePreview(plan, inputs) {
    if (!els.heroPreview) return;
    els.heroPreview.querySelector("[data-preview-balance]").textContent = fmtUSD(inputs.balance);
    els.heroPreview.querySelector("[data-preview-payment]").textContent = fmtUSD(inputs.payment);
    els.heroPreview.querySelector("[data-preview-time]").textContent = plan.payoffPossible
      ? formatDuration(plan.months)
      : "Increase payment";
  }

  function renderTimeline(plan, inputs) {
    if (!els.timelineBar || !plan.payoffPossible) {
      if (els.timelineBar) els.timelineBar.innerHTML = "";
      return;
    }
    const total = plan.months;
    const markers = [0, Math.floor(total / 4), Math.floor(total / 2), Math.floor((3 * total) / 4), total];
    els.timelineBar.innerHTML = `
      <div class="sc5-timeline-track" role="img" aria-label="Payoff progress from month 1 to month ${total}">
        <span class="sc5-timeline-start">Month 1</span>
        <span class="sc5-timeline-fill" style="width:100%"></span>
        <span class="sc5-timeline-end">Month ${total}</span>
      </div>
      <p class="sc5-timeline-caption">Estimated debt-free in <strong>${formatDuration(total)}</strong> at ${fmtUSD(inputs.payment)}/month.</p>
    `;

    if (els.timelineChart && plan.monthlyBalances.length > 1) {
      const max = plan.monthlyBalances[0] || 1;
      const points = plan.monthlyBalances
        .filter((_, i) => i % Math.max(1, Math.floor(plan.monthlyBalances.length / 24)) === 0 || i === plan.monthlyBalances.length - 1)
        .map((bal, i, arr) => {
          const x = (i / (arr.length - 1 || 1)) * 100;
          const y = 100 - (bal / max) * 100;
          return `${x},${y}`;
        })
        .join(" ");
      els.timelineChart.innerHTML = `
        <svg viewBox="0 0 100 40" preserveAspectRatio="none" class="sc5-chart-svg" aria-hidden="true">
          <polyline points="${points}" fill="none" stroke="currentColor" stroke-width="2"/>
        </svg>
        <div class="sc5-chart-labels"><span>${fmtUSD(max)}</span><span>$0</span></div>
      `;
    }
  }

  function renderWhatIf(inputs) {
    if (!els.whatIfGrid) return;
    const base = payoffPlan(inputs.balance, inputs.apr, inputs.payment - (Number(els.extra?.value) || 0), {
      lumpSum: inputs.lump,
    });
    const cards = [
      { title: "Pay $50 more", payment: inputs.payment - (Number(els.extra?.value) || 0) + 50 },
      { title: "Pay $100 more", payment: inputs.payment - (Number(els.extra?.value) || 0) + 100 },
      { title: "Lump sum $1,000", payment: inputs.payment - (Number(els.extra?.value) || 0), lump: 1000 },
    ];

    els.whatIfGrid.innerHTML = cards
      .map((c) => {
        const plan = payoffPlan(inputs.balance, inputs.apr, c.payment, { lumpSum: c.lump || inputs.lump });
        let benefit = "Compare with your baseline.";
        if (base.payoffPossible && plan.payoffPossible) {
          const monthsSaved = base.months - plan.months;
          const interestSaved = base.interestPaid - plan.interestPaid;
          if (monthsSaved > 0) {
            benefit = `Save <strong>${monthsSaved} month${monthsSaved === 1 ? "" : "s"}</strong>`;
            if (interestSaved > 0) benefit += ` · ${fmtUSD(interestSaved)} less interest`;
          } else if (interestSaved > 0) {
            benefit = `Save <strong>${fmtUSD(interestSaved)}</strong> in interest`;
          }
        }
        return `
          <article class="sc5-what-if-card">
            <h3>${c.title}</h3>
            <p class="sc5-what-if-stat">${plan.payoffPossible ? formatDuration(plan.months) : "Not enough"}</p>
            <p class="sc5-what-if-benefit">${benefit}</p>
          </article>
        `;
      })
      .join("");
  }

  function renderPaymentTable(balance, apr) {
    if (!els.paymentTable) return;
    const payments = [100, 150, 200, 250, 300, 500];
    els.paymentTable.innerHTML = payments
      .map((p) => {
        const plan = payoffPlan(balance, apr, p, {});
        return `
          <tr>
            <th scope="row">${fmtUSD(p)}</th>
            <td>${plan.payoffPossible ? formatDuration(plan.months) : "—"}</td>
            <td>${plan.payoffPossible ? fmtUSD(plan.interestPaid) : "—"}</td>
          </tr>
        `;
      })
      .join("");
  }

  function renderRealistic(balance, apr) {
    if (!els.realisticGrid) return;
    const levels = [
      { key: "comfortable", label: "Comfortable", pct: 0.025, floor: 100 },
      { key: "moderate", label: "Moderate", pct: 0.04, floor: 175 },
      { key: "aggressive", label: "Aggressive", pct: 0.07, floor: 300 },
    ];
    els.realisticGrid.innerHTML = levels
      .map((lv) => {
        const pay = Math.max(balance * lv.pct, lv.floor);
        const plan = payoffPlan(balance, apr, pay, {});
        return `
          <article class="sc5-realistic-card sc5-realistic-card--${lv.key}">
            <h3>${lv.label}</h3>
            <p class="sc5-realistic-payment">${fmtUSD(pay)}/mo</p>
            <p>${plan.payoffPossible ? formatDuration(plan.months) : "Raise payment"}</p>
            <p class="sc5-realistic-interest">${plan.payoffPossible ? fmtUSD(plan.interestPaid) + " interest" : ""}</p>
          </article>
        `;
      })
      .join("");
  }

  function renderBudgetImpact(inputs) {
    if (!els.budgetImpact) return;
    const basePay = inputs.payment - (Number(els.extra?.value) || 0);
    const boosted = basePay + 75;
    const base = payoffPlan(inputs.balance, inputs.apr, basePay, { lumpSum: inputs.lump });
    const better = payoffPlan(inputs.balance, inputs.apr, boosted, { lumpSum: inputs.lump });
    if (base.payoffPossible && better.payoffPossible) {
      const monthsSaved = base.months - better.months;
      els.budgetImpact.innerHTML = `
        Paying an additional <strong>$75/month</strong> (${fmtUSD(boosted)} total) could help you become debt-free
        <strong>${monthsSaved} month${monthsSaved === 1 ? "" : "s"} earlier</strong> and save about
        <strong>${fmtUSD(Math.max(0, base.interestPaid - better.interestPaid))}</strong> in interest versus ${fmtUSD(basePay)}/month on this model.
      `;
    } else {
      els.budgetImpact.textContent =
        "Try a higher monthly payment in the planner—small increases often move the payoff date meaningfully.";
    }
  }

  function renderResults() {
    const inputs = readInputs();
    syncSliders();
    const plan = payoffPlan(inputs.balance, inputs.apr, inputs.payment, { lumpSum: inputs.lump });
    const baseNoExtra = payoffPlan(inputs.balance, inputs.apr, Number(els.payment?.value) || 200, {
      lumpSum: inputs.lump,
    });
    baselinePlan = plan;

    if (els.results.duration) {
      els.results.duration.textContent = plan.payoffPossible ? formatDuration(plan.months) : "Will not pay off";
    }
    if (els.results.interest) {
      els.results.interest.textContent = plan.payoffPossible ? fmtUSD(plan.interestPaid) : "—";
    }
    if (els.results.date) {
      els.results.date.textContent = debtFreeDate(plan.months);
    }
    if (els.results.saved) {
      let saved = 0;
      if (baseNoExtra.payoffPossible && plan.payoffPossible) {
        saved = baseNoExtra.interestPaid - plan.interestPaid;
      }
      els.results.saved.textContent = saved > 0 ? fmtUSD(saved) : "—";
    }
    if (els.results.warning) {
      els.results.warning.hidden = plan.payoffPossible;
      if (!plan.payoffPossible) {
        els.results.warning.textContent =
          "At this payment, monthly interest meets or exceeds your payment. Increase the monthly amount or lower APR.";
      }
    }

    updatePreview(plan, inputs);
    renderTimeline(plan, inputs);
    renderWhatIf(inputs);
    renderPaymentTable(inputs.balance, inputs.apr);
    renderRealistic(inputs.balance, inputs.apr);
    renderBudgetImpact(inputs);
  }

  function applyDebtType(type) {
    selectedDebtType = type;
    const cfg = DEBT_TYPES[type] || DEBT_TYPES["credit-card"];
    els.debtTypeCards?.forEach((card) => {
      card.classList.toggle("is-selected", card.dataset.debtType === type);
      card.setAttribute("aria-pressed", card.dataset.debtType === type ? "true" : "false");
    });
    if (els.apr) els.apr.value = cfg.apr;
    const hint = document.getElementById("sc5-debt-type-hint");
    if (hint) hint.textContent = cfg.hint;
    renderResults();
  }

  els.debtTypeCards?.forEach((card) => {
    card.addEventListener("click", () => applyDebtType(card.dataset.debtType));
  });

  [els.balance, els.apr, els.payment, els.extra, els.lump].forEach((input) => {
    input?.addEventListener("input", renderResults);
  });

  els.aprRange?.addEventListener("input", () => {
    if (els.apr) els.apr.value = els.aprRange.value;
    renderResults();
  });

  els.paymentRange?.addEventListener("input", () => {
    if (els.payment) els.payment.value = els.paymentRange.value;
    renderResults();
  });

  els.quickForm?.addEventListener("submit", (e) => {
    e.preventDefault();
    const balance = Number(els.quickBalance?.value) || 5000;
    const apr = Number(els.quickApr?.value) || 22;
    const payment = Number(els.quickPayment?.value) || 200;
    if (els.balance) els.balance.value = balance;
    if (els.apr) els.apr.value = apr;
    if (els.payment) els.payment.value = payment;
    const plan = payoffPlan(balance, apr, payment, {});
    if (els.quickResults) {
      els.quickResults.hidden = false;
      els.quickResults.innerHTML = `
        <p class="sc5-quick-result-main"><strong>${plan.payoffPossible ? formatDuration(plan.months) : "Will not pay off"}</strong></p>
        <p>Estimated interest paid: <strong>${plan.payoffPossible ? fmtUSD(plan.interestPaid) : "—"}</strong></p>
      `;
    }
    renderResults();
    document.getElementById("sc5-planner")?.scrollIntoView({ behavior: "smooth", block: "start" });
  });

  document.querySelectorAll("[data-scroll-to]").forEach((btn) => {
    btn.addEventListener("click", () => {
      const id = btn.getAttribute("data-scroll-to");
      document.getElementById(id)?.scrollIntoView({ behavior: "smooth", block: "start" });
    });
  });

  applyDebtType("credit-card");
  if (els.balance) els.balance.value = 5000;
  if (els.payment) els.payment.value = 200;
  if (els.extra) els.extra.value = 0;
  if (els.lump) els.lump.value = 0;
  renderResults();
})();
