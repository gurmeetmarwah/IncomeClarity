/**
 * Rent affordability calculator — hub page
 */
(function (global) {
  'use strict';

  var CITY_MULT = {
    austin: 1.0,
    dallas: 0.95,
    'new-york-city': 1.38,
    miami: 1.17,
    chicago: 1.05
  };

  function fmt(n) {
    return '$' + Math.round(n).toLocaleString('en-US');
  }

  function el(id) {
    return document.getElementById(id);
  }

  function num(id, fallback) {
    var node = el(id);
    if (!node) return fallback || 0;
    var v = parseFloat(node.value);
    return isNaN(v) ? (fallback || 0) : v;
  }

  function setBar(id, pct) {
    var node = el(id);
    if (node) node.style.width = Math.max(0, Math.min(100, pct)) + '%';
  }

  function setBarValue(id, pct) {
    var node = el(id);
    if (node) node.textContent = Math.round(Math.max(0, Math.min(100, pct))) + '%';
  }

  function setText(id, value) {
    var node = el(id);
    if (node) node.textContent = value;
  }

  function setWidth(id, pct) {
    var node = el(id);
    if (node) node.style.width = Math.max(0, Math.min(100, pct)) + '%';
  }

  function bindRentCalculator() {
    var form = el('ra-calc-form');
    if (!form) return;
    var netInput = el('ra-net');
    var incomeInput = el('ra-income');

    var baseline = {
      income: 95000,
      net: 5800,
      debt: 450,
      savePct: 15,
      transport: 300,
      family: 1,
      roommate: false,
      city: 'austin'
    };

    var scenario = {
      debtCut: 0,
      salaryBoost: 0,
      cityShift: 0
    };
    var netManuallyEdited = false;

    function estimatedNetFromIncome(income) {
      return (income / 12) * 0.73;
    }

    function syncNetFromIncome() {
      if (!incomeInput || !netInput || netManuallyEdited) return;
      netInput.value = Math.round(estimatedNetFromIncome(num('ra-income', 95000)));
    }

    function readBaselineFromForm() {
      baseline.income = num('ra-income', 95000);
      baseline.net = num('ra-net', 5800);
      baseline.debt = num('ra-debt', 450);
      baseline.savePct = num('ra-save', 15);
      baseline.transport = num('ra-transport', 300);
      baseline.family = num('ra-family', 1);
      baseline.roommate = el('ra-roommate') && el('ra-roommate').value === 'yes';
      baseline.city = el('ra-city') ? el('ra-city').value : 'austin';
    }

    function effectiveInputs() {
      var income = baseline.income + scenario.salaryBoost;
      var net = baseline.net;
      if (!netManuallyEdited) {
        net = estimatedNetFromIncome(income);
      } else if (scenario.salaryBoost) {
        // If user manually overrides take-home, still scale with salary scenarios.
        net = net + estimatedNetFromIncome(scenario.salaryBoost);
      }
      if (scenario.cityShift) {
        net = net * (1 + scenario.cityShift / 100);
      }
      if (!num('ra-net', 0) && el('ra-net')) {
        net = income / 12 * 0.73;
      }
      var debt = Math.max(0, baseline.debt - scenario.debtCut);
      var roommate = baseline.roommate;
      return {
        income: income,
        net: net,
        debt: debt,
        savePct: baseline.savePct / 100,
        transport: baseline.transport,
        family: baseline.family,
        roommate: roommate,
        city: baseline.city
      };
    }

    function calc() {
      readBaselineFromForm();
      var inp = effectiveInputs();
      var net = inp.net || inp.income / 12 * 0.73;
      var grossMonthly = inp.income / 12;
      var baseEss = 0.3 + Math.min(0.07, inp.family * 0.01) + Math.min(0.07, inp.transport / Math.max(1, net));
      var debtPct = inp.debt / Math.max(1, net);
      var comfortPct = Math.max(0.2, 1 - baseEss - inp.savePct - debtPct - 0.08);
      if (inp.roommate) comfortPct += 0.05;
      comfortPct = Math.min(0.4, comfortPct);
      var mult = CITY_MULT[inp.city] || 1;
      var comfortFromNet = net * comfortPct;
      var comfortFromGross = grossMonthly * 0.3;
      var comfort = Math.min(comfortFromNet, comfortFromGross) / mult;
      var low = comfort * 0.88;
      var high = comfort * 1.03;
      var stretch = comfort * 1.15;
      var risk = comfort * 1.35;

      var ranges = el('ra-ranges');
      if (ranges) {
        ranges.innerHTML =
          '<article class="ra-range ra-range--good">' +
            '<h4>Comfortable</h4><strong>' + fmt(low) + ' – ' + fmt(high) + '</strong>' +
            '<p>Room for savings and emergencies.</p></article>' +
          '<article class="ra-range ra-range--mid">' +
            '<h4>Stretch budget</h4><strong>' + fmt(stretch) + '</strong>' +
            '<p>Lower margin for surprises.</p></article>' +
          '<article class="ra-range ra-range--risk">' +
            '<h4>High risk</h4><strong>' + fmt(risk) + '+</strong>' +
            '<p>Higher stress and less flexibility.</p></article>';
      }

      var rentPct = Math.min(58, Math.max(10, (comfort / net) * 100));
      var saveShare = Math.round(inp.savePct * 100);
      var essShare = Math.round(baseEss * 100);
      var discShare = Math.max(0, 100 - rentPct - saveShare - essShare);

      setBar('bar-rent', rentPct);
      setBar('bar-save', saveShare);
      setBar('bar-ess', essShare);
      setBar('bar-disc', discShare);
      setBarValue('bar-rent-value', rentPct);
      setBarValue('bar-save-value', saveShare);
      setBarValue('bar-ess-value', essShare);
      setBarValue('bar-disc-value', discShare);

      var impactGood = el('impact-good');
      var impactRisk = el('impact-risk');
      if (impactGood) impactGood.textContent = fmt(high) + '/mo';
      if (impactRisk) impactRisk.textContent = fmt(risk) + '/mo';

      setBar('bb-rent', rentPct);
      setBar('bb-gro', Math.min(20, Math.round(10 + inp.family * 1.5)));
      setBar('bb-trans', Math.min(18, Math.round((inp.transport / Math.max(1, net)) * 100) + 3));
      setBar('bb-sav', saveShare);
      setBar('bb-debt', Math.min(22, Math.round(debtPct * 100)));
      setBar('bb-ent', Math.max(2, Math.round(discShare * 0.45)));
      setBarValue('bb-rent-value', rentPct);
      setBarValue('bb-gro-value', Math.min(20, Math.round(10 + inp.family * 1.5)));
      setBarValue('bb-trans-value', Math.min(18, Math.round((inp.transport / Math.max(1, net)) * 100) + 3));
      setBarValue('bb-sav-value', saveShare);
      setBarValue('bb-debt-value', Math.min(22, Math.round(debtPct * 100)));
      setBarValue('bb-ent-value', Math.max(2, Math.round(discShare * 0.45)));
      setText('scenario-comfort', fmt(low) + ' - ' + fmt(high));
      setText('scenario-stretch', fmt(stretch) + '/mo');
      setText('scenario-risk', fmt(risk) + '+/mo');
      setText('scenario-rent-share', Math.round(rentPct) + '%');

      var summary = el('ra-summary');
      if (summary) {
        summary.textContent = 'Based on ' + fmt(grossMonthly) + '/mo gross and ' + fmt(net) + '/mo take-home, a comfortable rent target is about ' +
          fmt(low) + ' to ' + fmt(high) + ' in your selected city.';
      }

      updateScenarioVisuals();
    }

    function updateScenarioVisuals() {
      var baseDebt = baseline.debt;
      var cut = Math.min(scenario.debtCut, baseDebt);
      var afterDebt = Math.max(0, baseDebt - cut);
      var remainPct = baseDebt > 0 ? (afterDebt / baseDebt) * 100 : 100;

      setText('w-debt-value', '−' + fmt(cut) + '/mo');
      setText('w-debt-before', fmt(baseDebt) + '/mo');
      setText('w-debt-after', fmt(afterDebt) + '/mo');
      setWidth('w-debt-remain-bar', remainPct);
      setWidth('w-debt-cut-bar', 100 - remainPct);

      var wDebt = el('w-debt');
      if (wDebt && baseDebt > 0) {
        var debtMax = Math.max(25, Math.ceil(baseDebt / 25) * 25);
        wDebt.max = String(debtMax);
        if (+wDebt.value > baseDebt) {
          wDebt.value = String(baseDebt);
          scenario.debtCut = baseDebt;
        }
      }

      setWidth('w-salary-fill', (scenario.salaryBoost / 30000) * 100);
      setText('w-salary-value', '+' + fmt(scenario.salaryBoost) + '/yr');

      var city = scenario.cityShift;
      setWidth('w-city-fill-down', city < 0 ? (Math.abs(city) / 20) * 100 : 0);
      setWidth('w-city-fill-up', city > 0 ? (city / 25) * 100 : 0);
      var cityLabel = el('w-city-value');
      if (cityLabel) {
        cityLabel.textContent = (city > 0 ? '+' : '') + city + '%';
        cityLabel.className = 'ra-scenario-delta' +
          (city < 0 ? ' ra-scenario-delta--down' : city > 0 ? ' ra-scenario-delta--up' : '');
      }
    }

    form.addEventListener('submit', function (e) {
      e.preventDefault();
      scenario = { debtCut: 0, salaryBoost: 0, cityShift: 0 };
      ['w-debt', 'w-salary', 'w-city'].forEach(function (id) {
        var s = el(id);
        if (s) s.value = 0;
      });
      if (!netManuallyEdited) {
        syncNetFromIncome();
      }
      calc();
    });

    var btn = el('ra-calc-btn');
    if (btn) btn.addEventListener('click', function (e) {
      e.preventDefault();
      calc();
    });

    if (incomeInput) {
      incomeInput.addEventListener('input', function () {
        netManuallyEdited = false;
        syncNetFromIncome();
        calc();
      });
      incomeInput.addEventListener('change', function () {
        netManuallyEdited = false;
        syncNetFromIncome();
        calc();
      });
    }

    if (netInput) {
      netInput.addEventListener('input', function () {
        var raw = netInput.value.trim();
        netManuallyEdited = raw !== '';
        calc();
      });
      netInput.addEventListener('change', function () {
        var raw = netInput.value.trim();
        netManuallyEdited = raw !== '';
        calc();
      });
    }

    ['ra-debt', 'ra-city', 'ra-save', 'ra-roommate', 'ra-family', 'ra-transport'].forEach(function (id) {
      var node = el(id);
      if (node) node.addEventListener('input', calc);
      if (node) node.addEventListener('change', calc);
    });

    var wDebt = el('w-debt');
    if (wDebt) wDebt.addEventListener('input', function () {
      scenario.debtCut = +wDebt.value || 0;
      calc();
    });
    var wSal = el('w-salary');
    if (wSal) wSal.addEventListener('input', function () {
      scenario.salaryBoost = +wSal.value || 0;
      calc();
    });
    var wCity = el('w-city');
    if (wCity) wCity.addEventListener('input', function () {
      scenario.cityShift = +wCity.value || 0;
      calc();
    });

    syncNetFromIncome();
    calc();
  }

  function init() {
    bindRentCalculator();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }

  global.RentAfford = { fmt: fmt, calc: bindRentCalculator };
})(typeof window !== 'undefined' ? window : this);
