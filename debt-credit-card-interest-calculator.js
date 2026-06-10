(function () {
  function fmtUSD(amount) {
    return new Intl.NumberFormat("en-US", {
      style: "currency",
      currency: "USD",
      maximumFractionDigits: 0,
    }).format(amount);
  }

  function fmtUSDPrecise(amount) {
    return new Intl.NumberFormat("en-US", {
      style: "currency",
      currency: "USD",
      minimumFractionDigits: 2,
      maximumFractionDigits: 2,
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
    return (
      years +
      " year" +
      (years === 1 ? "" : "s") +
      " " +
      remainingMonths +
      " month" +
      (remainingMonths === 1 ? "" : "s")
    );
  }

  function monthlyInterest(balance, apr) {
    return balance * (apr / 100 / 12);
  }

  function dailyInterest(balance, apr) {
    return balance * (apr / 100 / 365);
  }

  function analyzeInterestSplit(balance, apr, payment) {
    var interest = monthlyInterest(balance, apr);
    var daily = dailyInterest(balance, apr);
    var principal = Math.max(0, payment - interest);
    var pctToInterest = payment > 0 ? Math.round((interest / payment) * 100) : 100;
    var pctToPrincipal = payment > 0 ? Math.max(0, 100 - pctToInterest) : 0;
    var breakEvenPayment = Math.ceil(interest + 1);
    var status;
    var headline;
    var detail;

    if (payment <= interest + 0.5) {
      status = "no-payoff";
      headline = "Your payment does not cover interest—the balance grows";
      detail =
        "Month-one interest is <strong>" +
        fmtUSD(interest) +
        "</strong> (~" +
        fmtUSDPrecise(daily) +
        "/day), but you are paying <strong>" +
        fmtUSD(payment) +
        "</strong>. The unpaid interest gets added to your balance, so next month's interest charge is higher. You need at least <strong>" +
        fmtUSD(breakEvenPayment) +
        "/month</strong> to start paying down principal.";
    } else if (principal < payment * 0.1) {
      status = "barely";
      headline = "Almost all of your payment is interest";
      detail =
        "Of your <strong>" +
        fmtUSD(payment) +
        "</strong> payment, about <strong>" +
        fmtUSD(interest) +
        "</strong> (" +
        pctToInterest +
        "%) goes to interest and only <strong>" +
        fmtUSD(principal) +
        "</strong> hits principal in month one. At " +
        apr +
        "% APR on " +
        fmtUSD(balance) +
        ", interest costs dominate until you pay more.";
    } else {
      status = "slow";
      headline = "Some of your payment fights the balance—but interest still takes a big share";
      detail =
        "About <strong>" +
        pctToInterest +
        "%</strong> of your payment covers interest in month one (~" +
        fmtUSDPrecise(daily) +
        "/day). The rest reduces principal. Total interest over the full payoff still depends on how long you keep this payment—see the scenarios below.";
    }

    return {
      payment: payment,
      interest: interest,
      daily: daily,
      principal: principal,
      pctToInterest: Math.min(100, pctToInterest),
      pctToPrincipal: Math.max(0, pctToPrincipal),
      breakEvenPayment: breakEvenPayment,
      status: status,
      headline: headline,
      detail: detail,
    };
  }

  function buildInterestExplainerHTML(split) {
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
      '<p class="min-pay-split-explainer__formula">Daily interest on this balance: <strong>' +
      fmtUSDPrecise(split.daily) +
      "/day</strong> · Monthly interest charge: <strong>" +
      fmtUSD(split.interest) +
      "</strong></p>" +
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
      fmtUSD(split.payment) +
      "</strong> payment</p>" +
      "</div>" +
      '<p class="min-pay-split-explainer__detail">' +
      split.detail +
      "</p>" +
      (split.status === "no-payoff"
        ? '<p class="min-pay-split-explainer__action">Raise your monthly payment to at least <strong>' +
          fmtUSD(split.breakEvenPayment) +
          '</strong>, or use the <a href="/debt/credit-cards/minimum-payment-calculator">minimum payment calculator</a> to see how issuer minimums compare.</p>'
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
          payoffPossible: false,
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
          endingBalance: Math.max(0, remaining),
        });
        yearlyInterest = 0;
        yearlyPrincipal = 0;
      }
    }

    return {
      months: months,
      interestPaid: interestPaid,
      timeline: timeline,
      payoffPossible: true,
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
          payoffPossible: scenarioPlan.payoffPossible,
        };
      })
      .filter(function (s) {
        return s.payoffPossible && Number.isFinite(s.months);
      });
  }

  function buildScenarioCardsHTML(balance, apr, payment, plan, whatIfs, split) {
    var payoffDuration = plan.payoffPossible
      ? formatPayoffDuration(plan.months)
      : "Balance won\u2019t shrink";
    var interestLine = plan.payoffPossible ? fmtUSD(plan.interestPaid) : "Grows over time";

    var quote1 =
      "At " +
      apr +
      "% APR, you would pay <strong>" +
      interestLine +
      "</strong> in total interest while clearing " +
      fmtUSD(balance) +
      " at " +
      fmtUSD(payment) +
      "/month.";
    if (!plan.payoffPossible) {
      quote1 =
        "Paying <strong>" +
        fmtUSD(payment) +
        "/month</strong> does not beat month-one interest (<strong>" +
        fmtUSD(split.interest) +
        "</strong>). Your balance—and future interest—keep climbing.";
    } else if (plan.interestPaid > balance) {
      quote1 =
        "Total interest (<strong>" +
        fmtUSD(plan.interestPaid) +
        "</strong>) exceeds your starting balance. A higher payment cuts this sharply.";
    }

    var firstLift = whatIfs[0];
    var card2Html;

    if (firstLift) {
      var interestSaved =
        plan.payoffPossible ? plan.interestPaid - firstLift.interestPaid : null;
      var quote2 = "Same balance and APR—only the monthly payment changes.";
      if (interestSaved !== null && interestSaved > 0) {
        quote2 =
          "Pay <strong>" +
          fmtUSD(firstLift.newPayment) +
          "/month</strong> instead and save <strong>" +
          fmtUSD(interestSaved) +
          "</strong> in total interest" +
          (plan.payoffPossible
            ? " while finishing <strong>" +
              formatPayoffDuration(plan.months - firstLift.months) +
              " sooner</strong>."
            : ".");
      }

      card2Html =
        '<article class="debt-minimum-card debt-minimum-card--lift">' +
        '<h3 class="debt-minimum-card-heading">' +
        '<span class="debt-minimum-label">Scenario 2</span>' +
        '<span class="debt-minimum-context">+' +
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
        "<div><dt>Total interest</dt><dd><strong>" +
        fmtUSD(firstLift.interestPaid) +
        "</strong></dd></div>" +
        "<div><dt>Time to pay off</dt><dd><strong>" +
        formatPayoffDuration(firstLift.months) +
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
        '<span class="debt-minimum-context">Pay more to cut interest</span>' +
        '<span class="debt-minimum-sum">' +
        fmtUSD(balance) +
        " balance · " +
        apr +
        "% APR</span>" +
        "</h3>" +
        '<dl class="debt-minimum-stats">' +
        "<div><dt>Tip</dt><dd><strong>Add $50–$100</strong> above your current payment to see interest drop fast.</dd></div>" +
        "</dl>" +
        '<p class="debt-minimum-eq"><span class="debt-minimum-eq-quote">Try the <a href="/debt/credit-cards/credit-card-payoff-calculator#payoff">payoff calculator</a> with a payment above month-one interest.</span></p></article>';
    }

    return (
      '<article class="debt-minimum-card debt-minimum-card--interest">' +
      '<h3 class="debt-minimum-card-heading">' +
      '<span class="debt-minimum-label">Your numbers</span>' +
      '<span class="debt-minimum-context">Paying ' +
      fmtUSD(payment) +
      "/month</span>" +
      '<span class="debt-minimum-sum">' +
      fmtUSD(balance) +
      " balance · " +
      apr +
      "% APR</span>" +
      "</h3>" +
      '<dl class="debt-minimum-stats">' +
      "<div><dt>Month-one interest</dt><dd><strong>" +
      fmtUSD(split.interest) +
      "</strong> <span class=\"debt-minimum-stat-detail\">(~" +
      fmtUSDPrecise(split.daily) +
      "/day)</span></dd></div>" +
      "<div><dt>Total interest</dt><dd><strong>" +
      interestLine +
      "</strong></dd></div>" +
      "<div><dt>Time to pay off</dt><dd><strong>" +
      payoffDuration +
      "</strong></dd></div>" +
      "</dl>" +
      '<p class="debt-minimum-eq"><span class="debt-minimum-eq-quote">' +
      quote1 +
      "</span></p></article>" +
      card2Html
    );
  }

  var form = document.getElementById("cc-int-form");
  var resultPanel = document.getElementById("cc-int-result");
  var summaryPanel = document.getElementById("cc-int-summary");
  var outputShell = document.getElementById("cc-int-calc-output");
  var cardsRoot = document.getElementById("cc-int-cards-root");

  function runCalculation() {
    var balance = Number(document.getElementById("cc-int-balance")?.value);
    var apr = Number(document.getElementById("cc-int-apr")?.value);
    var payment = Number(document.getElementById("cc-int-payment")?.value);

    if (!balance || balance <= 0 || !payment || payment <= 0) return;

    var split = analyzeInterestSplit(balance, apr, payment);
    var plan = payoffPlanWithTimeline(balance, apr, payment);
    var whatIfs = buildWhatIfScenarios(balance, apr, payment);

    outputShell?.classList.add("min-pay-calc-output--active");

    var payoffLine = plan.payoffPossible
      ? "Total interest <strong>" +
        fmtUSD(plan.interestPaid) +
        "</strong> · Paid off in <strong>" +
        formatPayoffDuration(plan.months) +
        "</strong>"
      : '<strong class="min-pay-no-payoff-label">Interest keeps compounding</strong> · Need at least <strong>' +
        fmtUSD(split.breakEvenPayment) +
        "/month</strong> to shrink balance";

    if (summaryPanel) {
      summaryPanel.innerHTML =
        '<div class="min-pay-result-head cc-int-result-head" role="status">' +
        '<p class="min-pay-result-kicker cc-int-result-kicker">Month-one interest charge</p>' +
        '<p class="min-pay-result-amount cc-int-result-amount">' +
        fmtUSD(split.interest) +
        '<span>/month</span></p>' +
        '<p class="min-pay-result-sub">' +
        payoffLine +
        "</p>" +
        '<p class="min-pay-result-detail">Daily interest: <strong>' +
        fmtUSDPrecise(split.daily) +
        "</strong> · To principal: <strong>" +
        fmtUSD(split.principal) +
        "</strong> of your " +
        fmtUSD(payment) +
        " payment</p></div>" +
        buildInterestExplainerHTML(split);
    }

    if (cardsRoot) {
      cardsRoot.innerHTML = buildScenarioCardsHTML(balance, apr, payment, plan, whatIfs, split);
    }

    var whatIfHtml = whatIfs
      .map(function (scenario) {
        var interestSaved = plan.payoffPossible
          ? plan.interestPaid - scenario.interestPaid
          : null;
        var monthsSaved =
          plan.payoffPossible && Number.isFinite(plan.months)
            ? plan.months - scenario.months
            : null;
        var saveLine = "Compared with paying " + fmtUSD(payment) + "/month.";
        if (interestSaved !== null && interestSaved > 0) {
          saveLine =
            "You save <strong>" +
            fmtUSD(interestSaved) +
            "</strong> in total interest" +
            (monthsSaved !== null && monthsSaved > 0
              ? " and finish <strong>" +
                monthsSaved +
                " month" +
                (monthsSaved === 1 ? "" : "s") +
                " sooner</strong>."
              : ".");
        }

        return (
          '<article class="what-if-card">' +
          "<h3>Pay " +
          fmtUSD(scenario.newPayment) +
          "/month (+" +
          fmtUSD(scenario.increment) +
          ")</h3>" +
          "<p>Total interest: <strong>" +
          fmtUSD(scenario.interestPaid) +
          "</strong></p>" +
          "<p>Debt-free in <strong>" +
          formatPayoffDuration(scenario.months) +
          "</strong></p>" +
          "<p>" +
          saveLine +
          "</p></article>"
        );
      })
      .join("");

    var warnings = "";
    if (!plan.payoffPossible) {
      warnings +=
        '<p class="debt-result-warning"><strong>Why is total interest growing?</strong> Your payment (' +
        fmtUSD(payment) +
        ") does not cover month-one interest (" +
        fmtUSD(split.interest) +
        "). Unpaid interest is added to your balance, so next month's charge is higher. This is how revolving debt spirals—not a calculator bug. Pay at least <strong>" +
        fmtUSD(split.breakEvenPayment) +
        "/month</strong> to start reducing what you owe.</p>";
    } else if (plan.interestPaid > balance) {
      warnings +=
        '<p class="debt-result-warning">At this payment, total interest (<strong>' +
        fmtUSD(plan.interestPaid) +
        "</strong>) exceeds your original balance (<strong>" +
        fmtUSD(balance) +
        "</strong>). Even small payment increases save thousands.</p>";
    }

    var timelineHtml = "";
    if (plan.payoffPossible && plan.timeline.length) {
      var maxYearlyPayment = Math.max.apply(
        null,
        plan.timeline
          .map(function (row) {
            return row.principalPaid + row.interestPaid;
          })
          .concat([1])
      );
      var maxEndingBalance = Math.max.apply(
        null,
        plan.timeline
          .map(function (row) {
            return row.endingBalance;
          })
          .concat([1])
      );

      timelineHtml =
        '<h3 id="cc-int-result-heading" class="debt-timeline-heading">Year-by-year interest paid</h3>' +
        '<div class="debt-timeline-wrap">' +
        plan.timeline
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
              "<span>Interest: " +
              fmtUSD(row.interestPaid) +
              "</span>" +
              "<span>Principal: " +
              fmtUSD(row.principalPaid) +
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
        '<h2 class="what-if-title">What if you paid more each month?</h2>' +
        '<div class="what-if-grid">' +
        (whatIfHtml ||
          '<p>Raise your payment above month-one interest to see how much total interest you can avoid. Try the <a href="/debt/credit-cards/credit-card-payoff-calculator#payoff">payoff calculator</a> with a fixed amount you can sustain.</p>') +
        "</div>";
    }
  }

  form?.addEventListener("submit", function (event) {
    event.preventDefault();
    runCalculation();
  });

  form?.addEventListener("input", runCalculation);

  runCalculation();
})();
