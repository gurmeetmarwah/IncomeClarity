(function () {
  const CITIES = {
    dallas: { name: "Dallas, TX", state: "Texas", col: 1, rent3br: 2100, mortgage3br: 2450, utilities: 380, daycare: 1100, transit: 750 },
    austin: { name: "Austin, TX", state: "Texas", col: 1.14, rent3br: 2450, mortgage3br: 2800, utilities: 400, daycare: 1250, transit: 780 },
    phoenix: { name: "Phoenix, AZ", state: "Arizona", col: 1.02, rent3br: 2050, mortgage3br: 2350, utilities: 420, daycare: 1050, transit: 720 },
    tampa: { name: "Tampa, FL", state: "Florida", col: 1.04, rent3br: 2200, mortgage3br: 2550, utilities: 360, daycare: 1150, transit: 740 },
    atlanta: { name: "Atlanta, GA", state: "Georgia", col: 1.06, rent3br: 2150, mortgage3br: 2500, utilities: 370, daycare: 1200, transit: 760 },
    denver: { name: "Denver, CO", state: "Colorado", col: 1.18, rent3br: 2650, mortgage3br: 3050, utilities: 390, daycare: 1400, transit: 820 },
    seattle: { name: "Seattle, WA", state: "Washington", col: 1.35, rent3br: 3200, mortgage3br: 3650, utilities: 410, daycare: 1650, transit: 680 },
    los_angeles: { name: "Los Angeles, CA", state: "California", col: 1.42, rent3br: 3400, mortgage3br: 3900, utilities: 420, daycare: 1700, transit: 720 },
    chicago: { name: "Chicago, IL", state: "Illinois", col: 1.12, rent3br: 2400, mortgage3br: 2750, utilities: 400, daycare: 1350, transit: 650 },
    nyc: { name: "New York, NY", state: "New York", col: 1.55, rent3br: 3800, mortgage3br: 4300, utilities: 450, daycare: 1900, transit: 520 },
  };

  const LIFESTYLES = {
    bare: { label: "Bare Minimum", multiplier: 0.78, savingsRate: 0.05, classLabel: "Essentials-focused", food: 850, misc: 350 },
    stable: { label: "Stable", multiplier: 0.92, savingsRate: 0.08, classLabel: "Stable middle-class", food: 950, misc: 450 },
    comfortable: { label: "Comfortable", multiplier: 1, savingsRate: 0.12, classLabel: "Comfortable middle-class", food: 1100, misc: 650 },
    upper: { label: "Upper Middle Class", multiplier: 1.22, savingsRate: 0.18, classLabel: "Upper middle-class", food: 1350, misc: 950 },
  };

  const HOUSING_TYPE = { apartment: { rentMul: 0.82, ownMul: 0.88 }, townhome: { rentMul: 0.95, ownMul: 1 }, single: { rentMul: 1, ownMul: 1 }, luxury: { rentMul: 1.45, ownMul: 1.55 } };
  const HOUSING_STATUS = { rent: { mode: "rent", extra: 0 }, own: { mode: "own", extra: 0 }, mortgage: { mode: "own", extra: 150 } };
  const CHILDCARE = { none: { cost: 0 }, part: { cost: 650 }, full: { mul: 1 }, private: { cost: 1850 } };
  const TRANSPORT = { one_car: { cost: 650 }, two_cars: { cost: 950 }, transit: { cost: 420 }, remote: { cost: 280 } };
  const HEALTH = { employer: { cost: 520 }, marketplace: { cost: 780 }, hdhp: { cost: 620 } };
  const STATE_COMFORT = { Texas: 108000, Florida: 112000, California: 158000, Arizona: 106000, Georgia: 104000, Colorado: 122000, Washington: 138000, Illinois: 118000, "New York": 165000 };
  const TAX_RATE = { Texas: 0.22, Florida: 0.22, Arizona: 0.23, Georgia: 0.23, Colorado: 0.24, Washington: 0.25, California: 0.28, Illinois: 0.25, "New York": 0.29 };
  const COMPARE_KEYS = ["dallas", "austin", "phoenix", "tampa"];
  const PIE_COLORS = {
    housing: "#0f7b6c",
    childcare: "#2d6a9f",
    food: "#38a169",
    transportation: "#3182ce",
    healthcare: "#627d98",
    misc: "#94a3b8",
  };

  function fmtUSD(n) {
    return new Intl.NumberFormat("en-US", { style: "currency", currency: "USD", maximumFractionDigits: 0 }).format(n);
  }

  function fmtRange(low, high) {
    return fmtUSD(low) + "–" + fmtUSD(high);
  }

  function computeBudget(inputs) {
    const city = CITIES[inputs.city] || CITIES.dallas;
    const lifestyle = LIFESTYLES[inputs.lifestyle] || LIFESTYLES.comfortable;
    const housingType = HOUSING_TYPE[inputs.housingType] || HOUSING_TYPE.single;
    const housingStatus = HOUSING_STATUS[inputs.housingStatus] || HOUSING_STATUS.rent;
    const childcareCfg = CHILDCARE[inputs.childcare] || CHILDCARE.full;
    const transport = TRANSPORT[inputs.transport] || TRANSPORT.two_cars;
    const health = HEALTH[inputs.health] || HEALTH.employer;

    let housingBase = housingStatus.mode === "rent" ? city.rent3br * housingType.rentMul : city.mortgage3br * housingType.ownMul;
    housingBase += (housingStatus.extra || 0) + city.utilities * housingType.rentMul;

    const childcare = childcareCfg.mul ? city.daycare * childcareCfg.mul * lifestyle.multiplier : (childcareCfg.cost || 0) * city.col;
    const food = lifestyle.food * city.col;
    const transportation = transport.cost * (city.transit / 750);
    const healthcare = health.cost * (0.85 + city.col * 0.15);
    const misc = lifestyle.misc * city.col;
    const essentials = housingBase + childcare + food + transportation + healthcare + misc;
    const savings = essentials * lifestyle.savingsRate;
    const monthlyNeed = essentials + savings;
    const taxRate = TAX_RATE[city.state] || 0.24;
    const annualGross = Math.round((monthlyNeed * 12) / (1 - taxRate));

    const breakdown = [
      { key: "housing", label: "Housing", amount: housingBase },
      { key: "childcare", label: "Childcare", amount: childcare },
      { key: "food", label: "Food", amount: food },
      { key: "transportation", label: "Transportation", amount: transportation },
      { key: "healthcare", label: "Healthcare", amount: healthcare },
      { key: "misc", label: "Other & lifestyle", amount: misc },
    ].map((b) => ({ ...b, pct: essentials > 0 ? Math.round((b.amount / essentials) * 100) : 0 }));

    return { city, lifestyle, monthlyNeed, annualGross, low: Math.round(annualGross * 0.92), high: Math.round(annualGross * 1.08), savings, breakdown, essentials, taxRate };
  }

  const els = {
    heroPreview: document.getElementById("f4-hero-preview"),
    quickResults: document.getElementById("f4-quick-results"),
    resultIncome: document.getElementById("f4-result-income"),
    resultIncomeHero: document.getElementById("f4-result-income-hero"),
    resultRangeHero: document.getElementById("f4-result-range-hero"),
    resultRange: document.getElementById("f4-result-range"),
    resultClass: document.getElementById("f4-result-class"),
    resultSavings: document.getElementById("f4-result-savings"),
    budgetList: document.getElementById("f4-budget-list"),
    pieChart: document.getElementById("f4-pie-chart"),
    pieLegend: document.getElementById("f4-pie-legend"),
    cityCompare: document.getElementById("f4-city-compare"),
    stateTable: document.getElementById("f4-state-table-body"),
    exampleCard: document.getElementById("f4-example-dallas"),
    housingLocal: document.getElementById("f4-housing-local"),
    childcareLocal: document.getElementById("f4-childcare-local"),
    oneIncome: document.getElementById("f4-one-income-note"),
  };

  function readPlannerInputs() {
    return {
      city: document.getElementById("f4-city")?.value || "dallas",
      lifestyle: document.querySelector("[data-f4-lifestyle].is-selected")?.dataset.f4Lifestyle || "comfortable",
      housingType: document.getElementById("f4-housing-type")?.value || "single",
      housingStatus: document.getElementById("f4-housing-status")?.value || "rent",
      childcare: document.getElementById("f4-childcare")?.value || "full",
      transport: document.getElementById("f4-transport")?.value || "two_cars",
      health: document.getElementById("f4-health")?.value || "employer",
    };
  }

  function readQuickInputs() {
    return {
      city: document.getElementById("f4-quick-city")?.value || "dallas",
      lifestyle: document.getElementById("f4-quick-lifestyle")?.value || "comfortable",
      housingType: document.getElementById("f4-quick-housing")?.value || "single",
      childcare: "full",
      housingStatus: "rent",
      transport: "two_cars",
      health: "employer",
    };
  }

  function syncQuickToPlanner(inputs) {
    const cityEl = document.getElementById("f4-city");
    const housingEl = document.getElementById("f4-housing-type");
    if (cityEl) cityEl.value = inputs.city;
    if (housingEl) housingEl.value = inputs.housingType;
    document.querySelectorAll("[data-f4-lifestyle]").forEach((card) => {
      const on = card.dataset.f4Lifestyle === inputs.lifestyle;
      card.classList.toggle("is-selected", on);
      card.setAttribute("aria-pressed", on ? "true" : "false");
    });
  }

  function housingLabel(key) {
    return { apartment: "Apartment (3BR)", townhome: "Townhome", single: "Single-family home", luxury: "Premium home" }[key] || key;
  }

  function renderQuickResults(result, inputs, opts) {
    if (!els.quickResults) return;
    const city = CITIES[inputs.city] || CITIES.dallas;
    const lifestyle = LIFESTYLES[inputs.lifestyle] || LIFESTYLES.comfortable;
    els.quickResults.innerHTML =
      '<p class="f4-quick-result-kicker">Your quick estimate</p>' +
      '<p class="f4-quick-result-label">Household income needed</p>' +
      '<p class="f4-quick-result-range">' + fmtRange(result.low, result.high) + '</p>' +
      '<p class="f4-quick-result-unit">per year · gross, before tax</p>' +
      '<ul class="f4-quick-result-meta">' +
      '<li><span>City</span><strong>' + city.name + '</strong></li>' +
      '<li><span>Lifestyle</span><strong>' + lifestyle.label + '</strong></li>' +
      '<li><span>Housing</span><strong>' + housingLabel(inputs.housingType) + '</strong></li>' +
      '<li><span>Monthly budget</span><strong>' + fmtUSD(Math.round(result.monthlyNeed)) + '/mo</strong></li>' +
      '</ul>' +
      '<a class="f4-quick-result-link" href="#f4-planner">See full breakdown in planner ↓</a>';
    if (opts && opts.pulse) {
      els.quickResults.classList.add("f4-quick-results--pulse");
      window.setTimeout(function () { els.quickResults.classList.remove("f4-quick-results--pulse"); }, 900);
    }
  }

  function renderQuickFromForm(opts) {
    const inputs = readQuickInputs();
    renderQuickResults(computeBudget(inputs), inputs, opts);
  }

  function renderPie(breakdown) {
    if (!els.pieChart) return;
    let cursor = 0;
    const stops = breakdown.filter((b) => b.amount > 0).map((b) => {
      const start = cursor;
      cursor += b.pct;
      return PIE_COLORS[b.key] + " " + start + "% " + cursor + "%";
    }).join(", ");
    els.pieChart.style.background = "conic-gradient(" + (stops || "#e0e7ef 0 100%") + ")";
  }

  function renderPieLegend(breakdown) {
    if (!els.pieLegend) return;
    els.pieLegend.innerHTML = breakdown.filter((b) => b.amount > 0).map((b) =>
      `<span class="f4-pie-legend-item"><i style="background:${PIE_COLORS[b.key]}"></i>${b.label} <strong>${b.pct}%</strong></span>`
    ).join("");
  }

  function renderBudgetList(breakdown) {
    if (!els.budgetList) return;
    els.budgetList.innerHTML = breakdown.filter((b) => b.amount > 0).map((b) =>
      `<div class="f4-budget-row f4-budget-row--${b.key}"><span class="f4-budget-label">${b.label}</span><span class="f4-budget-amt">${fmtUSD(b.amount)}</span></div>`
    ).join("");
  }

  function renderResults(result) {
    if (els.resultIncomeHero) els.resultIncomeHero.textContent = fmtRange(result.low, result.high);
    if (els.resultRangeHero) els.resultRangeHero.textContent = fmtUSD(result.annualGross) + "/year midpoint · " + result.lifestyle.classLabel;
    if (els.resultIncome) els.resultIncome.textContent = fmtUSD(result.annualGross) + "/year";
    if (els.resultRange) els.resultRange.textContent = fmtRange(result.low, result.high) + " typical range";
    if (els.resultClass) els.resultClass.textContent = result.lifestyle.classLabel;
    if (els.resultSavings) els.resultSavings.textContent = fmtUSD(result.savings) + "/mo";
    renderBudgetList(result.breakdown);
    renderPie(result.breakdown);
    renderPieLegend(result.breakdown);
    updateHeroPreview(result);
    updateLocalSections(result);
  }

  function updateHeroPreview(result) {
    if (!els.heroPreview) return;
    els.heroPreview.querySelector("[data-f4-preview-city]").textContent = result.city.name;
    els.heroPreview.querySelector("[data-f4-preview-lifestyle]").textContent = result.lifestyle.label;
    els.heroPreview.querySelector("[data-f4-preview-income]").textContent = fmtRange(result.low, result.high) + "/year";
  }

  function updateLocalSections(result) {
    const housing = result.breakdown.find((b) => b.key === "housing");
    const childcare = result.breakdown.find((b) => b.key === "childcare");
    if (els.housingLocal && housing) {
      els.housingLocal.innerHTML = `<p><strong>${result.city.name}</strong> — housing + utilities in your model: <strong>${fmtUSD(housing.amount)}/mo</strong>. Typical 3-bedroom rent ~ <strong>${fmtUSD(result.city.rent3br)}</strong>; mortgage ~ <strong>${fmtUSD(result.city.mortgage3br)}</strong> before taxes and insurance.</p>`;
    }
    if (els.childcareLocal && childcare) {
      els.childcareLocal.innerHTML = `<p>Daycare in ${result.city.name} often runs near <strong>${fmtUSD(result.city.daycare)}/mo</strong> per child. Your settings: <strong>${fmtUSD(childcare.amount)}/mo</strong>.</p>`;
    }
    if (els.oneIncome) {
      els.oneIncome.innerHTML = `In <strong>${result.city.name}</strong>, one income for a family of four at a <strong>${result.lifestyle.label.toLowerCase()}</strong> level often needs <strong>${fmtUSD(result.annualGross)}+</strong> gross—or about <strong>${fmtUSD(Math.round(result.annualGross / 2))}</strong> per earner with two incomes.`;
    }
    if (els.exampleCard) {
      els.exampleCard.innerHTML = `<h3>${result.city.name} family of 4</h3><dl class="f4-example-dl"><div><dt>Modeled income</dt><dd>${fmtUSD(result.annualGross)}</dd></div><div><dt>Housing</dt><dd>${fmtUSD(housing?.amount || 0)}/mo</dd></div><div><dt>Lifestyle</dt><dd>${result.lifestyle.label}</dd></div></dl>`;
    }
  }

  function renderCityCompare(activeCity) {
    if (!els.cityCompare) return;
    const lifestyle = readPlannerInputs().lifestyle;
    els.cityCompare.innerHTML = COMPARE_KEYS.map((key) => {
      const r = computeBudget(Object.assign({}, readPlannerInputs(), { city: key, lifestyle }));
      const housing = r.breakdown.find((b) => b.key === "housing");
      const cc = r.breakdown.find((b) => b.key === "childcare");
      const active = key === activeCity ? " is-active" : "";
      return `<button type="button" class="f4-city-card${active}" data-f4-compare-city="${key}"><h3>${r.city.name}</h3><p class="f4-city-card-income">${fmtUSD(r.annualGross)}/yr</p><p class="f4-city-card-detail">Housing ~${fmtUSD(housing?.amount || 0)}/mo</p><p class="f4-city-card-detail">Childcare ~${fmtUSD(cc?.amount || 0)}/mo</p></button>`;
    }).join("");
    els.cityCompare.querySelectorAll("[data-f4-compare-city]").forEach((btn) => {
      btn.addEventListener("click", () => {
        const city = btn.getAttribute("data-f4-compare-city");
        const cityEl = document.getElementById("f4-city");
        const quickCity = document.getElementById("f4-quick-city");
        if (cityEl) cityEl.value = city;
        if (quickCity) quickCity.value = city;
        renderAll();
      });
    });
  }

  function renderStateTable() {
    if (!els.stateTable) return;
    els.stateTable.innerHTML = Object.entries(STATE_COMFORT).map(([state, salary]) =>
      `<tr><th scope="row">${state}</th><td>${fmtUSD(salary)}/year</td></tr>`
    ).join("");
  }

  function renderAll() {
    const inputs = readPlannerInputs();
    renderResults(computeBudget(inputs));
    renderCityCompare(inputs.city);
  }

  document.querySelectorAll("[data-f4-lifestyle]").forEach((card) => {
    card.addEventListener("click", () => {
      document.querySelectorAll("[data-f4-lifestyle]").forEach((c) => {
        c.classList.remove("is-selected");
        c.setAttribute("aria-pressed", "false");
      });
      card.classList.add("is-selected");
      card.setAttribute("aria-pressed", "true");
      const ql = document.getElementById("f4-quick-lifestyle");
      if (ql) ql.value = card.dataset.f4Lifestyle;
      renderAll();
    });
  });

  ["f4-city", "f4-housing-type", "f4-housing-status", "f4-childcare", "f4-transport", "f4-health"].forEach((id) => {
    document.getElementById(id)?.addEventListener("change", renderAll);
  });

  document.getElementById("f4-quick-form")?.addEventListener("submit", (e) => {
    e.preventDefault();
    const inputs = readQuickInputs();
    syncQuickToPlanner(inputs);
    renderAll();
    renderQuickFromForm({ pulse: true });
    els.quickResults?.scrollIntoView({ behavior: "smooth", block: "nearest" });
  });

  ["f4-quick-city", "f4-quick-lifestyle", "f4-quick-housing"].forEach((id) => {
    document.getElementById(id)?.addEventListener("change", () => renderQuickFromForm());
  });

  document.querySelectorAll("[data-scroll-to]").forEach((btn) => {
    btn.addEventListener("click", () => {
      document.getElementById(btn.getAttribute("data-scroll-to"))?.scrollIntoView({ behavior: "smooth", block: "start" });
    });
  });

  renderStateTable();
  renderQuickFromForm();
  renderAll();
})();
