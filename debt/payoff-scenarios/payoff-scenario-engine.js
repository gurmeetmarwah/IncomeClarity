(function (global) {
  const DEBT_TYPES = {
    "credit-card": { label: "Credit Card", apr: 22, hint: "Revolving APR—paying more than the minimum usually saves years of interest." },
    "personal-loan": { label: "Personal Loan", apr: 14, hint: "Fixed installment loans often have lower APR than cards but still reward extra payments." },
    medical: { label: "Medical Debt", apr: 8, hint: "Some medical balances are low- or no-interest—confirm your actual rate." },
    auto: { label: "Auto Loan", apr: 7, hint: "Auto loans amortize on a schedule; extra payments cut total interest." },
    student: { label: "Student Loan", apr: 6, hint: "Federal and private rates vary widely—use your servicer’s rate." },
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
    let principalPaid = 0;
    const monthlyBalances = [remaining];
    const schedule = [];

    if (remaining <= 0) {
      return {
        months: 0,
        interestPaid: 0,
        principalPaid: 0,
        payoffPossible: true,
        monthlyBalances: [0],
        schedule: [],
        yearly: [],
      };
    }

    while (remaining > 0.01 && months < 1200) {
      const interest = remaining * monthlyRate;
      const principal = Math.min(payment - interest, remaining);
      if (principal <= 0) {
        return {
          months: Infinity,
          interestPaid: Infinity,
          principalPaid: Infinity,
          payoffPossible: false,
          monthlyBalances,
          schedule,
          yearly: [],
        };
      }
      remaining -= principal;
      interestPaid += interest;
      principalPaid += principal;
      months += 1;
      remaining = Math.max(0, remaining);
      monthlyBalances.push(remaining);
      schedule.push({
        month: months,
        interest,
        principal,
        balance: remaining,
        payment: interest + principal,
      });
    }

    return {
      months,
      interestPaid,
      principalPaid,
      payoffPossible: true,
      monthlyBalances,
      schedule,
      yearly: buildYearlyBreakdown(schedule),
    };
  }

  function buildYearlyBreakdown(schedule) {
    if (!schedule.length) {
      return [];
    }
    const years = [];
    let bucket = { year: 1, principal: 0, interest: 0, endBalance: schedule[0].balance };

    schedule.forEach((row, index) => {
      bucket.principal += row.principal;
      bucket.interest += row.interest;
      bucket.endBalance = row.balance;
      const isYearEnd = (index + 1) % 12 === 0 || index === schedule.length - 1;
      if (isYearEnd) {
        years.push({
          year: bucket.year,
          label: "Year " + bucket.year,
          principal: bucket.principal,
          interest: bucket.interest,
          endBalance: bucket.endBalance,
          total: bucket.principal + bucket.interest,
        });
        bucket = { year: bucket.year + 1, principal: 0, interest: 0, endBalance: row.balance };
      }
    });

    return years;
  }

  function elId(prefix, suffix) {
    return prefix + "-" + suffix;
  }

  function initPayoffScenario(config) {
    const p = config.idPrefix;
    const defaults = {
      balance: config.defaultBalance,
      payment: config.defaultPayment,
      apr: 22,
    };

    const els = {
      balance: document.getElementById(elId(p, "balance")),
      apr: document.getElementById(elId(p, "apr")),
      aprRange: document.getElementById(elId(p, "apr-range")),
      payment: document.getElementById(elId(p, "payment")),
      paymentRange: document.getElementById(elId(p, "payment-range")),
      extra: document.getElementById(elId(p, "extra")),
      lump: document.getElementById(elId(p, "lump")),
      debtTypeCards: document.querySelectorAll("[data-debt-type]"),
      quickBalance: document.getElementById(elId(p, "quick-balance")),
      quickApr: document.getElementById(elId(p, "quick-apr")),
      quickPayment: document.getElementById(elId(p, "quick-payment")),
      quickForm: document.getElementById(elId(p, "quick-form")),
      heroPreview: document.getElementById(elId(p, "hero-preview")),
      results: {
        duration: document.getElementById(elId(p, "result-duration")),
        interest: document.getElementById(elId(p, "result-interest")),
        saved: document.getElementById(elId(p, "result-saved")),
        date: document.getElementById(elId(p, "result-date")),
        warning: document.getElementById(elId(p, "result-warning")),
      },
      quickResults: document.getElementById(elId(p, "quick-results")),
      timelineBar: document.getElementById(elId(p, "timeline-bar")),
      vizPanel: document.getElementById(elId(p, "viz-panel")),
      chartSummary: document.getElementById(elId(p, "chart-summary")),
      stackedChart: document.getElementById(elId(p, "stacked-chart")),
      timelineChart: document.getElementById(elId(p, "balance-chart")),
      chartInsight: document.getElementById(elId(p, "chart-insight")),
      whatIfGrid: document.getElementById(elId(p, "what-if-grid")),
      paymentTable: document.getElementById(elId(p, "payment-table-body")),
      budgetImpact: document.getElementById(elId(p, "budget-impact")),
      realisticGrid: document.getElementById(elId(p, "realistic-grid")),
    };

    let selectedDebtType = "credit-card";

    function readInputs() {
      const balance = Number(els.balance?.value) || defaults.balance;
      const apr = Number(els.apr?.value) || defaults.apr;
      const payment =
        (Number(els.payment?.value) || defaults.payment) + (Number(els.extra?.value) || 0);
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

    function splitSegmentHeights(totalPx, interestAmt, principalAmt, totalAmt) {
      if (!totalAmt || totalPx <= 0) {
        return { interestPx: 0, principalPx: 0 };
      }
      const minSlice = 14;
      let interestPx = Math.round((interestAmt / totalAmt) * totalPx);
      let principalPx = totalPx - interestPx;
      if (interestAmt > 0 && interestPx < minSlice) {
        interestPx = minSlice;
      }
      if (principalAmt > 0 && principalPx < minSlice) {
        principalPx = minSlice;
      }
      const sum = interestPx + principalPx;
      if (sum > totalPx) {
        const scale = totalPx / sum;
        interestPx = Math.round(interestPx * scale);
        principalPx = totalPx - interestPx;
      } else if (sum < totalPx) {
        principalPx += totalPx - sum;
      }
      return { interestPx, principalPx };
    }

    function renderStackedChart(yearly) {
      if (!els.stackedChart || !yearly.length) {
        return;
      }

      const chartMaxPx = 220;
      const maxTotal = Math.max(...yearly.map((y) => y.total), 1);
      const yAxisMaxLabel = fmtUSD(maxTotal);

      const bars = yearly
        .map((y, index) => {
          const barPx = Math.max(52, Math.round((y.total / maxTotal) * chartMaxPx));
          const { interestPx, principalPx } = splitSegmentHeights(
            barPx,
            y.interest,
            y.principal,
            y.total
          );
          const interestPct = y.total ? Math.round((y.interest / y.total) * 100) : 0;
          const principalPct = y.total ? 100 - interestPct : 0;
          const showInterestLabel = interestPx >= 22;
          const showPrincipalLabel = principalPx >= 22;

          return `
          <div class="sc5-bar-col" style="--sc5-bar-delay:${index * 60}ms">
            <div class="sc5-bar-track" title="Year ${y.year}: ${fmtUSD(y.principal)} principal, ${fmtUSD(y.interest)} interest">
              <div class="sc5-bar-stack" style="height:${barPx}px">
                <div class="sc5-bar-segment sc5-bar-segment--interest" style="height:${interestPx}px">
                  ${showInterestLabel ? `<span class="sc5-segment-label">${interestPct}%</span>` : ""}
                  <span class="sc5-segment-amt">${fmtUSD(y.interest)}</span>
                </div>
                <div class="sc5-bar-segment sc5-bar-segment--principal" style="height:${principalPx}px">
                  ${showPrincipalLabel ? `<span class="sc5-segment-label">${principalPct}%</span>` : ""}
                  <span class="sc5-segment-amt">${fmtUSD(y.principal)}</span>
                </div>
              </div>
            </div>
            <span class="sc5-bar-label">${y.label.replace("Year ", "Y")}</span>
            <span class="sc5-bar-total">${fmtUSD(y.total)} paid</span>
          </div>
        `;
        })
        .join("");

      els.stackedChart.innerHTML = `
      <div class="sc5-stacked-chart-wrap">
        <div class="sc5-stacked-yaxis" aria-hidden="true">
          <span>${yAxisMaxLabel}</span>
          <span>${fmtUSD(maxTotal / 2)}</span>
          <span>$0</span>
        </div>
        <div class="sc5-stacked-chart-inner" style="--sc5-chart-max:${chartMaxPx}px">${bars}</div>
      </div>
    `;
    }

    function renderBalanceChart(yearly, startBalance) {
      if (!els.timelineChart || !yearly.length) {
        return;
      }

      const points = [{ x: 0, y: startBalance, label: "Start" }];
      yearly.forEach((y) => {
        points.push({ x: y.year, y: y.endBalance, label: y.label });
      });

      const maxY = Math.max(startBalance, 1);
      const maxX = Math.max(points[points.length - 1].x, 1);
      const width = 320;
      const height = 140;
      const pad = { top: 12, right: 12, bottom: 28, left: 44 };
      const innerW = width - pad.left - pad.right;
      const innerH = height - pad.top - pad.bottom;

      function coord(pt) {
        return {
          sx: pad.left + (pt.x / maxX) * innerW,
          sy: pad.top + innerH - (pt.y / maxY) * innerH,
        };
      }

      const linePoints = points.map(coord);
      const linePath = linePoints.map((pt, i) => (i === 0 ? "M" : "L") + pt.sx + " " + pt.sy).join(" ");
      const areaPath =
        linePath +
        " L" +
        linePoints[linePoints.length - 1].sx +
        " " +
        (pad.top + innerH) +
        " L" +
        linePoints[0].sx +
        " " +
        (pad.top + innerH) +
        " Z";

      const dots = linePoints
        .map(
          (pt, i) =>
            `<circle class="sc5-balance-dot" cx="${pt.sx}" cy="${pt.sy}" r="4"><title>${points[i].label}: ${fmtUSD(points[i].y)}</title></circle>`
        )
        .join("");

      const yTicks = [0, maxY * 0.5, maxY]
        .map((val) => {
          const y = pad.top + innerH - (val / maxY) * innerH;
          return `
          <line class="sc5-grid-line" x1="${pad.left}" y1="${y}" x2="${width - pad.right}" y2="${y}"/>
          <text class="sc5-axis-label" x="${pad.left - 6}" y="${y + 4}" text-anchor="end">${fmtUSD(val)}</text>
        `;
        })
        .join("");

      const xLabels = points
        .filter((pt, i) => i === 0 || i === points.length - 1 || i % 2 === 0)
        .map((pt) => {
          const c = coord(pt);
          return `<text class="sc5-axis-label sc5-axis-label--x" x="${c.sx}" y="${height - 6}" text-anchor="middle">${pt.label.replace("Year ", "Y")}</text>`;
        })
        .join("");

      els.timelineChart.innerHTML = `
      <svg class="sc5-balance-svg" viewBox="0 0 ${width} ${height}" role="img" aria-label="Balance declining from ${fmtUSD(startBalance)} to zero">
        ${yTicks}
        <path class="sc5-balance-area" d="${areaPath}"/>
        <path class="sc5-balance-line" d="${linePath}"/>
        ${dots}
        ${xLabels}
      </svg>
    `;
    }

    function renderTimeline(plan, inputs) {
      if (els.timelineBar) {
        els.timelineBar.innerHTML = "";
      }
      if (els.vizPanel) {
        els.vizPanel.hidden = !plan.payoffPossible;
      }
      if (els.chartSummary) {
        els.chartSummary.innerHTML = "";
      }
      if (els.stackedChart) {
        els.stackedChart.innerHTML = "";
      }
      if (els.timelineChart) {
        els.timelineChart.innerHTML = "";
      }
      if (els.chartInsight) {
        els.chartInsight.textContent = "";
      }

      if (!plan.payoffPossible) {
        if (els.timelineBar) {
          els.timelineBar.innerHTML =
            '<p class="sc5-timeline-caption sc5-timeline-caption--warn">Raise your monthly payment to see a payoff chart.</p>';
        }
        return;
      }

      const total = plan.months;
      const startBalance = plan.monthlyBalances[0] || inputs.balance;
      const interestShare =
        plan.interestPaid + plan.principalPaid > 0
          ? Math.round((plan.interestPaid / (plan.interestPaid + plan.principalPaid)) * 100)
          : 0;

      if (els.timelineBar) {
        els.timelineBar.innerHTML = `
        <div class="sc5-timeline-track" role="img" aria-label="Payoff progress from month 1 to month ${total}">
          <span class="sc5-timeline-start">Month 1</span>
          <span class="sc5-timeline-fill" style="width:100%"></span>
          <span class="sc5-timeline-end">Month ${total}</span>
        </div>
        <p class="sc5-timeline-caption">Debt-free in <strong>${formatDuration(total)}</strong> at ${fmtUSD(inputs.payment)}/month · ${fmtUSD(plan.interestPaid)} interest total.</p>
      `;
      }

      if (els.chartSummary) {
        els.chartSummary.innerHTML = `
        <article class="sc5-summary-pill sc5-summary-pill--principal">
          <span class="sc5-summary-label">Principal paid</span>
          <strong class="sc5-summary-value">${fmtUSD(plan.principalPaid)}</strong>
        </article>
        <article class="sc5-summary-pill sc5-summary-pill--interest">
          <span class="sc5-summary-label">Interest paid</span>
          <strong class="sc5-summary-value">${fmtUSD(plan.interestPaid)}</strong>
        </article>
        <article class="sc5-summary-pill sc5-summary-pill--share">
          <span class="sc5-summary-label">Share to interest</span>
          <strong class="sc5-summary-value">${interestShare}%</strong>
        </article>
      `;
      }

      renderStackedChart(plan.yearly);
      renderBalanceChart(plan.yearly, startBalance);

      if (els.chartInsight && plan.yearly.length) {
        const firstYear = plan.yearly[0];
        const firstInterestShare = firstYear.total
          ? Math.round((firstYear.interest / firstYear.total) * 100)
          : 0;
        if (firstInterestShare >= 55) {
          els.chartInsight.innerHTML =
            "In <strong>year 1</strong>, about <strong>" +
            firstInterestShare +
            "%</strong> of your payment may go to interest—common on high-APR cards. Extra payments attack principal faster.";
        } else {
          els.chartInsight.innerHTML =
            "Your payment mix shifts toward <strong>principal</strong> as the balance falls—watch the green bars grow taller each year.";
        }
      }
    }

    function renderWhatIf(inputs) {
      if (!els.whatIfGrid) return;
      const base = payoffPlan(inputs.balance, inputs.apr, inputs.payment - (Number(els.extra?.value) || 0), {
        lumpSum: inputs.lump,
      });

      els.whatIfGrid.innerHTML = config.whatIf
        .map((c) => {
          const basePayment = inputs.payment - (Number(els.extra?.value) || 0);
          const payment = c.extra != null ? basePayment + c.extra : basePayment;
          const lump = c.lump != null ? c.lump : inputs.lump;
          const plan = payoffPlan(inputs.balance, inputs.apr, payment, { lumpSum: lump });
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
      els.paymentTable.innerHTML = config.paymentTablePayments
        .map((pay) => {
          const plan = payoffPlan(balance, apr, pay, {});
          return `
          <tr>
            <th scope="row">${fmtUSD(pay)}</th>
            <td>${plan.payoffPossible ? formatDuration(plan.months) : "—"}</td>
            <td>${plan.payoffPossible ? fmtUSD(plan.interestPaid) : "—"}</td>
          </tr>
        `;
        })
        .join("");
    }

    function renderRealistic(balance, apr) {
      if (!els.realisticGrid) return;
      els.realisticGrid.innerHTML = config.realistic
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
      const boosted = basePay + config.budgetBoost;
      const base = payoffPlan(inputs.balance, inputs.apr, basePay, { lumpSum: inputs.lump });
      const better = payoffPlan(inputs.balance, inputs.apr, boosted, { lumpSum: inputs.lump });
      if (base.payoffPossible && better.payoffPossible) {
        const monthsSaved = base.months - better.months;
        els.budgetImpact.innerHTML = `
        Paying an additional <strong>${fmtUSD(config.budgetBoost)}/month</strong> (${fmtUSD(boosted)} total) could help you become debt-free
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
      const baseNoExtra = payoffPlan(inputs.balance, inputs.apr, Number(els.payment?.value) || defaults.payment, {
        lumpSum: inputs.lump,
      });

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
      const hint = document.getElementById(elId(p, "debt-type-hint"));
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
      const balance = Number(els.quickBalance?.value) || defaults.balance;
      const apr = Number(els.quickApr?.value) || defaults.apr;
      const payment = Number(els.quickPayment?.value) || defaults.payment;
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
      document.getElementById(elId(p, "planner"))?.scrollIntoView({ behavior: "smooth", block: "start" });
    });

    document.querySelectorAll("[data-scroll-to]").forEach((btn) => {
      btn.addEventListener("click", () => {
        const id = btn.getAttribute("data-scroll-to");
        document.getElementById(id)?.scrollIntoView({ behavior: "smooth", block: "start" });
      });
    });

    applyDebtType("credit-card");
    if (els.balance) els.balance.value = defaults.balance;
    if (els.payment) els.payment.value = defaults.payment;
    if (els.extra) els.extra.value = 0;
    if (els.lump) els.lump.value = 0;
    renderResults();
  }

  global.IncomeClarityPayoffScenario = { init: initPayoffScenario };
})(typeof window !== "undefined" ? window : globalThis);
