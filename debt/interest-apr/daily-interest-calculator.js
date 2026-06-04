(function () {
  "use strict";

  const fmt = (n) =>
    new Intl.NumberFormat("en-US", {
      style: "currency",
      currency: "USD",
      minimumFractionDigits: 2,
      maximumFractionDigits: 2,
    }).format(n);

  const fmtPct = (n) => n.toFixed(2) + "%";

  function num(id) {
    return Math.max(0, parseFloat(document.getElementById(id)?.value) || 0);
  }

  function isCompound() {
    return document.querySelector('input[name="dic-mode"]:checked')?.value === "compound";
  }

  function calcSimple(principal, apr, days) {
    const dailyRate = apr / 100 / 365;
    const dailyInterest = principal * dailyRate;
    const periodInterest = dailyInterest * days;
    const ending = principal + periodInterest;
    return {
      dailyInterest,
      periodInterest,
      ending,
      effectiveApr: apr,
      balances: milestoneBalances(principal, apr, days, false),
    };
  }

  function calcCompound(principal, apr, days) {
    const r = apr / 100 / 365;
    const dailyInterest = principal * r;
    const ending = principal * Math.pow(1 + r, days);
    const periodInterest = ending - principal;
    const effectiveApr = (Math.pow(1 + r, 365) - 1) * 100;
    return {
      dailyInterest,
      periodInterest,
      ending,
      effectiveApr,
      balances: milestoneBalances(principal, apr, days, true),
    };
  }

  function milestoneBalances(principal, apr, days, compound) {
    const r = apr / 100 / 365;
    const points = [1, 7, Math.max(1, days)];
    const unique = [...new Set(points)].sort((a, b) => a - b);
    return unique.map((d) => {
      let bal;
      if (compound) {
        bal = principal * Math.pow(1 + r, d);
      } else {
        bal = principal + principal * r * d;
      }
      return { day: d, balance: bal };
    });
  }

  function render() {
    const principal = num("dic-principal");
    const apr = num("dic-apr");
    const days = Math.max(1, Math.round(num("dic-days")));
    const compound = isCompound();

    const result = compound
      ? calcCompound(principal, apr, days)
      : calcSimple(principal, apr, days);

    const set = (id, text) => {
      const el = document.getElementById(id);
      if (el) el.textContent = text;
    };

    set("dic-daily", fmt(result.dailyInterest) + "/day");
    set("dic-period", fmt(result.periodInterest));
    set("dic-effective", fmtPct(result.effectiveApr));
    set("dic-ending", fmt(result.ending));

    const formulaDaily = document.getElementById("dic-formula-daily");
    const formulaExample = document.getElementById("dic-formula-example");
    if (formulaDaily) {
      formulaDaily.textContent = fmtPct((apr / 365) * 100) + " per day";
    }
    if (formulaExample) {
      formulaExample.textContent = fmt(result.dailyInterest) + "/day";
    }

    const progression = document.getElementById("dic-progression");
    if (progression) {
      progression.innerHTML = result.balances
        .map(
          (p) => `
        <div class="dic-progress-step">
          <span class="dic-progress-day">Day ${p.day}</span>
          <strong class="dic-progress-bal">${fmt(p.balance)}</strong>
        </div>`
        )
        .join("");
    }

    const bar = document.getElementById("dic-progress-bar");
    if (bar && result.balances.length) {
      const max = result.balances[result.balances.length - 1].balance;
      const min = principal;
      bar.innerHTML = result.balances
        .map((p) => {
          const pct = max > min ? ((p.balance - min) / (max - min)) * 100 : 0;
          return `<div class="dic-progress-bar__seg" style="--dic-h:${Math.max(12, pct)}%" title="Day ${p.day}: ${fmt(p.balance)}"><span>Day ${p.day}</span></div>`;
        })
        .join("");
    }

    document.getElementById("dic-results")?.removeAttribute("hidden");
  }

  function applyExample(principal, apr, days, compound) {
    document.getElementById("dic-principal").value = principal;
    document.getElementById("dic-apr").value = apr;
    document.getElementById("dic-days").value = days;
    const mode = compound ? "compound" : "simple";
    const radio = document.querySelector(`input[name="dic-mode"][value="${mode}"]`);
    if (radio) radio.checked = true;
    render();
  }

  document.getElementById("dic-form")?.addEventListener("submit", (e) => {
    e.preventDefault();
    render();
  });

  document.querySelectorAll('input[name="dic-mode"]').forEach((r) => {
    r.addEventListener("change", render);
  });

  ["dic-principal", "dic-apr", "dic-days"].forEach((id) => {
    document.getElementById(id)?.addEventListener("input", render);
  });

  document.querySelectorAll("[data-dic-example]").forEach((btn) => {
    btn.addEventListener("click", () => {
      applyExample(
        Number(btn.dataset.principal),
        Number(btn.dataset.apr),
        Number(btn.dataset.days || 30),
        btn.dataset.compound === "true"
      );
      document.getElementById("dic-calc")?.scrollIntoView({ behavior: "smooth", block: "start" });
    });
  });

  document.querySelectorAll("[data-scroll-to]").forEach((btn) => {
    btn.addEventListener("click", () => {
      document.getElementById(btn.getAttribute("data-scroll-to"))?.scrollIntoView({
        behavior: "smooth",
        block: "start",
      });
    });
  });

  document.getElementById("dic-recalc")?.addEventListener("click", () => {
    document.getElementById("dic-calc")?.scrollIntoView({ behavior: "smooth", block: "start" });
  });

  render();
})();
