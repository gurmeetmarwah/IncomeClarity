(function () {
  const CITIES = {
    dallas: { name: "Dallas, TX", col: 1, daycare: 1100, nanny: 3400, preschool: 900, afterschool: 500, au_pair: 1900, rent3br: 2100, tax: 0.22 },
    austin: { name: "Austin, TX", col: 1.14, daycare: 1250, nanny: 3800, preschool: 1050, afterschool: 580, au_pair: 2100, rent3br: 2450, tax: 0.22 },
    phoenix: { name: "Phoenix, AZ", col: 1.02, daycare: 1050, nanny: 3200, preschool: 880, afterschool: 520, au_pair: 1850, rent3br: 2050, tax: 0.23 },
    tampa: { name: "Tampa, FL", col: 1.04, daycare: 1150, nanny: 3300, preschool: 920, afterschool: 540, au_pair: 1950, rent3br: 2200, tax: 0.22 },
    atlanta: { name: "Atlanta, GA", col: 1.06, daycare: 1200, nanny: 3500, preschool: 950, afterschool: 560, au_pair: 2000, rent3br: 2150, tax: 0.23 },
    denver: { name: "Denver, CO", col: 1.18, daycare: 1400, nanny: 4200, preschool: 1100, afterschool: 620, au_pair: 2300, rent3br: 2650, tax: 0.24 },
    seattle: { name: "Seattle, WA", col: 1.35, daycare: 1650, nanny: 5200, preschool: 1280, afterschool: 720, au_pair: 2800, rent3br: 3200, tax: 0.25 },
    chicago: { name: "Chicago, IL", col: 1.12, daycare: 1350, nanny: 4000, preschool: 1050, afterschool: 600, au_pair: 2200, rent3br: 2400, tax: 0.25 },
    nyc: { name: "New York, NY", col: 1.55, daycare: 1900, nanny: 5800, preschool: 1500, afterschool: 850, au_pair: 3200, rent3br: 3800, tax: 0.29 },
  };

  const COMPARE_KEYS = ["dallas", "austin", "phoenix", "seattle"];
  const PIE_COLORS = {
    tuition: "#0f7b6c",
    meals: "#38a169",
    transport: "#3182ce",
    supplies: "#2d6a9f",
    fees: "#94a3b8",
  };

  const CARE_TYPES = {
    daycare_center: { label: "Daycare center", base: "daycare", mul: 1 },
    home_daycare: { label: "Home daycare", base: "daycare", mul: 0.88 },
    nanny: { label: "Nanny", base: "nanny", mul: 1 },
    au_pair: { label: "Au pair", base: "au_pair", mul: 1 },
    preschool: { label: "Preschool", base: "preschool", mul: 1 },
    afterschool: { label: "After-school care", base: "afterschool", mul: 1 },
  };

  const AGE_GROUPS = {
    infant: { label: "Infant", mul: 1.28 },
    toddler: { label: "Toddler", mul: 1.05 },
    preschool: { label: "Preschool", mul: 0.92 },
    school_age: { label: "School-age", mul: 0.78 },
  };

  const FREQUENCY = {
    full_time: { label: "Full-time", mul: 1 },
    part_time: { label: "Part-time", mul: 0.62 },
    three_day: { label: "3 days/week", mul: 0.72 },
    afterschool_only: { label: "After-school only", mul: 0.5 },
  };

  const HOUSING = {
    renting: { label: "Renting", housingMul: 1 },
    mortgage: { label: "Mortgage", housingMul: 1.05 },
    owned: { label: "Owned (no payment)", housingMul: 0.35 },
  };

  function fmtUSD(n) {
    return new Intl.NumberFormat("en-US", { style: "currency", currency: "USD", maximumFractionDigits: 0 }).format(n);
  }

  function fmtRange(low, high) {
    return fmtUSD(low) + "–" + fmtUSD(high);
  }

  function clamp(n, min, max) {
    return Math.min(max, Math.max(min, n));
  }

  function affordabilityLevel(pctGross) {
    if (pctGross < 10) return { label: "Comfortable", slug: "comfortable", desc: "Childcare is a manageable share of gross income." };
    if (pctGross < 20) return { label: "Moderate", slug: "moderate", desc: "Typical for many working families—watch other essentials." };
    if (pctGross < 30) return { label: "Financially tight", slug: "tight", desc: "Care costs may crowd out savings and flexibility." };
    return { label: "High burden", slug: "burden", desc: "Childcare is a major stress on the household budget." };
  }

  function perChildMonthly(city, careType, age, frequency) {
    const care = CARE_TYPES[careType] || CARE_TYPES.daycare_center;
    const ageMul = (AGE_GROUPS[age] || AGE_GROUPS.toddler).mul;
    const freq = FREQUENCY[frequency] || FREQUENCY.full_time;
    let base = city[care.base] || city.daycare;
    if (care.base === "daycare") base *= care.mul;
    if (careType === "afterschool" || frequency === "afterschool_only") {
      base = city.afterschool;
      return Math.round(base * city.col * (frequency === "afterschool_only" ? 1 : freq.mul));
    }
    return Math.round(base * ageMul * city.col * freq.mul);
  }

  function computeChildcare(inputs) {
    const city = CITIES[inputs.city] || CITIES.dallas;
    const children = clamp(Math.round(inputs.children), 1, 4);
    const income = clamp(inputs.income, 30000, 300000);
    const housing = HOUSING[inputs.housing] || HOUSING.renting;

    const childCosts = [];
    for (let i = 0; i < children; i++) {
      const age = inputs.ages[i] || inputs.age || "toddler";
      const sibMul = i === 0 ? 1 : i === 1 ? 0.96 : 0.92;
      childCosts.push(Math.round(perChildMonthly(city, inputs.careType, age, inputs.frequency) * sibMul));
    }

    const monthly = childCosts.reduce((s, c) => s + c, 0);
    const low = Math.round(monthly * 0.92);
    const high = Math.round(monthly * 1.1);
    const pctGross = income > 0 ? (monthly * 12 / income) * 100 : 0;
    const affordability = affordabilityLevel(pctGross);

    const monthlyTakeHome = Math.round((income / 12) * (1 - city.tax));
    const housingEst = Math.round(city.rent3br * housing.housingMul * 0.42);
    const otherEssentials = Math.round(1650 * city.col * (1 + (children - 1) * 0.12));
    const remaining = Math.max(0, monthlyTakeHome - monthly - housingEst - otherEssentials);

    const grossNeededComfort = Math.round((monthly * 12) / 0.1);
    const grossNeededModerate = Math.round((monthly * 12) / 0.2);

    const breakdown = [
      { key: "tuition", label: "Tuition / care", amount: Math.round(monthly * 0.85) },
      { key: "meals", label: "Meals", amount: Math.round(monthly * 0.05) },
      { key: "transport", label: "Transportation", amount: Math.round(monthly * 0.04) },
      { key: "supplies", label: "Supplies", amount: Math.round(monthly * 0.03) },
      { key: "fees", label: "Registration & fees", amount: Math.round(monthly * 0.03) },
    ].filter((b) => b.amount > 0);

    const essentials = breakdown.reduce((s, b) => s + b.amount, 0);
    breakdown.forEach((b) => {
      b.pct = essentials > 0 ? Math.round((b.amount / essentials) * 100) : 0;
    });

    const daycareCompare = Math.round(perChildMonthly(city, "daycare_center", inputs.age || "toddler", inputs.frequency) * children * 0.96);
    const nannyCompare = Math.round(perChildMonthly(city, "nanny", inputs.age || "toddler", inputs.frequency) * children * 0.96);

    return {
      city,
      children,
      income,
      monthly,
      low,
      high,
      pctGross,
      affordability,
      monthlyTakeHome,
      housingEst,
      otherEssentials,
      remaining,
      breakdown,
      childCosts,
      grossNeededComfort,
      grossNeededModerate,
      daycareCompare,
      nannyCompare,
      careLabel: (CARE_TYPES[inputs.careType] || CARE_TYPES.daycare_center).label,
      ageLabel: (AGE_GROUPS[inputs.age] || AGE_GROUPS.toddler).label,
    };
  }

  const els = {
    heroPreview: document.getElementById("cc-hero-preview"),
    quickResults: document.getElementById("cc-quick-results"),
    resultMonthly: document.getElementById("cc-result-monthly"),
    resultPct: document.getElementById("cc-result-pct"),
    resultAfford: document.getElementById("cc-result-afford"),
    resultRemaining: document.getElementById("cc-result-remaining"),
    budgetList: document.getElementById("cc-budget-list"),
    pieChart: document.getElementById("cc-pie-chart"),
    pieLegend: document.getElementById("cc-pie-legend"),
    cityCompare: document.getElementById("cc-city-compare"),
    compareDaycare: document.getElementById("cc-compare-daycare"),
    compareNanny: document.getElementById("cc-compare-nanny"),
    oneIncome: document.getElementById("cc-one-income-note"),
    budgetImpact: document.getElementById("cc-budget-impact-note"),
    salaryNote: document.getElementById("cc-salary-note"),
    exampleCards: document.getElementById("cc-example-cards"),
    cityContext: document.getElementById("cc-city-context"),
    affordContext: document.getElementById("cc-afford-context"),
    breakdownIntro: document.getElementById("cc-breakdown-intro"),
    examplesIntro: document.getElementById("cc-examples-intro"),
  };

  function readQuickInputs() {
    return {
      city: document.getElementById("cc-quick-city")?.value || "dallas",
      children: Number(document.getElementById("cc-quick-children")?.value) || 2,
      careType: document.getElementById("cc-quick-care")?.value || "daycare_center",
      income: Number(document.getElementById("cc-quick-income")?.value) || 100000,
      age: "toddler",
      ages: ["toddler", "toddler"],
      frequency: "full_time",
      housing: "renting",
    };
  }

  function readPlannerInputs() {
    const children = Number(document.querySelector("[data-cc-children].is-selected")?.dataset.ccChildren || 2);
    const age = document.querySelector("[data-cc-age].is-selected")?.dataset.ccAge || "toddler";
    const ages = [];
    for (let i = 0; i < children; i++) ages.push(i === 0 ? age : i === 1 ? "toddler" : "preschool");
    return {
      city: document.getElementById("cc-city")?.value || "dallas",
      children,
      careType: document.getElementById("cc-care-type")?.value || "daycare_center",
      frequency: document.getElementById("cc-frequency")?.value || "full_time",
      income: Number(document.getElementById("cc-income")?.value) || 100000,
      housing: document.getElementById("cc-housing")?.value || "renting",
      age,
      ages,
    };
  }

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
          '<span class="cc-pie-legend-item"><i style="background:' +
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
          '<div class="cc-budget-row cc-budget-row--' +
          b.key +
          '"><span>' +
          b.label +
          "</span><strong>" +
          fmtUSD(b.amount) +
          "</strong></div>"
      )
      .join("");
  }

  function updateHeroPreview(result) {
    if (!els.heroPreview) return;
    els.heroPreview.querySelector("[data-cc-preview-city]").textContent = result.city.name;
    els.heroPreview.querySelector("[data-cc-preview-cost]").textContent = fmtUSD(result.monthly) + "/mo";
    els.heroPreview.querySelector("[data-cc-preview-income]").textContent = fmtUSD(result.income) + "/yr";
    const aff = els.heroPreview.querySelector("[data-cc-preview-afford]");
    if (aff) {
      aff.textContent = result.affordability.label;
      aff.className = "cc-afford-badge cc-afford-badge--" + result.affordability.slug;
    }
  }

  function renderQuickResults(result, opts) {
    if (!els.quickResults) return;
    els.quickResults.innerHTML =
      '<p class="cc-quick-result-kicker">Your quick estimate</p>' +
      '<p class="cc-quick-result-label">Estimated childcare costs</p>' +
      '<p class="cc-quick-result-range">' +
      fmtRange(result.low, result.high) +
      "/month</p>" +
      '<p class="cc-quick-result-unit">' +
      result.children +
      " " +
      (result.children === 1 ? "child" : "children") +
      " · " +
      result.careLabel +
      " · " +
      result.city.name +
      "</p>" +
      '<p class="cc-quick-result-afford">Affordability: <strong class="cc-afford-badge cc-afford-badge--' +
      result.affordability.slug +
      '">' +
      result.affordability.label +
      "</strong></p>" +
      '<ul class="cc-quick-result-meta">' +
      "<li><span>% of household income</span><strong>" +
      result.pctGross.toFixed(1) +
      "%</strong></li>" +
      "<li><span>Est. remaining budget</span><strong>" +
      fmtUSD(result.remaining) +
      "/mo</strong></li>" +
      "</ul>" +
      '<a class="cc-quick-result-link" href="#cc-planner">Fine-tune in full planner ↓</a>';
    if (opts && opts.pulse) {
      els.quickResults.classList.add("cc-quick-results--pulse");
      window.setTimeout(function () {
        els.quickResults.classList.remove("cc-quick-results--pulse");
      }, 900);
    }
  }

  function renderResults(result) {
    if (els.resultMonthly) els.resultMonthly.textContent = fmtUSD(result.monthly) + "/month";
    if (els.resultPct) els.resultPct.textContent = result.pctGross.toFixed(1) + "% of household income";
    if (els.resultAfford) {
      els.resultAfford.textContent = result.affordability.label;
      els.resultAfford.className = "cc-afford-badge cc-afford-badge--" + result.affordability.slug;
    }
    if (els.resultRemaining) els.resultRemaining.textContent = fmtUSD(result.remaining) + "/month";
    renderBudgetList(result.breakdown);
    renderPie(result.breakdown);
    renderPieLegend(result.breakdown);
    updateHeroPreview(result);
    updateSections(result, readPlannerInputs());
    renderExamples(readPlannerInputs());
  }

  function updateAffordabilityBands(result) {
    document.querySelectorAll("[data-cc-band]").forEach((card) => {
      card.classList.toggle("is-active", card.getAttribute("data-cc-band") === result.affordability.slug);
    });
    if (els.affordContext) {
      els.affordContext.innerHTML =
        "<strong>Your selection (" +
        result.city.name +
        "):</strong> modeled childcare is <strong>" +
        fmtUSD(result.monthly) +
        "/month</strong> — about <strong>" +
        result.pctGross.toFixed(1) +
        "%</strong> of <strong>" +
        fmtUSD(result.income) +
        "</strong> gross income → <span class=\"cc-afford-badge cc-afford-badge--" +
        result.affordability.slug +
        "\">" +
        result.affordability.label +
        "</span>";
    }
  }

  function updateCityContext(result, inputs) {
    if (!els.cityContext) return;
    const infant = perChildMonthly(result.city, "daycare_center", "infant", inputs.frequency);
    const toddler = perChildMonthly(result.city, "daycare_center", "toddler", inputs.frequency);
    const nanny = perChildMonthly(result.city, "nanny", inputs.age || "toddler", inputs.frequency);
    els.cityContext.innerHTML =
      "<strong>Selected metro:</strong> " +
      result.city.name +
      " · Your modeled total <strong>" +
      fmtUSD(result.monthly) +
      "/mo</strong> (" +
      result.children +
      " " +
      (result.children === 1 ? "child" : "children") +
      ", " +
      result.careLabel +
      "). Typical benchmarks here: infant daycare ~<strong>" +
      fmtUSD(infant) +
      "/mo</strong>, toddler daycare ~<strong>" +
      fmtUSD(toddler) +
      "/mo</strong>, nanny ~<strong>" +
      fmtUSD(nanny) +
      "/mo</strong> per child (full-time).";
  }

  function updateSections(result, inputs) {
    updateAffordabilityBands(result);
    updateCityContext(result, inputs || readPlannerInputs());
    if (els.breakdownIntro) {
      els.breakdownIntro.textContent =
        "Monthly split for " +
        result.city.name +
        " at " +
        fmtUSD(result.monthly) +
        "/mo total—tuition dominates most families’ care line.";
    }
    if (els.examplesIntro) {
      els.examplesIntro.textContent =
        "First card reflects your current planner settings in " +
        result.city.name +
        ". Compare cards show other metros.";
    }
    if (els.compareDaycare) els.compareDaycare.textContent = fmtUSD(result.daycareCompare) + "/mo";
    if (els.compareNanny) els.compareNanny.textContent = fmtUSD(result.nannyCompare) + "/mo";
    if (els.oneIncome) {
      els.oneIncome.innerHTML =
        "<p>In <strong>" +
        result.city.name +
        "</strong>, full-time care for <strong>" +
        result.children +
        " " +
        (result.children === 1 ? "child" : "children") +
        "</strong> can run <strong>" +
        fmtUSD(result.monthly) +
        "/month</strong>—often close to a rent or mortgage line. At <strong>" +
        fmtUSD(result.income) +
        "</strong> gross, that is about <strong>" +
        result.pctGross.toFixed(0) +
        "%</strong> of income before food, housing, and savings.</p>";
    }
    if (els.budgetImpact) {
      els.budgetImpact.innerHTML =
        "<p>Modeled take-home: <strong>" +
        fmtUSD(result.monthlyTakeHome) +
        "/month</strong>. After childcare (<strong>" +
        fmtUSD(result.monthly) +
        "</strong>), housing (~<strong>" +
        fmtUSD(result.housingEst) +
        "</strong>), and other essentials (~<strong>" +
        fmtUSD(result.otherEssentials) +
        "</strong>), about <strong>" +
        fmtUSD(result.remaining) +
        "</strong> remains for savings, debt, and discretionary spending.</p>";
    }
    if (els.salaryNote) {
      els.salaryNote.innerHTML =
        "<p>For <strong>" +
        result.affordability.label.toLowerCase() +
        "</strong> affordability (under 10% of gross on care), household income near <strong>" +
        fmtUSD(result.grossNeededComfort) +
        "/year</strong> may be needed at these settings. For a <strong>moderate</strong> ~20% share, roughly <strong>" +
        fmtUSD(result.grossNeededModerate) +
        "/year</strong>. Compare with our <a href=\"/living/lifestyle-family/family-of-4-income-guide\">family of 4 income guide</a>.</p>";
    }
  }

  function renderCityCompare(activeCity, baseInputs) {
    if (!els.cityCompare) return;
    const base = baseInputs || readPlannerInputs();
    els.cityCompare.innerHTML = COMPARE_KEYS.map((key) => {
      const r = computeChildcare(Object.assign({}, base, { city: key }));
      const active = key === activeCity ? " is-active" : "";
      const infant = perChildMonthly(CITIES[key], "daycare_center", "infant", base.frequency);
      const nanny = perChildMonthly(CITIES[key], "nanny", base.age || "toddler", base.frequency);
      return (
        '<button type="button" class="cc-city-card' +
        active +
        '" data-cc-compare-city="' +
        key +
        '"><h3>' +
        r.city.name +
        '</h3><p class="cc-city-card-cost">' +
        fmtUSD(r.monthly) +
        '/mo total</p><p class="cc-city-card-detail">Infant daycare ~' +
        fmtUSD(infant) +
        '/mo</p><p class="cc-city-card-detail">Nanny ~' +
        fmtUSD(nanny) +
        "/mo</p></button>"
      );
    }).join("");
    els.cityCompare.querySelectorAll("[data-cc-compare-city]").forEach((btn) => {
      btn.addEventListener("click", () => {
        const city = btn.getAttribute("data-cc-compare-city");
        const cityEl = document.getElementById("cc-city");
        const quickCity = document.getElementById("cc-quick-city");
        if (cityEl) cityEl.value = city;
        if (quickCity) quickCity.value = city;
        renderAll();
      });
    });
  }

  function renderExampleCard(title, r, extra) {
    return (
      '<article class="cc-example-card' +
      (extra && extra.isYours ? " cc-example-card--yours" : "") +
      '"><h3>' +
      title +
      "</h3><dl><div><dt>Children</dt><dd>" +
      r.children +
      "</dd></div><div><dt>Care type</dt><dd>" +
      r.careLabel +
      '</dd></div><div><dt>Monthly childcare</dt><dd>' +
      fmtUSD(r.monthly) +
      "</dd></div><div><dt>% of income</dt><dd>" +
      r.pctGross.toFixed(1) +
      "%</dd></div></dl></article>"
    );
  }

  function renderExamples(inputs) {
    if (!els.exampleCards) return;
    const current = computeChildcare(inputs);
    const otherCities = COMPARE_KEYS.filter((k) => k !== inputs.city).slice(0, 2);
    const compareExamples = [
      { city: "dallas", children: 2, careType: "daycare_center", income: 110000, age: "toddler", label: "Dallas, TX" },
      { city: "phoenix", children: 1, careType: "home_daycare", income: 85000, age: "infant", label: "Phoenix, AZ" },
      { city: "seattle", children: 2, careType: "daycare_center", income: 145000, age: "toddler", label: "Seattle, WA" },
      { city: "austin", children: 2, careType: "daycare_center", income: 120000, age: "toddler", label: "Austin, TX" },
    ].filter((ex) => otherCities.indexOf(ex.city) !== -1);

    let html = renderExampleCard("Your settings · " + current.city.name, current, { isYours: true });
    compareExamples.forEach((ex) => {
      const r = computeChildcare(
        Object.assign({}, inputs, {
          city: ex.city,
          children: ex.children,
          careType: ex.careType,
          income: ex.income,
          age: ex.age,
          ages: Array.from({ length: ex.children }, (_, i) => (i === 0 ? ex.age : "toddler")),
          frequency: "full_time",
          housing: "renting",
        })
      );
      html += renderExampleCard(ex.label, r, null);
    });
    els.exampleCards.innerHTML = html;
  }

  function syncQuickToPlanner(inputs) {
    document.getElementById("cc-city").value = inputs.city;
    document.getElementById("cc-income").value = inputs.income;
    document.getElementById("cc-care-type").value = inputs.careType;
    document.querySelectorAll("[data-cc-children]").forEach((btn) => {
      const on = Number(btn.dataset.ccChildren) === inputs.children;
      btn.classList.toggle("is-selected", on);
      btn.setAttribute("aria-pressed", on ? "true" : "false");
    });
  }

  function selectCard(group, btn) {
    document.querySelectorAll("[data-" + group + "]").forEach((c) => {
      c.classList.remove("is-selected");
      c.setAttribute("aria-pressed", "false");
    });
    btn.classList.add("is-selected");
    btn.setAttribute("aria-pressed", "true");
  }

  function renderQuickFromForm(opts) {
    const inputs = readQuickInputs();
    const result = computeChildcare(inputs);
    renderQuickResults(result, opts);
    updateHeroPreview(result);
    updateSections(result, inputs);
    renderCityCompare(inputs.city, inputs);
    renderExamples(inputs);
    return result;
  }

  function renderAll() {
    const inputs = readPlannerInputs();
    const result = computeChildcare(inputs);
    renderResults(result);
    renderCityCompare(inputs.city, inputs);
    return result;
  }

  document.querySelectorAll("[data-cc-children]").forEach((btn) => {
    btn.addEventListener("click", () => {
      selectCard("cc-children", btn);
      renderAll();
    });
  });

  document.querySelectorAll("[data-cc-age]").forEach((btn) => {
    btn.addEventListener("click", () => {
      selectCard("cc-age", btn);
      renderAll();
    });
  });

  ["cc-city", "cc-care-type", "cc-frequency", "cc-income", "cc-housing"].forEach((id) => {
    const el = document.getElementById(id);
    el?.addEventListener("change", renderAll);
    el?.addEventListener("input", renderAll);
  });

  document.getElementById("cc-quick-form")?.addEventListener("submit", (e) => {
    e.preventDefault();
    syncQuickToPlanner(readQuickInputs());
    renderAll();
    renderQuickFromForm({ pulse: true });
    els.quickResults?.scrollIntoView({ behavior: "smooth", block: "nearest" });
  });

  ["cc-quick-city", "cc-quick-children", "cc-quick-care", "cc-quick-income"].forEach((id) => {
    document.getElementById(id)?.addEventListener("change", renderQuickFromForm);
    document.getElementById(id)?.addEventListener("input", renderQuickFromForm);
  });

  document.querySelectorAll("[data-scroll-to]").forEach((btn) => {
    btn.addEventListener("click", () => {
      document.getElementById(btn.getAttribute("data-scroll-to"))?.scrollIntoView({ behavior: "smooth", block: "start" });
    });
  });

  renderQuickFromForm();
  renderAll();
})();
