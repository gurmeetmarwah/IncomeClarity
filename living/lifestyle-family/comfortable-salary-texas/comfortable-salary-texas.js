(function () {
  const CITIES = {
    dallas: { name: "Dallas, TX", col: 1, rent3br: 2150, mortgage3br: 2480, utilities: 410, daycare: 1150, insurance: 195, propTax: 780, carFactor: 1 },
    houston: { name: "Houston, TX", col: 1.02, rent3br: 2100, mortgage3br: 2420, utilities: 420, daycare: 1120, insurance: 210, propTax: 820, carFactor: 1.02 },
    austin: { name: "Austin, TX", col: 1.14, rent3br: 2550, mortgage3br: 2920, utilities: 400, daycare: 1280, insurance: 200, propTax: 760, carFactor: 0.95 },
    san_antonio: { name: "San Antonio, TX", col: 0.92, rent3br: 1850, mortgage3br: 2150, utilities: 390, daycare: 980, insurance: 175, propTax: 680, carFactor: 1 },
    fort_worth: { name: "Fort Worth, TX", col: 0.98, rent3br: 2000, mortgage3br: 2320, utilities: 405, daycare: 1080, insurance: 190, propTax: 740, carFactor: 1.02 },
    el_paso: { name: "El Paso, TX", col: 0.82, rent3br: 1550, mortgage3br: 1820, utilities: 360, daycare: 850, insurance: 165, propTax: 580, carFactor: 1.05 },
  };

  const COMPARE_KEYS = ["houston", "dallas", "austin", "san_antonio", "fort_worth", "el_paso"];
  const AFFORDABLE_KEYS = ["san_antonio", "el_paso", "fort_worth"];
  const TX_EFFECTIVE_TAX = 0.22;
  const PIE_COLORS = {
    housing: "#1e3a5f",
    property_tax: "#c45c4a",
    transportation: "#2b6cb0",
    food: "#38a169",
    healthcare: "#805ad5",
    childcare: "#d69e2e",
    lifestyle: "#718096",
  };

  const LIFESTYLES = {
    lean: { label: "Lean budget", multiplier: 0.8, savingsRate: 0.05, classLabel: "Lean household budget", food: 750, lifestyle: 300 },
    steady: { label: "Steady", multiplier: 0.94, savingsRate: 0.09, classLabel: "Steady Texas middle-class", food: 900, lifestyle: 480 },
    comfortable: { label: "Comfortable", multiplier: 1, savingsRate: 0.12, classLabel: "Comfortable Texas lifestyle", food: 1050, lifestyle: 620 },
    affluent: { label: "Affluent", multiplier: 1.2, savingsRate: 0.17, classLabel: "Affluent / upper tier", food: 1280, lifestyle: 900 },
  };

  const FAMILY = {
    single: { label: "Single adult", housingMul: 0.5, foodMul: 0.46, transportMul: 0.68, childcareMul: 0, children: 0 },
    couple: { label: "Couple (no kids)", housingMul: 0.7, foodMul: 0.7, transportMul: 0.85, childcareMul: 0, children: 0 },
    family3: { label: "Family of 3", housingMul: 0.86, foodMul: 0.88, transportMul: 0.94, childcareMul: 0.52, children: 1 },
    family4: { label: "Family of 4", housingMul: 1, foodMul: 1, transportMul: 1, childcareMul: 1, children: 2 },
    large: { label: "Large family (5+)", housingMul: 1.12, foodMul: 1.18, transportMul: 1.12, childcareMul: 1.3, children: 3 },
  };

  const HOUSING_TYPE = {
    apartment: { rentMul: 0.8, ownMul: 0.86 },
    townhome: { rentMul: 0.94, ownMul: 0.98 },
    single: { rentMul: 1, ownMul: 1 },
    luxury: { rentMul: 1.42, ownMul: 1.5 },
  };

  const HOUSING_STATUS = {
    rent: { mode: "rent", extra: 0 },
    mortgage: { mode: "own", extra: 120 },
    owned: { mode: "own", extra: -350 },
  };

  const CHILDCARE = {
    none: { mul: 0 },
    part: { mul: 0.4 },
    full: { mul: 1 },
    private: { mul: 1.65 },
  };

  const TRANSPORT = {
    one_car: { cost: 680 },
    two_cars: { cost: 980 },
    transit: { cost: 280 },
    remote: { cost: 300 },
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
    const family = FAMILY[inputs.family] || FAMILY.family4;
    const housingType = HOUSING_TYPE[inputs.housingType] || HOUSING_TYPE.single;
    const housingStatus = HOUSING_STATUS[inputs.housingStatus] || HOUSING_STATUS.rent;
    const childcareCfg = CHILDCARE[inputs.childcare] || CHILDCARE.full;
    const transport = TRANSPORT[inputs.transport] || TRANSPORT.two_cars;

    const rentOrMortgage =
      (housingStatus.mode === "rent" ? city.rent3br * housingType.rentMul : city.mortgage3br * housingType.ownMul) *
      family.housingMul;
    const utilities = city.utilities * housingType.rentMul * family.housingMul * 1.08;
    const insurance = housingStatus.mode === "own" ? city.insurance * housingType.ownMul * family.housingMul : city.insurance * 0.25;
    const propertyTax =
      housingStatus.mode === "own" ? city.propTax * housingType.ownMul * family.housingMul * 1.05 : 0;

    let housingBase = rentOrMortgage + utilities + insurance + propertyTax + (housingStatus.extra || 0);

    const childcarePerChild = city.daycare * lifestyle.multiplier * childcareCfg.mul;
    const childcare = Math.round(childcarePerChild * family.children * family.childcareMul);
    const food = Math.round(lifestyle.food * city.col * family.foodMul * lifestyle.multiplier);
    const transportation = Math.round(
      transport.cost * city.carFactor * family.transportMul * lifestyle.multiplier * (city.col * 0.25 + 0.85)
    );
    const healthcare = Math.round(560 * (0.88 + city.col * 0.1) * (0.52 + family.housingMul * 0.48));
    const lifestyleSpend = Math.round(lifestyle.lifestyle * city.col * lifestyle.multiplier);

    const essentials = housingBase + childcare + food + transportation + healthcare + lifestyleSpend;
    const savings = Math.round(essentials * lifestyle.savingsRate);
    const monthlyNeed = essentials + savings;
    const annualGross = Math.round((monthlyNeed * 12) / (1 - TX_EFFECTIVE_TAX));
    const monthlyTakeHome = Math.round((annualGross / 12) * (1 - TX_EFFECTIVE_TAX));

    const breakdown = [
      { key: "housing", label: "Rent / mortgage & utilities", amount: Math.round(rentOrMortgage + utilities + insurance) },
      { key: "property_tax", label: "Property tax (owners)", amount: Math.round(propertyTax) },
      { key: "transportation", label: "Cars & commute", amount: transportation },
      { key: "food", label: "Food & groceries", amount: food },
      { key: "healthcare", label: "Healthcare", amount: healthcare },
      { key: "childcare", label: "Childcare", amount: childcare },
      { key: "lifestyle", label: "Discretionary", amount: lifestyleSpend },
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
      monthlyTakeHome,
      low: Math.round(annualGross * 0.9),
      high: Math.round(annualGross * 1.1),
      savings,
      breakdown,
      essentials,
      housingBase: Math.round(housingBase),
      rentOrMortgage: Math.round(rentOrMortgage),
      propertyTax: Math.round(propertyTax),
      utilities: Math.round(utilities),
    };
  }

  const els = {
    heroPreview: document.getElementById("tx-hero-preview"),
    quickResults: document.getElementById("tx-quick-results"),
    resultIncome: document.getElementById("tx-result-income"),
    resultIncomeHero: document.getElementById("tx-result-income-hero"),
    resultRangeHero: document.getElementById("tx-result-range-hero"),
    resultRange: document.getElementById("tx-result-range"),
    resultTakehome: document.getElementById("tx-result-takehome"),
    resultClass: document.getElementById("tx-result-class"),
    resultSavings: document.getElementById("tx-result-savings"),
    budgetList: document.getElementById("tx-budget-list"),
    pieChart: document.getElementById("tx-pie-chart"),
    pieLegend: document.getElementById("tx-pie-legend"),
    cityCompare: document.getElementById("tx-city-compare"),
    cityContext: document.getElementById("tx-city-context"),
    taxNote: document.getElementById("tx-tax-note"),
    propTaxNote: document.getElementById("tx-proptax-note"),
    commuteNote: document.getElementById("tx-commute-note"),
    eightyK: document.getElementById("tx-80k-note"),
    vsCalifornia: document.getElementById("tx-vs-california"),
    affordableGrid: document.getElementById("tx-affordable-grid"),
    familyCards: document.getElementById("tx-family-cards"),
    exampleCards: document.getElementById("tx-example-cards"),
    lifestyleActive: document.getElementById("tx-lifestyle-active"),
  };

  function readPlannerInputs() {
    return {
      city: document.getElementById("tx-city")?.value || "dallas",
      lifestyle: document.querySelector("[data-tx-lifestyle].is-selected")?.dataset.txLifestyle || "comfortable",
      family: document.querySelector("[data-tx-family].is-selected")?.dataset.txFamily || "family4",
      housingType: document.getElementById("tx-housing-type")?.value || "single",
      housingStatus: document.getElementById("tx-housing-status")?.value || "rent",
      childcare: document.getElementById("tx-childcare")?.value || "full",
      transport: document.getElementById("tx-transport")?.value || "two_cars",
    };
  }

  function readQuickInputs() {
    const family = document.getElementById("tx-quick-family")?.value || "family4";
    return Object.assign({}, readPlannerInputs(), {
      city: document.getElementById("tx-quick-city")?.value || "dallas",
      lifestyle: document.getElementById("tx-quick-lifestyle")?.value || "comfortable",
      family: family,
      housingStatus: document.getElementById("tx-quick-housing")?.value || "rent",
      housingType: document.getElementById("tx-quick-housing-type")?.value || "single",
      childcare: family === "single" || family === "couple" ? "none" : "full",
    });
  }

  function housingStatusLabel(key) {
    return { rent: "Renting", mortgage: "Mortgage", owned: "Owned (paid off)" }[key] || key;
  }

  function syncQuickToPlanner(inputs) {
    const cityEl = document.getElementById("tx-city");
    const statusEl = document.getElementById("tx-housing-status");
    const typeEl = document.getElementById("tx-housing-type");
    if (cityEl) cityEl.value = inputs.city;
    if (statusEl) statusEl.value = inputs.housingStatus;
    if (typeEl) typeEl.value = inputs.housingType;
    document.querySelectorAll("[data-tx-lifestyle]").forEach((card) => {
      const on = card.dataset.txLifestyle === inputs.lifestyle;
      card.classList.toggle("is-selected", on);
      card.setAttribute("aria-pressed", on ? "true" : "false");
    });
    document.querySelectorAll("[data-tx-family]").forEach((card) => {
      const on = card.dataset.txFamily === inputs.family;
      card.classList.toggle("is-selected", on);
      card.setAttribute("aria-pressed", on ? "true" : "false");
    });
    const childcareEl = document.getElementById("tx-childcare");
    if (childcareEl) childcareEl.value = inputs.childcare;
  }

  function renderQuickResults(result, inputs, opts) {
    if (!els.quickResults) return;
    els.quickResults.innerHTML =
      '<p class="tx-quick-result-kicker">Texas quick estimate</p>' +
      '<p class="tx-quick-result-label">Gross salary for comfortable living</p>' +
      '<p class="tx-quick-result-range">' +
      fmtRange(result.low, result.high) +
      "</p>" +
      '<p class="tx-quick-result-unit">per year · no TX state income tax modeled</p>' +
      '<ul class="tx-quick-result-meta">' +
      "<li><span>Metro</span><strong>" +
      result.city.name +
      "</strong></li>" +
      "<li><span>Est. take-home</span><strong>" +
      fmtUSD(result.monthlyTakeHome) +
      "/mo</strong></li>" +
      "<li><span>Household</span><strong>" +
      result.family.label +
      "</strong></li>" +
      "<li><span>Lifestyle</span><strong>" +
      result.lifestyle.label +
      "</strong></li>" +
      "</ul>" +
      '<a class="tx-quick-result-link" href="#tx-planner">Open full Texas planner ↓</a>';
    if (opts && opts.pulse) {
      els.quickResults.classList.add("tx-quick-results--pulse");
      window.setTimeout(function () {
        els.quickResults.classList.remove("tx-quick-results--pulse");
      }, 900);
    }
  }

  function renderBudgetList(breakdown) {
    if (!els.budgetList) return;
    els.budgetList.innerHTML = breakdown
      .map(
        (b) =>
          '<div class="tx-budget-row tx-budget-row--' +
          b.key +
          '"><span class="tx-budget-label">' +
          b.label +
          '</span><span class="tx-budget-amt">' +
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
          '<span class="tx-pie-legend-item"><i style="background:' +
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
    const cityEl = els.heroPreview.querySelector("[data-tx-preview-city]");
    const lifestyleEl = els.heroPreview.querySelector("[data-tx-preview-lifestyle]");
    const incomeEl = els.heroPreview.querySelector("[data-tx-preview-income]");
    const takehomeEl = els.heroPreview.querySelector("[data-tx-preview-takehome]");
    if (cityEl) cityEl.textContent = result.city.name;
    if (lifestyleEl) lifestyleEl.textContent = result.lifestyle.label;
    if (incomeEl) incomeEl.textContent = fmtUSD(result.annualGross) + "/yr gross";
    if (takehomeEl) takehomeEl.textContent = fmtUSD(result.monthlyTakeHome) + "/mo take-home";
  }

  function updateSections(result, inputs) {
    if (els.cityContext) {
      els.cityContext.innerHTML =
        "<strong>" +
        result.city.name +
        "</strong> · " +
        result.family.label +
        " · <strong>" +
        result.lifestyle.label +
        "</strong> → about <strong>" +
        fmtUSD(result.annualGross) +
        "/year gross</strong> (<strong>" +
        fmtUSD(result.monthlyTakeHome) +
        "/mo</strong> estimated take-home with no state income tax).";
    }
    if (els.lifestyleActive) {
      els.lifestyleActive.textContent = result.lifestyle.classLabel;
      document.querySelectorAll("[data-tx-lifestyle-band]").forEach((card) => {
        card.classList.toggle("is-active", card.getAttribute("data-tx-lifestyle-band") === inputs.lifestyle);
      });
    }
    if (els.taxNote) {
      const caEquiv = Math.round(result.annualGross * 1.08);
      els.taxNote.innerHTML =
        "<p>Texas has <strong>no state income tax</strong> on wages. Our model uses ~<strong>22%</strong> effective federal + payroll withholding—so the same lifestyle often needs <strong>less gross</strong> than California, where state tax can push effective rates toward <strong>28%+</strong>.</p>" +
        "<p>At your settings, modeled gross <strong>" +
        fmtUSD(result.annualGross) +
        "</strong> in Texas might compare to roughly <strong>" +
        fmtUSD(caEquiv) +
        "+</strong> gross for a similar monthly budget in a high-tax state—illustrative only.</p>";
    }
    if (els.propTaxNote) {
      els.propTaxNote.innerHTML =
        "<p>Texas trades income tax for <strong>high property taxes</strong>. In <strong>" +
        result.city.name +
        "</strong>, modeled total housing <strong>" +
        fmtUSD(result.housingBase) +
        "/mo</strong> includes rent/mortgage <strong>" +
        fmtUSD(result.rentOrMortgage) +
        "</strong>, utilities <strong>" +
        fmtUSD(result.utilities) +
        "</strong>" +
        (result.propertyTax > 0
          ? ", and property tax <strong>" + fmtUSD(result.propertyTax) + "/mo</strong>"
          : " (property tax applies mainly to owners)") +
        ".</p><p>Typical 3BR rent ~<strong>" +
        fmtUSD(result.city.rent3br) +
        "</strong>; owner property tax benchmark ~<strong>" +
        fmtUSD(result.city.propTax) +
        "/mo</strong> before insurance and maintenance.</p>";
    }
    if (els.commuteNote) {
      els.commuteNote.innerHTML =
        "<p>Most Texas metros are <strong>car-dependent</strong>. Your model includes <strong>" +
        (inputs.transport === "two_cars" ? "two vehicles" : inputs.transport === "one_car" ? "one vehicle" : inputs.transport === "transit" ? "limited transit" : "remote / low commute") +
        "</strong>—insurance, fuel, and tolls add up fast in DFW, Houston, and Austin sprawl.</p>";
    }
    if (els.eightyK) {
      const monthlyTakeHome80 = Math.round((80000 / 12) * (1 - TX_EFFECTIVE_TAX));
      const gap = Math.round(result.monthlyNeed - monthlyTakeHome80);
      const verdict =
        gap > 350
          ? "likely <strong>below</strong> your comfortable budget line"
          : gap > 0
            ? "<strong>workable</strong> with tight discretionary spending"
            : "<strong>may cover</strong> your modeled comfort tier";
      els.eightyK.innerHTML =
        "<p><strong>$80,000</strong> gross in Texas (~<strong>" +
        fmtUSD(monthlyTakeHome80) +
        "/mo</strong> take-home) for a <strong>" +
        result.family.label +
        "</strong> in <strong>" +
        result.city.name +
        "</strong> is " +
        verdict +
        ". Planner target ~<strong>" +
        fmtUSD(result.monthlyNeed) +
        "/mo</strong> all-in; gap about <strong>" +
        fmtUSD(Math.max(0, gap)) +
        "/mo</strong> at these settings.</p>" +
        "<p>Singles in San Antonio or El Paso often stretch $80k further than families renting a 3-bedroom in Austin or Dallas.</p>";
    }
    if (els.vsCalifornia) {
      const caGross = Math.round(result.annualGross * 1.12);
      els.vsCalifornia.innerHTML =
        "<p>Same household settings modeled in Texas vs a typical California metro: Texas gross <strong>" +
        fmtUSD(result.annualGross) +
        "</strong> vs illustrative California need <strong>" +
        fmtUSD(caGross) +
        "+</strong>—mostly from state tax and higher coastal rent, not a guarantee.</p>" +
        '<p>See our <a href="/living/cost-of-living/cost-of-living-california-vs-texas.html">California vs Texas cost of living guide</a> or the <a href="/living/lifestyle-family/comfortable-salary-california">California comfortable salary planner</a> for side-by-side framing.</p>';
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
          '<button type="button" class="tx-family-card' +
          active +
          '" data-tx-family-pick="' +
          key +
          '"><h3>' +
          FAMILY[key].label +
          '</h3><p class="tx-family-card-salary">' +
          fmtUSD(r.annualGross) +
          '/yr</p><p class="tx-family-card-detail">' +
          lifestyleLabel +
          " · " +
          fmtUSD(r.monthlyTakeHome) +
          "/mo take-home</p></button>"
        );
      })
      .join("");
    els.familyCards.querySelectorAll("[data-tx-family-pick]").forEach((btn) => {
      btn.addEventListener("click", () => {
        const key = btn.getAttribute("data-tx-family-pick");
        document.querySelectorAll("[data-tx-family]").forEach((c) => {
          const on = c.dataset.txFamily === key;
          c.classList.toggle("is-selected", on);
          c.setAttribute("aria-pressed", on ? "true" : "false");
        });
        const qf = document.getElementById("tx-quick-family");
        if (qf) qf.value = key;
        renderAll();
      });
    });
  }

  function renderExamples(inputs, result) {
    if (!els.exampleCards) return;
    const examples = [
      { city: "dallas", family: "family4", lifestyle: "comfortable", income: 125000, title: "Dallas–Fort Worth family" },
      { city: "houston", family: "couple", lifestyle: "steady", income: 95000, title: "Houston couple" },
      { city: "austin", family: "family3", lifestyle: "comfortable", income: 140000, title: "Austin family of 3" },
    ];
    let html =
      '<article class="tx-example-card tx-example-card--yours"><h3>Your scenario · ' +
      result.city.name +
      '</h3><dl><div><dt>Modeled gross</dt><dd>' +
      fmtUSD(result.annualGross) +
      '</dd></div><div><dt>Est. take-home</dt><dd>' +
      fmtUSD(result.monthlyTakeHome) +
      '/mo</dd></div><div><dt>Household</dt><dd>' +
      result.family.label +
      "</dd></div></dl></article>";
    examples.forEach((ex) => {
      if (ex.city === inputs.city && ex.family === inputs.family) return;
      const r = computeBudget(
        Object.assign({}, inputs, { city: ex.city, family: ex.family, lifestyle: ex.lifestyle })
      );
      html +=
        '<article class="tx-example-card"><h3>' +
        ex.title +
        '</h3><dl><div><dt>Actual income</dt><dd>' +
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
        '<article class="tx-affordable-card"><h3>' +
        r.city.name +
        '</h3><p class="tx-affordable-salary">' +
        fmtUSD(r.annualGross) +
        '/yr gross</p><p class="tx-affordable-detail">Rent ~' +
        fmtUSD(r.city.rent3br) +
        "/mo · Take-home ~" +
        fmtUSD(r.monthlyTakeHome) +
        "/mo</p></article>"
      );
    }).join("");
  }

  function renderCityCompare(activeCity, inputs) {
    if (!els.cityCompare) return;
    const tags = {
      austin: "Fastest-growing — housing pressure",
      houston: "Large metro, varied neighborhoods",
      dallas: "DFW hub — strong job market",
      san_antonio: "Often lower rent than Austin",
      el_paso: "Among lowest TX modeled costs",
    };
    els.cityCompare.innerHTML = COMPARE_KEYS.map((key) => {
      const r = computeBudget(Object.assign({}, inputs, { city: key }));
      const active = key === activeCity ? " is-active" : "";
      return (
        '<button type="button" class="tx-city-card' +
        active +
        '" data-tx-compare-city="' +
        key +
        '"><h3>' +
        r.city.name +
        '</h3><p class="tx-city-card-income">' +
        fmtUSD(r.annualGross) +
        "/yr</p>" +
        (tags[key] ? '<p class="tx-city-card-tag">' + tags[key] + "</p>" : "") +
        '<p class="tx-city-card-detail">Take-home ~' +
        fmtUSD(r.monthlyTakeHome) +
        "/mo · Rent ~" +
        fmtUSD(r.city.rent3br) +
        "/mo</p></button>"
      );
    }).join("");
    els.cityCompare.querySelectorAll("[data-tx-compare-city]").forEach((btn) => {
      btn.addEventListener("click", () => {
        const city = btn.getAttribute("data-tx-compare-city");
        const cityEl = document.getElementById("tx-city");
        const quickCity = document.getElementById("tx-quick-city");
        if (cityEl) cityEl.value = city;
        if (quickCity) quickCity.value = city;
        renderAll();
      });
    });
  }

  function renderResults(result, inputs) {
    if (els.resultIncomeHero) els.resultIncomeHero.textContent = fmtRange(result.low, result.high);
    if (els.resultRangeHero)
      els.resultRangeHero.textContent =
        fmtUSD(result.annualGross) + "/yr · " + fmtUSD(result.monthlyTakeHome) + "/mo take-home";
    if (els.resultIncome) els.resultIncome.textContent = fmtUSD(result.annualGross) + "/year gross";
    if (els.resultRange) els.resultRange.textContent = fmtRange(result.low, result.high);
    if (els.resultTakehome) els.resultTakehome.textContent = fmtUSD(result.monthlyTakeHome) + "/month";
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

  document.querySelectorAll("[data-tx-lifestyle]").forEach((card) => {
    card.addEventListener("click", () => {
      document.querySelectorAll("[data-tx-lifestyle]").forEach((c) => {
        c.classList.remove("is-selected");
        c.setAttribute("aria-pressed", "false");
      });
      card.classList.add("is-selected");
      card.setAttribute("aria-pressed", "true");
      const ql = document.getElementById("tx-quick-lifestyle");
      if (ql) ql.value = card.dataset.txLifestyle;
      renderAll();
    });
  });

  document.querySelectorAll("[data-tx-family]").forEach((card) => {
    card.addEventListener("click", () => {
      document.querySelectorAll("[data-tx-family]").forEach((c) => {
        c.classList.remove("is-selected");
        c.setAttribute("aria-pressed", "false");
      });
      card.classList.add("is-selected");
      card.setAttribute("aria-pressed", "true");
      const qf = document.getElementById("tx-quick-family");
      if (qf) qf.value = card.dataset.txFamily;
      const childcareEl = document.getElementById("tx-childcare");
      if (childcareEl) {
        const noKids = card.dataset.txFamily === "single" || card.dataset.txFamily === "couple";
        childcareEl.value = noKids ? "none" : childcareEl.value === "none" ? "full" : childcareEl.value;
      }
      renderAll();
    });
  });

  ["tx-city", "tx-housing-type", "tx-housing-status", "tx-childcare", "tx-transport"].forEach((id) => {
    document.getElementById(id)?.addEventListener("change", renderAll);
  });

  document.getElementById("tx-quick-form")?.addEventListener("submit", (e) => {
    e.preventDefault();
    syncQuickToPlanner(readQuickInputs());
    renderAll();
    renderQuickFromForm({ pulse: true });
    els.quickResults?.scrollIntoView({ behavior: "smooth", block: "nearest" });
  });

  ["tx-quick-city", "tx-quick-lifestyle", "tx-quick-family", "tx-quick-housing", "tx-quick-housing-type"].forEach((id) => {
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
