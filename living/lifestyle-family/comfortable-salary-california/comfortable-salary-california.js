(function () {
  const CITIES = {
    los_angeles: { name: "Los Angeles, CA", col: 1.38, rent3br: 3600, mortgage3br: 4100, utilities: 450, daycare: 1850, insurance: 220, propTax: 680, transit: 780 },
    san_diego: { name: "San Diego, CA", col: 1.32, rent3br: 3200, mortgage3br: 3650, utilities: 420, daycare: 1700, insurance: 200, propTax: 620, transit: 750 },
    san_francisco: { name: "San Francisco, CA", col: 1.65, rent3br: 4500, mortgage3br: 5200, utilities: 480, daycare: 2200, insurance: 260, propTax: 900, transit: 520 },
    san_jose: { name: "San Jose, CA", col: 1.55, rent3br: 4200, mortgage3br: 4800, utilities: 460, daycare: 2100, insurance: 250, propTax: 850, transit: 720 },
    sacramento: { name: "Sacramento, CA", col: 1.08, rent3br: 2400, mortgage3br: 2750, utilities: 380, daycare: 1400, insurance: 180, propTax: 480, transit: 700 },
    fresno: { name: "Fresno, CA", col: 0.92, rent3br: 1950, mortgage3br: 2250, utilities: 350, daycare: 1100, insurance: 160, propTax: 380, transit: 680 },
    bakersfield: { name: "Bakersfield, CA", col: 0.88, rent3br: 1750, mortgage3br: 2050, utilities: 340, daycare: 950, insurance: 150, propTax: 350, transit: 660 },
    riverside: { name: "Riverside, CA", col: 1.02, rent3br: 2550, mortgage3br: 2900, utilities: 390, daycare: 1250, insurance: 175, propTax: 510, transit: 720 },
  };

  const COMPARE_KEYS = ["san_francisco", "los_angeles", "san_diego", "sacramento", "san_jose", "fresno"];
  const AFFORDABLE_KEYS = ["sacramento", "fresno", "bakersfield", "riverside"];
  const CA_TAX = 0.28;
  const PIE_COLORS = {
    housing: "#0f7b6c",
    transportation: "#3182ce",
    food: "#38a169",
    healthcare: "#627d98",
    childcare: "#2d6a9f",
    lifestyle: "#94a3b8",
  };

  const LIFESTYLES = {
    basic: { label: "Basic survival", multiplier: 0.78, savingsRate: 0.04, classLabel: "Essentials-focused", food: 780, lifestyle: 280 },
    stable: { label: "Stable", multiplier: 0.92, savingsRate: 0.08, classLabel: "Stable middle-class", food: 920, lifestyle: 420 },
    comfortable: { label: "Comfortable", multiplier: 1, savingsRate: 0.12, classLabel: "Comfortable middle-class", food: 1100, lifestyle: 650 },
    upper: { label: "Upper middle class", multiplier: 1.24, savingsRate: 0.18, classLabel: "Upper middle-class", food: 1380, lifestyle: 980 },
  };

  const FAMILY = {
    single: { label: "1 adult", housingMul: 0.52, foodMul: 0.48, transportMul: 0.62, childcareMul: 0, children: 0 },
    couple: { label: "Couple", housingMul: 0.72, foodMul: 0.72, transportMul: 0.82, childcareMul: 0, children: 0 },
    family3: { label: "Family of 3", housingMul: 0.88, foodMul: 0.9, transportMul: 0.92, childcareMul: 0.55, children: 1 },
    family4: { label: "Family of 4", housingMul: 1, foodMul: 1, transportMul: 1, childcareMul: 1, children: 2 },
    large: { label: "Large family (5+)", housingMul: 1.14, foodMul: 1.22, transportMul: 1.1, childcareMul: 1.35, children: 3 },
  };

  const HOUSING_TYPE = {
    apartment: { rentMul: 0.82, ownMul: 0.88 },
    townhome: { rentMul: 0.95, ownMul: 1 },
    single: { rentMul: 1, ownMul: 1 },
    luxury: { rentMul: 1.48, ownMul: 1.58 },
  };

  const HOUSING_STATUS = {
    rent: { mode: "rent", extra: 0 },
    mortgage: { mode: "own", extra: 180 },
    owned: { mode: "own", extra: -400 },
  };

  const CHILDCARE = {
    none: { mul: 0 },
    part: { mul: 0.42 },
    full: { mul: 1 },
    private: { mul: 1.75 },
  };

  const TRANSPORT = {
    one_car: { cost: 720 },
    two_cars: { cost: 1050 },
    transit: { cost: 380 },
    remote: { cost: 320 },
  };

  function fmtUSD(n) {
    return new Intl.NumberFormat("en-US", { style: "currency", currency: "USD", maximumFractionDigits: 0 }).format(n);
  }

  function fmtRange(low, high) {
    return fmtUSD(low) + "–" + fmtUSD(high);
  }

  function computeBudget(inputs) {
    const city = CITIES[inputs.city] || CITIES.san_diego;
    const lifestyle = LIFESTYLES[inputs.lifestyle] || LIFESTYLES.comfortable;
    const family = FAMILY[inputs.family] || FAMILY.family4;
    const housingType = HOUSING_TYPE[inputs.housingType] || HOUSING_TYPE.single;
    const housingStatus = HOUSING_STATUS[inputs.housingStatus] || HOUSING_STATUS.rent;
    const childcareCfg = CHILDCARE[inputs.childcare] || CHILDCARE.full;
    const transport = TRANSPORT[inputs.transport] || TRANSPORT.two_cars;

    let housingBase =
      (housingStatus.mode === "rent" ? city.rent3br * housingType.rentMul : city.mortgage3br * housingType.ownMul) *
      family.housingMul;
    housingBase += city.utilities * housingType.rentMul * family.housingMul * 0.85;
    if (housingStatus.mode === "own") {
      housingBase += (city.propTax + city.insurance) * housingType.ownMul * family.housingMul * 0.9;
    }
    housingBase += housingStatus.extra || 0;

    const childcarePerChild = city.daycare * lifestyle.multiplier * childcareCfg.mul;
    const childcare = Math.round(childcarePerChild * family.children * family.childcareMul);

    const food = Math.round(lifestyle.food * city.col * family.foodMul * lifestyle.multiplier);
    const transportation = Math.round(transport.cost * (city.transit / 750) * family.transportMul * lifestyle.multiplier);
    const healthcare = Math.round(620 * (0.9 + city.col * 0.12) * (0.55 + family.housingMul * 0.5));
    const lifestyleSpend = Math.round(lifestyle.lifestyle * city.col * lifestyle.multiplier);

    const essentials = housingBase + childcare + food + transportation + healthcare + lifestyleSpend;
    const savings = Math.round(essentials * lifestyle.savingsRate);
    const monthlyNeed = essentials + savings;
    const annualGross = Math.round((monthlyNeed * 12) / (1 - CA_TAX));

    const breakdown = [
      { key: "housing", label: "Housing", amount: Math.round(housingBase) },
      { key: "transportation", label: "Transportation", amount: transportation },
      { key: "food", label: "Food", amount: food },
      { key: "healthcare", label: "Healthcare", amount: healthcare },
      { key: "childcare", label: "Childcare", amount: childcare },
      { key: "lifestyle", label: "Lifestyle & other", amount: lifestyleSpend },
    ]
      .filter((b) => b.amount > 0)
      .map((b) => ({
        ...b,
        pct: essentials > 0 ? Math.round((b.amount / essentials) * 100) : 0,
      }));

    return {
      city,
      lifestyle,
      family,
      monthlyNeed,
      annualGross,
      low: Math.round(annualGross * 0.9),
      high: Math.round(annualGross * 1.1),
      savings,
      breakdown,
      essentials,
      housingBase: Math.round(housingBase),
    };
  }

  const els = {
    heroPreview: document.getElementById("ca-hero-preview"),
    quickResults: document.getElementById("ca-quick-results"),
    resultIncome: document.getElementById("ca-result-income"),
    resultIncomeHero: document.getElementById("ca-result-income-hero"),
    resultRangeHero: document.getElementById("ca-result-range-hero"),
    resultRange: document.getElementById("ca-result-range"),
    resultClass: document.getElementById("ca-result-class"),
    resultSavings: document.getElementById("ca-result-savings"),
    budgetList: document.getElementById("ca-budget-list"),
    pieChart: document.getElementById("ca-pie-chart"),
    pieLegend: document.getElementById("ca-pie-legend"),
    cityCompare: document.getElementById("ca-city-compare"),
    cityContext: document.getElementById("ca-city-context"),
    affordableGrid: document.getElementById("ca-affordable-grid"),
    housingNote: document.getElementById("ca-housing-note"),
    hundredK: document.getElementById("ca-100k-note"),
    familyCards: document.getElementById("ca-family-cards"),
    exampleCards: document.getElementById("ca-example-cards"),
    lifestyleActive: document.getElementById("ca-lifestyle-active"),
  };

  function readPlannerInputs() {
    return {
      city: document.getElementById("ca-city")?.value || "san_diego",
      lifestyle: document.querySelector("[data-ca-lifestyle].is-selected")?.dataset.caLifestyle || "comfortable",
      family: document.querySelector("[data-ca-family].is-selected")?.dataset.caFamily || "family4",
      housingType: document.getElementById("ca-housing-type")?.value || "single",
      housingStatus: document.getElementById("ca-housing-status")?.value || "rent",
      childcare: document.getElementById("ca-childcare")?.value || "full",
      transport: document.getElementById("ca-transport")?.value || "two_cars",
    };
  }

  function readQuickInputs() {
    return Object.assign({}, readPlannerInputs(), {
      city: document.getElementById("ca-quick-city")?.value || "san_diego",
      lifestyle: document.getElementById("ca-quick-lifestyle")?.value || "comfortable",
      family: document.getElementById("ca-quick-family")?.value || "family4",
      housingStatus: document.getElementById("ca-quick-housing")?.value || "rent",
      housingType: "single",
      childcare: document.getElementById("ca-quick-family")?.value === "single" || document.getElementById("ca-quick-family")?.value === "couple" ? "none" : "full",
    });
  }

  function housingStatusLabel(key) {
    return { rent: "Renting", mortgage: "Mortgage", owned: "Owned home" }[key] || key;
  }

  function syncQuickToPlanner(inputs) {
    const cityEl = document.getElementById("ca-city");
    const housingStatusEl = document.getElementById("ca-housing-status");
    if (cityEl) cityEl.value = inputs.city;
    if (housingStatusEl) housingStatusEl.value = inputs.housingStatus;
    document.querySelectorAll("[data-ca-lifestyle]").forEach((card) => {
      const on = card.dataset.caLifestyle === inputs.lifestyle;
      card.classList.toggle("is-selected", on);
      card.setAttribute("aria-pressed", on ? "true" : "false");
    });
    document.querySelectorAll("[data-ca-family]").forEach((card) => {
      const on = card.dataset.caFamily === inputs.family;
      card.classList.toggle("is-selected", on);
      card.setAttribute("aria-pressed", on ? "true" : "false");
    });
    const childcareEl = document.getElementById("ca-childcare");
    if (childcareEl) childcareEl.value = inputs.childcare;
  }

  function renderQuickResults(result, inputs, opts) {
    if (!els.quickResults) return;
    els.quickResults.innerHTML =
      '<p class="ca-quick-result-kicker">Your quick estimate</p>' +
      '<p class="ca-quick-result-label">Estimated comfortable salary</p>' +
      '<p class="ca-quick-result-range">' +
      fmtRange(result.low, result.high) +
      "</p>" +
      '<p class="ca-quick-result-unit">per year · gross, before CA tax</p>' +
      '<ul class="ca-quick-result-meta">' +
      "<li><span>City</span><strong>" +
      result.city.name +
      "</strong></li>" +
      "<li><span>Lifestyle</span><strong>" +
      result.lifestyle.label +
      "</strong></li>" +
      "<li><span>Household</span><strong>" +
      result.family.label +
      "</strong></li>" +
      "<li><span>Housing</span><strong>" +
      housingStatusLabel(inputs.housingStatus) +
      "</strong></li>" +
      "</ul>" +
      '<a class="ca-quick-result-link" href="#ca-planner">Fine-tune in full planner ↓</a>';
    if (opts && opts.pulse) {
      els.quickResults.classList.add("ca-quick-results--pulse");
      window.setTimeout(function () {
        els.quickResults.classList.remove("ca-quick-results--pulse");
      }, 900);
    }
  }

  function renderBudgetList(breakdown) {
    if (!els.budgetList) return;
    els.budgetList.innerHTML = breakdown
      .map(
        (b) =>
          '<div class="ca-budget-row ca-budget-row--' +
          b.key +
          '"><span class="ca-budget-label">' +
          b.label +
          '</span><span class="ca-budget-amt">' +
          fmtUSD(b.amount) +
          "</span></div>"
      )
      .join("");
  }

  function renderPie(breakdown) {
    if (!els.pieChart) return;
    let cursor = 0;
    const stops = breakdown
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
      .map(
        (b) =>
          '<span class="ca-pie-legend-item"><i style="background:' +
          PIE_COLORS[b.key] +
          '"></i>' +
          b.label +
          " <strong>" +
          b.pct +
          "%</strong></span>"
      )
      .join("");
  }

  function updateHeroPreview(result) {
    if (!els.heroPreview) return;
    const cityEl = els.heroPreview.querySelector("[data-ca-preview-city]");
    const lifestyleEl = els.heroPreview.querySelector("[data-ca-preview-lifestyle]");
    const incomeEl = els.heroPreview.querySelector("[data-ca-preview-income]");
    if (cityEl) cityEl.textContent = result.city.name;
    if (lifestyleEl) lifestyleEl.textContent = result.lifestyle.label;
    if (incomeEl) incomeEl.textContent = fmtUSD(result.annualGross) + "/year";
  }

  function updateSections(result, inputs) {
    if (els.cityContext) {
      els.cityContext.innerHTML =
        "<strong>Your selection:</strong> " +
        result.city.name +
        " · " +
        result.family.label +
        " · <strong>" +
        result.lifestyle.label +
        "</strong> lifestyle → modeled comfortable salary <strong>" +
        fmtUSD(result.annualGross) +
        "/year</strong> (~<strong>" +
        fmtUSD(Math.round(result.monthlyNeed)) +
        "/mo</strong> all-in including savings).";
    }
    if (els.lifestyleActive) {
      els.lifestyleActive.textContent = result.lifestyle.classLabel;
      document.querySelectorAll("[data-ca-lifestyle-band]").forEach((card) => {
        card.classList.toggle("is-active", card.getAttribute("data-ca-lifestyle-band") === inputs.lifestyle);
      });
    }
    if (els.housingNote) {
      els.housingNote.innerHTML =
        "<p>In <strong>" +
        result.city.name +
        "</strong>, modeled housing (rent/mortgage, utilities, insurance &amp; taxes where applicable): <strong>" +
        fmtUSD(result.housingBase) +
        "/mo</strong>. Typical 3-bedroom rent ~<strong>" +
        fmtUSD(result.city.rent3br) +
        "</strong>; mortgage ~<strong>" +
        fmtUSD(result.city.mortgage3br) +
        "</strong> before your down payment and rate.</p>" +
        "<ul class='ca-housing-list'>" +
        "<li>Utilities ~<strong>" +
        fmtUSD(result.city.utilities) +
        "/mo</strong></li>" +
        "<li>Home insurance ~<strong>" +
        fmtUSD(result.city.insurance) +
        "/mo</strong> (modeled)</li>" +
        "<li>Property tax ~<strong>" +
        fmtUSD(result.city.propTax) +
        "/mo</strong> (modeled for owners)</li>" +
        "</ul>";
    }
    if (els.hundredK) {
      const at100 = computeBudget(Object.assign({}, inputs, {}));
      const monthlyTakeHome100 = Math.round((100000 / 12) * (1 - CA_TAX));
      const gap = Math.round(at100.monthlyNeed - monthlyTakeHome100);
      const verdict =
        gap > 400
          ? "likely <strong>tight or below</strong> your modeled comfort line"
          : gap > 0
            ? "<strong>borderline</strong>—may work with careful budgeting"
            : "<strong>may work</strong> for your current settings";
      els.hundredK.innerHTML =
        "<p>At <strong>$100,000</strong> gross in <strong>" +
        result.city.name +
        "</strong> (~<strong>" +
        fmtUSD(monthlyTakeHome100) +
        "/mo</strong> take-home), a <strong>" +
        result.family.label +
        "</strong> household at <strong>" +
        result.lifestyle.label.toLowerCase() +
        "</strong> is " +
        verdict +
        ". Your planner targets ~<strong>" +
        fmtUSD(at100.monthlyNeed) +
        "/mo</strong> all-in vs ~<strong>" +
        fmtUSD(monthlyTakeHome100) +
        "/mo</strong> take-home—a gap of about <strong>" +
        fmtUSD(Math.max(0, gap)) +
        "/mo</strong> when costs run high.</p>" +
        "<p>Singles and couples without childcare often fare better on $100k; families in coastal metros usually need more. Compare cities below or open our <a href=\"/hourly-to-salary-after-tax#hourly-salary-form\">take-home calculator</a>.</p>";
    }
  }

  function renderFamilyCards(inputs) {
    if (!els.familyCards) return;
    const lifestyleLabel = (LIFESTYLES[inputs.lifestyle] || LIFESTYLES.comfortable).label;
    els.familyCards.innerHTML = Object.keys(FAMILY)
      .map((key) => {
        const r = computeBudget(Object.assign({}, inputs, { family: key }));
        const active = key === inputs.family ? " is-active" : "";
        return (
          '<button type="button" class="ca-family-card' +
          active +
          '" data-ca-family-pick="' +
          key +
          '"><h3>' +
          FAMILY[key].label +
          '</h3><p class="ca-family-card-salary">' +
          fmtUSD(r.annualGross) +
          '/yr</p><p class="ca-family-card-detail">' +
          lifestyleLabel +
          " · " +
          r.city.name +
          "</p></button>"
        );
      })
      .join("");
    els.familyCards.querySelectorAll("[data-ca-family-pick]").forEach((btn) => {
      btn.addEventListener("click", () => {
        const key = btn.getAttribute("data-ca-family-pick");
        document.querySelectorAll("[data-ca-family]").forEach((c) => {
          const on = c.dataset.caFamily === key;
          c.classList.toggle("is-selected", on);
          c.setAttribute("aria-pressed", on ? "true" : "false");
        });
        const quickFamily = document.getElementById("ca-quick-family");
        if (quickFamily) quickFamily.value = key;
        renderAll();
      });
    });
  }

  function renderExamples(inputs, result) {
    if (!els.exampleCards) return;
    const examples = [
      { city: "san_diego", family: "family4", lifestyle: "comfortable", income: 155000, title: "San Diego family of 4" },
      { city: "los_angeles", family: "couple", lifestyle: "stable", income: 120000, title: "Los Angeles couple" },
    ];
    let html =
      '<article class="ca-example-card ca-example-card--yours"><h3>Your settings · ' +
      result.city.name +
      '</h3><dl><div><dt>Comfort salary</dt><dd>' +
      fmtUSD(result.annualGross) +
      '</dd></div><div><dt>Household</dt><dd>' +
      result.family.label +
      '</dd></div><div><dt>Lifestyle</dt><dd>' +
      result.lifestyle.label +
      "</dd></div></dl></article>";
    examples.forEach((ex) => {
      if (ex.city === inputs.city && ex.family === inputs.family) return;
      const r = computeBudget(
        Object.assign({}, inputs, { city: ex.city, family: ex.family, lifestyle: ex.lifestyle })
      );
      html +=
        '<article class="ca-example-card"><h3>' +
        ex.title +
        '</h3><dl><div><dt>Combined income</dt><dd>' +
        fmtUSD(ex.income) +
        '</dd></div><div><dt>Modeled need</dt><dd>' +
        fmtUSD(r.annualGross) +
        '</dd></div><div><dt>Lifestyle</dt><dd>' +
        LIFESTYLES[ex.lifestyle].label +
        "</dd></div></dl></article>";
    });
    els.exampleCards.innerHTML = html;
  }

  function renderAffordableGrid(inputs) {
    if (!els.affordableGrid) return;
    els.affordableGrid.innerHTML = AFFORDABLE_KEYS.map((key) => {
      const r = computeBudget(Object.assign({}, inputs, { city: key }));
      return (
        '<article class="ca-affordable-card"><h3>' +
        r.city.name +
        '</h3><p class="ca-affordable-salary">' +
        fmtUSD(r.annualGross) +
        '/yr comfortable</p><p class="ca-affordable-detail">Rent ~' +
        fmtUSD(r.city.rent3br) +
        "/mo · " +
        r.family.label +
        "</p></article>"
      );
    }).join("");
  }

  function renderCityCompare(activeCity, inputs) {
    if (!els.cityCompare) return;
    els.cityCompare.innerHTML = COMPARE_KEYS.map((key) => {
      const r = computeBudget(Object.assign({}, inputs, { city: key }));
      const active = key === activeCity ? " is-active" : "";
      const tag =
        key === "san_francisco"
          ? "$220k+ typical for family comfort"
          : key === "los_angeles"
            ? "$160k+ for comfortable living"
            : key === "san_diego"
              ? "$145k+ estimated"
              : key === "sacramento"
                ? "Lower housing pressure"
                : "";
      return (
        '<button type="button" class="ca-city-card' +
        active +
        '" data-ca-compare-city="' +
        key +
        '"><h3>' +
        r.city.name +
        '</h3><p class="ca-city-card-income">' +
        fmtUSD(r.annualGross) +
        "/yr</p>" +
        (tag ? '<p class="ca-city-card-tag">' + tag + "</p>" : "") +
        '<p class="ca-city-card-detail">Housing ~' +
        fmtUSD(r.housingBase) +
        "/mo · Rent ~" +
        fmtUSD(r.city.rent3br) +
        "/mo</p></button>"
      );
    }).join("");
    els.cityCompare.querySelectorAll("[data-ca-compare-city]").forEach((btn) => {
      btn.addEventListener("click", () => {
        const city = btn.getAttribute("data-ca-compare-city");
        const cityEl = document.getElementById("ca-city");
        const quickCity = document.getElementById("ca-quick-city");
        if (cityEl) cityEl.value = city;
        if (quickCity) quickCity.value = city;
        renderAll();
      });
    });
  }

  function renderResults(result, inputs) {
    if (els.resultIncomeHero) els.resultIncomeHero.textContent = fmtRange(result.low, result.high);
    if (els.resultRangeHero)
      els.resultRangeHero.textContent = fmtUSD(result.annualGross) + "/year midpoint · " + result.lifestyle.classLabel;
    if (els.resultIncome) els.resultIncome.textContent = fmtUSD(result.annualGross) + "/year";
    if (els.resultRange) els.resultRange.textContent = fmtRange(result.low, result.high) + " typical range";
    if (els.resultClass) els.resultClass.textContent = result.lifestyle.classLabel;
    if (els.resultSavings) els.resultSavings.textContent = fmtUSD(result.savings) + "/month";
    renderBudgetList(result.breakdown);
    renderPie(result.breakdown);
    renderPieLegend(result.breakdown);
    updateHeroPreview(result);
    updateSections(result, inputs);
    renderFamilyCards(inputs);
    renderExamples(inputs, result);
    renderAffordableGrid(inputs);
  }

  function renderQuickFromForm(opts) {
    const inputs = readQuickInputs();
    const result = computeBudget(inputs);
    renderQuickResults(result, inputs, opts);
    updateHeroPreview(result);
    updateSections(result, inputs);
    renderCityCompare(inputs.city, inputs);
    return result;
  }

  function renderAll() {
    const inputs = readPlannerInputs();
    const result = computeBudget(inputs);
    renderResults(result, inputs);
    renderCityCompare(inputs.city, inputs);
  }

  document.querySelectorAll("[data-ca-lifestyle]").forEach((card) => {
    card.addEventListener("click", () => {
      document.querySelectorAll("[data-ca-lifestyle]").forEach((c) => {
        c.classList.remove("is-selected");
        c.setAttribute("aria-pressed", "false");
      });
      card.classList.add("is-selected");
      card.setAttribute("aria-pressed", "true");
      const ql = document.getElementById("ca-quick-lifestyle");
      if (ql) ql.value = card.dataset.caLifestyle;
      renderAll();
    });
  });

  document.querySelectorAll("[data-ca-family]").forEach((card) => {
    card.addEventListener("click", () => {
      document.querySelectorAll("[data-ca-family]").forEach((c) => {
        c.classList.remove("is-selected");
        c.setAttribute("aria-pressed", "false");
      });
      card.classList.add("is-selected");
      card.setAttribute("aria-pressed", "true");
      const qf = document.getElementById("ca-quick-family");
      if (qf) qf.value = card.dataset.caFamily;
      const childcareEl = document.getElementById("ca-childcare");
      if (childcareEl) {
        const noKids = card.dataset.caFamily === "single" || card.dataset.caFamily === "couple";
        childcareEl.value = noKids ? "none" : childcareEl.value === "none" ? "full" : childcareEl.value;
      }
      renderAll();
    });
  });

  ["ca-city", "ca-housing-type", "ca-housing-status", "ca-childcare", "ca-transport"].forEach((id) => {
    document.getElementById(id)?.addEventListener("change", renderAll);
  });

  document.getElementById("ca-quick-form")?.addEventListener("submit", (e) => {
    e.preventDefault();
    syncQuickToPlanner(readQuickInputs());
    renderAll();
    renderQuickFromForm({ pulse: true });
    els.quickResults?.scrollIntoView({ behavior: "smooth", block: "nearest" });
  });

  ["ca-quick-city", "ca-quick-lifestyle", "ca-quick-family", "ca-quick-housing"].forEach((id) => {
    document.getElementById(id)?.addEventListener("change", renderQuickFromForm);
  });

  document.querySelectorAll("[data-scroll-to]").forEach((btn) => {
    btn.addEventListener("click", () => {
      document.getElementById(btn.getAttribute("data-scroll-to"))?.scrollIntoView({ behavior: "smooth", block: "start" });
    });
  });

  renderQuickFromForm();
  renderAll();
})();
