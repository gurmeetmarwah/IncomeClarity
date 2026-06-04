(function () {
  "use strict";

  const engine = window.IncomeClarityPayoffScenario;
  if (!engine) return;

  const { payoffPlan, formatDuration, fmtUSD, debtFreeDate, DEBT_TYPES } = engine;

  const MIXED_APR = 16;

  function num(id) {
    return Math.max(0, parseFloat(document.getElementById(id)?.value) || 0);
  }

  function monthsDiff(a, b) {
    if (!a.payoffPossible || !b.payoffPossible) return 0;
    return Math.max(0, a.months - b.months);
  }

  function interestDiff(base, better) {
    if (!base.payoffPossible || !better.payoffPossible) return 0;
    return Math.max(0, base.interestPaid - better.interestPaid);
  }

  function formatMonthsSaved(m) {
    if (m <= 0) return "—";
    const y = Math.floor(m / 12);
    const mo = m % 12;
    if (y === 0) return `${mo} month${mo === 1 ? "" : "s"}`;
    if (mo === 0) return `${y} year${y === 1 ? "" : "s"}`;
    return `${y} year${y === 1 ? "" : "s"} ${mo} month${mo === 1 ? "" : "s"}`;
  }

  function readSimulator() {
    const balance = num("podf-balance");
    const apr =
      document.querySelector("[data-podf-debt].is-selected")?.dataset.podfDebt === "mixed"
        ? MIXED_APR
        : num("podf-apr");
    const basePay = num("podf-payment");
    const extra = num("podf-extra-slider") || num("podf-extra");
    return { balance, apr, basePay, extra, totalPay: basePay + extra };
  }

  function applyDebtType(type) {
    document.querySelectorAll("[data-podf-debt]").forEach((btn) => {
      const on = btn.dataset.podfDebt === type;
      btn.classList.toggle("is-selected", on);
      btn.setAttribute("aria-pressed", on ? "true" : "false");
    });
    const hint = document.getElementById("podf-debt-hint");
    if (type === "mixed") {
      if (document.getElementById("podf-apr")) document.getElementById("podf-apr").value = MIXED_APR;
      if (hint) hint.textContent = "Blended rate for multiple debts—adjust APR to match your mix.";
    } else {
      const cfg = DEBT_TYPES[type] || DEBT_TYPES["credit-card"];
      if (document.getElementById("podf-apr")) document.getElementById("podf-apr").value = cfg.apr;
      if (hint) hint.textContent = cfg.hint;
    }
    renderAll();
  }

  function renderQuick() {
    const balance = num("podf-quick-balance");
    const apr = num("podf-quick-apr");
    const pay = num("podf-quick-payment");
    const extra = num("podf-quick-extra");
    const base = payoffPlan(balance, apr, pay, {});
    const boosted = payoffPlan(balance, apr, pay + extra, {});
    const set = (id, text) => {
      const el = document.getElementById(id);
      if (el) el.textContent = text;
    };
    set(
      "podf-quick-current",
      base.payoffPossible ? formatDuration(base.months) : "Will not pay off"
    );
    set(
      "podf-quick-with-extra",
      boosted.payoffPossible ? formatDuration(boosted.months) : "Raise payment"
    );
    set("podf-quick-time-saved", formatMonthsSaved(monthsDiff(base, boosted)));
    set(
      "podf-quick-interest-saved",
      interestDiff(base, boosted) > 0 ? fmtUSD(interestDiff(base, boosted)) : "—"
    );
  }

  function renderSimulator() {
    const { balance, apr, basePay, extra, totalPay } = readSimulator();
    const base = payoffPlan(balance, apr, basePay, {});
    const plan = payoffPlan(balance, apr, totalPay, {});
    const set = (id, text) => {
      const el = document.getElementById(id);
      if (el) el.textContent = text;
    };
    set("podf-result-date", debtFreeDate(plan.months));
    set("podf-result-interest", plan.payoffPossible ? fmtUSD(plan.interestPaid) : "—");
    set(
      "podf-result-saved",
      interestDiff(base, plan) > 0 ? fmtUSD(interestDiff(base, plan)) : "—"
    );
    set("podf-result-months-saved", formatMonthsSaved(monthsDiff(base, plan)));

    const extraOut = document.getElementById("podf-extra-slider-out");
    if (extraOut) extraOut.textContent = fmtUSD(extra) + "/mo";

  }

  function renderExtraCards() {
    const grid = document.getElementById("podf-extra-grid");
    if (!grid) return;
    const { balance, apr, basePay } = readSimulator();
    const base = payoffPlan(balance, apr, basePay, {});
    [25, 50, 100, 200].forEach((amt) => {
      const plan = payoffPlan(balance, apr, basePay + amt, {});
      const card = grid.querySelector(`[data-extra-amt="${amt}"]`);
      if (!card) return;
      const timeEl = card.querySelector("[data-extra-time]");
      const intEl = card.querySelector("[data-extra-interest]");
      if (timeEl) {
        timeEl.textContent = formatMonthsSaved(monthsDiff(base, plan));
      }
      if (intEl) {
        intEl.textContent =
          interestDiff(base, plan) > 0 ? fmtUSD(interestDiff(base, plan)) : "—";
      }
    });
  }

  function simulateMultiCard(cards, total, order) {
    const state = cards.map((c) => ({
      bal: c.bal,
      apr: c.apr,
      min: Math.max(25, c.bal * 0.02),
    }));
    let months = 0;
    let totalPaid = 0;
    const startBal = cards.reduce((s, c) => s + c.bal, 0);
    while (state.some((c) => c.bal > 0.01) && months < 600) {
      months++;
      let spend = 0;
      state.forEach((c) => {
        if (c.bal <= 0) return;
        c.bal += c.bal * (c.apr / 100 / 12);
        const pay = Math.min(c.min, c.bal);
        c.bal -= pay;
        spend += pay;
      });
      let extra = total - spend;
      const ordered =
        order === "avalanche"
          ? [...state].sort((a, b) => b.apr - a.apr)
          : [...state].sort((a, b) => a.bal - b.bal);
      ordered.forEach((c) => {
        if (extra <= 0 || c.bal <= 0) return;
        const take = Math.min(extra, c.bal);
        c.bal -= take;
        extra -= take;
      });
      totalPaid += total - extra;
    }
    const interest = totalPaid - startBal;
    return { months, years: (months / 12).toFixed(1) };
  }

  function renderSnowballAvalanche() {
    const cards = [
      { bal: 4000, apr: 22 },
      { bal: 1100, apr: 18 },
    ];
    const total = 460;
    const snow = simulateMultiCard(cards, total, "snowball");
    const aval = simulateMultiCard(cards, total, "avalanche");
    const set = (id, val) => {
      const el = document.getElementById(id);
      if (el) el.textContent = val;
    };
    set("podf-snowball-years", snow.years + " years");
    set("podf-avalanche-years", aval.years + " years");
    set("podf-table-snow", snow.years + " years");
    set("podf-table-aval", aval.years + " years");
  }

  function renderIncomePct() {
    const income = num("podf-income");
    const { balance, apr, basePay } = readSimulator();
    const onePct = Math.round((income / 12) * 0.01);
    const base = payoffPlan(balance, apr, basePay, {});
    const boosted = payoffPlan(balance, apr, basePay + onePct, {});
    const set = (id, text) => {
      const el = document.getElementById(id);
      if (el) el.textContent = text;
    };
    set("podf-income-pct-pay", fmtUSD(onePct) + "/month");
    set(
      "podf-income-pct-savings",
      interestDiff(base, boosted) > 0 ? fmtUSD(interestDiff(base, boosted)) + "+" : "—"
    );
  }

  function renderAll() {
    renderQuick();
    renderSimulator();
    renderExtraCards();
    renderSnowballAvalanche();
    renderIncomePct();
  }

  document.querySelectorAll("[data-podf-debt]").forEach((btn) => {
    btn.addEventListener("click", () => applyDebtType(btn.dataset.podfDebt));
  });

  [
    "podf-quick-balance",
    "podf-quick-apr",
    "podf-quick-payment",
    "podf-quick-extra",
    "podf-balance",
    "podf-apr",
    "podf-payment",
    "podf-extra",
    "podf-income",
  ].forEach((id) => {
    document.getElementById(id)?.addEventListener("input", renderAll);
  });

  const extraSlider = document.getElementById("podf-extra-slider");
  const extraInput = document.getElementById("podf-extra");
  extraSlider?.addEventListener("input", () => {
    if (extraInput) extraInput.value = extraSlider.value;
    renderAll();
  });
  extraInput?.addEventListener("input", () => {
    if (extraSlider) extraSlider.value = Math.min(500, extraInput.value || 0);
    renderAll();
  });

  document.getElementById("podf-quick-form")?.addEventListener("submit", (e) => {
    e.preventDefault();
    const balance = num("podf-quick-balance");
    const apr = num("podf-quick-apr");
    const pay = num("podf-quick-payment");
    const extra = num("podf-quick-extra");
    document.getElementById("podf-balance").value = balance;
    document.getElementById("podf-apr").value = apr;
    document.getElementById("podf-payment").value = pay;
    document.getElementById("podf-extra").value = extra;
    document.getElementById("podf-extra-slider").value = extra;
    renderAll();
    document.getElementById("podf-simulator")?.scrollIntoView({ behavior: "smooth", block: "start" });
  });

  document.querySelectorAll("[data-scroll-to]").forEach((btn) => {
    btn.addEventListener("click", () => {
      document.getElementById(btn.getAttribute("data-scroll-to"))?.scrollIntoView({
        behavior: "smooth",
        block: "start",
      });
    });
  });

  document.querySelectorAll("[data-extra-amt]").forEach((card) => {
    card.addEventListener("click", () => {
      const amt = Number(card.dataset.extraAmt) || 0;
      const slider = document.getElementById("podf-extra-slider");
      const input = document.getElementById("podf-extra");
      if (slider) slider.value = amt;
      if (input) input.value = amt;
      renderAll();
      document.getElementById("podf-simulator")?.scrollIntoView({ behavior: "smooth", block: "start" });
    });
  });

  applyDebtType("credit-card");
  renderAll();
})();
