(function () {
  function fmtUSD(amount) {
    return new Intl.NumberFormat("en-US", {
      style: "currency",
      currency: "USD",
      maximumFractionDigits: 0
    }).format(amount);
  }

  function formatPayoffDuration(months) {
    if (!Number.isFinite(months) || months === Number.POSITIVE_INFINITY) {
      return "Will not pay off";
    }
    const years = Math.floor(months / 12);
    const remainingMonths = months % 12;
    if (years === 0) {
      return remainingMonths + " month" + (remainingMonths === 1 ? "" : "s");
    }
    if (remainingMonths === 0) {
      return years + " year" + (years === 1 ? "" : "s");
    }
    return years + " year" + (years === 1 ? "" : "s") + " " + remainingMonths + " month" + (remainingMonths === 1 ? "" : "s");
  }

  function monthlyInterest(balance, apr) {
    return balance * (apr / 100 / 12);
  }

  /**
   * Estimate issuer minimum for month 1.
   * method: "2pct" = max(floor, 2% balance)
   *         "1pct-plus-interest" = max(floor, 1% balance + interest)
   *         "3pct" = max(floor, 3% balance)
   */
  function methodMeta(method) {
    if (method === "1pct-plus-interest") {
      return {
        label: "1% of balance + interest",
        short: "1% + interest",
        note: "Many US issuers use a version of this—interest plus a slice of principal.",
      };
    }
    if (method === "3pct") {
      return {
        label: "3% of balance only",
        short: "3% of balance",
        note: "Simplified estimate. Does not add interest separately.",
      };
    }
    return {
      label: "2% of balance only",
      short: "2% of balance",
      note: "Simplified estimate. At high APR this can equal your monthly interest—so nothing pays down the balance.",
    };
  }

  function suggestMinimumPayment(balance, apr, method, floor) {
    const interest = monthlyInterest(balance, apr);
    var raw;
    if (method === "1pct-plus-interest") {
      raw = balance * 0.01 + interest;
    } else if (method === "3pct") {
      raw = balance * 0.03;
    } else {
      raw = balance * 0.02;
    }
    return Math.max(floor, Math.round(raw));
  }

  function analyzePaymentSplit(balance, apr, payment, method) {
    var interest = monthlyInterest(balance, apr);
    var principal = Math.max(0, payment - interest);
    var meta = methodMeta(method);
    var pctToInterest = payment > 0 ? Math.round((interest / payment) * 100) : 100;
    var pctToPrincipal = payment > 0 ? Math.max(0, 100 - pctToInterest) : 0;
    var coversInterest = payment > interest + 0.5;
    var breakEvenPayment = Math.ceil(interest + 1);
    var status;
    var headline;
    var detail;

    if (payment <= interest + 0.5) {
      status = "no-payoff";
      headline = "This estimated minimum only covers interest—not principal";
      detail =
        "Your estimated minimum (" +
        fmtUSD(payment) +
        ") is about the same as month-one interest (" +
        fmtUSD(interest) +
        "). With the <strong>" +
        meta.short +
        "</strong> formula at " +
        apr +
        "% APR, your balance would not shrink. Real card minimums vary—check your statement. To start paying down, you need at least <strong>" +
        fmtUSD(breakEvenPayment) +
        "/month</strong>.";
    } else if (principal < payment * 0.1) {
      status = "barely";
      headline = "Almost all of your minimum goes to interest";
      detail =
        "Only about <strong>" +
        fmtUSD(principal) +
        "</strong> of your " +
        fmtUSD(payment) +
        " payment hits principal in month one. The rest (~" +
        fmtUSD(interest) +
        ") is interest. Payoff is possible but very slow—paying <strong>" +
        fmtUSD(breakEvenPayment + 50) +
        "+/month</strong> changes the timeline dramatically.";
    } else {
      status = "slow";
      headline = "Your minimum pays some principal—but slowly";
      detail =
        "About <strong>" +
        pctToPrincipal +
        "%</strong> of your estimated minimum goes to principal in month one. That is better than interest-only, but minimums still stretch payoff over many years. See pay-more scenarios below.";
    }

    return {
      payment: payment,
      interest: interest,
      principal: principal,
      pctToInterest: Math.min(100, pctToInterest),
      pctToPrincipal: Math.max(0, pctToPrincipal),
      coversInterest: coversInterest,
      breakEvenPayment: breakEvenPayment,
      status: status,
      headline: headline,
      detail: detail,
      meta: meta,
    };
  }

  function buildSplitExplainerHTML(split) {
    var barPrincipal = split.pctToPrincipal;
    var barInterest = split.pctToInterest;
    if (split.status === "no-payoff") {
      barPrincipal = 0;
      barInterest = 100;
    }

    return (
      '<aside class="min-pay-split-explainer min-pay-split-explainer--' +
      split.status +
      '" role="note">' +
      '<p class="min-pay-split-explainer__title">' +
      split.headline +
      "</p>" +
      '<p class="min-pay-split-explainer__formula">Formula used: <strong>' +
      split.meta.label +
      "</strong>. " +
      split.meta.note +
      "</p>" +
      '<div class="min-pay-split-visual" aria-hidden="true">' +
      '<div class="min-pay-split-bar">' +
      (barPrincipal > 0
        ? '<span class="min-pay-split-bar__principal" style="width:' +
          Math.max(barPrincipal, 4) +
          '%">Principal ' +
          split.pctToPrincipal +
          "%</span>"
        : "") +
      '<span class="min-pay-split-bar__interest" style="width:' +
      Math.max(barInterest, barPrincipal > 0 ? barInterest : 100) +
      '%">Interest ' +
      split.pctToInterest +
      "%</span>" +
      "</div>" +
      '<p class="min-pay-split-visual__caption">Month-one split of your <strong>' +
      fmtUSD(split.payment || 0) +
      "</strong> payment</p>" +
      "</div>" +
      '<p class="min-pay-split-explainer__detail">' +
      split.detail +
      "</p>" +
      (split.status === "no-payoff"
        ? '<p class="min-pay-split-explainer__action">Try <strong>1% + interest</strong> in the dropdown if your issuer uses that formula, or use the <a href="/debt/credit-cards/credit-card-payoff-calculator#payoff">payoff calculator</a> with at least <strong>' +
          fmtUSD(split.breakEvenPayment) +
          "/month</strong>.</p>"
        : "") +
      "</aside>"
    );
  }

  function payoffPlanWithTimeline(balance, apr, payment) {
    var monthlyRate = apr / 100 / 12;
    var months = 0;
    var interestPaid = 0;
    var remaining = balance;
    var yearlyInterest = 0;
    var yearlyPrincipal = 0;
    var timeline = [];

    while (remaining > 0.01 && months < 1200) {
      var interest = remaining * monthlyRate;
      var principalPaid = Math.min(payment - interest, remaining);
      if (principalPaid <= 0) {
        return {
          months: Number.POSITIVE_INFINITY,
          interestPaid: Number.POSITIVE_INFINITY,
          timeline: timeline,
          payoffPossible: false
        };
      }
      remaining -= principalPaid;
      interestPaid += interest;
      yearlyInterest += interest;
      yearlyPrincipal += principalPaid;
      months += 1;

      if (months % 12 === 0 || remaining <= 0.01) {
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
      months: months,
      interestPaid: interestPaid,
      timeline: timeline,
      payoffPossible: true
    };
  }

  function buildWhatIfScenarios(balance, apr, payment) {
    return [50, 100, 200]
      .map(function (increment) {
        var newPayment = payment + increment;
        var scenarioPlan = payoffPlanWithTimeline(balance, apr, newPayment);
        return {
          increment: increment,
          newPayment: newPayment,
          months: scenarioPlan.months,
          interestPaid: scenarioPlan.interestPaid,
          payoffPossible: scenarioPlan.payoffPossible
        };
      })
      .filter(function (s) {
        return s.payoffPossible && Number.isFinite(s.months);
      });
  }

  function buildScenarioCardsHTML(balance, apr, minimum, minPlan, whatIfs) {
    var payoffDuration = minPlan.payoffPossible
      ? formatPayoffDuration(minPlan.months)
      : "Balance won\u2019t shrink";
    var interestLine = minPlan.payoffPossible ? fmtUSD(minPlan.interestPaid) : "Grows over time";

    var quote1 =
      "This is your estimated minimum—not a target. Most of each payment goes to interest at first.";
    if (!minPlan.payoffPossible) {
      quote1 =
        "With this formula, your payment (~" +
        fmtUSD(minimum) +
        ") matches month-one interest (~" +
        fmtUSD(monthlyInterest(balance, apr)) +
        ")—so nothing pays down the balance. Try <strong>1% + interest</strong> if that matches your card, or pay more.";
    } else if (minPlan.interestPaid > balance) {
      quote1 = "At this payment level, total interest can exceed what you originally borrowed.";
    }

    var firstLift = whatIfs[0];
    var card2Html;

    if (firstLift) {
      var monthsSaved = minPlan.payoffPossible ? minPlan.months - firstLift.months : null;
      var interestSaved =
        minPlan.payoffPossible ? minPlan.interestPaid - firstLift.interestPaid : null;
      var quote2 = "Same balance and APR—only the monthly payment changes.";
      if (monthsSaved !== null && monthsSaved > 0 && interestSaved !== null && interestSaved > 0) {
        quote2 =
          "You'd finish <strong>" +
          monthsSaved +
          " month" +
          (monthsSaved === 1 ? "" : "s") +
          " sooner</strong> and pay <strong>" +
          fmtUSD(interestSaved) +
          "</strong> less in interest.";
      }

      card2Html =
        '<article class="debt-minimum-card debt-minimum-card--lift">' +
        '<h3 class="debt-minimum-card-heading">' +
        '<span class="debt-minimum-label">Scenario 2</span>' +
        '<span class="debt-minimum-context">Minimum + ' +
        fmtUSD(firstLift.increment) +
        "/month</span>" +
        '<span class="debt-minimum-sum">' +
        fmtUSD(balance) +
        " balance · " +
        apr +
        "% APR</span>" +
        "</h3>" +
        '<dl class="debt-minimum-stats">' +
        "<div><dt>Monthly payment</dt><dd><strong>" +
        fmtUSD(firstLift.newPayment) +
        "/month</strong></dd></div>" +
        "<div><dt>Time to pay off</dt><dd><strong>" +
        formatPayoffDuration(firstLift.months) +
        "</strong></dd></div>" +
        "<div><dt>Total interest</dt><dd><strong>" +
        fmtUSD(firstLift.interestPaid) +
        "</strong></dd></div>" +
        "</dl>" +
        '<p class="debt-minimum-eq"><span class="debt-minimum-eq-quote">' +
        quote2 +
        "</span></p></article>";
    } else {
      card2Html =
        '<article class="debt-minimum-card">' +
        '<h3 class="debt-minimum-card-heading">' +
        '<span class="debt-minimum-label">Scenario 2</span>' +
        '<span class="debt-minimum-context">Pay more than the minimum</span>' +
        '<span class="debt-minimum-sum">' +
        fmtUSD(balance) +
        " balance · " +
        apr +
        "% APR</span>" +
        "</h3>" +
        '<dl class="debt-minimum-stats">' +
        "<div><dt>Tip</dt><dd><strong>Add $50–$100</strong> above your minimum to see payoff accelerate.</dd></div>" +
        "</dl>" +
        '<p class="debt-minimum-eq"><span class="debt-minimum-eq-quote">Try the <a href="/debt/credit-cards/credit-card-payoff-calculator#payoff">payoff calculator</a> with a fixed payment you can sustain.</span></p></article>';
    }

    var monthOneInterest = monthlyInterest(balance, apr);
    var principalShare = Math.max(0, minimum - monthOneInterest);

    return (
      '<article class="debt-minimum-card debt-minimum-card--min">' +
      '<h3 class="debt-minimum-card-heading">' +
      '<span class="debt-minimum-label">Your estimate</span>' +
      '<span class="debt-minimum-context">Paying only the suggested minimum</span>' +
      '<span class="debt-minimum-sum">' +
      fmtUSD(balance) +
      " balance · " +
      apr +
      "% APR</span>" +
      "</h3>" +
      '<dl class="debt-minimum-stats">' +
      "<div><dt>Suggested minimum</dt><dd><strong>" +
      fmtUSD(minimum) +
      "/month</strong></dd></div>" +
      "<div><dt>Month-one interest</dt><dd><strong>" +
      fmtUSD(monthOneInterest) +
      "</strong> <span class=\"debt-minimum-stat-detail\">(~" +
      fmtUSD(principalShare) +
      " to principal)</span></dd></div>" +
      "<div><dt>Time to pay off</dt><dd><strong>" +
      payoffDuration +
      "</strong></dd></div>" +
      "<div><dt>Total interest</dt><dd><strong>" +
      interestLine +
      "</strong></dd></div>" +
      "</dl>" +
      '<p class="debt-minimum-eq"><span class="debt-minimum-eq-quote">' +
      quote1 +
      "</span></p></article>" +
      card2Html
    );
  }

  var form = document.getElementById("min-pay-form");
  var resultPanel = document.getElementById("min-pay-result");
  var summaryPanel = document.getElementById("min-pay-summary");
  var outputShell = document.getElementById("min-pay-calc-output");
  var cardsRoot = document.getElementById("min-pay-cards-root");

  function runCalculation(options) {
    var shouldScroll = options && options.scroll;
    var balance = Number(document.getElementById("min-balance")?.value);
    var apr = Number(document.getElementById("min-apr")?.value);
    var method = document.getElementById("min-method")?.value || "1pct-plus-interest";
    var floor = Number(document.getElementById("min-floor")?.value) || 25;

    if (!balance || balance <= 0) return;

    var minimum = suggestMinimumPayment(balance, apr, method, floor);
    var split = analyzePaymentSplit(balance, apr, minimum, method);
    var minPlan = payoffPlanWithTimeline(balance, apr, minimum);
    var whatIfs = buildWhatIfScenarios(balance, apr, minimum);

    outputShell?.classList.add("min-pay-calc-output--active");

    var payoffLine = minPlan.payoffPossible
      ? "Payoff in <strong>" +
        formatPayoffDuration(minPlan.months) +
        "</strong> · Total interest <strong>" +
        fmtUSD(minPlan.interestPaid) +
        "</strong>"
      : '<strong class="min-pay-no-payoff-label">Balance won\u2019t shrink</strong> at this payment · Need at least <strong>' +
        fmtUSD(split.breakEvenPayment) +
        "/month</strong> to pay principal";

    if (summaryPanel) {
      summaryPanel.innerHTML =
        '<div class="min-pay-result-head" role="status">' +
        '<p class="min-pay-result-kicker">Estimated minimum payment</p>' +
        '<p class="min-pay-result-amount">' +
        fmtUSD(minimum) +
        '<span>/month</span></p>' +
        '<p class="min-pay-result-sub">' +
        payoffLine +
        "</p>" +
        '<p class="min-pay-result-detail">Month-one interest: <strong>' +
        fmtUSD(split.interest) +
        "</strong> · To principal: <strong>" +
        fmtUSD(split.principal) +
        "</strong></p></div>" +
        buildSplitExplainerHTML(split);
    }

    if (cardsRoot) {
      cardsRoot.innerHTML = buildScenarioCardsHTML(balance, apr, minimum, minPlan, whatIfs);
    }

    var whatIfHtml = whatIfs
      .map(function (scenario) {
        var monthsSaved =
          minPlan.payoffPossible && Number.isFinite(minPlan.months)
            ? minPlan.months - scenario.months
            : null;
        var interestSaved = minPlan.payoffPossible
          ? minPlan.interestPaid - scenario.interestPaid
          : null;
        var saveLine =
          monthsSaved !== null && monthsSaved > 0
            ? "You save <strong>" +
              monthsSaved +
              " month" +
              (monthsSaved === 1 ? "" : "s") +
              "</strong>" +
              (interestSaved !== null && interestSaved > 0
                ? " and <strong>" + fmtUSD(interestSaved) + "</strong> in interest."
                : ".")
            : "Compared with paying only the estimated minimum.";

        return (
          '<article class="what-if-card">' +
          "<h3>Pay " +
          fmtUSD(scenario.newPayment) +
          "/month (+" +
          fmtUSD(scenario.increment) +
          ")</h3>" +
          "<p>Debt-free in <strong>" +
          formatPayoffDuration(scenario.months) +
          "</strong></p>" +
          "<p>Interest paid: <strong>" +
          fmtUSD(scenario.interestPaid) +
          "</strong></p>" +
          "<p>" +
          saveLine +
          "</p></article>"
        );
      })
      .join("");

    var warnings = "";
    if (!minPlan.payoffPossible) {
      warnings +=
        '<p class="debt-result-warning"><strong>Why no payoff timeline?</strong> With the <em>' +
        split.meta.short +
        "</em> formula, your estimated minimum (" +
        fmtUSD(minimum) +
        ") does not exceed month-one interest (" +
        fmtUSD(split.interest) +
        "). The calculator cannot project a payoff because the balance would not shrink. This is common with <strong>2% of balance only</strong> at high APR—not a bug. Switch to <strong>1% + interest</strong> if that matches your card, or enter a higher fixed payment in the <a href=\"/debt/credit-cards/credit-card-payoff-calculator#payoff\">payoff calculator</a>.</p>";
    } else if (minPlan.interestPaid > balance) {
      warnings +=
        '<p class="debt-result-warning">Paying only this minimum level, total interest can exceed your original balance.</p>';
    }

    var timelineHtml = "";
    if (minPlan.payoffPossible && minPlan.timeline.length) {
      var maxYearlyPayment = Math.max.apply(
        null,
        minPlan.timeline.map(function (row) {
          return row.principalPaid + row.interestPaid;
        }).concat([1])
      );
      var maxEndingBalance = Math.max.apply(
        null,
        minPlan.timeline.map(function (row) {
          return row.endingBalance;
        }).concat([1])
      );

      timelineHtml =
        '<h3 id="min-pay-result-heading" class="debt-timeline-heading">Year-by-year at minimum payment</h3>' +
        '<div class="debt-timeline-wrap">' +
        minPlan.timeline
          .map(function (row) {
            var yearlyTotalPaid = row.principalPaid + row.interestPaid;
            var paidWidth = (yearlyTotalPaid / maxYearlyPayment) * 100;
            var interestShare =
              yearlyTotalPaid > 0 ? (row.interestPaid / yearlyTotalPaid) * 100 : 0;
            var principalShare = 100 - interestShare;
            var balanceWidth = (row.endingBalance / maxEndingBalance) * 100;
            return (
              '<article class="debt-timeline-item">' +
              '<div class="debt-timeline-head"><strong>Year ' +
              row.year +
              "</strong><span>Ending balance: " +
              fmtUSD(row.endingBalance) +
              "</span></div>" +
              '<div class="debt-timeline-metrics">' +
              "<span>Principal: " +
              fmtUSD(row.principalPaid) +
              "</span>" +
              "<span>Interest: " +
              fmtUSD(row.interestPaid) +
              "</span>" +
              "<span>Total paid: " +
              fmtUSD(yearlyTotalPaid) +
              "</span></div>" +
              '<div class="debt-timeline-bar" aria-hidden="true">' +
              '<div class="debt-timeline-bar-fill" style="width:' +
              Math.max(paidWidth, 6).toFixed(1) +
              '%">' +
              '<span class="debt-principal-fill" style="width:' +
              Math.max(principalShare, 2).toFixed(1) +
              '%"></span>' +
              '<span class="debt-interest-fill" style="width:' +
              Math.max(interestShare, 2).toFixed(1) +
              '%"></span></div></div>' +
              '<div class="debt-timeline-balance" aria-hidden="true">' +
              '<span style="width:' +
              Math.max(balanceWidth, row.endingBalance > 0 ? 4 : 0).toFixed(1) +
              '%"></span></div></article>'
            );
          })
          .join("") +
        "</div>";
    }

    if (resultPanel) {
      resultPanel.innerHTML =
        warnings +
        timelineHtml +
        '<h2 class="what-if-title">What if you paid more than the minimum?</h2>' +
        '<div class="what-if-grid">' +
        (whatIfHtml ||
          '<p>Add $50 or more above your estimated minimum to see faster payoff paths in the <a href="/debt/credit-cards/credit-card-payoff-calculator#payoff">payoff calculator</a>.</p>') +
        "</div>";
    }

    if (shouldScroll) {
      resultPanel?.focus({ preventScroll: true });
      outputShell?.scrollIntoView({ behavior: "smooth", block: "nearest" });
    }
  }

  var methodSelect = document.getElementById("min-method");
  var methodHint = document.getElementById("min-method-hint");

  function updateMethodHint() {
    if (!methodHint || !methodSelect) return;
    var meta = methodMeta(methodSelect.value);
    methodHint.textContent = meta.note;
  }

  methodSelect?.addEventListener("change", function () {
    updateMethodHint();
    runCalculation();
  });

  form?.addEventListener("submit", function (event) {
    event.preventDefault();
    runCalculation({ scroll: true });
  });

  updateMethodHint();
  runCalculation();
})();
