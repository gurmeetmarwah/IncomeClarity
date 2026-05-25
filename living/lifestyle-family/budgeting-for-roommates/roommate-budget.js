(function () {
  const CITIES = {
    austin: { name: "Austin, TX", state: "Texas", col: 1.14, rent2br: 2400, solo1br: 1650, utilities: 95, tax: 0.22 },
    dallas: { name: "Dallas, TX", state: "Texas", col: 1, rent2br: 2100, solo1br: 1450, utilities: 85, tax: 0.22 },
    phoenix: { name: "Phoenix, AZ", state: "Arizona", col: 1.02, rent2br: 2050, solo1br: 1380, utilities: 90, tax: 0.23 },
    tampa: { name: "Tampa, FL", state: "Florida", col: 1.04, rent2br: 2200, solo1br: 1500, utilities: 80, tax: 0.22 },
    atlanta: { name: "Atlanta, GA", state: "Georgia", col: 1.06, rent2br: 2150, solo1br: 1480, utilities: 88, tax: 0.23 },
    denver: { name: "Denver, CO", state: "Colorado", col: 1.18, rent2br: 2650, solo1br: 1850, utilities: 92, tax: 0.24 },
    chicago: { name: "Chicago, IL", state: "Illinois", col: 1.12, rent2br: 2400, solo1br: 1720, utilities: 95, tax: 0.25 },
    seattle: { name: "Seattle, WA", state: "Washington", col: 1.35, rent2br: 3200, solo1br: 2100, utilities: 100, tax: 0.25 },
  };

  const COMPARE_KEYS = ["austin", "dallas", "phoenix", "tampa"];
  const BEST_KEYS = ["austin", "chicago", "denver", "atlanta"];
  const PIE_COLORS = {
    rent: "#0f7b6c",
    utilities: "#2d6a9f",
    food: "#38a169",
    internet: "#3182ce",
    misc: "#94a3b8",
  };

  // Monthly household estimates (split among roommates — not multiplied per person).
  const SHARED_DEFAULTS = {
    internet: 75,
    streaming: 35,
    groceries: 220,
    parking: 85,
    cleaning: 40,
  };

  /** Slight scale-up for larger households (utilities, shared groceries). */
  function householdScale(n) {
    return 1 + Math.max(0, n - 2) * 0.12;
  }

  function householdUtilities(city, n) {
    return Math.round(city.utilities * city.col * householdScale(n));
  }

  function householdGroceries(city, n) {
    return Math.round(SHARED_DEFAULTS.groceries * city.col * (1.25 + Math.max(0, n - 2) * 0.2));
  }

  function fmtUSD(n) {
    return new Intl.NumberFormat("en-US", { style: "currency", currency: "USD", maximumFractionDigits: 0 }).format(n);
  }

  function fmtRange(low, high) {
    return fmtUSD(low) + "–" + fmtUSD(high);
  }

  function clamp(n, min, max) {
    return Math.min(max, Math.max(min, n));
  }

  function bedroomWeights(structure, count) {
    const n = Math.max(2, Math.min(6, count));
    const w = new Array(n).fill(1);
    if (structure === "master" && n >= 2) w[0] = 1.35;
    if (structure === "shared" && n >= 3) {
      w[n - 2] = 0.75;
      w[n - 1] = 0.75;
    }
    if (structure === "mix" && n >= 3) {
      const priv = Math.ceil(n / 2);
      for (let i = 0; i < priv; i++) w[i] = 1.15;
      for (let i = priv; i < n; i++) w[i] = 0.88;
    }
    return w;
  }

  function incomeWeights(count) {
    const presets = {
      2: [1.1, 0.9],
      3: [1.2, 1, 0.85],
      4: [1.25, 1.05, 0.95, 0.8],
      5: [1.3, 1.1, 1, 0.9, 0.75],
      6: [1.3, 1.15, 1.05, 1, 0.9, 0.75],
    };
    const p = presets[count] || presets[3];
    return p.slice(0, count);
  }

  const STRUCTURE_LABELS = {
    equal: "Equal bedrooms",
    master: "Master bedroom pays more",
    shared: "Shared bedroom discount",
    mix: "Private + shared mix",
  };

  /** Bedroom structure always controls rent split. */
  function rentSplitWeights(structure, count) {
    return bedroomWeights(structure, count);
  }

  /** Split method controls shared bills only. */
  function billSplitWeights(method, structure, count) {
    const n = Math.max(2, Math.min(6, count));
    if (method === "income") return incomeWeights(n);
    if (method === "bedroom") return bedroomWeights(structure, n);
    if (method === "custom") return new Array(n).fill(1);
    return new Array(n).fill(1);
  }

  function shareAmount(total, weights, index) {
    const sum = weights.reduce((a, b) => a + b, 0) || 1;
    return (total * weights[index]) / sum;
  }

  function avgPerPerson(total, n) {
    return total / Math.max(1, n);
  }

  function readSharedFlags(prefix) {
    return {
      utilities: document.getElementById(prefix + "util")?.checked !== false,
      internet: document.getElementById(prefix + "internet")?.checked !== false,
      streaming: document.getElementById(prefix + "streaming")?.checked !== false,
      groceries: document.getElementById(prefix + "groceries")?.checked !== false,
      parking: document.getElementById(prefix + "parking")?.checked === true,
      cleaning: document.getElementById(prefix + "cleaning")?.checked !== false,
    };
  }

  function readQuickInputs() {
    const city = document.getElementById("rm-quick-city")?.value || "austin";
    const rent = Number(document.getElementById("rm-quick-rent")?.value) || CITIES[city].rent2br;
    const roommates = Number(document.getElementById("rm-quick-roommates")?.value) || 3;
    const utilIncluded = document.getElementById("rm-quick-util-included")?.value === "yes";
    return {
      city,
      rent,
      roommates,
      structure: "equal",
      splitMethod: "equal",
      utilIncluded,
      shared: { utilities: !utilIncluded, internet: true, streaming: false, groceries: false, parking: false, cleaning: false },
    };
  }

  function readPlannerInputs() {
    const city = document.getElementById("rm-city")?.value || "austin";
    const rent = Number(document.getElementById("rm-rent")?.value) || CITIES[city].rent2br;
    const roommates = Number(document.querySelector("[data-rm-roommates].is-selected")?.dataset.rmRoommates || 3);
    const structure = document.querySelector("[data-rm-structure].is-selected")?.dataset.rmStructure || "equal";
    const splitMethod = document.querySelector("[data-rm-split].is-selected")?.dataset.rmSplit || "equal";
    const utilIncluded = document.getElementById("rm-util-included")?.value === "yes";
    const shared = readSharedFlags("rm-");
    if (utilIncluded) shared.utilities = false;
    return { city, rent, roommates, structure, splitMethod, utilIncluded, shared };
  }

  function computeRoommateBudget(inputs) {
    const city = CITIES[inputs.city] || CITIES.austin;
    const n = clamp(Math.round(inputs.roommates), 2, 6);
    const rent = clamp(inputs.rent, 500, 10000);
    const rentWeights = rentSplitWeights(inputs.structure, n);
    const billWeights = billSplitWeights(inputs.splitMethod, inputs.structure, n);
    const col = city.col;

    const utilHouse = inputs.shared.utilities ? householdUtilities(city, n) : 0;
    const internet = inputs.shared.internet ? Math.round(SHARED_DEFAULTS.internet * col) : 0;
    const streaming = inputs.shared.streaming ? Math.round(SHARED_DEFAULTS.streaming * col) : 0;
    const groceries = inputs.shared.groceries ? householdGroceries(city, n) : 0;
    const parking = inputs.shared.parking ? Math.round(SHARED_DEFAULTS.parking * col) : 0;
    const cleaning = inputs.shared.cleaning ? Math.round(SHARED_DEFAULTS.cleaning * col) : 0;

    const sharedBills = utilHouse + internet + streaming + groceries + parking + cleaning;
    const totalHousehold = rent + sharedBills;

    const perPerson = [];
    for (let i = 0; i < n; i++) {
      const rentShare = shareAmount(rent, rentWeights, i);
      const billShare = shareAmount(sharedBills, billWeights, i);
      const monthly = Math.round(rentShare + billShare);
      perPerson.push({
        label: "Roommate " + (i + 1),
        rent: Math.round(rentShare),
        bills: Math.round(billShare),
        monthly,
      });
    }

    const rentShares = perPerson.map((p) => p.rent);
    const monthlyShares = perPerson.map((p) => p.monthly);
    const rentLow = Math.min.apply(null, rentShares);
    const rentHigh = Math.max.apply(null, rentShares);
    const monthlyLow = Math.min.apply(null, monthlyShares);
    const monthlyHigh = Math.max.apply(null, monthlyShares);
    const hasRentSpread = rentHigh - rentLow >= 5;
    const hasMonthlySpread = monthlyHigh - monthlyLow >= 5;

    const rentPerPerson = Math.round(rentShares.reduce((s, v) => s + v, 0) / n);
    const housingPerPerson = Math.round(
      rentPerPerson +
        avgPerPerson(utilHouse, n) +
        (inputs.shared.internet ? avgPerPerson(internet, n) : 0)
    );
    const avgMonthly = Math.round(monthlyShares.reduce((s, v) => s + v, 0) / n);
    const low = hasMonthlySpread ? monthlyLow : Math.round(avgMonthly * 0.94);
    const high = hasMonthlySpread ? monthlyHigh : Math.round(avgMonthly * 1.08);

    const soloMonthly = Math.round(
      city.solo1br * col +
        city.utilities * col +
        SHARED_DEFAULTS.groceries * col +
        SHARED_DEFAULTS.internet * col * 0.5 +
        120
    );
    const savings = Math.max(0, soloMonthly - avgMonthly);
    const savingsPct = soloMonthly > 0 ? Math.round((savings / soloMonthly) * 100) : 0;

    const annualGross = Math.round((avgMonthly * 12) / (1 - city.tax));
    const incomeLow = Math.round(annualGross * 0.92);
    const incomeHigh = Math.round(annualGross * 1.1);

    const misc = Math.round((streaming + cleaning + parking) / n);
    const breakdown = [
      { key: "rent", label: "Rent", amount: avgPerPerson(rent, n) },
      { key: "utilities", label: "Utilities", amount: avgPerPerson(utilHouse, n) },
      { key: "food", label: "Groceries", amount: avgPerPerson(groceries, n) },
      { key: "internet", label: "Internet & streaming", amount: avgPerPerson(internet + streaming, n) },
      { key: "misc", label: "Parking & supplies", amount: misc },
    ].filter((b) => b.amount > 0);

    const essentials = breakdown.reduce((s, b) => s + b.amount, 0);
    breakdown.forEach((b) => {
      b.pct = essentials > 0 ? Math.round((b.amount / essentials) * 100) : 0;
    });

    return {
      city,
      n,
      rent,
      structure: inputs.structure,
      structureLabel: STRUCTURE_LABELS[inputs.structure] || inputs.structure,
      splitMethod: inputs.splitMethod,
      rentPerPerson,
      rentLow,
      rentHigh,
      hasRentSpread,
      hasMonthlySpread,
      housingPerPerson,
      avgMonthly,
      monthlyLow,
      monthlyHigh,
      low,
      high,
      perPerson,
      soloMonthly,
      savings,
      savingsPct,
      incomeLow,
      incomeHigh,
      breakdown,
      totalHousehold,
      rentWeights,
      billWeights,
      utilHouse,
      groceriesHouse: groceries,
    };
  }

  const els = {
    heroPreview: document.getElementById("rm-hero-preview"),
    quickResults: document.getElementById("rm-quick-results"),
    resultPerPersonHero: document.getElementById("rm-result-per-person-hero"),
    resultRange: document.getElementById("rm-result-range"),
    resultSavings: document.getElementById("rm-result-savings"),
    resultIncome: document.getElementById("rm-result-income"),
    resultRentShare: document.getElementById("rm-result-rent-share"),
    budgetList: document.getElementById("rm-budget-list"),
    pieChart: document.getElementById("rm-pie-chart"),
    pieLegend: document.getElementById("rm-pie-legend"),
    cityCompare: document.getElementById("rm-city-compare"),
    aloneCompare: document.getElementById("rm-alone-compare"),
    incomeSection: document.getElementById("rm-income-note"),
    bestCities: document.getElementById("rm-best-cities-grid"),
    exampleCards: document.getElementById("rm-example-cards"),
    splitBreakdown: document.getElementById("rm-split-breakdown"),
    splitContext: document.getElementById("rm-split-context"),
  };

  function renderPie(breakdown) {
    if (!els.pieChart) return;
    let cursor = 0;
    const stops = breakdown
      .filter((b) => b.amount > 0)
      .map((b) => {
        const start = cursor;
        cursor += b.pct;
        return PIE_COLORS[b.key] + " " + start + "% " + cursor + "%";
      })
      .join(", ");
    els.pieChart.style.background = "conic-gradient(" + (stops || "#e0e7ef 0 100%") + ")";
  }

  function renderPieLegend(breakdown) {
    if (!els.pieLegend) return;
    els.pieLegend.innerHTML = breakdown
      .filter((b) => b.amount > 0)
      .map(
        (b) =>
          '<span class="rm-pie-legend-item"><i style="background:' +
          PIE_COLORS[b.key] +
          '"></i>' +
          b.label +
          " <strong>" +
          b.pct +
          "%</strong></span>"
      )
      .join("");
  }

  function renderBudgetList(breakdown) {
    if (!els.budgetList) return;
    els.budgetList.innerHTML = breakdown
      .map(
        (b) =>
          '<div class="rm-budget-row rm-budget-row--' +
          b.key +
          '"><span>' +
          b.label +
          "</span><strong>" +
          fmtUSD(b.amount) +
          "</strong></div>"
      )
      .join("");
  }

  function formatShareAmount(low, high, hasSpread) {
    return hasSpread ? fmtRange(low, high) : fmtUSD(low);
  }

  function renderSplitBreakdown(result) {
    if (!els.splitBreakdown) return;
    els.splitBreakdown.innerHTML = result.perPerson
      .map(
        (p) =>
          '<div class="rm-split-row"><span>' +
          p.label +
          '</span><div class="rm-split-amts"><strong>' +
          fmtUSD(p.monthly) +
          '/mo</strong><span>Rent ' +
          fmtUSD(p.rent) +
          " · Bills " +
          fmtUSD(p.bills) +
          "</span></div></div>"
      )
      .join("");
    if (els.splitContext) {
      els.splitContext.textContent =
        result.structureLabel +
        " · Rent split by bedroom · Shared bills: " +
        (result.splitMethod === "equal"
          ? "equal"
          : result.splitMethod === "income"
            ? "by income"
            : result.splitMethod === "bedroom"
              ? "by bedroom"
              : "custom");
    }
  }

  function renderResults(result) {
    const headline = result.hasMonthlySpread
      ? formatShareAmount(result.monthlyLow, result.monthlyHigh, true) + "/month"
      : fmtUSD(result.avgMonthly) + "/month";
    const rentTxt = result.hasRentSpread
      ? formatShareAmount(result.rentLow, result.rentHigh, true) + "/mo rent"
      : fmtUSD(result.rentPerPerson) + "/mo rent";
    if (els.resultPerPersonHero) els.resultPerPersonHero.textContent = headline;
    if (els.resultRange) {
      els.resultRange.textContent = result.hasMonthlySpread
        ? "Range across roommates · average " + fmtUSD(result.avgMonthly) + "/mo"
        : fmtRange(result.low, result.high) + "/month typical range";
    }
    if (els.resultRentShare) {
      els.resultRentShare.textContent =
        rentTxt +
        " · Housing bundle ~" +
        fmtUSD(result.housingPerPerson) +
        "/mo (before other shared bills)";
    }
    if (els.resultSavings) els.resultSavings.textContent = fmtUSD(result.savings) + "/month vs living alone";
    if (els.resultIncome) els.resultIncome.textContent = fmtRange(result.incomeLow, result.incomeHigh) + "/year";
    renderSplitBreakdown(result);
    renderBudgetList(result.breakdown);
    renderPie(result.breakdown);
    renderPieLegend(result.breakdown);
    updateHeroPreview(result, "planner");
    updateAloneCompare(result);
    updateIncomeNote(result);
  }

  function renderQuickResults(result, opts) {
    if (!els.quickResults) return;
    updateHeroPreview(result, "quick");
    els.quickResults.innerHTML =
      '<p class="rm-quick-result-kicker">Your quick estimate</p>' +
      '<p class="rm-quick-result-label">Rent share per roommate</p>' +
      '<p class="rm-quick-result-range">' +
      (result.hasRentSpread ? formatShareAmount(result.rentLow, result.rentHigh, true) : fmtUSD(result.rentPerPerson)) +
      "/mo" +
      "</p>" +
      '<p class="rm-quick-result-unit">of ' +
      fmtUSD(result.rent) +
      " total rent · " +
      result.n +
      " people in " +
      result.city.name +
      "</p>" +
      '<p class="rm-quick-result-allin">All-in with shared bills: <strong>' +
      fmtRange(result.low, result.high) +
      "/mo</strong> <span>(rent + utilities + internet)</span></p>" +
      '<ul class="rm-quick-result-meta">' +
      "<li><span>Rent only</span><strong>" +
      fmtUSD(result.rentPerPerson) +
      "/mo each</strong></li>" +
      "<li><span>Housing bundle</span><strong>" +
      fmtUSD(result.housingPerPerson) +
      "/mo each</strong></li>" +
      "<li><span>vs living alone</span><strong>~" +
      fmtUSD(result.savings) +
      " saved</strong></li>" +
      "</ul>" +
      '<a class="rm-quick-result-link" href="#rm-planner">Add groceries &amp; more in full planner ↓</a>';
    if (opts && opts.pulse) {
      els.quickResults.classList.add("rm-quick-results--pulse");
      window.setTimeout(function () {
        els.quickResults.classList.remove("rm-quick-results--pulse");
      }, 900);
    }
  }

  function updateHeroPreview(result, source) {
    if (!els.heroPreview) return;
    const useQuick = source === "quick";
    const inputs = useQuick ? readQuickInputs() : readPlannerInputs();
    const preview = useQuick ? computeRoommateBudget(inputs) : result;
    els.heroPreview.querySelector("[data-rm-preview-rent]").textContent = fmtUSD(preview.rent);
    els.heroPreview.querySelector("[data-rm-preview-roommates]").textContent = String(preview.n);
    const rentShare = els.heroPreview.querySelector("[data-rm-preview-rent-share]");
    const allIn = els.heroPreview.querySelector("[data-rm-preview-allin]");
    if (rentShare) {
      rentShare.textContent = preview.hasRentSpread
        ? formatShareAmount(preview.rentLow, preview.rentHigh, true) + "/mo"
        : fmtUSD(preview.rentPerPerson) + "/mo";
    }
    if (allIn) {
      allIn.textContent = preview.hasMonthlySpread
        ? formatShareAmount(preview.monthlyLow, preview.monthlyHigh, true) + "/mo"
        : fmtUSD(preview.avgMonthly) + "/mo";
    }
  }

  function updateAloneCompare(result) {
    if (!els.aloneCompare) return;
    els.aloneCompare.innerHTML =
      "<p>Living with <strong>" +
      result.n +
      " roommates</strong> in <strong>" +
      result.city.name +
      "</strong> could reduce monthly housing-related costs by about <strong>" +
      result.savingsPct +
      "%</strong> compared to a typical solo 1-bedroom (~" +
      fmtUSD(result.soloMonthly) +
      "/mo alone vs ~" +
      fmtUSD(result.avgMonthly) +
      "/mo your share).</p>";
  }

  function updateIncomeNote(result) {
    if (!els.incomeSection) return;
    els.incomeSection.innerHTML =
      "<p>In <strong>" +
      result.city.name +
      "</strong>, a roommate setup often lowers the gross salary needed for the same lifestyle. Modeled midpoint: <strong>" +
      fmtRange(result.incomeLow, result.incomeHigh) +
      "/year</strong> per person at ~" +
      fmtUSD(result.avgMonthly) +
      "/mo all-in—versus roughly <strong>" +
      fmtUSD(Math.round((result.soloMonthly * 12) / (1 - result.city.tax))) +
      "/year</strong> gross living alone on similar assumptions.</p>";
  }

  function renderCityCompare(activeCity, inputsTemplate) {
    if (!els.cityCompare) return;
    const base = inputsTemplate || readPlannerInputs();
    els.cityCompare.innerHTML = COMPARE_KEYS.map((key) => {
      const r = computeRoommateBudget(Object.assign({}, base, { city: key, rent: CITIES[key].rent2br }));
      const active = key === activeCity ? " is-active" : "";
      return (
        '<button type="button" class="rm-city-card' +
        active +
        '" data-rm-compare-city="' +
        key +
        '"><h3>' +
        r.city.name +
        '</h3><p class="rm-city-card-cost">' +
        fmtUSD(r.avgMonthly) +
        '/mo each</p><p class="rm-city-card-detail">Typical 2BR ~' +
        fmtUSD(CITIES[key].rent2br) +
        '</p><p class="rm-city-card-detail">Save ~' +
        fmtUSD(r.savings) +
        "/mo vs solo</p></button>"
      );
    }).join("");
    els.cityCompare.querySelectorAll("[data-rm-compare-city]").forEach((btn) => {
      btn.addEventListener("click", () => {
        const city = btn.getAttribute("data-rm-compare-city");
        const cityEl = document.getElementById("rm-city");
        const quickCity = document.getElementById("rm-quick-city");
        const rentEl = document.getElementById("rm-rent");
        const quickRent = document.getElementById("rm-quick-rent");
        if (cityEl) cityEl.value = city;
        if (quickCity) quickCity.value = city;
        if (rentEl) rentEl.value = CITIES[city].rent2br;
        if (quickRent) quickRent.value = CITIES[city].rent2br;
        renderAll();
      });
    });
  }

  function renderBestCities() {
    if (!els.bestCities) return;
    const scores = { austin: "High", chicago: "Strong", denver: "Moderate", atlanta: "High" };
    els.bestCities.innerHTML = BEST_KEYS.map((key) => {
      const r = computeRoommateBudget({ city: key, rent: CITIES[key].rent2br, roommates: 3, structure: "equal", splitMethod: "equal", shared: { utilities: true, internet: true, streaming: true, groceries: true, parking: false, cleaning: true } });
      return (
        '<article class="rm-best-card"><h3>' +
        r.city.name +
        '</h3><p><strong>Affordability:</strong> ' +
        (scores[key] || "Good") +
        '</p><p><strong>Per-person cost:</strong> ~' +
        fmtUSD(r.avgMonthly) +
        "/mo (3 roommates)</p><p><strong>Rent sharing benefit:</strong> ~" +
        r.savingsPct +
        "% vs solo 1BR</p></article>"
      );
    }).join("");
  }

  function renderExamples() {
    if (!els.exampleCards) return;
    const examples = [
      { city: "dallas", rent: 2700, n: 3, label: "3 roommates — Dallas, TX", housing: "Apartment rent" },
      { city: "phoenix", rent: 2550, n: 2, label: "2 roommates — Phoenix, AZ", housing: "Townhome rental" },
    ];
    els.exampleCards.innerHTML = examples
      .map((ex) => {
        const r = computeRoommateBudget({
          city: ex.city,
          rent: ex.rent,
          roommates: ex.n,
          structure: "equal",
          splitMethod: "equal",
          shared: { utilities: true, internet: true, streaming: true, groceries: true, parking: false, cleaning: true },
        });
        return (
          '<article class="rm-example-card"><h3>' +
          ex.label +
          "</h3><dl><div><dt>" +
          ex.housing +
          "</dt><dd>" +
          fmtUSD(ex.rent) +
          '</dd></div><div><dt>Monthly cost per person</dt><dd>' +
          fmtUSD(r.avgMonthly) +
          "</dd></div></dl></article>"
        );
      })
      .join("");
  }

  function syncQuickToPlanner(inputs) {
    const cityEl = document.getElementById("rm-city");
    const rentEl = document.getElementById("rm-rent");
    const utilEl = document.getElementById("rm-util-included");
    const quickUtil = document.getElementById("rm-quick-util-included");
    if (cityEl) cityEl.value = inputs.city;
    if (rentEl) rentEl.value = inputs.rent;
    if (utilEl) utilEl.value = inputs.utilIncluded ? "yes" : "no";
    if (quickUtil) quickUtil.value = inputs.utilIncluded ? "yes" : "no";
    document.querySelectorAll("[data-rm-roommates]").forEach((btn) => {
      const on = Number(btn.dataset.rmRoommates) === inputs.roommates;
      btn.classList.toggle("is-selected", on);
      btn.setAttribute("aria-pressed", on ? "true" : "false");
    });
  }

  function renderQuickFromForm(opts) {
    const inputs = readQuickInputs();
    const result = computeRoommateBudget(inputs);
    renderQuickResults(result, opts);
    return result;
  }

  function renderAll() {
    const inputs = readPlannerInputs();
    const result = computeRoommateBudget(inputs);
    renderResults(result);
    renderCityCompare(inputs.city, inputs);
    return result;
  }

  function selectCard(group, btn) {
    document.querySelectorAll("[data-" + group + "]").forEach((c) => {
      c.classList.remove("is-selected");
      c.setAttribute("aria-pressed", "false");
    });
    btn.classList.add("is-selected");
    btn.setAttribute("aria-pressed", "true");
  }

  document.querySelectorAll("[data-rm-roommates]").forEach((btn) => {
    btn.addEventListener("click", () => {
      selectCard("rm-roommates", btn);
      renderAll();
    });
  });

  document.querySelectorAll("[data-rm-structure]").forEach((btn) => {
    btn.addEventListener("click", () => {
      selectCard("rm-structure", btn);
      renderAll();
    });
  });

  document.querySelectorAll("[data-rm-split]").forEach((btn) => {
    btn.addEventListener("click", () => {
      selectCard("rm-split", btn);
      renderAll();
    });
  });

  ["rm-city", "rm-rent", "rm-util-included", "rm-util", "rm-internet", "rm-streaming", "rm-groceries", "rm-parking", "rm-cleaning"].forEach((id) => {
    document.getElementById(id)?.addEventListener("change", renderAll);
    document.getElementById(id)?.addEventListener("input", renderAll);
  });

  document.getElementById("rm-quick-form")?.addEventListener("submit", (e) => {
    e.preventDefault();
    const inputs = readQuickInputs();
    syncQuickToPlanner(inputs);
    renderAll();
    renderQuickFromForm({ pulse: true });
    els.quickResults?.scrollIntoView({ behavior: "smooth", block: "nearest" });
  });

  ["rm-quick-city", "rm-quick-rent", "rm-quick-roommates", "rm-quick-util-included"].forEach((id) => {
    const el = document.getElementById(id);
    el?.addEventListener("change", () => {
      const city = document.getElementById("rm-quick-city")?.value;
      if (id === "rm-quick-city" && city && CITIES[city]) {
        const rentEl = document.getElementById("rm-quick-rent");
        if (rentEl && !rentEl.dataset.touched) rentEl.value = CITIES[city].rent2br;
      }
      renderQuickFromForm();
    });
    el?.addEventListener("input", () => {
      if (id === "rm-quick-rent") {
        const rentEl = document.getElementById("rm-quick-rent");
        if (rentEl) rentEl.dataset.touched = "1";
      }
      renderQuickFromForm();
    });
  });

  document.querySelectorAll("[data-scroll-to]").forEach((btn) => {
    btn.addEventListener("click", () => {
      document.getElementById(btn.getAttribute("data-scroll-to"))?.scrollIntoView({ behavior: "smooth", block: "start" });
    });
  });

  renderBestCities();
  renderExamples();
  renderQuickFromForm();
  renderAll();
  updateHeroPreview(computeRoommateBudget(readQuickInputs()), "quick");
})();
